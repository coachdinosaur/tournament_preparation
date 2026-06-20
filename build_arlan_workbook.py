#!/usr/bin/env python
"""Build the Arlan Cabe Rounds 1-2 game-preparation DOCX.

Reuses build_standalone_report.render_report() unchanged, then sets
``page_break_before`` on the major section headings so each top-level section
(dashboard, tournament-wide gates, each round, and the appendix) starts on a
fresh page. No application code is modified by this script.
"""
from __future__ import annotations

from pathlib import Path

from docx import Document

from build_standalone_report import render_report

ROOT = Path(__file__).resolve().parent
STEM = "Arlan_Cabe_Rounds_1_2_Coaching_Workbook"
SOURCE = ROOT / f"{STEM}.md"
OUTPUT = ROOT / f"{STEM}.docx"
TITLE = "Arlan Cabe — Round-by-Round Game Preparation"

# Section headings that should start a new page (matched by prefix).
BREAK_BEFORE = (
    "Tournament Dashboard",
    "Round 1 — Black",
    "Round 2 — White",
    "Appendix",
)


def main() -> None:
    render_report(SOURCE, OUTPUT, TITLE)

    doc = Document(str(OUTPUT))
    broken = []
    for section in doc.sections:
        for paragraph in section.header.paragraphs:
            for run in paragraph.runs:
                run.text = run.text.replace(" — FM Dino Ballecer", "")

    for par in doc.paragraphs:
        text = par.text.strip()
        style = par.style.name if par.style else ""
        if style.startswith(("Heading", "Title")) and any(text.startswith(b) for b in BREAK_BEFORE):
            par.paragraph_format.page_break_before = True
            broken.append(text[:48])
    doc.save(str(OUTPUT))
    print(f"saved -> {OUTPUT.name}  (page breaks before {len(broken)} headings)")
    for b in broken:
        print("   *", b.encode("ascii", "replace").decode("ascii"))


if __name__ == "__main__":
    main()
