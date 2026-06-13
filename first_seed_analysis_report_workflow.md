# First Seed Analysis and Report Workflow

## Subject

First seed analyzed: **GM Vignesh, N R**

Roster player ID: `2`

Generated dossier:

`manual_sections/Opponent_GM_Vignesh_N_R.md`

## What Was Analyzed

The app is tournament-specific. It analyzes the fixed roster, not arbitrary uploaded PGNs.

For the first seed, the app used:

- ChessBase PGN games from `chessbasepgn/`
- Lichess tournament-pool metadata from `tournament_pool_2026.db` / CSV
- The roster name matcher in `prep_manual_app.py`
- The bundled opening database in `openings/`
- Stockfish 18 from the sibling `Extract_ZST/stockfish/` folder

The generated Vignesh dossier currently has:

- **187 total games on file**
- **104 over-the-board PGN games**
- **83 Lichess online metadata rows**
- **104/104 analyzable PGN games analyzed by Stockfish**
- **0 pending engine games**
- **Depth 12**

The reason the engine count is `104`, not `187`, is that Lichess rows are metadata-only in this app. They help with opening/repertoire statistics, but they do not include move lists for local engine analysis.

## Command Used

The full per-player analysis command was:

```powershell
python prep_manual_app.py --analyze --scope player --player 2 --depth 12 --export
```

Meaning:

- `--scope player`: analyze one roster player only
- `--player 2`: GM Vignesh, N R
- `--depth 12`: use Stockfish depth 12
- `--export`: regenerate the Markdown manual sections after analysis

## Analysis Pipeline

The app does the analysis in this order:

1. **Scan PGNs**
   - Reads `.pgn` files under the project folder.
   - Matches player names in PGN headers to the fixed roster.
   - Stores games in `prep_manual.db`.

2. **Classify openings**
   - Uses PGN ECO/opening headers when present.
   - Otherwise replays the moves and checks the bundled opening database.
   - Falls back to the built-in opening classifier.

3. **Classify structure families**
   - Tags games against the prep manual's core structure families.
   - Examples: Advance Caro-Kann, Catalan / Reti Squeeze, Anti-Sicilian Counter-Package.

4. **Run engine analysis**
   - Replays each PGN game into FEN positions.
   - Uses Stockfish to evaluate positions.
   - Computes centipawn loss per move.
   - Groups accuracy by phase:
     - Opening
     - Middlegame
     - Endgame

5. **Build player profile**
   - Summarizes opening breadth, strong lines, repair lines, phase accuracy, and weakness categories.
   - Classifies endgame and simplified-position weakness samples.

6. **Export report sections**
   - Writes the updated opponent dossier into `manual_sections/`.

## Current First Seed Findings

### Overall Engine Profile

From the completed depth-12 run:

- **Analyzed games:** 104/104
- **Overall ACPL:** 13.9
- **Opening ACPL:** 7.7
- **Middlegame ACPL:** 11.7
- **Endgame ACPL:** 18.0

Interpretation:

Vignesh is most accurate in the opening phase and least accurate in the endgame phase, but the overall ACPL is still strong. Any report should describe these as relative tendencies, not as broad weaknesses.

### Opening Repertoire

The profile found:

- **128 distinct openings**
- Strong evidence of a broad repertoire
- Strong confidence lines include:
  - Sicilian Defense: Nyezhmetdinov-Rossolimo Attack
  - Rapport-Jobava System
  - English Opening: Agincourt Defense, Neo-Catalan Declined

Repair or target lines currently flagged:

- Caro-Kann Defense: Advance Variation, Tal Variation
- Queen's Gambit Declined: Ragozin Defense, Alekhine Variation

These should be treated as candidate targets, not automatic game-plan choices. Check whether they fit Dino's repertoire before recommending them.

### Structure Targets and Avoids

Engine fingerprint currently flags:

Target structures by lower accuracy:

- IQP / Panov Attack
- Catalan / Reti Squeeze

Structures where he appears solid:

- Advance Caro-Kann
- Fianchetto KID / Grunfeld Complexes

Result-score tables also show that he scores very well in several families, so the final report should balance engine accuracy with practical results.

### Endgame / Simplified-Position Categories

Classified weakness categories:

- Drawing defense failure: 4 samples
- Philidor: 3 samples
- Conversion failure: 2 samples
- Rook activity: 2 samples
- Rook behind pawn: 1 sample

Interpretation:

The report should not say "Vignesh is weak in endgames" broadly. A better phrasing is:

> In the analyzed sample, his least accurate phase is the endgame, with several classified rook-ending and drawing-defense samples. If Dino reaches a simplified rook ending, active-rook and defensive-resource awareness should be treated as practical chances.

## Turning This Into A Report

Use this report structure:

### 1. Executive Summary

Purpose:

Give Dino the short version before detailed prep.

Include:

- Overall strength
- Main repertoire profile
- Main target opportunities
- Main avoid zones
- One practical game-plan sentence

Example:

> Vignesh is a high-accuracy, broad-repertoire GM. His opening accuracy is strong, so the prep should not depend on catching him in a cheap opening trap. The best practical chances are to steer toward selected repair lines and keep pressure into simplified positions, especially rook endings where the sample shows drawing-defense and conversion issues.

### 2. Opening Repertoire

Split into:

- As White
- As Black
- Confidence lines
- Repair lines

For each line, include:

- Opening name
- ECO
- Game count
- Score
- Suggested action: target, avoid, or prepare neutralizer

### 3. Phase Accuracy

Include:

- Overall ACPL
- Opening ACPL
- Middlegame ACPL
- Endgame ACPL

Use plain interpretation:

- Lower ACPL means cleaner play
- Compare phases inside the same player profile
- Do not compare too aggressively across players unless analysis depth and sample sizes match

### 4. Middlegame and Structure Notes

Use:

- Core structure family scores
- Engine fingerprint by family
- Serious error counts

Convert into practical prep:

- Structures to steer toward
- Structures to avoid
- Structures where Dino needs model-game review

### 5. Endgame and Simplified Positions

Use the weakness category table and sample positions.

For each sample:

- Opponent
- Move number
- Mistake type
- Engine-preferred move
- Training theme

Do not overload the report with all samples. Pick the clearest 3 to 5.

### 6. Practical Game Plan For Dino

This should be the final actionable section.

Use bullets like:

- Do not rely on opening surprise only; Vignesh's opening ACPL is low.
- If playing Black, check whether Dino can reach the flagged Caro-Kann Advance / Tal structures safely.
- If playing White, investigate whether Dino can steer toward IQP / Panov or Catalan / Reti structures without entering Vignesh's strongest comfort zones.
- Keep pieces active into rook endings; the sample shows practical chances around Philidor, rook activity, and drawing-defense decisions.
- Prepare 3 model games from his losses or serious engine-error samples.

## Report Quality Rules

Use evidence-based wording:

- Say "the sample shows" instead of "he is bad at".
- Say "candidate target" instead of "guaranteed weakness".
- Include game counts next to repertoire claims.
- Include analysis depth next to engine claims.
- Separate Lichess metadata from OTB PGN engine analysis.

Avoid:

- Overstating personality traits.
- Calling a GM weak based on a small sample.
- Recommending a line Dino does not already understand.
- Mixing result-score targets and engine-accuracy targets without explaining the difference.

## Optimization Notes For The Second Seed

Use this first-seed workflow as the structure for the second seed, not as a source of copied conclusions. The second seed needs a fresh evidence pass from his own games.

### Second Seed Target

- Player: GM Shyaam, Nikhil P
- Player ID: `3`
- Main dossier after export: `manual_sections/Opponent_GM_Shyaam_Nikhil_P.md`
- Suggested report files:
  - `second_seed_report.md`
  - `second_seed_report.docx`
- Suggested report title: `Second Seed Report: GM Shyaam, Nikhil P`

### Analysis Command

