# Second Seed Report: GM Shyaam, Nikhil P

*Prepared 2026-06-14 for FM Dino Ballecer ("Coach Dinosaur"). Roster player `3`.*

**Title:** GM | **Federation:** IND | **FIDE (standard):** 2435

**Basis of this report.** Curated from the refreshed auto-generated dossier
[Opponent_GM_Shyaam_Nikhil_P.md](manual_sections/Opponent_GM_Shyaam_Nikhil_P.md), cross-checked
against Dino's self-audit
[Dino_Ballecer_Needs_Improvement.md](manual_sections/Dino_Ballecer_Needs_Improvement.md) and the
web-sourced [Live_Scouting_2026-06-13.md](manual_sections/Live_Scouting_2026-06-13.md).

- **101 games on file** = **101 over-the-board PGN games** + **0 Lichess online records without full move lists**.
- **Engine claims below are from 101/101 OTB PGN games analysed by Stockfish 18 at depth 12.**
  There are **0 pending engine games**. Unlike the first seed, there is no Lichess-only layer without
  move lists here.
- **Command used:** `python prep_manual_app.py --analyze --scope player --player 3 --depth 12 --export`.

---

## 1. Executive Summary

Shyaam is an active 2435 GM with a broad, flexible repertoire (**79 distinct openings**) and a file
score of **44W 43D 14L (64.9%)**. His White results are stronger than his Black results: **71.4% as
White** versus **58.7% as Black**, so Dino's best practical chances are more likely to come when
Dino has White.

- **Freshness matters.** Live scouting says Shyaam scored 7/9 at Sevilla 2026 and won the side blitz
  with 6/7, but also lost 11 FIDE points over 9 standard games in June 2026. Treat him as active and
  prepared, with possible recent repertoire drift from the ChessBase sample.
- **Best possible target as White:** stress his Sicilian setup. The dossier flags his **Najdorf
  family as Black** at **1W 1D 2L (37.5%)**, and the engine split shows his **Anti-Sicilian
  Counter-Package as Black** has the highest practical error density here (**ACPL 16.3, 5 serious
  errors over 174 moves**).
- **Do not oversimplify the evidence.** Shyaam still scores **4W 0D 1L (80.0%)** as Black in the
  Anti-Sicilian family, so this is a target because the engine found pressure points, not because his
  results are poor.
- **As Black, prepare for quiet first moves.** His White comfort zone is 1.Nf3 / King's Indian Attack
  / Nimzo-Larsen: Zukertort **4/4**, KIA with ...e6 **3/3**, and the Nimzo-Larsen complex unbeaten
  in the sample.
- **One-sentence game plan:** *With White, keep Dino in his existing Moscow/Rossolimo/KIA-style
  anti-Sicilian universe and make Shyaam solve middlegame problems there; with Black, neutralise
  Shyaam's 1.Nf3/KIA move orders without drifting into Dino's own under-rehearsed Dragon or Benoni
  liabilities.*

---

## 2. Opening Repertoire

**As White - 49 games, 71.4%.** Shyaam leans on flexible flank and KIA systems: Zukertort, King's
Indian Attack, and Nimzo-Larsen. These are not single-line trap targets; they are move-order
systems where Dino needs a clear setup.

**As Black - 52 games, 58.7%.** His Black file is more targetable. The main possible target is the
Sicilian/Najdorf complex, but the recommendation must pass Dino's repertoire-fit test.

### Confidence lines - do not let him coast

| Line | ECO | Games | Score | Suggested action |
|---|---|---:|---:|---|
| Zukertort Opening | A05 | 4 | 100.0% | Prepare neutralizer as Black; expect 1.Nf3 move orders |
| King's Indian Attack, with ...e6 | A07 | 3 | 100.0% | Avoid autopilot ...e6 KIA structures unless Dino has model games ready |
| Nimzo-Larsen Attack complex | A01/A06 | 5 | 80.0% | Prepare a compact setup; do not improvise against 1.b3/1.Nf3 |
| Reversed-Sicilian / Flank family as White | A-file systems | 11 | 90.9% | Avoid as Black; this is a comfort zone |
| Catalan / Reti family as White | A04-A14/E00s | 18 | 86.1% | Avoid entering without concrete prep |

### Repair / target lines - candidate targets only

| Line | ECO | Games | Score | Suggested action |
|---|---|---:|---:|---|
| Sicilian Defense: Najdorf Variation as Black | B90/B94 | 4 | 37.5% | Target only with a concrete prepared line; do not improvise an Open Sicilian |
| King's Indian Attack: Symmetrical Defense as Black | A05 | 2 | 25.0% | Candidate White target if Dino can reach a familiar KIA structure |
| Catalan / Reti family as Black | A/E systems | 4 | 50.0% | Weak result flag, but the engine says he played cleanly; not a standalone target |
| Reversed-Sicilian / Flank family as Black | A-file systems | 3 | 33.3% | Tiny result sample; use only if it fits Dino's existing White move order |

