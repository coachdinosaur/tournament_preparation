# Dino Ballecer — Round-by-Round Game Preparation (Rounds 4–9)

Standalone operational playbook for **FM Dino Ballecer (2372, PHI)** covering Rounds 4–9, **24–27 June 2026** (times Asia/Manila, UTC+8). It gives deep round-by-round preparation for Rounds 4–9. This document is separate from the Tournament Preparation Manual and does not modify it.

Recommendations are curated from the **improved seed reports** (Stockfish 18, depth 12) and the opponent dossiers. Where a seed report demoted a target, that decision is honored here. Move lines were replayed for legality with the workspace SAN validator before this file was rendered.

**Evidence labels** — `(C)` classical engine/result evidence · `(R)` rapid/online, tendency only · `(I)` inference from repertoire fit. **Color** — `● Black` (graphite) · `○ White` (slate). Updated through Round 1, Dino's overall form is White **95.6%**, Black **72.6%** — the Black repertoire remains the priority for this event. `(C)`

## Tournament Dashboard

Legend: `●` = Dino has Black (graphite) · `○` = Dino has White (slate). "Intention" is the planned opening; "priority" is the one thing to get right.

**Live status — after Round 2 (23 June 2026): 0.5/2.** Dino drew IM James Morris with Black in 46 moves, and lost to IM Tan Jun Ying with Black in 34 moves. Round 3 is **Tuesday, 23 June at 16:00** against FM Arlan Cabe with White.

| Round / Date | Time · Bd | Color | Opponent | Rtg | Opening intention & prep priority |
|---|---|---|---|---|---|
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

## Systems Library — Plans & Pawn Breaks

Single-source reference for the recurring systems used below. Each block covers piece routes, the pawn break that defines the plan, exchange policy, one tactical motif, and one engine-style cue. Round cards cross-link here so the same system is documented once.

### Taimanov (Black, `1.e4 c5 2.Nf3 e6 3.d4 cxd4 4.Nxd4 Nc6 5.Nc3 Qc7 6.Be3 a6`) — used R1, R4, R8

- **Piece routes.** `Nge7` is the modern flavour (dodges `Nb3 + e5`); `Bd6` vs `Bd3`, `Be7` vs `f3`-setups; queen stays on c7; rook to c8 once `...b5` lands.
- **Defining breaks.** `...b5` always; `...b5–b4` to displace `Nc3`; `...d5` only after `...a6 + ...b5 + ...Bb7 + ...Rc8` are in place (premature drops a tempo to `exd5`).
- **Exchange policy.** Trade knights on d4 only when White recaptures with the e-pawn (good for Black) — never with the b-pawn (good for White). Keep queens to press the endgame.
- **Tactical motif.** `...Nxe4` shots when `Nc3` is overloaded after `...b5–b4`; `...Bc5` pins along the a7–g1 diagonal vs `Be3`.
- **Engine-style cue.** Vs English Attack (`Be3 + f3 + Qd2 + O-O-O`), counter-castle queenside with `...b5–b4 + ...a5–a4`; do **not** race on the kingside.

### Anti-Catalan / anti-Réti with `...dxc4` (Black, `1.Nf3 Nf6 2.c4 e6 3.g3 d5 4.Bg2 Be7 5.O-O O-O 6.d4 dxc4`) — used R2, R4, R6

- **Piece routes.** `...a6 + ...b5 + ...Bb7` to hold the c4-pawn while developing; `...Nbd7 + ...Rc8`; `...Bf6` is the principal regrouping vs `Ne5`.
- **Defining breaks.** `...c5` (the main equalizer — frees the bishop, opens the c-file); `...b5–b4` if White goes `Nbd2`.
- **Exchange policy.** Do **not** trade the light-squared bishop voluntarily — it is the piece the Catalan was built to neutralise. Trade dark-square bishops on `Bg5` if offered.
- **Tactical motif.** `...Nb6 + ...Bxg2 + ...Nbd5` to overload White's recovery of c4; `...c5 + ...cxd4 + ...Nb4` queenside swing.
- **Engine-style cue.** If White abandons c4 recovery for a kingside attack (`Ne5 + h4`), simplify with `...Nfd7 + ...Bf6` — White's compensation needs the bishop pair to mean anything.

### Moscow `Bb5+` (White, `1.e4 c5 2.Nf3 d6 3.Bb5+ Nd7 4.O-O Ngf6 5.Re1 a6 6.Bf1`) — used R5

- **Piece routes.** `c3 + d4` slow centre; `Nbd2 → f1 → g3` Spanish-style reroute; `Bf1 → c2` only after `c3`.
- **Defining break.** `d4` only after `c3` and `Re1` are in place; `e5` push if Black plays `...b5` without `...e6`.
- **Exchange policy.** Avoid the early bishop trade — `Bf1` retreat preserves the long-term Spanish bishop. Trade knights on `d4` once Black is committed.
- **Tactical motif.** Sacrificial `Nd5` against `...e6/...b5/...Bb7` set-ups; `e5–e6` wedge if Black delays `...e6`.
- **Engine-style cue.** If Black goes `...g6` for a Dragon-flavour, switch to a `c4 + Nc3` Maróczy bind — do **not** revert to Open Sicilian.

### Rossolimo fianchetto (White, `1.e4 c5 2.Nf3 Nc6 3.Bb5 g6 4.Bxc6 dxc6 5.d3 Bg7 6.h3`) — used R5, R7

