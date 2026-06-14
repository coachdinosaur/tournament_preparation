# Seed Analysis and Report Workflow

*Originally written for the first seed (GM Vignesh); now the general per-seed workflow. The
first-seed specifics below are kept as the worked example. Lessons from later seeds are folded in as
dated, attributed patches.*

## Subject

First seed analyzed: **GM Vignesh, N R**

Roster player ID: `2`

Generated dossier:

`manual_sections/Opponent_GM_Vignesh_N_R.md`

## What Was Analyzed

The app is tournament-specific. It analyzes the fixed roster, not arbitrary uploaded PGNs.

For the first seed, the app used:

- ChessBase PGN games from `chessbasepgn/`
- Lichess tournament-pool metadata from `tournament_pool_2026.db` / CSV
- The roster name matcher in `prep_manual_app.py`
- The bundled opening database in `openings/`
- Stockfish 18 from the sibling `Extract_ZST/stockfish/` folder

The generated Vignesh dossier currently has:

- **187 total games on file**
- **104 over-the-board PGN games**
- **83 Lichess online metadata rows**
- **104/104 analyzable PGN games analyzed by Stockfish**
- **0 pending engine games**
- **Depth 12**

The reason the engine count is `104`, not `187`, is that Lichess rows are metadata-only in this app. They help with opening/repertoire statistics, but they do not include move lists for local engine analysis.

## Command Used

The full per-player analysis command was:

```powershell
python prep_manual_app.py --analyze --scope player --player 2 --depth 12 --export
```

Meaning:

- `--scope player`: analyze one roster player only
- `--player 2`: GM Vignesh, N R
- `--depth 12`: use Stockfish depth 12
- `--export`: regenerate the Markdown manual sections after analysis

## Analysis Pipeline

The app does the analysis in this order:

1. **Scan PGNs**
   - Reads `.pgn` files under the project folder.
   - Matches player names in PGN headers to the fixed roster.
   - Stores games in `prep_manual.db`.

2. **Classify openings**
   - Uses PGN ECO/opening headers when present.
   - Otherwise replays the moves and checks the bundled opening database.
   - Falls back to the built-in opening classifier.

3. **Classify structure families**
   - Tags games against the prep manual's core structure families.
   - Examples: Advance Caro-Kann, Catalan / Reti Squeeze, Anti-Sicilian Counter-Package.

4. **Run engine analysis**
   - Replays each PGN game into FEN positions.
   - Uses Stockfish to evaluate positions.
   - Computes centipawn loss per move.
   - Groups accuracy by phase:
     - Opening
     - Middlegame
     - Endgame

5. **Build player profile**
   - Summarizes opening breadth, strong lines, repair lines, phase accuracy, and weakness categories.
   - Classifies endgame and simplified-position weakness samples.

6. **Export report sections**
   - Writes the updated opponent dossier into `manual_sections/`.

## Current First Seed Findings

### Overall Engine Profile

From the completed depth-12 run:

- **Analyzed games:** 104/104
- **Overall ACPL:** 13.9
- **Opening ACPL:** 7.7
- **Middlegame ACPL:** 11.7
- **Endgame ACPL:** 18.0

Interpretation:

Vignesh is most accurate in the opening phase and least accurate in the endgame phase, but the overall ACPL is still strong. Any report should describe these as relative tendencies, not as broad weaknesses.

### Opening Repertoire

The profile found:

- **128 distinct openings**
- Strong evidence of a broad repertoire
- Strong confidence lines include:
  - Sicilian Defense: Nyezhmetdinov-Rossolimo Attack
  - Rapport-Jobava System
  - English Opening: Agincourt Defense, Neo-Catalan Declined

Repair or target lines currently flagged:

- Caro-Kann Defense: Advance Variation, Tal Variation
- Queen's Gambit Declined: Ragozin Defense, Alekhine Variation

These should be treated as candidate targets, not automatic game-plan choices. Check whether they fit Dino's repertoire before recommending them.

### Structure Targets and Avoids

Engine fingerprint currently flags:

Target structures by lower accuracy:

- IQP / Panov Attack
- Catalan / Reti Squeeze

Structures where he appears solid:

- Advance Caro-Kann
- Fianchetto KID / Grunfeld Complexes

Result-score tables also show that he scores very well in several families, so the final report should balance engine accuracy with practical results.

### Endgame / Simplified-Position Categories

Classified weakness categories:

- Drawing defense failure: 4 samples
- Philidor: 3 samples
- Conversion failure: 2 samples
- Rook activity: 2 samples
- Rook behind pawn: 1 sample

Interpretation:

The report should not say "Vignesh is weak in endgames" broadly. A better phrasing is:

> In the analyzed sample, his least accurate phase is the endgame, with several classified rook-ending and drawing-defense samples. If Dino reaches a simplified rook ending, active-rook and defensive-resource awareness should be treated as practical chances.

## Turning This Into A Report

Use this report structure:

### 1. Executive Summary

Purpose:

Give Dino the short version before detailed prep.

Include:

- Overall strength
- Main repertoire profile
- Main target opportunities
- Main avoid zones
- One practical game-plan sentence

Example:

> Vignesh is a high-accuracy, broad-repertoire GM. His opening accuracy is strong, so the prep should not depend on catching him in a cheap opening trap. The best practical chances are to steer toward selected repair lines and keep pressure into simplified positions, especially rook endings where the sample shows drawing-defense and conversion issues.

### 2. Opening Repertoire

Split into:

- As White
- As Black
- Confidence lines
- Repair lines

For each line, include:

- Opening name
- ECO
- Game count
- Score
- Suggested action: target, avoid, or prepare neutralizer

### 3. Phase Accuracy

Include:

- Overall ACPL
- Opening ACPL
- Middlegame ACPL
- Endgame ACPL

Use plain interpretation:

- Lower ACPL means cleaner play
- Compare phases inside the same player profile
- Do not compare too aggressively across players unless analysis depth and sample sizes match

### 4. Middlegame and Structure Notes

Use:

- Core structure family scores
- Engine fingerprint by family
- Serious error counts

Convert into practical prep:

- Structures to steer toward
- Structures to avoid
- Structures where Dino needs model-game review

### 5. Endgame and Simplified Positions

Use the weakness category table and sample positions.

For each sample:

- Opponent
- Move number
- Mistake type
- Engine-preferred move
- Training theme