Analyze all available games for the second seed at the same practical depth used for the first seed:

```powershell
python prep_manual_app.py --analyze --scope player --player 3 --depth 12 --export
```

After the command finishes, verify that the Shyaam dossier reports:

- Total games
- OTB PGN games
- Lichess metadata games
- Engine-analyzed games
- Pending games
- Overall ACPL
- Phase ACPL
- Profile confidence lines
- Top weakness categories

If pending games remain, do not hide that in the report. State the coverage directly.

### Reusable Report Checklist

For the second seed, collect the same fixed evidence fields before writing prose:

- Game coverage: total games, OTB PGNs, Lichess metadata, analyzed count, pending count.
- Opening profile: strongest lines, candidate weak lines, color split, and sample counts.
- Phase profile: opening, middlegame, and endgame ACPL with mistake counts.
- Practical repair lines: what Dino should review or avoid before the game.
- Structure targets: structures Dino can realistically reach from his current repertoire.
- Structure avoids: lines where the opponent's sample looks too clean or too comfortable.
- Endgame profile: top weakness categories and 3 to 5 clean sample positions.
- Confidence notes: high, medium, or low confidence for each major claim.

### Writing Rules For The Second Seed

- Do not copy Vignesh-specific opening or endgame conclusions into Shyaam's report.
- Keep all labels evidence-based: every strength, weakness, or tendency needs a number, sample count, phase score, or concrete game example.
- Separate engine-analyzed OTB PGNs from Lichess metadata.
- Include the engine depth near tactical or accuracy claims.
- Prefer "candidate target" and "sample suggests" when the evidence is limited.
- Tie recommendations to Dino's actual preparation, not to abstract engine preferences.

### DOCX Reuse

The embedded DOCX builder below can be reused for the second seed by changing only the config values:

- `SOURCE_MD = "second_seed_report.md"`
- `OUTPUT_DOCX = "second_seed_report.docx"`
- `REPORT_TITLE = "Second Seed Report: GM Shyaam, Nikhil P"`

Longer term, extract the embedded builder into a permanent `build_standalone_report.py` script so each seed report can be regenerated with config changes instead of copying code.

## Producing the Report Files (Markdown + Standalone DOCX)

Each seed report ships as **two files at the repo root**:

1. `<seed>_report.md` — the curated 6-section report (see *Turning This Into A Report* above).
2. `<seed>_report.docx` — the **same** report as a standalone Word file, formatted in this manual's
   style (same fonts, heading styles, bullets, bordered tables).

> **Do not modify `Tournament_Preparation_Manual.docx`.** The standalone `.docx` only *borrows* the
> manual's look by opening it as a **read-only style template**; the manual file itself is never
> written to. "Format it like the manual" — not "append it to the manual."

### Step 1 — Write the curated Markdown

Author `<seed>_report.md` following the 6-section structure and the Report Quality Rules above.

### Step 2 — Generate the standalone DOCX

Needs `python-docx` (already installed; otherwise `pip install python-docx`). Save the script below
as `build_standalone_report.py` **in the project root**, edit the three CONFIG lines at the top for
the seed, and run:

```powershell
python -X utf8 build_standalone_report.py
```

