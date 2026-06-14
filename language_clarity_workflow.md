# Language Clarity Workflow

Use this workflow when simplifying the curated seed scouting reports for FM Dino Ballecer. The
standard is:

> Plain enough for a young reader, precise enough for an IM-strength prep file.

The goal is simple narrative, not childish language. Make engine-heavy or computer-chess-heavy prose
easier to understand while preserving the chess meaning, evidence discipline, numbers, and report
structure.

## Source of Truth and Scope

The original Markdown reports are the source inputs:

- `first_seed_report.md`
- `second_seed_report.md`
- `third_seed_report.md`
- `fourth_seed_report.md`
- `fifth_seed_report.md`
- `sixth_seed_report.md`
- `seventh_seed_report.md`
- `eighth_seed_report.md`
- Any future `*_seed_report.md`

Create a separate improved Markdown report using the `_improved` suffix, then generate the matching
standalone DOCX from that improved Markdown. Never hand-edit a DOCX file.

Use this naming pattern:

- Source: `first_seed_report.md`
- Improved Markdown: `first_seed_report_improved.md`
- Improved DOCX: `first_seed_report_improved.docx`

Do not use alternate names such as `*_clarified.md`, `*_plain.md`, or ad hoc DOCX variants. The
standard output stem is always `<original-stem>_improved`.

When the user asks for a range such as "Language clarity from 1 to 8," process the seed reports one
by one in seed order. Finish the improved Markdown, improved DOCX, and verification for the current
seed before moving to the next seed.

| Seed | Source | Improved Markdown | Improved DOCX |
|---:|---|---|---|
| 1 | `first_seed_report.md` | `first_seed_report_improved.md` | `first_seed_report_improved.docx` |
| 2 | `second_seed_report.md` | `second_seed_report_improved.md` | `second_seed_report_improved.docx` |
| 3 | `third_seed_report.md` | `third_seed_report_improved.md` | `third_seed_report_improved.docx` |
| 4 | `fourth_seed_report.md` | `fourth_seed_report_improved.md` | `fourth_seed_report_improved.docx` |
| 5 | `fifth_seed_report.md` | `fifth_seed_report_improved.md` | `fifth_seed_report_improved.docx` |
| 6 | `sixth_seed_report.md` | `sixth_seed_report_improved.md` | `sixth_seed_report_improved.docx` |
| 7 | `seventh_seed_report.md` | `seventh_seed_report_improved.md` | `seventh_seed_report_improved.docx` |
| 8 | `eighth_seed_report.md` | `eighth_seed_report_improved.md` | `eighth_seed_report_improved.docx` |

Out of scope for a clarity pass:

- `seed_analysis_report_workflow.md`
- `Tournament_Preparation_Manual.docx`
- Everything under `manual_sections/`

Those files are internal workflow, source, dossier, or scouting material. The clarity pass is for the
reader-facing seed reports only.

## Preserve the Chess

Do not change chess content or evidence. Preserve:

- Opening names
- ECO codes
- Move notation
- Ratings
- Game counts
- Scores and percentages
- ACPL values
- Stockfish depth
- Classical, online, rapid, blitz, and metadata caveats
- Evidence caveats and sample-size warnings
- Conclusions
- Target recommendations
- Confidence levels

Do not strip a technical term that carries real chess meaning. If a term is necessary, either explain
it briefly at first use or rewrite the surrounding sentence so the term is easier to follow.

Do not make the report vague, childish, or non-chess. Dino should still be able to use it as serious
tournament preparation.

## Rewrite Examples

Use these as prose examples, not as a global find/replace dictionary.

| Dense phrase | Clearer prose option |
|---|---|
| `engine fingerprint` | `engine pattern` |
| `phase accuracy` | `how clean he plays in the opening, middlegame, and endgame` |
| `candidate target` | Keep this evidence term unless the nearby wording already makes the caution clear; then `possible target` may work in body prose |
| `repair line` | `line Dino needs to fix or prepare` |
| `metadata rows` | `online records without full move lists` |
| `small-sample volatility` | `an uneven result from only a few games` |
| `soft-by-result, clean-by-engine` | `the results are poor, but the moves were not full of mistakes` |

Apply the same style to similar phrases: keep the chess idea, reduce the computer-chess wording, and
keep the evidence next to the claim.

## Sentence-Level Rules

- Use one main idea per sentence.
- Prefer active voice.
- Break up jargon piles.
- Keep the count, score, ACPL, depth, or sample size close to the claim it supports.
- Use short parenthetical explanations only when they help.
- Keep strong claims tied to evidence. For example, prefer "the sample shows" over "he is bad at."

## Structure Protection

Do not apply rewrite examples mechanically. They are for body prose only.

Keep the fixed H2 report sections unchanged across all reports:

- `Executive Summary`
- `Opening Repertoire`
- `Phase Accuracy`
- `Middlegame and Structure Notes`
- `Endgame and Simplified Positions`
- `Practical Game Plan for Dino`
- `Method & Caveats`

The numbered prefixes may stay as written in each report, such as `## 3. Phase Accuracy`.
H3 subsections are report-specific. Do not standardize them across reports unless the user
explicitly asks for a structural rewrite.

