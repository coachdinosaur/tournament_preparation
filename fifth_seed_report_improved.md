# Fifth Seed Report: IM Chan, Kim Yew

*Prepared 2026-06-14 for FM Dino Ballecer ("Coach Dinosaur"). Roster player `6`.*

**Title:** IM | **Federation:** MAS | **FIDE (standard):** 2360 | **Rapid / Blitz:** 2177 / 2187

**Basis of this report.** Curated from the refreshed auto-generated dossier
[Opponent_IM_Chan_Kim_Yew.md](manual_sections/Opponent_IM_Chan_Kim_Yew.md), cross-checked against
Dino's self-audit
[Dino_Ballecer_Needs_Improvement.md](manual_sections/Dino_Ballecer_Needs_Improvement.md) and the
web-sourced [Live_Scouting_2026-06-13.md](manual_sections/Live_Scouting_2026-06-13.md).

- **134 games on file** = **99 over-the-board PGN games** + **35 Lichess online records without full move lists**.
- **Engine claims below are from 99/99 OTB PGN games analysed by Stockfish 18 at depth 12.** There
  are **0 pending engine games**.
- **Mixed time controls in the engine sample.** Of the 99 analysed games, **60 are classical opens**
  and **39 are online Titled Tuesday rapid** events. Because Dino plays a classical event, this
  report leads with the **classical-only** subset and flags where the headline numbers are inflated
  by speed games.
- **Command used:** `python prep_manual_app.py --analyze --scope player --player 6 --depth 12 --export`.

---

## 1. Executive Summary

Chan is a young (born 2002), currently active Malaysian IM with the deepest file in the pool (**134
games**) and a solid but not crushing overall score of **59W 32D 43L (56.0%)**. He scores **63.8% as
White (69 games)** and **47.7% as Black (65 games)**, so his Black is the more targetable side.

- **The single most important read in this file: separate his classical play from his online play.**
  Across all 99 analysed games his ACPL is 23.1 and his endgame ACPL is 29.9, with 41 blunders. But
  that is made worse by 39 online Titled Tuesday rapid games. **Restricted to his 60 classical
  games, he is much cleaner: overall ACPL 16.1, endgame ACPL 20.8, only 8 blunders.** Do not build
  the match plan around an endgame collapse that mostly happens at speed.
- **Best classical target when Dino has White:** the **Advance Caro-Kann against his Black**. His
  classical Advance Caro file is **0W 2D 3L (20.0%)** over 5 games, and **his two most recent
  classical games on record (Apr 2026 Bangkok, Feb 2026 Cannes) are both Advance Caro-Kann losses.**
  This is a strong, fresh result target - but a workload warning, because the engine says he defends
  it cleanly (ACPL 15.0, 0 blunders) and Dino has no Advance Caro games in his own file.
