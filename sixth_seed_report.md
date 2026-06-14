# Sixth Seed Report: IM Susilodinata, Andrean

*Prepared 2026-06-14 for FM Dino Ballecer ("Coach Dinosaur"). Roster player `7`.*

**Title:** IM | **Federation:** INA | **FIDE (standard):** 2360 | **Rapid / Blitz:** 2208 / 2221

**Basis of this report.** Curated from the refreshed auto-generated dossier
[Opponent_IM_Susilodinata_Andrean.md](manual_sections/Opponent_IM_Susilodinata_Andrean.md),
cross-checked against Dino's self-audit
[Dino_Ballecer_Needs_Improvement.md](manual_sections/Dino_Ballecer_Needs_Improvement.md) and the
web-sourced [Live_Scouting_2026-06-13.md](manual_sections/Live_Scouting_2026-06-13.md).

- **101 games on file** = **101 over-the-board PGN games** + **0 Lichess online metadata rows**.
- **Engine claims below are from 101/101 OTB PGN games analysed by Stockfish 18 at depth 12.** There
  are **0 pending engine games**. (The shipped dossier had a stale 2-game cache analysed at depth 16;
  it was fully re-analysed at depth 12 before this report.)
- **This is a genuinely classical file — no online-inflation problem.** Only **1 of 101** games is a
  speed event, and it is a rapid game **Susilodinata lost to Dino himself** (Oct 2025, see below). So
  the headline numbers below already are the classical picture; the lone rapid game is noted, not
  blended in.
- **Recency:** the file spans 2002–2026, but **70 of the classical games are from 2023 onward** and he
  is currently active, so the dossier is **current and high-confidence**. The **18 pre-2010 games are
  junior chess** (World U12/U14, 2002–2004 — including a loss to a 12-year-old Carlsen) and are
  down-weighted: they say nothing about his 2026 repertoire.
- **Command used:** `python prep_manual_app.py --analyze --scope player --player 7 --depth 12 --export`.

---

## 1. Executive Summary

Susilodinata is an **active, experienced grinder** — born 1990, a late-blooming IM (2024), Indonesia's
#9 — and the engine profile matches the reputation: **solid, accurate, and draw-heavy**. Across his
100 classical games he is **43W 31D 26L (58.5%)** with an overall ACPL of **19.8** and only **25
blunders in 100 games**. There is no cheap tactical hole here; the plan is positional pressure on his
softer side, not a knockout.

- **Black is the side to target.** He scores **63.0% with White (50g)** but **54.0% with Black (50g)**,
  and his recent losses cluster on the Black side.
- **Best structural target — but a workload one: the Catalan/Réti squeeze against his Black.** With
  Black in that family he is **2-3-4 (38.9%) over 9 classical games**, his worst structure by result.
  But his ACPL there is a clean **17.8** — he is being **out-prepared and ground down, not blundering**
  — and, critically, **reaching it needs a Réti/KIA/g3 move-order, which is not Dino's standard 1.e4.**
  This is a "train it or skip it" target, not a ready weapon.
- **Best concrete opening target: the Slav Modern Line against his Black** (**0-1-1, 25%**, incl. a 2023
  classical loss to Chatalbashev), plus a visible **recent wobble in his non-Tal Caro-Kann lines** — he
  lost 2024–2026 classical games in the Caro Tartakower, Maróczy and "Endgame" variations.
- **Clear avoid: his Caro-Kann Advance, Tal Variation.** It is his pet and it is solid — **2-2-0 (75%)
  over 4 classical games, ACPL 15.0** — so do not walk into the Advance Caro hoping for a leak.
- **Dragon caution for Dino-as-Black.** Susilodinata plays the **Yugoslav Attack against the Dragon**
  (a 2025 classical game on file), which is exactly the structure where Dino has **3 documented losses**
  (`e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6`). If Dino has Black and Susilodinata opens 1.e4, **do not volunteer
  the Dragon** until that line is repaired.
- **Live edge:** Dino has **already beaten him** — the one non-classical game on file is an Oct 2025
  rapid where Susilodinata, as White, met Dino's Sicilian with the **Alapin and lost**. Dino's Alapin-
  as-Black is a 100% line in his own file. Useful confidence, but it is a rapid result.
