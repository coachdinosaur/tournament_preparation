# Eighth Seed Report: FM Ang, Ern Jie Anderson

*Prepared 2026-06-14 for FM Dino Ballecer ("Coach Dinosaur"). Roster player `9`.*

**Title:** FM | **Federation:** MAS | **FIDE (standard):** 2309 (rapid 2253, **blitz 1993**) |
**Born 2010** — a 15-year-old who made FM in 2025.

**Basis of this report.** Curated from the refreshed auto-generated dossier
[Opponent_FM_Ang_Ern_Jie_Anderson.md](manual_sections/Opponent_FM_Ang_Ern_Jie_Anderson.md),
cross-checked against Dino's self-audit
[Dino_Ballecer_Needs_Improvement.md](manual_sections/Dino_Ballecer_Needs_Improvement.md) and the
web-sourced [Live_Scouting_2026-06-13.md](manual_sections/Live_Scouting_2026-06-13.md).

- **100 games on file** = **100 over-the-board PGN games** + **0 Lichess online metadata rows**.
- **Engine claims below are from 100/100 OTB PGN games analysed by Stockfish 18 at depth 12.** There
  are **0 pending engine games**. (The shipped dossier had a stale **15-of-100** cache at depth 16
  reading "overall ACPL 14.3"; it was fully re-analysed at depth 12 before this report.)
- **Mixed time controls in the engine sample — and the "0 Lichess" header hides it.** Of the 100
  analysed games, **79 are classical** and **21 are online speed events** (chess.com *Titled
  Tuesday*). Those speed games sit inside the ChessBase PGNs, so they never show in the Lichess count.
  Because Dino plays a classical event, this report leads with the **classical-only** subset and
  flags where the headline numbers are inflated by speed games.
- **Command used:** `python prep_manual_app.py --analyze --scope player --player 9 --depth 12 --export`.

---

## 1. Executive Summary

Ang is the lowest-rated of the eight combatants, but the single most important fact about this
pairing is off the board: **he is a 15-year-old (born 2010) who made FM in 2025 and is the player in
this field most likely to be underrated.** A junior improving on the Malaysian/junior circuit gains
strength faster than the rating list updates, and his **entire 100-game file is fresh (Nov 2023 →
Dec 2025, 57 games in 2025 alone)** with zero ancient junior games to discount. **Do not prepare him
as a flat 2309 — treat 2309 as a floor.**

- **His weak side is the one Dino actually faces with White.** In classical play Ang is **18-13-9
  (61.2%) as White** but only **10-15-14 (44.9%) as Black**. Dino plays 1.e4, so **Dino's White game
  meets Ang's weaker defending half**, while **Dino's Black game meets Ang's stronger attacking half**
  — the danger pairing.
- **Dino's confidence weapons actually occur here** (unlike vs Thejkumar). As Black, Ang answers
  1.e4 with **1...c5 (Accelerated Dragon / Maróczy)** or **1...e5 (Ruy Lopez complex)**. Dino's
  **Rossolimo (3.Bb5)** sidesteps the Accelerated Dragon and his **Maróczy comfort zone**; Dino's
  **Center Game** sidesteps Ang's entire Ruy Lopez book. Both land Ang in fresh, low-theory problems.
- **The cleanest structural target plays straight to Dino's biggest strength.** As Black in an
  **Anti-Sicilian Counter-Package** structure Ang is **0-0-2 (0.0%) with a wretched ACPL 38.3**
  (small sample, 2 classical games) — and that family is **Dino's single best domain (96.0% over 25
  games)**. Meeting Ang's Sicilian with a Bb5 anti-Sicilian denies his strength and invites his worst.
- **He is shaky when scrambled, not when calculating slowly.** His **blitz (1993) trails his standard
  (2309) by ~300 points** — the classic junior signature. In a classical game that converts to:
  **pose fresh problems early so he burns clock**, then reach the later phases where his **endgame is
  his softest classical phase (ACPL 22.3)** under time pressure. It is a "make him work" edge, not a
  guaranteed collapse — his endgame is only moderately loose for a junior.