Do not overload the report with all samples. Pick the clearest 3 to 5.

### 6. Practical Game Plan For Dino

This should be the final actionable section.

Use bullets like:

- Do not rely on opening surprise only; Vignesh's opening ACPL is low.
- If playing Black, check whether Dino can reach the flagged Caro-Kann Advance / Tal structures safely.
- If playing White, investigate whether Dino can steer toward IQP / Panov or Catalan / Reti structures without entering Vignesh's strongest comfort zones.
- Keep pieces active into rook endings; the sample shows practical chances around Philidor, rook activity, and drawing-defense decisions.
- Prepare 3 model games from his losses or serious engine-error samples.

## Report Quality Rules

Use evidence-based wording:

- Say "the sample shows" instead of "he is bad at".
- Say "candidate target" instead of "guaranteed weakness".
- Include game counts next to repertoire claims.
- Include analysis depth next to engine claims.
- Separate Lichess metadata from OTB PGN engine analysis.

Avoid:

- Overstating personality traits.
- Calling a GM weak based on a small sample.
- Recommending a line Dino does not already understand.
- Mixing result-score targets and engine-accuracy targets without explaining the difference.

## Optimization Notes For Later Seeds

Use this first-seed workflow as the structure for later seeds, not as a source of copied conclusions.
Each seed needs a fresh evidence pass from his own games.

### Current Progress

Completed standalone reports:

- Seed 1: `first_seed_report.md` / `first_seed_report.docx`
- Seed 2: `second_seed_report.md` / `second_seed_report.docx`
- Seed 3: `third_seed_report.md` / `third_seed_report.docx`
- Seed 4: `fourth_seed_report.md` / `fourth_seed_report.docx`
- Seed 5: `fifth_seed_report.md` / `fifth_seed_report.docx`
- Seed 6: `sixth_seed_report.md` / `sixth_seed_report.docx` (player `7`; dossier had a stale 2-game
  depth-16 cache — re-analysed at depth 12 first)
- Seed 7: `seventh_seed_report.md` / `seventh_seed_report.docx` (player `8`; dossier had a stale
  2-of-102 cache — re-analysed first)
- Seed 8: `eighth_seed_report.md` / `eighth_seed_report.docx` (player `9`; dossier had a stale
  15-of-100 cache at depth 16 — re-analysed at depth 12 first. Time-control split: **79 classical /
  21 online** Titled Tuesday; classical-only verdicts. Headline read: a fresh, all-2023–2025 file for
  a **b. 2010 FM** — recency caution *inverts* (likely stronger than the file); weaker as Black
  (44.9%) than White (61.2%), so Dino-White meets his soft side and Dino's e4 weapons — Rossolimo vs
  the Accelerated Dragon, Center Game vs 1...e5 — actually apply. Anti-Sicilian Counter-Package as
  Black 0/2 / ACPL 38.3 is his worst sample and Dino's best domain.)

Current next target:

- Seed 9: **FM Arlan Cabe** — player ID `10`, dossier
  `manual_sections/Opponent_FM_Arlan_Cabe.md`, report stem `ninth_seed_report`.
- **Arlan Cabe exception (do not auto-generate).** Cabe is Dino's coaching partner; his combat file
  is intentionally withheld (0 games on file) and the live scouting confirms it. **Do not create a
  ninth-seed combat report unless the user explicitly asks for one.** With seed 8 done, the curated
  per-seed report run is effectively complete for the eight combatants.

### Seed Queue

Use the app/export order, which is sorted by current roster FIDE rating. In this workspace the
current database player IDs are:

| Seed | Player | Player ID | Dossier | Report stem | Report title |
|---:|---|---:|---|---|---|
| 1 | GM Vignesh, N R | 2 | `manual_sections/Opponent_GM_Vignesh_N_R.md` | `first_seed_report` | `First Seed Report: GM Vignesh, N R` |
| 2 | GM Shyaam, Nikhil P | 3 | `manual_sections/Opponent_GM_Shyaam_Nikhil_P.md` | `second_seed_report` | `Second Seed Report: GM Shyaam, Nikhil P` |
| 3 | IM Morris, James | 104 | `manual_sections/Opponent_IM_Morris_James.md` | `third_seed_report` | `Third Seed Report: IM Morris, James` |
| 4 | IM Tan, Jun Ying | 5 | `manual_sections/Opponent_IM_Tan_Jun_Ying.md` | `fourth_seed_report` | `Fourth Seed Report: IM Tan, Jun Ying` |
| 5 | IM Chan, Kim Yew | 6 | `manual_sections/Opponent_IM_Chan_Kim_Yew.md` | `fifth_seed_report` | `Fifth Seed Report: IM Chan, Kim Yew` |
| 6 | IM Susilodinata, Andrean | 7 | `manual_sections/Opponent_IM_Susilodinata_Andrean.md` | `sixth_seed_report` | `Sixth Seed Report: IM Susilodinata, Andrean` |
| 7 | GM Thejkumar, M. S. | 8 | `manual_sections/Opponent_GM_Thejkumar_M_S.md` | `seventh_seed_report` | `Seventh Seed Report: GM Thejkumar, M. S.` |
| 8 | FM Ang, Ern Jie Anderson | 9 | `manual_sections/Opponent_FM_Ang_Ern_Jie_Anderson.md` | `eighth_seed_report` | `Eighth Seed Report: FM Ang, Ern Jie Anderson` |
| 9 | FM Arlan Cabe | 10 | `manual_sections/Opponent_FM_Arlan_Cabe.md` | `ninth_seed_report` | `Ninth Seed Report: FM Arlan Cabe` |

Player IDs are database IDs, not ordinal seeds. If `prep_manual.db` is rebuilt from scratch, verify
IDs from the app roster before running a player-scoped command. Morris is currently `104` in this
workspace because he was added after older roster rows had already existed.

### Per-Player Analysis Command

Analyze all available games for each seed at the same practical depth used for the first seed.

Examples:

```powershell
# Second seed
python prep_manual_app.py --analyze --scope player --player 3 --depth 12 --export

# Third seed
python prep_manual_app.py --analyze --scope player --player 104 --depth 12 --export

# Fourth seed
python prep_manual_app.py --analyze --scope player --player 5 --depth 12 --export

# Fifth seed
python prep_manual_app.py --analyze --scope player --player 6 --depth 12 --export
```

After the command finishes, verify that the selected player's dossier reports:

- Total games
- OTB PGN games
- Lichess metadata games
- Engine-analyzed games
- Pending games
- Overall ACPL
- Phase ACPL
- Profile confidence lines
- Top weakness categories

If pending games remain, do not hide that in the report. State the coverage directly.

### Depth / Export Consistency Note

The app now resolves engine-depth defaults at call time, so a command such as:

```powershell
python prep_manual_app.py --analyze --scope player --player 6 --depth 12 --export
```

should export dossier text that cites the active depth-12 profile. This matters because older cache
rows at another depth can remain in `GameAnalysis`. If a future dossier prints a depth that does not
match the current run, verify the cache directly before writing the report:

```powershell
@'
import sqlite3
conn = sqlite3.connect("prep_manual.db")
cur = conn.cursor()
player_id = 5  # change for current seed
for row in cur.execute("""
select ga.depth, count(*)
from GameAnalysis ga
join Games g on g.dedup_hash = ga.dedup_hash
where g.player_id = ?
group by ga.depth
order by ga.depth
""", (player_id,)):
    print(row)
'@ | python -
```

Use the complete current-depth run for the curated report, and note any partial older-depth cache
only if it affects interpretation.

### Direct SQLite Query Gotcha

If you query `prep_manual.db` directly for color splits or opening scores, `Games.presult` is stored
from the roster player's perspective as text values:

- `win`
- `draw`
- `loss`

Do **not** query it as PGN-style numeric results such as `presult='1'`, `presult='1/2'`, or
`presult='0'`; that returns zeroed W-D-L counts. Use this scoring expression instead:

```sql
sum(case when presult='win' then 1 when presult='draw' then 0.5 else 0 end)
```

For color-split structure tables, join `Games`, `Tags`, and `GameAnalysis`, then count serious
errors from `blunders_json` only for the roster player's mover (`white` if `Games.color='white'`,
`black` if `Games.color='black'`).

