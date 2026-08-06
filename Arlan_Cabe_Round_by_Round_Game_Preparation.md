# Arlan Cabe — Round-by-Round Game Preparation

Standalone operational playbook for **FM Arlan Cabe (2298, PHI)** covering all nine rounds, **22–27 June 2026** (times Asia/Manila, UTC+8). It gives deep round-by-round preparation for Rounds 1–2 and 4–9. Round 3 (Dino Ballecer, a PHI compatriot who shares a coach) is deliberately kept to a brief public-file note under the shared-information integrity gate — not a preparation target, mirroring Dino's own playbook. This document is separate from the Tournament Preparation Manual and the Arlan Cabe Rounds 1–2 Coaching Workbook, and does not modify them.

Cabe is the **lowest seed in the field (2298)** and is outrated in eight of nine pairings, so the through-line is **resilient, low-variance preparation that fights up**: sound structures, his own best-scoring weapons, and pressure into the field's soft endgames — not theory duels against better-booked opponents.

**Evidence labels** — `(C)` classical engine/result evidence · `(R)` rapid/online, tendency only · `(I)` inference from repertoire fit. **Color** — `● Black` (graphite) · `○ White` (slate). Opponent engine reads are Stockfish-18 depth-12 classical; **Cabe's own profile is result-based — his file has no engine fingerprint**, so Cabe-side claims are repertoire/result evidence, not ACPL. Cabe's form: White **64.1%**, Black **47.6%** — his White games (1.e4) are where his results are strongest. `(C)`

## Tournament Dashboard

Legend: `●` = Cabe has Black (graphite) · `○` = Cabe has White (slate). "Intention" is the planned opening; "priority" is the one thing to get right.

| Round / Date | Time · Bd | Color | Opponent | Rtg | Opening intention & prep priority |
|---|---|---|---|---|---|
| R1 · Mon Jun 22 | 16:00 · B4 | ● Black | GM Thejkumar, M. S. (IND) | 2358 | **1–0, completed.** Slav Defense, Semi-Slav (`5.e3 a6`); 46 moves |
| R2 · Tue Jun 23 | 10:00 · B2 | ○ White | IM Morris, James (AUS) | 2423 | **0–1, completed.** Pirc Defense, Quiet Center (`5.Nc3 O-O`); 69 moves |
| R3 · Tue Jun 23 | 16:00 · B5 | ● Black | Dino Ballecer (PHI) | 2372 | **NEXT.** Compatriot — public-file only (shared-coach gate) |
| R4 · Wed Jun 24 | 10:00 · B1 | ● Black | IM Tan, Jun Ying (MAS) | 2404 | `...d5` anti-English/Réti; deny the g3 squeeze (A14 0/4) |
| R5 · Wed Jun 24 | 16:00 · B5 | ○ White | GM Vignesh, N R (IND) | 2515 | 1.e4 low-theory anti-Sicilian; **no gamble** vs the top seed |
| R6 · Thu Jun 25 | 16:00 · B2 | ● Black | GM Shyaam, Nikhil P (IND) | 2435 | Najdorf vs 1.e4 / `...d5` vs flank; pose problems |
| R7 · Fri Jun 26 | 10:00 · B4 | ○ White | IM Chan, Kim Yew (MAS) | 2360 | 1.e4 mainline anti-Caro; long game, press move 30–40 |
| R8 · Fri Jun 26 | 16:00 · B3 | ● Black | FM Ang, Ern Jie Anderson (MAS) | 2309 | `...d5` vs 1.d4 — **no `...g6`**; treat 2309 as a floor |
| R9 · Sat Jun 27 | 16:00 · B3 | ○ White | IM Susilodinata, Andrean (INA) | 2360 | 1.e4; sidestep his Advance-Caro Tal; out-press late |

## Tournament-Wide Gates

Four standing rules that override any round-specific idea.

**Gate 1 — Lowest seed: fight up with resilience, not bluff.** `(C)`/`(R)` At 2298 Cabe is outrated in eight of nine pairings (only the R3 gate game vs Dino is near-level). Against higher-rated, better-booked opponents the winning method is **solid, low-variance structures** that reach a playable middlegame where the rating gap matters least — then make them actually win. Avoid sharp theoretical duels where a 2400–2500 simply out-prepares him: Cabe's own losses in the **Keres Attack, Najdorf Opocensky (vs Gukesh), and Pirc Austrian** came exactly in such lines.

**Gate 2 — Consolidate the broad repertoire; no mid-event improvising.** `(C)`/`(I)` Cabe's file spans **70 distinct openings** — a real liability against opponents who can aim at the gaps. Lock **one** reliable system per defense before the event: as White (1.e4) one anti-Sicilian, one anti-Caro, one anti-French; as Black the **Najdorf** (with a solid backup) vs 1.e4 and **one `...d5` system** vs 1.d4/1.Nf3/1.c4. Decide the night before each round — double-round mornings need review, not decisions.

**Gate 3 — Target the field's soft endgames, but sharpen your own first.** `(C)` The pool's recurring weakness is the endgame: **Tan ACPL 42.3** (16 drawing-defense failures), **Morris 36.2**, **Thejkumar 30.0**, **Susilodinata 26.4**, **Ang 22.3**, **Chan (classical) 20.8**. Keep pieces on, reach the late phase, and press. Caveat: Cabe has **no engine profile**, so this only pays if he drills his own active-rook and conversion technique concretely (his Slav-Quiet loss to Milat is the warning).

**Gate 4 — Recovery on the three double-round days** (Tue Jun 23 = R2 + R3, Wed Jun 24 = R4 + R5, Fri Jun 26 = R7 + R8). Morning game (10:00) → eat and reset, do not re-open theory in the gap; fix only the *one* line the next opponent is most likely to play. Evening game (16:00) → short physical reset over deep prep. Lock each next-round opening the night before. (Bonus: the R3 evening game is the integrity-gate pairing, so the Tuesday double needs no evening prep.)

## Systems Library — Plans & Pawn Breaks

Single-source reference for the recurring systems used below. Each block covers piece routes, the pawn break that defines the plan, exchange policy, one tactical motif, and one engine-style cue. Round cards cross-link here so the same system is documented once.

### QGD / Slav `...d5` (Black, vs `1.d4`) — used R1, R8

- **Piece routes.** QGD: `Be7 + Nbd7 + Re8 + Nf8 → g6` Capablanca regrouping. Slav: `...dxc4 + ...Bf5 + ...e6 + ...Bb4` Krause.
- **Defining breaks.** `...c5` (the main equalizer in QGD, after `...b6` and `...Bb7`); `...e5` if White delays `Nf3`; `...dxc4 + ...b5 + ...a6` Slav anti-Meran when allowed.
- **Exchange policy.** QGD: trade pieces on the c-file once `...c5` lands. Slav: **keep the light-squared bishop on f5/g6** — it is the piece the Slav was built around; do not let it be traded for a knight without good reason.
- **Tactical motif.** `...Nxe4` shots when `Bg5` is overloaded; Cambridge Springs `...Qa5 + ...c6 + ...dxc4` if White goes classical `Bg5`.
- **Engine-style cue.** Vs Catalan-style `g3` setups, switch to the **Anti-Catalan with `...dxc4`** block below — different exchange policy.

