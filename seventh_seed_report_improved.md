# Seventh Seed Report: GM Thejkumar, M. S.

*Prepared 2026-06-14 for FM Dino Ballecer ("Coach Dinosaur"). Roster player `8`.*

**Title:** GM | **Federation:** IND | **FIDE (standard):** 2352 (official pairing list; his FIDE
profile reads **2358** and is flagged **inactive**)

**Basis of this report.** Curated from the refreshed auto-generated dossier
[Opponent_GM_Thejkumar_M_S.md](manual_sections/Opponent_GM_Thejkumar_M_S.md), cross-checked against
Dino's self-audit [Dino_Ballecer_Needs_Improvement.md](manual_sections/Dino_Ballecer_Needs_Improvement.md)
and the web-sourced [Live_Scouting_2026-06-13.md](manual_sections/Live_Scouting_2026-06-13.md).

- **102 games on file** = **102 over-the-board PGN games** + **0 Lichess online records without full move lists**.
- **Engine claims below are from 102/102 OTB PGN games analysed by Stockfish 18 at depth 12.** There
  are **0 pending engine games**. (The shipped dossier had a stale 2-of-102 cache reading an incorrect
  "endgame ACPL 281.0"; it was fully re-analysed before this report.)
- **Mixed time controls in the engine sample — and the "0 Lichess" header hides it.** Of the 102
  analysed games, **48 are classical opens** and **54 are online/rapid speed events** (50 chess.com
  *Titled Tuesday* + 4 *Pune Rapid*). Those speed games sit inside the ChessBase PGNs, so they never
  show in the Lichess count. Because Dino plays a classical event, this report leads with the
  **classical-only** subset and flags where the headline numbers are inflated by speed games.
- **Command used:** `python prep_manual_app.py --analyze --scope player --player 8 --depth 12 --export`.

---

## 1. Executive Summary

Thejkumar is a genuine GM (IND, 2352/2358) but the single most important fact about this pairing is
off the board: **he is effectively inactive — no FIDE-rated games since February 2024 — and has moved
into coaching.** His 102-game file is therefore **pre-2024**, which cuts both ways: it shows the
  stable, trusted lines a now-coaching player is most likely to reuse, but it also means **expect
OTB rust** in long-game calculation and clock handling.

- **Separate his classical play from his speed play.** Across all 102 games his profile looks much worse
  (overall ACPL 41.8, endgame 67.0, 81 serious errors), but **54 of those games are online/rapid**.
  Restricted to his **48 classical games he is a normal solid GM: 21W 15D 12L (59.4%), overall ACPL
  21.9, endgame ACPL 30.0, 24 blunders.** Do not build the plan around a speed-game collapse.
- **As White he is a 1.d4 player** (QGD/Ragozin, Semi-Slav, Slav, KID-as-White). **As Black he is a
  near-pure Caro-Kann player.** So Dino's main e4 weapons do not apply here: there is no Sicilian for
  the Moscow/Rossolimo and no French for the KIA — against this opponent the White game is a
  **Caro-Kann battle**.
- **Cleanest result target (Dino with White):** his **Caro-Kann Advance, Short Variation** is **0W 0D
  2L (0.0%)** in classical play. But this is a **workload target, not a free one**: the leak only
  appears if Dino plays the **Advance (3.e5)**, and Dino's audit flags **no Advance Caro-Kann games**.
  Dino's only tested anti-Caro is the **Two Knights Attack (1 game, 100%)**.
- **Cleanest fit (Dino with Black):** steer toward a **fresh, unbalanced middlegame** rather than a
  symmetrical QGD theory duel. His classical White results are soft in exactly the structures that
  stay double-edged — **Catalan/Réti-as-White 42.9% and IQP/Panov-as-White 33.3%** — and against a
  rusty opponent the goal is to make him solve problems over the board, not recite preparation.
- **His softest phase is the endgame** (classical ACPL 30.0, 24 blunders / 48 games, clustered in the
  late-middlegame-to-endgame transition). Keep pieces on into the first time control.
