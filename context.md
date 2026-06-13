# `prep_manual_app.py` — Context & Architecture

A single-file, zero-dependency (Python 3.10+ standard library only) local web app that builds
the **2026 Tournament Preparation Manual** for **FM Dino Ballecer** ("Coach Dinosaur"), who is
playing a 10-player closed round-robin. It ingests PGN game databases for Dino and his 9
opponents, classifies every game by opening and by one of six "Core Structure Families,"
produces per-opponent dossiers and a self-audit for Dino, and exports Markdown sections ready to
paste into `Tournament_Preparation_Manual.docx`.

Everything (server, analysis engine, database layer, and the entire front-end) lives in the one
file [prep_manual_app.py](prep_manual_app.py). No internet access is required at runtime; the
browser UI is served locally and uses only vanilla JS.

---

## 1. How to run it

```bash
python prep_manual_app.py                 # scan + serve UI at http://localhost:8765 (opens browser)
python prep_manual_app.py --port 9000      # custom port
python prep_manual_app.py --no-browser     # serve but don't auto-open a browser
python prep_manual_app.py --export         # headless: scan + write manual_sections/*.md, then exit
python prep_manual_app.py --scan-only       # headless: scan the DB and exit (no server, no export)
```

On every startup `main()` runs `init_db()` then a full `scan(conn)`, prints a per-player game
count table, and (unless `--export`/`--scan-only`) starts a `ThreadingHTTPServer` bound to
`127.0.0.1`. `sys.stdout` is reconfigured to UTF-8 so the Unicode roster/board characters print
on Windows consoles.

### Key paths (module constants, top of file)
| Constant | Meaning |
|---|---|
| `BASE_DIR` | Folder containing the script — the PGN scan root. |
| `DB_PATH` | `prep_manual.db` (SQLite, auto-created/rebuilt). |
| `EXPORT_DIR` | `manual_sections/` — where Markdown exports are written. |
| `LICHESS_DB` / `LICHESS_CSV` | `tournament_pool_2026.db` / `..._Games.csv` — optional online scout data produced by a separate `lichess_tournament_prep.py`. |
| `DEFAULT_PORT` | `8765`. |

---

## 2. The roster

`ROSTER` (a list of dicts) is the source of truth: **Dino (the "hero") + 9 opponents**, each with
`real_name`, `title`, `federation`, `fide`, `is_hero`. `HERO_NAME = "Dino Ballecer"` and
`HERO_ALIASES` seed the name-matcher so his own games attach even when a PGN spells him
differently ("Coach Dinosaur", "Ballecer, Dino", …).

`init_db()` upserts every `ROSTER` row into the `Roster` table (keyed on `real_name`) and then
**prunes** any `Roster` row whose `real_name` is no longer in `ROSTER` — so removing a player from
the list cleanly deletes them (and their games cascade) on the next run. This is what removes the
formerly-mistaken "IM Vignesh, Advaith Vemula" entry now that the roster lists "IM Morris, James"
instead.

### Name spelling bridges — `ROSTER_ALIASES`
ChessBase PGN exports sometimes compress initials or vary spelling in a way the token matcher
(see §7) can't bridge on its own (it needs ≥2 shared name tokens). `ROSTER_ALIASES` maps the raw
**lower-cased PGN header string** → roster `real_name`, and `init_db()` seeds those into the
`Aliases` table so the games attach on scan. Current entries:

| PGN header (as exported) | Roster player |
|---|---|
| `shyam,nikil p` | GM Shyaam, Nikhil P |
| `thejkumar,ms.` | GM Thejkumar, M. S. |
| `vignesh,nr.` | GM Vignesh, N R |

Without these, those three would land in the "Unmatched Names" list instead of attaching.

---

## 3. The six Core Structure Families

A prep concept from the manual's Part III. Every game is tagged with zero or more of these
families (constants `FAM_*`, collected in `ALL_FAMILIES`):

1. **Advance Caro-Kann**
2. **Reversed-Sicilian / Flank Annexation**
3. **Fianchetto KID / Grünfeld Complexes**
4. **Catalan / Réti Squeeze**
5. **Anti-Sicilian Counter-Package**
6. **IQP / Panov Attack**

These drive the "structure-family record" rows in dossiers and the targeting/avoidance pointers in
the exports.

---

## 4. Mini chess engine (`MiniBoard`)

Because OTB PGNs frequently lack `[ECO]`/`[Opening]` headers and FEN data, the app replays the
moves itself.

