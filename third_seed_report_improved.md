# Third Seed Report: IM Morris, James

*Prepared 2026-06-14 for FM Dino Ballecer ("Coach Dinosaur"). Roster player `104`.*

**Title:** IM | **Federation:** AUS | **FIDE (standard):** 2423

**Basis of this report.** Curated from the refreshed auto-generated dossier
[Opponent_IM_Morris_James.md](manual_sections/Opponent_IM_Morris_James.md), cross-checked against
Dino's self-audit
[Dino_Ballecer_Needs_Improvement.md](manual_sections/Dino_Ballecer_Needs_Improvement.md) and the
web-sourced [Live_Scouting_2026-06-13.md](manual_sections/Live_Scouting_2026-06-13.md).

- **100 games on file** = **100 over-the-board PGN games** + **0 Lichess online records without full move lists**.
- **Engine claims below are from 100/100 OTB PGN games analysed by Stockfish 18 at depth 12.**
  There are **0 pending engine games**.
- **Command used:** `python prep_manual_app.py --analyze --scope player --player 104 --depth 12 --export`.

---

## 1. Executive Summary

Morris is an active 2423 IM with a broad, offbeat repertoire (**62 distinct openings**) and a file
score of **42W 28D 30L (56.0%)**. His White score is better than his Black score: **60.4% as White**
versus **51.9% as Black**, so Dino's cleanest practical targets are likely to come when Dino has
White.

- **Freshness matters.** Live scouting says Morris was active in May 2026, strong across all three
  time controls, and top seed at the Australian Open / Oceania Zonal. Do not expect a clock edge.
- **Best possible target as White:** steer toward Catalan/Reti squeeze structures against his
  Black repertoire. Morris scores only **1W 1D 3L (30.0%)** there over five tagged games, with
  **ACPL 30.0** and **7 serious errors over 165 Morris moves**.
- **Secondary White target:** prepare specifically for the **Nimzowitsch Defense: Williams
  Variation**. Morris is **0W 3D 4L (21.4%)** as Black over seven games in that line.
- **Do not lean too hard on the engine table.** The Fianchetto KID / Grunfeld complex shows engine
  strain (**ACPL 29.0**) but Morris scores **80.0%** there as Black. Treat it as a study zone, not an
  automatic target.
- **As Black, avoid Dino's autopilot Dragon leak.** Morris has a strong anti-Sicilian/Closed
  Sicilian White file, while Dino's own audit flags repeated losses after
  `e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6`.
- **One-sentence game plan:** *With White, make Morris solve either a prepared Catalan/Reti squeeze
  or a concrete anti-Nimzowitsch line; with Black, choose a durable anti-1.e4 setup that avoids
  Dino's leaky Dragon habits and keeps enough tension to test Morris's late-game technique.*

---

## 2. Opening Repertoire

**As White - 48 games, 60.4%.** Morris mixes mainline 1.e4 territory with anti-Sicilian and offbeat
systems: King's Knight Opening, French Chigorin, Closed Sicilian, Caro-Kann Exchange, Najdorf, and
Nimzo-Larsen move orders. Dino should expect flexibility rather than one fixed opening setup.

**As Black - 52 games, 51.9%.** The Black repertoire is more targetable. The main result weakness is
his Nimzowitsch Defense: Williams Variation; the main structure weakness is Catalan/Reti when he has
Black.

### Confidence lines - do not let him coast

| Line | ECO | Games | Score | Suggested action |
|---|---|---:|---:|---|
| Pseudo Queen's Indian Defense | A47 | 4 | 100.0% | Prepare a neutralizer as White; do not wander into his setup |
| Sicilian Defense: Closed | B23 | 4 | 100.0% | As Black, avoid casual Sicilian handling and force him to solve early |
| Zukertort Opening: Nimzo-Larsen Variation | A05 | 3 | 100.0% | Prepare a compact response to 1.Nf3 / 1.b3 style move orders |
| Fianchetto KID / Grunfeld complex as Black | A/E systems | 5 | 80.0% | Avoid as a main target unless Dino has model games ready |
| Anti-Sicilian Counter-Package as White | B-file systems | 13 | 73.1% | Do not let his anti-Sicilian comfort meet Dino's known Dragon problem |

### Repair / target lines - candidate targets only