- **One-sentence game plan:** *Treat the White game as a Caro-Kann fight — play the tested Two Knights
  Attack unless Dino is willing to train the Advance as a project — and with Black aim for a fresh,
  unbalanced structure that makes a rusty, inactive GM calculate and burn clock, then keep enough
  material on to reach the late phase where his accuracy drops.*

---

## 2. Opening Repertoire

*Result tables below are **classical-only**; openings with ≥2 classical games shown. Online/rapid
games are excluded because they roughly double his error rate and distort the percentages.*

**As White — 25 classical games, 60.0%.** A pure queen's-pawn player: 1.d4 into Ragozin/QGD,
Semi-Slav and Slav structures, with occasional KID-as-White. No 1.e4 in the classical set.

| Line | ECO | Games | Score | Suggested action |
|---|---|---:|---:|---|
| Queen's Gambit Declined: Ragozin Defense | D38 | 5 | 70.0% | His main, draw-heavy (2-3-0); not a target |
| Semi-Slav Defense | D43 | 3 | 66.7% | Comfortable; neutral |
| King's Indian Defense: Orthodox (Aronin-Taimanov) | E97 | 2 | 100.0% | He scores well facing the KID; do not invite it |
| Semi-Slav Defense: Chigorin | D46 | 2 | 50.0% | Neutral |
| Queen's Indian Defense: Capablanca | E16 | 2* | 0.0% | *Same game duplicated across two PGN imports — really **one** loss (vs Ghosh, 2024); a thin signal, not two data points |

**As Black — 23 classical games, 58.7%.** Almost everything is a Caro-Kann. This is the side Dino
actually faces with White, and it is deeply theoretical, trusted territory for Thejkumar.

| Line | ECO | Games | Score | Suggested action |
|---|---|---:|---:|---|
| Caro-Kann: Advance, Short Variation | B12 | 2 | **0.0%** | **Top White result target** (0-0-2), but requires the Advance, which Dino does not play |
| Caro-Kann: Advance, Botvinnik-Carls | B12 | 3 | 66.7% | His preferred Advance answer; he is comfortable here |
| Caro-Kann (main / B15) | B15 | 2 | 100.0% | Solid; not a target |
| Caro-Kann: Exchange | B13 | 2 | 100.0% | He is fine vs the Exchange; not a soft target |

### Repertoire-fit check (against Dino's own file)

- **White is a Caro-Kann problem, not a Sicilian/French one.** Dino's headline weapons — Moscow/
  Rossolimo (100%) and the KIA vs the French (91.7%) — **will not occur**, because Thejkumar answers
  1.e4 with 1...c6. Plan the White game specifically against the Caro-Kann.
- **Tested anti-Caro = Two Knights Attack.** Dino's file shows one Caro-Kann game, a Two Knights
  Attack win (B10, 100%/1). It is low-theory and side-steps Thejkumar's deep Advance/Classical
  preparation — a sensible practical default against a booked-up but rusty opponent.
- **The Advance Short target is a project, not a surprise.** The 0/2 result is real but tiny, and
  Dino has **no Advance Caro-Kann games** (a flagged gap in his audit). Only choose the Advance if
  he is willing to train it with model games first; otherwise the result edge is unreachable.
- **As Black, avoid feeding his comfort zones.** He scores 100% facing the KID-as-White (E97) and is
  solid in his Ragozin/Semi-Slav universe, so a quiet symmetrical QGD plays to his strengths. Prefer
  a Benoni/Grünfeld-flavoured, unbalanced setup (Dino's Neo-Grünfeld is 100%/2, his Benoni reps are
  live) to pose fresh problems.

---

## 3. Phase Accuracy

*From 102 analysed OTB PGN games at depth 12. Lower ACPL = cleaner play. The classical/online split
is the most important row here.*

| Subset | Games | Record | Overall ACPL | Opening | Middlegame | Endgame | Blunders | Mistakes |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| All analysed | 102 | 49-19-34 (57.4%) | 32.4* | 9.6 | 19.4 | 49.2 | 81 | 114 |
| **Classical only** | **48** | **21-15-12 (59.4%)** | **21.9** | **7.9** | **17.1** | **30.0** | **24** | **38** |
| Online / rapid | 54 | 28-4-22 (55.6%) | 41.8 | 11.1 | 21.5 | 67.0 | 57 | 76 |