### Repertoire-fit check

- **Keep Dino's anti-Sicilian base.** Dino's own White file is strongest in the Moscow/Rossolimo
  zone: Moscow Main Line **9/9**, Moscow **5/5**, Rossolimo **2/2**. This maps naturally to
  Shyaam's least accurate aggregate structure family, but with an important caveat: Shyaam scores
  well there by result, so Dino needs concrete middlegame ideas, not just a familiar label.
- **Najdorf target: conditional.** Shyaam's Najdorf results as Black are poor enough to investigate,
  but Dino's current file does not show the Open Sicilian as a main weapon. Prepare one narrow
  Najdorf sideline only if Dino can drill it; otherwise use Moscow/Rossolimo to deny Shyaam his
  normal Najdorf.
- **KIA target: plausible.** Dino already has King's Indian Attack material in his White repertoire
  (especially vs the French). Shyaam's KIA Symmetrical sample as Black is only two games, but 25.0%
  makes it worth a focused check.

---

## 3. Phase Accuracy

*From 101 analysed OTB PGN games at depth 12. Lower ACPL = cleaner play.*

| Phase | ACPL |
|---|---:|
| Overall | 14.5 |
| Opening | 9.9 |
| Middlegame | 13.2 |
| **Endgame** | **17.0** |

Serious errors on file: **8 blunders, 43 mistakes, 173 inaccuracies**.

**Interpretation (within-player only).** Shyaam is cleanest in the opening and least accurate in the
endgame. The gap is meaningful, but it is not a broad "bad endgame" claim: ACPL 17.0 over a 101-game
GM sample is still strong. The practical read is that Dino should keep pressure after simplification
instead of assuming the opening must decide the game.

> **Cross-player caution.** Dino's own depth-12 profile is much shakier and much smaller: 7 analysed
> games, overall ACPL 26.7, endgame ACPL 36.7. Endgame pressure is a chance only if Dino sharpens his
> own rook-ending and drawing-defense technique first.

---

## 4. Middlegame and Structure Notes

*Engine pattern over the core structure families at depth 12. Results and engine accuracy are
separate evidence types; where they disagree, the report says so.*

| Structure family | Games (result) | Result % | Moves | ACPL | Serious err | Read |
|---|---:|---:|---:|---:|---:|---|
| Anti-Sicilian Counter-Package | 12 | 66.7% | 425 | **14.6** | **7** | Engine-pressure target, but not a result weakness |
| Fianchetto KID / Grunfeld Complexes | 1 | 50.0% | 19 | 13.1 | 0 | Too small to target |
| Catalan / Reti Squeeze | 22 | **79.5%** | 718 | 13.1 | 8 | Avoid as Black; comfort zone when he has White |
| IQP / Panov Attack | 2 | 75.0% | 66 | 12.9 | 1 | Too small; useful for Dino training, not a Shyaam target |
| Reversed-Sicilian / Flank Annexation | 14 | 78.6% | 442 | **12.3** | 2 | Avoid as Black; accurate aggregate |

**Color split that matters for Dino:**

- **Anti-Sicilian when Shyaam is Black:** 5 games, **80.0% result**, but **ACPL 16.3** and **5 serious
  errors**. This is the most useful tension in the file: he has scored well, yet the engine sees
  pressure points.
- **Catalan / Reti when Shyaam is White:** 18 games, **86.1%**. Do not let him get an easy 1.Nf3 /
  Reti squeeze as White.
- **Reversed-Sicilian / Flank when Shyaam is White:** 11 games, **90.9%**. Another avoid zone when
  Dino has Black.
- **Advance Caro-Kann:** 0 games. Dino still needs to train this family from his own audit, but it
  is not evidence for or against Shyaam.

**Practical structure verdicts:**

- **Steer toward with White:** Dino's prepared Moscow/Rossolimo/KIA anti-Sicilian positions, because
  they are already in his file and Shyaam's engine accuracy is most stressed there.
- **Steer toward only with proof:** Open Sicilian Najdorf targets. The result signal is real, but
  switching Dino into a broad Open Sicilian workload for one opponent is a bad trade unless the line
  is narrow and drilled.
- **Avoid with Black:** Shyaam's Reti/Catalan and reversed-flank comfort systems. Prepare a reliable
  setup against 1.Nf3, 1.b3, and KIA move orders.
- **Do not overread:** Fianchetto KID/Grunfeld and IQP/Panov samples are too small here, even though
  Dino needs IQP/Panov training for his own manual.

