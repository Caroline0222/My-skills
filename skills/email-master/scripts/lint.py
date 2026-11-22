#!/usr/bin/env python3
"""Pre-send linter for email-master.

Checks only what a machine can check. Judgement calls stay with SKILL.md.

    python3 scripts/lint.py draft.txt
    python3 scripts/lint.py draft.txt --mode A
    cat draft.txt | python3 scripts/lint.py -
    python3 scripts/lint.py draft.txt --json

Exit codes: 0 clean or warnings only, 1 errors found, 2 bad input.

Stdlib only. No network, no state, no writes.
"""

import argparse
import json
import re
import sys

# --- Phase 4.7, always banned ---------------------------------------------

BLACKLIST = [
    r"we refer to",
    r"please be advised",
    r"kindly",
    r"please revert",
    r"please do the needful",
    r"as per my last email",
    r"as per our conversation",
    r"i hope this email finds you well",
    r"loop(?:ing)? in",
    r"circle back",
    r"quick heads?-up",
    r"hop on a (?:quick )?call",
    r"jump on a (?:quick )?call",
    r"as a gesture of goodwill",
    r"敬请悉知",
    r"恳请批示",
    r"赋能",
    r"抓手",
    r"闭环",
]

# --- 1.3, banned in Mode D only -------------------------------------------

D_BANNED = [
    r"please find",
    r"as mentioned",
]

D_AUDIT_VERBS = [
    r"\bcheck (?:the|your|whether)",
    r"\bverify\b",
    r"\bvalidate\b",
    r"confirm the split",
]

# --- Phase 4.8, labelling forbidden in A and D ----------------------------

LABELS = [
    r"action required",
    r"for information",
    r"option [abc]\b",
    r"\bfirst[,:.]",
    r"\bsecond[,:.]",
    r"\bthird[,:.]",
]

# --- Gate 1 / Gate 13, absolute promises ----------------------------------

ABSOLUTES = [
    r"zero risk",
    r"100%\s*(?:safe|secure|reliable|guaranteed|bug[- ]free)",
    r"guarantee[ds]?\b",
    r"bug[- ]free",
    r"will not fail",
    r"risk[- ]free",
]

SILENT_CONSENT = [
    r"if we (?:do not|don't) hear (?:back|from you)",
    r"if no (?:response|reply|objection)",
    r"in the absence of (?:a )?(?:response|reply|objection)",
    r"unless we hear otherwise",
]

VAGUE_TIME = [
    r"as soon as possible",
    r"\bASAP\b",
    r"at your earliest convenience",
    r"\bEOD\b",
    r"\bCOB\b",
    r"in the coming days",
    r"\bshortly\b",
]

CURRENCY = re.compile(
    r"\b(?:HKD|SGD|USD|CNY|RMB|MYR|THB|IDR|PHP|VND|EUR|GBP|AUD|NZD|JPY|KRW"
    r"|TWD|NTD|CHF|INR|AED|SAR)\b|[$€£¥₹]|元|港[币幣]|美元|人民币"
)
MONEY = re.compile(
    r"(?<![\w/.,])(?:[A-Z]{3}\s*)?("
    r"\d{1,3}(?:,\d{3})+(?:\.\d+)?"
    r"|\d+(?:\.\d+)?\s*[kKmM]\b"
    r"|\d+\s*[万萬千]"
    r"|\d{5,}(?:\.\d+)?"
    r")(?![\d,])"
)
PHONE = re.compile(r"\+?\d[\d\s().\-]{5,}\d")
MONEY_UNIT = re.compile(
    r"^\s*(?:users?|licen[cs]es?|man[- ]days?|days?|weeks?|months?|hours?"
    r"|people|resources?|modules?|records?|items?|seats?|tickets?|calls?"
    r"|requests?|transactions?|万|人天|个|台|条|次)",
    re.I,
)

MONTHS = (r"Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec"
          r"|January|February|March|April|June|July|August|September"
          r"|October|November|December")
