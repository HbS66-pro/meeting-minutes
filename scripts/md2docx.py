#!/usr/bin/env python3
"""会议纪要 Markdown → DOCX（只依赖 python-docx，不需要 pandoc / LibreOffice）

用法:
    python md2docx.py 草稿.md                  # 输出同名 .docx
    python md2docx.py 草稿.md 成稿.docx        # 指定输出
    python md2docx.py 草稿.md --check          # 生成后逐段校验格式

Markdown 子集:
    # 标题        → 主标题（黑体三号、居中）
    ## 标题       → 一级标题（黑体三号）
    ### 标题      → 二级标题（黑体四号）
    其他非空行    → 正文段（宋体小四、首行缩进 2 字符、固定行距 28 磅）
    兼容旧稿: 整行 **…** 当标题（无序号→主标题或一级，中文序数→一级，数字编号→二级）
    行内 **…** 加粗黑色；==…== 加粗蓝色

格式常量集中在下面「格式规格」一节，改样式只改那里。
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor

# ------------------------------- 格式规格 -------------------------------
FONT_LATIN = "Times New Roman"
LINE_SPACING_PT = 28
FIRST_LINE_CHARS = 2
EMPHASIS_BLUE = RGBColor(0, 0, 255)
TEXT_BLACK = RGBColor(0, 0, 0)

SPEC = {
    "title": {"cn": "黑体", "size": 16, "bold": True, "center": True, "indent": False},
    "h1": {"cn": "黑体", "size": 16, "bold": True, "center": False, "indent": False},
    "h2": {"cn": "黑体", "size": 14, "bold": True, "center": False, "indent": False},
    "body": {"cn": "宋体", "size": 12, "bold": False, "center": False, "indent": True},
}

# ------------------------------- Markdown 解析 -------------------------------
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
SEPARATOR_RE = re.compile(r"^[-*_]{3,}$")
CN_ORDINAL_RE = re.compile(r"^[一二三四五六七八九十]+、")
ARABIC_ORDINAL_RE = re.compile(r"^\d+[.、]")


def heading_kind(level: int, has_title: bool) -> str:
    """# → 主标题（只认第一个）；## → 一级；### 及更深 → 二级"""
    if level == 1:
        return "h1" if has_title else "title"
    return "h1" if level == 2 else "h2"


def parse_markdown(text: str) -> list[tuple[str, str]]:
    """→ [(kind, text)]，kind ∈ title/h1/h2/body"""
    blocks: list[tuple[str, str]] = []
    has_title = False
    for raw in text.splitlines():
        line = raw.strip()
        if not line or SEPARATOR_RE.match(line):
            continue

        m = HEADING_RE.match(line)
        if m:
            kind = heading_kind(len(m.group(1)), has_title)
            has_title = has_title or kind == "title"
            blocks.append((kind, m.group(2)))
            continue

        if line.startswith("- ") or line.startswith("> "):
            line = line[2:].strip()
            if not line:
                continue

        kind = _legacy_heading_kind(line, allow_title=not has_title)
        if kind:
            has_title = has_title or kind == "title"
            blocks.append((kind, line[2:-2].strip()))
        else:
            blocks.append(("body", line))
    return blocks


def _legacy_heading_kind(line: str, allow_title: bool) -> str | None:
    """整行 **…** 视为标题（兼容旧稿）；行内有其他标记就不算

    无序号 → 主标题（仅当还没有主标题）或一级标题（如「重点」「待办」）
    """
    if len(line) < 5 or not (line.startswith("**") and line.endswith("**")):
        return None
    inner = line[2:-2].strip()
    if "**" in inner or "==" in inner:
        return None
    if CN_ORDINAL_RE.match(inner):
        return "h1"
    if ARABIC_ORDINAL_RE.match(inner):
        return "h2"
    return "title" if allow_title else "h1"