- **The harder game is Dino-Black vs Ang-White.** Ang's strong side runs on **g3 systems** — his
  **Catalan/Réti as White (27 games)** plus his **pet King's Indian Defence, Fianchetto (Uhlmann-Szabo)
  where he is 3-0-0, 100%**. Avoid the symmetrical squeeze and his pet line; unbalance early.
- **One-sentence game plan:** *With White, take Ang into Dino's home turf — a Bb5 anti-Sicilian vs
  1...c5 or the Center Game vs 1...e5 — to pose fresh problems that eat a junior's clock and steer
  toward his softer late phase; with Black, refuse the Catalan squeeze and his pet KID-Fianchetto,
  unbalancing with ...dxc4 / Benoni / Neo-Grünfeld — and respect that he is stronger than 2309.*

---

## 2. Opening Repertoire

*Result tables below are **classical-only**; openings with ≥2 classical games shown. Online/rapid
games are excluded because they roughly double his error rate and distort the percentages.*

**As White — 40 classical games, 61.2%.** A pure g3 player: 1.d4 / 1.Nf3 / 1.c4 into Catalan, Réti,
King's Indian Attack, Slav, and fianchetto-KID structures. No 1.e4. This is the side Dino faces when
he himself has Black.

| Line | ECO | Games | Score | Suggested action |
|---|---|---:|---:|---|
| King's Indian Attack | A07 | 4 | **37.5%** | **Softest White line by result (1-1-2)** and the home of his late blunders (§5) — but hard for Dino's Black repertoire to steer into |
| Slav Defense: Modern Line | D11 | 4 | 50.0% | Neutral; he is even here |
| King's Indian Defense: Fianchetto, Uhlmann-Szabo | E62 | 3 | **100.0%** | **His pet g3 weapon (3-0-0) — do not walk into it as Black** |
| King's Indian Attack: Spassky Variation | A05 | 2 | 25.0% | Soft (0-1-1), same KIA family as A07 |
| Catalan Opening: Open Defense | E04 | 2 | 50.0% | Neutral; the ...dxc4 lines are the right unbalancing try |
| Catalan Opening (main) | E00 | 2 | 50.0% | Neutral; draw-prone (0-2-0) |
| Zukertort Opening: Sicilian Invitation | A04 | 2 | 50.0% | Neutral |

**As Black — 39 classical games, 44.9%.** His weaker half, and the side Dino meets with White. He
answers 1.e4 with **1...c5 (Accelerated Dragon)** or **1...e5 (Ruy Lopez)**, and meets queen's-pawn
openings with the Slav.

| Line | ECO | Games | Score | Suggested action |
|---|---|---:|---:|---|
| Sicilian: Accelerated Dragon, Maróczy Bind | B36/B38 | 5 | 66.7% | **His best Black line — avoid the main line; Rossolimo (3.Bb5) sidesteps it** |
| Ruy Lopez: Morphy Defense, Anderssen | C77 | 2 | **0.0%** | His worst 1...e5 result (0-0-2) — but Dino plays the Center Game, not the Ruy |
| Ruy Lopez: Closed, Breyer/Zaitsev Hybrid | C95 | 2 | 25.0% | Soft (0-1-1); his 1...e5 complex leaks generally |
| Ruy Lopez: Closed, Anti-Marshall | C88 | 2 | 50.0% | Even |
| Slav Defense: Exchange | D10 | 2 | 50.0% | Draw-prone (0-2-0); not a target |
| English: Symmetrical, Fianchetto | A34 | 2 | 25.0% | Soft, but arises vs 1.c4 — won't occur vs Dino's 1.e4 |

### Repertoire-fit check (against Dino's own file)

- **Dino's e4 weapons apply — this is the opposite of the Thejkumar pairing.** Ang as Black plays
  open Sicilians and 1...e5, both reachable by 1.e4. Dino's **Moscow/Rossolimo (100%) and Center Game
  (100%) are live here**, where against Thejkumar they were moot.
- **vs 1...c5 → Rossolimo, not the open Sicilian.** Ang's main is the **Accelerated Dragon (2...Nc6,
  …g6), 66.7%/5 — his strongest Black line**, and he likes the Maróczy. Meeting 2...Nc6 with **3.Bb5
  (Rossolimo Fianchetto)** denies him both. Dino's record there is tested if not dominant —
  **Rossolimo B30 100%/2, Rossolimo Fianchetto B31 50%/2** — and the broader **Anti-Sicilian
  Counter-Package is his best structure (96.0%/25)**, versus Ang's **0-0-2 / ACPL 38.3** in it.
