# First Seed Scouting Report — GM Vignesh, N R

*Prepared 2026-06-13 for FM Dino Ballecer ("Coach Dinosaur"). Roster player `2`.*

**Title:** GM | **Federation:** IND | **FIDE (standard):** 2515 *(rapid 2381 / blitz 2453)*

**Basis of this report.** Curated from the auto-generated dossier
[Opponent_GM_Vignesh_N_R.md](manual_sections/Opponent_GM_Vignesh_N_R.md), cross-checked against
Dino's self-audit [Dino_Ballecer_Needs_Improvement.md](manual_sections/Dino_Ballecer_Needs_Improvement.md)
and the web-sourced [Live_Scouting_2026-06-13.md](manual_sections/Live_Scouting_2026-06-13.md).

- **187 games on file** = **104 over-the-board PGN** + **83 Lichess online metadata rows**.
- **Engine claims below are from the 104 OTB games, all analysed by Stockfish at depth 12.** The 83
  Lichess rows are metadata only (no move lists), so they feed opening/result statistics but **not**
  centipawn analysis. Where a "recent loss" is a Lichess blitz/rapid game it is labelled as such and
  treated as weak evidence for classical prep.

---

## 1. Executive Summary

Vignesh is the **strongest player in the pool and currently match-sharp** (7/9 at the 51st Ciudad de
Sevilla Open 2026, plus 6/7 in the side blitz). On file he is **122W 44D 21L (77.0%)** with a broad,
accurate repertoire (**128 distinct openings**, opening ACPL just **7.7** over 104 games at depth 12).

- **Do not plan around an opening trap.** His opening phase is his *cleanest* phase; a 128-opening
  spread means surprise value is low.
- **Do not plan to out-clock him.** His blitz (2453) is higher than his rapid (2381); the live read
  is that he is dangerous in time scrambles. Keep the game on Dino's preparation, not on the clock.
- **Best candidate targets are specific, not broad.** The sample shows two concrete soft spots — the
  **Advance Caro-Kann, Tal Variation** as Black (0/2) and the **Caro-Kann Tartakower** when he is
  White (0/2) — plus a relative dip in **endgame** accuracy (ACPL 18.0, the worst of his four phases).
- **One-sentence game plan:** *As White, steer toward the Advance Caro-Kann (Tal Variation) — which
  doubles as a structure Dino's own audit says he must train — keep the game classical and unbalanced
  rather than a clock race, and if it simplifies, press a rook ending with an active rook, because the
  sample shows repeated drawing-defence and active-rook lapses there.*

> ⚠️ **Freshness caveat (from live scouting):** the Caro-Kann targets predate his Sevilla 2026 games.
> Mine his Sevilla scores before committing — he may have patched the Tal line. See §6.

---

## 2. Opening Repertoire

**As White — 91 games, 80.8%.** Mainly 1.e4 (Rossolimo/Moscow-style anti-Sicilians, open Sicilians)
plus English/Catalan setups. Accurate and high-scoring; little to exploit head-on.

**As Black — 96 games, 73.4%.** Broader and slightly more porous than his White results — this is the
side where the two clean targets live.

### Confidence lines — do **not** walk into these

| Line | ECO | Games | Score | Suggested action |
|---|---|---:|---:|---|
| Sicilian Defense: Nyezhmetdinov-Rossolimo Attack | B30 | 6 | 100.0% | Avoid — pet anti-Sicilian as White |
| Rapport-Jobava System | D01 | 5 | 100.0% | Avoid — he neutralises the Jobava/London cleanly as Black; don't try it |
| English Opening: Agincourt, Neo-Catalan Declined | A14 | 4 | 100.0% | Avoid — comfortable as White |
| Sicilian Defense: Najdorf, English Attack | B90 | 3 | 100.0% | Avoid — well prepared as Black |

### Repair / target lines — candidate targets only

| Line | ECO | Games | Score | Suggested action |
|---|---|---:|---:|---|
| Caro-Kann Defense: Advance Variation, **Tal Variation** (he is **Black**) | B12 | 2 | 0.0% | **Target as White** — fits a structure Dino must build anyway (see fit note) |
| Caro-Kann Defense: **Tartakower Variation** (he is **White**) | B15 | 2 | 0.0% | Target as Black **only if** Dino adds the Caro-Kann — not in his current repertoire |
| Queen's Gambit Declined: Ragozin, Alekhine Variation | D38 | 2 | 25.0% | Weak flag — tiny sample, one source is a Lichess blitz loss; candidate only |

### Repertoire-fit check (the decisive filter)

The workflow rule is *don't recommend a line Dino doesn't already understand*. Applying it:

- **Advance Caro-Kann, Tal Variation (Dino as White): KEEP — high value, needs reps.** This is a
  genuine convergence: it is one of Vignesh's two 0/2 lines **and** Dino's own audit flags the
  *Advance Caro-Kann* core family as a **zero-rep gap** ("schedule training games in it"). The target
  is real, but Dino must put in practice games on the Tal Variation before the event — he cannot
  improvise it cold against a 2515.
- **Caro-Kann Tartakower (Dino as Black): DROP for this event.** Vignesh's 0/2 as White is tempting,
  but Dino does **not** play the Caro-Kann as Black (his Black book is Sicilian/Benoni-based).
  Learning a new defence for one game against an in-form GM is the wrong trade. File it as "future
  repertoire," not event prep.

---

## 3. Phase Accuracy

*From 104 analysed OTB games at depth 12. Lower ACPL = cleaner play.*

| Phase | ACPL |
|---|---:|
| Overall | 13.9 |
| Opening | 7.7 |
| Middlegame | 11.7 |
| **Endgame** | **18.0** |

Serious errors on file: **10 blunders, 46 mistakes, 151 inaccuracies**.

**Interpretation (within-player only).** He is most accurate in the opening and **least accurate in
the endgame** — but 18.0 is still a strong number in absolute terms. Read this as a *relative
tendency*: as the game simplifies, the gap between his best and his actual move widens. It is not a
licence to call a 2515 "bad at endgames."

> **Cross-player caution.** Dino's own profile shows overall ACPL 26.7 (endgame 36.7), but that came
> from only **7** analysed games versus Vignesh's **104**. Depth matches (both 12); sample sizes do
> not. Do not lean on a head-to-head ACPL comparison — see the two-edged endgame note in §6.

---

## 4. Middlegame and Structure Notes

*Engine fingerprint over the six core structure families (depth 12). The key discipline here is to
keep **result-score** evidence and **engine-accuracy** evidence separate — they don't always agree.*

| Structure family | Games (result) | Result % | Moves | ACPL | Serious err | Read |
|---|---:|---:|---:|---:|---:|---|
| IQP / Panov Attack | 7 | 71.4% | 96 | **17.6** | 2 | **Engine target** — least accurate, high error density. Dino zero-rep family → train + target |
| Catalan / Réti Squeeze | 32 | 70.3% | 535 | 13.0 | 5 | Engine target **but his most-played comfort zone** — steer here only with concrete prep |
| Anti-Sicilian Counter-Package | 23 | 87.0% | 477 | 11.8 | 9 | **Avoid** — his strongest family by result |
| Reversed-Sicilian / Flank Annexation | 14 | 82.1% | 225 | 10.7 | 1 | Avoid — strong and accurate |
| Fianchetto KID / Grünfeld Complexes | 7 | 71.4% | 123 | 8.7 | 0 | Avoid — accurate, no serious errors |
| Advance Caro-Kann | 4 | **50.0%** | 69 | 7.9 | 0 | **Paradox — read carefully below** |

