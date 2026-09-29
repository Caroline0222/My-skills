# Interview Coach · 面试陪练

An AI workflow skill that turns JD + resume + company info into a structured 6-chapter interview prep playbook.

Works across industries: **Product / Operations / Sales / HR / Finance / Tech / Design / Legal / Project Management**.

---

## What It Is

An open-source AI tool. **No fabrication. No exaggeration. No empty talk. Asks before assuming when info is missing.**

> 一个开源的 AI 工具。**不虚构 · 不夸大 · 不写空话 · 信息不足会先追问**。

Feed it your JD, resume, and target company — get back a 6-chapter playbook:

| Chapter | Question It Answers / 回答的问题 |
|---------|-------------------------------|
| **A — Understand the Opportunity** | What is this company and role really about? / 这家公司和岗位到底是什么 |
| **B — My Positioning** | Why am I a match for this role? / 我跟这个岗位为什么匹配 |
| **C — Evidence + Stories** | Which experiences back up my claims? / 我有哪些经历能接住这个问题 |
| **D — Prep + Deep Dive** | What will the interviewer press on, and how do I prep? / 面试官会怎么追问，我提前怎么答 |
| **E — Fit + Practice** | What does each round look like? How do I crack a case? / 几轮面试准备什么、Case 怎么拆 |
| **F — Final Execution** | Concrete actions before / during / after the interview / 面前面中面后的具体动作 |

---

## Repository Layout

```
My-skills/
├── README.md
├── LICENSE
├── interview-coach/                         # The skill
│   ├── SKILL.md                             # Main entry point
│   ├── references/                          # 9 workflow docs
│   │   ├── info-gathering.md                # 信息收集与追问
│   │   ├── jd-parsing.md                    # JD 拆解
│   │   ├── company-research.md              # 公司调研
│   │   ├── candidate-positioning.md         # 候选人定位
│   │   ├── evidence-and-stories.md          # 证据与故事
│   │   ├── prep-and-deep-dive.md            # 准备与深挖
│   │   ├── interview-formats.md             # 面试形式
│   │   ├── execution-checklist.md           # 执行清单
│   │   └── anti-ai-style.md                 # 去 AI 味
│   └── assets/
│       └── cards-template.html              # 金秋配色弹药库模板
├── 面试陪练-样例输出-v4.4.html             # Sample: PM (林青 → 智聘 AI)
├── 面试陪练-样例-张可欣-华泰国际.html      # Sample: BA (fictional)
└── 样例截图-华泰国际-首屏.png              # Header preview image
```

---

## Sample Preview

![Header preview](./样例截图-华泰国际-首屏.png)

Open the `.html` files locally in a browser to view the full playbook.

---

## How to Use

### In WorkBuddy

1. Copy the `interview-coach/` folder to `~/.workbuddy/skills/`
2. Restart WorkBuddy
3. In chat, say "use 面试陪练 to prep me for [company] [role]" and attach JD + resume

### Standalone

- `SKILL.md` — main entry point, follow the workflow described there
- `references/` — step-by-step guidance for each chapter
- `assets/cards-template.html` — visual template for the final output

---

## License

MIT