- **vs 1...e5 → Center Game.** Dino's **Center Game, Paulsen (C22) is 100%/3** and sidesteps Ang's
  entire Ruy Lopez book (where his only clear leak, the C77 Anderssen at 0/2, Dino could not reach
  through a Ruy anyway). The Center Game's value here is **fresh problems for a junior**, not a result
  table.
- **As Black, the KIA leak is real but hard to reach.** Ang's softest White line is the **KIA (A07
  37.5%, Spassky A05 25%)**, but the KIA arises against ...e6/...d5 French-type setups that are **not
  in Dino's Black repertoire** (Sicilian Dragon / Benoni / Grünfeld). Treat it as useful context, not
  a plan Dino can force.
- **As Black, avoid his comfort zone.** He scores **100% in his pet KID-Fianchetto (E62)** and is
  clean in the **Fianchetto-KID/Grünfeld family as White (75.0%, ACPL 14.4, 0 blunders)**. A
  symmetrical Catalan squeeze plays to his strength; prefer **...dxc4 Catalan, a Benoni (Dino lives
  there), or his 100% Neo-Grünfeld** to unbalance.

---

## 3. Phase Accuracy

*From 100 analysed OTB PGN games at depth 12. Lower ACPL = cleaner play. The classical/online split
is the most important row here.*

| Subset | Games | Record | Overall ACPL | Opening | Middlegame | Endgame | Blunders | Mistakes |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| All analysed | 100 | 40-30-30 (55.0%) | 23.0* | 8.7 | 20.0 | 30.1 | 37 | 94 |
| **Classical only** | **79** | **28-28-23 (53.2%)** | **17.5** | **8.2** | **15.1** | **22.3** | **15** | **55** |
| Online / rapid | 21 | 12-2-7 (61.9%) | 44.4 | 10.8 | 38.2 | 61.6 | 22 | 39 |

*The all-games overall/endgame figures are dominated by the online half and are shown only to expose
the inflation; use the classical row for every verdict. Note Ang actually **scores** better online
(61.9%) than classical (53.2%) while playing far **less accurately** — weaker Titled-Tuesday fields,
not a sign he is sharp at speed.*

**Interpretation (within-player only).** In classical chess Ang's **opening is his most accurate
phase (ACPL 8.2)** — a well-prepared junior who knows his lines — with the **middlegame (15.1)** and
**endgame (22.3)** progressively looser. His **15 classical blunders over 79 games** are not random:
they cluster in the **late middlegame / move-30+ transition** (see §5). This is a normal, slightly
loose-late junior profile, **not** an endgame leaker — phrase any endgame edge as "make him work,"
not "he collapses."

> **Underrated amplifier (read this against the accuracy table, not instead of it).** These numbers
> describe a 13–15-year-old across 2023–2025. A player improving this fast is, if anything,
> **stronger now than the file shows** — the opposite of the Thejkumar "rust" caveat. The clean
> opening ACPL means Dino will not catch him cold in theory; the edge is **position type and clock**,
> exploiting that his **blitz (1993) is ~300 points below his classical** — i.e. he is least
> comfortable when forced to improvise quickly in an unfamiliar structure.

---

## 4. Middlegame and Structure Notes

*Classical-only structure split by Ang's color (result **and** engine accuracy, which are separate
evidence types).*

| Structure family | His color | Games | Result % | ACPL | B/M | Read |
|---|---|---:|---:|---:|---:|---|
| Catalan / Réti Squeeze | White | 27 | 55.6% | 19.7 | 8/14 | His main White structure (10-10-7); beatable — losses to Romanov (GM) and others, real blunders |
| Fianchetto KID / Grünfeld | White | 10 | **75.0%** | 14.4 | 0/7 | **His comfort zone (7-1-2), cleanest engine play — do not invite it** |
| Reversed-Sicilian / Flank | White | 10 | 55.0% | 17.4 | 3/4 | Even (4-3-3); neutral |
| Catalan / Réti Squeeze | Black | 5 | 70.0% | 12.5 | 0/4 | Comfortable defending the squeeze too; not a target |
| Anti-Sicilian Counter-Package | Black | 2 | **0.0%** | **38.3** | 1/4 | **Worst sample on file (0-0-2), highest ACPL — tiny but striking, and Dino's home turf** |
| IQP / Panov Attack | White | 2 | 100.0% | 12.5 | 0/0 | Clean on a 2-game sample; don't hand him an IQP |

