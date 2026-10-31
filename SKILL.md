---
name: meeting-minutes
description: 把会议录音文字稿和笔记整理成正式会议纪要（中英文会议都支持，输出语言跟随输入）。三种输出：叙事（留讨论过程与人物，内部存档）、归纳（零人名，问题→改法→做法，默认，送审用）、总结（编号清单，只要重点与待办）。触发词：会议纪要、整理会议记录、会议总结、会议摘要、待办清单、meeting minutes、meeting notes、action items。
---

# 会议纪要

## 一、先定模式

三模式不是三个模板，是同一份材料的三个压缩层级：**叙事留过程，归纳留结论，总结留行动**。事实层共用一套规则，差别只在"保留什么"。

| 模式 | 给谁 | 留什么 | 篇幅 |
|---|---|---|---|
| 叙事 `narrative` | 自己回看、组内交接、存档 | 谁提了什么、谁追问、怎么定下来的 | 转录的 10–20% |
| 归纳 `inductive` | 送审、评审、修改清单（**默认**） | 问题→改法→做法，零人名 | 转录的 8–15% |
| 总结 `brief` | 群里转发、自己的待办 | 编号结论 + 待办，无过程 | 全文 ≤400 字，5–15 条 |

判定：

- 用户没说 → **归纳**
- 出现"记下过程""谁说了什么""留档" → 叙事
- 出现"总结一下""只要重点""列个清单""有哪些待办" → 总结
- 拿不准且返工代价高时，一句话问清楚，不猜两遍

## 二、语言：输入什么语言，输出什么语言

- **中文会** → 中文纪要，按本文的中文规范写。
- **英文会** → 英文纪要，结构不变；别套中文公文腔，也别写英文的 AI 腔（`Furthermore/Moreover` 堆砌、`In conclusion` 收尾、每段等长）。
- **中英混合** → 按主要语言写，专有名词保留原文。

排版跟着语言走：中文用 `--lang zh`（默认），英文用 `--lang en`。英文模式下标题与正文都是 Times New Roman，不首行缩进、段后 6pt。

## 三、通用原则（三模式都适用）

1. **只写会上说过的**。不补全、不推断未讨论的决议；数字、金额、日期、人名以转录为准，拿不准就标"待确认"。
2. **对事直说，对人留面**。材料、方案的问题直接写，不弱化；针对个人的批评去掉人名，落到事上。
3. **按主题，不按时间**。3–9 个主题，散落的对话归到对应主题下。
4. **强调不均匀**。真正重要的才加粗，两级：`**…**`＝加粗黑色（重点），`==…==`＝加粗蓝色（更重点）。总量少而精。
5. **去 AI 腔**。不用"进行了X""系统梳理了""首先/其次/最后"，不写"值得注意的是"这类零主语评论，句长段长不齐。清单见 `references/writing.md`。

## 四、三种骨架

### 叙事

```markdown
# 项目——会议主题（日期，X老师指导）

## 一、会议概要
2–3 句：为什么开、开到哪一步

## 二、讨论要点
### 1. 主题
谁汇报了什么 → 谁追问或反对 → 落到什么结论

## 三、后续工作
**事项：** 动作（谁、何时）
```

有人物、有过渡（"翻到第 12 页时"），关键原话用引号。目的：三个月后回看，知道当时为什么这么定。

### 归纳（默认）

骨架同上，但「二、讨论要点」每条写成 **问题 → 结论 → 做法**，零人名、零职称、零内部代号。目的：拿到就能照着改。

会议是逐页、逐节给意见（打磨会、评审会）时，不必另起格式：主题按材料页序排，每节标题写清位置（`### 5. 第 5–7 页 方案概述`），段内仍按"现状 → 结论 → 改法"写。写法细则见 `references/modes.md`。

### 总结

```markdown
# 会议主题（日期）

## 重点
1. ……

## 待办
1. 动作——责任人（时间）
```

每条一句话，动词或判断开头；没责任人就写"待定"。不写概要、不写过程、不再分小标题。用户只要在聊天里看，就直接贴出来；要文件再生成 docx。

## 五、工作流

