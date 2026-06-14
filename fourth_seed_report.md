# Fourth Seed Report: IM Tan, Jun Ying

*Prepared 2026-06-14 for FM Dino Ballecer ("Coach Dinosaur"). Roster player `5`.*

**Title:** IM | **Federation:** MAS | **FIDE (standard):** 2404

**Basis of this report.** Curated from the refreshed auto-generated dossier
[Opponent_IM_Tan_Jun_Ying.md](manual_sections/Opponent_IM_Tan_Jun_Ying.md), cross-checked against
Dino's self-audit
[Dino_Ballecer_Needs_Improvement.md](manual_sections/Dino_Ballecer_Needs_Improvement.md) and the
web-sourced [Live_Scouting_2026-06-13.md](manual_sections/Live_Scouting_2026-06-13.md).

- **101 games on file** = **101 over-the-board PGN games** + **0 Lichess online metadata rows**.
- **Engine claims below are from 101/101 OTB PGN games analysed by Stockfish 18 at depth 12.**
  There are **0 pending engine games**.
- **Command used:** `python prep_manual_app.py --analyze --scope player --player 5 --depth 12 --export`.

---

## 1. Executive Summary

Tan is a young, freshly titled Malaysian IM with a broad repertoire (**77 distinct openings**) and a
balanced but not dominant file score of **46W 15D 40L (53.0%)**. He scores **56.0% as White** and
**50.0% as Black**, so Dino should expect a playable game if the opening choice is practical rather
than theoretical for its own sake.

- **Freshness matters.** Live scouting says Tan is a new IM from 2025, still rising, and likely
  stronger in classical chess than his current 2404 rating fully shows. Treat 2404 as a floor, not a
  ceiling.
- **Clock pressure is part of the plan.** His rapid/blitz ratings are far below his standard rating
  and inactive. The practical goal is to pose fresh problems early, make him spend time, and avoid a
  memorized theoretical duel.
- **Best candidate target when Dino has White:** investigate the **Advance Caro-Kann** signal
  against Tan's Black file: **0W 1D 1L (25.0%)**, **ACPL 43.8**, and **9 serious errors over 72 Tan
  moves**. This is strong opponent evidence but a workload warning, because Dino has no practical
  Advance Caro-Kann reps in his own file.
- **Most realistic White-game fit:** stay closer to Dino's anti-Sicilian base. Tan scores well in
  the Anti-Sicilian family (**81.2%**), but the engine sample is volatile (**ACPL 41.2**, **18
  serious errors over 227 moves**). This is an engine-pressure target, not a result-score weakness.
- **Best candidate target when Dino has Black:** meet Tan's English/Reti move orders with a prepared
  setup. His **English Opening: Agincourt Defense, Neo-Catalan Declined** file is **0W 0D 4L
  (0.0%)**, and his broader Catalan/Reti family scores only **43.3%**.
- **One-sentence game plan:** *With White, use a prepared anti-Sicilian or narrow Advance Caro-Kann
  file to pose early decisions; with Black, neutralize his English/Reti systems without giving him a
  clean fianchetto setup, then keep pressure into rook endings where the sample shows defensive
  volatility.*

---

## 2. Opening Repertoire

**As White - 50 games, 56.0%.** Tan's White file leans heavily toward English, Reti, and fianchetto
move orders. The main target is not one trap line; it is making his flank openings solve concrete
early problems instead of letting him coast into a quiet squeeze.

**As Black - 51 games, 50.0%.** His Black file is more targetable by result, but Dino must filter the
targets through repertoire fit. The Sicilian/Modern area shows practical leaks, while some
high-scoring anti-Sicilian structures still show engine volatility.

### Confidence lines - do not let him coast

| Line | ECO | Games | Score | Suggested action |
|---|---|---:|---:|---|
| King's Indian Defense: Orthodox Variation, Positional Defense as White | E94 | 4 | 75.0% | As Black, avoid drifting into his comfortable KID squeeze |
| English Opening: Symmetrical Variation / Four Knights as White | A30/A35 | 4 | 87.5% | Prepare a concrete equalizing setup against 1.c4 / 1.Nf3 |
| Reti Opening: Advance Variation, Michel Gambit as White | A09 | 2 | 100.0% | Do not improvise against early Reti/fianchetto move orders |
| Queen's Pawn Game: Modern Defense as Black | A40 | 3 | 66.7% | Prepare a White setup; do not allow easy Modern/Indian development |
| Anti-Sicilian Counter-Package as Black | B-file systems | 8 | 81.2% | Engine-volatile but high-scoring; target only with real prep |
| IQP / Panov structures as White | B/D systems | 3 | 83.3% | Avoid as a main Black target; he is clean here in the sample |

### Repair / target lines - candidate targets only