```python
#!/usr/bin/env python
"""Render <seed>_report.md as a standalone <seed>_report.docx, styled from the Tournament
Preparation Manual (used READ-ONLY as a template). The manual itself is never modified."""
import re
from pathlib import Path
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

ROOT = Path(__file__).resolve().parent

# ===== CONFIG — change these three lines per seed =====
MD         = ROOT / "first_seed_report.md"
OUT        = ROOT / "first_seed_report.docx"
HEADER_NEW = "First Seed Report: GM Vignesh, N R"     # replaces the manual's running-header title
# ======================================================

TEMPLATE     = ROOT / "Tournament_Preparation_Manual.docx"   # read-only style template; never written
HEADER_OLD   = "Tournament Preparation Manual"
BULLET_NUMID = 2

LINK_RE = re.compile(r'\[([^\]]+)\]\([^)]*\)')
def strip_links(s): return LINK_RE.sub(r'\1', s)

# ---- recursive inline parser: **bold**, *italic*, `code` (code may nest in emphasis) ----
def _fmt(b, i, m):
    d = {}
    if b: d["bold"] = True
    if i: d["italic"] = True
    if m: d["mono"] = True
    return d
def _emit(text, bold, italic, out):
    while text:
        m = re.search(r'(\*\*|\*|`)', text)
        if not m:
            out.append((text, _fmt(bold, italic, False))); return
        if m.start() > 0:
            out.append((text[:m.start()], _fmt(bold, italic, False)))
        mk = m.group(1); rest = text[m.end():]
        if mk == '`':
            j = rest.find('`')
            if j < 0: out.append(('`' + rest, _fmt(bold, italic, False))); return
            out.append((rest[:j], _fmt(bold, italic, True))); text = rest[j+1:]
        elif mk == '**':
            j = rest.find('**')
            if j < 0: out.append(('**' + rest, _fmt(bold, italic, False))); return
            _emit(rest[:j], True, italic, out); text = rest[j+2:]
        else:
            j = rest.find('*')
            if j < 0: out.append(('*' + rest, _fmt(bold, italic, False))); return
            _emit(rest[:j], bold, True, out); text = rest[j+1:]
def inline_runs(text):
    text = strip_links(text).replace("⚠️", "").replace("⚠", "").strip()
    out = []; _emit(text, False, False, out)
    return out or [("", {})]

# ---- block parser (handles hard-wrapped list items / paragraphs) ----
def cells(row):
    row = row.strip()
    if row.startswith("|"): row = row[1:]
    if row.endswith("|"): row = row[:-1]
    return [c.strip() for c in row.split("|")]
def is_block_start(line):
    s = line.strip()
    if not s: return True
    if re.match(r'#{1,6}\s', s): return True
    if s.startswith(("|", ">")): return True
    if re.fullmatch(r'-{3,}', s): return True
    if re.match(r'-\s+', s) or re.match(r'\d+\.\s+', s): return True
    return False
def collect_cont(lines, i):
    n = len(lines); buf = []
    while i < n and not is_block_start(lines[i]):
        buf.append(lines[i].strip()); i += 1
    return " ".join(x for x in buf if x), i
def is_sep(line):
    s = line.strip()
    return bool(s) and set(s) <= set("|:- ") and "-" in s
def parse_blocks(md):
    lines = md.split("\n"); blocks = []; i = 0; n = len(lines)
    while i < n:
        s = lines[i].rstrip()
        if not s.strip(): i += 1; continue
        if re.fullmatch(r'-{3,}', s.strip()): i += 1; continue
        m = re.match(r'(#{1,6})\s+(.*)', s)
        if m: blocks.append(("h", len(m.group(1)), m.group(2).strip())); i += 1; continue
        if s.lstrip().startswith("|") and i+1 < n and is_sep(lines[i+1]):
            tbl = [s]; sep = lines[i+1]; j = i + 2
            while j < n and lines[j].lstrip().startswith("|"): tbl.append(lines[j]); j += 1
            aligns = ["center" if c.startswith(":") and c.endswith(":") else "right" if c.endswith(":") else "left"
                      for c in cells(sep)]
            blocks.append(("table", cells(tbl[0]), aligns, [cells(r) for r in tbl[1:]])); i = j; continue
        if s.lstrip().startswith(">"):
            q = []
            while i < n and lines[i].lstrip().startswith(">"):
                q.append(re.sub(r'^\s*>\s?', '', lines[i])); i += 1
            blocks.append(("quote", " ".join(x.strip() for x in q if x.strip()))); continue
        m = re.match(r'\s*-\s+(.*)', s)
        if m:
            extra, i = collect_cont(lines, i + 1)
            blocks.append(("bullet", (m.group(1).strip() + " " + extra).strip())); continue
        m = re.match(r'\s*(\d+)\.\s+(.*)', s)
        if m:
            extra, i = collect_cont(lines, i + 1)
            blocks.append(("number", m.group(1), (m.group(2).strip() + " " + extra).strip())); continue
        extra, i = collect_cont(lines, i + 1)
        blocks.append(("p", (s.strip() + " " + extra).strip()))
    return blocks

