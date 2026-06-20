# Dino Ballecer — Round-by-Round Game Preparation

Standalone operational playbook for **FM Dino Ballecer (2372, PHI)** covering all nine rounds, **22–27 June 2026** (times Asia/Manila, UTC+8). It gives deep Black preparation for Rounds 1–2 and one-page match cards for Rounds 3–9. This document is separate from the Tournament Preparation Manual and does not modify it.

Recommendations are curated from the **improved seed reports** (Stockfish 18, depth 12) and the opponent dossiers. Where a seed report demoted a target, that decision is honored here. Move lines were replayed for legality with the workspace SAN validator before this file was rendered.

**Evidence labels** — `(C)` classical engine/result evidence · `(R)` rapid/online, tendency only · `(I)` inference from repertoire fit. **Color** — `● Black` (graphite) · `○ White` (slate). Dino's overall form: White **95.6%**, Black **73.3%** — the Black repertoire is the priority for this event. `(C)`

## Tournament Dashboard

Legend: `●` = Dino has Black (graphite) · `○` = Dino has White (slate). "Intention" is the planned opening; "priority" is the one thing to get right.

| Round / Date | Time · Bd | Color | Opponent | Rtg | Opening intention & prep priority |
|---|---|---|---|---|---|
| R1 · Mon Jun 22 | 16:00 · B5 | ● Black | IM Morris, James (AUS) | 2423 | Narrow Taimanov/Kan vs 1.e4; **no autopilot Dragon** |
| R2 · Tue Jun 23 | 10:00 · B1 | ● Black | IM Tan, Jun Ying (MAS) | 2404 | One ...Nf6/...e6/...d5 vs Réti/English; deny the g3 squeeze |
| R3 · Tue Jun 23 | 16:00 · B5 | ○ White | FM Arlan Cabe (PHI) | 2298 | Bb5 anti-Sicilian; public-file only (shared-coach gate) |
| R4 · Wed Jun 24 | 10:00 · B2 | ● Black | GM Vignesh, N R (IND) | 2515 | Solid Taimanov / QGD; **no clock race** vs the top seed |
| R5 · Wed Jun 24 | 16:00 · B4 | ○ White | GM Shyaam, Nikhil P (IND) | 2435 | Moscow/Rossolimo + Center Game; keep him solving |
| R6 · Thu Jun 25 | 16:00 · B3 | ● Black | IM Chan, Kim Yew (MAS) | 2360 | Anti-Catalan/Réti; long classical game, press move 30–40 |
| R7 · Fri Jun 26 | 10:00 · B3 | ○ White | FM Ang, Ern Jie Anderson (MAS) | 2309 | Rossolimo + Center Game; treat 2309 as a floor |
| R8 · Fri Jun 26 | 16:00 · B4 | ● Black | IM Susilodinata, Andrean (INA) | 2360 | Taimanov vs 1.e4 — **Dragon off the board** (he plays Yugoslav) |
| R9 · Sat Jun 27 | 16:00 · B2 | ○ White | GM Thejkumar, M. S. (IND) | 2358 | Two Knights Attack vs his Caro-Kann; out-stamina a rusty GM |

## Tournament-Wide Gates

Four standing rules that override any round-specific idea.

**Gate 1 — Keep the unrepaired Dragon off the board.** `(C)` Dino has **three documented losses** in the exact sequence `1.e4 c5 2.Nf3 d6 3.d4 cxd4 4.Nxd4 Nf6 5.Nc3 g6` (Dragon, Yugoslav Attack, Modern Line). Two opponents who open 1.e4 — **R8 Susilodinata** (plays the Yugoslav Attack) and any 1.e4 from **R1 Morris / R4 Vignesh** — could reach it. Default to the Taimanov/Kan package below. The Dragon may be used **only** if the written move-order repair (file + two model games + one checked fallback) has passed; otherwise it is forbidden.