*The all-games overall/endgame figures are dominated by the online half and are shown only to expose
the inflation; use the classical row for every verdict.*

**Interpretation (within-player only).** In classical chess Thejkumar is a solid GM whose **opening
is his most accurate phase (ACPL 7.9)** — no surprise for a now-coach playing trusted lines — and
whose **endgame is his weakest (ACPL 30.0)**. His 24 classical blunders over 48 games are not random;
they cluster in the **late-middlegame-into-endgame transition** (see §5). Online his error rate roughly
doubles, consistent with his much lower, inactive rapid/blitz ratings (2242 / 2303).

> **Rust amplifier.** These are pre-2024 games by a player who has not competed since. A two-year
> classical layoff typically hurts calculation stamina and clock management more than opening
> knowledge — which lines up with the file: clean openings, looser late play. Treat his endgame phase
> as the place where rust is most likely to compound.

---

## 4. Middlegame and Structure Notes

*Classical-only structure split by Thejkumar's color (results **and** engine accuracy, which are
separate evidence types).*

| Structure family | His color | Games | Result % | ACPL | B/M | Read |
|---|---|---:|---:|---:|---:|---|
| Catalan / Réti Squeeze | White | 7 | **42.9%** | 19.1 | 1/10 | Poor result (2-2-3), but the engine says he played cleanly |
| Advance Caro-Kann | Black | 6 | 50.0% | 19.7 | 2/7 | Even; his trusted defensive structure |
| Catalan / Réti Squeeze | Black | 4 | 62.5% | 20.9 | 2/3 | Comfortable; not a target |
| IQP / Panov Attack | Black | 3 | 100.0% | 12.9 | 0/1 | Very clean as Black; do not hand him this |
| IQP / Panov Attack | White | 3 | **33.3%** | 13.6 | 1/1 | Poor result (0-2-1) on a tiny sample; clean engine play |

**Practical structure verdicts:**

- **Poor results, but not messy moves.** His two weakest classical White families (Catalan/Réti 42.9%,
  IQP/Panov 33.3%) show low ACPL, so the losses are about being outplayed and ground down, not about
  simple blunders. For Dino that means these are *playable, double-edged* targets that reward genuine
  understanding — useful against a rusty opponent — not trap lines.
- **Do not invite his clean zones.** He is 100% and very accurate in **IQP/Panov as Black** (ACPL
  12.9) and comfortable defending the **Advance Caro-Kann as Black** (ACPL 19.7); avoid lines that let
  him reach those.
- **Small-sample discipline.** Every classical family here is 3–7 games; treat these as pointers, not
  laws, and weight the **2023–2024 games** over the older bulk.

---

## 5. Endgame and Simplified Positions

The dossier's raw "endgame ACPL 281.0 / 7 blunders" came from a stale 2-game cache and is discarded. On
the full depth-12 re-analysis, his **classical** endgame ACPL is **30.0 with 24 blunders over 48
games** — the weakest of his three phases, and the most plausible place for inactivity to show. The
clearest classical late errors (move ≥ 30):

| Game | Move | Severity | Theme | Engine prefers |
|---|---|---|---|---|
| vs Nikitenko, Mihail (Colombo, Nov 2022) | 39.Qe4 | blunder (loss ~730) | Queen misstep in a Semi-Slav middlegame-to-ending | Qa8-a7 |
| vs Liyanapathirana, Pasan (Nov 2022) | 33...Qg2+ | blunder (loss ~269) | Premature check, lost coordination (Advance Caro as Black) | Qa8-h1 |
| vs Fominyh, Alexander (Colombo, Dec 2022) | 37.Rc1 | blunder (loss ~219) | Passive rook in a QGA ending he then lost | Rd1-e1 |

**Honest phrasing for Dino:** *Thejkumar's endgame is his softest classical phase, with real
late-phase blunders, but the sample is older and modest — this is a "keep the game going and make him
work late" edge, not a guaranteed technical collapse. Reaching the first time control with pieces on
is worth more than trading into a clean ending and hoping.*

