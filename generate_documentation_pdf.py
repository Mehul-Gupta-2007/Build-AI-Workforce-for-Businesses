from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "Mend-Project-Documentation.md"
OUTPUT = ROOT / "Mend-Project-Documentation.pdf"

INK = colors.HexColor("#20231F")
MUTED = colors.HexColor("#72786E")
LIME = colors.HexColor("#D3F36B")
PALE = colors.HexColor("#F3F6EC")
LINE = colors.HexColor("#E3E7DC")
CORAL = colors.HexColor("#B95A49")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CoverKicker", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=8, leading=11, textColor=MUTED, spaceAfter=12, alignment=TA_LEFT))
styles.add(ParagraphStyle(name="CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=34, leading=38, textColor=INK, alignment=TA_LEFT, spaceAfter=5))
styles.add(ParagraphStyle(name="CoverSubtitle", parent=styles["Normal"], fontName="Helvetica", fontSize=14, leading=19, textColor=MUTED, spaceAfter=15))
styles.add(ParagraphStyle(name="SectionHeading", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=17, leading=21, textColor=INK, spaceBefore=11, spaceAfter=8, keepWithNext=True))
styles.add(ParagraphStyle(name="SubHeading", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=INK, spaceBefore=7, spaceAfter=4, keepWithNext=True))
styles.add(ParagraphStyle(name="BodyCopy", parent=styles["BodyText"], fontName="Helvetica", fontSize=9, leading=13, textColor=INK, spaceAfter=6))
styles.add(ParagraphStyle(name="BulletCopy", parent=styles["BodyText"], fontName="Helvetica", fontSize=9, leading=12.5, textColor=INK, leftIndent=13, firstLineIndent=-8, bulletIndent=1, spaceAfter=3))
styles.add(ParagraphStyle(name="Callout", parent=styles["BodyText"], fontName="Helvetica", fontSize=9, leading=13, textColor=INK, leftIndent=8, rightIndent=8, spaceBefore=5, spaceAfter=8, borderColor=LINE, borderWidth=.6, borderPadding=8, backColor=PALE))
styles.add(ParagraphStyle(name="CodeBlock", parent=styles["Code"], fontName="Courier", fontSize=8, leading=11, textColor=INK, leftIndent=8, rightIndent=8, borderColor=LINE, borderWidth=.5, borderPadding=8, backColor=colors.HexColor("#F7F8F5"), spaceBefore=2, spaceAfter=8))
styles.add(ParagraphStyle(name="SmallMeta", parent=styles["Normal"], fontName="Helvetica", fontSize=8, leading=11, textColor=MUTED))


def inline_markup(text: str) -> str:
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"`([^`]+)`", r'<font name="Courier" size="8">\1</font>', text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*(.+?)\*", r"<i>\1</i>", text)
    return text


class MendDocTemplate(BaseDocTemplate):
    def __init__(self, filename: Path):
        page_width, page_height = A4
        left = right = 19 * mm
        top = 20 * mm
        bottom = 18 * mm
        super().__init__(str(filename), pagesize=A4, leftMargin=left, rightMargin=right, topMargin=top, bottomMargin=bottom, title="Mend Project Documentation", author="Mend")
        frame = Frame(left, bottom, page_width - left - right, page_height - top - bottom, id="content")
        self.addPageTemplates(PageTemplate(id="mend", frames=frame, onPage=self.decorate_page))

    def decorate_page(self, canvas, doc):
        canvas.saveState()
        page_width, page_height = A4
        canvas.setFillColor(INK)
        canvas.rect(0, page_height - 5 * mm, page_width, 5 * mm, fill=1, stroke=0)
        canvas.setFillColor(LIME)
        canvas.rect(19 * mm, page_height - 5 * mm, 16 * mm, 5 * mm, fill=1, stroke=0)
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(.5)
        canvas.line(19 * mm, 14 * mm, page_width - 19 * mm, 14 * mm)
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(MUTED)
        canvas.drawString(19 * mm, 9.5 * mm, "MEND  /  PROJECT DOCUMENTATION")
        canvas.drawRightString(page_width - 19 * mm, 9.5 * mm, str(doc.page))
        canvas.restoreState()


def build_story(markdown: str):
    lines = markdown.splitlines()
    story = []
    i = 0
    cover = True
    while i < len(lines):
        line = lines[i].strip()
        if not line or line == "---":
            i += 1
            continue
        if line.startswith("# "):
            title = line[2:].strip()
            if cover:
                story.append(Spacer(1, 23 * mm))
                story.append(Paragraph("AUTONOMOUS WORKFLOW RECOVERY", styles["CoverKicker"]))
                story.append(Paragraph(inline_markup(title), styles["CoverTitle"]))
                i += 1
                continue
            story.append(Paragraph(inline_markup(title), styles["SectionHeading"]))
            i += 1
            continue
        if line.startswith("## "):
            heading = line[3:].strip()
            if cover and heading == "Project Documentation":
                story.append(Paragraph(inline_markup(heading), styles["CoverSubtitle"]))
                story.append(Spacer(1, 2 * mm))
                story.append(Paragraph("A practical guide to the Mend workflow recovery console, its demo features, setup, and path to production.", styles["BodyCopy"]))
                story.append(Spacer(1, 3 * mm))
                story.append(Paragraph("PROJECT GUIDE  ·  OCTOBER 2026", styles["CoverKicker"]))
                story.append(Spacer(1, 8 * mm))
                story.append(Table([[Paragraph("MONITOR", styles["SmallMeta"]), Paragraph("DIAGNOSE", styles["SmallMeta"]), Paragraph("RECOVER", styles["SmallMeta"])]], colWidths=[52 * mm] * 3, style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), PALE), ("BOX", (0, 0), (-1, -1), .6, LINE), ("INNERGRID", (0, 0), (-1, -1), .5, LINE), ("LEFTPADDING", (0, 0), (-1, -1), 10), ("TOPPADDING", (0, 0), (-1, -1), 10), ("BOTTOMPADDING", (0, 0), (-1, -1), 10)])))
                story.append(Spacer(1, 8 * mm))
                cover = False
            else:
                story.append(Paragraph(inline_markup(heading), styles["SectionHeading"]))
            i += 1
            continue
        if line.startswith("### "):
            story.append(Paragraph(inline_markup(line[4:].strip()), styles["SubHeading"]))
            i += 1
            continue
        if line.startswith("> "):
            text = line[2:]
            while i + 1 < len(lines) and lines[i + 1].strip().startswith("> "):
                i += 1
                text += " " + lines[i].strip()[2:]
            story.append(Paragraph(inline_markup(text), styles["Callout"]))
            i += 1
            continue
        if line.startswith("``` ") or line == "```":
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") or " ")
                i += 1
            text = "<br/>".join(code_lines)
            story.append(Paragraph(text, styles["CodeBlock"]))
            i += 1
            continue
        if re.match(r"^\d+\.\s", line):
            while i < len(lines) and re.match(r"^\d+\.\s", lines[i].strip()):
                match = re.match(r"^(\d+)\.\s+(.*)$", lines[i].strip())
                story.append(Paragraph(f"<b>{match.group(1)}.</b> {inline_markup(match.group(2))}", styles["BulletCopy"]))
                i += 1
            continue
        if line.startswith("- "):
            while i < len(lines) and lines[i].strip().startswith("- "):
                story.append(Paragraph("• " + inline_markup(lines[i].strip()[2:]), styles["BulletCopy"]))
                i += 1
            continue
        paragraph = line
        while i + 1 < len(lines) and lines[i + 1].strip() and not lines[i + 1].strip().startswith(("#", ">", "- ", "```", "---")) and not re.match(r"^\d+\.\s", lines[i + 1].strip()):
            i += 1
            paragraph += " " + lines[i].strip()
        story.append(Paragraph(inline_markup(paragraph), styles["BodyCopy"]))
        i += 1
    return story


if __name__ == "__main__":
    if not SOURCE.exists():
        raise SystemExit(f"Documentation source not found: {SOURCE}")
    doc = MendDocTemplate(OUTPUT)
    doc.build(build_story(SOURCE.read_text(encoding="utf-8")))
    print(f"Created {OUTPUT}")