- `MiniBoard` holds an 8×8 board as a 64-char list, side to move, castling rights, en-passant
  square, and full-move counter.
- `push_san(san)` applies one SAN move: handles castling, captures, promotions, en passant,
  disambiguation (file/rank), and uses `_attacked()` / `_king_sq()` to resolve ambiguous moves by
  legality (it makes/unmakes candidate moves to discard those leaving the king in check).
- `fen()` serializes the position to a FEN string.
- `fens_for(moves)` returns `([start_fen, fen_after_ply1, …], error_or_None)`; on an illegal/
  unparseable move it stops gracefully and returns the partial FEN list plus an error message
  (surfaced in the board viewer as `replay_error`).

These FENs feed the UI replayer, the bundled **opening-database classification**, and the optional
**Stockfish analysis** (both in §15) — `MiniBoard` is not a legality-checking referee for arbitrary
input.

---

## 5. PGN parsing

- `split_pgn_stream(raw)` splits a multi-game PGN file into individual game blocks (new block
  starts at each `[Event ` tag).
- `clean_movetext(text)` strips comments `{…}`, recursive variations `(…)`, NAGs `$n`, move
  numbers, and result tokens, leaving a flat list of SAN moves (also trims `?!` annotations).
- `parse_pgn_game(pgn)` returns `{"headers": {...}, "moves": [...]}` (or `None` if no headers).

Files are read as `utf-8-sig` with `errors="replace"` so BOMs and odd encodings don't crash the
scan.

---

## 6. Opening classification (move-based)

`BOOK` is a large hand-built list of `(move-sequence-prefix, opening name, ECO)` triples covering
Sicilians, Caro-Kann, French, 1.e4 e5 systems, 1.d4 complexes, English/Réti/flank openings, etc.
It is normalized (check marks stripped) and sorted **longest-prefix-first**.

`classify_opening(moves)` takes the first 14 plies, finds the longest `BOOK` prefix that matches,
and returns `(name, eco)`. It then applies a couple of feature refinements for transpositional
systems (e.g. detecting a Catalan from the `{d4, c4, g3}` pawn skeleton, or a London System when
`Bf4` appears early). Falls back to `("Irregular Opening", "A00")`.