### Patches Folded In From The Fifth-Seed Run (Chan, player 6)

These three things cost real time on the fifth seed because the earlier workflow did not mention
them. Do them up front on every later seed.

#### 1. Split the engine sample by time control — this is mandatory, not optional

The analysed PGN set silently mixes **classical opens** with **online rapid/blitz** events
(ChessBase "Titled Tuesday" PGNs, Lichess blitz). Online error rates run roughly **2x** the
classical rate for the same player, so the all-games ACPL, blunder count, and endgame profile are
inflated and can invent weaknesses that do not exist in classical play. Because the target event is
classical, **base every accuracy and structure verdict on the classical-only subset**, and show the
all-games numbers only to expose the inflation.

Fifth-seed proof: all 99 Chan games read overall ACPL 23.1 / endgame 29.9 / 41 blunders; but 39 were
online Titled Tuesday. The **60 classical** games read overall ACPL **16.1** / endgame **20.8** / **8
blunders** — the correct picture, and it killed two false targets (an "endgame weakness" and a
"Catalan-as-Black volatility" that were both online-only artifacts).

Reusable classifier + split (change `PLAYER`):

```python
import sqlite3, json, re
conn = sqlite3.connect("prep_manual.db"); cur = conn.cursor()
PLAYER = 6
def is_online(ev):
    return bool(re.search(r'titled tuesday|blitz|rapid|online|lichess|chess\.com', ev or "", re.I))
rows = cur.execute("""
  select g.color, g.presult, g.event, ga.phase_json, ga.blunders_json
  from GameAnalysis ga join Games g on g.dedup_hash = ga.dedup_hash
  where g.player_id = ? and ga.depth = 12""", (PLAYER,)).fetchall()
agg = {k: {"g":0,"w":0,"d":0,"l":0,"cp":0.0,"mv":0,"ecp":0.0,"emv":0,"b":0,"m":0}
       for k in ("classical","online")}
for color, res, event, pj, bj in rows:
    a = agg["online" if is_online(event) else "classical"]
    a["g"] += 1; a["w"] += res=="win"; a["d"] += res=="draw"; a["l"] += res=="loss"
    s = (json.loads(pj) if pj else {}).get(color, {})
    for ph in ("op","mid","end"):
        a["cp"] += s.get(ph,[0,0])[0]; a["mv"] += s.get(ph,[0,0])[1]
    a["ecp"] += s.get("end",[0,0])[0]; a["emv"] += s.get("end",[0,0])[1]
    for x in (json.loads(bj) if bj else []):
        if x.get("mover") == color:
            if x["sev"] == "blunder": a["b"] += 1
            elif x["sev"] == "mistake": a["m"] += 1
for k, a in agg.items():
    score = 100.0*(a["w"]+0.5*a["d"])/a["g"] if a["g"] else 0
    acpl  = a["cp"]/a["mv"] if a["mv"] else 0
    eacpl = a["ecp"]/a["emv"] if a["emv"] else 0
    print(f'{k:9} | {a["g"]:2} games ({a["w"]}-{a["d"]}-{a["l"]}, {score:.1f}%) '
          f'| overall ACPL {acpl:.1f} | endgame ACPL {eacpl:.1f} | {a["b"]}b {a["m"]}m')
```

Reuse the same `is_online()` filter when you build the color-split structure table so the structure
verdicts are classical-only too.

#### 2. `GameAnalysis` JSON shapes (so you don't have to inspect them first)

- `phase_json`: `{"white": {"op": [cp_loss, n_moves], "mid": [...], "end": [...]}, "black": {...}}`.
  Phase ACPL for a side = `cp_loss / n_moves`. Overall ACPL = sum of the three `cp_loss` over sum of
  the three `n_moves`, for the roster player's color only.
- `blunders_json`: a list of one dict per flagged move: keys `ply`, `move_no`, `mover`
  (`"white"`/`"black"`), `san`, `sev` (`"blunder"`/`"mistake"`/`"inaccuracy"`), `loss`, `before`,
  `after`, `fen_before`, `fen_after`, `move_uci`, `best_uci`, `best`. Count the roster player's
  serious errors with `mover == <player color>` and `sev in ("blunder","mistake")`. **`loss` is
  centipawns capped at 1500** — mate/huge swings all show as 1500, so do not read a 1500 as an exact
  magnitude or sort model games purely by it.

#### 3. Check the dossier's analysed count before trusting it