| Line | ECO | Games | Score | Suggested action |
|---|---|---:|---:|---|
| English Opening: Agincourt Defense, Neo-Catalan Declined as White | A14 | 4 | 0.0% | Best Black-game opening target if Dino can drill the setup |
| Zukertort Opening: Kingside Fianchetto as White | A04 | 2 | 0.0% | Candidate Black target; small sample, same flank-opening theme |
| English Symmetrical: Anti-Benoni / Spielmann as White | A32 | 2 | 25.0% | Useful anti-English branch to review |
| Modern Defense: Standard Defense as Black | B06 | 2 | 0.0% | Candidate White target against his ...g6/...d6 setup |
| Sicilian Richter-Rauzer Modern cluster as Black | B60/B61 | 3 | 16.7% | Strong result signal, but it requires Open Sicilian workload |
| Advance Caro-Kann structures as Black | B12 family | 2 | 25.0% | Strong evidence target, but only if Dino trains this family first |

### Repertoire-fit check

- **White plan A: anti-Sicilian pressure.** Dino's own White file is strongest in Moscow/Rossolimo
  territory, and Tan's anti-Sicilian engine numbers are shaky despite his good results. This is the
  lowest-friction practical path.
- **White plan B: Advance Caro-Kann project.** The opponent evidence is excellent, but Dino's audit
  says he has zero practical games in the Advance Caro-Kann family. Use it only if there is time for
  targeted training games and model-game review.
- **White plan C: Open Sicilian/Richter-Rauzer.** Tan's Richter-Rauzer results are poor, but this is
  the highest workload option. Do not build a broad Open Sicilian file overnight.
- **Black plan: prepared anti-English/Reti.** Tan's A14 Neo-Catalan Declined score is 0/4, and his
  wider Catalan/Reti file is under 50%. Dino should prepare one setup against 1.c4 / 1.Nf3 / g3,
  not a scattered menu of equalizers.
- **Avoid Dino's own Black autopilot.** Dino's audit flags repeated Dragon losses. If Tan starts
  with 1.e4, Dino should not enter a leaky Dragon route just because Tan's Sicilian samples are
  volatile.

---

## 3. Phase Accuracy

*From 101 analysed OTB PGN games at depth 12. Lower ACPL = cleaner play.*

| Phase | ACPL |
|---|---:|
| Overall | 31.0 |
| Opening | 10.4 |
| Middlegame | 24.2 |
| **Endgame** | **42.3** |

Serious errors on file: **72 blunders, 158 mistakes, 245 inaccuracies**.

**Interpretation (within-player only).** Tan is much cleaner in the opening than later in the game.
The endgame is the least accurate phase by a wide margin, and the total blunder/mistake count is
high for a 101-game sample. The right conclusion is not "he is weak"; it is that Dino should keep
the position problem-rich after the opening and not assume the prep must win immediately.

> **Cross-player caution.** Dino's own depth-12 profile is based on only 7 analysed losses, with
> overall ACPL 26.7 and endgame ACPL 36.7. Endgame pressure against Tan is useful only if Dino also
> rehearses his own active-rook and drawing-defense technique.

---

## 4. Middlegame and Structure Notes

*Result score and engine accuracy are separate evidence types. The table below splits tagged
structure families by Tan's color, because Dino's practical choices depend on who has White.*

| Structure family | Tan color | Games | Result % | Moves | ACPL | Serious err | Read |
|---|---|---:|---:|---:|---:|---:|---|
| Advance Caro-Kann | Black | 2 | **25.0%** | 72 | **43.8** | **9** | Best evidence target, but Dino has no reps |
| Reversed-Sicilian / Flank Annexation | Black | 3 | 66.7% | 95 | **65.6** | **9** | Engine target, not a result weakness |
| Anti-Sicilian Counter-Package | Black | 8 | **81.2%** | 227 | **41.2** | **18** | Fits Dino, but must be prepared |
| Catalan / Reti Squeeze | Black | 7 | **35.7%** | 245 | 26.8 | 14 | Result target when Dino has White |
| Catalan / Reti Squeeze | White | 23 | 45.7% | 733 | 29.3 | 52 | Main Black-game structure to prepare against |
| Fianchetto KID / Grunfeld Complexes | Black | 4 | 50.0% | 142 | 39.5 | 11 | Volatile, but not clearly targetable |
| Fianchetto KID / Grunfeld Complexes | White | 2 | 75.0% | 60 | 38.5 | 8 | Avoid giving him easy comfort |
| IQP / Panov Attack | White | 3 | **83.3%** | 107 | **17.4** | 2 | Avoid as a Black-game target |

**Practical structure verdicts:**

- **Steer toward with White if trained:** Advance Caro-Kann. It has both result weakness and engine
  volatility, but Dino's own file has zero reps, so training must come first.
- **Steer toward with White as the realistic default:** anti-Sicilian pressure from Dino's existing
  Moscow/Rossolimo universe. Tan has scored well, so Dino needs middlegame ideas, not a label.
- **Investigate with White:** Catalan/Reti structures against Tan's Black repertoire. The result
  signal is good at 35.7%, but Dino has only one Catalan/Reti game in his own file.
- **Prepare carefully with Black:** Tan's English/Reti systems. His result score is poor enough to
  target, but he plays the structure often, so Dino needs a clean move order and model games.
