#!/usr/bin/env python3
"""
lichess_tournament_prep.py
==========================
Scouting pipeline for a 10-player closed round-robin (2026).

Fetches each opponent's most recent public Lichess games (2026 only,
max 100/player), parses PGN metadata, tags games against the 6 Core
Structure Families from the Tournament Preparation Manual, and writes
everything into a relational SQLite database: tournament_pool_2026.db

Optionally exports a multi-tab spreadsheet (tournament_pool_2026.xlsx)
if `openpyxl` is installed; otherwise falls back to per-table CSVs.

Usage:
    pip install requests            # (openpyxl optional, for .xlsx)
    python lichess_tournament_prep.py
    python lichess_tournament_prep.py --xlsx     # also export spreadsheet

Google Colab:
    !pip install requests openpyxl
    %run lichess_tournament_prep.py --xlsx

Dependencies: requests (required); openpyxl (optional). Everything else
is the Python standard library.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
import sqlite3
import sys
import time
from pathlib import Path

import requests

# ---------------------------------------------------------------------------
# 1. USER INPUT — HANDLE MAPPING
# ---------------------------------------------------------------------------
# Fill in the real Lichess username for each opponent as you confirm them.
# Leave as None (or "") to skip that player without breaking the run.
# ---------------------------------------------------------------------------
OPPONENTS: dict[str, dict] = {
    "GM Vignesh, N R":            {"federation": "IND", "title": "GM", "fide": 2515, "lichess": "Goodgoodchess"},
    "GM Shyaam, Nikhil P":        {"federation": "IND", "title": "GM", "fide": 2435, "lichess": None},
    "IM Vignesh, Advaith Vemula": {"federation": "IND", "title": "IM", "fide": 2421, "lichess": None},
    "IM Tan, Jun Ying":           {"federation": "MAS", "title": "IM", "fide": 2404, "lichess": None},
    "IM Chan, Kim Yew":           {"federation": "MAS", "title": "IM", "fide": 2360, "lichess": "Smirnov85"},
    "IM Susilodinata, Andrean":   {"federation": "INA", "title": "IM", "fide": 2360, "lichess": None},
    "GM Thejkumar, M. S.":        {"federation": "IND", "title": "GM", "fide": 2358, "lichess": None},
    "FM Ang, Ern Jie Anderson":   {"federation": "MAS", "title": "FM", "fide": 2309, "lichess": None},
    "FM Arlan Cabe":              {"federation": "PHI", "title": "FM", "fide": 2298, "lichess": None},
}

# ---------------------------------------------------------------------------
# 2. CONFIGURATION
# ---------------------------------------------------------------------------
DB_PATH = "tournament_pool_2026.db"
MAX_GAMES_PER_PLAYER = 100
YEAR = 2026
SINCE_MS = int(dt.datetime(YEAR, 1, 1, tzinfo=dt.timezone.utc).timestamp() * 1000)
UNTIL_MS = int(dt.datetime(YEAR + 1, 1, 1, tzinfo=dt.timezone.utc).timestamp() * 1000)
API_URL = "https://lichess.org/api/games/user/{username}"
REQUEST_TIMEOUT = 120          # streaming PGN export can be slow
POLITE_DELAY_SECONDS = 2.0     # pause between players
MAX_RETRIES_ON_429 = 3

# ---------------------------------------------------------------------------
# 3. CORE STRUCTURE FAMILY ROUTING (from Prep Manual, Part III)
# ---------------------------------------------------------------------------
# Each family is matched by (a) ECO-code ranges and/or (b) case-insensitive
# keyword groups against the PGN "Opening" header. A game may match more
# than one family (e.g. Catalan-Grünfeld hybrids) — all matches are stored
# in the GameTags table.
# ---------------------------------------------------------------------------

def _eco_in(eco: str, ranges: list[tuple[str, str]]) -> bool:
    if not eco or len(eco) < 2:
        return False
    eco = eco.strip().upper()[:3]
    for lo, hi in ranges:
        if lo <= eco <= hi:
            return True
    return False


def _name_has(opening: str, *all_of_groups) -> bool:
    """True if the opening name contains at least one keyword from EVERY group."""
    low = (opening or "").lower()
    return all(any(kw in low for kw in group) for group in all_of_groups)


STRUCTURE_FAMILIES: list[dict] = [
    {
        "family": "Advance Caro-Kann",
        "match": lambda eco, op: (
            _eco_in(eco, [("B12", "B12")]) and _name_has(op, ("caro",), ("advance",))
        ) or _name_has(op, ("caro-kann", "caro kann"), ("advance", "tal variation", "short variation")),
    },
    {
        "family": "Reversed-Sicilian / Flank Annexation",
        "match": lambda eco, op: (
            _eco_in(eco, [("A20", "A29")])                       # 1.c4 e5 complex
            or _name_has(op, ("reversed sicilian",))
            or _name_has(op, ("king's english", "kings english"))
            or _name_has(op, ("king's indian attack", "kings indian attack"))  # KIA-killer file
        ),
    },
    {
        "family": "Fianchetto KID / Grünfeld Complexes",
        "match": lambda eco, op: (
            _eco_in(eco, [("D70", "D99")])                       # Grünfeld
            or _eco_in(eco, [("E60", "E69")])                    # Fianchetto KID zone
            or _name_has(op, ("grünfeld", "grunfeld", "gruenfeld"))
            or _name_has(op, ("king's indian", "kings indian"), ("fianchetto",))
        ),
    },
    {
        "family": "Catalan / Réti Squeeze",
        "match": lambda eco, op: (
            _eco_in(eco, [("E01", "E09")])                       # Catalan
            or _eco_in(eco, [("A04", "A09"), ("A11", "A14")])    # Réti / Zukertort / English-Réti
            or _name_has(op, ("catalan",))
            or _name_has(op, ("réti", "reti", "zukertort", "nimzo-larsen", "nimzowitsch-larsen"))
        ),
    },
    {
        "family": "Anti-Sicilian Counter-Package",
        "match": lambda eco, op: (
            _eco_in(eco, [("B21", "B26")])                       # Smith-Morra, Alapin, Closed, Grand Prix
            or _eco_in(eco, [("B30", "B31"), ("B51", "B52")])    # Rossolimo, Moscow
            or _name_has(op, ("sicilian",), ("alapin", "rossolimo", "moscow", "closed",
                                             "grand prix", "smith-morra", "smith morra",
                                             "mcdonnell", "bowdler", "wing gambit"))
        ),
    },
    {
        "family": "IQP / Panov Attack",
        "match": lambda eco, op: (
            _eco_in(eco, [("B13", "B14")])                       # Exchange / Panov-Botvinnik
            and _name_has(op, ("caro",))
        ) or _name_has(op, ("panov",))
          or _name_has(op, ("tarrasch defense", "tarrasch defence"))   # classic IQP carrier
          or _name_has(op, ("queen's gambit accepted", "queens gambit accepted")),
    },
]


def tag_structures(eco: str, opening: str) -> list[str]:
    return [f["family"] for f in STRUCTURE_FAMILIES if f["match"](eco, opening)]


# ---------------------------------------------------------------------------
# 4. PGN PARSING (stdlib only)
# ---------------------------------------------------------------------------
HEADER_RE = re.compile(r'^\[(\w+)\s+"(.*)"\]\s*$', re.MULTILINE)
CLOCK_RE = re.compile(r"\{\s*\[%clk\s+([\d:.]+)\]\s*\}")
MOVE_NUM_RE = re.compile(r"(\d+)\.(?!\.\.)")   # full-move numbers like "34."


def split_pgn_stream(raw: str) -> list[str]:
    """Split a multi-game PGN export into individual game strings."""
    games, current = [], []
    for line in raw.splitlines():
        if line.startswith("[Event ") and current:
            games.append("\n".join(current).strip())
            current = []
        current.append(line)
    if current:
        block = "\n".join(current).strip()
        if block:
            games.append(block)
    return games


def parse_game(pgn: str) -> dict | None:
    headers = dict(HEADER_RE.findall(pgn))
    if not headers:
        return None

    # Movetext = everything after the last header line
    last_header_end = 0
    for m in HEADER_RE.finditer(pgn):
        last_header_end = m.end()
    movetext = pgn[last_header_end:].strip()

    move_numbers = [int(n) for n in MOVE_NUM_RE.findall(movetext)]
    total_moves = max(move_numbers) if move_numbers else 0

    clocks = CLOCK_RE.findall(movetext)
    # Even indices = White's remaining clock after each move, odd = Black's.
    move_times = json.dumps(clocks) if clocks else None

    site = headers.get("Site", "")
    lichess_id = site.rsplit("/", 1)[-1] if "lichess.org" in site else site or None

    return {
        "lichess_game_id": lichess_id,
        "white": headers.get("White", "?"),
        "black": headers.get("Black", "?"),
        "result": headers.get("Result", "*"),
        "eco": headers.get("ECO", ""),
        "opening": headers.get("Opening", ""),
        "total_moves": total_moves,
        "termination": headers.get("Termination", ""),
        "date_utc": headers.get("UTCDate", headers.get("Date", "")),
        "time_control": headers.get("TimeControl", ""),
        "variant": headers.get("Variant", "Standard"),
        "white_elo": headers.get("WhiteElo", ""),
        "black_elo": headers.get("BlackElo", ""),
        "move_times": move_times,
    }


# ---------------------------------------------------------------------------
# 5. LICHESS API FETCH
# ---------------------------------------------------------------------------
def fetch_player_pgn(session: requests.Session, username: str) -> str | None:
    params = {
        "max": MAX_GAMES_PER_PLAYER,
        "since": SINCE_MS,
        "until": UNTIL_MS,
        "moves": "true",
        "opening": "true",     # ECO + Opening headers
        "clocks": "true",      # [%clk ...] tags where available
        "tags": "true",
        "perfType": "ultraBullet,bullet,blitz,rapid,classical,correspondence",
    }
    headers = {"Accept": "application/x-chess-pgn"}
    url = API_URL.format(username=username)

    for attempt in range(1, MAX_RETRIES_ON_429 + 2):
        try:
            resp = session.get(url, params=params, headers=headers,
                               timeout=REQUEST_TIMEOUT, stream=False)
        except requests.RequestException as exc:
            print(f"    !! network error for {username}: {exc}", file=sys.stderr)
            return None

        if resp.status_code == 200:
            return resp.text
        if resp.status_code == 404:
            print(f"    !! username not found on Lichess: {username}", file=sys.stderr)
            return None
        if resp.status_code == 429:
            wait = 60 * attempt
            print(f"    .. rate-limited (429). Sleeping {wait}s "
                  f"(attempt {attempt}/{MAX_RETRIES_ON_429}) ...")
            time.sleep(wait)
            continue
        print(f"    !! HTTP {resp.status_code} for {username}", file=sys.stderr)
        return None
    return None


# ---------------------------------------------------------------------------
# 6. SQLITE SCHEMA
# ---------------------------------------------------------------------------
SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Players (
    player_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    real_name        TEXT NOT NULL UNIQUE,
    title            TEXT,
    federation       TEXT,
    fide_rating      INTEGER,
    lichess_username TEXT,
    games_fetched    INTEGER DEFAULT 0,
    fetched_at_utc   TEXT
);

CREATE TABLE IF NOT EXISTS Games (
    game_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id        INTEGER NOT NULL REFERENCES Players(player_id) ON DELETE CASCADE,
    lichess_game_id  TEXT,
    date_utc         TEXT,
    white            TEXT,
    black            TEXT,
    white_elo        TEXT,
    black_elo        TEXT,
    result           TEXT,
    player_color     TEXT CHECK (player_color IN ('white','black','unknown')),
    player_result    TEXT CHECK (player_result IN ('win','loss','draw','unknown')),
    eco              TEXT,
    opening          TEXT,
    total_moves      INTEGER,
    termination      TEXT,
    time_control     TEXT,
    variant          TEXT,
    move_times_json  TEXT,
    UNIQUE (player_id, lichess_game_id)
);

CREATE TABLE IF NOT EXISTS GameTags (
    tag_id           INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id          INTEGER NOT NULL REFERENCES Games(game_id) ON DELETE CASCADE,
    structure_family TEXT NOT NULL,
    UNIQUE (game_id, structure_family)
);

CREATE INDEX IF NOT EXISTS idx_games_player  ON Games(player_id);
CREATE INDEX IF NOT EXISTS idx_games_eco     ON Games(eco);
CREATE INDEX IF NOT EXISTS idx_tags_family   ON GameTags(structure_family);

CREATE VIEW IF NOT EXISTS v_structure_summary AS
SELECT p.real_name,
       t.structure_family,
       COUNT(*)                                            AS games,
       SUM(CASE WHEN g.player_result = 'win'  THEN 1 ELSE 0 END) AS wins,
       SUM(CASE WHEN g.player_result = 'draw' THEN 1 ELSE 0 END) AS draws,
       SUM(CASE WHEN g.player_result = 'loss' THEN 1 ELSE 0 END) AS losses
FROM GameTags t
JOIN Games   g ON g.game_id   = t.game_id
JOIN Players p ON p.player_id = g.player_id
GROUP BY p.real_name, t.structure_family;
"""