**Gate 2 — Stay in Dino's anti-Sicilian strengths with White.** `(C)` Confirmed weapons to keep sharp, not replace: Moscow Main Line **9/9**, Moscow **5/5**, Rossolimo **2/2**, Anti-Sicilian Counter-Package **24/25 (96%)**, KIA vs the French **91.7%/6**, Center Game (Paulsen) **3/3**, Two Knights Attack vs the Caro-Kann **1/1**. Every White card is built from this set so no new theory is improvised mid-event.

**Gate 3 — Rehearse active-rook and drawing-defense technique.** `(C)` Dino's own endgame is his weakest phase (depth-12 ACPL **36.7**, with **4 drawing-defense failures** on file). Most opponents are *also* weakest in the endgame, so "press into a rook ending" only pays if Dino's technique is tighter than theirs. Before the event: pass one active-rook set and one Philidor/second-rank drawing-defense set under the clock.

**Gate 4 — Recovery on the three double-round days** (Tue Jun 23 = R2 + R3, Wed Jun 24 = R4 + R5, Fri Jun 26 = R7 + R8; plus the quick Mon-evening R1 → Tue-morning R2 turnaround). Morning game (10:00) → eat and reset, do not re-open theory in the 4-hour gap; fix only the *one* line the next opponent is most likely to play. Evening game (16:00) → short physical reset over deep prep. Lock each next-round opening choice the night before so double-round mornings need review, not decisions.

## Round 1 — ● Black vs IM Morris, James (2423)

*Mon Jun 22, 16:00, Board 5. Source: third improved seed report + DB (100 games).*

**Opponent snapshot.** `(C)` Active 2423 IM, broad/offbeat (62 openings), **60.4% as White**. As White he is a near-pure 1.e4 player who steers into **quiet, non-theoretical Sicilians** rather than sharp Open theory. His least accurate phase is the endgame (ACPL **36.2**: rook-behind-pawn, Philidor, conversion). No clock edge — he is strong across all time controls.

**Morris's first move (48 White games).** `(C)`

| Morris plays | Games | Dino's answer |
|---|---|---|
| `1.e4` | 43 | `1...c5` — Taimanov/Kan via `2...e6` (ladder below) |
| `1.Nf3` | 4 | `1...Nf6` heading for a Neo-Grünfeld `...g6/...d5` |
| `1.c4` | 1 | `1...Nf6` / `...g6 ...d5` central claim |

**What Morris does against `1...c5` (his anti-Sicilian mix).** `(C)` Of his Sicilians, White's 2nd move is `2.Nf3` ~11 and `2.Nc3` ~5; the tagged systems are **Closed Sicilian ×4**, **Moscow ×3**, Rossolimo, Grand Prix, plus `3.b3` (Westerinen) and `3.g3` (KIA) against `...e6`, and only an occasional true Open Sicilian (Najdorf/Classical). **Playing `2...e6` first denies him the Moscow/Rossolimo Bb5 systems entirely** (no `...d6`/`...Nc6` target), which is the main reason it is the recommended move order. `(I)`

### Ranked response ladder

**1 — Recommended: `1...c5` and `2...e6` (narrow Taimanov/Kan).** Durable, low-theory, and it sidesteps every Bb5 system. One main structure to know, six branches to recognize:

| If Morris plays | Branch | Reference line |
|---|---|---|
| `2.Nf3` then `3.d4` | Open Sicilian (Taimanov) | `1.e4 c5 2.Nf3 e6 3.d4 cxd4 4.Nxd4 Nc6 5.Nc3 Qc7 6.Be3 a6` |
| `2.Nf3` then `3.d4` | Open Sicilian (Kan) | `1.e4 c5 2.Nf3 e6 3.d4 cxd4 4.Nxd4 a6 5.Nc3 Qc7 6.Bd3 Nf6` |
| `2.c3` | Alapin | `1.e4 c5 2.c3 d5 3.exd5 Qxd5 4.d4 Nf6 5.Nf3 e6` |
| `2.Nc3` + `3.g3` | Closed Sicilian | `1.e4 c5 2.Nc3 e6 3.g3 d5 4.exd5 exd5 5.Bg2 Nf6` |
| `2.Nf3` + `3.d3`/`g3` | King's Indian Attack | `1.e4 c5 2.Nf3 e6 3.d3 Nc6 4.g3 d5 5.Nbd2 Nf6 6.Bg2 Be7` |
| `2.Nc3` + `f4` | Grand Prix | `1.e4 c5 2.Nc3 Nc6 3.f4 e6 4.Nf3 d5` |
| `2.Nf3` + `3.b3` | Westerinen / hedgehog | `1.e4 c5 2.Nf3 e6 3.b3 Nc6 4.Bb2 d5 5.exd5 exd5` |

