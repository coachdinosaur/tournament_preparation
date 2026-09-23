# Ellie (ellie16): Weaknesses and Improvement Plan

*Prepared 2026-09-24 for Ellie and her coach (Lichess: Chess_Attack_Juras).*

**Basis of this report.** All 31 competitive Lichess games since coaching settled in (30 rated + 1 casual
vs a human, **30 Jul – 22 Sep 2026**), plus 35 checkmate-drill games from the same period. Games before
June were excluded on the coach's advice (pre-coaching beginner play). Casual games against friends and
the Lichess AI were also left out. Every move was checked by **Stockfish 18 at depth 16**; the
10 games in the coach's study were re-checked at depth 18.

Error sizes used below: an **error** loses 1–3 pawns of value; a **blunder** loses 3+ pawns (usually a
piece, a queen, or the game).

---

## 1. The Short Version

Ellie is **improving fast**: her rapid rating went from **873 to about 990 in eight weeks**, and she scores
**15 wins, 5 draws, 11 losses** in this period. Her openings are already sound. She is losing points in
four specific, very trainable ways:

| # | Weakness | Evidence |
|---|---|---|
| 1 | **Not finishing won games** | She had a winning position (+3 or more) in **10 of her 16 non-wins**. That is 6 losses and 4 draws thrown away. |
| 2 | **Forgetting her own king** | In 3 losses her queen went pawn-hunting on the other side of the board and she was mated or collapsed. 8 times she allowed a mate from a position that was not lost. |
| 3 | **Not checking checks and captures (both sides)** | 57 times she did not punish an opponent's blunder. 45 times the best move was a check she did not see. 40 times she left something hanging. |
| 4 | **Playing too fast** | Median think time is **5 seconds a move**. **68% of her serious mistakes were played in 10 seconds or less.** In her losses she still had **5½ minutes left on average** of a 10-minute clock. |

**The one habit that fixes most of this:** before every move, ask *"What are all the checks and captures
— for me and for my opponent?"* and when the position is winning, ask *"How can I lose from here?"*

**Good news for the coach:** she gets into winning positions *all the time*. Converting even half of those
10 games would have turned about 5 losses/draws into wins, a big rating jump without learning anything new.

---

## 2. The Numbers

**Results since 30 Jul (31 games):** 15W 5D 11L (56%).
As White **8W 3D 4L** · As Black **7W 2D 7L**.

**Accuracy by phase** (average centipawn loss per move; lower is better):

| Phase | Avg loss | Blunders per 40 moves |
|---|---:|---:|
| Opening (moves 1–10) | **45** | **0.9** |
| Middlegame | 113 | 4.4 |
| Endgame | 101 | 4.7 |

The opening is her strongest phase by far. **Games are decided after move 10**, so that is where training
time should go.

**Where her first serious error happened in each loss:** opening 3 · middlegame 3 · endgame 4.

**Clock:** the median move takes 5 s. She has lost 0 games on time, and 2 opponents lost on time
against her. Time is not her problem; *unused* time is.

**Trend:** blunders per game went from 3.7 (August) to 3.3 (September). That is slightly better but
not yet a real change, so the habits below still need to be built.

---

## 3. Weakness 1: Finishing Won Games (Biggest Opportunity)

She was **+3 or better** in these games and did not win:

| Date | Result | Peak | What went wrong | Game |
|---|---|---:|---|---|
| 30 Jul | Draw | mate | Pushed her own a-pawn instead of stopping the opponent's f-pawn (47…a4?? instead of 47…Rb8). | [mTRcV52K](https://lichess.org/mTRcV52K) |
| 4 Aug | Draw | +15 | Let a +15 position slip until she was lost by move 53. The opponent then stalemated her, which saved the draw. | [AcsuuVJN](https://lichess.org/AcsuuVJN) |
| 6 Aug | Loss | +6 | Queen pawn-grab (…Rxa2) then 33…Qc3?? allowed a mating attack. | [272djLV3](https://lichess.org/272djLV3) |
| 6 Aug | Draw | +15 | Queen vs rook, winning. 73…Qc7?? walked into a **skewer** (Rg7+ and Rxc7). | [lXEMbnIu](https://lichess.org/lXEMbnIu) |
| 29 Aug | Loss | +5 | Queen raid, then king walk 40.Kh3?? into …g2+ and a new queen. | [hRZVSLvD](https://lichess.org/hRZVSLvD) |
| 30 Aug | Loss | +4 | Queen took three pawns (…Qxa2, Qxc2, Qxd3), then 21…Qa5?? Qxg7#. | [9P9uvvXN](https://lichess.org/9P9uvvXN) |
| 30 Aug | Draw | mate | **Two queens and a rook, then stalemate** (48.Qg6??; 48.Qd8# was mate). | [Zkkv2PVq](https://lichess.org/Zkkv2PVq) |
| 18 Sep | Loss | +7 | Missed 27…Qd1+ winning a rook, then pawn-pushed while her king was attacked. | [rAy1Gg7I](https://lichess.org/rAy1Gg7I) |
| 19 Sep | Loss | +6 | King ran up the board into checks, and her time dropped to 14 s. | [psMichA1](https://lichess.org/psMichA1) |
| 21 Sep | Loss | +5 | Missed 25…Qxa1+ (a free rook **with check**), then 26…Rhe8?? to a discovered check. | [IWds74e6](https://lichess.org/IWds74e6) |

**Patterns inside the conversion problem**

- **Stalemate awareness.** Her drill record in the basic mates is good (below), but in a real game she
  stalemated with *two queens and a rook*. The lesson is that once the opponent has only a king (plus
  blocked pawns), every move needs a stalemate check.
- **Pawn races.** Stop the opponent's passed pawn *before* pushing your own.
- **Queen endings and skewers.** With a queen vs a rook, keep the queen off lines where the rook can
  check the king and hit the queen.
- **"Win more" greed.** When she's winning, she keeps grabbing pawns instead of making the position
  safe. The rule should be: **when you're winning, trade pieces and protect your king.**

**Checkmate drills since June (vs coach / AI):**

| Drill | Result | Read |
|---|---|---|
| K+Q vs K | 5/5 mates | Solid |
| K+R+R vs K | 2/2 mates | Solid |
| K+R vs K | 6/8 mates | Mostly solid; 2 drills ran out |
| K+B+B vs K | 4/6 mates | One drill ended "insufficient material" (**she lost a bishop**) and one hit the 50-move limit |
| **K+Q vs K+N** | **2/6 mates** | **Weakest drill.** Queen vs a minor piece needs work (forks!) |
| K+Q vs K+B | 1/2 mates | Small sample |

The coach has clearly been building technique here. The next step is to **connect the drills to real
games**: start drills from *messier* winning positions (queen + pawns vs rook, extra piece in the
middlegame) and play them out against the AI at 10+0.

---

## 4. Weakness 2: Forgetting Her Own King

The most repeated way she loses a good position:

1. Her queen goes to the far side of the board to collect pawns (…Qxa2, …Qxb3, …Qxc2, …Qxd3).
2. The opponent's queen and rook swing toward her king.
3. She makes one natural-looking move and gets mated or loses the queen.

Clear examples: [272djLV3](https://lichess.org/272djLV3) (mated with 9 min left),
[9P9uvvXN](https://lichess.org/9P9uvvXN) (Qxg7# with 8 min left),
[rAy1Gg7I](https://lichess.org/rAy1Gg7I), and the 20 Sep game vs Fielder770 where the
opponent twice ignored …Rxg2+ before finally playing …Qxh2#.

**Rules to teach:**

- **"One pawn is not worth my king."** Before taking a pawn with the queen, count how many enemy pieces
  can reach her king in two moves.
- **When an enemy rook or queen lines up on her king's file or diagonal, stop and defend first.**
- **Keep at least one defender near the king.** In the losses, the queen was the *only* defender, and
  she moved it away.

---

## 5. Weakness 3: Checks and Captures (For Both Sides)

At ~1000 level, opponents blunder constantly, and so does Ellie. Games go to whoever notices first.

- **Missed opponent blunders: 57.** The opponent dropped material and she played a normal move.
- **Missed her own check: 45.** Two recent examples: 25…**Qxa1+** won a free rook with check
  ([IWds74e6](https://lichess.org/IWds74e6)), and 27…**Qd1+** followed by …Qxg4 won a rook
  ([rAy1Gg7I](https://lichess.org/rAy1Gg7I)).
- **Left material en prise: 40.** Examples: 25.Qd7?? simply hung the queen (the opponent missed it), and
  6…Nxd4? walked into 7.Qxd4 with 8.Qxd8+ coming.
- **In-between moves (zwischenzug).** She recaptures automatically. Example: 14.exf6! wins a piece
  before recapturing on d3 ([Pirc game 18 Sep](https://lichess.org/LTyHtVM0)).
- **Discovered checks.** A rook in front of a queen that is aiming at her king is a loaded gun
  (26…Rhe8?? 27.Rxe8+, [IWds74e6](https://lichess.org/IWds74e6)).

---

## 6. Weakness 4: Speed

| Stat | Value |
|---|---:|
| Median time per move | 5 s |
| Median time on a move that was a serious mistake | 6.5 s |
| Serious mistakes played in ≤ 10 s | **68%** |
| Clock left at the end of losses (average) | **5 min 31 s** of 10 min |

She is not making mistakes because she is short of time. She is making them because she doesn't
**stop** at the critical moments. In 10+0 games, she can afford about **20 seconds on 8–10 moves per
game**.

**"Stop signs": moments that deserve 20+ seconds**

1. The opponent just **captured** or gave **check**.
2. An enemy piece just moved **toward her king**.
3. She is about to **take a pawn with her queen**.
4. The evaluation feels **winning**, whenever she thinks "I'm winning."
5. **Few pieces left** (endgame), where every move matters and stalemate becomes possible.

For practice games, **switch to 15+10** for the next month. That builds the stopping habit without
clock panic. Then go back to 10+0.

---

## 7. Openings (Keep, Just Patch)

Openings are **not** the problem (0.9 blunders per 40 opening moves). Don't spend much training time here.

| Ellie | Line | Score | Note |
|---|---|---|---|
| White | 1.e4 e5, Four Knights (Italian / Spanish) | 3W 3D 2L | Good, keep it |
| White | 1.e4 vs other replies (…Nc6, …Nf6, …b6, …c6, …d6) | 5/5 wins | Fine |
| White | 1.e4 c5 2.Bc4 (Bowdler) | 0/2 | Both lost in the middlegame. Try a simple **2.Nf3 + 3.Bc4** or **2.Nc3** plan the coach likes |
| Black | 1.e4 e5 | 4W 1D 3L | Good, keep it |
| Black | 1.d4 d5 (with …Nc6 / …Bg4) | 1W 4L | Losses were mostly middlegame, but see the trap below |

**One opening trap to fix now:** 1.d4 d5 2.Nf3 Nc6 3.c4 dxc4 4.Nc3 Nf6 5.e4 Bg4 6.Bxc4. Here
**6…Nxd4? loses a piece** to 7.Qxd4!, because 7…Bxf3 is met by **8.Qxd8+** with check first. The right
order is **6…Bxf3 7.gxf3 Qxd4**: *remove the defender first, then take the pawn.*

---

## 8. Strengths to Build On

- **Solid, principled openings.** She develops knights early, castles, and fights for the center.
- **Clean games when calm:** 18 Sep London (0 blunders), 9 Sep Four Knights (0 blunders), and
  20 Sep vs Qknights, where she punished 14…Bxd1 with **15.Bxf7#**.
- **She creates winning chances constantly.** Ten +3 positions in the games she didn't win shows her
  play is often good enough; the finishing is what's missing.
- **Basic mates are solid:** K+Q vs K 5/5, K+R+R vs K 2/2.
- **Rating trend is strongly up:** +120 in eight weeks.

---

## 9. Six-Week Training Plan

### Every day at home (25–30 min)

| Block | What | How |
|---|---|---|
| 10 min | Lichess puzzles by theme | Rotate: **Hanging piece**, **Mate in 1 / Mate in 2**, **Discovered attack**, **Intermezzo**, **Defensive move**, **Queen endgame** |
| 10 min | "Opponent's threat" drill | On a random puzzle position, *before* solving, say out loud what the **opponent** threatens |
| 5–10 min | One game from this report | Replay one game from the tables above and find the move she missed |

### With the coach (weekly session, ~60 min)

| Week | Focus | Session plan |
|---|---|---|
| 1 | **Blunder check (CCT)** | Teach "Checks, Captures, Threats — mine, then theirs." Solve training positions 1–4 below. Play 2 training games at 15+10 where she must say "CCT" out loud before each move. |
| 2 | **King safety** | Positions 5–7. Rule: "one pawn is not worth my king." Play out the 6 Aug and 30 Aug positions (before the queen raid) from both sides vs the coach. |
| 3 | **Finishing won games I** | Stalemate traps (position 8) and pawn races (position 9). Drill: Ellie has +5 in a messy position vs the AI, and must win without stalemate. |
| 4 | **Finishing won games II** | Queen vs minor piece (her weakest drill: K+Q vs K+N 2/6), queen vs rook (position 10). "When winning, trade pieces." |
| 5 | **In-between moves and discovered checks** | Positions 11–12. Theme puzzles: Intermezzo and Discovered attack. |
| 6 | **Review + stop-sign test** | Coach reviews her last 10 games. For each error, *was it a stop-sign moment?* How long did she think? Adjust. |

### Practice games

- **Next 4 weeks: 15+10 rapid** (not 10+0). The goal is to use time on stop-sign moves.
- After each loss, before the next game, she writes **one line**: *"I lost because I missed ___."*
- Once a week, the coach looks at those lines. The same line repeating is the next training topic.

**Targets to track (coach checks monthly):**

| Measure | Now | Target in 6 weeks |
|---|---:|---:|
| Blunders per game | 3.3 | under 2 |
| Won positions (+3) not won | 10 of 31 games | under 1 in 6 |
| Clock left in losses | 5½ min | under 3 min (she used it) |
| K+Q vs K+N drill | 2/6 | 5/6 |

---

## 10. Tournament-Day Card

Print this and keep it next to the scoresheet.

> **Before every move: CCT.** Checks, Captures, Threats. Mine first, then my opponent's.
>
> **Stop signs (think 20+ seconds):** a capture or check just happened · a piece is coming at my king ·
> I want to grab a pawn with my queen · I'm winning · few pieces left.
>
> **When I'm winning:** trade pieces · protect my king · stop their passed pawn · **check for stalemate
> every move** once they only have a king.
>
> **Clock:** use it. Finishing with lots of time left and a loss is the worst result.

---

## 11. Training Positions (Solve First, Answers Below)

Paste the FEN into Lichess (*Tools → Board editor → FEN*) or click the link.

| # | Theme | Position (FEN) | Task |
|---|---|---|---|
| 1 | Remove the defender | `r2qkb1r/ppp1pppp/2n2n2/8/2BPP1b1/2N2N2/PP3PPP/R1BQK2R b KQkq - 0 6` [open](https://lichess.org/analysis/standard/r2qkb1r/ppp1pppp/2n2n2/8/2BPP1b1/2N2N2/PP3PPP/R1BQK2R_b_KQkq_-_0_6) | Black to play. Is 6…Nxd4 safe? What should Black play? |
| 2 | Free material with check | `3r2kr/2p3p1/p4q1p/2Q5/4R3/PP4P1/5P1P/R5K1 b - - 0 25` [open](https://lichess.org/analysis/standard/3r2kr/2p3p1/p4q1p/2Q5/4R3/PP4P1/5P1P/R5K1_b_-_-_0_25) | Black to play and win material. |
| 3 | Discovered check | `3r3r/2p3pk/p4q1p/8/4R3/PP4P1/2Q2P1P/R5K1 b - - 2 26` [open](https://lichess.org/analysis/standard/3r3r/2p3pk/p4q1p/8/4R3/PP4P1/2Q2P1P/R5K1_b_-_-_2_26) | Black to play. What does White threaten? (She played 26…Rhe8??) |
| 4 | Check that wins | `5rk1/1p3pp1/7Q/p1p1P3/3p2R1/3q3P/5PP1/6K1 b - - 0 27` [open](https://lichess.org/analysis/standard/5rk1/1p3pp1/7Q/p1p1P3/3p2R1/3q3P/5PP1/6K1_b_-_-_0_27) | Black to play and win. |
| 5 | King safety | `8/1Q3pk1/6pp/2qp4/8/3P2P1/r6P/5R1K b - - 5 33` [open](https://lichess.org/analysis/standard/8/1Q3pk1/6pp/2qp4/8/3P2P1/r6P/5R1K_b_-_-_5_33) | Black to play. What is White threatening against f7? |
| 6 | King safety | `1r3rk1/ppR3pp/3p1p2/5P2/3pP1Q1/5R2/3q2PP/6K1 b - - 0 21` [open](https://lichess.org/analysis/standard/1r3rk1/ppR3pp/3p1p2/5P2/3pP1Q1/5R2/3q2PP/6K1_b_-_-_0_21) | Black to play. Find White's threat, then Black's best move. (She played 21…Qa5??) |
| 7 | King walk | `3r2k1/8/1N5p/Q4p2/P1P5/3P1qp1/5P1K/5R2 w - - 0 40` [open](https://lichess.org/analysis/standard/3r2k1/8/1N5p/Q4p2/P1P5/3P1qp1/5P1K/5R2_w_-_-_0_40) | White to play. Why is 40.Kh3 a disaster? Where must the king go? |
| 8 | Stalemate | `1Q6/8/8/8/4Q1Pk/6p1/6K1/5R2 w - - 1 48` [open](https://lichess.org/analysis/standard/1Q6/8/8/8/4Q1Pk/6p1/6K1/5R2_w_-_-_1_48) | White to play and mate in one. Which "natural" move stalemates? |
| 9 | Pawn race | `3r4/4KP2/8/p6p/7k/8/8/8 b - - 1 47` [open](https://lichess.org/analysis/standard/3r4/4KP2/8/p6p/7k/8/8/8_b_-_-_1_47) | Black to play. Push the a-pawn or stop the f-pawn? |
| 10 | Queen vs rook skewer | `6R1/3k4/8/1K6/8/8/8/2q5 b - - 15 73` [open](https://lichess.org/analysis/standard/6R1/3k4/8/1K6/8/8/8/2q5_b_-_-_15_73) | Black to play. Why does 73…Qc7 lose the queen? Find a safe winning move. |
| 11 | In-between move | `r1b1r1k1/ppB2pbp/2p2np1/4P3/8/2Nn1N2/PPP2PPP/R4RK1 w - - 0 14` [open](https://lichess.org/analysis/standard/r1b1r1k1/ppB2pbp/2p2np1/4P3/8/2Nn1N2/PPP2PPP/R4RK1_w_-_-_0_14) | White to play. Don't recapture on d3 yet! |
| 12 | Pinned knight | `3r1rk1/ppp1bppp/4pn2/4P1B1/2B5/2N2P2/PP3P1P/R4R1K b - - 0 13` [open](https://lichess.org/analysis/standard/3r1rk1/ppp1bppp/4pn2/4P1B1/2B5/2N2P2/PP3P1P/R4R1K_b_-_-_0_13) | Black to play. The knight is attacked. Is it really stuck? |

### Answers

1. **6…Bxf3! 7.gxf3 Qxd4** wins the pawn safely. After 6…Nxd4? 7.Qxd4!, the move 7…Bxf3 fails to
   **8.Qxd8+** (check first!), and Black is a piece down. *Remove the defender, then take.*
2. **25…Qxa1+.** The rook on a1 is loose on the long diagonal, and she takes it **with check**.
3. White threatens **Re-anything with a discovered check** from Qc2 to h7. 26…Qg6! blocks the
   diagonal. 26…Rhe8?? lost to 27.Rxe8+.
4. **27…Qd1+! 28.Kh2 Qxg4.** The check wins the rook on g4.
5. White threatens **Qxf7+** with a mating net (Qf8+, Rf7+). **33…Rf2!** blocks the f-file and keeps
   Black winning.
6. White threatens **Qxg7#**. **21…Qd1+** first (or 21…Rf7) defends. 21…Qa5?? 22.Qxg7#.
7. After 40.Kh3?? g2+, the pawn promotes. **40.Kg1** (or 40.fxg3) holds.
8. **48.Qd8#** (or 48.Qh7+ Kg5 49.Qh5#). **48.Qg6??** is stalemate: Black has no legal move and is not in check.
9. **47…Rb8!** stops the f-pawn (…Rf8 and …Rxf7) and Black wins. 47…a4?? 48.Kxd8, and White queens first.
10. After 73…Qc7?? 74.Rg7+, the rook checks the king and **skewers** the queen. Win with checks that keep
    the queen safe, e.g. **73…Qb2+ 74.Ka6 Qa2+ 75.Kb6 Qe6+ 76.Kc5 Qxg8**.
11. **14.exf6!** attacks the bishop and wins a piece before recapturing on d3.
12. **13…Nd5!** The knight is only "pinned" to a *defended* bishop on e7. After 14.Bxe7 Nxe7, nothing is lost.

---

## Appendix: Games Used

31 competitive games, 30 Jul – 22 Sep 2026, from `lichess.org/@/ellie16`. The 10 games from the coach's
study (18–22 Sep) are included. Full per-move engine output is available on request.