def bullet_is_real(doc):
    try: numbering = doc.part.numbering_part.element
    except Exception: return False
    num = next((e for e in numbering.findall(qn('w:num')) if e.get(qn('w:numId')) == str(BULLET_NUMID)), None)
    if num is None: return False
    absId = num.find(qn('w:abstractNumId')).get(qn('w:val'))
    for ab in numbering.findall(qn('w:abstractNum')):
        if ab.get(qn('w:abstractNumId')) == absId:
            for lvl in ab.findall(qn('w:lvl')):
                if lvl.get(qn('w:ilvl')) == "0":
                    nf = lvl.find(qn('w:numFmt'))
                    return nf is not None and nf.get(qn('w:val')) == "bullet"
    return False

# ---- builders ----
def add_runs(p, runs):
    for text, f in runs:
        r = p.add_run(text)
        if f.get("bold"):   r.bold = True
        if f.get("italic"): r.italic = True
        if f.get("mono"):   r.font.name = "Consolas"
    return p
def set_pstyle(p, style_id):
    pPr = p._p.get_or_add_pPr()
    ex = pPr.find(qn('w:pStyle'))
    if ex is not None: pPr.remove(ex)
    e = OxmlElement('w:pStyle'); e.set(qn('w:val'), style_id); pPr.insert(0, e)
def set_bullet(p):
    pPr = p._p.get_or_add_pPr()
    numPr = OxmlElement('w:numPr')
    il = OxmlElement('w:ilvl'); il.set(qn('w:val'), "0"); numPr.append(il)
    nid = OxmlElement('w:numId'); nid.set(qn('w:val'), str(BULLET_NUMID)); numPr.append(nid)
    pPr.append(numPr)
def style_table(tbl):
    tblPr = tbl.tblPr
    w = OxmlElement('w:tblW'); w.set(qn('w:type'), 'dxa'); w.set(qn('w:w'), '9360'); tblPr.append(w)
    b = OxmlElement('w:tblBorders')
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        e = OxmlElement('w:' + edge); e.set(qn('w:val'), 'single')
        e.set(qn('w:color'), 'auto'); e.set(qn('w:sz'), '4'); b.append(e)
    tblPr.append(b)

# ---- main ----
doc = Document(str(TEMPLATE))
real_bullets = bullet_is_real(doc)

# resolve style IDs from the template body (apply by ID, not display name)
defined_ids = {s.style_id for s in doc.styles if s.style_id}
level_to_id = {}; list_id = "ListParagraph"
for p in doc.paragraphs:
    nm = p.style.name if p.style else ""
    pPr = p._p.find(qn('w:pPr')); ps = pPr.find(qn('w:pStyle')) if pPr is not None else None
    if ps is None: continue
    sid = ps.get(qn('w:val'))
    if nm.startswith("Heading"):
        lvl = nm.replace("Heading", "").strip()
        if lvl.isdigit(): level_to_id.setdefault(int(lvl), sid)
    elif nm == "List Paragraph": list_id = sid
title_id = "Title" if "Title" in defined_ids else level_to_id.get(1, "Heading1")
def style_for(report_level):
    if report_level == 1: return title_id            # report H1 -> Title
    t = report_level - 1                             # report H2 -> Heading1, H3 -> Heading2 ...
    return level_to_id.get(t) or (("Heading%d" % t) if ("Heading%d" % t) in defined_ids else level_to_id.get(1, "Heading1"))

# clear the body but keep the trailing section properties (page setup + header/footer refs)
body = doc.element.body
sectPr = body.find(qn('w:sectPr'))
for child in list(body):
    if child.tag in (qn('w:p'), qn('w:tbl')): body.remove(child)