**Preferred path (since the engine/opening-DB layer, §15):** `scan()` now calls
`classify_opening_db(fens)` first — a FEN lookup against the bundled Lichess opening database — and
only falls back to `BOOK` when the DB has no hit or isn't present. A PGN's own `ECO`/`Opening`
headers still win when present. This is why stored openings are now specific (e.g. *"Sicilian
Defense: Nyezhmetdinov-Rossolimo Attack, Fianchetto Variation"* with an accurate ECO) rather than a
coarse `BOOK` label.

`tag_families(moves, eco, opening)` tags a game against the six families using **both** the move
stream (pawn-skeleton / move-order heuristics over the first ~30 plies) **and** a header fallback
(ECO ranges + opening-name keywords) so that move-less Lichess metadata rows can still be tagged.

---

## 7. Database layer & name matching

SQLite via `db()` (Row factory, foreign keys on). Schema (`SCHEMA`, applied by `init_db()`):

| Table | Purpose |
|---|---|
| `Roster` | The 10 players (`real_name` unique, `is_hero`). |
| `Aliases` | `alias` (lower-cased PGN name) → `player_id`, with `source` = `seed`/`auto`/`manual`. |
| `IgnoredNames` | Names deliberately not mapped (Dino's incidental opponents, etc.). |
| `Files` | One row per scanned PGN file (+ a synthetic row for the Lichess source). |
| `Games` | One row **per roster player per game** (so a roster-vs-roster game yields two rows). Includes color, `presult` (win/draw/loss/unknown), headers, `eco`, `opening`, `moves_json`, `source` (`pgn`/`lichess`), `lichess_id`, and a `dedup_hash`. `UNIQUE(player_id, dedup_hash)` prevents duplicates. |
| `Tags` | `(game_id, family)` rows from `tag_families`. |
| `UnmatchedNames` | PGN names that didn't resolve to a roster player, with a game count (shown in the UI for manual mapping). |

**Migration guard:** if an older DB lacks the `lichess_id` column, `init_db()` drops and recreates
`Games`/`Tags` (a later `scan()` refills them).

### Matching a PGN name to a roster player
- `name_tokens(s)` lower-cases, strips punctuation, and drops title words (`gm`, `im`, `fm`, …).
- `auto_match(conn, name)` scores roster players by **shared token count**, returning a player only
  if the best score is **≥2 and strictly greater** than the runner-up (so a single shared token, or
  a tie between two players, yields no match — this is intentionally conservative).
- `resolve_name(conn, name)` checks `Aliases` first (exact lower-cased key); else tries
  `auto_match` and, on success, caches the result as an `auto` alias. `ROSTER_ALIASES` (§2) and
  `HERO_ALIASES` are pre-seeded as `seed` aliases to cover spellings `auto_match` can't reach.

---

## 8. The scan pipeline (`scan(conn)`)

A **full rebuild** (it `DELETE`s `Games`, `Files`, `UnmatchedNames` first; aliases and ignored
names are kept). For each PGN:

1. Iterates **`BASE_DIR.rglob("*.pgn")`** — note **`rglob`**, so it recurses into subfolders
   (e.g. `chessbasepgn/`), not just the top-level folder.
2. Splits into games, parses headers + moves.
3. Classifies opening (header `ECO`/`Opening` win if present, else the move-based guess) and tags
   families.
4. Computes a `dedup_hash` from white|black|date|result|first-40-moves.
5. For **each side** (white, black), resolves the name to a roster player; matches are inserted into
   `Games` (with `presult_for(result, color)`), non-matches accumulate in an `unmatched` counter
   (skipping `?`/`NN`). Family tags are written for stored games.

After the files, `ingest_lichess_pool(conn, summary)` pulls the optional Lichess scout data
(`lichess_pool_rows()` reads the SQLite DB or its CSV export), inserting **metadata-only** rows
(`moves_json = []`, `source='lichess'`, a `lichess_id`) — these link out to lichess.org instead of
the built-in board. Standard-variant games only; deduped by `lichess:<id>`.

Finally, unmatched names not in `IgnoredNames` are written to `UnmatchedNames`. Returns a summary
`{files, games_seen, games_stored}`.

`tc_label(tc)` converts a Lichess time control to bullet/blitz/rapid/classical labels for the
event string.

---

## 9. Analysis functions

- `score_pct(w,d,l)` → percentage score; `wdl(games)` → `{n,w,d,l,score}`.
- `opening_table(games)` → per-opening W/D/L rows, sorted by frequency.
- `family_table(games)` → one row per family (including zero-game families).
- `player_games(conn, pid)` → all of a player's games with their family tags and a derived
  `opponent` field (the other side), newest first.
- `player_dossier(conn, pid)` → profile + totals + source split (pgn vs lichess) + White/Black
  repertoire tables + family table + full game list. Powers the **Opponents** tab and the exported
  opponent dossiers.
- `hero_improvement(conn)` → Dino's self-audit. Generates a prioritized **bullet list** of findings:
  colour imbalance (White vs Black score gap), weak openings (<50% over ≥2 games each colour), loss
  phase distribution (opening ≤20 / middlegame 21–40 / endgame >40 moves), **repeated problem lines**
  (≥2 losses sharing the same first 8 plies), under-repped/under-performing structure families, and
  "confidence weapons" (≥70% over ≥3 games) to keep rather than change. Powers the **Dino — Needs
  Improvement** tab and `Dino_Ballecer_Needs_Improvement.md`.

---

## 10. Markdown export (`export_markdown`)

Writes into `manual_sections/`:

- `Opponent_<Name>.md` for each opponent (sorted by FIDE desc): record, White/Black repertoire
  tables, structure-family table, **prep pointers** (target the families/openings they score badly
  in, avoid the ones they score well in), and up to 6 recent losses as model games (with a
  lichess.org replay link when the game is online).
- `Dino_Ballecer_Needs_Improvement.md`: the self-audit bullets + opening/family tables + loss
  profile + repeated problem lines.
- `00_INDEX.md`: an index of everything written.

Helpers: `md_wdl`, `md_opening_table`, `md_family_table`, `safe_filename`.

---

## 11. HTTP server & API (`Handler`)

A `BaseHTTPRequestHandler` (logging silenced). JSON helpers `_json`/`_html`/`_body_json`. Every
request opens its own short-lived `db()` connection (the server is threaded).

### GET
| Route | Returns |
|---|---|
| `/` | The entire single-page UI (`HTML_PAGE`). |
| `/api/state` | Roster (with per-player W/D/L/score), files (with stored counts), unmatched names, active aliases, folder path. |
| `/api/player?id=` | `player_dossier` JSON. |
| `/api/improvement` | `hero_improvement` JSON. |
| `/api/game?id=` | One game's headers, SAN move list, and the full FEN sequence (`fens_for`) for the board viewer, plus board orientation and any `replay_error`. |

### POST (JSON body)
| Route | Action |
|---|---|
| `/api/scan` | Re-run `scan` (the **Rescan** button). |
| `/api/map` | Add a `manual` alias (name → player_id), clear it from ignored, and rescan. |
| `/api/unmap` | Delete an alias and rescan. |
| `/api/ignore` | Add a name to `IgnoredNames` and drop it from `UnmatchedNames`. |
| `/api/paste` | Save pasted PGN text as a new `.pgn` file in `BASE_DIR` (rejects non-PGN), then rescan. |
| `/api/export` | Run `export_markdown`, return the file list. |

`state()` is the method backing `/api/state`.

---

## 12. Front-end (`HTML_PAGE`)

One self-contained HTML string: dark-theme CSS + vanilla JS, no external assets. Tabs:

- **Overview** — the round-robin pool table (games loaded per player) + a "waiting for PGN" panel
  listing opponents with zero games. Rows click through to the opponent dossier.
- **Opponents** — a player list + dossier pane (repertoire tables, family table, full game list).
  Clicking an OTB game opens the **board viewer**; a Lichess-sourced game opens lichess.org.
- **Dino — Needs Improvement** — the self-audit (priority bullets, opening/family tables, loss
  profile, repeated problem lines, all losses).
- **Files & Names** — scanned files (parsed vs stored counts), **unmatched names** with Map/Ignore
  controls, active alias mappings (with Remove), and a **paste-a-PGN** box.
- **Export Manual Sections** — triggers `/api/export` and lists what was written.

**Board viewer**: a CSS-grid board rendered from the FEN list, Unicode chess glyphs, move list with
click-to-jump, prev/next/first/last buttons, flip, and arrow-key/Escape navigation. It consumes the
FENs produced server-side by `MiniBoard`, so no chess logic runs in the browser.

---

## 13. Data flow at a glance

```
*.pgn files (incl. subfolders)  ─┐
                                 ├─►  scan()  ─►  SQLite (Games/Tags/…)  ─►  analysis  ─►  JSON API  ─►  browser UI
tournament_pool_2026.db / .csv ──┘                                                   └─►  export_markdown()  ─►  manual_sections/*.md
(optional Lichess scout)                                                                                          (paste into the .docx)
```

---

## 14. Gotchas & conventions worth remembering

- **`scan()` recurses** (`rglob`): PGNs in subfolders like `chessbasepgn/` are picked up. (Earlier
  it used `glob` and silently ignored subfolders.)
- **`init_db()` prunes** the `Roster` to match the `ROSTER` list, and seeds `HERO_ALIASES` +
  `ROSTER_ALIASES`. To change the pool, edit `ROSTER` (and add a `ROSTER_ALIASES` entry if a PGN
  spells the name in a way `auto_match` can't bridge with ≥2 shared tokens).
- **A scan is a full rebuild** of games, but **aliases/ignored names persist** — manual mappings
  survive rescans.
- **Games are stored per roster player**, so a game between two roster members is counted for both;
  totals can exceed the literal PGN game count, and `Files.stored` is reported via
  `COUNT(DISTINCT dedup_hash)`.
- **Unmatched names are expected and fine** — they're the opponents *inside* each opponent's PGN
  (e.g. a different "Vignesh,B2." who is not in the pool). Only Dino + the 9 roster players should
  resolve.
- **Lichess rows have no moves** — they link out rather than opening the built-in viewer.
- **Coaching partner exception**: FM Arlan Cabe is on the roster but intentionally has no PGN
  dropped in (he shows 0 games by design), so his combat-file prep is withheld out of respect.
- The exported Markdown is meant to be pasted into `Tournament_Preparation_Manual.docx`; the docx
  itself is hand-curated (the app does not write the .docx).
```

---

## 15. Engine analysis & opening database (optional layer)

A layer that lets the app's **automated analysis** reason with a real engine + a real opening
database. It is **for the generated analysis** (dossiers, the self-audit, the export) — **not** an
interactive board for the user (they have their own setup). It stays **stdlib-only** (`subprocess`,
`urllib`), **single-file**, and **offline by default**; every piece **degrades gracefully** when its
dependency is absent.

### What it adds (the three prioritised wins)
1. **Better opening classification** — `classify_opening_db(fens)` looks the replayed position up in
   the bundled Lichess opening DB; `scan()` prefers it over `BOOK` (see §6).
2. **Blunder detection in Dino's losses** — `hero_blunder_findings()` pinpoints the exact critical
   move in each loss (eval swing + the move the engine prefers) and reports **accuracy-by-phase**
   (real ACPL), replacing the old move-count `loss_phases` guess. Surfaced in the **Dino — Needs
   Improvement** tab and `Dino_Ballecer_Needs_Improvement.md`.
3. **Opponent weakness fingerprint** — `opponent_fingerprint(pid)` gives each opponent's accuracy
   (overall / by phase / by structure family), blunder counts, and which structures to **target**
   (least accurate) vs **avoid** (solid). Surfaced in the **Opponents** dossier and `Opponent_*.md`.

### External assets (located, not vendored-large)
| Asset | Where | How found |
|---|---|---|
| **Stockfish** (native UCI binary) | `../Extract_ZST/stockfish/…avx2.exe` by default | `find_stockfish()` probes `PREP_STOCKFISH`, `./stockfish/*.exe`, the sibling path, then `shutil.which`. None ⇒ engine features hidden. |
| **Opening DB** (Lichess `chess-openings`, CC0) | `./openings/` (copied into the repo, ~2 MB) | `openings_index.json` = `{4-field-FEN → [{eco,name,variation,…}]}`; `load_opening_index()` caches it. |

### Engine plumbing
- `class Engine` — a persistent UCI client over `subprocess`. `analyse(fen, depth)` returns
  `(cp, mate, bestmove)` in **side-to-move POV**; one shared process guarded by `_ENGINE_LOCK`,
  started lazily by `get_engine()`.
- `eval_position(conn, fen, depth)` — returns **White-POV** `(score_cp, bestmove)` (mate folded into
  a large signed cp via `fold_score`), **cached in `PositionEval`** by the 4-field FEN key
  (`epd_key`) so transpositions/opening positions are computed once. Falls back to Lichess
  **cloud-eval** when `--online` and no local engine.
- `analyze_game(conn, dedup_hash, moves, depth, allow_engine)` — per-move centipawn loss vs the
  engine's best; rolls up per-side ACPL, phase sums, and the significant moves; **cached in
  `GameAnalysis` keyed by `dedup_hash`** (stable across rescans). `allow_engine=False` = read cache
  only (used by every GET so dossiers never block on the engine).
- `analyze_all(conn, scope, …)` — the heavy pass (dedup by hash). `scope` = `all | losses | player`.

### Caches (added to `SCHEMA`, never wiped by `scan()`)
`PositionEval(fen, depth → score_cp, bestmove)`, `GameAnalysis(dedup_hash → acpl/phase/blunders
JSON)`, `ExplorerCache(fen, scope → json)`. New DBs get them via `CREATE IF NOT EXISTS`; existing
DBs pick them up on the next `init_db()` (no destructive migration).

### Triggering analysis (it's the only slow part — off the hot path)
- **CLI:** `--engine-check` (probe + start-position eval), `--analyze [--scope all|losses|player]
  [--player ID] [--depth N] [--max-games K]`, `--online`.
- **API/UI:** POST `/api/analyze` runs `analyze_all` in a background thread; progress in the global
  `ANALYZE_STATUS`, exposed by `/api/state` (along with `engine`, `opening_db`, `online`,
  `analyzed_games`). The header **"Analyze with Stockfish"** button calls it and polls. Results then
  flow into the dossiers / self-audit / export automatically.

### Online opt-in (Lichess) — OFF by default
`ONLINE_ENABLED` (set by `--online`) gates `cloud_eval()` (eval fallback when no local engine) and
`explorer_lookup()` (population/theory context, cached in `ExplorerCache`, reachable at
`GET /api/explorer?fen=…&scope=masters|lichess`). With it off the app makes **zero network calls** —
the offline-by-default guarantee is intact.

### Gotchas worth remembering
- **`GameAnalysis`/`PositionEval` survive a rescan** (keyed by `dedup_hash` / FEN, not `game_id`),
  so analysis isn't lost when `scan()` rebuilds `Games`.
- **Depth keys the cache.** The analysis pass computes at its requested depth; GET/export show the
  **best available depth** for a game if the exact one isn't cached (so a depth-12 pass still
  displays even when the default is 16).
- **No engine ⇒ no crash:** classification still upgrades via the opening DB; the engine sections
  render an "unavailable / not analysed yet" note instead.
- **Scores are normalised** to White POV in storage; findings display from the **mover's** POV (a
  blunder shows the number dropping).
```