Do not rewrite table column headers or other structural anchors, including:

- `Read`
- `Suggested action`
- `Line`
- `ECO`
- `Games`
- `Score`
- `ACPL`
- `Phase`
- `Subset`
- `Record`
- `Overall ACPL`
- `Opening`
- `Middlegame`
- `Endgame`
- `Structure family`
- `<name> color` / `His color`
- `Result %`
- `Moves`
- `Err`
- `Serious err`
- `B/M`
- `Errors`
- `Blunders`
- `Mistakes`
- `Game`
- `Move`
- `Severity`
- `Theme`
- `Category`
- `Engine prefers`
- `Training theme`
- `Practical read`

For example, do not change the heading `Phase Accuracy` to `How Clean He Plays in the Opening,
Middlegame, and Endgame`. That expansion belongs only inside a body sentence where it reads
naturally.

## Table Rules

Keep each report's table structure and numbers stable. Table schemas differ across reports, so do
not force one report's table shape onto another.

Simplify table text only where it improves readability. Start with prose-heavy cells such as `Read`
or `Suggested action`. Do not change numeric cells, opening names, ECO codes, move notation, or
evidence labels.

Column names affect DOCX rendering. The builder sizes tables by column count, and it has special
handling for a five-column table whose last header starts with `Suggested`. Renaming `Suggested
action` or changing a column count can silently change the rendered layout.

Do not expand a table into prose unless the original table is genuinely unclear. If prose is needed,
add a short sentence before or after the table without changing the table's evidence.

## Markdown Compatibility

Stay within the Markdown subset supported by `build_standalone_report.py`:

- Headings
- `**bold**`
- `*italic*`
- Inline `code`
- Tables
- Bullets
- Numbered lists
- Block quotes
- Links, which render as plain text in DOCX

Markdown links are allowed, but the DOCX builder renders only the link text and drops the URL. Do not
rely on clickable targets in the final DOCX. Do not add images; image syntax is not supported and can
render as broken plain text.

Do not add unsupported Markdown constructs such as footnotes, HTML blocks, definition lists,
strikethrough, task lists, images, or fenced code/diagram blocks. The DOCX builder will not render
them reliably.

## Workflow

1. Check the current worktree:

   ```powershell
   git status --short
   ```

   Note and preserve any in-flight user changes. Do not revert unrelated dirty files.

2. Read the target Markdown report before creating the improved copy.

3. Identify prose that is too engine-heavy or computer-chess-heavy. Focus on sentences where the
   chess meaning is sound but the wording is harder than needed.

4. Create the improved Markdown file using the `_improved` suffix, such as
   `first_seed_report_improved.md`. Rewrite only unclear prose in that improved file. Preserve chess
   meaning, section structure, table structure, evidence, and numbers.

5. Build the improved standalone DOCX from the improved Markdown source:

   ```powershell
   python -X utf8 build_standalone_report.py <stem>_improved.md <stem>_improved.docx --title "<existing report title>"
   ```

   Use the existing report title so the DOCX running header stays unchanged. The exact stems and
   titles are listed in the seed queue table in `seed_analysis_report_workflow.md`.

   Do not rely on H1 inference for `first_seed_report.md`: its H1 is `First Seed Scouting Report -
   GM Vignesh, N R`, but its canonical running header is `First Seed Report: GM Vignesh, N R`.
   Always pass:

   ```powershell
   python -X utf8 build_standalone_report.py first_seed_report_improved.md first_seed_report_improved.docx --title "First Seed Report: GM Vignesh, N R"
   ```

   For other reports, `--title` may be omitted only when the Markdown H1 is already the intended
   running header.

6. Optionally render-check the DOCX when final layout quality matters. Use the Step 3 render-check
   procedure in `seed_analysis_report_workflow.md`, which uses LibreOffice `soffice.com` and Poppler
   `pdftoppm.exe`. Delete any `*_render` scratch artifacts afterward unless the user asks to keep
   them.

7. Review the diff against the original report. Confirm the improved report changed clarity only,
   not chess meaning, conclusions, structure, or numbers.

For a multi-seed request, repeat steps 2 through 7 for each requested seed in order. For "Language
clarity from 1 to 8," start with `first_seed_report.md` and continue through
`eighth_seed_report.md`. Do not skip ahead; keep each seed's improved Markdown and DOCX as a complete
pair before starting the next seed.

## Verification Checklist

Before finishing a clarity pass, confirm:

- The fixed section headings, including `Method & Caveats`, are unchanged.
- Table headers and structural anchors are unchanged.
- Opening names, ECO codes, move notation, ratings, counts, scores, ACPL values, depth, and evidence
  caveats are unchanged.
- Conclusions, target recommendations, and confidence levels are unchanged.
- Any simplified technical phrase still means the same chess thing.
- The improved DOCX was generated from the improved Markdown, not hand-edited.
- The improved files use the required `_improved` stem, such as `first_seed_report_improved.md` and
  `first_seed_report_improved.docx`.
- The original seed report files remain available for comparison.
- The build command and title handling match `build_standalone_report.py`.

No automated tests are required for this workflow document itself.