**2 — Familiar backup: `2...Nc6`.** Use only if Dino prefers the structures. It must be played with eyes open to two things: Morris's Rossolimo, and the requirement to avoid Dino's loss move-order.
- Rossolimo: `1.e4 c5 2.Nf3 Nc6 3.Bb5 e6 4.O-O Nge7 5.c3 a6 6.Ba4` — or `3...g6 4.Bxc6 dxc6 5.d3 Bg7`.
- Accelerated-Dragon route that **avoids** the documented loss sequence (note: `...g6` without the `...d6/...Nf6/Nc3` order): `1.e4 c5 2.Nf3 Nc6 3.d4 cxd4 4.Nxd4 g6 5.c4 Bg7 6.Be3 Nf6 7.Nc3 Ng4` (Maróczy).

**3 — Dragon: behind a pass/fail repair gate only.** The exact line `1.e4 c5 2.Nf3 d6 3.d4 cxd4 4.Nxd4 Nf6 5.Nc3 g6` is Dino's 3-loss sequence. **Do not play it** unless the Gate-1 repair has passed. Listed here only so it is recognized and declined.

**4 — Caro-Kann: low-priority alternative.** `(C)`/`(I)` Morris scores only **33.3%** in the Caro-Kann Exchange as White, but Dino has **no practical Caro-Kann reps**, so this is a fallback to study, not a match plan: `1.e4 c6 2.d4 d5 3.exd5 cxd5 4.Bd3 Nc6`.

**Against `1.Nf3` / `1.c4` (rare).** Compact central claim into a Neo-Grünfeld, one of Dino's 100% structures: `1.Nf3 Nf6 2.c4 g6 3.g3 Bg7 4.Bg2 d5 5.cxd5 Nxd5 6.O-O`.

### Game notes

- **Expected middlegame:** a quiet Sicilian where Black equalizes comfortably and the game is decided later — exactly where Morris's endgame (ACPL 36.2) is loosest. Keep pieces and tension into the first time control rather than mass-trading early. `(C)`
- **Clock policy:** no time race; Morris is sharp at speed. Spend opening time confirming which quiet system he has chosen, then play on understanding. `(I)`
- **Match-day checklist:** ☐ Taimanov vs Kan choice locked ☐ Bb5 systems confirmed irrelevant after `2...e6` ☐ Dragon explicitly off ☐ Neo-Grünfeld vs `1.Nf3/1.c4` recalled ☐ one active-rook hold rehearsed.

## Round 2 — ● Black vs IM Tan, Jun Ying (2404)

*Tue Jun 23, 10:00, Board 1. Source: fourth improved seed report + DB (101 games) + TWIC rapid (Jun 17–19).*

**Opponent snapshot.** `(C)` Young, rising MAS IM (77 openings). As White he leans heavily on **English / Réti / g3 fianchetto** systems and tries to coast into a calm squeeze. Treat 2404 as a floor. His endgame is his weakest phase by a wide margin (ACPL **42.3**, **16 drawing-defense failures**), and his rapid/blitz are far below his classical — so pose early problems and make him spend clock.

**Tan's first move.** `(C)` classical: `1.Nf3` ×33, `1.d4` ×16, `1.e4` ×1. `(R)` tendency — his seven White games at the FIDE World Rapid Team (17–19 Jun 2026) were **four `1.Nf3`, three `1.d4`, zero `1.e4`**, all transposing to English/Réti/Catalan/QGD/KID structures with g3. The newest data only reinforces the classical picture.

### Ranked response ladder

**1 — Recommended: one `...Nf6 / ...e6 / ...d5` system** against everything, so move-order tricks transpose into the same Catalan/QGD structures:

| If Tan plays | Reference line |
|---|---|
| `1.Nf3` (main) | `1.Nf3 Nf6 2.c4 e6 3.g3 d5 4.Bg2 Be7 5.O-O O-O 6.d4 dxc4` |
| `1.d4` | `1.d4 Nf6 2.c4 e6 3.Nf3 d5 4.g3 Be7 5.Bg2 O-O 6.O-O dxc4` |
| `1.c4` (English) | `1.c4 e6 2.Nc3 d5 3.d4 Nf6 4.Nf3 Be7` |
| `1.b3` | `1.Nf3 Nf6 2.b3 g6 3.Bb2 Bg7 4.g3 O-O 5.Bg2 d6` |

**2 — Surprise option: early `...d5–d4` against the Réti** — *requires concrete checking before use.* `(R)` In the rapid event Tan was beaten exactly this way: `1.Nf3 d5 2.c4 d4 3.b4 c5 4.Bb2 Nf6` (Aswath–Tan, 0–1). A prepared one-game weapon, not a default.

**3 — Dino-native backup: `...g6` KID/Benoni — demoted.** `(C)`/`(R)` Tan scores well in King's-Indian structures (KID Orthodox `E94` 75%, plus a rapid KID win), so do not volunteer his comfort zone: `1.d4 Nf6 2.c4 g6 3.Nc3 Bg7` is a fallback only.

**4 — Rare `1.e4`:** transpose to the Round 1 anti-`1.e4` matrix (Taimanov/Kan). Do **not** switch to the Dragon.

### Game notes

- **Why this plan:** Tan's clearest result weakness is the **English Agincourt / Neo-Catalan Declined (`A14`), 0/4** `(C)` — reached precisely by meeting his fianchetto with an early `...d5` and `...dxc4`. The objective is to deny a frictionless g3 squeeze and force an early structural decision. `(I)`
- **Expected middlegame:** an Open Catalan / hanging-pawns or IQP-flavored structure with active pieces, steered toward a rook ending where his drawing-defense record is poor — but only pressed if Gate 3 is satisfied. `(C)`
- **Clock policy:** create the first real problem by move 10–12; his speed rating says time pressure is where he cracks. `(I)`
- **Model games to study:** Tan's `A14` losses vs Nguyen Ngoc Truong Son, Fus, Yu Jennifer, Sumets; then his §5 rook-ending samples. `(C)`
- **Match-day checklist (and double-round opener):** ☐ one move-order memorized for `1.Nf3`/`1.d4`/`1.c4` ☐ `...d5–d4` surprise checked or shelved ☐ `1.e4` → Taimanov, not Dragon ☐ recovery plan for R3 same evening.

## Round 3 — ○ White vs FM Arlan Cabe (2298)

*Tue Jun 23, 16:00, Board 5. Source: dossier only (81 games; no seed report; engine fingerprint unavailable). Evidence is opening-result based, not engine-based.*

> **Integrity gate.** Cabe is a PHI compatriot. This card is a **public-file audit only** — built from his published game record, with **no use of shared-coaching information**. Treat every read as a tendency from public games.

- **Likely branches** `(C)` — Cabe answers `1.e4` with `1...c5` ×20 (Najdorf, Lasker-Pelikan, Sicilian-French), `1...e5` ×3, and rare `...d6`/`...g6`/`...e6`.
- **Primary plan:** Dino's Bb5 anti-Sicilian. Vs `...d6` Najdorf order → Moscow `1.e4 c5 2.Nf3 d6 3.Bb5+ Nd7 4.O-O Ngf6 5.Re1 a6 6.Bf1`. Vs `...Nc6` → Rossolimo `1.e4 c5 2.Nf3 Nc6 3.Bb5`. Keeps Dino in his 96% Anti-Sicilian domain and out of Cabe's sharp Najdorf prep.
- **Fallback:** vs `1...e5`, Center Game `1.e4 e5 2.d4 exd4 3.Qxd4 Nc6 4.Qe3` (Dino 3/3); vs the French, KIA `1.e4 e6 2.d3 d5 3.Nd2`.
- **Line to avoid:** a sharp main-line Open Najdorf theory duel — Cabe is broad (70 openings) and booked there; the Bb5 systems sidestep it.
- **Target structure:** IQP / Panov — his softest family on file (**33.3%**, 3 games). `(C)`
- **Phase objective:** reach a clean middlegame a class ahead and convert; do not gamble for a refutation.
- **30-minute review:** Bb5+ Moscow vs `...d6` · Rossolimo vs `...Nc6` · Center Game vs `...e5` · KIA vs French · Cabe's recent Black losses in Keres/Najdorf/Pirc sharp lines.