---

## 5. Endgame and Simplified Positions

The endgame is Shyaam's least accurate phase (**ACPL 17.0**). The classified late-position sample
contains **18 endgame / simplified-position samples**, with the top categories:

| Category | Samples | Practical read |
|---|---:|---|
| Conversion failure | 5 | Winning or pressing positions can become non-winning |
| Philidor | 5 | Rook-ending defensive technique appears repeatedly |
| Drawing defense failure | 3 | Some drawable positions became losing |
| Rook behind pawn | 3 | Passed-pawn rook placement is a recurring theme |
| Rook activity | 2 | Passive rook decisions show up in the sample |

Five clean samples to review:

| Game | Move | Severity | Category | Engine prefers | Training theme |
|---|---|---|---|---|---|
| vs Shen, Ree Herng | 31...Rf6 | blunder | Philidor / conversion failure | Rf4-f1 | Keep the rook active in the defensive zone |
| vs Nagare, Kaivalya Sandip | 40...Na7 | mistake | Drawing-defense failure | Nc6-d4 | Centralise the defender instead of retreating passively |
| vs Krishnan, Ritvik | 33...Rb6 | mistake | Philidor / drawing defense | Rb8xb3 | Use active rook counterplay, not passive holding |
| vs Dotzer, Lukas | 34...Bc7 | mistake | Drawing-defense failure | Bd6-e7 | Preserve defensive coordination in simplified play |
| vs Gavrilescu, David | 37.Ra7 | mistake | Rook activity / rook behind pawn / conversion | Be4-d5 | Improve the active piece before chasing material |

**The honest phrasing for Dino:** *The sample suggests practical chances in simplified rook and
minor-piece endings, especially around active-rook play, Philidor-type defense, and conversion
technique. This is a pressure plan, not a claim that Shyaam is weak in endgames.*

---

## 6. Practical Game Plan for Dino

1. **Start from Dino's actual White weapons.** The best fit is the Moscow/Rossolimo/KIA
   anti-Sicilian package. It keeps Dino in known territory while attacking Shyaam's highest-error
   structure family.
2. **Treat the Najdorf as a narrow project, not a new repertoire.** Shyaam's Najdorf as Black is
   37.5% over 4 games, including recent 2026 losses. Prepare one concrete sideline if Dino can drill
   it; otherwise use the Moscow/Rossolimo to avoid his main Najdorf preparation.
3. **Check the KIA Symmetrical target.** Shyaam is 25.0% over 2 games as Black in that line. The
   sample is small, but Dino already has KIA themes in his file, so this is more realistic than
   learning a fresh Open Sicilian branch.
4. **As Black, build a 1.Nf3 / KIA / Nimzo-Larsen neutralizer.** Shyaam's White comfort lines are
   high-scoring and flexible. Dino should choose a setup he understands, not drift into generic
   ...e6 KIA structures where Shyaam is 3/3.
5. **Do not ignore Dino's own Black weaknesses.** Dino's audit flags a repeated Dragon sequence with
   3 losses and a broader Black score gap. If Shyaam chooses 1.e4, Dino should not enter a leaky
   Dragon by habit.
6. **Keep endgames alive, but train first.** Shyaam's endgame phase is his least accurate, with
   rook-ending and drawing-defense samples. Dino's own endgame sample is also weak, so this plan
   requires rook-ending reps before the event.
7. **Model games to study:** the recent Black losses vs Weerasekara (Nimzo-Indian, 2026.05.21),
   Siva Kumar (Najdorf, 2026.05.19), Sathvik (Najdorf, 2026.04.16), and Balakrishnan (Najdorf,
   2026.01.16), plus the five endgame samples in section 5.
8. **Freshness to-do before final prep.** Pull Shyaam's Sevilla 2026 and June 2026 games before
   locking the opening choice; live scouting says his recent activity is high enough that the
   ChessBase sample may lag his current repertoire.

---

## Method & Caveats

- **Analysis command:** `python prep_manual_app.py --analyze --scope player --player 3 --depth 12 --export`.
- **Coverage:** 101 total games, 101 OTB PGNs, 0 Lichess records without full move lists, 101/101
  analysed at depth 12, 0 pending.
- **Evidence discipline applied:** every major claim has a count, score, ACPL, or concrete game
  sample; Lichess records without full moves are separated from engine analysis; result targets and
  engine-accuracy targets are checked against each other.
- **Known limitations:** depth 12 is a screening depth, not final engine truth; some candidate
  targets rest on 2-4 game samples; several OTB PGNs are rapid/blitz events; the freshest Sevilla /
  June 2026 games should be mined before committing to a final opening file.
