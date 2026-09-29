# My Skills · 我的 Skill 合集

A collection of AI workflow skills I built and use daily.
我的 AI 工作流 Skill 合集，每个都来自真实工作场景，持续更新。

> Compatible with WorkBuddy / Claude Code — copy any skill folder to `~/.claude/skills/` and it works.
> 兼容 WorkBuddy / Claude Code：把任意 skill 文件夹复制到 `~/.claude/skills/` 即可使用。

---

## Skills · Skill 索引

| Skill | What it does | Status |
|-------|-------------|--------|
| **[interview-coach](skills/interview-coach/)** · 面试陪练 | Turns JD + resume + company info into a structured 6-chapter interview playbook. 把 JD + 简历 + 公司信息变成 6 章结构化面试弹药库 | ✅ v4.4 |

<!-- Add new skills here, one row each -->

---

## Repo Structure · 目录结构

```
My-skills/
├── skills/                  # Skill bodies · Skill 本体
│   └── interview-coach/     # SKILL.md + references/ + assets/
├── samples/                 # Sample outputs · 产出样例
│   └── interview-coach/     # 2 sample playbooks + screenshots
└── publish.sh               # One-command release script · 一键发布脚本
```

---

## Featured: interview-coach · 面试陪练

An AI workflow skill that turns JD + resume + company info into a structured 6-chapter interview prep playbook. Works across industries: **Product / Operations / Sales / HR / Finance / Tech / Design / Legal / Project Management**.

一个开源的 AI 工具。**不虚构 · 不夸大 · 不写空话 · 信息不足会先追问**。

| Chapter | Question It Answers / 回答的问题 |
|---------|-------------------------------|
| **A — Understand the Opportunity** | What is this company and role really about? / 这家公司和岗位到底是什么 |
| **B — My Positioning** | Why am I a match for this role? / 我跟这个岗位为什么匹配 |
| **C — Evidence + Stories** | Which experiences back up my claims? / 我有哪些经历能接住这个问题 |
| **D — Prep + Deep Dive** | What will the interviewer press on, and how do I prep? / 面试官会怎么追问，我提前怎么答 |
| **E — Fit + Practice** | What does each round look like? How do I crack a case? / 几轮面试准备什么、Case 怎么拆 |
| **F — Final Execution** | Concrete actions before / during / after the interview / 面前面中面后的具体动作 |

---

## Sample Preview

![Header preview](./samples/interview-coach/样例截图-华泰国际-首屏.png)

Open the `.html` files in [samples/](samples/interview-coach/) locally in a browser to view full playbooks.

---

## How to Use · 怎么用

1. Pick a skill from the index above · 从上面的索引挑一个 skill
2. Copy its folder (e.g. `skills/interview-coach/`) to `~/.workbuddy/skills/` or `~/.claude/skills/`
3. Restart the app, then just describe your task in chat — the skill triggers automatically

---

## License

MIT