- **Piece routes.** `Nbd2 → c4` (or `→ f1 → e3`); queen to `e1` or `d2`; rook-lift `Re3 → g3` is a known kingside try.
- **Defining break.** `e5` after `Nf3 → h2 + f4`; alternative `c3 + d4` if Black delays `...e5`.
- **Exchange policy.** Bishop-pair is already gone — fight for the dark squares with `Be3 + Qd2`. Exchange-sac for two minors if Black's queenside is loose.
- **Tactical motif.** `e5` thrust opens the `d3–h7` diagonal once `Nh2` is in; `Bxa7` shots in lines with a slow `...b6`.
- **Engine-style cue.** Black's structure is bishop-pair vs nothing-special; **time matters more than material** — if you keep him cramped to move 30, the doubled c-pawns become the story.

### Two Knights anti-Caro (White, `1.e4 c6 2.Nc3 d5 3.Nf3 Bg4 4.h3 Bxf3 5.Qxf3 Nf6`) — used R9

- **Piece routes.** Queen `f3 → g3`; `d3 + Bg5`; long castling is the principled try.
- **Defining break.** `e5` (kicking the f6-knight) when Black commits `...e6` without `...Nbd7`; `g4 → g5` wedge after `O-O-O`.
- **Exchange policy.** Accept the bishop trade (`Bxf3`) gratefully — two-bishops vs one-knight balance is fine while the pawn structure stays flexible.
- **Tactical motif.** `Bxf6 + Nxd5` exchange sac if Black recaptures with the queen; `Nd5` jumps when `...e6` weakens dark squares.
- **Engine-style cue.** Be ready to meet `...c5` with `d4` (not `cxd4` — Black gets a hanging-pawn structure that suits him).

## Round 4 — ● Black vs GM Vignesh, N R (2515)

*Wed Jun 24, 10:00, Board 2. Source: first improved seed report (187 games; 99 classical) + DB. Top seed, currently match-sharp.*

**Opponent snapshot.** `(C)` The **strongest player in the pool and currently match-sharp** (7/9 at Sevilla 2026, plus 6/7 in the side blitz). In the classical subset that drives prep he is **49W 40D 10L (69.7%)**, with a broad repertoire (**128 distinct openings**). His **opening is his cleanest phase (ACPL 7.6** over 99 classical games) — so there is no trap to set and no gamble to risk. His endgame is his least-accurate phase but still strong (**ACPL 17.6**). **No clock edge to chase:** his blitz (2453) is *higher* than his rapid (2381) — he is lethal in time scrambles. The only evidence-backed pressure points are structural and conditional (his Black-side **Catalan/Réti** at 40.0% and a tiny high-ACPL **IQP/Panov** sample), both needing real prep, not a cheap trick. `(C)`

**Vignesh's first move (51 White games).** `(C)`

| Vignesh plays | Games | Dino's answer |
|---|---|---|
| `1.e4` | 21 | `1...c5` — Taimanov/Kan via `2...e6` (ladder below) |
| `1.d4` | 16 | `1...Nf6` heading for `...e6/...d5` (Catalan/QGD) |
| `1.Nf3` | 8 | `1...Nf6` → `...e6/...d5`, transposing |
| `1.c4` | 6 | `1...e6` → `...d5` central claim |

**Why one Black structure covers everything.** `(I)` Meeting `1.e4` with `2...e6` (Taimanov/Kan) and meeting `1.d4/1.Nf3/1.c4` with `...Nf6/...e6/...d5` collapses his whole move-order menu into two well-understood structures — the same two Dino prepares for R1 and R2 — so the top seed gets no fresh decision to exploit.

### Ranked response ladder

**1 — Recommended vs `1.e4`: narrow Taimanov/Kan (`2...e6`).** Low-theory, sidesteps every Bb5 system and the Dragon:

| If Vignesh plays | Branch | Reference line |
|---|---|---|
| `2.Nf3` then `3.d4` | Open Sicilian (Taimanov) | `1.e4 c5 2.Nf3 e6 3.d4 cxd4 4.Nxd4 Nc6 5.Nc3 Qc7 6.Be3 a6` |
| `2.Nf3` then `3.d4` | Open Sicilian (Kan) | `1.e4 c5 2.Nf3 e6 3.d4 cxd4 4.Nxd4 a6 5.Nc3 Qc7 6.Bd3 Nf6` |
| `2.c3` | Alapin | `1.e4 c5 2.c3 d5 3.exd5 Qxd5 4.d4 Nf6 5.Nf3 e6` |

**Critical position (Taimanov, White to move 7):** `r1b1kbnr/1pqp1ppp/p1n1p3/8/3NP3/2N1B3/PPP2PPP/R2QKB1R w KQkq - 0 7`. *Vignesh-specific:* he is broad enough to choose anything — be ready for `Bd3`, `Be2`, and `f3` setups equally. **No gamble** from this position; equality is the result. Plans/breaks: **Systems Library — Taimanov**.

**2 — Recommended vs `1.d4 / 1.Nf3 / 1.c4`: one `...Nf6/...e6/...d5` system with `...dxc4`.** The same R2 Catalan/QGD setup; `...dxc4` keeps it unbalanced rather than a dry equal game:

| If Vignesh plays | Reference line |
|---|---|
| `1.d4` | `1.d4 Nf6 2.c4 e6 3.Nf3 d5 4.g3 Be7 5.Bg2 O-O 6.O-O dxc4` |
| `1.Nf3` | `1.Nf3 Nf6 2.c4 e6 3.g3 d5 4.Bg2 Be7 5.O-O O-O 6.d4 dxc4` |
| `1.c4` | `1.c4 e6 2.Nc3 d5 3.d4 Nf6 4.Nf3 Be7` |

**Critical position (after `1.d4` anti-Catalan reference line, White to move 7):** `rnbq1rk1/ppp1bppp/4pn2/8/2pP4/5NP1/PP2PPBP/RNBQ1RK1 w - - 0 7` (transposes from `1.Nf3` and `1.c4`). *Vignesh-specific:* expect `Qc2 + a4`; the `...dxc4` imbalance keeps the position alive. Plans/breaks: **Systems Library — Anti-Catalan with `...dxc4`**.