def tokenize(text: str) -> list[tuple[str, bool, bool]]:
    """行内强调 → [(片段, 加粗, 蓝色)]；标记不成对时原样输出并告警"""
    if text.count("**") % 2 or text.count("==") % 2:
        print(f"[warn] 强调标记不成对，按原文输出：{text[:40]}", file=sys.stderr)
        return [(text, False, False)] if text else []

    tokens: list[tuple[str, bool, bool]] = []
    buf: list[str] = []
    bold = blue = False
    i = 0
    while i < len(text):
        if text.startswith("**", i):
            if buf:
                tokens.append(("".join(buf), bold, blue))
                buf = []
            bold = not bold
            i += 2
        elif text.startswith("==", i):
            if buf:
                tokens.append(("".join(buf), bold, blue))
                buf = []
            blue = not blue
            i += 2
        else:
            buf.append(text[i])
            i += 1
    if buf:
        tokens.append(("".join(buf), bold, blue))
    return tokens


def plain_text(text: str) -> str:
    return "".join(seg for seg, _, _ in tokenize(text))


# ------------------------------- 排版 -------------------------------
def init_styles(doc: Document) -> None:
    normal = doc.styles["Normal"]
    normal.font.name = FONT_LATIN
    normal.font.size = Pt(SPEC["body"]["size"])
    normal.element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), SPEC["body"]["cn"])
    pf = normal.paragraph_format
    pf.line_spacing = Pt(LINE_SPACING_PT)
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)


def add_paragraph(doc: Document, spec: dict) -> object:
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.line_spacing = Pt(LINE_SPACING_PT)
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    if spec["center"]:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if spec["indent"]:
        # 用 first_line_indent 建 w:ind（保证 pPr 子元素顺序合法），再补 firstLineChars
        pf.first_line_indent = Pt(spec["size"] * FIRST_LINE_CHARS)
        p._p.pPr.find(qn("w:ind")).set(qn("w:firstLineChars"), str(FIRST_LINE_CHARS * 100))
    return p


def add_run(p, text: str, spec: dict, bold: bool, blue: bool) -> None:
    run = p.add_run(text)
    run.font.name = FONT_LATIN
    run.font.size = Pt(spec["size"])
    run.font.bold = spec["bold"] or bold or blue
    run.font.color.rgb = EMPHASIS_BLUE if blue else TEXT_BLACK
    run._element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), spec["cn"])


def build(blocks: list[tuple[str, str]], out_path: Path) -> Path:
    doc = Document()
    init_styles(doc)
    for kind, text in blocks:
        spec = SPEC[kind]
        p = add_paragraph(doc, spec)
        for seg, bold, blue in tokenize(text):
            add_run(p, seg, spec, bold, blue)

    props = doc.core_properties
    props.title = next((t for k, t in blocks if k == "title"), "")
    props.author = ""
    props.last_modified_by = ""
    props.comments = ""          # 清掉 python-docx 默认的 "generated by python-docx"
    props.language = "zh-CN"
    now = datetime.now(timezone.utc).replace(microsecond=0)
    props.created = now
    props.modified = now
    props.revision = 1
    doc.save(str(out_path))
    return out_path