The dossier prints `From N analysed game(s) at depth 12`. If `N` is far below the OTB PGN count, the
cache is partial/stale and the profile is garbage — the fifth-seed dossier arrived showing **1 of
99** analysed. Re-run the full `--analyze` pass, then re-read the dossier, before writing anything.

Quick precheck (change `PLAYER`):

```python
import sqlite3
conn = sqlite3.connect("prep_manual.db"); cur = conn.cursor()
PLAYER = 6
otb = cur.execute("select count(*) from Games where player_id=? and (source is null or source not like '%lichess%')",(PLAYER,)).fetchone()[0]
ana = cur.execute("""select count(*) from GameAnalysis ga join Games g on g.dedup_hash=ga.dedup_hash
                     where g.player_id=? and ga.depth=12""",(PLAYER,)).fetchone()[0]
print(f"OTB PGNs: {otb}  analysed@12: {ana}  -> {'RUN ANALYSIS' if ana < otb else 'ok'}")
```

#### 4. Reconcile a poor result against clean engine accuracy

When a line has a bad result score but clean engine ACPL and few blunders (Chan's Advance Caro-Kann:
20% over 5, yet ACPL 15.0 with 0 blunders), the opponent is being **out-prepared / ground down**, not
blundering it away. Frame it as an out-prep target that needs genuine understanding (and a check on
Dino's own reps), not a surprise trap.

### Patches Folded In From The Seventh-Seed Run (Thejkumar, player 8)

Three things bit on the seventh seed that the earlier patches did not fully cover. Do them on every
later seed.

#### 1. `0 Lichess online` does NOT mean `classical-only` — always run the time-control split

Thejkumar's dossier header read *"102 games (102 over-the-board PGN, 0 Lichess online)"*, which looks
like a clean classical file. It is not: **54 of the 102 are online/rapid** (50 chess.com *Titled
Tuesday* + 4 *Pune Rapid*) and only **48 are classical**. The online games hide inside the ChessBase
PGN set, so they never show up in the Lichess count. Run the fifth-seed patch-1 `is_online()` split on
**every** seed regardless of the Lichess number, and widen the regex to catch OTB rapid events too:

```python
def is_online(ev):
    return bool(re.search(r'titled tuesday|blitz|rapid|online|lichess|chess\.com|bullet|arena', ev or "", re.I))
```

Proof of inflation on this seed: all 102 games read 57.4% with a wildly broken engine profile; the
**48 classical** games read **21W 15D 12L (59.4%)** and are the only basis for accuracy/structure
verdicts.

#### 2. Watch for duplicate games imported under two event names

The same OTB game can be stored twice with a different `dedup_hash` when two PGN files spell the
headers differently. Thejkumar's single QID Capablanca loss to Ghosh appears as **both**
`Bangalore op-A 1st (R4)` and `1st Bangalore Int Open (R4.7)` — same date `2024.01.20`, same opponent
(name order flipped), same `0-1 in 56`. Counting both turns one result into a phantom `0/2`. Before
treating any 2-game "target" as two data points, de-dup candidate samples on
`(date, opponent, total_moves)`.

#### 3. Actual DB schema in this workspace (the patch snippets above assume it; confirm if rebuilt)

- Roster table is **`Roster(player_id, real_name, title, federation, fide, is_hero)`** — there is no
  `Players` table and no `id` column. Look up a seed by `player_id`.
- Engine cache is **`GameAnalysis`** keyed by `dedup_hash`: columns `depth, engine, analyzed_at,
  acpl_white, acpl_black, moves_white, moves_black, phase_json, blunders_json`. Join to `Games` on
  `dedup_hash`. The `phase_json` / `blunders_json` shapes are exactly as documented in fifth-seed
  patch 2 (verified again here).
- Structure families are **`Tags(game_id, family)`** — join on `Games.game_id`, not `dedup_hash`.
  Note family strings can carry mojibake (`Gr�nfeld`, `R�ti`); match on a substring, not equality.
  A game can carry **several** family tags; count it in **each** (the dossier convention), not just one.

### Accuracy & Efficiency Upgrades (2026-06-14, from the seed 6–7 runs)

These change *how* you run a seed, not just what to watch for. Adopt them from the eighth seed on.

#### A. Run the evidence pack with one script — `seed_evidence.py`

Every field the report needs — coverage, time-control split, recency histogram, color-split opening
tables, classical phase ACPL, structure ACPL by family, late-blunder samples, classical model losses,
and duplicate-game detection — now comes from a single read-only script:

```powershell
python seed_evidence.py <player_id> --depth 12
```

It encodes the real schema and the classical-only verdict rule, so you stop re-typing and re-adapting
the snippets scattered through this file (those remain only as reference). It is **read-only**, so it
is safe to run while a *different* player's `--analyze` is in flight. Validated against the seventh
seed: its structure-ACPL table reproduces the hand-built numbers exactly.

#### B. Overlap the slow engine pass — analyze first, gather in parallel

The dossier almost always ships with a **stale/partial engine cache** (seed 5: 1/99; seed 7: 2/102 at
depth 12; seed 6: 2/101 at depth **16**), so a full `--analyze` is effectively mandatory every seed and
is the dominant wall-clock cost (~100 games × depth 12, single-threaded writer). Don't sit idle:

1. Kick off `--analyze … --player N --depth 12 --export` **in the background first**.
2. While it runs, read the opponent's **`Live_Scouting_*` entry** and run the **result-only** parts of
   `seed_evidence.py` (coverage / TC-split / recency / openings / model-losses need no engine data).
3. You may also **write report N's prose while seed N+1 analyses** — but **never run two `--analyze`
   passes at once**: the DB is a single writer with only an 8 s `busy_timeout`, so concurrent passes
   risk lock failures. Serialise the engine; pipeline the writing.

#### C. Two new accuracy rules

- **Recency weighting.** A career PGN file can span decades. Seed 6 (Susilodinata) includes **18
  pre-2010 junior games** (W-ch U12/U14, 2002–2004 — even a loss to a 12-year-old Carlsen). Those say
  nothing about a 2026 IM's prep. `seed_evidence.py` prints a by-year histogram and a pre-2010 flag;
  base "what he'll actually play" and any freshness claim on the **last ~3–5 years**, and explicitly
  down-weight or segregate the ancient games. Never average a 2002 result into a 2026 target.
- **Read Live Scouting *first*; let activity override the PGN percentages.** The single most important
  fact about seed 7 (Thejkumar inactive ~2 years, now coaching, OTB rust expected) exists **only** in
  `Live_Scouting_*`, not the dossier. Make the scouting entry **Step 0**: an inactive/active flag, a
  rating conflict, or a freshness note can reshape the whole plan before you read a single opening row.

#### D. Dino-weapon applicability check (accuracy)

Before recommending any of Dino's weapons, confirm it can **occur** given the opponent's actual
repertoire. Seed 7 was a Caro-Kann / 1.d4 player, so Dino's headline weapons (Moscow/Rossolimo vs the
Sicilian, KIA vs the French) were **all moot** — the White game was a Caro-Kann battle he is barely
booked for. Cross the opponent's color-split openings against Dino's `Needs_Improvement` file and only
recommend lines the pairing can actually reach.