- **One-sentence game plan:** *Press his Black side — aim a Réti/KIA squeeze at the Catalan/Réti
  structure he scores 38.9% in (if Dino will prepare it) and probe his non-Tal Caro/Slav lines — while
  steering clear of his rock-solid Advance Caro-Kann and keeping Dino's own Dragon off the board.*

---

## 2. Opening Repertoire

*Result tables are **classical-only** (the single rapid game is excluded) and show openings with ≥2
classical games. Pre-2010 junior games are still counted in the totals but are flagged where they
distort a small sample.*

**As White — 50 classical games, 63.0%.** A flexible, two-opening player: **1.d4 into the
Rapport-Jobava** (his most-played White system) and **1.e4** (Scotch, plus principled main lines
against the Sicilian). No single line dominates, so there is no narrow White-side book to exploit.

| Line | ECO | Games | Score | Suggested action |
|---|---|---:|---:|---|
| Rapport-Jobava System | D01 | 5 | 60.0% | His main 1.d4 weapon; he even lost with it (vs Pap, 2024) — playable, not feared |
| Scotch Game: Mieses | C45 | 2 | 75.0% | Comfortable; neutral |
| Sicilian: Najdorf, Lipnitsky Attack | B90 | 2 | 75.0% | He meets the Najdorf principally; not a target |
| Sicilian: Kalashnikov | B32 | 2 | 75.0% | Solid; neutral |
| Sicilian: Kan, Polugaevsky | B42 | 2 | 50.0% | Even; minor pointer |

**As Black — 50 classical games, 54.0%.** This is the softer, more targetable side: a **Caro-Kann**
player against 1.e4 and a **Slav / QGD** player against 1.d4.

| Line | ECO | Games | Score | Suggested action |
|---|---|---:|---:|---|
| Caro-Kann: Advance, Tal Variation | B12 | 4 | **75.0%** | **Avoid** — his solid pet (2-2-0, ACPL 15.0) |
| Caro-Kann: Panov, Modern Defense | B13 | 2 | 75.0% | Comfortable; not a target |
| Caro-Kann: Exchange | B13 | 2 | 75.0% | Fine vs the Exchange; neutral |
| Slav: Quiet, Schallopp Defense | D12 | 3 | 50.0% | Even; a workable Black-side pressure point |
| Slav: Czech, Krause Attack | D17 | 2 | 50.0% | Even; minor |
| **Slav: Modern Line** | **D11** | **2** | **25.0%** | **Top concrete target** (0-1-1; 2023 loss to Chatalbashev) |
| Caro-Kann: Two Knights, Mindeno | B11 | 2 | 50.0% | 1-0-1, but one loss is the 2002 junior game vs Nepomniachtchi — thin |

> **Recency note on the Caro-Kann.** His Advance *Tal* line is genuinely solid, but his **other** Caro
> lines have leaked recently: classical losses in the **Tartakower (vs Mohammad Fahad, 2024)**,
> **Maróczy (vs Siddharth, 2025)** and **"Endgame" variation (vs Liu Xiangyi, 2026)**. The Caro-Kann is
> not uniformly safe for him — just the Advance Tal is.

### Repertoire-fit check (against Dino's own file)

- **With White it is a Caro-Kann problem, like the seventh seed.** Dino's Moscow/Rossolimo (100%) only
  matters if Susilodinata plays a Sicilian (he plays the Caro vs 1.e4), and the KIA-vs-French weapon
  does not directly apply. Dino's one tested anti-Caro is the **Two Knights Attack (100%/1)** — a
  sensible, low-theory default that side-steps the Advance Tal entirely.
- **The Catalan/Réti target is reachable only off-repertoire.** The 38.9% leak appears when he defends a
  Réti/Catalan/g3 squeeze as Black. Dino is a 1.e4 player, so this needs a **KIA/Réti move-order** (Dino
  has KIA/g3 background, 91.7% vs the French) — promising, but prep required; it will not occur from his
  standard Open-Sicilian/e4 lines.
- **With Black, mind the Dragon.** If Susilodinata opens 1.e4, his **Yugoslav Attack** intersects Dino's
  3-loss Dragon line; prefer a different defence or a repaired Dragon. Against his 1.d4 Rapport-Jobava,
  Dino's active Benoni/Neo-Grünfeld setups pose more problems than a quiet symmetrical Slav.

---

## 3. Phase Accuracy

