# meeting-minutes

Turn a 1–3 hour meeting transcript into formal minutes — in Chinese or English.

> This skill was distilled from my practice in the **China International College Students' Innovation Competition** (中国国际大学生创新大赛): page-by-page material reviews, expert coaching sessions, revision checklists, deadline scrambles. It works well for competition work, and in my own use it performs just as well in ordinary meetings — lab meetings, project reviews, client calls.

An Agent Skill: written to the `SKILL.md` convention, so any agent that reads skills can load it. It also ships a standalone script that renders Markdown into a formatted `.docx`.

中文说明见 [README.zh-CN.md](README.zh-CN.md).

## Three modes

Same transcript, three products — not three templates:

| Mode | For | Keeps | Length |
|---|---|---|---|
| Narrative | internal archive, handover | who raised what, who pushed back, how it was decided | 10–20% of transcript |
| Inductive (default) | review, revision checklist | problem → fix → action, zero names | 8–15% |
| Brief | chat thread, personal todo | numbered conclusions + action items | ≤400 words, 5–15 items |

In one line: **narrative keeps the process, inductive keeps the conclusions, brief keeps the actions.**

See [`examples/demo.md`](examples/demo.md) for one fictional transcript rendered in all three modes.

## Why another minutes tool

Existing tools fall into two camps: the summary baked into ASR output (a play-by-play), or a "time / place / attendees / decisions" template (no judgement at all).

The hard part isn't compression, it's **editorial judgement**: what to cut as off-topic, which criticism to redirect at the work instead of the person, which line deserves bold. That is editing, not summarising.

## Context first

Before drafting, the skill goes looking for the project: previous minutes, decks, proposals, glossaries, progress notes in your workspace. Knowing what the project is doing — and what the last meeting settled — is what makes the minutes use the project's own terms instead of generic phrasing. If it cannot find that context, it asks which folder the project lives in rather than guessing.

## Install

```bash
git clone https://github.com/HbS66-pro/meeting-minutes.git
```

Copy it into your agent's skills directory, e.g.:

```bash
cp -r meeting-minutes ~/.dsh/skills/meeting-minutes
```

No package manager, no build step. If your agent reads skills from another directory, put it there.

## Usage

In conversation:

> Transcript is in `meeting.md`. Give me inductive minutes, save to the current folder.

- "keep the process / who said what" → narrative
- nothing specified → inductive
- "summary / just the points / action items" → brief

Chinese meetings:

> 转录在 `会议转录.md`，按归纳模式出纪要，存到当前目录。

The transcript determines the output language: an English meeting produces English minutes, a Chinese meeting produces Chinese minutes.

Just want the docx, no agent:

```bash
python -m pip install "python-docx>=1.0"
python scripts/md2docx.py draft.md out.docx --check           # Chinese layout
python scripts/md2docx.py notes.md out.docx --lang en --check  # English layout
```

`--check` reopens the file and verifies paragraph by paragraph: fonts, sizes, exact line spacing, first-line indent, paragraph spacing, and the two emphasis colours. It exits non-zero on any mismatch.

## Output format

Chinese (`--lang zh`, default): body 宋体 12pt, Latin text Times New Roman, exact 28pt line spacing, 2-character first-line indent; title and level-1 headings 黑体 16pt bold, level-2 黑体 14pt bold.

English (`--lang en`): Times New Roman throughout, no first-line indent, 6pt after paragraphs, same 28pt exact spacing and heading sizes.

Two emphasis levels in both: `**text**` black bold, `==text==` blue bold (#0000FF). Use them sparingly — only where it would change a decision.

## Upstream: where the text comes from

This skill starts from text; it does not do speech recognition. If you only have audio, [`references/transcription.md`](references/transcription.md) lays out four routes and a selection table: one-click cloud transcription (Quark's "Recording Notes" and similar, with speaker separation), local Whisper family, phone transcription saved as Markdown, and desktop automation as a last resort. It also includes ready-to-run `yt-dlp` / `ffmpeg` commands.

Rule of thumb: multi-speaker meetings that need names → cloud; confidential material → local faster-whisper, but you label speakers yourself.

## Repository layout

```
meeting-minutes/
├── SKILL.md                     # modes, rules, workflow, English quick reference
├── references/
│   ├── modes.md                 # mode criteria, good/bad examples, rewriting
│   ├── writing.md               # AI-tone, officialese, people vs. work
│   ├── transcription.md         # audio → text: four routes, commands
│   └── docx-format.md           # formatting spec and the Markdown subset
├── scripts/md2docx.py           # Markdown → docx (python-docx only)
└── examples/demo.md             # one transcript, three outputs
```

## Boundaries

- No speech-to-text, no meeting-platform integration, no calendar or reminders.
- Not zero-touch: names, numbers, amounts and dates need a human pass.
- No puffery: never praise results the meeting did not discuss.

## License

MIT. All names, organisations, projects and numbers in the examples are fictional.