DATE = re.compile(
    rf"\b(?:{MONTHS})[a-z]*\.?\s+\d{{1,2}}(?!\d)"
    rf"|\b\d{{1,2}}\s+(?:{MONTHS})\b"
    r"|\b\d{1,2}/\d{1,2}(?:/\d{2,4})?\b"
)
TZ = re.compile(
    r"\b(?:HKT|SGT|EST|EDT|CST|PST|PDT|MST|MDT|GMT|UTC|ICT|JST|KST"
    r"|AEST|AEDT|BST|CET|CEST|IST)\b|[+-]\d{1,2}(?::?\d{2})?"
)

SALUTATION = re.compile(r"^\s*(?:Dear|Hi|Hello|Hey|亲爱的|您好)\b", re.I)
SIGNOFF = re.compile(
    r"^\s*(Best regards|Kind regards|Warm regards|Best|Regards|Sincerely"
    r"|Yours sincerely|Thanks|Thank you|Many thanks|Cheers"
    r"|顺颂商祺|祝好|此致|敬礼)[,，]?\s*$",
    re.I,
)
BOLD = re.compile(r"\*\*[^*\n]+\*\*")
LISTY = re.compile(r"^\s*(?:#{1,6}\s|[-•*]\s|\d+[.)]\s)")
EMAIL_ADDR = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
AT_MENTION = re.compile(r"(?<![\w.@])@[A-Za-z][\w.-]*")
CJK = re.compile(r"[\u4e00-\u9fff]")

LENGTH = {"A": (120, 220), "B": (120, 220), "C": (120, 220), "D": (60, 120)}


class Hit:
    __slots__ = ("line", "severity", "rule", "detail")

    def __init__(self, line, severity, rule, detail):
        self.line = line
        self.severity = severity
        self.rule = rule
        self.detail = detail

    def as_dict(self):
        return {"line": self.line, "severity": self.severity,
                "rule": self.rule, "detail": self.detail}


def sentences(text):
    """Yield (offset, sentence). Splits on . ! ? and newlines, keeps CJK stops."""
    for m in re.finditer(r"[^.!?。！？\n]+[.!?。！？]?", text):
        if m.group().strip():
            yield m.start(), m.group()


def line_of(text, offset):
    return text.count("\n", 0, offset) + 1


def mask_phones(text):
    """Blank phone-number spans so they are not read as amounts. Same length."""
    out = list(text)
    for m in PHONE.finditer(text):
        span = m.group()
        if sum(c.isdigit() for c in span) < 8:
            continue
        for i in range(m.start(), m.end()):
            if out[i] != "\n":
                out[i] = " "
    return "".join(out)


def split_body(text):
    """Return (body_lines, has_signoff, closing_word)."""
    lines = text.split("\n")
    closing = None
    for i in range(len(lines) - 1, -1, -1):
        m = SIGNOFF.match(lines[i])
        if m:
            closing = m.group(1)
            return lines[:i], True, closing
    return lines, False, None


def word_count(text, lang):
    if lang == "zh" or len(CJK.findall(text)) > len(re.findall(r"[A-Za-z']+", text)):
        return len(CJK.findall(text)), "chars"
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'\-]*", text)), "words"