def derive_player_perspective(game: dict, username: str) -> tuple[str, str]:
    uname = username.lower()
    if game["white"].lower() == uname:
        color = "white"
    elif game["black"].lower() == uname:
        color = "black"
    else:
        return "unknown", "unknown"

    result = game["result"]
    if result == "1/2-1/2":
        return color, "draw"
    if (result == "1-0" and color == "white") or (result == "0-1" and color == "black"):
        return color, "win"
    if result in ("1-0", "0-1"):
        return color, "loss"
    return color, "unknown"


# ---------------------------------------------------------------------------
# 7. PIPELINE
# ---------------------------------------------------------------------------
def run_pipeline() -> Path:
    db_path = Path(DB_PATH)
    conn = sqlite3.connect(db_path)
    conn.executescript(SCHEMA)

    session = requests.Session()
    session.headers["User-Agent"] = "tournament-prep-scout/1.0"

    for real_name, meta in OPPONENTS.items():
        username = (meta.get("lichess") or "").strip()
        cur = conn.execute(
            """INSERT INTO Players (real_name, title, federation, fide_rating, lichess_username)
               VALUES (?,?,?,?,?)
               ON CONFLICT(real_name) DO UPDATE SET
                   lichess_username = excluded.lichess_username,
                   title = excluded.title,
                   federation = excluded.federation,
                   fide_rating = excluded.fide_rating
               RETURNING player_id""",
            (real_name, meta["title"], meta["federation"], meta["fide"], username or None),
        )
        player_id = cur.fetchone()[0]

        if not username:
            print(f"[skip] {real_name}: no Lichess handle mapped yet.")
            continue

        print(f"[pull] {real_name}  ->  lichess.org/@/{username}")
        raw = fetch_player_pgn(session, username)
        if not raw or not raw.strip():
            print(f"    .. no {YEAR} games returned.")
            conn.commit()
            time.sleep(POLITE_DELAY_SECONDS)
            continue

        games = [g for g in (parse_game(p) for p in split_pgn_stream(raw)) if g]
        inserted = 0
        for g in games:
            color, presult = derive_player_perspective(g, username)
            try:
                cur = conn.execute(
                    """INSERT OR IGNORE INTO Games
                       (player_id, lichess_game_id, date_utc, white, black,
                        white_elo, black_elo, result, player_color, player_result,
                        eco, opening, total_moves, termination, time_control,
                        variant, move_times_json)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (player_id, g["lichess_game_id"], g["date_utc"], g["white"],
                     g["black"], g["white_elo"], g["black_elo"], g["result"],
                     color, presult, g["eco"], g["opening"], g["total_moves"],
                     g["termination"], g["time_control"], g["variant"],
                     g["move_times"]),
                )
            except sqlite3.Error as exc:
                print(f"    !! insert error: {exc}", file=sys.stderr)
                continue
            if cur.rowcount == 0:
                continue
            game_id = cur.lastrowid
            inserted += 1
            for family in tag_structures(g["eco"], g["opening"]):
                conn.execute(
                    "INSERT OR IGNORE INTO GameTags (game_id, structure_family) VALUES (?,?)",
                    (game_id, family),
                )

        conn.execute(
            "UPDATE Players SET games_fetched = games_fetched + ?, fetched_at_utc = ? "
            "WHERE player_id = ?",
            (inserted, dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), player_id),
        )
        conn.commit()
        print(f"    ok {inserted} new games stored "
              f"({len(games)} parsed from API).")
        time.sleep(POLITE_DELAY_SECONDS)

    conn.commit()
    conn.close()
    print(f"\nDatabase ready: {db_path.resolve()}")
    return db_path


# ---------------------------------------------------------------------------
# 8. OPTIONAL EXPORT — multi-tab XLSX (openpyxl) or CSV fallback
# ---------------------------------------------------------------------------
EXPORT_QUERIES = {
    "Players": "SELECT * FROM Players ORDER BY fide_rating DESC",
    "Games": """SELECT p.real_name, g.* FROM Games g
                 JOIN Players p ON p.player_id = g.player_id
                 ORDER BY p.real_name, g.date_utc DESC""",
    "StructureTags": """SELECT p.real_name, g.lichess_game_id, g.eco, g.opening,
                               t.structure_family, g.player_color, g.player_result
                        FROM GameTags t
                        JOIN Games g   ON g.game_id = t.game_id
                        JOIN Players p ON p.player_id = g.player_id
                        ORDER BY t.structure_family, p.real_name""",
    "FamilySummary": "SELECT * FROM v_structure_summary ORDER BY real_name, games DESC",
}


def export_spreadsheet(db_path: Path) -> None:
    conn = sqlite3.connect(db_path)
    try:
        import openpyxl  # noqa: F401
        from openpyxl import Workbook

        wb = Workbook()
        wb.remove(wb.active)
        for sheet, query in EXPORT_QUERIES.items():
            cur = conn.execute(query)
            ws = wb.create_sheet(title=sheet)
            ws.append([d[0] for d in cur.description])
            for row in cur:
                ws.append(list(row))
        out = db_path.with_suffix(".xlsx")
        wb.save(out)
        print(f"Spreadsheet ready: {out.resolve()}")
    except ImportError:
        print("openpyxl not installed -> writing CSVs instead "
              "(pip install openpyxl for a single .xlsx).")
        for sheet, query in EXPORT_QUERIES.items():
            cur = conn.execute(query)
            out = db_path.with_name(f"{db_path.stem}_{sheet}.csv")
            with open(out, "w", newline="", encoding="utf-8") as fh:
                w = csv.writer(fh)
                w.writerow([d[0] for d in cur.description])
                w.writerows(cur)
            print(f"  wrote {out}")
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# 9. ENTRY POINT
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Lichess tournament-pool scout (2026).")
    ap.add_argument("--xlsx", action="store_true",
                    help="also export multi-tab spreadsheet / CSV fallback")
    args = ap.parse_args()

    path = run_pipeline()
    if args.xlsx:
        export_spreadsheet(path)
