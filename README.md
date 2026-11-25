# meeting-minutes

An Agent Skill (plus a standalone Markdown-to-Word formatter) for turning 1–3 hour meeting transcripts into structured minutes, in either Chinese or English.

中文说明见 [README.zh-CN.md](README.zh-CN.md).

I put this together while preparing for the **China International College Students' Innovation Competition** (中国国际大学生创新大赛), where we had endless page-by-page deck reviews, advisor coaching sessions, and tight revision deadlines. Since then I have also been using it for regular lab meetings, project reviews, and client calls.

It follows the `SKILL.md` convention so any agent that supports Agent Skills can load it. The bundled `scripts/md2docx.py` script also works standalone whenever you just want to turn Markdown into a clean `.docx`.

## Three output modes

Depending on who needs to read the minutes, the skill produces one of three formats from the same transcript:

| Mode | Best for | What it keeps | Typical length |
|---|---|---|---|
| `narrative` | Internal archive, handover | Who raised what, follow-up questions, how the decision landed | 10–20% of transcript |
| `inductive` (default) | Reviews, revision checklists | Problem, decision, and next action, with personal names stripped | 8–15% of transcript |
| `brief` | Group chats, personal todo list | Numbered takeaways and action items only | ≤400 words, 5–15 items |

### Quick example

Given a short fictional transcript snippet (translated from [`examples/demo.md`](examples/demo.md)):

```text
Speaker 1: First item is the procurement list: two clean benches, 120k budget.
Speaker 2: Does 120k include installation?
Speaker 1: No, installation is extra, roughly 8k.
Speaker 3: Why not buy one large bench instead? Two small ones take up more space.
Speaker 1: Lead time on the large one is 10 weeks, too late for the November inspection.
Speaker 2: Schedule comes first. Stick with two small ones and put installation into the budget.
Speaker 3: Fine, I will clear the room.
```

**Inductive mode** strips names and groups by issue:

> **1. Budget must include installation**
> The current 120k quote excludes installation (~8k), leaving a budget gap. Resubmit the list with installation itemized inside the total.
>
> **2. Keep two small clean benches**
> One large unit saves space, but its 10-week lead time misses the November inspection. **Prioritize schedule and order two small units**; the lab team will clear the room.

**Brief mode** cuts straight to takeaways and owners:

> **Key points**
> 1. Procurement budget updated to include installation (~128k total).
> 2. Staying with two small benches because the large unit misses the November inspection.
>
> **Action items**
> 1. Resubmit procurement list — Procurement (by Nov 5)
> 2. Clear room — Lab team (this week)

See [`examples/demo.md`](examples/demo.md) for the full side-by-side comparison including Narrative mode.

## Context-first workflow

Before writing anything, the skill looks around your workspace for project materials: earlier minutes, slide decks, proposals, glossaries, or progress notes. Reading those first helps it use the project's actual terminology and pick up where the last meeting left off. If it cannot locate the project folder, it asks instead of guessing.

The output language automatically follows the transcript: English transcripts yield English minutes, Chinese transcripts yield Chinese minutes.

## Install

Clone the repo and copy it into your agent's skills folder (for example `~/.claude/skills/` or `~/.dsh/skills/`):

```bash
git clone https://github.com/HbS66-pro/meeting-minutes.git
cp -r meeting-minutes ~/.dsh/skills/meeting-minutes
```

## Usage

In conversation with your agent:

> Transcript is in `meeting.md`. Write inductive minutes and save them to the current folder.

You can pick a mode in plain language: ask for "who said what / keep the discussion" for `narrative`, "summary / just the action items" for `brief`, or leave it unspecified to get `inductive`.

For Chinese meetings:

> 转录在 `会议转录.md`，按归纳模式出纪要，存到当前目录。

### Standalone `.docx` export

If you only want the Word formatter without using an agent:

```bash
python -m pip install "python-docx>=1.0"
python scripts/md2docx.py draft.md out.docx --check            # Chinese layout
python scripts/md2docx.py notes.md out.docx --lang en --check  # English layout
```

The `--check` flag reopens the generated `.docx` and checks every paragraph for font family, font size, line spacing, indentation, paragraph spacing, and emphasis colors, exiting non-zero if anything drifts.

## Word layout defaults

- **Chinese (`--lang zh`, default):** 12pt SimSun (宋体) body with Times New Roman for Latin text, exact 28pt line spacing, 2-character first-line indent; title and H1 in 16pt bold SimHei (黑体), H2 in 14pt bold SimHei.
- **English (`--lang en`):** Times New Roman throughout, no first-line indent, 6pt space after paragraphs, exact 28pt line spacing, same heading sizes.
- **Emphasis:** `**text**` renders as black bold; `==text==` renders as blue bold (`#0000FF`), intended only for decisions that change action.

## Turning audio into text

This skill starts from text and does not run speech recognition itself. If you only have a recording, [`references/transcription.md`](references/transcription.md) compares four practical routes (cloud transcription with speaker labels such as Quark Recording Notes, local Whisper / faster-whisper, mobile transcription saved to Markdown, and desktop automation fallback) along with ready-to-use `yt-dlp` and `ffmpeg` commands.

As a quick rule: use cloud transcription when you need multi-speaker labels; use local `faster-whisper` for confidential audio and label speakers manually.

## Repository layout

```text
meeting-minutes/
├── SKILL.md                     # modes, rules, workflow, English quick reference
├── references/
│   ├── modes.md                 # mode criteria, examples, and conversion tips
│   ├── writing.md               # tone checklist, avoiding officialese, handling criticism
│   ├── transcription.md         # audio-to-text routes and commands
│   └── docx-format.md           # Word formatting spec and supported Markdown syntax
├── scripts/md2docx.py           # Markdown -> docx converter (python-docx only)
└── examples/demo.md             # one transcript rendered in all three modes
```

## Notes and limits

- Does not handle speech-to-text, meeting platform hooks, or calendar reminders.
- Always do a quick human pass over names, numbers, budgets, and dates before sending minutes out.
- The skill is instructed not to invent praise or conclusions that were never discussed in the meeting.

## License

MIT. All names, organizations, projects, and figures in the examples are fictional.
