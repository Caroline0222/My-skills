# My Skills

Agent skills I use in daily cross-border project work. Each skill is a self-contained folder with a `SKILL.md`, a `references/` library, and sample outputs. Written for WorkBuddy and Claude Code; the format is portable to any agent that reads `SKILL.md`.

---

## Skills

| Skill | What it does | Version |
|-------|-------------|---------|
| **[email-master](skills/email-master/)** | Drafts and rewrites cross-border business email for clients, vendors, and internal teams, in English or Chinese. Routes by recipient tier, applies escalation rules to governance email, and scales output depth to the message: full package for high-stakes, a single note for short correspondence. 15 bilingual cases and an optional pre-send linter. | v8.2 |
| **[interview-coach](skills/interview-coach/)** | Turns a job description, a resume, and company research into a structured six-chapter interview playbook, from positioning and evidence to likely follow-up questions and round-by-round actions. | v4.4 |

---

## Install

Install one skill through the skills CLI:

```bash
npx skills add Caroline0222/My-skills --skill email-master
```

Install everything:

```bash
npx skills add Caroline0222/My-skills
```

Or copy a folder manually:

```bash
cp -r skills/email-master ~/.workbuddy/skills/
cp -r skills/email-master ~/.claude/skills/
```

---

## Usage

1. Install a skill, or copy its folder into your agent's skills directory.
2. Restart the agent so it picks up the new skill.
3. Describe the task in plain language. The skill triggers on its own.

Example prompts for `email-master`:

- *"A client is requesting new features during UAT while keeping next Friday's go-live date."*
- *"Communicate a 5-day launch delay to an executive with business impact and mitigation options."*
- *"Send a formal reminder to a vendor after two missed deadlines."*

---

## Repository structure

```
My-skills/
├── skills/
│   ├── email-master/              # SKILL.md + references/ + scripts/
│   └── interview-coach/           # SKILL.md + references/ + assets/
├── samples/
│   └── interview-coach/           # Sample playbooks and screenshots
├── publish.sh                     # Release helper
├── README.md
└── LICENSE
```

Each skill folder follows the same layout:

```
skill-name/
├── SKILL.md          # Rules and routing (required)
├── README.md         # Overview for humans
├── references/       # Detail loaded on demand
├── scripts/          # Optional deterministic checks
├── assets/           # Templates
└── samples/          # Example outputs, where relevant
```

---

## email-master

Cross-border business email is a governance problem before it is a writing problem. A single sentence can concede scope, imply consent, or promise a date nobody agreed to. This skill handles the writing and the exposure at the same time.

What it changes in practice:

| Behaviour | Effect |
|-----------|--------|
| **Audience routing** | Four modes (external client, internal peer or vendor, upward escalation, short relational correspondence), each with its own register, structure, and salutation rules. |
| **Governance gates** | 13 gates covering delay notices, vendor escalation, verbal-to-written confirmation, scope change and cost, complaint response, and concessions. |
| **Hard constraints** | No invented dates or amounts, body length by mode (120–180 words for governance, 60–120 for short notes), dual timezone, currency with tax basis, one bolded element per paragraph, and a banned-phrase list. |
| **Send-out package** | Three subject lines, the body, a short IM ping, and a pre-send check that includes a forwardability test. |
| **Pre-send linter** | `scripts/lint.py` checks the mechanical rules: banned phrases, length against the mode range, amounts without a currency, dates without a timezone, silent-consent wording, and enumerations in the wrong mode. |

The reference library holds 15 cases, each with an English and a Chinese version of the same email, covering scope additions, active and passive delays, vendor escalation, cross-team asks, deadline pushback, and post-launch credit.

```bash
python3 skills/email-master/scripts/lint.py draft.txt --mode A
```

---

## interview-coach

Interview preparation reduces to six questions. The skill answers them in order, so a candidate walks in with a position rather than a list of tips.

| Chapter | Question it answers |
|---------|---------------------|
| **A — Understand the opportunity** | What is this company and this role actually about? |
| **B — My positioning** | Why is this candidate a match? |
| **C — Evidence and stories** | Which experiences back up the claims? |
| **D — Prep and deep dive** | What will the interviewer press on, and how should it be prepared? |
| **E — Fit and practice** | What does each round look like, and how is a case broken down? |
| **F — Final execution** | What to do before, during, and after the interview? |

Built for Product, Operations, Sales, HR, Finance, Tech, Design, Legal, and Project Management roles. Sample playbooks are in [samples/interview-coach/](samples/interview-coach/).

---

## License

MIT