#### E. Engine throughput (optional; verify before committing)

On this 4-core box the engine runs `ENGINE_THREADS = 2`, `ENGINE_HASH_MB = 128`; testing `Threads = 4`
/ `Hash = 256` should cut wall-clock per pass. `ENGINE_DEPTH` also **defaults to 16** — which is why
stale caches surface depth-16 rows — so always pass `--depth 12` explicitly (this workflow already
does). The bigger win is a **code change**: `analyze_all` has no time-control filter and OTB `Games`
rows carry no `time_control` column, so the engine analyses the online half it later discards (seed 7:
54 of 102 games). Adding an event-regex *classical-only* filter to the player scope would roughly halve
the pass on online-heavy files. Recommend, don't silently implement.

### Reusable Report Checklist

For each seed, collect the same fixed evidence fields before writing prose:

- Game coverage: total games, OTB PGNs, Lichess metadata, analyzed count, pending count. Confirm the
  analysed count matches the OTB count before trusting the dossier (see fifth-seed patch 3).
- Time-control split: classical vs online (Titled Tuesday / blitz). Base verdicts on the classical
  subset; show all-games numbers only to expose inflation (see fifth-seed patch 1).
- Opening profile: strongest lines, candidate weak lines, color split, and sample counts.
- Phase profile: opening, middlegame, and endgame ACPL with mistake counts (classical subset).
- Practical repair lines: what Dino should review or avoid before the game.
- Structure targets: structures Dino can realistically reach from his current repertoire.
- Structure avoids: lines where the opponent's sample looks too clean or too comfortable.
- Endgame profile: top weakness categories and 3 to 5 clean sample positions.
- Confidence notes: high, medium, or low confidence for each major claim.

### Writing Rules For Later Seeds

- Do not copy another player's opening or endgame conclusions into the current report.
- Keep all labels evidence-based: every strength, weakness, or tendency needs a number, sample count, phase score, or concrete game example.
- Separate engine-analyzed OTB PGNs from Lichess metadata.
- Include the engine depth near tactical or accuracy claims.
- Prefer "candidate target" and "sample suggests" when the evidence is limited.
- Tie recommendations to Dino's actual preparation, not to abstract engine preferences.

### DOCX Reuse

Use the reusable root builder only. Do not copy the embedded Python block later in this file:

```powershell
python -X utf8 build_standalone_report.py second_seed_report.md second_seed_report.docx --title "Second Seed Report: GM Shyaam, Nikhil P"
python -X utf8 build_standalone_report.py third_seed_report.md third_seed_report.docx --title "Third Seed Report: IM Morris, James"
python -X utf8 build_standalone_report.py fourth_seed_report.md fourth_seed_report.docx --title "Fourth Seed Report: IM Tan, Jun Ying"
python -X utf8 build_standalone_report.py fifth_seed_report.md fifth_seed_report.docx --title "Fifth Seed Report: IM Chan, Kim Yew"
```

The embedded DOCX builder below is stale historical reference only. Do not copy from it. Run
`build_standalone_report.py` so each seed report uses the maintained implementation.

## Producing the Report Files (Markdown + Standalone DOCX)

Each seed report ships as **two files at the repo root**:

1. `<seed>_report.md` — the curated 6-section report (see *Turning This Into A Report* above).
2. `<seed>_report.docx` — the **same** report as a standalone Word file, formatted in this manual's
   style (same fonts, heading styles, bullets, bordered tables).

> **Do not modify `Tournament_Preparation_Manual.docx`.** The standalone `.docx` only *borrows* the
> manual's look by opening it as a **read-only style template**; the manual file itself is never
> written to. "Format it like the manual" — not "append it to the manual."

### Step 1 — Write the curated Markdown

Author `<seed>_report.md` following the 6-section structure and the Report Quality Rules above.

### Step 2 — Generate the standalone DOCX

Needs `python-docx` (already installed; otherwise `pip install python-docx`). The reusable builder
now lives at `build_standalone_report.py` in the project root. It defaults to the second-seed file
names, but accepts explicit input/output paths and a running-header title:

```powershell
python -X utf8 build_standalone_report.py second_seed_report.md second_seed_report.docx --title "Second Seed Report: GM Shyaam, Nikhil P"
```

For the first seed, run:

```powershell
python -X utf8 build_standalone_report.py first_seed_report.md first_seed_report.docx --title "First Seed Report: GM Vignesh, N R"
```

For the current next seed after Tan, run:

```powershell
python -X utf8 build_standalone_report.py fifth_seed_report.md fifth_seed_report.docx --title "Fifth Seed Report: IM Chan, Kim Yew"
```

The original embedded builder is kept below as a historical snapshot only. Do not copy from it for
new seed reports; the authoritative implementation is `build_standalone_report.py` at the project
root.

### Step 3 — Render-check the DOCX on Windows

The final DOCX should be visually checked by rendering it to page PNGs. On Windows this needs:

- LibreOffice (`soffice.com` / `soffice.exe`)
- Poppler (`pdftoppm.exe`, and usually `pdfinfo.exe`)
- Python package `pdf2image` if using the bundled renderer

**Current workspace render rule from the fourth-seed run:** use the explicit `soffice.com` +
`pdftoppm.exe` manual path below. The packaged Documents `render_docx.py` path did not work reliably
in this chat:

- First attempt failed because `soffice` / `pdftoppm` were not on `PATH`, even though they were
  installed.
- Prepending `C:\Program Files\LibreOffice\program` to `PATH` before running plain `python` caused
  `python` to resolve to LibreOffice's bundled Python, which then failed with
  `ModuleNotFoundError: No module named 'pdf2image'`.