**3 — Dragon: forbidden (Gate 1).** The seed report names Dino's exact 3-loss sequence and warns explicitly against walking a leaky Dragon into an in-form GM's preparation. Do not play it.

**4 — Demoted target — do not chase.** `(C)` Do **not** revive the Advance Caro-Kann "Tal" line as a Vignesh weakness: the 0/2 evidence is Lichess-blitz metadata, while his **classical** Advance Caro is **2/2, ACPL 7.9, zero serious errors**. The seed report demoted it; it stays demoted here.

### Game notes

- **Expected middlegame:** an Open-Catalan / hanging-pawns or IQP structure with active pieces (the `...dxc4` lines), or a sound Taimanov. Equalize cleanly and make the top seed win a balanced position over the board. `(C)`
- **Phase objective:** survive the opening dead-even (his opening ACPL 7.6 means no gambles pay), deny him a risk-free squeeze, and reach a rook ending only with Gate-3 technique in hand (his endgame ACPL 17.6 is loosest-but-search). `(C)`
- **Clock policy:** **no clock race.** Blitz 2453 > rapid 2381 — he is dangerous in scrambles; play on preparation and known plans, not the clock. `(R)`/`(C)`
- **Lines to avoid:** opening gambles; the demoted Advance-Caro "Tal" target; and any assumption that the Moscow is automatically good (he is 3-1-0 vs the Moscow as Black — a prepared improvement is needed, not the label). `(C)`
- **Model games to study:** Vignesh's classical losses and endgame samples — Aaditya Dhingra 2026, Goh Zi Han 2026, Shahil Dey 2026, Anand Batsukh 2025, Sukovic 2025. Do **not** use the Lichess "recent losses" as classical models. `(C)`