0. **先摸背景，别直接写**：动手前先在工作区里翻这个会议和项目的材料——上一次纪要、项目文档、方案/PPT、术语表、进度记录。搞清楚这个项目在做什么、上次会定了什么、哪些叫法是对的，写出来的纪要才会用对术语、接得上上下文。找不到就先问一句项目在哪个目录。
1. **看材料**：有转录以转录为准，笔记补漏；只有笔记就在开头注明"据笔记整理"；**只有音频没有文字**，先按 `references/transcription.md` 选一条转写路。缺责任人、截止时间等关键项就问，不编。
1. **读透**：先通读转录理解来龙去脉，再对照材料（PPT、申报书、方案）核术语、地名、数据，不只凭笔记硬写。
2. **边读边抽**：标四类——结论与判断、问题、动作与责任人、跑题（删）。
3. **成稿**：按模式骨架写 md，语法见 `references/docx-format.md`。
4. **自检**：过一遍 `references/writing.md` 的清单，改完再读一遍。
5. **出 docx**：`python scripts/md2docx.py 草稿.md 成稿.docx --check`，一次生成并验格式；英文稿加 `--lang en`（需 python-docx，无 pandoc、无 LibreOffice）。
6. **命名与存放**：`{日期}_{主题}_纪要.docx`，有外部专家时在主题里标注"（X老师指导）"；存到用户指定目录，没指定就存当前目录。

## 六、边界

- 不做语音转写，从文本开始；音频怎么变文字见 `references/transcription.md`。
- 不承诺零人工：人名、数字、金额、日期必须有人过一遍。
- 不写成宣传稿：不给没讨论过的成绩下评价。

## 七、参考

- `references/modes.md` — 三模式判据、好例坏例、模式间改写
- `references/writing.md` — 去 AI 腔清单、公文腔对照、人事分寸
- `references/transcription.md` — 音频怎么变文字：四条路、选型表、交接格式
- `references/docx-format.md` — docx 格式规范、脚本能认的 md 语法、`--check` 用法
- `scripts/md2docx.py` — 生成脚本，只依赖 python-docx

---

## English quick reference

Turn a meeting transcript into formal minutes. Output language follows the meeting language; this section is the full operating guide for English meetings.

### Modes

| Mode | Audience | Keeps | Length |
|---|---|---|---|
| narrative | internal archive, handover | who raised what, who pushed back, how it was decided | 10–20% of transcript |
| inductive (default) | review, revision checklist | problem → fix → action, zero names | 8–15% |
| brief | chat thread, personal todo | numbered conclusions + action items | ≤400 words, 5–15 items |

Pick: nothing specified → inductive; "archive / who said what" → narrative; "summary / just the points / action items" → brief.

### Rules

1. **Only what was said.** No invented decisions, dates, owners, or numbers. Flag uncertain items as "to confirm".
2. **Hard on the work, soft on the person.** State problems with the material plainly; remove names when criticizing people.
3. **By topic, not by timeline.** 3–9 topics; fold scattered remarks into the matching topic.
4. **Bold sparingly, two levels.** `**text**` = black bold; `==text==` = blue bold (#0000FF). If everything is bold, nothing is.
5. **No AI tone.** No `Furthermore/Moreover` stacking, no `In conclusion`, no "it is worth noting that", no uniform paragraph lengths.

### Structure

```markdown
# Project — Meeting topic (date)

## Summary
2–3 sentences: why it met, where it landed

## Discussion
### 1. Topic
problem → decision → action (inductive); who raised → who pushed → conclusion (narrative)

## Next steps
**Action:** verb-first, owner, date
```

Brief mode: `# Meeting (date)` + `## Key points` (numbered) + `## Next steps` (numbered, owner in parentheses).

### Workflow

0. **Find the project first.** Search the workspace for previous minutes, decks, terminology and progress notes. Knowing what the project is doing and what the last meeting settled is what makes the minutes use the right terms. If you cannot find that context, ask which folder the project lives in.
1. Read the full transcript before drafting; check names, numbers and terms against source material.
2. Mark conclusions, problems, actions/owners, and off-topic material to drop.
3. Draft in the chosen mode's structure.
4. Self-check against the five rules; read it once more.
5. Export: `python scripts/md2docx.py draft.md out.docx --lang en --check` (needs `python-docx` only).
6. Name it `{date}_{topic}_minutes.docx`; save where the user asks, default current directory.

### Formatting

`--lang en`: Times New Roman throughout, no first-line indent, 6pt after paragraphs, exact 28pt line spacing, 12pt body, 16pt/14pt bold headings. `--lang zh` (default) adds Chinese fonts and a 2-character first-line indent.