**The Advance Caro-Kann paradox (don't mis-target it).** By *engine accuracy* this is his **cleanest**
family (ACPL 7.9, zero serious errors) — so the raw fingerprint says "avoid." By *result* it is his
**worst** family (50%, 2-0-2), and the specific **Tal Variation sub-line is 0/2**. The reconciliation:
he doesn't play the Advance Caro sloppily move-to-move; he has simply **lost concrete games in one
named line**. So the target is the **precise Tal Variation**, prepared deeply — not a vague hope that
he'll drift in Advance Caro structures generally. Steer toward the *line*, not the *family average*.

**Practical structure verdicts:**

- **Steer toward (with prep):** IQP / Panov positions — his least-accurate structure, and a family
  Dino's audit also lists as a zero-rep gap to build. Best single convergence on the White side.
- **Steer toward only with a concrete idea:** Catalan / Réti — engine flags occasional errors, but
  it's his most-played family (32 games, 70%); entering it blind means entering his comfort zone.
- **Avoid:** Anti-Sicilian Counter-Package, Reversed-Sicilian/Flank, Fianchetto KID/Grünfeld — strong
  results *and* clean engine numbers. No edge here.
- **Model-game review for Dino:** IQP/Panov and Advance Caro-Kann Tal — the two structures he must
  both learn and target, so build them together.

---

## 5. Endgame and Simplified Positions

The endgame is his least-accurate phase (ACPL 18.0). Classified weakness categories from the OTB
sample (12 classified late-position samples): **drawing-defence failure ×4, Philidor ×3, conversion
failure ×2, rook activity ×2, rook-behind-pawn ×1** — i.e. the cluster is almost entirely
**rook-and-pawn technique**. The five clearest samples (all OTB):

| Game | Move | Severity | Category | Engine prefers | Training theme |
|---|---|---|---|---|---|
| vs Aaditya, Dhingra | 37...Bg5 | blunder | Drawing-defence failure | h5–h4 | Hold the draw with the pawn break, not a passing bishop move |
| vs Boci, Mateo | 38...Kg5 | blunder | Drawing-defence failure | Rc2–c1 | Keep the rook active on defence rather than walking the king |
| vs Sukovic, Andrej | 39.Rd2 | mistake | Philidor / rook activity / conversion | Rf2–f4 | Activate the rook to convert; passive Rd2 lets the win slip |
| vs Anand, Batsukh | 36.Bd3 | mistake | Philidor / rook behind pawn | Rc1–c5 | Rook to the 5th / behind the passer instead of a quiet bishop move |
| vs Ruzhansky, Elias | 38.Rxc6 | mistake | Rook activity | a5–a6 | Push the passed pawn instead of grabbing material |

**The honest phrasing for the manual:** *In the analysed sample, his least accurate phase is the
endgame, with several classified rook-ending and drawing-defence lapses. If Dino reaches a simplified
rook ending, treating active-rook play (rook behind passers, rook to the 5th), accurate Philidor /
second-rank defence, and clean conversion as real practical chances is justified.* It is **not** a
claim that the endgame is a general weakness.

---

## 6. Practical Game Plan for Dino

1. **No opening surprise.** His opening ACPL is 7.7 over 128 openings — don't build the game around
   a one-move trap. Aim for a sound line that produces an unbalanced, *playable* middlegame.
2. **No clock race.** Live scouting: blitz 2453 > rapid 2381, "dangerous in time scrambles." Manage
   the clock conservatively; don't bank on outplaying him fast.
3. **As White — primary plan:** prepare the **Advance Caro-Kann, Tal Variation (B12)** where he is
   0/2 as Black. This is the best convergence in the file: a real target line *and* a core structure
   Dino's audit flags as a zero-rep must-build. **Action: play training games in it before the
   event** — the edge is the prepared line, not improvisation.
4. **As White — secondary plan:** prepare a **Panov / IQP** try (his least-accurate structure, ACPL
   17.6, and Dino's other zero-rep core family). Train it alongside the Advance Caro so the two
   White structures reinforce each other.
5. **As Black — do not chase the Caro-Kann Tartakower target.** It's a real Vignesh soft spot (0/2 as
   White) but it's outside Dino's repertoire; adopting a new defence for one game is the wrong risk.
   **Instead, fix Dino's own Black liability first:** his audit shows **3 losses** in the exact
   Sicilian Dragon sequence `e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6` (B70/B76). Against an in-form 2515, do
   **not** walk a leaky Dragon into his preparation — choose a solid, well-rehearsed Black setup.
6. **Endgames — press, but mind the two-edged sword.** If the game simplifies into a rook ending,
   keep the rook active (behind passers, to the 5th) and know the Philidor / second-rank draw — the
   sample shows him lapsing exactly there. **Caveat:** Dino's *own* endgame is his weakest phase too
   (ACPL 36.7; 4/4 drawing-defence failures in his small sample). "Grind him in the endgame" only
   works if Dino sharpens his own rook-ending technique first — otherwise the plan backfires.
7. **Build 3 model games — from the right source.** Use the **OTB endgame samples** above (vs
   Aaditya, Boci, Sukovic, Anand) as the model games, **not** the "recent losses" list in the
   dossier — those are all **Lichess blitz/rapid** games and are weak evidence for classical prep.
8. **Validate before committing (live-scouting to-do).** His Sevilla 2026 games post-date this PGN
   drop. Pull his Sevilla scores and check whether the Advance Caro-Kann Tal line has been patched
   before locking it in as the main White plan.

---

## Method & Caveats

- **Command that produced the underlying analysis:** `python prep_manual_app.py --analyze --scope
  player --player 2 --depth 12 --export` (per the workflow).
- **Evidence discipline applied:** game counts shown next to repertoire claims; depth (12) and sample
  size (104 OTB) shown next to engine claims; Lichess metadata kept separate from OTB engine
  analysis; result-score targets and engine-accuracy targets reconciled explicitly (the Advance Caro
  paradox); every target filtered against Dino's actual repertoire before being recommended.
- **Known limitations:** depth 12 is a screening depth, not deep verification; some target lines rest
  on 2-game samples (flagged inline); the freshest evidence (Sevilla 2026) is not yet in the PGN set.
