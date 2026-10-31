# meeting-minutes

把 1–3 小时的会议转录，整理成一份能直接用的正式纪要——中文会、英文会都支持。

> 这个 skill 是我在准备**中国国际大学生创新大赛**的过程中提炼出来的：逐页打磨材料、专家指导会、修改清单、赶截止前的那几轮。它对竞赛好用；在实验室组会、项目评审、客户沟通这些普通会议上，我用下来表现同样稳定。

一个 Agent Skill：按 `SKILL.md` 约定编写，任何能读 skill 的 agent 都能加载；附带的 `scripts/md2docx.py` 也可以单独当「Markdown → 排版 docx」的转换器用。

English: [README.md](README.md)

## 三种模式

同一份转录的三种产物，不是三个模板：

| 模式 | 给谁 | 留什么 | 篇幅 |
|---|---|---|---|
| 叙事 | 自己回看、组内交接、存档 | 谁提了什么、谁追问、怎么定下来的 | 转录的 10–20% |
| 归纳（默认） | 送审、评审、修改清单 | 问题 → 改法 → 做法，零人名 | 转录的 8–15% |
| 总结 | 群里转发、自己的待办 | 编号结论 + 待办，无过程 | ≤400 字，5–15 条 |

一句话：**叙事留过程，归纳留结论，总结留行动。**

见 [`examples/demo.md`](examples/demo.md)：同一段虚构转录跑出三种产物。

## 它解决什么

现成的会议纪要工具分两种：ASR 自带的摘要（流水账），或者「时间 / 地点 / 参会人 / 决议」的模板填空（给不出判断）。

这活真正的难处不在压缩信息，在**取舍与分寸**：哪些跑题该删、哪些批评要转到事上、哪条结论必须加粗。这是编辑判断，不是摘要。

## 先摸背景

动笔之前，skill 会先去工作区里找这个项目和这次会议的材料——上一次纪要、方案、PPT、术语表、进度记录。知道项目在做什么、上次会定了什么，纪要才会用对术语、接得上上下文。找不到就先问一句项目在哪个目录，不硬猜。

## 安装

```bash
git clone https://github.com/HbS66-pro/meeting-minutes.git
```

复制进 agent 的 skill 目录，例如：

```bash
cp -r meeting-minutes ~/.dsh/skills/meeting-minutes
```

没有包管理、没有构建步骤。你的 agent 从别的目录读 skill，就放到那里。

## 用法

对话里直接说：

> 转录在 `会议转录.md`，按归纳模式出纪要，存到当前目录。

- 说「要过程 / 谁说了什么」→ 叙事模式
- 什么都不说 → 归纳模式
- 说「总结 / 只要重点 / 待办」→ 总结模式

英文会议：

> Transcript is in `meeting.md`. Inductive minutes, please.

输出语言跟着会议语言走：中文会出中文纪要，英文会出英文纪要。

只想要 docx，不走 agent：

```bash
python -m pip install "python-docx>=1.0"
python scripts/md2docx.py 草稿.md 成稿.docx --check            # 中文排版
python scripts/md2docx.py notes.md out.docx --lang en --check  # 英文排版
```

`--check` 会重新打开产物逐段核对：字体、字号、固定行距、首行缩进、段前段后、两级强调色；有一项不符就非零退出。

## 输出格式

中文（`--lang zh`，默认）：正文宋体 12pt、西文 Times New Roman、固定行距 28 磅、首行缩进 2 字符；主标题与一级标题黑体 16pt 加粗，二级标题黑体 14pt 加粗。

英文（`--lang en`）：全篇 Times New Roman、不首行缩进、段后 6pt，行距与字号同上。

中英都用两级强调：`**重点**` 黑色加粗，`==更重点==` 蓝色加粗（#0000FF）。少而精，只标会改变决策的地方。

## 上游：文本从哪来

本 skill 从文本开始，不做语音识别。只有音频时，[`references/transcription.md`](references/transcription.md) 给了四条路和选型表：云端一键转写（夸克「录音纪要」等，自带说话人分离）、本地 Whisper 家族、手机转写存 md、Windows 桌面自动化兜底，另附可直接运行的 `yt-dlp` / `ffmpeg` 命令。

经验规则：多人会议要人名 → 云端；涉密内容 → 本地 faster-whisper，但说话人要自己标。

## 仓库结构

```
meeting-minutes/
├── SKILL.md                     # 模式、原则、工作流、英文速查
├── references/
│   ├── modes.md                 # 三模式判据、好坏例、互相改写
│   ├── writing.md               # 去 AI 腔、去公文腔、人事分寸
│   ├── transcription.md         # 音频→文字：四条路、命令备查
│   └── docx-format.md           # 格式规范与脚本能认的 Markdown
├── scripts/md2docx.py           # Markdown → docx（只依赖 python-docx）
└── examples/demo.md             # 同一段转录的三种产物
```

## 边界

- 不做语音转写、不做会议平台集成、不做日程与提醒。
- 不承诺零人工：人名、数字、金额、日期必须有人过一遍。
- 不写成宣传稿：不给会上没讨论过的成绩下评价。

## 许可

MIT。示例中的人名、单位、项目、数据全部虚构。