- **Easiest White fit:** if Chan answers 1.e4 with the French, use Dino's proven **King's
  Indian Attack (91.7% over 6 of Dino's own games)**. Chan plays the French and his most-played
  French line sits at 50%. This needs no new prep.
- **Best classical target when Dino has Black:** his **fianchetto/King's-Indian White setups**. With
  White in the Fianchetto KID / Grünfeld family he scores only **41.7% (0W 5D 1L)** over 6 classical
  games — he draws a lot and almost never wins there. The goal is a safe equalizer that denies him a
  win, not a knockout.
- **Avoid as Black:** letting him reach a clean **Catalan / Réti squeeze with White**. He is genuinely
  strong and clean there (**67.9%, ACPL 13.5** over 14 classical games). His online Catalan looks
  shaky; his classical Catalan does not.
- **One-sentence game plan:** *With White, meet his French with the proven KIA and prepare the
  Advance Caro-Kann only as a trained project; with Black, deny him a comfortable Catalan/Réti
  squeeze and steer toward his draw-heavy fianchetto setups, while keeping the game in long classical
  positions rather than the kind of speed shuffle where his blunder rate spikes.*

---

## 2. Opening Repertoire

**As White - 69 games, 63.8%.** Chan's White is a 1.d4 / 1.c4 / 1.Nf3 player: Catalan, English, Réti
and fianchetto King's-Indian structures. He is comfortable and well-scoring in his main Catalan/Réti
universe, so there is no cheap White-side trap to set; the targets are his quieter, draw-heavy
fianchetto KID lines.

**As Black - 65 games, 47.7%.** This is his softer side and where the real opening targets live. The
Advance Caro-Kann is the main weak spot; the Petrov and Classical Caro-Kann are secondary result
signals on small samples.

### Confidence lines - do not let him coast

| Line | ECO | Games | Score | Suggested action |
|---|---|---:|---:|---|
| Catalan Opening: Closed as White | E01 | 3 | 83.3% | As Black, do not hand him a calm closed Catalan squeeze |
| Pirc Defense: Kholmov System as White | B07 | 3 | 100.0% | Do not drift into a Pirc/Modern vs his 1.e4 sidelines |
| Sicilian: Nyezhmetdinov-Rossolimo, Fianchetto as Black | B31 | 3 | 100.0% | He is comfortable vs the Rossolimo; bring real ideas, not just the move order |
| Sicilian: Taimanov, Bastrikov as Black | B47 | 3 | 83.3% | Strong Taimanov scorer; avoid a generic Open Sicilian race |
| Bogo-Indian Defense: Retreat Variation as Black | E11 | 2 | 75.0% | Solid vs 1.d4/Nf3; not a target |

### Repair / target lines - candidate targets only

| Line | ECO | Games | Score | Suggested action |
|---|---|---:|---:|---|
| Caro-Kann: Advance (incl. Tal) as Black | B12 | 5 | 20.0% | **Top White target** - fresh, classical, recurring; train it first |
| Petrov's Defense: Nimzowitsch Attack as Black | C42 | 2 | 0.0% | Possible White target on a small sample; needs a 1.e4 e5 plan |
| Caro-Kann: Classical Variation as Black | B19 | 2 | 25.0% | Secondary Caro target if Dino prefers the Classical mainline |
| King's Indian Defense: Fianchetto as White | E60 | 3 | 33.3% | Best Black-game opening target; draw-heavy fianchetto play |
| Queen's Pawn Game: Symmetrical as White | D02 | 2 | 25.0% | Minor Black-game signal; small sample |
| English: Symmetrical, Three Knights as Black | A34 | 2 | 25.0% | Minor; useful if Dino opens 1.c4 |

> **Online-only caveat:** his Ruy Lopez Anti-Marshall file reads 0/2, but both games are Lichess
> blitz records without full moves, so treat it as speed noise, not a classical White-side weakness.

### Repertoire-fit check

- **White plan A - KIA vs the French (easiest fit).** Dino's own King's Indian Attack is a
  tested 91.7% weapon over 6 games. Chan plays the French; his most-played French line is 50%. This
  is the highest-confidence path and does not require a new opening project.
- **White plan B - Advance Caro-Kann project.** The Chan-specific evidence is excellent and current,
  but Dino's audit flags **zero practical Advance Caro-Kann reps**. Use it only after training games
  and model-game review, not as a cold surprise.
- **White plan C - anti-Sicilian default.** Dino's Moscow/Rossolimo file is 100%, but Chan defends
  Sicilians well (Rossolimo Fianchetto 100%, Taimanov 83%). If Chan answers 1.e4 with 1...c5, play
  for a normal game, not a refutation.
- **Black plan - deny the Catalan/Réti squeeze.** Prepare one solid setup against 1.c4 / 1.Nf3 / g3.
  Chan's classical Catalan/Réti as White is strong (67.9%, ACPL 13.5), so the objective is a clean
  equalizer, then steer toward his draw-heavy fianchetto KID structures.
- **Dino's Dragon risk is low here.** Chan is a 1.d4/1.c4/1.Nf3 player with White, so Dino's flagged
  Dragon problem line (3 losses from `e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6`) is unlikely to appear in this
  pairing.

---

## 3. Phase Accuracy

*From 99 analysed OTB PGN games at depth 12. Lower ACPL = cleaner play. The split below is the most
important table in this section.*

| Subset | Games | Overall ACPL | Endgame ACPL | Blunders | Mistakes |
|---|---:|---:|---:|---:|---:|
| All analysed | 99 | 23.1 | 29.9 | 41 | 88 |
| **Classical only** | **60** | **16.1** | **20.8** | **8** | **31** |
| Online (Titled Tuesday) | 39 | 34.6 | 46.0 | 33 | 57 |

Per-phase ACPL across all 99 games: opening 12.4, middlegame 18.5, endgame 29.9.

**Interpretation (within-player only).** In classical chess Chan is an accurate, low-blunder player:
8 blunders across 60 games and an endgame ACPL of 20.8 are not the profile of a player who hands back
endings. His error rate roughly **doubles online**, which matches his rating profile (standard 2360
vs rapid 2177 / blitz 2187). The practical takeaway is not "grind his endgame"; it is "keep him in
long, classical-rich positions and do not expect speed-style gifts."

> **Cross-player caution.** Dino's own depth-12 profile rests on only 7 analysed losses (overall
> ACPL 26.7, endgame 36.7, with 4 drawing-defense samples). Against a classically-clean defender like
> Chan, Dino's own endgame technique is the bigger variable - any "outplay him later" plan needs Dino
> to tighten his own conversion and drawing-defense first.