*From 101 analysed OTB PGN games at depth 12. The classical row (100 games) is the basis; the lone
rapid game is shown only for completeness.*

| Subset | Games | Record | Overall ACPL | Opening | Middlegame | Endgame | Blunders | Mistakes |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| **Classical** | **100** | **43-31-26 (58.5%)** | **19.8** | **10.2** | **14.6** | **26.4** | **25** | **69** |
| Online (rapid, the Dino game) | 1 | 0-0-1 | 33.7 | 10.2 | 11.9 | 51.7 | 0 | 4 |

**Interpretation (within-player only).** This is a clean, accurate profile: an overall classical ACPL
of **19.8** with **25 blunders across 100 games** is a solid IM who does not hand games away. His most
accurate phase is the **opening (ACPL 10.2)** — consistent with a well-booked grinder — and, as usual,
the **endgame is his least accurate (26.4)**, though "least accurate" here is still respectable. The
high **mistake** count (69) against the low blunder count (25) fits the draw-heavy record: many
small inaccuracies in long games, few outright collapses.

> **Practical reading:** you will not out-blunder him. The realistic edge is to keep pressure into long
> games and the move-30+ phase (see §5), where his accuracy dips and his 2024 results show real cracks,
> rather than to expect a quick tactical gift.

---

## 4. Middlegame and Structure Notes

*Classical-only structure split by Susilodinata's color (result **and** engine accuracy).*

| Structure family | His color | Games | Result % | ACPL | B/M | Read |
|---|---|---:|---:|---:|---:|---|
| Catalan / Réti Squeeze | Black | 9 | **38.9%** | 17.8 | 1/5 | **Top result target**; clean ACPL → out-prep, not out-blunder; needs a Réti/KIA move-order |
| Advance Caro-Kann | Black | 5 | 70.0% | 15.0 | 2/1 | **Avoid** — solid and accurate; his comfort zone |
| IQP / Panov Attack | Black | 6 | 66.7% | 12.0 | 1/3 | Very clean as Black; do not hand him this |
| Anti-Sicilian Counter-Package | Black | 3 | 66.7% | 20.2 | 0/5 | Comfortable; neutral |
| Anti-Sicilian Counter-Package | White | 3 | 66.7% | 14.6 | 0/0 | Clean with White; neutral |

**Practical structure verdicts:**

- **Steer toward (with prep): the Catalan/Réti squeeze vs his Black.** 38.9% over 9 classical games is
  his clear soft spot, but the clean ACPL (17.8) means he is **out-played, not blundering** — exactly
  the Chan-style "out-prep target that needs genuine understanding." Worth it **only** if Dino will
  prepare a KIA/Réti/g3 route to it.
- **Do not invite his clean families.** He is accurate and well-scoring in **Advance Caro-Kann (ACPL
  15.0)** and **IQP/Panov as Black (ACPL 12.0)**; avoid lines that let him reach those.
- **Small-sample discipline.** Every classical family here is 3–9 games; treat them as pointers, weight
  the 2023–2026 games, and do not read the 2002–2006 junior games as current evidence.

---

## 5. Endgame and Simplified Positions

His classical endgame ACPL (**26.4**) is his weakest phase but not a glaring weakness. What the data
does show is that **his late errors cluster in a rough 2024 competitive stretch** (Budapest GM events +
the 45th Olympiad) and in the **move-30-to-40 zone** — the place to keep pressure. The clearest recent
classical samples (move ≥ 30):

| Game | Move | Severity | Theme | Engine prefers |
|---|---|---|---|---|
| vs Tin, Jingyao (SGP-ch, Feb 2025) | 36...Nf4+ | blunder (loss ~227) | Late slip in a Semi-Slav he then lost | Re1xd1 |
| vs Mamatov, Melis (Oct 2024) | 37...Bc5 | blunder (loss ~393) | Loose piece move — in his *own* Advance Caro Tal | Rd2-f2 |
| vs Mohammad Fahad (Budapest, Oct 2024) | 39...Qxb3 | blunder (loss ~1500) | Decisive late error in a Caro Tartakower loss | Bb5-d7 |
| vs Mayank, Chakraborty (Budapest, Sep 2024) | 35.Qg5 | blunder (loss ~239) | Misjudged attack with White (Barry Attack) | Rh1-d1 |