### Anti-Catalan / anti-Réti with `...dxc4` (Black, `1.Nf3 d5 2.c4 e6 3.g3 Nf6 4.Bg2 Be7 5.O-O O-O 6.d4 dxc4`) — used R4, R6, R8

- **Piece routes.** `...a6 + ...b5 + ...Bb7` to hold the c4-pawn while developing; `...Nbd7 + ...Rc8`; `...Bf6` is the principal regrouping vs `Ne5`.
- **Defining breaks.** `...c5` (frees the bishop, opens the c-file); `...b5–b4` if White goes `Nbd2`.
- **Exchange policy.** Do **not** trade the light-squared bishop voluntarily — it is the piece the Catalan was built to neutralise. Trade dark-square bishops on `Bg5` if offered.
- **Tactical motif.** `...Nb6 + ...Bxg2 + ...Nbd5` to overload c4 recovery; `...c5 + ...cxd4 + ...Nb4` queenside swing.
- **Engine-style cue.** If White abandons c4 recovery for a kingside attack (`Ne5 + h4`), simplify with `...Nfd7 + ...Bf6` — White's compensation needs the bishop pair.

### Najdorf (Black, `1.e4 c5 2.Nf3 d6 3.d4 cxd4 4.Nxd4 Nf6 5.Nc3 a6`) — used R6

