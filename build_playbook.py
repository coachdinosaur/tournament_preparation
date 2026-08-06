#!/usr/bin/env python
"""Build the Dino Ballecer round-by-round playbook DOCX.

Reuses build_standalone_report.render_report() unchanged, then sets
``page_break_before`` on the major section headings so the dashboard, the
tournament-wide gates, each round, and the appendix each start on a fresh page
(one-card-per-page). No application code is modified by this script.
"""
from __future__ import annotations

from pathlib import Path

from docx import Document

from build_standalone_report import render_report

ROOT = Path(__file__).resolve().parent
STEM = "Dino_Ballecer_Round_by_Round_Game_Preparation"
SOURCE = ROOT / f"{STEM}.md"
OUTPUT = ROOT / f"{STEM}.docx"
TITLE = "Dino Ballecer — Round-by-Round Game Preparation"

# Section headings that should start a new page (matched by prefix).
BREAK_BEFORE = (
    "Tournament-Wide Gates",
    "Systems Library",
    "Round 1", "Round 2", "Round 3", "Round 4", "Round 5",
    "Round 6", "Round 7", "Round 8", "Round 9",
    "Appendix",
)


def main() -> None:
    render_report(SOURCE, OUTPUT, TITLE)

    doc = Document(str(OUTPUT))
    broken = []
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