**Practical structure verdicts:**

- **Steer Ang into an anti-Sicilian.** His **Anti-Sicilian Counter-Package as Black (0/2, ACPL
  38.3)** is the standout soft spot — by both result and accuracy — and it is **exactly where Dino is
  strongest (96.0%/25)**. The sample is only 2 classical games, so treat it as a strong pointer, not
  a law; but a Bb5 anti-Sicilian is the right default regardless, because it also denies his best
  Black line (the Accelerated Dragon).
- **His Catalan/Réti as White is playable, not a wall.** 55.6% over 27 games with **8 blunders and
  ACPL 19.7** — strong GMs (Romanov) have beaten it, and the late errors are real. As Dino-Black the
  job is to **unbalance (…dxc4) rather than be squeezed**, where his accuracy and results are both
  more vulnerable.
- **Do not invite his fianchetto-KID world.** He is **75.0% with ACPL 14.4 and zero blunders** in the
  Fianchetto-KID/Grünfeld family as White, and **100%** in his pet Uhlmann-Szabo (E62). A symmetrical
  KID/Catalan plays straight into his best, cleanest structure.
- **Small-sample discipline.** Several families here are 2–10 games; weight the **2025 games** (57 of
  100) most heavily, and treat single-digit samples as pointers, not verdicts.

---

## 5. Endgame and Simplified Positions

The dossier's earlier "endgame ACPL 20.4 from 15 games" was a partial depth-16 cache. On the full
depth-12 re-analysis, his **classical** endgame ACPL is **22.3 — his weakest phase**, with the
blunders concentrated in the **move-30+ transition** rather than in pure technical endings. The
clearest classical late errors (move ≥ 30):

| Game | Move | Severity | Theme | Engine prefers |
|---|---|---|---|---|
| vs Jaiveer, Mahendru (Aug 2025) | 32.Nd3 | blunder (loss ~244) | Mishandled a KIA middlegame-to-ending as White | Bc1-e3 |
| vs Vidyarthi, Vyom (Abu Dhabi, Aug 2025) | 33.Kg1 | blunder (loss ~259) | King step allowed …Qxf2 in a KIA he then lost | Qd4xf2 (for the opponent) |
| vs Tran, Thanh Tu (KL MCF, Aug 2025) | 34.Bd4 | blunder (loss ~277) | Drifting in an equal Nimzo-as-White structure | h2-h3 |
| vs Romanov, Evgeny (Bangkok, Apr 2025) | 38.Rg3 / 34.Rxg4 | two blunders | Out-played in a Catalan Closed by a 2600+ GM | Kh5-h4 / Rg2xg4 |

**Honest phrasing for Dino:** *Ang's endgame is his softest classical phase, and his late blunders
are real and recent — but the gap is modest (22.3) and most errors are late-middlegame transition
mistakes as White in his own openings, not failures of basic technique. This is a "keep the game
complex into the first time control and make a junior calculate" edge, not a guaranteed endgame
collapse.* The clock angle reinforces it: complications that eat time hit hardest against a player
whose speed rating (1993 blitz) is far below his classical.

> **Mirror caution.** Dino's own depth-12 profile shows **endgame ACPL 36.7 with 4 drawing-defense
> failures** — i.e. Dino's late technique is currently *looser* than Ang's classical 22.3. Any
> "outlast the junior late" plan needs Dino to tighten his own conversion and drawing-defense first,
> and this matters most in the Dino-Black game, his flagged weak half.

---

## 6. Practical Game Plan for Dino

1. **With White, take him to Dino's home turf.** Against **1...c5**, play a **Bb5 anti-Sicilian
   (Rossolimo 3.Bb5)** — it denies Ang's best Black line (the Accelerated Dragon / Maróczy, 66.7%)
   and steers toward the **Anti-Sicilian Counter-Package, where he is 0/2 (ACPL 38.3) and Dino is
   96%**. Against **1...e5**, play the **Center Game (100%/3)** to dodge his Ruy Lopez book entirely.