| Line | ECO | Games | Score | Suggested action |
|---|---|---:|---:|---|
| Nimzowitsch Defense: Williams Variation as Black | B00 | 7 | 21.4% | Best concrete White target if Dino starts with 1.e4 |
| Catalan / Reti structures when Morris is Black | A/E systems | 5 | 30.0% | Best structure target if Dino can drill a 1.Nf3 / c4 / d4 move order |
| Caro-Kann Defense: Exchange Variation as White | B13 | 3 | 33.3% | Possible Black target only if Dino can play the Caro-Kann confidently |
| Sicilian Defense: Najdorf Variation as White | B90 | 2 | 25.0% | Tiny sample; do not build a new Najdorf plan around this alone |
| IQP / Panov structures as White | B/D systems | 3 | 33.3% | Useful training theme, but too small as a standalone match plan |

### Repertoire-fit check

- **White plan A: Catalan/Reti squeeze.** This is the best Morris-specific lever, but Dino has only
  a small Catalan/Reti footprint in his own file. Use it only if there is enough time to drill the
  move order and model middlegames.
- **White plan B: 1.e4 anti-Nimzowitsch.** This is lower workload because Dino already plays 1.e4
  and scores well in anti-Sicilian systems. Prepare a direct answer to `1.e4 Nc6` rather than
  improvising against the Williams setup.
- **Black plan: no Dragon by habit.** Morris's White file includes anti-Sicilian and Closed Sicilian
  success, and Dino's own repeated-loss line is the Dragon move order. Pick a safer prepared setup
  unless the Dragon repair work is complete.
- **Caro-Kann target is conditional.** Morris's Caro-Kann Exchange score is poor, but Dino's audit
  also says his Advance Caro-Kann family has zero practical reps. Do not choose the Caro-Kann just
  because the table marks a target.

---

## 3. Phase Accuracy

*From 100 analysed OTB PGN games at depth 12. Lower ACPL = cleaner play.*

| Phase | ACPL |
|---|---:|
| Overall | 25.8 |
| Opening | 11.1 |
| Middlegame | 19.1 |
| **Endgame** | **36.2** |

Serious errors on file: **53 blunders, 100 mistakes, 237 inaccuracies**.

**Interpretation (within-player only).** Morris is cleanest in the opening and least accurate after
simplification. The gap is large enough to shape prep, but the right wording is still evidence-based:
the sample suggests late-game volatility, not a blanket claim that he is weak in endgames.

> **Cross-player caution.** Dino's own depth-12 engine sample is only 7 analysed losses, with overall
> ACPL 26.7 and endgame ACPL 36.7. Endgame pressure against Morris is useful only if Dino also drills
> his own active-rook and drawing-defense technique.

---

## 4. Middlegame and Structure Notes

*Results and engine accuracy are separate evidence types. The table below splits tagged
structure families by Morris's color, because Dino's practical choices depend on who has White.*

| Structure family | Morris color | Games | Result % | Moves | ACPL | Serious err | Read |
|---|---|---:|---:|---:|---:|---:|---|
| Catalan / Reti Squeeze | Black | 5 | **30.0%** | 165 | **30.0** | 7 | Best White-game target |
| Fianchetto KID / Grunfeld Complexes | Black | 5 | **80.0%** | 134 | 29.0 | 3 | Volatile but high-scoring; avoid as default |
| Reversed-Sicilian / Flank Annexation | White | 12 | 62.5% | 351 | **31.0** | **23** | Pressure possible, but not a result weakness |
| Anti-Sicilian Counter-Package | White | 13 | 73.1% | 328 | 20.1 | 15 | Prepare neutralizer as Black |
| IQP / Panov Attack | White | 3 | 33.3% | 106 | 19.9 | 4 | Interesting, but small sample |
| Catalan / Reti Squeeze | White | 4 | 62.5% | 131 | 20.2 | 8 | Prepare a steady setup if Dino has Black |

**Practical structure verdicts:**

- **Steer toward with White:** Catalan/Reti pressure if Dino can prepare the move order. This has
  both a poor-result signal and an engine-pressure signal when Morris has Black.
- **Steer toward with White as a lower-load option:** 1.e4 with specific anti-Nimzowitsch prep.
  Morris's Williams Variation score is the cleanest opening-line result weakness.
- **Avoid with White unless prepared:** Fianchetto KID / Grunfeld structures. Morris's engine ACPL
  is not low there, but his result score is excellent.
- **Prepare carefully with Black:** anti-Sicilian and Closed Sicilian structures. Morris scores well
  there, and Dino's Dragon audit makes casual Sicilian play too expensive.
- **Do not overread:** IQP/Panov is a useful theme for Dino's own training, but three Morris games
  are not enough to make it the primary match plan.