- Running the packaged renderer with explicit CPython 3.11 found `pdf2image`, but LibreOffice exited
  with `Failed to produce PDF for rasterization (direct and ODT fallback)`.
- The direct Windows command using `soffice.com` converted the DOCX successfully, and Poppler
  generated all page PNGs. Prefer that path for later seed reports.

Install checks:

```powershell
# In PowerShell, use where.exe. Plain "where" can resolve as a PowerShell alias.
where.exe soffice
where.exe pdfinfo
where.exe pdftoppm
python -m pip show pdf2image
```

If the tools were just installed but the current shell still cannot see them, either reopen
PowerShell or refresh the current process PATH:

```powershell
$env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' +
            [Environment]::GetEnvironmentVariable('Path','User')
where.exe soffice
where.exe pdfinfo
where.exe pdftoppm
```

If `winget` is installed but not on PATH, call it directly:

```powershell
& "$env:LOCALAPPDATA\Microsoft\WindowsApps\winget.exe" install --id TheDocumentFoundation.LibreOffice -e --accept-source-agreements --accept-package-agreements
& "$env:LOCALAPPDATA\Microsoft\WindowsApps\winget.exe" install --id oschwartz10612.Poppler -e --accept-source-agreements --accept-package-agreements
python -m pip install --user pdf2image
```

Expected persistent PATH entries after install:

- `C:\Program Files\LibreOffice\program`
- Poppler's winget package bin folder, usually:
  `C:\Users\Admin\AppData\Local\Microsoft\WinGet\Packages\oschwartz10612.Poppler_Microsoft.Winget.Source_8wekyb3d8bbwe\poppler-25.07.0\Library\bin`
- `C:\Users\Admin\AppData\Local\Microsoft\WindowsApps` for `winget.exe`

If a newly installed tool is still not visible, use explicit paths for the current session. This is
the Windows-safe manual render path. Change `$report` for the current seed:

```powershell
$report = "fifth_seed_report"   # change to the current report stem
$out = Join-Path (Get-Location) "${report}_render"
New-Item -ItemType Directory -Force -Path $out | Out-Null

& "C:\Program Files\LibreOffice\program\soffice.com" --headless --norestore --convert-to pdf --outdir $out (Join-Path (Get-Location) "${report}.docx")

$popplerBin = Get-ChildItem "$env:LOCALAPPDATA\Microsoft\WinGet\Packages" -Recurse -Filter pdftoppm.exe |
  Select-Object -First 1 -ExpandProperty DirectoryName
& (Join-Path $popplerBin "pdftoppm.exe") -png -r 144 (Join-Path $out "${report}.pdf") (Join-Path $out "page")
```

LibreOffice may print `Could not find platform independent libraries <prefix>` after a successful
manual conversion. Treat that as harmless if `${report}.pdf` and all expected `page-*.png` files
exist and the PNGs pass visual inspection.

Then inspect every generated `page-*.png`. Do not ship the DOCX if a table row is split awkwardly,
text is clipped, page headers/footers are misplaced, or a table starts with only a stranded header
row at the bottom of a page. Render artifacts are QA scratch files; delete them unless they are
explicitly needed.

> **Stale snapshot warning:** The embedded Python block below is an outdated snapshot kept for
> historical reference only. The authoritative implementation is `build_standalone_report.py` at the
> project root: always run that script, and never copy from the block below.
>
> Known divergences from the live script:
>
> - The embedded block has hardcoded `MD` / `OUT` / `HEADER_NEW` config lines; the live script uses
>   argparse positional paths plus `--title`, and can infer the title from the Markdown H1.
> - The embedded block has a `bullet_is_real()` branch and literal bullet fallback; the live script
>   always emits real Word bullets.
> - The embedded block's `style_table` only sets borders and a bold header; the live script adds
>   per-column widths, cell margins, `cantSplit` rows, repeating header rows, and 9pt table text.
> - The embedded block only sets `run.font.name` for monospace text; the live script also sets
>   `w:rFonts` `ascii` and `hAnsi` to keep the rendered font stable.

```python
#!/usr/bin/env python
"""Render <seed>_report.md as a standalone <seed>_report.docx, styled from the Tournament
Preparation Manual (used READ-ONLY as a template). The manual itself is never modified."""
import re
from pathlib import Path
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

ROOT = Path(__file__).resolve().parent

# ===== CONFIG — change these three lines per seed =====
MD         = ROOT / "first_seed_report.md"
OUT        = ROOT / "first_seed_report.docx"
HEADER_NEW = "First Seed Report: GM Vignesh, N R"     # replaces the manual's running-header title
# ======================================================

TEMPLATE     = ROOT / "Tournament_Preparation_Manual.docx"   # read-only style template; never written
HEADER_OLD   = "Tournament Preparation Manual"
BULLET_NUMID = 2

LINK_RE = re.compile(r'\[([^\]]+)\]\([^)]*\)')
def strip_links(s): return LINK_RE.sub(r'\1', s)

# ---- recursive inline parser: **bold**, *italic*, `code` (code may nest in emphasis) ----
def _fmt(b, i, m):
    d = {}
    if b: d["bold"] = True
    if i: d["italic"] = True
    if m: d["mono"] = True
    return d
def _emit(text, bold, italic, out):
    while text:
        m = re.search(r'(\*\*|\*|`)', text)
        if not m:
            out.append((text, _fmt(bold, italic, False))); return
        if m.start() > 0:
            out.append((text[:m.start()], _fmt(bold, italic, False)))
        mk = m.group(1); rest = text[m.end():]
        if mk == '`':
            j = rest.find('`')
            if j < 0: out.append(('`' + rest, _fmt(bold, italic, False))); return
            out.append((rest[:j], _fmt(bold, italic, True))); text = rest[j+1:]
        elif mk == '**':
            j = rest.find('**')
            if j < 0: out.append(('**' + rest, _fmt(bold, italic, False))); return
            _emit(rest[:j], True, italic, out); text = rest[j+2:]
        else:
            j = rest.find('*')
            if j < 0: out.append(('*' + rest, _fmt(bold, italic, False))); return
            _emit(rest[:j], bold, True, out); text = rest[j+1:]
def inline_runs(text):
    text = strip_links(text).replace("⚠️", "").replace("⚠", "").strip()
    out = []; _emit(text, False, False, out)
    return out or [("", {})]