## Round 4 — ● Black vs GM Vignesh, N R (2515)

*Wed Jun 24, 10:00, Board 2. Source: first improved seed report (187 games; 99 classical). Top seed, currently match-sharp.*

- **Likely branches** `(C)` — Vignesh's White is mixed: `1.e4` ×21, `1.d4` ×16, `1.Nf3` ×8, `1.c4` ×6. Expect a principled main line, not a trap.
- **Primary plan:** reuse the **Taimanov/Kan package** vs `1.e4` (R1 ladder); vs `1.d4/1.Nf3/1.c4` use the **R2 `...Nf6/...e6/...d5`** Catalan/QGD setup. One consistent Black structure across his whole move-order menu.
- **Fallback:** if he avoids theory, accept a solid equal middlegame and play the person, not the line.
- **Line to avoid:** **no clock race** (blitz 2453 > rapid 2381 — he is lethal in scrambles) and **no opening gamble** (opening ACPL **7.6**). Do not revive the Advance Caro-Kann "Tal" target — the seed report demoted it as Lichess-blitz-only. `(C)`
- **Target structure:** none to force; keep the game sound and reach a rook ending only with Gate-3 technique in hand (his endgame is his least-accurate phase but still strong, ACPL 17.6). `(C)`
- **Phase objective:** survive the opening even, deny him a risk-free squeeze, and make the top seed beat a solid position over the board.
- **30-minute review:** Taimanov vs `1.e4` · `...e6/...d5` vs `1.d4/Nf3/c4` · Dragon explicitly off · one drawing-defense hold (this is a double-round morning — review, don't re-learn).

## Round 5 — ○ White vs GM Shyaam, Nikhil P (2435)

*Wed Jun 24, 16:00, Board 4. Source: second improved seed report (101 games).*

- **Likely branches** `(C)` — Shyaam vs `1.e4`: `1...c5` ×19, `1...e5` ×7, rare `1...e6`.
- **Primary plan:** Dino's **Moscow/Rossolimo/KIA package**. Vs the Sicilian keep him in the Bb5 universe where his anti-Sicilian engine accuracy is most stressed (ACPL 16.3 as Black, despite good results). `1.e4 c5 2.Nf3 d6 3.Bb5+` / `2...Nc6 3.Bb5`.
- **Fallback:** vs `1...e5`, the **Center Game** `1.e4 e5 2.d4 exd4 3.Qxd4 Nc6 4.Qe3` (dodges his `...e5` theory); vs the French, the proven **KIA**.
- **Line to avoid:** a broad Open Sicilian / main-line Najdorf workload — his Najdorf is a soft 37.5% but only worth a **narrow** prepared sideline, not a new repertoire. `(C)`
- **Target structure:** his KIA-Symmetrical-as-Black (25%, small) and the engine-stressed anti-Sicilian middlegames; bring concrete ideas, not just the move order.
- **Phase objective:** make a strong GM solve middlegame problems in Dino's home structures; keep pieces on toward his weaker endgame (ACPL 17.0).
- **30-minute review:** Bb5 vs `...c5` · Center Game vs `...e5` · KIA vs French · Shyaam's Najdorf losses (Siva Kumar, Sathvik, Balakrishnan) · recovery after R4 same day.

## Round 6 — ● Black vs IM Chan, Kim Yew (2360)

*Thu Jun 25, 16:00, Board 3. Source: fifth improved seed report (classical subset, 60 games). Single-game day.*

- **Likely branches** `(C)` — Chan's White is universal: `1.d4` ×14, `1.Nf3` ×13, `1.e4` ×12, `1.c4` ×12. His strength is a clean **Catalan/Réti squeeze** (67.9%, ACPL 13.5); his **fianchetto-KID as White is draw-heavy** (41.7%, **0 wins in 6**).
- **Primary plan:** an **anti-Catalan/Réti** setup that denies the frictionless squeeze (R2 `...Nf6/...e6/...d5`, with `...dxc4` to unbalance), then steer toward his draw-heavy fianchetto-KID structures. If he plays `1.e4`, use the **Taimanov** (R1).
- **Fallback:** if he forces symmetry, hold the equalizer and play for the long game — he draws far more than he wins in these structures.
- **Line to avoid:** handing him a clean closed Catalan; and do **not** turn the game into a speed shuffle — his error rate roughly doubles online/at speed, but his **classical** endgame is clean (ACPL 20.8). `(C)`
- **Target structure / phase objective:** keep enough pieces on to reach the **move 30–40 transition**, where his classical loose moves cluster; this is a pressure-late plan, not an early-trade grind.
- **30-minute review:** one anti-Réti/Catalan move-order · `...dxc4` unbalancing idea · Taimanov vs `1.e4` · Chan's model losses (Heberla, KID-fianchetto collapse; Cruz Estrada, Black) · own drawing-defense.

## Round 7 — ○ White vs FM Ang, Ern Jie Anderson (2309)

*Fri Jun 26, 10:00, Board 3. Source: eighth improved seed report (classical subset, 79 games). Underrated 15-year-old — treat 2309 as a floor.*

- **Likely branches** `(C)` — Ang vs `1.e4`: `1...c5` ×10 (Accelerated Dragon / Maróczy, his best Black line) and `1...e5` ×10 (Ruy complex), `1...e6` ×3.
- **Primary plan:** take him to Dino's home turf. Vs `1...c5` play the **Rossolimo `3.Bb5`** — it sidesteps the Accelerated Dragon and lands him in the **Anti-Sicilian Counter-Package, where he is 0/2 (ACPL 38.3)** and Dino is **96%**. `1.e4 c5 2.Nf3 Nc6 3.Bb5 g6 4.Bxc6 dxc6 5.d3 Bg7 6.h3`. Vs `1...e5` play the **Center Game** `1.e4 e5 2.d4 exd4 3.Qxd4 Nc6 4.Qe3`, dodging his entire Ruy book.
- **Fallback:** vs the French, the proven KIA.
- **Line to avoid:** a main-line Open Sicilian into his Maróczy prep, and any sharp Ruy theory — both play to his preparation.
- **Target structure / phase objective:** win by **position type and clock**, not theory (his opening ACPL 8.2 is clean). Pose a fresh, slightly unfamiliar middlegame that makes a junior burn clock (blitz 1993 ≈ 300 below classical), then keep it complex into move 30+ (endgame his softest, ACPL 22.3).
- **30-minute review:** Rossolimo vs `...c5/...g6` · Center Game vs `...e5` · KIA vs French · Ang's model losses (Quizon, Accelerated Dragon; Vidyarthi, KIA collapse) · this is a double-round morning — review only.

## Round 8 — ● Black vs IM Susilodinata, Andrean (2360)

*Fri Jun 26, 16:00, Board 4. Source: sixth improved seed report (classical subset, 100 games).*

> **Dragon caution (Gate 1).** Susilodinata plays the **Yugoslav Attack against the Dragon** — exactly Dino's 3-loss structure. With Black vs his `1.e4`, **do not volunteer the Dragon.**

- **Likely branches** `(C)` — heavy `1.e4` ×42 (Scotch + principled anti-Sicilian), plus `1.d4` ×8 into the **Rapport-Jobava**. A solid, draw-heavy grinder (only 25 blunders in 100 games).
- **Primary plan:** vs `1.e4`, the **Taimanov/Kan package** (R1) — never the Dragon. Vs `1.d4` Rapport-Jobava, an **active Benoni / Neo-Grünfeld** (Dino's 100% Neo-Grünfeld) rather than a quiet symmetrical Slav, to pose real problems.
- **Fallback:** if he plays the Scotch (`1.e4 e5`?) Dino stays in his chosen `...c5`; keep to one Black structure.
- **Line to avoid:** the Dragon/Yugoslav, and his rock-solid **Advance Caro-Kann Tal** (irrelevant to Dino-Black, but noted: do not imagine it leaks). `(C)`
- **Target structure / phase objective:** win the **long** game — keep pressure into move 30+, where his 2024 results cracked; but tighten Dino's own endgame first (his ACPL 26.4 is cleaner than Dino's 36.7). Confidence point: Dino already beat him once (Oct 2025 rapid, Alapin as Black) — real, but rapid. `(R)`
- **30-minute review:** Taimanov vs `1.e4` (Dragon OFF) · Benoni/Neo-Grünfeld vs Rapport-Jobava · one drawing-defense hold · recovery after R7 same day.

## Round 9 — ○ White vs GM Thejkumar, M. S. (2358)

*Sat Jun 27, 16:00, Board 2. Final round. Source: seventh improved seed report (classical subset, 48 games). Inactive since Feb 2024, now coaching — expect rust.*

- **Likely branches** `(C)` — Thejkumar answers `1.e4` with **`1...c6` ×25 (near-pure Caro-Kann)**; essentially no Sicilian and no French. **Moscow/Rossolimo/KIA do not apply here — this is a Caro-Kann battle.**
- **Primary plan:** the **Two Knights Attack**, Dino's tested anti-Caro (B10, 100%/1), low-theory and sidestepping his deep Advance/Classical prep: `1.e4 c6 2.Nc3 d5 3.Nf3 Bg4 4.h3 Bxf3 5.Qxf3 Nf6`.
- **Fallback (trained only):** the **Advance** `1.e4 c6 2.d4 d5 3.e5 Bf5 4.Nf3 e6 5.Be2 c5`. His Advance-Short is 0/2 `(C)`, but Dino has **no Advance Caro reps** — use only if it has been drilled with model games; otherwise stay with the Two Knights.
- **Line to avoid:** out-theorizing a GM in his own trusted Caro lines (his opening ACPL 7.9 is his best phase). Win by structure type and stamina, not a sharper line.
- **Target structure / phase objective:** keep pieces on into the first time control — his endgame is his softest classical phase (ACPL 30.0) and a two-year layoff hurts late calculation and clock most.
- **30-minute review:** Two Knights main vs `1...c6` · Advance only if trained · Thejkumar's Advance-Short losses (Nikitenko, Mahdavi) · own conversion technique · it is the last round — bring a rested head, not new theory.

## Appendix — Evidence & Verification Notes

- **Sources.** Schedule, colors, boards, and ratings from `manual_sections/Tournament_Schedule.md`. Opponent reads from the eight `*_seed_report_improved.md` files (Stockfish 18, depth 12) and `manual_sections/Opponent_*.md`; Dino's profile from `manual_sections/Dino_Ballecer_Needs_Improvement.md`. Opening distributions queried from `prep_manual.db`. Tan's rapid tendency from the FIDE World Rapid Team PGN (17–19 Jun 2026).
- **Seed-report mapping (by seeding, not round).** R1 Morris = 3rd · R2 Tan = 4th · R4 Vignesh = 1st · R5 Shyaam = 2nd · R6 Chan = 5th · R7 Ang = 8th · R8 Susilodinata = 6th · R9 Thejkumar = 7th. R3 Cabe has no seed report (dossier only).
- **Evidence discipline.** `(C)` classical, `(R)` rapid/online tendency only, `(I)` inference. Rapid evidence never overrides classical results. Demoted targets in the improved seed reports are not revived here (e.g., Vignesh's Advance Caro "Tal" line).
- **Move legality.** Every line above was replayed through the workspace SAN validator (`fens_for` / `MiniBoard`, `prep_manual_app.py`); all sequences are legal from the start position.
- **Scope.** This playbook is the sole deliverable; it does not alter the manual, the database, or any application code.