def lint(text, mode=None, lang="en"):
    hits = []
    lines = text.split("\n")

    body_lines, has_signoff, closing = split_body(text)
    body = "\n".join(body_lines)
    salutation_end = 0
    for i, ln in enumerate(body_lines):
        if SALUTATION.match(ln):
            salutation_end = i + 1
            break
    core = "\n".join(body_lines[salutation_end:])

    n, unit = word_count(core, lang)
    if mode is None:
        mode = "D" if n <= 120 else "A"
        inferred = True
    else:
        inferred = False

    # 1. blacklist, always
    for pat in BLACKLIST:
        for m in re.finditer(pat, text, re.I):
            hits.append(Hit(line_of(text, m.start()), "error", "blacklist",
                            f'"{m.group(0)}" (Phase 4.7)'))

    # 2. mode-scoped register rules
    if mode in ("A", "D"):
        for pat in LABELS + [r"two things"]:
            for m in re.finditer(pat, text, re.I):
                hits.append(Hit(line_of(text, m.start()), "error", "enumeration",
                                f'"{m.group(0)}" is labelling — Mode {mode} carries priority '
                                f"by order and paragraph weight (4.8)"))
        for i, ln in enumerate(body_lines, 1):
            if LISTY.match(ln):
                sev = "error" if mode == "D" else "warning"
                hits.append(Hit(i, sev, "enumeration",
                                f"structured list in Mode {mode} — priority should read as prose (4.8)"))

    if mode == "D":
        for pat in D_BANNED:
            for m in re.finditer(pat, text, re.I):
                hits.append(Hit(line_of(text, m.start()), "error", "mode D register",
                                f'"{m.group(0)}" is banned in Mode D (1.3)'))
        for pat in D_AUDIT_VERBS:
            for m in re.finditer(pat, text, re.I):
                hits.append(Hit(line_of(text, m.start()), "warning", "mode D register",
                                f'"{m.group(0)}" reads as an audit of a non-vendor (1.3)'))

    # 3. absolutes and silent consent, one line per rule
    def grouped(pats, severity, rule, note):
        by_line = {}
        for pat in pats:
            for m in re.finditer(pat, text, re.I):
                ln = line_of(text, m.start())
                by_line.setdefault(ln, [])
                term = m.group(0).strip()
                if term.lower() not in (t.lower() for t in by_line[ln]):
                    by_line[ln].append(term)
        for ln, terms in sorted(by_line.items()):
            found = ", ".join(f'"{t}"' for t in terms)
            hits.append(Hit(ln, severity, rule, f"{found} — {note}"))

    grouped(ABSOLUTES, "warning", "absolute claim",
            'use "keep risk within acceptable thresholds" (Gate 1)')
    grouped(SILENT_CONSENT, "error", "silent consent",
            "assumes agreement; require written confirmation (Gate 4)")

    # 4. vague timelines
    for pat in VAGUE_TIME:
        for m in re.finditer(pat, text, re.I):
            hits.append(Hit(line_of(text, m.start()), "warning", "vague deadline",
                            f'"{m.group(0)}" — name a date and a timezone'))

    # 5. money without a currency code
    masked = mask_phones(text)
    for off, s in sentences(masked):
        if CURRENCY.search(s):
            continue
        for m in MONEY.finditer(s):
            tail = s[m.end():m.end() + 24]
            if MONEY_UNIT.match(tail):
                continue
            hits.append(Hit(line_of(text, off + m.start()), "warning", "money",
                            f'"{m.group(0).strip()}" has no currency code and tax basis (4.4)'))
            break

    # 6. date without timezone (references to a past note are not deadlines)
    REF_PAST = re.compile(r"(?:note|letter|e-?mail|message|reply|call)\s+(?:of|dated|sent on|from)\s*$",
                          re.I)
    for off, s in sentences(text):
        m = DATE.search(s)
        if not m or TZ.search(s):
            continue
        if REF_PAST.search(s[max(0, m.start() - 30):m.start()]):
            continue
        hits.append(Hit(line_of(text, off + m.start()), "warning", "timezone",
                        f'"{m.group(0)}" carries no timezone (4.3)'))

    # 7. bold density
    core_off = text.find(core) if core else 0
    core_off = max(core_off, 0)
    for m in re.finditer(r"(?:[^\n]|\n(?!\s*\n))+", core):
        bolds = len(BOLD.findall(m.group()))
        if bolds > 1:
            hits.append(Hit(line_of(text, core_off + m.start()), "warning", "bold",
                            f"{bolds} bolded elements in one paragraph (4.6)"))

    # 8. @ in the body
    stripped = EMAIL_ADDR.sub("", core)
    for m in AT_MENTION.finditer(stripped):
        hits.append(Hit(line_of(text, m.start()), "error", "addressing",
                        f'"{m.group(0)}" — use Name (Team): deliverable (1.3)'))

    # 9. length
    lo, hi = LENGTH[mode]
    if not (lo <= n <= hi):
        sev = "warning" if n < lo else "error"
        why = f"below the {lo} floor — do not pad, but check nothing is missing" \
            if n < lo else f"over the {hi} ceiling — cut, do not compress (4.2)"
        hits.append(Hit(0, sev, "length", f"{n} {unit} in Mode {mode} (range {lo}-{hi}); {why}"))

    # 10. sign-off
    if not has_signoff:
        hits.append(Hit(len(lines), "error", "sign-off", "no closing line found (4.5)"))
    elif mode == "A" and closing and closing.lower().strip() == "thanks":
        hits.append(Hit(len(lines), "error", "sign-off",
                        'never "Thanks" alone to a client (4.5)'))

    # 11. placeholders
    tbc = len(re.findall(r"\[TBC\]|\[待确认\]", text, re.I))
    if tbc:
        hits.append(Hit(0, "warning", "placeholder",
                        f"{tbc} × [TBC] — list every one in the Governance Check (4.1)"))

    # 12. "as agreed" needs evidence
    for m in re.finditer(r"\bas agreed\b", text, re.I):
        hits.append(Hit(line_of(text, m.start()), "warning", "as agreed",
                        "only valid where written evidence of mutual acceptance exists (Gate 4)"))

    hits.sort(key=lambda h: (h.line, h.rule))
    return hits, mode, inferred, n, unit


