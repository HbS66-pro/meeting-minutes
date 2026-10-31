# meeting-minutes

把 1–3 小时的会议转录，整理成一份能直接用的正式纪要。

一个 Agent Skill：按 `SKILL.md` 约定编写，Claude Code、DSH 等能读 skill 的 agent 都能用。附带的 `scripts/md2docx.py` 也可以单独当「Markdown → 中文排版 docx」的转换器用。

## 三种模式

同一份转录的三种产物，不是三个模板：

| 模式 | 给谁 | 留什么 | 篇幅 |
|---|---|---|---|
| 叙事 | 自己回看、组内交接、存档 | 谁提了什么、谁追问、怎么定下来的 | 转录的 10–20% |
| 归纳（默认） | 送审、评审、修改清单 | 问题 → 改法 → 做法，零人名 | 转录的 8–15% |
| 总结 | 群里转发、自己的待办 | 编号结论 + 待办，无过程 | ≤400 字，5–15 条 |

三句话概括：**叙事留过程，归纳留结论，总结留行动。**

见 [`examples/demo.md`](examples/demo.md)：同一段虚构转录跑出三种产物。

## 它解决什么

现成的会议纪要工具分两种：ASR 自带的摘要（流水账），或者「时间 / 地点 / 参会人 / 决议」的模板填空（给不出判断）。

这活真正的难处不在压缩信息，在**取舍与分寸**：哪些跑题该删、哪些批评要转到事上、哪条结论必须加粗。这是编辑判断，不是摘要。

## 安装

```bash
git clone https://github.com/HbS66-pro/meeting-minutes.git
```

放进 agent 的 skill 目录：

```bash
# Claude Code
mv meeting-minutes ~/.claude/skills/meeting-minutes
# DSH
mv meeting-minutes ~/.dsh/skills/meeting-minutes
```

没有包管理、没有构建步骤，复制目录即可。

## 用法

对话里直接说：

> 转录在 `会议转录.md`，按归纳模式出纪要，存到当前目录。

- 说「要过程 / 谁说了什么」→ 叙事模式
- 什么都不说 → 归纳模式
- 说「总结 / 只要重点 / 待办」→ 总结模式

只想要 docx，不走 agent：

```bash
python -m pip install "python-docx>=1.0"
python scripts/md2docx.py 草稿.md 成稿.docx --check
```

`--check` 会逐段核对字体、字号、行距（固定 28 磅）、首行缩进、两级强调色，不通过就报错退出。

## 输出格式

正文宋体小四、西文 Times New Roman、固定行距 28 磅、首行缩进 2 字符；主标题与一级标题黑体三号、二级标题黑体四号。

两级强调：`**重点**` 加粗黑色，`==更重点==` 加粗蓝色（#0000FF）。加粗不均匀——只有真会改变决策的才加。

## 上游：文本从哪来

本 skill 从文本开始，不做语音识别。手上有音频时，[`references/transcription.md`](references/transcription.md) 给了四条路和选型表：云端一键转写（夸克「录音纪要」等，自带说话人分离）、本地 Whisper 家族、手机转写存 md、Windows 桌面自动化。

一句话：多人会议要人名就走云端；涉密内容走本地 faster-whisper，但要自己标说话人。

## 仓库结构

```
meeting-minutes/
├── SKILL.md                     # 模式判据、通用原则、工作流、边界
├── references/
│   ├── modes.md                 # 三模式判据、好坏例、互相改写
│   ├── writing.md               # 去 AI 腔、去公文腔、人事分寸
│   ├── transcription.md         # 音频怎么变文字
│   └── docx-format.md           # 格式规范与脚本能认的 Markdown
├── scripts/md2docx.py           # Markdown → docx（只依赖 python-docx）
└── examples/demo.md             # 同一段转录的三种产物
```

## 边界

- 不做语音转写，也不做会议平台集成、日程、提醒。
- 不承诺零人工：人名、数字、金额、日期必须有人过一遍。
- 不写成宣传稿：不给会上没讨论过的成绩下评价。

## 许可

MIT。示例中的人名、单位、项目、数据全部虚构。

---

## English

An Agent Skill that turns a 1–3 hour meeting transcript into a formal Chinese meeting-minutes document. Three modes — narrative (with speakers and process), inductive (no names, problem → fix → action, default), and brief (numbered conclusions + action items). Ships a `python-docx` script that renders Markdown into a Chinese-formatted `.docx` (SimSun 12pt, exact 28pt line spacing, 2-character first-line indent, two emphasis levels) and self-checks the formatting with `--check`.

Start from text: no ASR included; see `references/transcription.md` for upstream options.