2. **Win the opening by position type, not by theory.** His opening ACPL (8.2) is his cleanest phase,
   so do not hunt for a sharper line inside his prep. The goal is a **fresh, slightly unfamiliar
   middlegame** that makes a junior solve problems and **burn clock** — his blitz (1993) says that is
   where he is weakest.
3. **Keep the game complex into the first time control.** His softest classical phase is the endgame
   (ACPL 22.3) and his blunders cluster at move 30+. Don't simplify early and hope; make him calculate
   a live late middlegame.
4. **With Black (the hard game), refuse the squeeze.** Avoid a symmetrical Catalan and **never walk
   into his pet KID-Fianchetto (E62, 100%)**. Unbalance with **...dxc4 in the Catalan**, a **Benoni**
   (Dino's lived-in structure), or his **100% Neo-Grünfeld** — pose problems instead of being ground.
5. **Do not let the rating lull you.** Treat 2309 as a floor: he is a fast-improving 15-year-old and
   the highest upset risk per rating point in the field. Prep him like a stronger player.
6. **Tighten Dino's own Black and drawing-defense first.** Dino-Black meets Ang's stronger side; with
   Dino's 73.3% Black score, his repeated Dragon-line losses (moot here — Ang never plays 1.e4), and
   4/4 drawing-defense failures, the prep priority for *this* pairing is **non-Dragon Black** structures
   (Benoni / Neo-Grünfeld) and late-game defence.
7. **Model games to study:**
   - **vs Romanov, Evgeny (Bangkok 2025, Catalan Closed, 38 moves)** — how a strong player beats Ang's
     main White structure; two late blunders.
   - **vs Idani, Pouya** and **vs Flores Quillas (both Olympiad 2024, Ruy Lopez Anderssen C77, 0/2)** —
     his 1...e5 leak, even though Dino will reach it via the Center Game, not a Ruy.
   - **vs Quizon, Daniel (Wch U20 2024, Accelerated Dragon, 29 moves)** — how his pet Sicilian was
     punished; reinforces the case for sidestepping it with the Rossolimo.
   - **vs Vidyarthi, Vyom (Abu Dhabi 2025, KIA, 53 moves)** — a model of his soft KIA and a move-30+
     collapse as White; his most instructive recent classical loss.
   - **vs Wagh, Suyog (Penang 2025, Slav, 45 moves)** — his **most recent classical loss on file**
     (Dec 2025), the freshest read on his current form.

---

## Method & Caveats

- **Analysis command:** `python prep_manual_app.py --analyze --scope player --player 9 --depth 12 --export`.
- **Coverage:** 100 total games, 100 OTB PGNs, 0 Lichess rows, **100/100 analysed at depth 12**, 0
  pending. The shipped dossier's partial 15-of-100 cache (depth 16) was discarded and the full set
  re-analysed; a few stale depth-14/16 rows remain in the cache but are unused.
- **Time-control split:** 79 classical vs 21 online (chess.com Titled Tuesday). All accuracy and
  structure verdicts use the **classical** subset; all-games numbers are shown only to expose the
  speed-game inflation. The "0 Lichess online" header is misleading — the speed games are ChessBase
  PGNs.
- **Recency:** the file spans **Nov 2023 → Dec 2025** with **no pre-2010 games** and **57 of 100 in
  2025**. Unusually for this project the recency caution **inverts**: the evidence is current, and a
  rapidly improving junior is likely **stronger now than his file**.
- **Duplicate-game check:** 0 duplicate-candidate games (same date/opponent/move-count under two event
  spellings). The 2-game samples above are distinct games.
- **Underrated caveat:** born 2010, FM 2025, blitz 1993 ≪ standard 2309. Every percentage here is a
  *lower bound* on his true current strength; lean on fresh problems and the clock, not on his rating.
- **Known limitations:** depth 12 is a screening depth, not final engine truth; the standout
  anti-Sicilian and IQP targets rest on 2-game samples (flagged as pointers); result-score targets and
  engine-accuracy targets are reconciled explicitly (his Catalan/Réti is soft by result *and* shows
  real blunders, while his fianchetto-KID is clean on both counts).