def render(hits, mode, inferred, n, unit, path):
    head = f"{path} · Mode {mode}{' (inferred)' if inferred else ''} · {n} {unit}"
    print(head)
    print("─" * len(head))
    if not hits:
        print("✓ clean")
    for h in hits:
        mark = "✗" if h.severity == "error" else "⚠"
        loc = f"{h.line:>4}" if h.line else "   —"
        print(f"{mark} {loc}  {h.rule:<18} {h.detail}")
    errs = sum(1 for h in hits if h.severity == "error")
    warns = len(hits) - errs
    print("─" * len(head))
    print(f"{errs} error{'s' if errs != 1 else ''} · {warns} warning{'s' if warns != 1 else ''}")
    return errs


def main():
    ap = argparse.ArgumentParser(description="Pre-send linter for email-master.")
    ap.add_argument("file", help="path to the draft, or - for stdin")
    ap.add_argument("--mode", choices=list(LENGTH), help="A/B/C/D; omit to infer")
    ap.add_argument("--lang", choices=["en", "zh"], default="en")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--strict", action="store_true", help="warnings also fail the run")
    a = ap.parse_args()

    if a.file == "-":
        text = sys.stdin.read()
        path = "<stdin>"
    else:
        try:
            with open(a.file, encoding="utf-8") as f:
                text = f.read()
        except OSError as e:
            print(f"cannot read {a.file}: {e}", file=sys.stderr)
            return 2
        path = a.file

    if not text.strip():
        print("empty input", file=sys.stderr)
        return 2

    hits, mode, inferred, n, unit = lint(text, a.mode, a.lang)

    if a.json:
        print(json.dumps({
            "file": path, "mode": mode, "inferred": inferred,
            "length": n, "unit": unit,
            "errors": sum(1 for h in hits if h.severity == "error"),
            "warnings": sum(1 for h in hits if h.severity == "warning"),
            "findings": [h.as_dict() for h in hits],
        }, ensure_ascii=False, indent=2))
        return 1 if any(h.severity == "error" for h in hits) else 0

    errs = render(hits, mode, inferred, n, unit, path)
    if errs:
        return 1
    return 1 if (a.strict and hits) else 0


if __name__ == "__main__":
    sys.exit(main())
