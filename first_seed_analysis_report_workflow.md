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

## Next Player Workflow

For the next seed, run the same player-scope pattern:

```powershell
python prep_manual_app.py --analyze --scope player --player 3 --depth 12 --export
```

Then review:

```text
manual_sections/Opponent_GM_Shyaam_Nikhil_P.md
```

Repeat one player at a time so each dossier becomes complete and easy to verify.