**Honest phrasing for Dino:** *Susilodinata defends competently and draws a lot; his late play is
loosest in long, pressured games, and his 2024 results show that pressure does eventually tell. The
edge is "make him hold a long, slightly worse position to the first time control," not "trade into an
ending and grind a clean technical win."*

> **Mirror caution.** Dino's own classical endgame technique (depth-12: ACPL 36.7, 4 drawing-defense
> failures on file) is **looser than Susilodinata's 26.4**. A "press him in long endings" plan only pays
> off if Dino tightens his own conversion and drawing-defence first — against a 31-draws-in-100 grinder,
> Dino is the more likely one to crack in a marathon.

---

## 6. Practical Game Plan for Dino

1. **Play the Black side of the board against him.** His White is flexible and well-scoring (63%); his
   Black (54%) and his recent losses are the targets. Plan to make *his* defence work.
2. **With White, treat it as a Caro-Kann fight — Two Knights Attack default.** It is Dino's tested
   anti-Caro (100%/1), low on theory, and avoids his solid Advance Tal. Do **not** enter the Advance
   hoping for a leak; that is his comfort zone (75%, ACPL 15.0).
3. **Optional White project: a KIA/Réti squeeze.** His worst structure is the Catalan/Réti as Black
   (38.9%). Dino's KIA background (91.7% vs the French) is the natural bridge, but it needs a prepared
   move-order against a Caro player. Train it or leave it — it will not appear by accident from 1.e4.
4. **Probe his non-Tal Caro and his Slav.** The concrete result target is the **Slav Modern Line
   (25%)**, and his 2024–2026 Black losses in the Caro Tartakower/Maróczy/"Endgame" lines show the
   Caro-Kann is only safe for him in the Advance Tal.
5. **With Black, keep Dino's Dragon off the board.** Susilodinata plays the Yugoslav Attack, which is
   Dino's 3-loss problem line. Choose a different defence to 1.e4, or only allow the Dragon if that
   exact line is repaired first.
6. **Win the long game, don't expect a short one.** He blunders rarely (25/100) and draws a third of
   his games. Keep pressure into the move-30+ phase, where his 2024 results cracked, rather than
   simplifying early.
7. **Tighten Dino's own endgame first.** Against a 31-draws grinder whose technique (ACPL 26.4) is
   cleaner than Dino's (36.7, 4 drawing-defence failures), Dino's own conversion/defence is the larger
   risk in any marathon.
8. **Use the live edge sensibly.** Dino already beat him once (Oct 2025 rapid, Dino's Alapin as Black).
   It is real confidence and a known opponent, but it was a rapid game — do not over-read it into the
   classical plan.
9. **Freshness to-do.** He is active (rapid as recent as June 2026); mine any 2026 classical games
   (SGP-ch and the Asian/Indonesian circuit) before the round to confirm he is still on the Caro-Kann /
   Rapport-Jobava and still leaking in the Catalan/Réti.

---

## Method & Caveats

- **Analysis command:** `python prep_manual_app.py --analyze --scope player --player 7 --depth 12 --export`.
- **Coverage:** 101 total games, 101 OTB PGNs, 0 Lichess rows, **101/101 analysed at depth 12**, 0
  pending. The shipped dossier's stale 2-game depth-16 cache was discarded and the full set
  re-analysed at depth 12; the evidence pack was generated with `seed_evidence.py 7 --depth 12`.
- **Time-control split:** 100 classical opens vs 1 online rapid game (the loss to Dino). All verdicts
  use the classical set; the rapid game is reported, not blended.
- **Recency:** 70 classical games are 2023 or later and he is active, so the file is current. The 18
  pre-2010 games are junior chess (W-ch U12/U14, 2002–2004) and are explicitly down-weighted; no
  duplicate games were detected.
- **Applicability checks applied:** the Catalan/Réti target is flagged as off-Dino's-1.e4-repertoire,
  and the Dragon/Yugoslav-Attack intersection with Dino's documented weakness is called out — both per
  the workflow's repertoire-applicability rule.
- **Known limitations:** depth 12 is a screening depth, not final engine truth; classical family
  samples are 3–9 games each; result-score and engine-accuracy targets are reconciled explicitly (the
  Catalan/Réti and Advance-Caro reads both note that he plays cleanly by ACPL).