> **Mirror caution.** Dino's own depth-12 profile (7 analysed losses) shows endgame ACPL 36.7 with
> **4 drawing-defense failures** — i.e. Dino's late technique is currently *looser* than Thejkumar's
> classical 30.0. Any "outlast him in the endgame" plan needs Dino to tighten his own conversion and
> drawing-defense first.

---

## 6. Practical Game Plan for Dino

1. **Treat the White game as a Caro-Kann fight.** Forget Moscow/Rossolimo/KIA here — they cannot
   occur. Prepare specifically against 1...c6.
2. **Default White weapon: the Two Knights Attack.** It is Dino's one tested anti-Caro (100%/1), low
   on theory, and dodges Thejkumar's deep, trusted Advance/Classical preparation — ideal against a
   booked-but-rusty opponent.
3. **Only play the Advance as a trained project.** The 0/2 classical result in the Advance Short is
   the cleanest result target, but Dino has zero Advance Caro reps; reaching it cold against a GM is
   the wrong risk. Train it with model games first, or leave it.
4. **With Black, pick a fresh, unbalanced structure.** Avoid a symmetrical QGD/Slav theory duel
   (his comfort zone). Lean on Dino's 100% Neo-Grünfeld or his live Benoni to pose problems and eat
   clock — exactly what tends to expose two-year rust.
5. **Keep pieces on into the first time control.** His weakest classical phase is the endgame (ACPL
   30.0, 24 blunders/48), clustered in the move-30+ transition. Don't simplify early and hope; make
   him calculate a complex late middlegame.
6. **Don't out-theory a GM — out-stamina a rusty one.** His opening accuracy (ACPL 7.9) is the best
   part of his game; surprise value comes from *position type and clock*, not from a sharper line in
   his own pet variations.
7. **Tighten Dino's own late technique first.** Dino's drawing-defense (4/4 failures on file) is the
   real risk in any long ending; the "make him work late" plan only pays off if Dino doesn't return
   the favour.
8. **Model games to study:** his classical Advance-Short losses to **Nikitenko (Colombo 2022, 36
   moves)** and **Mahdavi (Dubai 2022, 28 moves)**; his late-phase blunder losses to **Nikitenko
   (Semi-Slav, 39.Qe4)** and **Fominyh (QGA ending, 37.Rc1)**; and his most recent classical loss, the
   **QID Capablanca vs Ghosh (Bangalore, Jan 2024)** — his freshest competitive game on file.
9. **Freshness to-do.** He is inactive, so there are no 2025–2026 games to mine; the Jan 2024
   Bangalore event is the latest evidence. If he has played any unrated/coaching games since, they are
   not in this file — assume the pre-2024 repertoire and prepare for rust.

---

## Method & Caveats

- **Analysis command:** `python prep_manual_app.py --analyze --scope player --player 8 --depth 12 --export`.
- **Coverage:** 102 total games, 102 OTB PGNs, 0 Lichess records without full move lists, **102/102
  analysed at depth 12**, 0 pending. The shipped dossier's 2-of-102 cache was discarded and the full set re-analysed.
- **Time-control split:** 48 classical opens vs 54 online/rapid (Titled Tuesday + Pune Rapid). All
  accuracy and structure verdicts use the **classical** subset; all-games numbers are shown only to
  expose the speed-game inflation. The "0 Lichess online" header is misleading — the speed games are
  ChessBase PGNs.
- **Duplicate-game note:** his QID Capablanca loss to Ghosh is stored twice under two event spellings
  (`Bangalore op-A 1st` / `1st Bangalore Int Open`, same date/opponent/56 moves), so that "0/2" is
  really one loss. Other 2-game samples were checked and are distinct.
- **Activity caveat:** the entire file is pre-2024; Thejkumar has not played rated chess since Feb
  2024 and now coaches. Read every tendency as his *trusted pre-layoff repertoire*, and weight the
  rust factor accordingly.
- **Rating note:** the manual uses **2352** to match the organizer's pairing list; his FIDE profile
  reads **2358** and is flagged inactive. Low stakes, but flagged for a deliberate call.
- **Known limitations:** depth 12 is a screening depth, not final engine truth; classical family
  samples are 2–7 games each; result targets and engine-accuracy targets are checked against each
  other (his soft White families are clean by ACPL, meaning the results are poor but the moves are not
  full of mistakes).