- **Piece routes.** `...e5 → Nb3 → ...Be6 + ...Nbd7 + ...Be7`; vs English Attack `...e5 + ...Be6 + ...Nbd7 + ...h5` (king-on-e7 plan).
- **Defining breaks.** `...e5` (Cabe's reliable Najdorf structure); `...d5` only after `...Nbd7/...Bb7/...Rc8` in Scheveningen flavours.
- **Exchange policy.** Trade dark-square bishops if offered; keep queens on for `...Qb6 → Qb4` queenside play.
- **Tactical motif.** `...Nxe4` if `Nc3` becomes overloaded; `...d5` central break exploiting `Nd4 + Nc3` if White delays.
- **Engine-style cue.** **Cabe has documented leaks** in Keres Attack and Najdorf Opocensky — if a 2435+ goes there, switch to a solid Moscow fallback (`1.e4 c5 2.Nf3 d6 3.d4 cxd4 4.Nxd4 Nf6 5.Nc3 → Be3/Bg5`) rather than walk into prep.

### Anti-Nimzowitsch d5-wedge (White, `1.e4 Nc6 2.d4 d5 3.Nc3 dxe4 4.d5`) — used R2

- **Piece routes.** `c4 + Nge2 + Be3` to support the d5-wedge; queen to `d2 → Rd1` long castling principled.
- **Defining break.** `d5–d6` wedge if Black plays `...Ne5` and forgets defence; `f3` to recover e4 if Black insists on holding the pawn.
- **Exchange policy.** Avoid trading the d-pawn — it is the entire idea. Trade knights for bishops if offered (`Bxf3 → gxf3` is fine).
- **Tactical motif.** `Nxe4 + Bg5 + Qd4` triple attack against `...Nf6`; `d5–d6` wedge fork on c7/e7.
- **Engine-style cue.** Morris scores **21%** in this structure (0W 3D 4L) — the whole prep is to reach this position and play sound chess. Do not search for a refutation; equality-from-White wins.

### KIA anti-Sicilian (White, `1.e4 c5 2.Nf3 e6 3.d3 Nc6 4.g3 d5 5.Nbd2 Nf6 6.Bg2 Be7`) — used R5

- **Piece routes.** `O-O + Re1 + Nf1 → h2`; pawn to `e5` once Black commits the f6-knight; queen to `e2 → e3`.
- **Defining break.** `e5` (the King's Indian Attack thrust); `c3 + d4` if Black overcommits to the queenside.
- **Exchange policy.** Hold the dark-squared bishop on the long diagonal; trade light-squared bishops only if it opens `f5` for the knight.
- **Tactical motif.** `Nh2 + f4 + e5` kingside roller; `Bf4 + Qd2 + h4` if Black castles short and the e-file is closed.
- **Engine-style cue.** Vs a 2515 (Vignesh), use this as an **equalizer not an attacker** — accept symmetry around move 15 rather than overcommitting to a slow kingside attack.

### Anti-Caro mainline (White, `1.e4 c6 2.d4 d5 3.Nc3 dxe4 4.Nxe4`) — used R7

- **Piece routes.** `Ng3` (vs `...Bf5`) then `Nf3 + h4`; bishop to `d3`; queen to `d2 → e2`.
- **Defining break.** `c4` push only after `O-O-O + Kb1`; otherwise it is a quiet manoeuvring game.
- **Exchange policy.** Trade Black's light-squared bishop on h7 (after `Bxd3`); keep the dark-squared bishop for the long diagonal.
- **Tactical motif.** `Ne5` lever against `...Bg6` or `...Bh7`; `Nf5` jumps when Black delays `...e6`.
- **Engine-style cue.** Chan's classical play is clean — the leverage is move 30–40, not the opening. Don't expect to win the Caro in the first 20 moves.

### Two Knights anti-Caro (White, `1.e4 c6 2.Nc3 d5 3.Nf3 Bg4 4.h3 Bxf3 5.Qxf3 Nf6`) — used R9

- **Piece routes.** Queen `f3 → g3`; `d3 + Bg5`; long castling principled.
- **Defining break.** `e5` (kicking f6) when Black commits `...e6` without `...Nbd7`; `g4 → g5` wedge after `O-O-O`.
- **Exchange policy.** Accept the bishop trade gratefully; two-bishops vs one-knight balance is fine while the pawn structure stays flexible.
- **Tactical motif.** `Bxf6 + Nxd5` exchange sac if Black recaptures with the queen; `Nd5` jumps when `...e6` weakens dark squares.
- **Engine-style cue.** Susilodinata's Advance-Caro Tal is 75% — sidestepping into the Two Knights gives Cabe a fresh structure his opponent has less depth in.

## Round 1 — ● Black vs GM Thejkumar, M. S. (2358)

*Completed Mon Jun 22, 16:00, Board 4. Source: official Round 1 PGN + seventh improved seed report (classical subset, 48 games) + DB.*

> **Result — 1–0 (46 moves).** Thejkumar–Cabe, Singapore, 22 June 2026. Arlan lost with Black.

### Post-game update — Round 1

- **Actual opening.** Arlan chose the **Slav Defense, Semi-Slav Variation (D45)**: `1.d4 d5 2.c4 c6 3.Nf3 Nf6 4.Nc3 e6 5.e3 a6 6.b3 c5`, heading into the recommended Slav/Semi-Slav setup.
- **Game shape.** White played `6.b3`, and Arlan countered with `6...c5`. Thejkumar gradually increased pressure on the queenside, exchanging dark-squared bishops (`20.Bxd7 Nxd7`). In the late middlegame, White's rooks occupied the active files, winning queenside pawns.
- **Finish.** White's active rooks and extra material forced Arlan to resign on move 46.
- **Prep implication.** The playbook's recommended Slav/Semi-Slav path was followed. Thejkumar's endgame play was solid, and the long layout did not yield the expected Rust blunders from the GM.

**Opponent snapshot.** `(C)` A genuine GM (2358) but **effectively inactive — no FIDE-rated games since Feb 2024, now coaching** — so expect OTB rust in long-game calculation and clock handling. In the classical subset he is **21W 15D 12L (59.4%)**, with his **opening his best phase (ACPL 7.9)** and his **endgame his weakest (ACPL 30.0, 24 blunders / 48)**, clustered in the move-30+ transition. As White he is a near-pure **1.d4** player (Ragozin/QGD, Semi-Slav, Slav, occasional KID-as-White E97 100%). `(C)`

**Thejkumar's first move (54 White games).** `(C)`

| Thejkumar plays | Games | Cabe's answer |
|---|---|---|
| `1.d4` | 53 | `1...d5` — QGD / Slav (solid main line) |
| `1.e4` | 1 | `1...c5` — Najdorf (his rare `1.e4`) |

**Why solid, not sharp.** `(I)` Cabe meets `1.d4` with his `...d5`. Thejkumar is comfortable and clean in his queen's-pawn universe (opening ACPL 7.9), so there is no opening trick to set — the plan is a sound structure that reaches the middlegame and then the late phase, where a two-year layoff hurts a coach most.

### Ranked response ladder

**1 — Recommended: solid `...d5` (QGD / Slav).** Reach a known, resilient structure and play the long game:

| If Thejkumar plays | Branch | Reference line |
|---|---|---|
| `2.c4 e6` | QGD | `1.d4 d5 2.c4 e6 3.Nc3 Nf6 4.Nf3 Be7 5.Bg5 O-O` |
| `2.c4 c6` | Slav | `1.d4 d5 2.c4 c6 3.Nf3 Nf6 4.Nc3 dxc4 5.a4 Bf5` |
| `2.Nf3` / `g3` | Catalan-decline | `1.d4 d5 2.c4 e6 3.g3 Nf6 4.Bg2 Be7 5.Nf3 O-O` |

**Critical position (QGD reference line, White to move 6):** `rnbq1rk1/ppp1bppp/4pn2/3p2B1/2PP4/2N2N2/PP2PPPP/R2QKB1R w KQ - 6 6`. *Thejkumar-specific:* expect the Cambridge-Springs (`7.e3 h6 8.Bh4`) or Exchange (`8.Bxf6`) — be ready with `8.Bh4 b6 9.Bd3`. Plans/breaks: **Systems Library — QGD / Slav**.

**2 — Backup: `...Nf6` Nimzo to unbalance.** If Cabe wants more imbalance — but **do not volunteer a pure KID** (Thejkumar is 100% vs the KID-as-White): `1.d4 Nf6 2.c4 e6 3.Nc3 Bb4 4.e3 O-O`.

**3 — vs his rare `1.e4`: Najdorf.** Cabe's main Sicilian: `1.e4 c5 2.Nf3 d6 3.d4 cxd4 4.Nxd4 Nf6 5.Nc3 a6`.

**Lines to avoid.** `(C)` Feeding him a KID-as-White (E97, 100%); a dry symmetric exchange line that lets a GM hold comfortably — keep some imbalance into the middlegame.

### Game notes

- **Expected middlegame:** a QGD/Slav structure with pieces on, steered toward the move-30+ phase where his endgame (ACPL 30.0) and rust show. `(C)`
- **Phase objective:** out-stamina a rusty GM — don't out-theory him (his opening 7.9 is his best phase). `(C)`
- **Clock policy:** opening round, fresh — invest time to reach a sound middlegame, then make him calculate late. `(I)`
- **Mirror caution (own side):** against a rusty-but-real GM, Cabe must hold his own technique; his Slav-Quiet loss (vs Milat) is the warning. `(C)`
- **Model games to study:** Thejkumar's late-phase losses — Nikitenko (Semi-Slav, 39.Qe4) and Fominyh (QGA ending, 37.Rc1); freshest game QID vs Ghosh (Bangalore, Jan 2024). `(C)`

**Match-day checklist:**

- ☐ QGD vs `2.c4 e6`
- ☐ Slav vs `Nf3`
- ☐ no pure KID
- ☐ Najdorf ready for rare `1.e4`
- ☐ one drawing-defense hold (Gate 3)

### In-Game Card — R1 ● Black vs Thejkumar (GM, 2358, two-year layoff)

**Opening choice.** Solid `...d5` (QGD/Slav) vs `1.d4`; Najdorf vs his rare `1.e4`.

**Three middlegame plans (Black).** (1) `...c5` break to free the position; (2) `...Re8 + ...Nf8 → g6` Capablanca regrouping in QGD `Bg5` lines; (3) keep pieces on to move 30+ (his endgame ACPL 30.0 + rust).

**Avoid.** Pure KID (he is 100% vs KID-as-White, E97); dry exchange Slav that lets a GM hold.

**Time budget (90+30, inc 30).** Opening to move 12 ≤ 20m · moves 13–25 ≤ 50m · moves 26–40 ≤ 50m · reserve 5m.

**Win condition.** Out-stamina a rusty GM. **Mirror caution:** Cabe has no engine profile — his Slav-Quiet loss to Milat is the warning.

## Round 2 — ○ White vs IM Morris, James (2423)

*Completed Tue Jun 23, 10:00, Board 2. Source: official Round 2 PGN + third improved seed report (100 games) + DB.*

> **Result — 0–1 (69 moves).** Cabe–Morris, Singapore, 23 June 2026. Arlan lost with White.

### Post-game update — Round 2

- **Actual opening.** Arlan opened `1.e4` and Morris answered with the **Pirc Defense, Quiet Center (B08)**: `1...d6 2.d4 Nf6 3.Nc3 g6 4.Nf3 Bg7 5.Be2 O-O 6.h3 a6`, which was the third priority in the response ladder.
- **Game shape.** Arlan played the recommended Anti-Pirc Center line with `5.Be2` and `6.h3`, but Morris generated active counterplay on both flanks. White's position became compromised in the late middlegame, and Black launched a kingside attack.
- **Finish.** Morris penetrated with his queen and rook, forcing checkmate on move 69.
- **Prep implication.** The game followed the Pirc Defense branch instead of the preferred Nimzowitsch (`1...Nc6`) or French (`1...e6`). Morris's late-game tactical alertness decided the game.

**Opponent snapshot.** `(C)` Active 2423 IM, broad/offbeat (**62 openings**), 56% overall — stronger as White (60.4%) than Black (51.9%), so **Cabe's White game meets Morris's softer half**. His phase profile is opening 11.1 / middlegame 19.1 / **endgame 36.2** (his worst by far, **53 blunders / 100**) — late-game volatility is the lever. No clock edge (strong at all time controls). As Black he answers `1.e4` with `1...Nc6` (Nimzowitsch), `1...e6` (French), `1...d6` (Pirc). `(C)`

**Morris's answer to `1.e4` (26 of 52 Black games met `1.e4`).** `(C)`

| Morris plays | Games | Cabe's weapon |
|---|---|---|
| `1...Nc6` | 15 | Anti-Nimzowitsch `2.d4`/`2.Nf3` (his 21% leak) |
| `1...e6` | 8 | Anti-French (Tarrasch `3.Nd2` or KIA) |
| `1...d6` | 3 | Anti-Pirc `2.d4` + `3.Nc3` |

**Why this is the soft half.** `(C)` Morris's clearest result weakness as Black is the **Nimzowitsch Defense: Williams Variation — 0W 3D 4L (21.4%)** over 7 games. Cabe already plays `1.e4`, so a clear anti-Nimzowitsch line is the lowest-workload, highest-value prep of the round.

### Ranked response ladder

**1 — Recommended vs `1...Nc6` (Nimzowitsch): a clear central line.** Don't improvise — head for the Williams structure where Morris is 21%:

| If Morris plays | Branch | Reference line |
|---|---|---|
| `2.d4 d5` | Williams main | `1.e4 Nc6 2.d4 d5 3.Nc3 dxe4 4.d5` |
| `2.Nf3` | flexible | `1.e4 Nc6 2.Nf3 d6 3.d4 Nf6 4.Nc3` |

**Critical position (Williams reference line, Black to move 4):** `r1bqkbnr/ppp1pppp/2n5/3P4/4p3/2N5/PPP2PPP/R1BQKBNR b KQkq - 0 4`. *Morris-specific:* the c6-knight must move — main is `4...Ne5 5.Qd4 Ng6 6.Nxe4`; `4...Nb8` is depressing for Black. Hold the d5-wedge with `c4 + Nge2` and trade into the endgame. Plans/breaks: **Systems Library — Anti-Nimzowitsch**.

**2 — vs `1...e6` (French): pick one and stick to it.** Tarrasch `1.e4 e6 2.d4 d5 3.Nd2 Nf6 4.e5 Nfd7 5.Bd3`, or the KIA `1.e4 e6 2.d3 d5 3.Nd2`.

**3 — vs `1...d6` (Pirc): a straightforward big centre.** `1.e4 d6 2.d4 Nf6 3.Nc3 g6 4.Nf3 Bg7 5.Be2`.

**Lines to avoid.** `(C)` A casual quiet line that lets a tactically strong IM equalize for free; out-booking him in sharp mainlines is unnecessary when his endgame (36.2) is the field's loosest.

### Game notes

- **Expected middlegame:** a sound `1.e4` structure steered toward simplification, where Morris's endgame (rook-activity / Philidor / conversion errors) is loosest. `(C)`
- **Phase objective:** reach a playable-to-better ending and press — Morris is the field's weakest finisher. `(C)`
- **Clock policy:** double-round morning — review only; no clock edge to chase, play on understanding. `(I)`
- **Model games to study:** Morris's Nimzowitsch-Williams losses (Parondo, Kevlishvili, Martinez Alcantara, Sanal); his §5 endgame samples (Gavilan Diaz, Bortnyk, Vokhidov). `(C)`

**Match-day checklist (double-round morning):**

- ☐ anti-Nimzowitsch vs `1...Nc6` locked
- ☐ one anti-French chosen (Tarrasch *or* KIA)
- ☐ anti-Pirc ready
- ☐ R3 is the gate game — no prep needed
- ☐ recovery plan

### In-Game Card — R2 ○ White vs Morris (IM, 2423)

**Opening choice.** `1.e4`. Vs `1...Nc6` (Nimzowitsch) → `2.d4 d5 3.Nc3 dxe4 4.d5` (Williams 21% line); vs `1...e6` → Tarrasch or KIA (pick one); vs `1...d6` → big-centre Pirc.

**Three middlegame plans (White).** (1) the d5-wedge cramps his Nc6 — defend it with `c4 + Nge2`; (2) trade into the endgame — his ACPL there is 36.2; (3) avoid early piece simplification; keep the d5-bind alive.

**Avoid.** A quiet line that lets a tactical IM equalize for free; out-booking him in sharp mainlines.

**Time budget (post-double morning).** Review only; play on understanding (no clock edge to chase).

**Win condition.** Reach a playable-to-better endgame; he is the field's weakest finisher (53 blunders / 100).

## Round 3 — ● Black vs Dino Ballecer (2372)

*Tue Jun 23, 16:00, Board 5. The compatriot pairing — public-file note only; no preparation built.*

> **Integrity gate.** Dino Ballecer is a PHI compatriot who **shares a coach** with Cabe. This card is intentionally a brief public-record note, with **no use of shared-coaching information** and **no worked-up game plan** — the mirror of how Dino's own playbook treats this same game. By the players' choice, neither side prepares deeply against the other.

- **Pairing:** Cabe has Black; Dino opens `1.e4`. From public games Dino is a `1.e4` player with a strong anti-Sicilian record, and Cabe answers `1.e4` with the Sicilian (Najdorf). `(I)`
- **Approach:** play a normal, principled game on general understanding — no scouting edge is used or implied. `(I)`
- **Double-round note:** this evening game needs no opening preparation, which is itself a recovery advantage on the Tuesday double (see Gate 4).

### In-Game Card — R3 ● Black vs Dino Ballecer (FM, 2372)

**Integrity gate.** No deep prep used. Play a principled Sicilian on general understanding — no scouting edge is implied. *Recovery focus:* this evening game needs no opening prep — sleep early for the R4 double-round morning.

## Round 4 — ● Black vs IM Tan, Jun Ying (2404)

*Wed Jun 24, 10:00, Board 1. Source: fourth improved seed report (101 games) + DB. Double-round morning; treat 2404 as a floor (rising junior IM).*

**Opponent snapshot.** `(C)` Young, rising MAS IM (**77 openings**), 53% overall, likely stronger than 2404. As White he leans **English / Réti / g3 fianchetto** (`1.Nf3` ×33, `1.d4` ×16). His endgame is his weakest phase by a wide margin (**ACPL 42.3, 16 drawing-defense failures**) and his rapid/blitz are far below classical — pose early problems and make him spend clock. His **English Agincourt / Neo-Catalan Declined (A14) is 0/4**. `(C)`

**Tan's first move (50 White games).** `(C)`

| Tan plays | Games | Cabe's answer |
|---|---|---|
| `1.Nf3` | 33 | `1...d5` → `...e6` (decline the Catalan) |
| `1.d4` | 16 | `1...d5` QGD / Slav |
| `1.e4` | 1 | `1...c5` Najdorf (rare) |

**Why `...d5` and decline.** `(C)`/`(I)` Meeting his fianchetto with an early `...d5/...e6` (and `...dxc4`) heads for the **A14 structure where Tan is 0/4**, denying him the frictionless g3 squeeze and forcing an early structural decision.

### Ranked response ladder

**1 — Recommended: one `...d5/...e6` system vs `1.Nf3 / 1.d4 / 1.c4`.** Transpose his move-orders into one Catalan/QGD structure with `...dxc4`:

| If Tan plays | Reference line |
|---|---|
| `1.Nf3` | `1.Nf3 d5 2.c4 e6 3.g3 Nf6 4.Bg2 Be7 5.O-O O-O 6.d4 dxc4` |
| `1.d4` | `1.d4 d5 2.c4 e6 3.Nf3 Nf6 4.g3 Be7 5.Bg2 O-O 6.O-O dxc4` |
| `1.c4` | `1.c4 e6 2.Nc3 d5 3.d4 Nf6 4.Nf3 Be7` |

**Critical position (after `1.Nf3` anti-Catalan reference line, White to move 7):** `rnbq1rk1/ppp1bppp/4pn2/8/2pP4/5NP1/PP2PPBP/RNBQ1RK1 w - - 0 7`. *Tan-specific:* he'll try `Qc2 + a4` (structural squeeze) — meet with `...a6 + ...b5 + ...Bb7`. Press toward a rook ending (his record: 16 draw-defense failures). Plans/breaks: **Systems Library — Anti-Catalan with `...dxc4`**.

**2 — vs rare `1.e4`: Najdorf.** `1.e4 c5 2.Nf3 d6 3.d4 cxd4 4.Nxd4 Nf6 5.Nc3 a6`.

**Lines to avoid.** `(C)` Drifting into a clean closed Catalan squeeze; his comfortable KID-as-White (E94, 75%) — don't volunteer a KID. Keep the imbalance via `...dxc4`.

### Game notes

- **Expected middlegame:** an Open-Catalan / QGD with `...dxc4`, steered toward a rook ending where Tan's drawing-defense record is poor (16 failures). `(C)`
- **Phase objective:** deny the g3 squeeze; create the first real problem by move 10–12 and make a junior spend clock (rapid/blitz far below classical). `(C)`/`(I)`
- **Clock policy:** double-round morning — review only; pose problems early. `(I)`
- **Model games to study:** Tan's A14 losses (Nguyen Ngoc Truong Son, Fus, Yu Jennifer, Sumets); his §5 endgame samples (Schnaider, Smail). `(C)`

**Match-day checklist (double-round morning):**

- ☐ one `...d5` move-order for `1.Nf3/1.d4/1.c4`
- ☐ `...dxc4` unbalancing idea
- ☐ Najdorf for rare `1.e4`
- ☐ R5 (Vignesh, White) locked the night before

### In-Game Card — R4 ● Black vs Tan (IM, 2404)

**Opening choice.** One `...d5/...e6` system vs `1.Nf3/d4/c4`; `...dxc4` to unbalance. Najdorf vs rare `1.e4`.

**Three middlegame plans (Black).** (1) hold the c4-pawn with `...a6 + ...b5 + ...Bb7`; (2) `...c5` break; (3) press into a rook ending — his record is 16 draw-defense failures.

**Avoid.** Clean closed Catalan squeeze; KID-as-White (he scores 75% in E94).

**Time budget (post-double morning).** Review only; first real problem by move 10–12.

**Win condition.** A14 Neo-Catalan structure where he is 0/4.

## Round 5 — ○ White vs GM Vignesh, N R (2515)

*Wed Jun 24, 16:00, Board 5. Source: first improved seed report (187 games; 99 classical) + DB. Top seed, match-sharp; double-round evening.*

**Opponent snapshot.** `(C)` The **strongest player in the field (2515)** and currently match-sharp (7/9 at Sevilla 2026). Classical **69.7%**, broad (**128 openings**), **opening his cleanest phase (ACPL 7.6)**, endgame loosest-but-strong (17.6). **Blitz (2453) > rapid (2381)** — dangerous in scrambles. As Black he plays the Sicilian (`1...c5` ×16), `1...e5` (7), and the Caro (`1...c6` ×4). There is no cheap target — the realistic underdog aim is a sound game with no gift. `(C)`

**Vignesh's answer to `1.e4` (27 of 53 Black games met `1.e4`).** `(C)`

| Vignesh plays | Games | Cabe's weapon |
|---|---|---|
| `1...c5` | 16 | Low-theory `2.Nf3 + d3/g3` (sidestep his Najdorf prep) |
| `1...e5` | 7 | Sound open game `2.Nf3` |
| `1...c6` | 4 | Mainline anti-Caro |

**Why solid, no gamble.** `(C)`/`(I)` Against the top seed the plan is **survival and soundness, not a refutation**: equalize-from-White cleanly, deny a risk-free squeeze, and make a 2515 actually win over the board. His opening ACPL 7.6 means gambles don't pay; his scramble strength means **no clock race**.

### Ranked response ladder

**1 — Recommended vs `1...c5`: a low-theory `d3/g3` setup Cabe already plays.** Dodge a Najdorf theory duel against a 2515:

| If Vignesh plays | Branch | Reference line |
|---|---|---|
| `2...e6` / `...d6` | KIA / small centre | `1.e4 c5 2.Nf3 e6 3.d3 Nc6 4.g3 d5 5.Nbd2 Nf6 6.Bg2 Be7` |
| open alternative | sound Open Sicilian | `1.e4 c5 2.Nf3 Nc6 3.d4 cxd4 4.Nxd4 Nf6 5.Nc3 e6` |

**Critical position (KIA reference line, White to move 7):** `r1bqk2r/pp2bppp/2n1pn2/2pp4/4P3/3P1NP1/PPPN1PBP/R1BQK2R w KQkq - 4 7`. *Vignesh-specific:* typical continuation `7.O-O O-O 8.Re1 b5 9.e5 Nd7 10.Nf1` — **accept equality cleanly**, do not overcommit to a slow kingside attack vs a 2515. Plans/breaks: **Systems Library — KIA anti-Sicilian**.

**2 — vs `1...e5`: a sound open game.** Cabe plays both — the Ruy `1.e4 e5 2.Nf3 Nc6 3.Bb5 a6 4.Ba4 Nf6 5.O-O`, or the Italian `3.Bc4`.

**3 — vs `1...c6`: a non-committal mainline anti-Caro.** `1.e4 c6 2.d4 d5 3.Nc3 dxe4 4.Nxe4` — solid, no theory gamble.

**Lines to avoid.** `(C)` A sharp Open-Najdorf main-line battle against a match-sharp 2515; any opening gamble (his opening is his best phase); and any clock race against his blitz strength.

### Game notes

- **Expected middlegame:** a sound, roughly balanced structure — accept equality and play the person, not the line. `(I)`
- **Phase objective:** survive the opening even and make the top seed grind; the realistic underdog result is built late. `(C)`
- **Clock policy:** double-round evening — short reset over deep prep; no scramble vs his blitz strength. `(R)`/`(C)`
- **Model games to study:** how Vignesh has been held or beaten — Aaditya Dhingra 2026, Goh Zi Han 2026, Sukovic 2025. `(C)`

**Match-day checklist (double-round evening):**

- ☐ low-theory anti-Sicilian chosen (no Najdorf duel)
- ☐ open-game line vs `1...e5`
- ☐ mainline anti-Caro vs `1...c6`
- ☐ recovery done after R4

### In-Game Card — R5 ○ White vs Vignesh (GM, 2515, top seed)

**Opening choice.** Low-theory `2.Nf3 + d3/g3` vs `1...c5` (no Najdorf duel); sound open game vs `1...e5`; non-committal anti-Caro mainline vs `1...c6`.

**Three middlegame plans (White).** (1) accept equality; (2) keep all pieces on so the top seed has to do the winning; (3) deny the bishop-pair trade — he wins long endgames.

**Avoid.** Najdorf theory war vs a match-sharp 2515; any opening gamble (his opening ACPL is 7.6); any clock race (his blitz 2453 > rapid 2381).

**Time budget (post-R4 double evening).** Short reset over deep re-study; opening locked from last night.

**Win condition.** Survival → grind the top seed even-or-better; the realistic underdog result is built late.

## Round 6 — ● Black vs GM Shyaam, Nikhil P (2435)

*Thu Jun 25, 16:00, Board 2. Source: second improved seed report (101 games) + DB. Single-game day.*

**Opponent snapshot.** `(C)` Active 2435 GM, broad (**79 openings**), 64.9% overall, stronger as White (71.4%). Phase profile opening 9.9 / middlegame 13.2 / **endgame 17.0** (his least accurate). As White he is flexible — `1.e4` ×23, `1.Nf3` ×14, plus g3/d4/b3/c4. He scores well in his Reti/Catalan and flank systems, so the aim against a strong, flexible GM is a sound structure that reaches his weaker endgame. `(C)`

**Shyaam's first move (49 White games).** `(C)`

| Shyaam plays | Games | Cabe's answer |
|---|---|---|
| `1.e4` | 23 | `1...c5` — Najdorf (Cabe's main Sicilian) |
| `1.Nf3` | 14 | `1...d5` → `...e6`, decline |
| `1.d4 / g3 / c4` | 11 | `1...d5` QGD / Catalan-decline |
| `1.b3` | 3 | `1...d5` solid central |

**Why.** `(I)` Cabe meets `1.e4` with his Najdorf and the flank systems with a solid `...d5`; against a strong, flexible GM the goal is a sound structure with `...dxc4` imbalance that steers toward his weaker endgame (17.0).

### Ranked response ladder

**1 — vs `1.e4`: Najdorf, but solid.** Be ready for his anti-Sicilian mix; don't invite his sharpest prep (Cabe's Najdorf has leaked in Keres/Opocensky lines):

| If Shyaam plays | Branch | Reference line |
|---|---|---|
| `2.Nf3 d6 3.d4` | Najdorf | `1.e4 c5 2.Nf3 d6 3.d4 cxd4 4.Nxd4 Nf6 5.Nc3 a6` |
| `2.Nf3 + 3.Bb5+` | Moscow (solid) | `1.e4 c5 2.Nf3 d6 3.Bb5+ Nd7 4.O-O Ngf6 5.Re1` |

**Critical position (Najdorf reference line, White to move 6):** `rnbqkb1r/1p2pppp/p2p1n2/8/3NP3/2N5/PPP2PPP/R1BQKB1R w KQkq - 0 6`. *Shyaam-specific:* read his choice at the board (English Attack vs Bc4 vs `Be2`). If `Be3 + f3 + Qd2` → `...e5 6.Nb3 Be6` (English-Attack-with-`...e5`); if Cabe's documented Keres/Opocensky leaks loom, **switch to the Moscow** rather than walk into prep. Plans/breaks: **Systems Library — Najdorf**.

**2 — vs `1.Nf3 / g3 / c4 / d4`: one `...d5` system.** `1.Nf3 d5 2.c4 e6 3.g3 Nf6 4.Bg2 Be7 5.O-O O-O 6.d4 dxc4`.

**3 — vs `1.b3`: solid central.** `1.b3 d5 2.Bb2 Nf6 3.e3 e6 4.Nf3 Be7`.

**Lines to avoid.** `(C)` Walking the Najdorf into a 2435's sharpest Keres / English-attack prep (Cabe's documented vulnerability); handing him a clean Reti/Catalan squeeze if he opens `1.Nf3` — unbalance with `...dxc4`.

### Game notes

- **Expected middlegame:** a Najdorf or Open-Catalan with pieces on, steered toward his weaker endgame (17.0). `(C)`
- **Phase objective:** pose problems and make a strong GM solve them; do not gift sharp prep. `(C)`
- **Clock policy:** single-game day — invest fully. `(I)`
- **Model games to study:** Shyaam's Black Najdorf losses for the structures (Siva Kumar, Sathvik 2026); for Cabe's own caution, his Najdorf losses (Gukesh Opocensky; Keres Attack). `(C)`

**Match-day checklist:**

- ☐ Najdorf main + a solid anti-Sicilian fallback
- ☐ `...d5` vs `1.Nf3/c4/g3`
- ☐ `...dxc4` unbalance
- ☐ one drawing-defense hold (Gate 3)

### In-Game Card — R6 ● Black vs Shyaam (GM, 2435)

**Opening choice.** Najdorf with a solid Moscow fallback vs `1.e4`; one `...d5/...dxc4` system vs `1.Nf3/c4/g3/d4`; solid central vs `1.b3`.

**Three middlegame plans (Black).** (1) Najdorf `...e5` structure to defuse his English Attack; (2) `...c5` break in the Open Catalan; (3) keep pieces on toward his endgame (ACPL 17.0).

**Avoid.** Keres Attack and Najdorf Opocensky (Cabe's own documented leaks); clean Réti/Catalan squeeze — unbalance with `...dxc4`.

**Time budget (single-game day).** Invest fully — no recovery constraint.

**Win condition.** Make a strong, flexible GM solve problems in your structure, not his.

## Round 7 — ○ White vs IM Chan, Kim Yew (2360)

*Fri Jun 26, 10:00, Board 4. Source: fifth improved seed report (classical subset, 60 games) + DB. Double-round morning.*

**Opponent snapshot.** `(C)` Young active MAS IM, 56% overall, **classical play much cleaner than online** (classical overall ACPL 16.1, endgame 20.8, only 8 blunders / 60). As Black he is mixed vs `1.e4`: `1...c6` (Caro), `1...e5`, `1...c5`, `1...e6`. His standard 2360 is well above his rapid/blitz (2177/2187) — keep it long and classical. His classical loose moves cluster at **move 30–40**. `(C)`

**Chan's answer to `1.e4` (21 of 48 Black games met `1.e4`).** `(C)`

| Chan plays | Games | Cabe's weapon |
|---|---|---|
| `1...c6` | 8 | Mainline anti-Caro (non-Advance) |
| `1...e5` | 6 | Sound open game `2.Nf3` |
| `1...c5` | 5 | Low-theory anti-Sicilian |
| `1...e6` | 2 | Anti-French (Tarrasch / KIA) |

**Why.** `(I)` Chan spreads his defenses, so Cabe needs a clear answer to each — all of which he already plays. Keep the game **long and classical** (his error rate doubles at speed) and press the move-30–40 transition.

### Ranked response ladder

**1 — Recommended vs `1...c6` (Caro): a mainline line.** `1.e4 c6 2.d4 d5 3.Nc3 dxe4 4.Nxe4` — solid, reaches a clean middlegame.

**Critical position (anti-Caro mainline, Black to move 4):** `rnbqkbnr/pp2pppp/2p5/8/3PN3/8/PPP2PPP/R1BQKBNR b KQkq - 0 4`. *Chan-specific:* he'll go classical `4...Bf5 5.Ng3 Bg6 6.h4 h6 7.Nf3 Nd7 8.h5 Bh7 9.Bd3 Bxd3 10.Qxd3`. Accept the Caro endgame structure; the leverage is move 30–40, not the opening. Plans/breaks: **Systems Library — Anti-Caro mainline**.

**2 — vs `1...e5`: a sound open game.** `1.e4 e5 2.Nf3 Nc6 3.Bb5 a6 4.Ba4 Nf6 5.O-O` (Ruy) or `3.Bc4` (Italian).

**3 — vs `1...c5`: a low-theory anti-Sicilian.** `1.e4 c5 2.Nf3 e6 3.d3 Nc6 4.g3 d5 5.Nbd2 Nf6 6.Bg2 Be7` (KIA-style), or a sound Open Sicilian.

**4 — vs `1...e6`: anti-French.** Tarrasch `1.e4 e6 2.d4 d5 3.Nd2`, or the KIA.

**Lines to avoid.** `(C)` A speed shuffle (his online error rate doubles; his classical endgame is clean at 20.8); an easy symmetric draw — keep pieces on to move 30–40.

### Game notes

- **Expected middlegame:** a sound `1.e4` structure kept complex into the first time control, where his classical loose moves cluster (move 30–40). `(C)`
- **Phase objective:** a pressure-late plan, not an early grind; make him solve problems with the clock running. `(C)`
- **Clock policy:** double-round morning — review only; keep it long and classical, not a speed shuffle. `(C)`
- **Model games to study:** Chan's classical late slips (Heberla, KID-fianchetto collapse; Hulka, passive rook); his Black loss vs Cruz Estrada (Sant Boi 2025). `(C)`

**Match-day checklist (double-round morning):**

- ☐ mainline anti-Caro vs `1...c6`
- ☐ open game vs `1...e5`
- ☐ low-theory anti-Sicilian vs `1...c5`
- ☐ anti-French ready
- ☐ R8 (Ang, Black) locked the night before

### In-Game Card — R7 ○ White vs Chan (IM, 2360)

**Opening choice.** Mainline anti-Caro `2.d4 d5 3.Nc3 dxe4 4.Nxe4`; sound open game vs `1...e5`; low-theory KIA-style vs `1...c5`; Tarrasch/KIA vs `1...e6`.

**Three middlegame plans (White).** (1) accept the Caro mainline endgame — his classical endgame ACPL is 20.8 (clean), so the leverage is the move-30–40 transition; (2) keep pieces on; (3) make him spend clock — his rapid/blitz is 2177/2187 vs classical 2360.

**Avoid.** Speed shuffle (his online error rate doubles — that is not the leverage); easy symmetric draw.

**Time budget (post-double morning).** Review only; long classical game.

**Win condition.** Complex middlegame into the first time control; his loose moves cluster move 30–40.

## Round 8 — ● Black vs FM Ang, Ern Jie Anderson (2309)

*Fri Jun 26, 16:00, Board 3. Source: eighth improved seed report (classical subset, 79 games) + DB. Double-round evening; underrated 15-year-old — treat 2309 as a floor.*

**Opponent snapshot.** `(C)` A fast-improving **15-year-old (FM 2025)** — the field's highest upset risk per rating point; **treat 2309 as a floor.** As White he is a **g3-based 1.d4 / 1.Nf3 player** (`1.d4` ×37, `1.Nf3` ×13) with a pet **King's Indian Defence Fianchetto (Uhlmann-Szabo E62, 3-0-0, 100%)** and a strong Fianchetto-KID/Grünfeld family (75%, ACPL 14.4). His opening is his cleanest phase (8.2); his endgame is softest (22.3); his blitz (1993) is ~300 below classical. `(C)`

**Ang's first move (51 White games).** `(C)`

| Ang plays | Games | Cabe's answer |
|---|---|---|
| `1.d4` | 37 | `1...d5` QGD / Slav (avoid his fianchetto-KID) |
| `1.Nf3` | 13 | `1...d5` → `...e6`, decline |
| `1.e4` | 1 | `1...c5` Najdorf (rare) |

**Why `...d5`, not `...g6`.** `(C)` Ang's comfort and best structure is the **fianchetto-KID / Grünfeld** where he is 75% and his pet E62 is 100% — so Cabe must **not** volunteer a KID / `...g6`. A `...d5` QGD/Slav keeps him out of his pet structures and asks a well-booked junior fresh questions.

### Ranked response ladder

**1 — Recommended: `...d5` QGD / Slav, deny the fianchetto-KID.**

| If Ang plays | Branch | Reference line |
|---|---|---|
| `1.d4 d5 2.c4 e6` | QGD | `1.d4 d5 2.c4 e6 3.Nc3 Nf6 4.Nf3 Be7 5.Bg5 O-O` |
| `1.d4 d5 2.c4 c6` | Slav | `1.d4 d5 2.c4 c6 3.Nf3 Nf6 4.Nc3 dxc4 5.a4 Bf5` |
| `1.Nf3` | Catalan-decline | `1.Nf3 d5 2.c4 e6 3.g3 Nf6 4.Bg2 Be7 5.O-O O-O 6.d4 dxc4` |

**Critical position (Slav reference line, White to move 6):** `rn1qkb1r/pp2pppp/2p2n2/5b2/P1pP4/2N2N2/1P2PPPP/R1BQKB1R w KQkq - 1 6`. *Ang-specific:* expect `6.Ne5 e6 7.Nxc4 Bb4` Krause variation — sound and solid; the leverage is the move-30+ phase, not theory. **No `...g6`** (his pet is KID-Fianchetto E62 100%). Plans/breaks: **Systems Library — QGD / Slav** (Anti-Catalan branch covers `1.Nf3` transposition).

**2 — vs rare `1.e4`: Najdorf.** `1.e4 c5 2.Nf3 d6 3.d4 cxd4 4.Nxd4 Nf6 5.Nc3 a6`.

**Lines to avoid.** `(C)` His pet KID-Fianchetto (E62, 100%) and the fianchetto-KID/Grünfeld family (75%) — **no `...g6` systems**; pose problems with `...d5/...dxc4` and make a junior calculate.

### Game notes

- **Expected middlegame:** a QGD/Slav/Open-Catalan with the `...dxc4` imbalance; keep it complex into move 30+, where his endgame (22.3) is softest. `(C)`
- **Phase objective:** win by position type and clock — his opening is clean (8.2), but his blitz (1993) says he cracks when rushed in unfamiliar structures. `(C)`/`(R)`
- **Clock policy:** double-round evening — short reset; pose problems early to eat his clock. `(C)`/`(R)`
- **Underrated caveat:** prep him like a stronger player; 2309 is a floor. `(C)`
- **Model games to study:** Romanov–Ang (Catalan Closed, how a strong player beats his main structure); Vidyarthi–Ang (KIA collapse, move-30+). `(C)`

**Match-day checklist (double-round evening):**

- ☐ `...d5` QGD/Slav, no `...g6`
- ☐ `...dxc4` unbalance
- ☐ Najdorf for rare `1.e4`
- ☐ recovery after R7

### In-Game Card — R8 ● Black vs Ang (FM, 2309, junior)

**Opening choice.** `...d5` QGD/Slav vs `1.d4/1.Nf3`. **No `...g6` systems** — his KID-Fianchetto is 100%.

**Three middlegame plans (Black).** (1) `...dxc4` imbalance; (2) hold the c4-pawn with `...a6 + ...b5 + ...Bb7`; (3) keep position live to move 30+ where his endgame (ACPL 22.3) softens.

**Avoid.** Any `...g6` (KID-Fianchetto / Grünfeld family — his pet); early simplification.

**Time budget (post-R7 double evening).** Short reset; opening locked from last night; pose problems early to eat his clock.

**Win condition.** Unfamiliar structure + clock pressure. Prep him like a 2400+.

## Round 9 — ○ White vs IM Susilodinata, Andrean (2360)

*Sat Jun 27, 16:00, Board 3. Final round. Source: sixth improved seed report (classical subset, 100 games) + DB.*

**Opponent snapshot.** `(C)` An **active, experienced grinder** (b. 1990, IM 2024): solid and **draw-heavy** — classical 58.5%, only **25 blunders / 100**, opening cleanest (10.2), **endgame softest (26.4)**. As Black he is a **Caro-Kann player** vs `1.e4` (`1...c6` ×18), with the **Advance Caro-Kann Tal as his rock-solid pet (75%, ACPL 15.0)**. His **Slav Modern Line is a soft 25%**, and his other Caro lines have leaked recently. `(C)`

**Susilodinata's answer to `1.e4` (23 of 50 Black games met `1.e4`).** `(C)`

| Susilodinata plays | Games | Cabe's weapon |
|---|---|---|
| `1...c6` | 18 | Anti-Caro — **not** the Advance (sidestep his Tal pet) |
| `1...c5` | 4 | Low-theory anti-Sicilian |
| `1...e6` | 1 | Anti-French |

**Why sidestep the Advance.** `(C)` His pet is the **Advance Caro-Kann Tal**, which he holds at 75% (ACPL 15.0) — do **not** enter the Advance hoping for a leak. A mainline/Exchange anti-Caro denies him his prepared structure and keeps the game in Cabe's hands.

### Ranked response ladder

**1 — Recommended vs `1...c6`: a non-Advance anti-Caro.** Sidestep his Advance Tal pet:

| If Susilodinata plays | Branch | Reference line |
|---|---|---|
| pin with `...Bg4` | Two Knights | `1.e4 c6 2.Nc3 d5 3.Nf3 Bg4 4.h3 Bxf3 5.Qxf3 Nf6` |
| simplify | Exchange | `1.e4 c6 2.d4 d5 3.exd5 cxd5 4.Bd3 Nc6 5.c3` |

**Critical position (Two Knights anti-Caro, White to move 6):** `rn1qkb1r/pp2pppp/2p2n2/3p4/4P3/2N2Q1P/PPPP1PP1/R1B1KB1R w KQkq - 1 6`. *Susilodinata-specific:* his Advance-Tal pet is 75% — the whole point of the Two Knights is to **sidestep** that comfort zone. Plan `Bd3 + Bg5 + O-O-O + g4–g5`. Plans/breaks: **Systems Library — Two Knights anti-Caro**.

**2 — vs `1...c5`: a low-theory anti-Sicilian.** `1.e4 c5 2.Nf3 e6 3.d3 Nc6 4.g3 d5 5.Nbd2 Nf6 6.Bg2 Be7`, or a sound Open Sicilian.

**3 — vs `1...e6`: anti-French.** Tarrasch `1.e4 e6 2.d4 d5 3.Nd2`.

**Lines to avoid.** `(C)` The Advance Caro (his comfort zone, 75%); a long symmetric grind against a 31-draws-in-100 grinder unless Cabe's own technique is sharp.

### Game notes

- **Expected middlegame:** a mainline/Exchange Caro structure with pieces on; keep pressure into move 30+, where his 2024 results cracked and his endgame (26.4) is softest. `(C)`
- **Phase objective:** it's the final round — out-press a draw-heavy grinder late, but only if Cabe's own conversion is sharp (no engine profile — train it). `(C)`/`(I)`
- **Clock policy:** final round — rested head, no new theory; build slow pressure. `(I)`
- **Model games to study:** Susilodinata's Black losses — Slav Modern vs Chatalbashev (2023); Caro Tartakower vs Mohammad Fahad (2024); late slip vs Tin Jingyao (2025). `(C)`

**Match-day checklist (final round):**

- ☐ non-Advance anti-Caro vs `1...c6`
- ☐ low-theory anti-Sicilian vs `1...c5`
- ☐ anti-French
- ☐ own conversion technique sharp

### In-Game Card — R9 ○ White vs Susilodinata (IM, 2360)

**Opening choice.** Non-Advance anti-Caro (Two Knights or Exchange) — sidestep his Advance-Tal pet. Low-theory anti-Sicilian vs `1...c5`. Tarrasch vs `1...e6`.

**Three middlegame plans (White).** (1) Exchange Caro `4.Bd3 + 5.c3 + Bf4` IQP / minority-attack structure; (2) Two Knights `Qf3 + Bg5` long castling; (3) keep pressure into move 30+ where his endgame (ACPL 26.4) and 2024 results cracked.

**Avoid.** The Advance Caro (his comfort zone, 75% / ACPL 15.0); long symmetric grind unless Cabe's own conversion is sharp.

**Time budget (final round).** Rested head, no new theory; build slow pressure.

**Win condition.** Out-press a draw-heavy grinder late. **Mirror caution:** Cabe has no engine profile — train conversion.

## Appendix — Evidence & Verification Notes

- **Sources.** Schedule, colors, boards, and ratings from `manual_sections/Tournament_Schedule.md`. The Round 1 and Round 2 results and moves come from the official PGN files `2nd_DAV_Go_Day1.pgn` and `2nd_DAV_Go_Day2.pgn`. Opponent reads from the eight `*_seed_report_improved.md` files (Stockfish 18, depth 12) and `manual_sections/Opponent_*.md`. Cabe's own repertoire and record from his dossier (`manual_sections/Opponent_FM_Arlan_Cabe.md`, 81 OTB games) and first-move queries against `prep_manual.db`.
- **Evidence asymmetry.** Opponent engine claims are `(C)` classical depth-12. **Cabe's own profile is result-based only — his dossier has no engine fingerprint** — so Cabe-side claims are repertoire/result evidence, not ACPL, and are labelled accordingly.
- **Seed-report mapping (by seeding, not round).** Vignesh = 1st · Shyaam = 2nd · Morris = 3rd · Tan = 4th · Chan = 5th · Susilodinata = 6th · Thejkumar = 7th · Ang = 8th. R3 (Dino) deliberately has no card — the integrity gate.
- **Evidence discipline.** `(C)` classical, `(R)` rapid/online tendency only, `(I)` inference. Rapid evidence never overrides classical results.
- **Move legality.** Every line above was replayed through the workspace SAN validator (`fens_for` / `MiniBoard`, `prep_manual_app.py`); all sequences are legal from the start position.
- **Integrity gate.** Cabe and Dino share a coach; neither player's playbook prepares deeply against the other (R3). This document uses only public-record context for that pairing.
- **Scope.** This playbook is a new standalone deliverable; it does not alter the manual, the database, the Dino playbook, or any application code.