# ---- block parser (handles hard-wrapped list items / paragraphs) ----
def cells(row):
    row = row.strip()
    if row.startswith("|"): row = row[1:]
    if row.endswith("|"): row = row[:-1]
    return [c.strip() for c in row.split("|")]
def is_block_start(line):
    s = line.strip()
    if not s: return True
    if re.match(r'#{1,6}\s', s): return True
    if s.startswith(("|", ">")): return True
    if re.fullmatch(r'-{3,}', s): return True
    if re.match(r'-\s+', s) or re.match(r'\d+\.\s+', s): return True
    return False
def collect_cont(lines, i):
    n = len(lines); buf = []
    while i < n and not is_block_start(lines[i]):
        buf.append(lines[i].strip()); i += 1
    return " ".join(x for x in buf if x), i
def is_sep(line):
    s = line.strip()
    return bool(s) and set(s) <= set("|:- ") and "-" in s
def parse_blocks(md):
    lines = md.split("\n"); blocks = []; i = 0; n = len(lines)
    while i < n:
        s = lines[i].rstrip()
        if not s.strip(): i += 1; continue
        if re.fullmatch(r'-{3,}', s.strip()): i += 1; continue
        m = re.match(r'(#{1,6})\s+(.*)', s)
        if m: blocks.append(("h", len(m.group(1)), m.group(2).strip())); i += 1; continue
        if s.lstrip().startswith("|") and i+1 < n and is_sep(lines[i+1]):
            tbl = [s]; sep = lines[i+1]; j = i + 2
            while j < n and lines[j].lstrip().startswith("|"): tbl.append(lines[j]); j += 1
            aligns = ["center" if c.startswith(":") and c.endswith(":") else "right" if c.endswith(":") else "left"
                      for c in cells(sep)]
            blocks.append(("table", cells(tbl[0]), aligns, [cells(r) for r in tbl[1:]])); i = j; continue
        if s.lstrip().startswith(">"):
            q = []
            while i < n and lines[i].lstrip().startswith(">"):
                q.append(re.sub(r'^\s*>\s?', '', lines[i])); i += 1
            blocks.append(("quote", " ".join(x.strip() for x in q if x.strip()))); continue
        m = re.match(r'\s*-\s+(.*)', s)
        if m:
            extra, i = collect_cont(lines, i + 1)
            blocks.append(("bullet", (m.group(1).strip() + " " + extra).strip())); continue
        m = re.match(r'\s*(\d+)\.\s+(.*)', s)
        if m:
            extra, i = collect_cont(lines, i + 1)
            blocks.append(("number", m.group(1), (m.group(2).strip() + " " + extra).strip())); continue
        extra, i = collect_cont(lines, i + 1)
        blocks.append(("p", (s.strip() + " " + extra).strip()))
    return blocks

def bullet_is_real(doc):
    try: numbering = doc.part.numbering_part.element
    except Exception: return False
    num = next((e for e in numbering.findall(qn('w:num')) if e.get(qn('w:numId')) == str(BULLET_NUMID)), None)
    if num is None: return False
    absId = num.find(qn('w:abstractNumId')).get(qn('w:val'))
    for ab in numbering.findall(qn('w:abstractNum')):
        if ab.get(qn('w:abstractNumId')) == absId:
            for lvl in ab.findall(qn('w:lvl')):
                if lvl.get(qn('w:ilvl')) == "0":
                    nf = lvl.find(qn('w:numFmt'))
                    return nf is not None and nf.get(qn('w:val')) == "bullet"
    return False

# ---- builders ----
def add_runs(p, runs):
    for text, f in runs:
        r = p.add_run(text)
        if f.get("bold"):   r.bold = True
        if f.get("italic"): r.italic = True
        if f.get("mono"):   r.font.name = "Consolas"
    return p
def set_pstyle(p, style_id):
    pPr = p._p.get_or_add_pPr()
    ex = pPr.find(qn('w:pStyle'))
    if ex is not None: pPr.remove(ex)
    e = OxmlElement('w:pStyle'); e.set(qn('w:val'), style_id); pPr.insert(0, e)
def set_bullet(p):
    pPr = p._p.get_or_add_pPr()
    numPr = OxmlElement('w:numPr')
    il = OxmlElement('w:ilvl'); il.set(qn('w:val'), "0"); numPr.append(il)
    nid = OxmlElement('w:numId'); nid.set(qn('w:val'), str(BULLET_NUMID)); numPr.append(nid)
    pPr.append(numPr)
def style_table(tbl):
    tblPr = tbl.tblPr
    w = OxmlElement('w:tblW'); w.set(qn('w:type'), 'dxa'); w.set(qn('w:w'), '9360'); tblPr.append(w)
    b = OxmlElement('w:tblBorders')
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        e = OxmlElement('w:' + edge); e.set(qn('w:val'), 'single')
        e.set(qn('w:color'), 'auto'); e.set(qn('w:sz'), '4'); b.append(e)
    tblPr.append(b)

# ---- main ----
doc = Document(str(TEMPLATE))
real_bullets = bullet_is_real(doc)

# resolve style IDs from the template body (apply by ID, not display name)
defined_ids = {s.style_id for s in doc.styles if s.style_id}
level_to_id = {}; list_id = "ListParagraph"
for p in doc.paragraphs:
    nm = p.style.name if p.style else ""
    pPr = p._p.find(qn('w:pPr')); ps = pPr.find(qn('w:pStyle')) if pPr is not None else None
    if ps is None: continue
    sid = ps.get(qn('w:val'))
    if nm.startswith("Heading"):
        lvl = nm.replace("Heading", "").strip()
        if lvl.isdigit(): level_to_id.setdefault(int(lvl), sid)
    elif nm == "List Paragraph": list_id = sid
title_id = "Title" if "Title" in defined_ids else level_to_id.get(1, "Heading1")
def style_for(report_level):
    if report_level == 1: return title_id            # report H1 -> Title
    t = report_level - 1                             # report H2 -> Heading1, H3 -> Heading2 ...
    return level_to_id.get(t) or (("Heading%d" % t) if ("Heading%d" % t) in defined_ids else level_to_id.get(1, "Heading1"))

# clear the body but keep the trailing section properties (page setup + header/footer refs)
body = doc.element.body
sectPr = body.find(qn('w:sectPr'))
for child in list(body):
    if child.tag in (qn('w:p'), qn('w:tbl')): body.remove(child)