# ------------------------------- 自检 -------------------------------
def verify(out_path: Path, blocks: list[tuple[str, str]]) -> list[str]:
    doc = Document(str(out_path))
    paras = doc.paragraphs
    problems: list[str] = []

    if len(paras) != len(blocks):
        problems.append(f"段落数应为 {len(blocks)}，实际 {len(paras)}")

    for idx, ((kind, text), p) in enumerate(zip(blocks, paras)):
        spec = SPEC[kind]
        pf = p.paragraph_format
        tag = f"第 {idx + 1} 段（{kind}）«{plain_text(text)[:16]}»"

        if p.text != plain_text(text):
            problems.append(f"{tag} 文字不符：{p.text[:24]!r}")
        if pf.line_spacing is None or abs(pf.line_spacing.pt - LINE_SPACING_PT) > 0.01:
            problems.append(f"{tag} 行距不是固定 {LINE_SPACING_PT} 磅")
        elif pf.line_spacing_rule != WD_LINE_SPACING.EXACTLY:
            problems.append(f"{tag} 行距规则不是「固定值」")
        if pf.space_before is None or pf.space_before.pt != 0 or pf.space_after is None or pf.space_after.pt != 0:
            problems.append(f"{tag} 段前段后不为 0")

        expect_align = WD_ALIGN_PARAGRAPH.CENTER if spec["center"] else None
        if p.alignment != expect_align:
            problems.append(f"{tag} 对齐方式不符：{p.alignment}")

        ind = p._p.pPr.find(qn("w:ind")) if p._p.pPr is not None else None
        chars = ind.get(qn("w:firstLineChars")) if ind is not None else None
        if spec["indent"] and chars != str(FIRST_LINE_CHARS * 100):
            problems.append(f"{tag} 首行缩进应为 {FIRST_LINE_CHARS} 字符，实际 {chars}")
        if not spec["indent"] and chars:
            problems.append(f"{tag} 标题不应有首行缩进")

        expected = tokenize(text)
        if len(p.runs) != len(expected):
            problems.append(f"{tag} 文字分段数不符（应有 {len(expected)} 个 run）")
            continue
        for run, (_, bold, blue) in zip(p.runs, expected):
            if run.font.name != FONT_LATIN:
                problems.append(f"{tag} 西文字体应为 {FONT_LATIN}，实际 {run.font.name}")
            rfonts = run._element.rPr.rFonts if run._element.rPr is not None else None
            cn = rfonts.get(qn("w:eastAsia")) if rfonts is not None else None
            if cn != spec["cn"]:
                problems.append(f"{tag} 中文字体应为 {spec['cn']}，实际 {cn}")
            if run.font.size is None or abs(run.font.size.pt - spec["size"]) > 0.01:
                problems.append(f"{tag} 字号应为 {spec['size']}pt")
            want_bold = bool(spec["bold"] or bold or blue)
            if bool(run.font.bold) != want_bold:
                problems.append(f"{tag} 加粗状态不符")
            want_color = EMPHASIS_BLUE if blue else TEXT_BLACK
            if run.font.color is None or run.font.color.rgb != want_color:
                problems.append(f"{tag} 字色不符")
    return problems


# ------------------------------- CLI -------------------------------
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="会议纪要 Markdown → DOCX")
    ap.add_argument("input", type=Path, help="Markdown 草稿")
    ap.add_argument("output", type=Path, nargs="?", help="输出 docx（默认同名）")
    ap.add_argument("--check", action="store_true", help="生成后逐段校验格式")
    args = ap.parse_args(argv)

    if not args.input.is_file():
        print(f"[error] 找不到输入文件：{args.input}", file=sys.stderr)
        return 2

    out = args.output or args.input.with_suffix(".docx")
    if out.suffix.lower() != ".docx":
        out = out.with_suffix(".docx")

    try:
        text = args.input.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        print("[error] 草稿不是 UTF-8 编码，请另存为 UTF-8 再试", file=sys.stderr)
        return 2

    blocks = parse_markdown(text)
    if not blocks:
        print("[error] 草稿是空的", file=sys.stderr)
        return 2
    if not any(kind == "title" for kind, _ in blocks):
        print("[warn] 没有主标题，首行建议写「# 会议主题（日期）」", file=sys.stderr)

    out.parent.mkdir(parents=True, exist_ok=True)
    build(blocks, out)
    print(f"已生成: {out}（{len(blocks)} 段）")

    if args.check:
        problems = verify(out, blocks)
        if problems:
            print(f"格式自检未通过，{len(problems)} 处问题：", file=sys.stderr)
            for item in problems:
                print(f"  - {item}", file=sys.stderr)
            return 1
        print(f"格式自检通过：{len(blocks)} 段")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