def emit_para():
    p = doc.add_paragraph(); sectPr.addprevious(p._p); return p
def emit_table(rows, cols):
    t = doc.add_table(rows=rows, cols=cols); sectPr.addprevious(t._tbl); return t

for blk in parse_blocks(MD.read_text(encoding="utf-8")):
    kind = blk[0]
    if kind == "h":
        p = emit_para(); set_pstyle(p, style_for(blk[1])); add_runs(p, inline_runs(blk[2]))
    elif kind == "p":
        add_runs(emit_para(), inline_runs(blk[1]))
    elif kind == "bullet":
        p = emit_para(); set_pstyle(p, list_id)
        if real_bullets: set_bullet(p); add_runs(p, inline_runs(blk[1]))
        else: add_runs(p, [("•  ", {})] + inline_runs(blk[1]))
    elif kind == "number":
        p = emit_para(); set_pstyle(p, list_id)
        add_runs(p, [(blk[1] + ".  ", {})] + inline_runs(blk[2]))
    elif kind == "quote":
        p = emit_para()
        add_runs(p, [(t, {**f, "italic": True}) for t, f in inline_runs(blk[1])])
        p.paragraph_format.left_indent = Pt(18)
    elif kind == "table":
        header, aligns, rows = blk[1], blk[2], blk[3]; nc = len(header)
        tbl = emit_table(len(rows) + 1, nc)
        for c, h in enumerate(header):
            add_runs(tbl.cell(0, c).paragraphs[0], [(strip_links(h), {"bold": True})])
        for ri, row in enumerate(rows):
            for c in range(nc):
                cp = tbl.cell(ri + 1, c).paragraphs[0]
                add_runs(cp, inline_runs(row[c] if c < len(row) else ""))
                if aligns[c] == "right":  cp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                elif aligns[c] == "center": cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        style_table(tbl._tbl)

# relabel the inherited running header so the standalone file isn't titled as the whole manual
for sec in doc.sections:
    for p in sec.header.paragraphs:
        for r in p.runs:
            if HEADER_OLD in r.text:
                r.text = r.text.replace(HEADER_OLD, HEADER_NEW)

doc.save(str(OUT))
print("saved ->", OUT.name)
```

### How it works (and the gotchas that matter when duplicating)

- **Manual as a read-only template.** Opens the manual, clears its body in memory (removing every
  paragraph/table but keeping the trailing `w:sectPr`, so page setup + header/footer survive), then
  renders the report before that `sectPr`. The output inherits the manual's fonts, heading styles,
  bullet list and table look. The manual on disk is never saved.
- **Apply styles by styleId, not display name.** The manual has duplicate latent heading styles, so
  `style="Heading 1"` raises `KeyError`. The script reads the body's real style IDs and maps report
  **H1 → Title, H2 → Heading 1, H3 → Heading 2**.
- **Bullets** reuse the manual's bullet list (`numId=2`); **tables** get full-width single-line
  borders, a bold header row, and right-aligned numeric columns.
- **Hard-wrapped Markdown is handled.** The parser merges multi-line (wrapped) list items and
  paragraphs, so wrapping in the `.md` never splits a bullet or breaks an inline `code` span.
- **Header is relabeled** so the standalone file doesn't claim to be the whole manual.

### Duplicating for the next seed

Edit the three CONFIG lines (`MD`, `OUT`, `HEADER_NEW`) — e.g. point them at `second_seed_report.md`
→ `second_seed_report.docx` — and re-run. Nothing else changes.

## Next Player Workflow

For the next seed, run the same player-scope pattern:

```powershell
python prep_manual_app.py --analyze --scope player --player 3 --depth 12 --export
```

Then review:

```text
manual_sections/Opponent_GM_Shyaam_Nikhil_P.md
```

Repeat one player at a time so each dossier becomes complete and easy to verify. Then produce that
seed's two report files (`second_seed_report.md` + `second_seed_report.docx`) with the steps in
*Producing the Report Files* above.