def emit_para():
    p = doc.add_paragraph(); sectPr.addprevious(p._p); return p
def emit_table(rows, cols):
    t = doc.add_table(rows=rows, cols=cols); sectPr.addprevious(t._tbl); return t

for blk in parse_blocks(MD.read_text(encoding="utf-8")):
    kind = blk[0]
    if kind == "h":
        p = emit_para(); set_pstyle(p, style_for(blk[1])); add_runs(p, inline_runs(blk[2]))
    elif kind == "p":
        add_runs(emit_para(), inline_runs(blk[1]))
    elif kind == "bullet":
        p = emit_para(); set_pstyle(p, list_id)
        if real_bullets: set_bullet(p); add_runs(p, inline_runs(blk[1]))
        else: add_runs(p, [("•  ", {})] + inline_runs(blk[1]))
    elif kind == "number":
        p = emit_para(); set_pstyle(p, list_id)
        add_runs(p, [(blk[1] + ".  ", {})] + inline_runs(blk[2]))
    elif kind == "quote":
        p = emit_para()
        add_runs(p, [(t, {**f, "italic": True}) for t, f in inline_runs(blk[1])])
        p.paragraph_format.left_indent = Pt(18)
    elif kind == "table":
        header, aligns, rows = blk[1], blk[2], blk[3]; nc = len(header)
        tbl = emit_table(len(rows) + 1, nc)
        for c, h in enumerate(header):
            add_runs(tbl.cell(0, c).paragraphs[0], [(strip_links(h), {"bold": True})])
        for ri, row in enumerate(rows):
            for c in range(nc):
                cp = tbl.cell(ri + 1, c).paragraphs[0]
                add_runs(cp, inline_runs(row[c] if c < len(row) else ""))
                if aligns[c] == "right":  cp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                elif aligns[c] == "center": cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        style_table(tbl._tbl)

# relabel the inherited running header so the standalone file isn't titled as the whole manual
for sec in doc.sections:
    for p in sec.header.paragraphs:
        for r in p.runs:
            if HEADER_OLD in r.text:
                r.text = r.text.replace(HEADER_OLD, HEADER_NEW)

doc.save(str(OUT))
print("saved ->", OUT.name)
```

### How it works (and the gotchas that matter when duplicating)

> These bullets describe the embedded historical snapshot, not the current script. For current
> behavior, see `build_standalone_report.py`: it always uses real Word bullets and does substantially
> more table work, including per-column widths, cell margins, `cantSplit`, repeating header rows,
> and 9pt table text, which is what satisfies the render-QA requirements above.

- **Manual as a read-only template.** Opens the manual, clears its body in memory (removing every
  paragraph/table but keeping the trailing `w:sectPr`, so page setup + header/footer survive), then
  renders the report before that `sectPr`. The output inherits the manual's fonts, heading styles,
  bullet list and table look. The manual on disk is never saved.
- **Apply styles by styleId, not display name.** The manual has duplicate latent heading styles, so
  `style="Heading 1"` raises `KeyError`. The script reads the body's real style IDs and maps report
  **H1 → Title, H2 → Heading 1, H3 → Heading 2**.
- **Bullets** reuse the manual's bullet list (`numId=2`); **tables** get full-width single-line
  borders, a bold header row, and right-aligned numeric columns.
- **Hard-wrapped Markdown is handled.** The parser merges multi-line (wrapped) list items and
  paragraphs, so wrapping in the `.md` never splits a bullet or breaks an inline `code` span.
- **Header is relabeled** so the standalone file doesn't claim to be the whole manual.

### Duplicating for the next seed

Do not edit copied CONFIG lines anymore. Use the root builder with explicit arguments:

```powershell
python -X utf8 build_standalone_report.py fifth_seed_report.md fifth_seed_report.docx --title "Fifth Seed Report: IM Chan, Kim Yew"
```

## Next Player Workflow

When one seed report is complete, meaning the Markdown is written, the DOCX is generated, and the
rendered `page-*.png` files pass visual QA, advance to the next row in the queue:

| If just completed | Next target | Command | Report files |
|---|---|---|---|
| Second seed, Shyaam | Third seed, Morris | `python prep_manual_app.py --analyze --scope player --player 104 --depth 12 --export` | `third_seed_report.md` / `third_seed_report.docx` |
| Third seed, Morris | Fourth seed, Tan | `python prep_manual_app.py --analyze --scope player --player 5 --depth 12 --export` | `fourth_seed_report.md` / `fourth_seed_report.docx` |
| Fourth seed, Tan | Fifth seed, Chan | `python prep_manual_app.py --analyze --scope player --player 6 --depth 12 --export` | `fifth_seed_report.md` / `fifth_seed_report.docx` |
| Fifth seed, Chan | Sixth seed, Susilodinata | `python prep_manual_app.py --analyze --scope player --player 7 --depth 12 --export` | `sixth_seed_report.md` / `sixth_seed_report.docx` |
| Sixth seed, Susilodinata | Seventh seed, Thejkumar | `python prep_manual_app.py --analyze --scope player --player 8 --depth 12 --export` | `seventh_seed_report.md` / `seventh_seed_report.docx` |
| Seventh seed, Thejkumar | Eighth seed, Ang | `python prep_manual_app.py --analyze --scope player --player 9 --depth 12 --export` | `eighth_seed_report.md` / `eighth_seed_report.docx` |
| Eighth seed, Ang | Ninth seed, Arlan Cabe | `python prep_manual_app.py --analyze --scope player --player 10 --depth 12 --export` | `ninth_seed_report.md` / `ninth_seed_report.docx` |

For the immediate next seed after Tan, run:

```powershell
python prep_manual_app.py --analyze --scope player --player 6 --depth 12 --export
```

Then review:

```text
manual_sections/Opponent_IM_Chan_Kim_Yew.md
```

Repeat one player at a time so each dossier becomes complete and easy to verify. Then produce that
seed's two report files (`fifth_seed_report.md` + `fifth_seed_report.docx`) with the steps in
*Producing the Report Files* above.

**Arlan Cabe exception:** the app keeps FM Arlan Cabe in the roster for completeness, but the manual
notes that his combat file is intentionally withheld. Do not create a ninth-seed combat report unless
the user explicitly asks for one.