**Match-day checklist (double-round morning — review, don't re-learn):**

- ☐ Taimanov/Kan vs `1.e4` locked
- ☐ `...e6/...d5` + `...dxc4` vs `1.d4/Nf3/c4`
- ☐ Dragon explicitly off
- ☐ no clock race
- ☐ one active-rook / drawing-defense hold rehearsed (Gate 3)
- ☐ R5 (Shyaam, White) choice locked the night before

### In-Game Card — R4 ● Black vs Vignesh (GM, 2515, top seed)

**Opening choice.** Narrow Taimanov via `2...e6` vs `1.e4`; one `...Nf6/...e6/...d5` system with `...dxc4` vs `1.d4/1.Nf3/1.c4`.

**Three middlegame plans (Black).** (1) accept equality cleanly — his opening ACPL is 7.6, no gamble pays; (2) `...c5` to free the structure; (3) keep queens on early — his blitz (2453) beats his rapid (2381), so scrambles favour him.

**Avoid.** Dragon (Gate 1); the demoted Advance-Caro "Tal" target; any clock race; an automatic Moscow without a prepared improvement.

**Time budget.** Be ready to invest 25–30m on the opening if he plays an unfamiliar sideline — equality out of his prep is fine.

**Win condition.** A balanced position where the top seed has to do all the winning over the board.

## Round 5 — ○ White vs GM Shyaam, Nikhil P (2435)

*Wed Jun 24, 16:00, Board 4. Source: second improved seed report (101 OTB games) + DB.*

**Opponent snapshot.** `(C)` Active 2435 GM with a broad, flexible repertoire (**79 openings**), **44W 43D 14L (64.9%)** on file. He is stronger with White (**71.4%**) than Black (**58.7%**), so Dino's best chances come in *this* White game. Across 101 analysed games his phase profile is opening **9.9** / middlegame **13.2** / **endgame 17.0** (his least accurate). The key tension: his Sicilian/anti-Sicilian defense scores **well by result** (Anti-Sicilian Counter-Package as Black 80%) yet shows the **highest engine-error density in the file** (ACPL 16.3, 5 serious errors / 174 moves) — pressure points exist, but he is not handing over blunders. `(C)`

**Shyaam's answer to `1.e4` (27 of 52 Black games met `1.e4`).** `(C)`

| Shyaam plays | Games | Dino's weapon |
|---|---|---|
| `1...c5` | 19 | Moscow (vs `...d6`) / Rossolimo (vs `...Nc6`) |
| `1...e5` | 7 | Center Game `2.d4` |
| `1...e6` | 1 | King's Indian Attack |

**Why the Bb5 universe.** `(I)` Keeping him in Moscow/Rossolimo structures denies him a main-line Najdorf and steers into exactly the family where his engine accuracy is most stressed — but because his *results* there are good, Dino must bring a concrete middlegame idea, not just a familiar label. `(C)`

### Ranked response ladder

**1 — Recommended vs `1...c5`: Moscow / Rossolimo.** Stay in Dino's confirmed anti-Sicilian domain (Moscow Main Line 9/9, Moscow 5/5, Rossolimo 2/2):

| If Shyaam plays | Branch | Reference line |
|---|---|---|
| `2...d6` | Moscow | `1.e4 c5 2.Nf3 d6 3.Bb5+ Nd7 4.O-O Ngf6 5.Re1 a6 6.Bf1` |
| `2...Nc6` | Rossolimo | `1.e4 c5 2.Nf3 Nc6 3.Bb5 e6 4.O-O Nge7` |
| `2...g6` | Rossolimo (fianchetto) | `1.e4 c5 2.Nf3 Nc6 3.Bb5 g6 4.Bxc6 dxc6 5.d3 Bg7 6.h3` |

**Critical position (Moscow reference line, Black to move 6):** `r1bqkb1r/1p1npppp/p2p1n2/2p5/4P3/5N2/PPPP1PPP/RNBQRBK1 b kq - 1 6`. *Shyaam-specific:* he's likeliest to play `...b6 + ...Bb7` Najdorf-flavour — answer with `c3 + d4` slow centre, **not** `d4` immediately. Bring **one** prepared improvement here, not just the label. Plans/breaks: **Systems Library — Moscow** (also see Rossolimo fianchetto for the `...g6` branch).

**2 — Recommended vs `1...e5`: Center Game.** Dodges his entire `...e5` book and lands a structure Dino owns (3/3): `1.e4 e5 2.d4 exd4 3.Qxd4 Nc6 4.Qe3`.

**3 — vs `1...e6` (French): King's Indian Attack.** Dino's proven weapon (91.7%/6): `1.e4 e6 2.d3 d5 3.Nd2 Nf6 4.Ngf3 c5 5.g3`.

**4 — Najdorf target: narrow and drilled only.** `(C)` His Najdorf as Black is a soft **37.5%/4** with recent 2026 losses, but switching Dino into a broad Open Sicilian for one opponent is a bad trade. Use Moscow/Rossolimo to deny his Najdorf; only prepare one concrete Najdorf sideline if Dino will actually drill it.

### Game notes

- **Expected middlegame:** an anti-Sicilian middlegame where a strong GM must solve problems in Dino's home structures; keep pieces on toward his weaker endgame (ACPL 17.0) rather than assuming the opening decides it. `(C)`
- **Phase objective:** out-prepare him in familiar territory and make him work; his KIA-Symmetrical-as-Black (25%, 2 games) and the engine-stressed anti-Sicilian are the soft spots — bring ideas, not just move orders. `(C)`
- **Clock policy:** standard pacing; this is the **double-round evening** after R4, so favour a short physical reset over deep re-study (Gate 4). `(I)`
- **Lines to avoid:** a broad Open Sicilian / main-line Najdorf workload, and an autopilot Moscow without a prepared improvement (his results in the Bb5 family are good). `(C)`
- **Model games to study:** Shyaam's recent Black losses vs Siva Kumar (Najdorf, 2026.05.19), Sathvik (Najdorf, 2026.04.16), Balakrishnan (Najdorf, 2026.01.16), and Weerasekara (Nimzo, 2026.05.21); plus his §5 endgame samples (Shen Ree Herng, Nagare, Krishnan). `(C)`

**Match-day checklist:**

- ☐ Moscow vs `...d6`
- ☐ Rossolimo vs `...Nc6/...g6`
- ☐ Center Game vs `...e5`
- ☐ KIA vs French
- ☐ one concrete Moscow improvement (not just the label)
- ☐ recovery completed after R4

### In-Game Card — R5 ○ White vs Shyaam (GM, 2435)

**Opening choice.** Moscow vs `...d6`; Rossolimo vs `...Nc6/...g6`; Center Game vs `1...e5`; KIA vs `1...e6`. Bring **one** prepared Moscow improvement — not just the label.

**Three middlegame plans (White).** (1) `Bf1` retreat preserves the Spanish bishop; (2) `Nbd2 → f1 → g3` Spanish reroute aims at h5/f5; (3) press toward his endgame (ACPL 17.0).

**Avoid.** Open Sicilian / main-line Najdorf workload; autopilot Moscow without a prepared idea (he is 3-1-0 vs the Moscow as Black).

**Time budget (post-R4 double evening).** Physical reset over deep re-study; the opening is locked from last night.

**Win condition.** Anti-Sicilian middlegame solved on Dino's home turf, not his.

## Round 6 — ● Black vs IM Chan, Kim Yew (2360)

*Thu Jun 25, 16:00, Board 3. Source: fifth improved seed report (classical subset, 60 games) + DB. Single-game day.*

**Opponent snapshot.** `(C)` Young (b. 2002), active MAS IM with the **deepest file in the pool (134 games)**, **56.0%** overall — **63.8% White / 47.7% Black**. The single most important read: **separate his classical play from his online play.** Across all 99 analysed games his ACPL is 23.1 (endgame 29.9, 41 blunders), but **restricted to his 60 classical games he is much cleaner — overall ACPL 16.1, endgame 20.8, only 8 blunders.** His classical strength is a clean **Catalan/Réti squeeze as White (67.9%, ACPL 13.5)**; his soft spot is the **draw-heavy fianchetto-KID as White (41.7%, 0 wins in 6)**. His standard 2360 sits well above his rapid/blitz (2177/2187). `(C)`

**Chan's first move (51 White games).** `(C)`

| Chan plays | Games | Dino's answer |
|---|---|---|
| `1.d4` | 14 | `1...Nf6` → `...e6/...d5`, with `...dxc4` |
| `1.Nf3` | 13 | `1...Nf6` → `...e6/...d5`, transposing |
| `1.e4` | 12 | `1...c5` — Taimanov via `2...e6` |
| `1.c4` | 12 | `1...e6` → `...d5` |

**Why deny the squeeze, not chase a trap.** `(I)` Chan is genuinely strong and clean in his main Catalan/Réti universe, so there is no cheap White-side hole. The plan is a sound equalizer that **unbalances with `...dxc4`** and steers toward his draw-heavy fianchetto-KID structures, then a long classical game — never a speed shuffle, where his error rate roughly doubles. `(C)`

### Ranked response ladder

**1 — Recommended vs `1.d4 / 1.Nf3 / 1.c4`: anti-Catalan/Réti with `...dxc4`.** One `...Nf6/...e6/...d5` system that refuses the frictionless squeeze:

| If Chan plays | Reference line |
|---|---|
| `1.Nf3` | `1.Nf3 Nf6 2.c4 e6 3.g3 d5 4.Bg2 Be7 5.O-O O-O 6.d4 dxc4` |
| `1.d4` | `1.d4 Nf6 2.c4 e6 3.Nf3 d5 4.g3 Be7 5.Bg2 O-O 6.O-O dxc4` |
| `1.c4` | `1.c4 e6 2.Nc3 d5 3.d4 Nf6 4.Nf3 Be7` |

**Critical position (after `1.d4` anti-Catalan reference line, White to move 7):** `rnbq1rk1/ppp1bppp/4pn2/8/2pP4/5NP1/PP2PPBP/RNBQ1RK1 w - - 0 7`. *Chan-specific:* he is genuinely strong in the closed Catalan/Réti — the `...dxc4` imbalance is the whole point; deny him the symmetrical squeeze. Plans/breaks: **Systems Library — Anti-Catalan with `...dxc4`**.

**2 — vs `1.e4`: Taimanov (`2...e6`).** He plays `1.e4` about a quarter of the time; meet it with the same narrow Taimanov Dino prepares elsewhere: `1.e4 c5 2.Nf3 e6 3.d4 cxd4 4.Nxd4 Nc6 5.Nc3 Qc7 6.Be3 a6`.

**3 — Backup: hold and outlast.** `(C)` If he forces symmetry, take the clean equalizer and play the long game — he **draws far more than he wins** in his fianchetto structures (0 wins in 6), so a balanced middlegame already favours the upset.

**Lines to avoid.** `(C)` Handing him a clean closed Catalan squeeze; and turning the game into a speed shuffle — his **classical** endgame is clean (ACPL 20.8), so the dramatic raw endgame numbers are online noise, not a grinding target.

### Game notes

- **Expected middlegame:** an Open-Catalan / QGD with the `...dxc4` imbalance, steered toward his draw-heavy fianchetto-KID structures; press the **move 30–40 transition**, where his classical loose moves cluster. `(C)`
- **Phase objective:** a pressure-late plan, not an early-trade grind — keep enough pieces on to reach the first time control with winning chances. `(C)`
- **Clock policy:** keep it long and classical; pose real problems and make him spend clock, but plan to win a long game, not bank a speed blunder. `(C)`
- **Lines to avoid (own side):** don't volunteer a quiet symmetrical Slav that hands him the squeeze; this is a single-game day, so there is no recovery constraint — invest fully. `(I)`
- **Model games to study:** Chan's KID-fianchetto collapse vs Heberla (Rilton Cup, Jan 2026) and his Black loss vs Cruz Estrada (Sant Boi, Dec 2025, English Anglo-Indian); plus his §5 late-transition samples (Hulka, Hari Madhavan). `(C)`

**Match-day checklist (single-game day):**

- ☐ one anti-Réti/Catalan move-order
- ☐ `...dxc4` unbalancing idea
- ☐ Taimanov vs `1.e4`
- ☐ Dragon explicitly off
- ☐ one drawing-defense hold (Gate 3)

### In-Game Card — R6 ● Black vs Chan (IM, 2360)

**Opening choice.** Anti-Catalan/Réti with `...dxc4` vs `1.d4/1.Nf3/1.c4`; Taimanov vs `1.e4`. Single-game day → invest fully.

**Three middlegame plans (Black).** (1) `...c5` break; (2) `...Bb7 + ...Nbd7 + ...Rc8` holding the c4-pawn long enough; (3) press the **move 30–40** transition — his classical loose moves cluster there.

**Avoid.** Symmetric Slav that hands him the squeeze; a speed-shuffle (his classical endgame is clean at ACPL 20.8 — the dramatic raw numbers are online noise).

**Time budget.** Long classical game; don't simplify before move 25.

**Win condition.** Fianchetto-KID-flavoured structure where his record is 0 wins in 6.

## Round 7 — ○ White vs FM Ang, Ern Jie Anderson (2309)

*Fri Jun 26, 10:00, Board 3. Source: eighth improved seed report (classical subset, 79 games) + DB. Underrated 15-year-old — treat 2309 as a floor.*

**Opponent snapshot.** `(C)` The lowest-rated opponent but the **highest upset risk per rating point**: a **15-year-old (b. 2010) who made FM in 2025**, on a fast-improving curve, with an entirely fresh file (Nov 2023–Dec 2025). **Treat 2309 as a floor, not a level.** Crucially, **his weaker half is the one Dino faces with White**: in classical play he is 61.2% as White but only **44.9% as Black**, and Dino opens `1.e4`. His opening is his most accurate phase (ACPL 8.2) — so the edge is **position type and clock**, not theory: his **blitz (1993) trails his classical by ~300 points**, and his endgame (ACPL 22.3) is his softest phase, with late blunders clustering at move 30+. `(C)`

**Ang's answer to `1.e4` (23 of 49 Black games met `1.e4`).** `(C)`

| Ang plays | Games | Dino's weapon |
|---|---|---|
| `1...c5` | 10 | Rossolimo `3.Bb5` (sidesteps the Accelerated Dragon) |
| `1...e5` | 10 | Center Game `2.d4` (dodges the Ruy) |
| `1...e6` | 3 | King's Indian Attack |

**Why this denies his strengths.** `(I)` His best Black line is the **Accelerated Dragon / Maróczy (66.7%/5)**; the Rossolimo `3.Bb5` sidesteps it and steers into the **Anti-Sicilian Counter-Package, where he is 0/2 (ACPL 38.3) and Dino is 96%/25**. The Center Game dodges his whole Ruy Lopez book. Both pose a junior fresh problems that eat clock. `(C)`

### Ranked response ladder

**1 — Recommended vs `1...c5`: Rossolimo `3.Bb5`.** Denies the Accelerated Dragon and his Maróczy comfort zone:

| If Ang plays | Branch | Reference line |
|---|---|---|
| `2...Nc6` + `...g6` | Rossolimo (fianchetto) | `1.e4 c5 2.Nf3 Nc6 3.Bb5 g6 4.Bxc6 dxc6 5.d3 Bg7 6.h3` |
| `2...Nc6` + `...e6` | Rossolimo | `1.e4 c5 2.Nf3 Nc6 3.Bb5 e6 4.O-O Nge7` |
| `2...d6` | Moscow `Bb5+` | `1.e4 c5 2.Nf3 d6 3.Bb5+ Nd7 4.O-O Ngf6 5.Re1` |

**Critical position (Rossolimo fianchetto reference line, Black to move 6):** `r1bqk1nr/pp2ppbp/2p3p1/2p5/4P3/3P1N1P/PPP2PP1/RNBQK2R b KQkq - 0 6`. *Ang-specific:* still light on Rossolimo theory at 15 — go for `Be3 + Qd2 + O-O + Rad1` and the `e5` push, posing fresh problems that eat clock. Plans/breaks: **Systems Library — Rossolimo fianchetto**.

**2 — Recommended vs `1...e5`: Center Game.** Dino's 100%/3 line, and it dodges his entire Ruy book (his only clear `1...e5` leak, the C77 Anderssen at 0/2, is unreachable through a Ruy anyway): `1.e4 e5 2.d4 exd4 3.Qxd4 Nc6 4.Qe3`.

**3 — vs `1...e6` (French): King's Indian Attack.** `1.e4 e6 2.d3 d5 3.Nd2 Nf6 4.Ngf3 c5 5.g3`.

**Lines to avoid.** `(C)` A main-line Open Sicilian into his Maróczy prep, and any sharp Ruy theory — both play straight to a well-booked junior's preparation. Don't simplify early; keep the position live.

### Game notes

- **Expected middlegame:** a fresh, slightly unfamiliar middlegame that makes a junior solve problems and burn clock; keep it complex into move 30+, where his endgame (ACPL 22.3) is softest. `(C)`
- **Phase objective:** win by **position type and clock**, not by out-theorizing his cleanest phase (opening ACPL 8.2). `(C)`
- **Clock policy:** pose the first real problem early — his blitz (1993) is ~300 below his classical, so time pressure in an unfamiliar structure is where he cracks. `(C)`/`(R)`
- **Underrated caveat:** prep him like a stronger player; every percentage here is a lower bound on his current strength. `(C)`
- **Model games to study:** Quizon–Ang (Accelerated Dragon, Wch U20 2024) — why to sidestep his pet Sicilian; Vidyarthi–Ang (KIA, Abu Dhabi 2025) — a move-30+ collapse; Romanov–Ang (Catalan Closed, Bangkok 2025) — how a strong player beats his main structure. `(C)`

**Match-day checklist (double-round morning — review only):**

- ☐ Rossolimo vs `...c5/...g6`
- ☐ Center Game vs `...e5`
- ☐ KIA vs French
- ☐ no main-line Open Sicilian
- ☐ R8 (Susilodinata, Black) choice locked the night before

### In-Game Card — R7 ○ White vs Ang (FM, 2309, junior)

**Opening choice.** Rossolimo `3.Bb5` vs `...c5` (denies his Accelerated Dragon); Center Game vs `1...e5`; KIA vs `1...e6`.

**Three middlegame plans (White).** (1) `Nh2 + f4 + e5` kingside roller; (2) `c3 + d4` central break if he delays `...e5`; (3) keep position live to move 30+ where his endgame (ACPL 22.3) softens.

**Avoid.** Open Sicilian into his Maróczy prep; sharp Ruy theory; early simplification.

**Time budget (post-double morning).** Review only; create the first real problem by move 10–12 (his blitz 1993 is ~300 below his classical).

**Win condition.** Unfamiliar structure + clock pressure. Prep him like a 2400.

## Round 8 — ● Black vs IM Susilodinata, Andrean (2360)

*Fri Jun 26, 16:00, Board 4. Source: sixth improved seed report (classical subset, 100 games).*

> **Dragon caution (Gate 1).** Susilodinata plays the **Yugoslav Attack against the Dragon** — exactly Dino's 3-loss structure. With Black vs his `1.e4`, **do not volunteer the Dragon.**

**Opponent snapshot.** `(C)` An **active, experienced grinder** (b. 1990; late IM in 2024; Indonesia's #9). The engine matches the reputation: **solid, accurate, draw-heavy** — classical **43W 31D 26L (58.5%)**, overall ACPL **19.8**, and only **25 blunders in 100 games**. There is no cheap tactical hole. His opening is cleanest (ACPL 10.2); his endgame is his least-accurate phase (**26.4**) but still respectable, with the **high mistake count (69) against few blunders (25)** fitting the draw-heavy record. His Black side (54.0%) is the softer half, and his recent losses cluster there. `(C)`

**Susilodinata's first move (51 White games).** `(C)`

| Susilodinata plays | Games | Dino's answer |
|---|---|---|
| `1.e4` | 42 | `1...c5` — Taimanov/Kan via `2...e6`; **Dragon off** |
| `1.d4` | 8 | `1...Nf6` → anti-Rapport-Jobava / Benoni-Neo-Grünfeld |
| `1.Nf3` | 1 | `1...Nf6` → `...d5` |

**Why this move order.** `(I)` He is overwhelmingly a `1.e4` player (Scotch + principled anti-Sicilians), so the game is almost certainly a Sicilian; `2...e6` keeps Dino in the narrow Taimanov/Kan and **off the Dragon his Yugoslav Attack punishes**. His occasional `1.d4` is the **Rapport-Jobava**, where the plan is to challenge the early `Bf4` and then unbalance. `(C)`

### Ranked response ladder

**1 — Recommended vs `1.e4`: narrow Taimanov/Kan (`2...e6`) — never the Dragon.**

| If Susilodinata plays | Branch | Reference line |
|---|---|---|
| `2.Nf3` then `3.d4` | Taimanov | `1.e4 c5 2.Nf3 e6 3.d4 cxd4 4.Nxd4 Nc6 5.Nc3 Qc7 6.Be3 a6` |
| `2.Nf3` then `3.d4` | Kan | `1.e4 c5 2.Nf3 e6 3.d4 cxd4 4.Nxd4 a6 5.Nc3 Qc7 6.Bd3 Nf6` |
| `2.c3` | Alapin (Dino beat him here) | `1.e4 c5 2.c3 d5 3.exd5 Qxd5 4.d4 Nf6 5.Nf3 e6` |

**Critical position (Taimanov, White to move 7):** `r1b1kbnr/1pqp1ppp/p1n1p3/8/3NP3/2N1B3/PPP2PPP/R2QKB1R w KQkq - 0 7`. *Susilodinata-specific:* he typically goes `Be2 + O-O + Nb3` (Scheveningen flavour) — **Dragon explicitly off** (his Yugoslav Attack is Dino's 3-loss structure). Plans/breaks: **Systems Library — Taimanov**.

**2 — vs `1.d4` Rapport-Jobava: challenge `Bf4`, then unbalance.** Don't drift into a quiet symmetrical Slav; pose problems:

| If Susilodinata plays | Reference line |
|---|---|
| `2.Nc3` + `3.Bf4` (Jobava) | `1.d4 Nf6 2.Nc3 d5 3.Bf4 a6 4.e3 e6` (then `...Bd6`, `...c5`) |
| a `c4`-based `1.d4` | `1.d4 Nf6 2.c4 g6 3.g3 Bg7 4.Bg2 d5` (Dino's 100% Neo-Grünfeld) |

**3 — Dragon: forbidden (Gate 1).** He plays the Yugoslav Attack — Dino's exact 3-loss structure. Do not volunteer it under any move order.

**Lines to avoid.** `(C)` The Dragon/Yugoslav; and do not imagine his **Advance Caro-Kann Tal** leaks — it is irrelevant to Dino-Black and is his rock-solid pet (75%, ACPL 15.0).

### Game notes

- **Expected middlegame:** a solid Taimanov, or an unbalanced Jobava/Benoni/Neo-Grünfeld; **win the long game** — keep pressure into move 30+, where his 2024 results cracked. `(C)`
- **Phase objective:** tighten Dino's own endgame *first* (his ACPL 36.7 is looser than Susilodinata's 26.4) before betting on a marathon against a 31-draws-in-100 grinder. `(C)`
- **Clock policy:** he blunders rarely and draws a third of his games — don't expect a short one; build slow pressure rather than forcing it. `(C)`
- **Confidence point:** Dino has **already beaten him** — Oct 2025 rapid, Susilodinata's Alapin met by Dino's 100% Alapin-as-Black. Real confidence, but a rapid result — don't over-read it. `(R)`
- **Model games to study:** his Black losses — Slav Modern Line vs Chatalbashev (2023); Caro Tartakower vs Mohammad Fahad (Budapest, 2024); late slips vs Tin Jingyao (SGP-ch, 2025) and Mamatov (2024). `(C)`

**Match-day checklist (double-round evening):**

- ☐ Taimanov vs `1.e4` (Dragon OFF)
- ☐ anti-Jobava `...a6/...e6` line
- ☐ Benoni/Neo-Grünfeld if a `c4`-based `1.d4`
- ☐ one drawing-defense hold (Gate 3)
- ☐ recovery completed after R7

### In-Game Card — R8 ● Black vs Susilodinata (IM, 2360)

**Opening choice.** Narrow Taimanov via `2...e6` vs `1.e4` — **Dragon explicitly off** (he plays the Yugoslav Attack). Anti-Jobava `...a6/...e6` vs his rare `1.d4 + Bf4`.

**Three middlegame plans (Black).** (1) `...b5–b4` to displace `Nc3`; (2) `...d5` only after full prep; (3) build slow pressure — he draws 31% of his games.

**Avoid.** The Dragon under any move order; symmetric Slav vs the Jobava (challenge `Bf4` instead).

**Time budget (post-R7 double evening).** Physical reset; opening locked from last night.

**Win condition.** Marathon technique into move 30+. **Pre-game cross-check:** Dino's ACPL 36.7 > Susilodinata's 26.4 — don't bet on a grind unless drawing-defense is sharp (Gate 3).

## Round 9 — ○ White vs GM Thejkumar, M. S. (2358)

*Sat Jun 27, 16:00, Board 2. Final round. Source: seventh improved seed report (classical subset, 48 games) + DB. Inactive since Feb 2024, now coaching — expect rust.*

**Opponent snapshot.** `(C)` A genuine GM (2358) but **effectively inactive — no FIDE-rated games since February 2024 — and now coaching.** His whole file is pre-2024, which cuts both ways: it shows the trusted lines he is likeliest to reuse, but it also means **expect OTB rust** in long-game calculation and clock handling. In the classical subset he is a normal solid GM — **21W 15D 12L (59.4%)**, overall ACPL 21.9 — with his **opening his best phase (ACPL 7.9)** and his **endgame his weakest (ACPL 30.0, 24 blunders / 48)**, clustered in the move-30+ transition. `(C)`

**Thejkumar's answer to `1.e4` (26 of 48 Black games met `1.e4`).** `(C)`

| Thejkumar plays | Games | Dino's weapon |
|---|---|---|
| `1...c6` (Caro-Kann) | 25 | Two Knights Attack `2.Nc3` |
| `1...Nf6` (rare) | 1 | Standard `2.e5` |

**Why this is a Caro-Kann battle, not a Sicilian one.** `(I)` As Black he is a **near-pure Caro-Kann player** — essentially no Sicilian and no French — so **Moscow/Rossolimo/KIA simply do not apply.** Plan the White game specifically against `1...c6`, and win by structure type and stamina, not by out-theorizing his cleanest phase. `(C)`

### Ranked response ladder

**1 — Recommended: Two Knights Attack.** Dino's tested anti-Caro (B10, 100%/1), low-theory, and it sidesteps his deep Advance/Classical preparation:

| If Thejkumar plays | Branch | Reference line |
|---|---|---|
| `3...Bg4` (pin) | Two Knights main | `1.e4 c6 2.Nc3 d5 3.Nf3 Bg4 4.h3 Bxf3 5.Qxf3 Nf6` |
| `3...dxe4` | Two Knights | `1.e4 c6 2.Nc3 d5 3.Nf3 dxe4 4.Nxe4` |

**Critical position (Two Knights main, White to move 6):** `rn1qkb1r/pp2pppp/2p2n2/3p4/4P3/2N2Q1P/PPPP1PP1/R1B1KB1R w KQkq - 1 6`. *Thejkumar-specific:* expect `...e6 + ...Bd6` Tartakower-flavour after a two-year layoff — counter-plan `Bd3 + Bg5 + O-O-O + g4–g5`. Plans/breaks: **Systems Library — Two Knights anti-Caro**.

**2 — Fallback (trained only): the Advance.** `1.e4 c6 2.d4 d5 3.e5 Bf5 4.Nf3 e6 5.Be2 c5`. His Advance-Short is **0/2** `(C)`, but Dino has **no Advance Caro reps** — use only if it has been drilled with model games; otherwise stay with the Two Knights.

**Lines to avoid.** `(C)` Out-theorizing a GM in his own trusted Caro lines (opening ACPL 7.9 is his best phase). The surprise value comes from position type and clock, not a sharper line in his pet variations.

### Game notes

- **Expected middlegame:** keep pieces on into the first time control — his softest classical phase is the endgame (ACPL 30.0) and a two-year layoff hurts late calculation and clock most. `(C)`
- **Phase objective:** out-stamina a rusty GM rather than out-theorize him; make him calculate a complex late middlegame instead of reciting preparation. `(C)`
- **Clock policy:** it is the **final round** — bring a rested head, not new theory; favour a structure he must solve over the board. `(I)`
- **Mirror caution (own side):** Dino's own late technique (ACPL 36.7, 4 drawing-defense failures) is looser than Thejkumar's 30.0 — tighten conversion/defence first so the "make him work late" plan doesn't backfire. `(C)`
- **Model games to study:** his classical Advance-Short losses to Nikitenko (Colombo, 2022) and Mahdavi (Dubai, 2022); his late-phase blunder losses to Nikitenko (Semi-Slav, 39.Qe4) and Fominyh (QGA ending, 37.Rc1); and his freshest game, the QID vs Ghosh (Bangalore, Jan 2024). `(C)`

**Match-day checklist (final round):**

- ☐ Two Knights main vs `1...c6`
- ☐ Advance only if trained
- ☐ own conversion technique sharp
- ☐ rested head — no new theory on the last day

### In-Game Card — R9 ○ White vs Thejkumar (GM, 2358, two-year layoff)

**Opening choice.** Two Knights Attack vs `1...c6` (B10). Advance is a fallback **only** if drilled.

**Three middlegame plans (White).** (1) queen to `g3` after the `Bxf3` trade — long castling principled; (2) `Bg5 + e5` if he commits `...e6` without `...Nbd7`; (3) keep pieces on into the first time control — his endgame is ACPL 30.0 plus rust.

**Avoid.** Out-theorizing him in his trusted Caro lines (his opening ACPL is 7.9 — his best phase).

**Time budget (final round).** Opening to move 12 ≤ 15m (low-theory by design); save clock for moves 25–40.

**Win condition.** Out-stamina a rusty GM. **Mirror caution:** Dino's ACPL 36.7 > Thejkumar's 30.0 — conversion must be sharp.

## Appendix — Evidence & Verification Notes

- **Sources.** Schedule, colors, boards, and ratings from `manual_sections/Tournament_Schedule.md`. The Round 1 and Round 2 results and moves come from the official PGN files `2nd_DAV_Go_Day1.pgn` and `2nd_DAV_Go_Day2.pgn`. Opponent reads come from the eight `*_seed_report_improved.md` files (Stockfish 18, depth 12) and `manual_sections/Opponent_*.md`; Dino's profile from `manual_sections/Dino_Ballecer_Needs_Improvement.md`. Opening distributions were queried from `prep_manual.db`. Tan's rapid tendency comes from the FIDE World Rapid Team PGN (17–19 Jun 2026).
- **Seed-report mapping (by seeding, not round).** R1 Morris = 3rd · R2 Tan = 4th · R4 Vignesh = 1st · R5 Shyaam = 2nd · R6 Chan = 5th · R7 Ang = 8th · R8 Susilodinata = 6th · R9 Thejkumar = 7th. R3 Cabe has no seed report (dossier only).
- **Evidence discipline.** `(C)` classical, `(R)` rapid/online tendency only, `(I)` inference. Rapid evidence never overrides classical results. Demoted targets in the improved seed reports are not revived here (e.g., Vignesh's Advance Caro "Tal" line).
- **Move legality.** Every line above was replayed through the workspace SAN validator (`fens_for` / `MiniBoard`, `prep_manual_app.py`); all sequences are legal from the start position.
- **Scope.** This update revises the playbook and ingests the official Round 1 and Round 2 PGNs into `prep_manual.db`; it does not alter the Tournament Preparation Manual or application code.