---

## 4. Middlegame and Structure Notes

*Results and engine accuracy are separate evidence types. The table below is the **classical-only**
structure split by Chan's color, because Dino's choices depend on who has White and because the online
games distort the family numbers.*

| Structure family | Chan color | Games | Result % | Moves | ACPL | B/M | Read |
|---|---|---:|---:|---:|---:|---:|---|
| Advance Caro-Kann | Black | 5 | **20.0%** | 162 | 15.0 | 0/3 | Top result target; he defends cleanly, so win by preparation, not cheap blunders |
| Fianchetto KID / Grünfeld | White | 6 | **41.7%** | 165 | 24.1 | 1/5 | Best Black-game target; draw-heavy, 0 wins in 6 |
| Catalan / Réti Squeeze | White | 14 | 67.9% | 469 | 13.5 | 2/5 | Do not allow as Black; strong and clean |
| Catalan / Réti Squeeze | Black | 5 | 60.0% | 168 | 21.6 | 2/0 | Not a classical target (online sample looked worse) |
| Reversed-Sicilian / Flank | Black | 2 | 25.0% | 72 | 24.7 | 1/4 | Uneven result from only a few games; pointer only |
| IQP / Panov Attack | Black | 2 | 50.0% | 52 | 18.7 | 1/1 | Solid; not a target |
| IQP / Panov Attack | White | 1 | 50.0% | 16 | 6.6 | 0/0 | Clean; not a target |

**Practical structure verdicts:**

- **Steer toward with White if trained:** Advance Caro-Kann. The result evidence (20%) and freshness
  (his last two classical losses) are excellent, but he does not blunder there (ACPL 15.0), so Dino
  needs genuine structural understanding, not a trap. Train it first.
- **Steer toward with Black:** his fianchetto KID / Grünfeld White setups (41.7%, 0 wins in 6). The
  realistic aim is to neutralize and outlast - he draws far more than he wins in this structure.
- **Avoid with Black:** giving him a clean Catalan / Réti squeeze (67.9%, ACPL 13.5). This is his
  comfort zone in classical play.
- **Do not overread the online-flavoured families.** His Catalan-as-Black and reversed-Sicilian
  numbers look much worse across all 99 games; the classical subset is far calmer. Use only the
  classical figures above for prep decisions.
- **Anti-Sicilian footnote:** the dossier shows him at 80% in the Anti-Sicilian family (5 games), but
  those are Lichess records without full move lists, so there is no engine confirmation - treat it as
  unconfirmed and avoid relying on it.

---

## 5. Endgame and Simplified Positions

The dossier's classified late-position categories - drawing-defense failure (11), Philidor (11),
rook-behind-pawn (7) - look alarming, but the cleanest samples (vs Rosen, Aslanov, Leiva) come from
**online rapid** events. In the **classical** subset, the endgame ACPL is a respectable **20.8** with
only **8 blunders over 60 games**, so this is **not** a reliable classical grinding target.

What the classical games do show is occasional looseness in **late-middlegame-into-endgame
transitions** around moves 30-38, usually a misplaced rook or a premature pawn break, rather than
textbook rook-ending technique failures. The clearest classical samples:

| Game | Move | Severity | Theme | Engine prefers |
|---|---|---|---|---|
| vs Heberla, Bartlomiej (Rilton Cup, Jan 2026) | 37.cxd7 | blunder | Late collapse after drifting (errs mv 34-37) | Re2xe4 |
| vs Hulka, Valentyn (Sant Boi, Dec 2025) | 33.Ra2 | blunder | Passive rook instead of activating | Ra3-a8 |
| vs Cruz Estrada, Filemon (Sant Boi, Dec 2025) | 32...f5 | blunder | Premature break in a balanced position | Bh3-g4 |
| vs Hari, Madhavan (Singapore, Jun 2025) | 35.Rc6 | blunder | Loose rook move under pressure | d4-d3 |
| vs Prasanth, Bhuvan (Singapore, Jun 2025) | 38...Nc4 | blunder | Knight wander, lost coordination | Re3-c3 |

**The honest phrasing for Dino:** *Chan defends classical endings competently; the dramatic endgame
weakness in the raw numbers is largely from online-speed games. The realistic chance is to keep the
position complex into the first time control (moves 30-40) where his classical samples show occasional
loose, drifting decisions - not to simplify and try to grind a clean rook ending.*

---

## 6. Practical Game Plan for Dino

1. **Keep the game long and classical; do not let it become a speed shuffle.** His error rate roughly
   doubles online and at fast time controls. Pose real problems and make him use the clock, but plan
   to win a long game, not to bank a speed blunder.
2. **Default White plan: KIA vs the French.** If Chan plays 1...e6, this is Dino's tested 91.7%
   weapon and needs no new prep. Highest-confidence path in the whole report.
3. **Conditional White project: Advance Caro-Kann.** If Dino is willing to train it, this is the best
   Chan-specific target - 20% classical result, and his two most recent classical losses are exactly
   here. But Dino has zero reps, and Chan defends it without blundering, so this requires real study,
   not a surprise.
4. **If Chan plays the Sicilian, play a normal game.** Dino's Moscow/Rossolimo is his 100% comfort
   zone, but Chan is strong in the Rossolimo Fianchetto and Taimanov. Aim for a playable middlegame,
   not a theoretical knockout.
5. **As Black, prepare one anti-Catalan/Réti setup.** Deny him the clean fianchetto squeeze he scores
   67.9% with, then steer toward his draw-heavy fianchetto KID structures (41.7%, 0 wins in 6) and
   play the long game.
6. **Do not bank on the endgame.** His classical endgame is clean (ACPL 20.8, 8 blunders / 60). Treat
   simplified positions as roughly equal work, and tighten Dino's own drawing-defense / conversion
   technique before relying on "outplay him later."
7. **Target the move 30-40 zone.** His classical loose moves cluster in the late-middlegame-to-endgame
   transition. Keep enough pieces on to make that phase a real decision, rather than trading into a
   clean ending.
8. **Model games to study:** his two 2026 Advance Caro-Kann losses (vs Ajay Santhosh, Bangkok Apr
   2026; vs Bogdanov, Cannes Feb 2026 - a 28-move loss); his late collapse vs Heberla (Rilton Cup
   Jan 2026, KID Fianchetto); and his Black loss vs Cruz Estrada (Sant Boi Dec 2025, English
   Anglo-Indian).
9. **Freshness to-do before final prep.** He is active (last standard games May 2026) and on the
   Malaysian circuit; mine any 2026 Malaysian-circuit and recent open games to confirm he is still
   defending the Advance Caro-Kann before committing the White project to it.

---

## Method & Caveats

- **Analysis command:** `python prep_manual_app.py --analyze --scope player --player 6 --depth 12 --export`.
- **Coverage:** 134 total games, 99 OTB PGNs, 35 Lichess records without full move lists, 99/99 OTB
  analysed at depth 12, 0 pending.
- **Time-control split:** 60 of the 99 analysed games are classical opens; 39 are online Titled
  Tuesday rapid. All accuracy and structure verdicts above use the classical subset; the all-games
  numbers are shown only to expose how much the online games inflate the blunder and endgame figures.
- **Depth note:** the entire 99-game cache is at depth 12 (verified directly); no stale older-depth
  rows remain for this player.
- **Evidence discipline applied:** every major claim carries a count, score, ACPL, or concrete game
  sample; result targets and engine-accuracy targets are checked against each other (notably the
  Advance Caro-Kann, where a poor result coexists with clean engine defense).
- **Known limitations:** depth 12 is a screening depth, not final engine truth; several targets rest
  on 2-5 game samples; Lichess records without full move lists are opening/result only and are excluded from all engine
  claims; Chan is active, so his freshest 2026 classical games should be re-checked before the round.