- **Avoid with Black:** IQP/Panov as a main target. Tan's sample there is small but strong by both
  result and engine cleanliness.
- **Do not overread:** Reversed-Sicilian/flank structures have the highest ACPL, but Tan still
  scores 66.7% there. Use the engine volatility as a training pointer, not as proof of a result
  weakness.

---

## 5. Endgame and Simplified Positions

The endgame is Tan's least accurate phase (**ACPL 42.3**). The classified late-position sample
contains **40 endgame / simplified-position samples**, with the top categories:

| Category | Samples | Practical read |
|---|---:|---|
| Drawing defense failure | 16 | Drawable positions became losing repeatedly in the sample |
| Rook activity | 10 | Passive rook decisions show up often |
| Philidor | 8 | Rook-ending defensive technique appears repeatedly |
| Rook behind pawn | 4 | Passed-pawn rook placement is a recurring theme |
| Conversion failure | 2 | Some winning or pressing positions became non-winning |

Five clean samples to review:

| Game | Move | Severity | Category | Engine prefers | Training theme |
|---|---|---|---|---|---|
| vs Schnaider, Ilan | 40...Rd7 | blunder | Drawing defense failure | Qe6-f7 | Keep the defender active instead of passive holding |
| vs Ardila, Oscar Humberto | 39...Rg6 | blunder | Conversion failure | Rf6-h6 | Convert with active rook placement before pawn-grabbing |
| vs Smail, Benedict | 35.e3 | blunder | Philidor | Rf1xf4 | Know the defensive drawing setup before simplifying |
| vs Santiago Vilca, Christian Amilca | 35...a5 | blunder | Rook behind pawn / drawing defense | Rd8-b8 | Put the rook behind the passed pawn |
| vs Tran, Dang Minh Quang | 32...Rd7 | blunder | Rook activity | Rf7xf1 | Trade or activate before the rook becomes passive |

**The honest phrasing for Dino:** *The sample suggests practical chances in simplified rook endings,
especially around active rook defense, Philidor-type positions, and drawing-defense decisions. Dino
should train these positions before trying to make "grind him down" the match plan.*

---

## 6. Practical Game Plan for Dino

1. **Make the opening fresh, not broad.** Tan's standard-vs-speed rating gap suggests he is much
   better with time and prep than in improvisational play. Choose one line that asks early
   questions and forces him to spend clock.
2. **Default White plan: anti-Sicilian pressure.** This best fits Dino's current strengths. Tan's
   result score is high in anti-Sicilians, but the engine sample shows enough serious errors to make
   it a real practical target if Dino brings concrete middlegame ideas.
3. **Conditional White project: Advance Caro-Kann.** The Tan-specific evidence is strong, but Dino
   has zero practical reps in this family. Play it only after training games and model games, not as
   a surprise-only weapon.
4. **Do not overcommit to the Richter-Rauzer.** Tan's Open Sicilian result signal is attractive, but
   the workload is high. If Dino cannot drill a narrow line deeply, use Moscow/Rossolimo-style
   pressure instead.
5. **As Black, build one anti-English/Reti file.** Start with the A14 Neo-Catalan Declined losses
   and the broader Catalan/Reti family. The goal is to deny Tan a calm fianchetto squeeze and give
   him early practical decisions.
6. **Avoid IQP/Panov as a Black target.** Tan scores 83.3% with clean engine numbers there. Dino
   needs IQP/Panov training for his own development, but it is not the first Tan-specific lever.
7. **Keep pieces active into rook endings.** Tan's endgame ACPL is his worst phase, with 16
   drawing-defense failures and 10 rook-activity samples. This is a pressure plan only if Dino
   studies the sample positions first.
8. **Model games to study:** Tan's A14 losses vs Nguyen Ngoc Truong Son, Fus, Yu Jennifer, and
   Sumets; his recent Black losses vs Salemgareev and Le Quang Liem; then the five endgame samples
   in section 5.
9. **Freshness to-do before final prep.** Mine Malaysian-circuit junior games from 2026 before
   locking the file. Live scouting says Tan is still rising, so older PGN evidence may lag his
   current choices.

---

## Method & Caveats

- **Analysis command:** `python prep_manual_app.py --analyze --scope player --player 5 --depth 12 --export`.
- **Coverage:** 101 total games, 101 OTB PGNs, 0 Lichess metadata rows, 101/101 analysed at depth
  12, 0 pending.
- **Depth note:** one older depth-16 cache row remains in `GameAnalysis`, but the exporter and this
  report use the complete 101-game depth-12 run.
- **Evidence discipline applied:** every major claim has a count, score, ACPL, or concrete game
  sample; result-score targets and engine-accuracy targets are reconciled explicitly.
- **Known limitations:** depth 12 is a screening depth, not final engine truth; several PGNs are
  rapid/blitz events; some candidate targets rest on 2-4 game samples; Tan's 2026 Malaysian-circuit
  games should be mined before committing to a final opening file.