---

## 5. Endgame and Simplified Positions

The endgame is Morris's least accurate phase (**ACPL 36.2**). The classified late-position sample
contains **29 endgame / simplified-position samples**, with the top categories:

| Category | Samples | Practical read |
|---|---:|---|
| Rook behind pawn | 10 | Passed-pawn rook placement recurs in the sample |
| Philidor | 9 | Rook-ending defensive technique appears repeatedly |
| Conversion failure | 4 | Winning or pressing positions can become non-winning |
| Rook activity | 4 | Passive rook decisions show up in simplified positions |
| Drawing defense failure | 2 | Some drawable positions became losing |

Five clean samples to review:

| Game | Move | Severity | Category | Engine prefers | Training theme |
|---|---|---|---|---|---|
| vs Gavilan Diaz, Mario | 40.Rg1 | blunder | Rook activity / rook behind pawn | Rb7-b6 | Keep the rook active and behind the passer |
| vs Al Hosani, Omran | 34.Nxf5 | blunder | Rook behind pawn / conversion failure | Rf1-c1 | Improve the rook before cashing tactics |
| vs Bortnyk, Olexandr | 31...Rxe5 | blunder | Philidor / drawing defense | Re8-e6 | Hold flexible rook defense instead of grabbing |
| vs Gavilan Diaz, Mario | 36.Rxd7 | blunder | Rook activity / conversion failure | Ra7-b7 | Preserve active rook support before material grabs |
| vs Vokhidov, Shamsiddin | 38.Rg4 | blunder | Philidor / rook behind pawn | Rf4-f3 | Keep the rook active in the passer's lane |

**The honest phrasing for Dino:** *The sample suggests practical chances in simplified rook endings,
especially around active-rook play, Philidor-type defense, and conversion technique. Dino still has
to train these positions himself before making "grind him down" the plan.*

---

## 6. Practical Game Plan for Dino

1. **Choose the White workload deliberately.** The highest-upside Morris target is a Catalan/Reti
   squeeze, but it is not Dino's deepest existing file. If prep time is short, use 1.e4 and prepare
   the anti-Nimzowitsch branch instead.
2. **Prepare for `1.e4 Nc6`.** Morris's Nimzowitsch Defense: Williams Variation is 21.4% over seven
   games. Dino needs one clear setup and two model games, not a broad survey.
3. **Do not chase the Grunfeld/KID label blindly.** Morris scores 80.0% in the tagged Fianchetto
   KID / Grunfeld structures as Black. The engine sees volatility, but the result table says he
   knows how to score there.
4. **As Black, repair or replace the Dragon route.** Morris's anti-Sicilian/Closed Sicilian success
   maps badly onto Dino's repeated Dragon-loss sequence. Use a safer prepared answer unless the
   Dragon file has been repaired.
5. **Treat Caro-Kann Exchange as conditional.** Morris scores only 33.3% there as White, but Dino
   should use it only if his Caro-Kann structures are ready. Do not create a new Black repertoire
   overnight.
6. **Keep tension into simplified positions.** Morris's endgame ACPL is his worst phase, with rook
   activity, Philidor, and conversion themes. This is a practical pressure plan, not an opening-only
   trap plan.
7. **Model games to study:** the Nimzowitsch Williams losses vs Parondo, Kevlishvili, Martinez
   Alcantara, and Sanal; then the five endgame samples in section 5.
8. **Freshness to-do before final prep.** Mine Morris's Oceania Zonal 2026 games before locking the
   opening choice. Live scouting says his recent activity is high enough that the PGN sample may lag
   his current repertoire.

---

## Method & Caveats

- **Analysis command:** `python prep_manual_app.py --analyze --scope player --player 104 --depth 12 --export`.
- **Coverage:** 100 total games, 100 OTB PGNs, 0 Lichess records without full move lists, 100/100
  analysed at depth 12, 0 pending.
- **Depth note:** two older depth-16 cache rows remain in `GameAnalysis`, but the exporter now uses
  the active `--depth 12` setting, so the Morris dossier and this report both cite the complete
  100-game depth-12 run.
- **Evidence discipline applied:** every major claim has a count, score, ACPL, or concrete game
  sample; result targets and engine-accuracy targets are checked against each other.
- **Known limitations:** depth 12 is a screening depth, not final engine truth; several PGNs are
  rapid/blitz events; some candidate targets rest on 2-5 game samples; the freshest 2026 Zonal games
  should be mined before committing to a final opening file.
