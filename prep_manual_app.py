#!/usr/bin/env python3
"""
prep_manual_app.py
==================
Local web app for building the 2026 Tournament Preparation Manual
for Dino Ballecer ("Coach Dinosaur").

What it does
------------
1. Scans THIS folder for every *.pgn file (multi-game PGN databases).
   Drop the opponents' PGN databases here later and click "Rescan".
2. Matches the player names found inside the PGNs to the 10-player
   roster (Dino + 9 opponents). Unrecognised names can be mapped by
   hand in the "Files & Names" tab.
3. Classifies every game by opening (from the moves themselves, so
   bare OTB PGNs without ECO/Opening headers work) and tags it
   against the 6 Core Structure Families of the Prep Manual.
4. Opponent dossiers: repertoire as White/Black, structure-family
   record, full game list with a built-in board viewer.
5. "Needs Improvement" report for Dino Ballecer generated from
   CoachDinosaur_Games.pgn (and any other PGN containing his games).
6. One-click export of Markdown sections (manual_sections/) ready to
   paste into Tournament_Preparation_Manual.docx.

Usage
-----
    python prep_manual_app.py            # starts http://localhost:8765
    python prep_manual_app.py --export   # headless: just write markdown
    python prep_manual_app.py --port 9000 --no-browser
    python prep_manual_app.py --engine-check        # test the Stockfish UCI link
    python prep_manual_app.py --analyze --scope player --player ID  # analyse one player
    python prep_manual_app.py --online ...           # opt in to Lichess explorer/cloud-eval

No third-party packages required (Python 3.10+ standard library only).
Optional engine analysis uses a local Stockfish binary (see find_stockfish());
optional opening classification uses the bundled Lichess opening database in
./openings/. Both degrade gracefully when absent.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import math
import os
import random
import re
import shutil
import sqlite3
import subprocess
import sys
import threading
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from collections import Counter
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import player_profile as profile_engine

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "prep_manual.db"
EXPORT_DIR = BASE_DIR / "manual_sections"
DEFAULT_PORT = 8765

# Lichess scout data produced by lichess_tournament_prep.py (metadata only,
# no moves — games link out to lichess.org instead of the built-in board).
LICHESS_DB = BASE_DIR / "tournament_pool_2026.db"
LICHESS_CSV = BASE_DIR / "tournament_pool_2026_Games.csv"

# ---------------------------------------------------------------------------
# OPTIONAL CHESS TOOLING — all of this degrades gracefully when absent.
# ---------------------------------------------------------------------------
# Stockfish: a local UCI engine binary drives the (optional) blunder / accuracy
# analysis. We probe a few sensible locations; set PREP_STOCKFISH to override.
# The repo deliberately ships NO engine binary (it is large); the app runs fine
# without one — engine sections simply stay hidden.
STOCKFISH_CANDIDATES = [
    os.environ.get("PREP_STOCKFISH", ""),
    str(BASE_DIR / "stockfish" / "stockfish-windows-x86-64-avx2.exe"),
    str(BASE_DIR / "stockfish" / "stockfish.exe"),
    str(BASE_DIR / "stockfish.exe"),
    # sibling project that already carries a native Stockfish 18 build
    str(BASE_DIR.parent / "Extract_ZST" / "stockfish" / "stockfish-windows-x86-64-avx2.exe"),
]


def find_stockfish() -> str | None:
    """Return the first Stockfish binary that exists, or None."""
    for cand in STOCKFISH_CANDIDATES:
        if cand and Path(cand).is_file():
            return cand
    return shutil.which("stockfish")


# Bundled Lichess opening database (CC0). openings_index.json maps a 4-field
# FEN (board / side / castling / ep) -> [{eco, name, variation, ...}].
OPENINGS_DIR = BASE_DIR / "openings"
if not (OPENINGS_DIR / "openings_index.json").is_file():
    _sib = BASE_DIR.parent / "et_optimus" / "endgame_trainer" / "assets" / "openings"
    if (_sib / "openings_index.json").is_file():
        OPENINGS_DIR = _sib
OPENING_INDEX_PATH = OPENINGS_DIR / "openings_index.json"
OPENING_EXPLAIN_PATH = OPENINGS_DIR / "opening_explanations.json"

# Engine analysis tunables.
ENGINE_DEPTH = 16            # search depth per position
ENGINE_THREADS = 2
ENGINE_HASH_MB = 128
ANALYZE_FROM_PLY = 8         # skip the first few book plies (ply 0 == before move 1)
ANALYZE_TO_PLY = 80          # cap work at ~move 40
# Centipawn-loss thresholds for classifying a side's move (loss vs engine best).
CP_INACCURACY = 50
CP_MISTAKE = 100
CP_BLUNDER = 200
EP_INACCURACY = 0.03       # expected-score loss; filters already-lost noise
EP_MISTAKE = 0.08
EP_BLUNDER = 0.18
MATE_CP = 10000             # internal score used to stand in for a forced mate

# Interactive play-bot tunables. The play engine is deliberately rating-limited
# and separate from the analysis engine so background analysis cannot stall games.
PLAY_ELO_MIN = 1320
PLAY_ELO_MAX = 3190
PLAY_DEFAULT_ELO = 2400
PLAY_MOVETIME_MS = 700
PLAY_MULTIPV = 4
PLAY_BLUNDER_CP = 300
PLAY_OPENING_PLY_LIMIT = 16
PLAY_CLOCK_PRESETS = ["60+30", "25+10", "15+10", "5+5"]

# Online opt-in (Lichess). OFF by default to preserve offline-by-default design.
ONLINE_ENABLED = False
LICHESS_CLOUD_EVAL = "https://lichess.org/api/cloud-eval"
LICHESS_EXPLORER = "https://explorer.lichess.ovh"
HTTP_TIMEOUT = 6

# ---------------------------------------------------------------------------
# ROSTER — Dino + the 9 opponents (same pool as lichess_tournament_prep.py)
# ---------------------------------------------------------------------------
HERO_NAME = "Dino Ballecer"
HERO_ALIASES = ["coach dinosaur", "ballecer, dino", "dino ballecer", "ballecer dino"]

ROSTER: list[dict] = [
    {"real_name": HERO_NAME,                  "title": "FM", "federation": "PHI", "fide": 2372, "is_hero": 1},
    {"real_name": "GM Vignesh, N R",          "title": "GM", "federation": "IND", "fide": 2515, "is_hero": 0},
    {"real_name": "GM Shyaam, Nikhil P",      "title": "GM", "federation": "IND", "fide": 2435, "is_hero": 0},
    {"real_name": "IM Morris, James",          "title": "IM", "federation": "AUS", "fide": 2423, "is_hero": 0},
    {"real_name": "IM Tan, Jun Ying",         "title": "IM", "federation": "MAS", "fide": 2404, "is_hero": 0},
    {"real_name": "IM Chan, Kim Yew",         "title": "IM", "federation": "MAS", "fide": 2360, "is_hero": 0},
    {"real_name": "IM Susilodinata, Andrean", "title": "IM", "federation": "INA", "fide": 2360, "is_hero": 0},
    {"real_name": "GM Thejkumar, M. S.",      "title": "GM", "federation": "IND", "fide": 2352, "is_hero": 0},
    {"real_name": "FM Ang, Ern Jie Anderson", "title": "FM", "federation": "MAS", "fide": 2309, "is_hero": 0},
    {"real_name": "FM Arlan Cabe",            "title": "FM", "federation": "PHI", "fide": 2298, "is_hero": 0},
]

# ChessBase PGN exports spell some names with compressed initials / variant
# spellings the token matcher can't bridge on its own (it needs >=2 shared
# tokens). Map the raw PGN header string (lower-cased) -> roster real_name so
# their games attach on scan. Keys must match the header text exactly.
ROSTER_ALIASES: dict[str, str] = {
    "shyam,nikil p": "GM Shyaam, Nikhil P",   # Shyam/Shyaam, Nikil/Nikhil
    "thejkumar,ms.": "GM Thejkumar, M. S.",   # "MS." one token vs "M. S."
    "vignesh,nr.":   "GM Vignesh, N R",       # "NR." one token vs "N R"
}

TITLE_WORDS = {"gm", "im", "fm", "cm", "nm", "wgm", "wim", "wfm", "wcm",
               "agm", "aim", "afm", "acm", "fst", "fi", "ca"}

# ---------------------------------------------------------------------------
# THE 6 CORE STRUCTURE FAMILIES (Prep Manual, Part III)
# ---------------------------------------------------------------------------
FAM_ADV_CARO = "Advance Caro-Kann"
FAM_REVSIC   = "Reversed-Sicilian / Flank Annexation"
FAM_KID_GRU  = "Fianchetto KID / Grünfeld Complexes"
FAM_CAT_RETI = "Catalan / Réti Squeeze"
FAM_ANTISIC  = "Anti-Sicilian Counter-Package"
FAM_IQP      = "IQP / Panov Attack"
ALL_FAMILIES = [FAM_ADV_CARO, FAM_REVSIC, FAM_KID_GRU, FAM_CAT_RETI, FAM_ANTISIC, FAM_IQP]


# ===========================================================================
# MINI CHESS ENGINE — replays SAN so the browser board viewer gets FENs
# ===========================================================================
FILES_STR = "abcdefgh"
KNIGHT_D = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
KING_D = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
BISHOP_D = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
ROOK_D = [(1, 0), (-1, 0), (0, 1), (0, -1)]
SAN_RE = re.compile(r'^([KQRBN]?)([a-h]?)([1-8]?)x?([a-h][1-8])(?:=([QRBN]))?$')


def _parse_sq(s: str) -> int:
    return (int(s[1]) - 1) * 8 + FILES_STR.index(s[0])


def _sq_name(i: int) -> str:
    return FILES_STR[i % 8] + str(i // 8 + 1)


class MiniBoard:
    def __init__(self):
        self.b = list("RNBQKBNR" + "P" * 8 + "." * 32 + "p" * 8 + "rnbqkbnr")
        self.white = True
        self.castle = set("KQkq")
        self.ep: int | None = None
        self.full = 1
        self.last_uci: str | None = None

    def fen(self) -> str:
        rows = []
        for r in range(7, -1, -1):
            row, empty = "", 0
            for f in range(8):
                p = self.b[r * 8 + f]
                if p == ".":
                    empty += 1
                else:
                    if empty:
                        row += str(empty)
                        empty = 0
                    row += p
            if empty:
                row += str(empty)
            rows.append(row)
        cast = "".join(c for c in "KQkq" if c in self.castle) or "-"
        ep = _sq_name(self.ep) if self.ep is not None else "-"
        side = "w" if self.white else "b"
        return f"{'/'.join(rows)} {side} {cast} {ep} 0 {self.full}"

    def _attacked(self, target: int, by_white: bool) -> bool:
        tr, tf = divmod(target, 8)
        pr = tr + (-1 if by_white else 1)
        if 0 <= pr < 8:
            for df in (-1, 1):
                f = tf + df
                if 0 <= f < 8 and self.b[pr * 8 + f] == ("P" if by_white else "p"):
                    return True
        for dx, dy in KNIGHT_D:
            r, f = tr + dy, tf + dx
            if 0 <= r < 8 and 0 <= f < 8 and self.b[r * 8 + f] == ("N" if by_white else "n"):
                return True
        for dx, dy in KING_D:
            r, f = tr + dy, tf + dx
            if 0 <= r < 8 and 0 <= f < 8 and self.b[r * 8 + f] == ("K" if by_white else "k"):
                return True
        for dirs, pcs in ((BISHOP_D, "BQ"), (ROOK_D, "RQ")):
            want = pcs if by_white else pcs.lower()
            for dx, dy in dirs:
                r, f = tr + dy, tf + dx
                while 0 <= r < 8 and 0 <= f < 8:
                    p = self.b[r * 8 + f]
                    if p != ".":
                        if p in want:
                            return True
                        break
                    r += dy
                    f += dx
        return False

    def _king_sq(self, white: bool) -> int:
        return self.b.index("K" if white else "k")

    def _reaches(self, frm: int, to: int) -> bool:
        p = self.b[frm]
        pt = p.upper()
        fr, ff = divmod(frm, 8)
        tr, tf = divmod(to, 8)
        dr, df = tr - fr, tf - ff
        if pt == "N":
            return (abs(dr), abs(df)) in ((1, 2), (2, 1))
        if pt == "K":
            return max(abs(dr), abs(df)) == 1
        if pt == "P":
            fwd = 1 if p == "P" else -1
            start = 1 if p == "P" else 6
            if df == 0 and self.b[to] == ".":
                if dr == fwd:
                    return True
                return dr == 2 * fwd and fr == start and self.b[frm + 8 * fwd] == "."
            if abs(df) == 1 and dr == fwd:
                return self.b[to] != "." or to == self.ep
            return False
        if pt == "B" and abs(dr) != abs(df):
            return False
        if pt == "R" and dr != 0 and df != 0:
            return False
        if pt == "Q" and not (dr == 0 or df == 0 or abs(dr) == abs(df)):
            return False
        sr = (dr > 0) - (dr < 0)
        sf = (df > 0) - (df < 0)
        r, f = fr + sr, ff + sf
        while (r, f) != (tr, tf):
            if self.b[r * 8 + f] != ".":
                return False
            r += sr
            f += sf
        return True

    def _make(self, frm: int, to: int, promo: str | None):
        p = self.b[frm]
        new_ep = None
        if p in "Pp":
            if to == self.ep and self.b[to] == ".":
                self.b[to + (-8 if p == "P" else 8)] = "."
            if abs(to - frm) == 16:
                new_ep = (frm + to) // 2
        self.b[to] = promo if promo else p
        self.b[frm] = "."
        for s in (frm, to):
            if s == 0:
                self.castle.discard("Q")
            elif s == 7:
                self.castle.discard("K")
            elif s == 56:
                self.castle.discard("q")
            elif s == 63:
                self.castle.discard("k")
        if p == "K":
            self.castle -= set("KQ")
        elif p == "k":
            self.castle -= set("kq")
        self.ep = new_ep
        if not self.white:
            self.full += 1
        self.white = not self.white

    def push_san(self, san: str):
        san = san.rstrip("+#!?").strip()
        self.last_uci = None
        if san in ("O-O", "0-0", "O-O-O", "0-0-0"):
            home = 0 if self.white else 56
            k = home + 4
            if san in ("O-O", "0-0"):
                rf, rt, kt = home + 7, home + 5, home + 6
            else:
                rf, rt, kt = home, home + 3, home + 2
            kp, rp = self.b[k], self.b[rf]
            self.b[k] = self.b[rf] = "."
            self.b[kt], self.b[rt] = kp, rp
            self.castle -= set("KQ") if self.white else set("kq")
            self.ep = None
            if not self.white:
                self.full += 1
            self.white = not self.white
            self.last_uci = _sq_name(k) + _sq_name(kt)
            return
        m = SAN_RE.match(san)
        if not m:
            raise ValueError(f"bad SAN: {san}")
        pt, dff, dfr, dest, promo = m.groups()
        pt = pt or "P"
        to = _parse_sq(dest)
        pc = pt if self.white else pt.lower()
        cands = []
        for i, p in enumerate(self.b):
            if p != pc:
                continue
            if dff and i % 8 != FILES_STR.index(dff):
                continue
            if dfr and i // 8 != int(dfr) - 1:
                continue
            t = self.b[to]
            if t != "." and t.isupper() == self.white:
                continue
            if self._reaches(i, to):
                cands.append(i)
        if len(cands) > 1:
            legal = []
            for i in cands:
                snap = (self.b[:], self.white, set(self.castle), self.ep, self.full)
                self._make(i, to, (promo if self.white else promo.lower()) if promo else None)
                if not self._attacked(self._king_sq(snap[1]), not snap[1]):
                    legal.append(i)
                self.b, self.white, self.castle, self.ep, self.full = snap
            if legal:
                cands = legal
        if not cands:
            raise ValueError(f"no candidate for {san}")
        frm = cands[0]
        self.last_uci = _sq_name(frm) + _sq_name(to) + (promo.lower() if promo else "")
        self._make(frm, to, (promo if self.white else promo.lower()) if promo else None)


def fens_for(moves: list[str]) -> tuple[list[str], str | None]:
    """Return ([start_fen, fen_after_ply1, ...], error_or_None)."""
    bd = MiniBoard()
    fens = [bd.fen()]
    for mv in moves:
        try:
            bd.push_san(mv)
        except Exception as exc:
            return fens, f"replay stopped at '{mv}': {exc}"
        fens.append(bd.fen())
    return fens, None


def moves_uci_for(moves: list[str]) -> tuple[list[tuple[str, str, str]], str | None]:
    """Return [(fen_before, uci, fen_after), ...] replayed from SAN moves."""
    bd = MiniBoard()
    out: list[tuple[str, str, str]] = []
    for mv in moves:
        before = bd.fen()
        try:
            bd.push_san(mv)
        except Exception as exc:
            return out, f"replay stopped at '{mv}': {exc}"
        if not bd.last_uci:
            return out, f"replay stopped at '{mv}': no UCI move produced"
        out.append((before, bd.last_uci, bd.fen()))
    return out, None


# ===========================================================================
# OPTIONAL CHESS TOOLING — Stockfish engine + bundled opening database.
# Everything here is for the app's *automated* analysis (the engine the model
# reasons over to build dossiers / the self-audit / the exported manual). It is
# NOT an interactive board tool. All of it degrades gracefully when absent.
# ===========================================================================
def epd_key(fen: str) -> str:
    """First 4 FEN fields (board / side / castling / ep) — the opening-DB and
    position-eval cache key. Drops the move counters so transpositions collide."""
    p = fen.split()
    return " ".join(p[:4]) if len(p) >= 4 else fen


# --- bundled opening database (Lichess chess-openings, CC0) ----------------
_OPENING_INDEX: dict | None = None


def load_opening_index() -> dict:
    """Lazy-load openings_index.json -> {4-field-FEN: [{eco,name,variation,...}]}."""
    global _OPENING_INDEX
    if _OPENING_INDEX is None:
        try:
            data = json.loads(OPENING_INDEX_PATH.read_text(encoding="utf-8"))
            _OPENING_INDEX = data.get("entriesByFen", data)
        except (OSError, ValueError):
            _OPENING_INDEX = {}
    return _OPENING_INDEX


def opening_db_available() -> bool:
    return bool(load_opening_index())


def _name_from_entry(entry: list) -> tuple[str, str]:
    e = entry[0]
    name = e.get("name", "") or ""
    var = e.get("variation", "") or ""
    full = f"{name}: {var}" if var and var.lower() not in name.lower() else name
    return full, e.get("eco", "") or ""


def classify_opening_db(fens: list[str]) -> tuple[str, str] | None:
    """Most-specific (deepest) opening name/ECO for a FEN sequence, or None."""
    idx = load_opening_index()
    if not idx or not fens:
        return None
    for k in range(len(fens) - 1, -1, -1):
        key = epd_key(fens[k])
        ent = idx.get(key)
        if not ent:  # en-passant-notation mismatch: retry with ep='-'
            parts = key.split()
            if len(parts) == 4 and parts[3] != "-":
                ent = idx.get(" ".join(parts[:3] + ["-"]))
        if ent:
            return _name_from_entry(ent)
    return None


# --- Stockfish UCI client (stdlib subprocess; no python-chess) -------------
def _white_to_move(fen: str) -> bool:
    parts = fen.split()
    return len(parts) < 2 or parts[1] == "w"


def fold_score(cp: int | None, mate: int | None, white_to_move: bool) -> int:
    """Engine score (side-to-move POV) -> a single White-POV centipawn scalar.
    Mate is folded into a large signed value so arithmetic stays simple."""
    if mate is not None:
        val = (MATE_CP - abs(mate)) * (1 if mate > 0 else -1)
    elif cp is not None:
        val = cp
    else:
        return 0
    return val if white_to_move else -val


def _uci_score_to_cp(cp: int | None, mate: int | None) -> int:
    """Convert a UCI side-to-move score into a comparable centipawn scalar."""
    if mate is not None:
        return (MATE_CP - abs(mate)) * (1 if mate > 0 else -1)
    return int(cp or 0)


def clamp_play_elo(elo: int | None) -> int:
    try:
        val = int(elo if elo is not None else PLAY_DEFAULT_ELO)
    except (TypeError, ValueError):
        val = PLAY_DEFAULT_ELO
    return max(PLAY_ELO_MIN, min(PLAY_ELO_MAX, val))


class Engine:
    """Minimal persistent UCI client around a Stockfish binary."""

    def __init__(self, path: str):
        self.path = path
        self.name = "Stockfish"
        self.proc = subprocess.Popen(
            [path], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL, text=True, bufsize=1)
        self._send("uci")
        for line in self.proc.stdout:                       # type: ignore[union-attr]
            if line.startswith("id name"):
                self.name = line[7:].strip()
            if line.startswith("uciok"):
                break
        self._send(f"setoption name Threads value {ENGINE_THREADS}")
        self._send(f"setoption name Hash value {ENGINE_HASH_MB}")
        self._ready()

    def _send(self, cmd: str) -> None:
        self.proc.stdin.write(cmd + "\n")                   # type: ignore[union-attr]
        self.proc.stdin.flush()                             # type: ignore[union-attr]

    def _ready(self) -> None:
        self._send("isready")
        for line in self.proc.stdout:                       # type: ignore[union-attr]
            if line.strip() == "readyok":
                return

    def analyse(self, fen_full: str, depth: int) -> tuple[int | None, int | None, str | None]:
        """Return (cp, mate, bestmove_uci) — score is side-to-move POV (UCI raw)."""
        self._send(f"position fen {fen_full}")
        self._send(f"go depth {depth}")
        cp = mate = None
        best = None
        for line in self.proc.stdout:                       # type: ignore[union-attr]
            line = line.strip()
            if line.startswith("info") and " score " in line:
                t = line.split()
                if "cp" in t:
                    cp, mate = int(t[t.index("cp") + 1]), None
                elif "mate" in t:
                    mate, cp = int(t[t.index("mate") + 1]), None
            elif line.startswith("bestmove"):
                parts = line.split()
                best = parts[1] if len(parts) > 1 and parts[1] != "(none)" else None
                break
        return cp, mate, best

    @staticmethod
    def _score_from_tokens(tokens: list[str]) -> tuple[int | None, int | None]:
        cp = mate = None
        if "cp" in tokens:
            try:
                cp = int(tokens[tokens.index("cp") + 1])
            except (IndexError, ValueError):
                cp = None
        if "mate" in tokens:
            try:
                mate = int(tokens[tokens.index("mate") + 1])
                cp = None
            except (IndexError, ValueError):
                mate = None
        return cp, mate

    def _set_play_options(self, elo: int, multipv: int) -> None:
        self._send("setoption name UCI_LimitStrength value true")
        self._send(f"setoption name UCI_Elo value {clamp_play_elo(elo)}")
        self._send(f"setoption name MultiPV value {max(1, int(multipv))}")
        self._ready()

    def _restore_play_options(self) -> None:
        try:
            self._send("setoption name MultiPV value 1")
            self._send("setoption name UCI_LimitStrength value false")
            self._ready()
        except Exception:
            pass

    def top_moves(self, fen_full: str, multipv: int, movetime_ms: int,
                  elo: int) -> list[dict]:
        """Return ranked UCI moves with side-to-move scores from a timed search."""
        found: dict[int, dict] = {}
        best = None
        try:
            self._set_play_options(elo, multipv)
            self._send(f"position fen {fen_full}")
            self._send(f"go movetime {max(1, int(movetime_ms))}")
            for line in self.proc.stdout:                   # type: ignore[union-attr]
                line = line.strip()
                if line.startswith("info") and " pv " in line and " score " in line:
                    t = line.split()
                    try:
                        idx = int(t[t.index("multipv") + 1]) if "multipv" in t else 1
                    except (IndexError, ValueError):
                        idx = 1
                    try:
                        uci = t[t.index("pv") + 1]
                    except (IndexError, ValueError):
                        continue
                    cp, mate = self._score_from_tokens(t)
                    found[idx] = {
                        "uci": uci,
                        "cp": cp,
                        "mate": mate,
                        "score": _uci_score_to_cp(cp, mate),
                        "multipv": idx,
                    }
                elif line.startswith("bestmove"):
                    parts = line.split()
                    best = parts[1] if len(parts) > 1 and parts[1] != "(none)" else None
                    break
        finally:
            self._restore_play_options()
        out = [found[k] for k in sorted(found)]
        if not out and best:
            out = [{"uci": best, "cp": None, "mate": None, "score": 0, "multipv": 1}]
        return out

    def score_move(self, fen_full: str, uci: str, movetime_ms: int,
                   elo: int) -> int | None:
        """Return a side-to-move score for one candidate UCI move."""
        cp = mate = None
        best = None
        try:
            self._set_play_options(elo, 1)
            self._send(f"position fen {fen_full}")
            self._send(f"go searchmoves {uci} movetime {max(1, int(movetime_ms))}")
            for line in self.proc.stdout:                   # type: ignore[union-attr]
                line = line.strip()
                if line.startswith("info") and " score " in line:
                    t = line.split()
                    cp, mate = self._score_from_tokens(t)
                elif line.startswith("bestmove"):
                    parts = line.split()
                    best = parts[1] if len(parts) > 1 and parts[1] != "(none)" else None
                    break
        finally:
            self._restore_play_options()
        if best != uci:
            return None
        return _uci_score_to_cp(cp, mate)

    def close(self) -> None:
        try:
            self._send("quit")
            self.proc.wait(timeout=3)
        except Exception:
            try:
                self.proc.kill()
            except Exception:
                pass


_ENGINE: Engine | None = None
_ENGINE_TRIED = False
_ENGINE_LOCK = threading.Lock()
_PLAY_ENGINE: Engine | None = None
_PLAY_ENGINE_TRIED = False
_PLAY_ENGINE_LOCK = threading.Lock()
_PLAYER_DATASET_CACHE: dict[int, dict] = {}
_PLAYER_DATASET_LOCK = threading.Lock()


def get_engine() -> Engine | None:
    """Lazily start (once) the shared Stockfish process; None if unavailable."""
    global _ENGINE, _ENGINE_TRIED
    with _ENGINE_LOCK:
        if _ENGINE is not None or _ENGINE_TRIED:
            return _ENGINE
        _ENGINE_TRIED = True
        path = find_stockfish()
        if not path:
            return None
        try:
            _ENGINE = Engine(path)
        except Exception:
            _ENGINE = None
        return _ENGINE


def get_play_engine() -> Engine | None:
    """Lazily start the dedicated Stockfish process used for interactive play."""
    global _PLAY_ENGINE, _PLAY_ENGINE_TRIED
    with _PLAY_ENGINE_LOCK:
        if _PLAY_ENGINE is not None or _PLAY_ENGINE_TRIED:
            return _PLAY_ENGINE
        _PLAY_ENGINE_TRIED = True
        path = find_stockfish()
        if not path:
            return None
        try:
            _PLAY_ENGINE = Engine(path)
        except Exception:
            _PLAY_ENGINE = None
        return _PLAY_ENGINE


def engine_info() -> dict:
    path = find_stockfish()
    return {"available": bool(path), "path": path or "",
            "name": _ENGINE.name if _ENGINE else ""}


def play_engine_info() -> dict:
    path = find_stockfish()
    return {"available": bool(path), "path": path or "",
            "name": _PLAY_ENGINE.name if _PLAY_ENGINE else ""}


def _presult_score(presult: str | None) -> float:
    return {"win": 1.0, "draw": 0.5, "loss": 0.0}.get(presult or "", 0.5)


def build_player_dataset(conn, player_id: int) -> dict:
    """Build exact-position persona move stats from this player's PGN rows."""
    with _PLAYER_DATASET_LOCK:
        cached = _PLAYER_DATASET_CACHE.get(player_id)
    if cached is not None:
        return cached

    positions: dict[str, dict] = {}
    replay_errors = []
    rows = conn.execute(
        """SELECT game_id, color, presult, moves_json
           FROM Games WHERE player_id=? AND source='pgn'
           ORDER BY game_id""", (player_id,)).fetchall()
    for r in rows:
        try:
            moves = json.loads(r["moves_json"] or "[]")
        except ValueError:
            replay_errors.append({"game_id": r["game_id"], "error": "bad moves_json"})
            continue
        replay, err = moves_uci_for(moves)
        if err:
            replay_errors.append({"game_id": r["game_id"], "error": err})
        want_even = r["color"] == "white"
        if r["color"] not in ("white", "black"):
            continue
        game_score = _presult_score(r["presult"])
        for ply_index, (fen_before, uci, _fen_after) in enumerate(replay):
            if (ply_index % 2 == 0) != want_even:
                continue
            ply_num = ply_index + 1
            key = epd_key(fen_before)
            entry = positions.setdefault(key, {
                "moves": {},
                "total": 0,
                "games": set(),
                "min_ply": ply_num,
            })
            entry["total"] += 1
            entry["games"].add(r["game_id"])
            entry["min_ply"] = min(entry["min_ply"], ply_num)
            mv = entry["moves"].setdefault(uci, {
                "count": 0,
                "score_sum": 0.0,
                "game_ids": set(),
                "min_ply": ply_num,
            })
            mv["count"] += 1
            mv["score_sum"] += game_score
            mv["game_ids"].add(r["game_id"])
            mv["min_ply"] = min(mv["min_ply"], ply_num)

    opening = {
        key: entry for key, entry in positions.items()
        if entry["min_ply"] <= PLAY_OPENING_PLY_LIMIT
    }
    dataset = {
        "player_id": player_id,
        "games": len(rows),
        "positions": positions,
        "opening": opening,
        "replay_errors": replay_errors,
    }
    with _PLAYER_DATASET_LOCK:
        _PLAYER_DATASET_CACHE[player_id] = dataset
    return dataset


def _persona_candidates(entry: dict) -> list[dict]:
    candidates = []
    total = max(1, int(entry.get("total") or 0))
    for uci, stats in entry.get("moves", {}).items():
        count = int(stats.get("count") or 0)
        if not count:
            continue
        score_rate = float(stats.get("score_sum") or 0.0) / count
        weight = count * (0.25 + score_rate)
        candidates.append({
            "uci": uci,
            "weight": max(0.01, weight),
            "count": count,
            "score_rate": score_rate,
            "source_games": len(stats.get("game_ids") or []),
            "matched_samples": total,
            "matched_share": count / total,
        })
    candidates.sort(key=lambda c: (-c["weight"], c["uci"]))
    return candidates


def _weighted_choice(candidates: list[dict]) -> dict | None:
    if not candidates:
        return None
    total = sum(float(c["weight"]) for c in candidates)
    if total <= 0:
        return candidates[0]
    pick = random.random() * total
    acc = 0.0
    for c in candidates:
        acc += float(c["weight"])
        if pick <= acc:
            return c
    return candidates[-1]


def _engine_choice(top_moves: list[dict]) -> dict | None:
    if not top_moves:
        return None
    choices = top_moves[:max(1, min(PLAY_MULTIPV, len(top_moves)))]
    weights = [max(1, len(choices) - i) for i, _ in enumerate(choices)]
    pick = random.random() * sum(weights)
    acc = 0
    for move, weight in zip(choices, weights):
        acc += weight
        if pick <= acc:
            return move
    return choices[0]


def _normalize_fen_full(fen: str) -> str:
    parts = (fen or "").split()
    if len(parts) == 4:
        return " ".join(parts + ["0", "1"])
    if len(parts) == 6 and parts[1] in ("w", "b"):
        return " ".join(parts)
    raise ValueError("valid FEN required")


def _fen_color_to_move(fen: str) -> str:
    parts = fen.split()
    if len(parts) < 2 or parts[1] not in ("w", "b"):
        raise ValueError("valid FEN required")
    return "white" if parts[1] == "w" else "black"


def _best_score(top_moves: list[dict]) -> int | None:
    vals = [int(m.get("score") or 0) for m in top_moves if m.get("uci")]
    return max(vals) if vals else None


def _candidate_passes_blunder_guard(engine: Engine, fen_full: str, candidate_uci: str,
                                    top_moves: list[dict], elo: int,
                                    movetime_ms: int) -> bool:
    best = _best_score(top_moves)
    if best is None:
        return False
    matching = next((m for m in top_moves if m.get("uci") == candidate_uci), None)
    if matching is not None:
        cand_score = int(matching.get("score") or 0)
    else:
        cand_score = engine.score_move(fen_full, candidate_uci, movetime_ms, elo)
        if cand_score is None:
            return False
    return best - cand_score <= PLAY_BLUNDER_CP


def select_bot_move(conn, player_id: int, fen: str, *, elo: int | None = None,
                    movetime_ms: int = PLAY_MOVETIME_MS,
                    dataset: dict | None = None,
                    engine: Engine | None = None) -> dict:
    """Choose a v1 exact-persona move or rating-limited engine fallback."""
    fen_full = _normalize_fen_full(fen)
    elo = clamp_play_elo(elo)
    dataset = dataset or build_player_dataset(conn, player_id)
    engine = engine or get_play_engine()
    if engine is None:
        raise RuntimeError("No engine available — drop a Stockfish binary in ./stockfish/ "
                           "(or set PREP_STOCKFISH).")

    key = epd_key(fen_full)
    source = None
    if key in dataset.get("opening", {}):
        source = ("opening", dataset["opening"][key])
    elif key in dataset.get("positions", {}):
        source = ("exact", dataset["positions"][key])

    with _PLAY_ENGINE_LOCK:
        top = engine.top_moves(fen_full, PLAY_MULTIPV, movetime_ms, elo)
        if source is not None:
            basis, entry = source
            candidate = _weighted_choice(_persona_candidates(entry))
            if candidate and _candidate_passes_blunder_guard(
                    engine, fen_full, candidate["uci"], top, elo, movetime_ms):
                return {
                    "uci": candidate["uci"],
                    "basis": basis,
                    "confidence": round(float(candidate["matched_share"]), 3),
                    "source_games": int(candidate["source_games"]),
                    "matched_samples": int(candidate["matched_samples"]),
                    "matched_share": round(float(candidate["matched_share"]), 3),
                    "elo": elo,
                }

        chosen = _engine_choice(top)
        if not chosen:
            raise RuntimeError("engine returned no legal move")
        return {
            "uci": chosen["uci"],
            "basis": "engine",
            "confidence": 0.0,
            "source_games": 0,
            "matched_samples": 0,
            "matched_share": 0.0,
            "elo": elo,
        }


def play_players_payload(conn) -> dict:
    rows = conn.execute(
        """SELECT r.player_id, r.real_name, r.title, r.federation, r.fide, r.is_hero,
                  COUNT(g.game_id) AS pgn_games
           FROM Roster r JOIN Games g ON g.player_id=r.player_id AND g.source='pgn'
           GROUP BY r.player_id
           HAVING pgn_games > 0
           ORDER BY r.is_hero DESC, r.fide DESC, r.real_name"""
    ).fetchall()
    players = []
    for r in rows:
        fide = r["fide"] if r["fide"] is not None else PLAY_DEFAULT_ELO
        players.append({
            "player_id": r["player_id"],
            "real_name": r["real_name"],
            "title": r["title"],
            "federation": r["federation"],
            "fide": r["fide"],
            "is_hero": bool(r["is_hero"]),
            "pgn_games": r["pgn_games"],
            "default_elo": clamp_play_elo(fide),
        })
    return {
        "players": players,
        "engine": play_engine_info(),
        "clock_presets": PLAY_CLOCK_PRESETS,
        "default_clock": PLAY_CLOCK_PRESETS[0],
        "elo_min": PLAY_ELO_MIN,
        "elo_max": PLAY_ELO_MAX,
        "movetime_ms": PLAY_MOVETIME_MS,
    }


def eval_position(conn, fen_full: str, depth: int = ENGINE_DEPTH,
                  allow_engine: bool = True) -> tuple[int, str | None] | None:
    """White-POV (score_cp, bestmove_uci) for a position. Cached in PositionEval
    by the 4-field FEN key. Falls back to Lichess cloud-eval when online and no
    local engine. Returns None if nothing can evaluate it."""
    key = epd_key(fen_full)
    row = conn.execute(
        "SELECT score_cp, bestmove FROM PositionEval WHERE fen=? AND depth=?",
        (key, depth)).fetchone()
    if row is not None:
        return row["score_cp"], row["bestmove"]
    if not allow_engine:
        return None
    score = None
    best = None
    src = None
    eng = get_engine()
    if eng is not None:
        with _ENGINE_LOCK:
            cp, mate, best = eng.analyse(key + " 0 1", depth)
        score = fold_score(cp, mate, _white_to_move(key))
        src = eng.name
    elif ONLINE_ENABLED:
        res = cloud_eval(key)
        if res is not None:
            score, best = res
            src = "lichess-cloud"
    if score is None:
        return None
    conn.execute(
        "INSERT OR REPLACE INTO PositionEval (fen, depth, score_cp, bestmove, source) "
        "VALUES (?,?,?,?,?)", (key, depth, int(score), best, src))
    return int(score), best


# --- UCI move -> readable long-algebraic (for showing the engine's best move) -
def uci_to_long(fen: str, uci: str | None) -> str:
    """g1f3 -> 'Ng1-f3', e7e8q -> 'e7-e8=Q', e1g1 -> 'O-O'. Uses the FEN board to
    name the piece and detect captures. Pretty enough for prep notes; no
    disambiguation/check marks needed because squares are explicit."""
    if not uci or len(uci) < 4:
        return uci or "?"
    board = fen.split()[0]
    sq: dict[str, str] = {}
    rank, file = 8, 0
    for ch in board:
        if ch == "/":
            rank, file = rank - 1, 0
        elif ch.isdigit():
            file += int(ch)
        else:
            sq[FILES_STR[file] + str(rank)] = ch
            file += 1
    frm, to, promo = uci[:2], uci[2:4], uci[4:5]
    piece = sq.get(frm, "")
    pt = piece.upper()
    if pt == "K" and frm in ("e1", "e8") and to in ("g1", "g8", "c1", "c8"):
        return "O-O" if to[0] == "g" else "O-O-O"
    capture = to in sq or (pt == "P" and frm[0] != to[0])
    head = "" if pt == "P" else pt
    s = f"{head}{frm}{'x' if capture else '-'}{to}"
    if promo:
        s += "=" + promo.upper()
    return s


def cp_to_pawns(cp: int) -> str:
    """Format a White-POV/side-POV centipawn scalar as a pawn string (#-mate aware)."""
    if cp >= MATE_CP - 1000:
        return f"#{MATE_CP - cp}"
    if cp <= -(MATE_CP - 1000):
        return f"#-{MATE_CP + cp}"
    return f"{cp / 100:+.1f}"


# --- online opt-in (Lichess) — OFF by default ------------------------------
def _http_get_json(url: str) -> dict | None:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "prep_manual_app"})
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as r:
            return json.load(r)
    except Exception:
        return None


def cloud_eval(epd: str) -> tuple[int, str | None] | None:
    """Lichess cloud eval (White POV cp) for a position; eval fallback when no
    local engine. Returns (score_cp, bestmove_uci) or None."""
    if not ONLINE_ENABLED:
        return None
    data = _http_get_json(LICHESS_CLOUD_EVAL + "?" +
                          urllib.parse.urlencode({"fen": epd}))
    pvs = (data or {}).get("pvs") or []
    if not pvs:
        return None
    pv = pvs[0]
    if pv.get("mate") is not None:
        m = pv["mate"]
        score = (MATE_CP - abs(m)) * (1 if m > 0 else -1)
    else:
        score = pv.get("cp")
    if score is None:
        return None
    moves = (pv.get("moves") or "").split()
    return int(score), (moves[0] if moves else None)


def explorer_lookup(conn, epd: str, scope: str = "masters") -> dict | None:
    """Lichess opening-explorer population stats for a position (cached). Used to
    add real theory context to generated dossiers when online is enabled."""
    row = conn.execute("SELECT json FROM ExplorerCache WHERE fen=? AND scope=?",
                        (epd, scope)).fetchone()
    if row is not None:
        return json.loads(row["json"])
    if not ONLINE_ENABLED:
        return None
    base = LICHESS_EXPLORER + ("/masters" if scope == "masters" else "/lichess")
    data = _http_get_json(base + "?" + urllib.parse.urlencode({"fen": epd}))
    if data is None:
        return None
    conn.execute("INSERT OR REPLACE INTO ExplorerCache (fen, scope, json, fetched_at) "
                 "VALUES (?,?,?,?)",
                 (epd, scope, json.dumps(data), dt.datetime.now().isoformat(timespec="seconds")))
    conn.commit()
    return data


# ===========================================================================
# PGN PARSING
# ===========================================================================
HEADER_RE = re.compile(r'^\[(\w+)\s+"(.*)"\]\s*$', re.MULTILINE)


def split_pgn_stream(raw: str) -> list[str]:
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


def clean_movetext(text: str) -> list[str]:
    text = re.sub(r"\{[^}]*\}", " ", text)
    depth_guard = 0
    while "(" in text and depth_guard < 50:
        text = re.sub(r"\([^()]*\)", " ", text)
        depth_guard += 1
    text = re.sub(r"\$\d+", " ", text)
    text = re.sub(r"\d+\.+", " ", text)
    out = []
    for tok in text.split():
        if tok in ("1-0", "0-1", "1/2-1/2", "*") or set(tok) <= {"."}:
            continue
        tok = re.sub(r"[?!]+$", "", tok)
        if tok:
            out.append(tok)
    return out


def parse_pgn_game(pgn: str) -> dict | None:
    headers = dict(HEADER_RE.findall(pgn))
    if not headers:
        return None
    last = 0
    for m in HEADER_RE.finditer(pgn):
        last = m.end()
    moves = clean_movetext(pgn[last:])
    return {"headers": headers, "moves": moves}


# ===========================================================================
# OPENING CLASSIFICATION (move-based, so headerless OTB PGNs work)
# ===========================================================================
BOOK: list[tuple[str, str, str]] = [
    # --- Sicilian ---
    ("e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 a6", "Sicilian: Najdorf", "B90"),
    ("e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6 Nc3 g6", "Sicilian: Dragon", "B70"),
    ("e4 c5 Nf3 d6 d4 cxd4 Qxd4", "Sicilian: 4.Qxd4 (Chekhover-style)", "B53"),
    ("e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 g6", "Sicilian: Accelerated Dragon", "B34"),
    ("e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 e5", "Sicilian: Sveshnikov/Kalashnikov", "B32"),
    ("e4 c5 Nf3 e6 d4 cxd4 Nxd4 a6", "Sicilian: Kan", "B42"),
    ("e4 c5 Nf3 e6 d4 cxd4 Nxd4 Nc6", "Sicilian: Taimanov", "B46"),
    ("e4 c5 Nf3 d6 Bb5+", "Sicilian: Moscow Variation (3.Bb5+)", "B51"),
    ("e4 c5 Nf3 Nc6 Bb5", "Sicilian: Rossolimo (3.Bb5)", "B30"),
    ("e4 c5 Nf3 d6 d4", "Sicilian: Open (2...d6)", "B50"),
    ("e4 c5 Nf3 Nc6 d4", "Sicilian: Open (2...Nc6)", "B32"),
    ("e4 c5 Nf3 e6 d4", "Sicilian: Open (2...e6)", "B40"),
    ("e4 c5 Nf3 e6", "Sicilian: 2...e6", "B40"),
    ("e4 c5 Nf3 g6", "Sicilian: Hyperaccelerated Dragon", "B27"),
    ("e4 c5 c3", "Sicilian: Alapin (2.c3)", "B22"),
    ("e4 c5 Nc3 Nc6 f4", "Sicilian: Grand Prix Attack", "B23"),
    ("e4 c5 Nc3", "Sicilian: Closed", "B23"),
    ("e4 c5 f4", "Sicilian: McDonnell/Grand Prix (2.f4)", "B21"),
    ("e4 c5 d4 cxd4 c3", "Sicilian: Smith-Morra Gambit", "B21"),
    ("e4 c5 d4", "Sicilian: 2.d4", "B21"),
    ("e4 c5 b4", "Sicilian: Wing Gambit", "B20"),
    ("e4 c5 g3", "Sicilian: 2.g3 (Closed setup)", "B20"),
    ("e4 c5 Bc4", "Sicilian: Bowdler Attack", "B20"),
    ("e4 c5 b3", "Sicilian: 2.b3", "B20"),
    ("e4 c5", "Sicilian Defence", "B20"),
    # --- Caro-Kann ---
    ("e4 c6 d4 d5 e5", "Caro-Kann: Advance", "B12"),
    ("e4 c6 d4 d5 exd5 cxd5 c4", "Caro-Kann: Panov-Botvinnik Attack", "B13"),
    ("e4 c6 d4 d5 exd5", "Caro-Kann: Exchange", "B13"),
    ("e4 c6 d4 d5 Nc3", "Caro-Kann: Main Line (3.Nc3)", "B15"),
    ("e4 c6 d4 d5 Nd2", "Caro-Kann: Main Line (3.Nd2)", "B15"),
    ("e4 c6 d4 d5 f3", "Caro-Kann: Fantasy Variation", "B12"),
    ("e4 c6 c4", "Caro-Kann: Accelerated Panov (2.c4)", "B10"),
    ("e4 c6 Nc3", "Caro-Kann: Two Knights", "B10"),
    ("e4 c6", "Caro-Kann Defence", "B10"),
    # --- French ---
    ("e4 e6 d4 d5 e5", "French: Advance", "C02"),
    ("e4 e6 d4 d5 Nc3 Bb4", "French: Winawer", "C15"),
    ("e4 e6 d4 d5 Nc3", "French: Classical/Steinitz complex", "C10"),
    ("e4 e6 d4 d5 Nd2", "French: Tarrasch", "C03"),
    ("e4 e6 d4 d5 exd5", "French: Exchange", "C01"),
    ("e4 e6", "French Defence", "C00"),
    # --- 1.e4 e5 ---
    ("e4 e5 Nf3 Nc6 Bb5 a6", "Ruy Lopez: Morphy Defence", "C70"),
    ("e4 e5 Nf3 Nc6 Bb5", "Ruy Lopez", "C60"),
    ("e4 e5 Nf3 Nc6 Bc4 Bc5", "Italian: Giuoco Piano", "C50"),
    ("e4 e5 Nf3 Nc6 Bc4 Nf6", "Italian: Two Knights Defence", "C55"),
    ("e4 e5 Nf3 Nc6 Bc4", "Italian Game", "C50"),
    ("e4 e5 Nf3 Nc6 d4", "Scotch Game", "C45"),
    ("e4 e5 Nf3 Nc6 Nc3", "Three/Four Knights Game", "C46"),
    ("e4 e5 Nf3 Nf6", "Petroff Defence", "C42"),
    ("e4 e5 Nf3 d6", "Philidor Defence", "C41"),
    ("e4 e5 d4 exd4 Qxd4", "Centre Game (3.Qxd4)", "C21"),
    ("e4 e5 d4", "Centre Game / Danish complex", "C21"),
    ("e4 e5 f4", "King's Gambit", "C30"),
    ("e4 e5 Nc3", "Vienna Game", "C25"),
    ("e4 e5 Bc4", "Bishop's Opening", "C23"),
    ("e4 e5", "Open Game (1.e4 e5)", "C20"),
    # --- other 1.e4 ---
    ("e4 d5", "Scandinavian Defence", "B01"),
    ("e4 Nf6", "Alekhine Defence", "B02"),
    ("e4 d6", "Pirc/Modern complex", "B07"),
    ("e4 g6", "Modern Defence", "B06"),
    ("e4 b6", "Owen Defence", "B00"),
    ("e4 Nc6", "Nimzowitsch Defence", "B00"),
    ("e4", "King's Pawn Opening", "B00"),
    # --- 1.d4 ---
    ("d4 d5 c4 e6 Nf3 Nf6 g3", "Catalan", "E01"),
    ("d4 Nf6 c4 e6 g3 d5", "Catalan", "E01"),
    ("d4 Nf6 c4 e6 g3", "Catalan move order", "E00"),
    ("d4 d5 c4 e6 Nc3 c5", "Tarrasch Defence (QGD)", "D32"),
    ("d4 d5 c4 e6", "Queen's Gambit Declined", "D30"),
    ("d4 d5 c4 c6 Nf3 Nf6 Nc3 e6", "Semi-Slav", "D43"),
    ("d4 d5 c4 c6", "Slav Defence", "D10"),
    ("d4 d5 c4 dxc4", "Queen's Gambit Accepted", "D20"),
    ("d4 d5 c4 Nc6", "Chigorin Defence", "D07"),
    ("d4 d5 c4 e5", "Albin Counter-Gambit", "D08"),
    ("d4 d5 c4", "Queen's Gambit", "D06"),
    ("d4 d5 Nf3 Nf6 c4 e6", "Queen's Gambit Declined", "D30"),
    ("d4 d5 Nf3 Nf6 c4 c6", "Slav Defence", "D10"),
    ("d4 d5 Nf3 Nf6 c4 dxc4", "Queen's Gambit Accepted", "D20"),
    ("d4 d5 Bf4", "London System", "D02"),
    ("d4 d5 Nf3 Nf6 Bf4", "London System", "D02"),
    ("d4 Nf6 Nf3 d5 Bf4", "London System", "D02"),
    ("d4 Nf6 Nf3 e6 Bf4", "London System", "A47"),
    ("d4 Nf6 Nf3 g6 Bf4", "London vs King's Indian setup", "A48"),
    ("d4 d5 Nf3 Nf6 e3", "Colle System", "D04"),
    ("d4 d5 e3", "Stonewall/Colle complex", "D00"),
    ("d4 d5 Bg5", "Levitsky Attack", "D00"),
    ("d4 d5 Nc3", "Veresov/Jobava complex", "D01"),
    ("d4 Nf6 c4 e6 Nc3 Bb4", "Nimzo-Indian", "E20"),
    ("d4 Nf6 c4 e6 Nf3 b6", "Queen's Indian", "E12"),
    ("d4 Nf6 c4 e6 Nf3 Bb4+", "Bogo-Indian", "E11"),
    ("d4 Nf6 c4 e6 Nf3 d5", "Queen's Gambit Declined", "D30"),
    ("d4 Nf6 c4 e6", "Indian: 2...e6 complex", "E10"),
    ("d4 Nf6 c4 g6 Nc3 d5", "Grünfeld Defence", "D80"),
    ("d4 Nf6 c4 g6 Nf3 Bg7 g3", "King's Indian: Fianchetto", "E62"),
    ("d4 Nf6 c4 g6 g3", "KID/Grünfeld: Fianchetto move order", "E60"),
    ("d4 Nf6 c4 g6 Nc3 Bg7 e4", "King's Indian: Mainline (e4)", "E70"),
    ("d4 Nf6 c4 g6", "King's Indian / Grünfeld complex", "E60"),
    ("d4 Nf6 c4 c5 d5 b5", "Benko Gambit", "A57"),
    ("d4 Nf6 c4 c5 d5 e6", "Modern Benoni", "A60"),
    ("d4 Nf6 c4 c5", "Benoni structures", "A56"),
    ("d4 Nf6 c4 d6", "Old Indian / KID move order", "A53"),
    ("d4 Nf6 Bg5", "Trompowsky Attack", "A45"),
    ("d4 Nf6 Bf4", "London System", "A45"),
    ("d4 Nf6 Nf3 g6 g3", "Fianchetto vs King's Indian", "E60"),
    ("d4 Nf6 Nf3 g6", "Indian: Nf3 + ...g6 complex", "A48"),
    ("d4 Nf6 Nf3 e6", "Indian: Nf3 + ...e6 complex", "A46"),
    ("d4 Nf6 Nf3", "Indian Game: 2.Nf3", "A46"),
    ("d4 Nf6", "Indian Game", "A45"),
    ("d4 f5", "Dutch Defence", "A80"),
    ("d4 e6 c4 f5", "Dutch Defence", "A84"),
    ("d4 g6", "Modern Defence vs d4", "A40"),
    ("d4 d6", "Old Indian/Modern complex", "A41"),
    ("d4 e6", "Horwitz Defence", "A40"),
    ("d4 d5", "Queen's Pawn Game", "D00"),
    ("d4", "Queen's Pawn Opening", "A40"),
    # --- 1.c4 / 1.Nf3 / others ---
    ("c4 e5 Nc3 Nf6 Nf3 Nc6", "English: Four Knights (Reversed Sicilian)", "A28"),
    ("c4 e5 Nc3 Nc6 g3", "English: Closed (Reversed Sicilian)", "A25"),
    ("c4 e5", "English: King's English (Reversed Sicilian)", "A20"),
    ("c4 Nf6 Nc3 e5", "English: Reversed Sicilian", "A22"),
    ("c4 c5", "English: Symmetrical", "A30"),
    ("c4 e6", "English: Agincourt", "A13"),
    ("c4 c6", "English: Caro/Slav setup", "A11"),
    ("c4 Nf6", "English: Anglo-Indian", "A15"),
    ("c4 g6", "English: vs Modern setup", "A10"),
    ("c4 f5", "English: Anglo-Dutch", "A10"),
    ("c4", "English Opening", "A10"),
    ("Nf3 d5 c4", "Réti Opening", "A09"),
    ("Nf3 d5 g3", "Réti / King's Indian Attack", "A07"),
    ("Nf3 d5 b3", "Nimzo-Larsen vs ...d5", "A06"),
    ("Nf3 Nf6 c4", "English/Réti: Anglo-Indian", "A15"),
    ("Nf3 Nf6 g3", "King's Indian Attack setup", "A05"),
    ("Nf3 c5 c4", "English: Symmetrical (Réti order)", "A30"),
    ("Nf3 d5", "Zukertort Opening", "A06"),
    ("Nf3 Nf6", "Zukertort: 1...Nf6", "A05"),
    ("Nf3", "Réti/Zukertort Opening", "A04"),
    ("b3", "Nimzo-Larsen Attack", "A01"),
    ("f4", "Bird's Opening", "A02"),
    ("g3", "King's Fianchetto Opening", "A00"),
    ("b4", "Sokolsky Opening", "A00"),
    ("Nc3", "Van Geet Opening", "A00"),
    ("e3", "Van't Kruijs Opening", "A00"),
    ("d3", "Mieses Opening", "A00"),
]
# normalize check marks so book prefixes match the stripped move stream
BOOK = [(" ".join(m.rstrip("+#") for m in seq.split()), nm, ec) for seq, nm, ec in BOOK]
BOOK.sort(key=lambda t: -len(t[0]))


def classify_opening(moves: list[str]) -> tuple[str, str]:
    """Return (opening name, approx ECO) from the SAN move list."""
    if not moves:
        return ("(no moves)", "")
    mv = [m.rstrip("+#") for m in moves[:14]]
    s = " ".join(mv)
    name, eco = "Irregular Opening", "A00"
    for seq, nm, ec in BOOK:
        if s == seq or s.startswith(seq + " "):
            name, eco = nm, ec
            break
    w6 = set(mv[0::2][:6])
    b6 = set(mv[1::2][:6])
    # feature refinements for transpositional systems
    if {"d4", "c4", "g3"} <= w6 and "g6" not in b6 and ("e6" in b6 or "d5" in b6):
        name, eco = "Catalan", "E01"
    elif name in ("Queen's Pawn Game", "Queen's Pawn Opening", "Indian Game",
                  "Indian Game: 2.Nf3", "Indian: Nf3 + ...e6 complex") and "Bf4" in w6:
        name, eco = "London System", "D02"
    return name, eco


def tag_families(moves: list[str], eco: str = "", opening: str = "") -> list[str]:
    """Tag a game against the 6 Core Structure Families (moves + header fallback)."""
    fams: set[str] = set()
    mv = [m.rstrip("+#") for m in moves[:30]]
    s = " ".join(mv)
    w = mv[0::2]
    b = mv[1::2]
    w8, b8 = set(w[:8]), set(b[:8])

    # 1. Advance Caro-Kann
    if s.startswith("e4 c6 d4 d5 e5") or s.startswith("e4 c6 e5"):
        fams.add(FAM_ADV_CARO)
    # 6. IQP / Panov
    if (s.startswith("e4 c6 d4 d5 exd5 cxd5 c4")
            or s.startswith("e4 c6 c4 d5 exd5 cxd5 d4")
            or s.startswith("d4 d5 c4 dxc4")
            or s.startswith("d4 d5 Nf3 Nf6 c4 dxc4")):
        fams.add(FAM_IQP)
    if mv[:1] == ["d4"] and "c4" in w[:4] and {"d5", "e6", "c5"} <= set(b[:5]):
        fams.add(FAM_IQP)  # Tarrasch-style IQP
    # 2. Reversed Sicilian / Flank Annexation
    if mv[:1] == ["c4"] and "e5" in b[:3]:
        fams.add(FAM_REVSIC)
    if {"Nf3", "g3", "d3", "e4"} <= set(w[:9]) and "c4" not in w[:5] and "d4" not in w[:5]:
        fams.add(FAM_REVSIC)  # King's Indian Attack
    # 3. Fianchetto KID / Grünfeld complexes
    if mv[:1] == ["d4"] and "g6" in b8:
        if "d5" in b[:6] and "c4" in w[:4]:
            fams.add(FAM_KID_GRU)            # Grünfeld
        if "g3" in w[:6] and "c4" in w[:6]:
            fams.add(FAM_KID_GRU)            # Fianchetto KID
    # 4. Catalan / Réti Squeeze
    if {"d4", "c4", "g3"} <= set(w[:6]) and "g6" not in b8:
        fams.add(FAM_CAT_RETI)
    if mv[:1] == ["Nf3"] and "c4" in w[:5] and "d4" not in w[:5] and "d5" in b[:4]:
        fams.add(FAM_CAT_RETI)               # Réti
    if mv[:1] == ["b3"] or (mv[:1] == ["Nf3"] and "b3" in w[:4]):
        fams.add(FAM_CAT_RETI)               # Nimzo-Larsen
    # 5. Anti-Sicilian Counter-Package
    if s.startswith("e4 c5"):
        w2 = w[1] if len(w) > 1 else ""
        w3 = w[2] if len(w) > 2 else ""
        if w2 in ("c3", "Nc3", "f4", "b4", "g3", "b3", "Bc4", "d4"):
            if w2 != "d4" or w3 == "c3":     # 2.d4 cxd4 3.c3 = Smith-Morra
                fams.add(FAM_ANTISIC)
            elif w2 == "d4":
                fams.add(FAM_ANTISIC)        # 2.d4 sidelines incl. Qxd4 recapture
        elif w2 == "Nf3" and w3 and w3 != "d4":
            fams.add(FAM_ANTISIC)            # Rossolimo, Moscow, 3.c3, 3.Bc4 ...
    # header fallback (ECO / Opening tag) for PGNs that have them
    eco = (eco or "").strip().upper()[:3]
    low = (opening or "").lower()

    def eco_in(lo, hi):
        return bool(eco) and lo <= eco <= hi

    if (eco_in("B12", "B12") and "advance" in low) or ("caro" in low and "advance" in low):
        fams.add(FAM_ADV_CARO)
    if eco_in("A20", "A29") or "reversed sicilian" in low or "king's indian attack" in low:
        fams.add(FAM_REVSIC)
    if eco_in("D70", "D99") or eco_in("E60", "E69") or "grunfeld" in low or "grünfeld" in low:
        fams.add(FAM_KID_GRU)
    if eco_in("E01", "E09") or eco_in("A04", "A09") or eco_in("A11", "A14") \
            or "catalan" in low or "reti" in low or "réti" in low:
        fams.add(FAM_CAT_RETI)
    if eco_in("B21", "B26") or eco_in("B30", "B31") or eco_in("B51", "B52"):
        fams.add(FAM_ANTISIC)
    if "panov" in low or ("caro" in low and eco_in("B13", "B14")) \
            or "queen's gambit accepted" in low or "tarrasch def" in low:
        fams.add(FAM_IQP)
    return sorted(fams)


# ===========================================================================
# DATABASE
# ===========================================================================
SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS Roster (
    player_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    real_name   TEXT NOT NULL UNIQUE,
    title       TEXT, federation TEXT, fide INTEGER,
    is_hero     INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS Aliases (
    alias      TEXT PRIMARY KEY,
    player_id  INTEGER NOT NULL REFERENCES Roster(player_id) ON DELETE CASCADE,
    source     TEXT DEFAULT 'auto'
);
CREATE TABLE IF NOT EXISTS IgnoredNames ( alias TEXT PRIMARY KEY );
CREATE TABLE IF NOT EXISTS Files (
    file_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    filename     TEXT UNIQUE,
    games_parsed INTEGER DEFAULT 0,
    scanned_at   TEXT
);
CREATE TABLE IF NOT EXISTS Games (
    game_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id     INTEGER REFERENCES Files(file_id) ON DELETE CASCADE,
    player_id   INTEGER NOT NULL REFERENCES Roster(player_id) ON DELETE CASCADE,
    color       TEXT, presult TEXT,
    white TEXT, black TEXT, result TEXT,
    date TEXT, event TEXT, round TEXT,
    eco TEXT, opening TEXT,
    total_moves INTEGER, moves_json TEXT,
    source TEXT DEFAULT 'pgn',
    lichess_id TEXT,
    dedup_hash  TEXT,
    UNIQUE (player_id, dedup_hash)
);
CREATE TABLE IF NOT EXISTS Tags (
    game_id INTEGER NOT NULL REFERENCES Games(game_id) ON DELETE CASCADE,
    family  TEXT NOT NULL,
    UNIQUE (game_id, family)
);
CREATE TABLE IF NOT EXISTS UnmatchedNames ( name TEXT PRIMARY KEY, games INTEGER );
CREATE INDEX IF NOT EXISTS idx_games_player ON Games(player_id);

-- Optional engine-analysis caches. Keyed by stable values (position FEN / the
-- game dedup_hash) so a full rescan (which rebuilds Games) never wipes them.
CREATE TABLE IF NOT EXISTS PositionEval (
    fen      TEXT NOT NULL,      -- 4-field FEN (board/side/castling/ep)
    depth    INTEGER NOT NULL,
    score_cp INTEGER,            -- White POV; mate folded into a large value
    bestmove TEXT,               -- UCI
    source   TEXT,
    PRIMARY KEY (fen, depth)
);
CREATE TABLE IF NOT EXISTS GameAnalysis (
    dedup_hash  TEXT NOT NULL,
    depth       INTEGER NOT NULL,
    engine      TEXT,
    analyzed_at TEXT,
    acpl_white  REAL, acpl_black REAL,
    moves_white INTEGER, moves_black INTEGER,
    phase_json  TEXT,            -- {white:{op:[sum,cnt],mid,end}, black:{...}}
    blunders_json TEXT,          -- [{ply,mover,move_no,san,sev,loss,before,after,best}]
    PRIMARY KEY (dedup_hash, depth)
);
CREATE TABLE IF NOT EXISTS ExplorerCache (
    fen TEXT NOT NULL, scope TEXT NOT NULL, json TEXT, fetched_at TEXT,
    PRIMARY KEY (fen, scope)
);
"""


def db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA busy_timeout = 8000")
    return conn


def init_db():
    conn = db()
    conn.executescript(SCHEMA)
    cols = {r[1] for r in conn.execute("PRAGMA table_info(Games)")}
    if "lichess_id" not in cols:  # migrate pre-Lichess databases (scan() refills)
        conn.executescript("DROP TABLE IF EXISTS Tags; DROP TABLE IF EXISTS Games;")
        conn.executescript(SCHEMA)
    ga_cols = list(conn.execute("PRAGMA table_info(GameAnalysis)"))
    ga_pk = [r[1] for r in sorted((r for r in ga_cols if r[5]), key=lambda r: r[5])]
    if ga_pk != ["dedup_hash", "depth"]:
        # Older databases keyed GameAnalysis only by dedup_hash, so analysing the
        # same game at a different depth overwrote the prior result. Rebuild the
        # table with the composite key and keep whatever cached rows still exist.
        conn.executescript("""
            DROP TABLE IF EXISTS GameAnalysis_legacy;
            ALTER TABLE GameAnalysis RENAME TO GameAnalysis_legacy;
        """)
        conn.executescript(SCHEMA)
        conn.execute("""
            INSERT OR IGNORE INTO GameAnalysis
                (dedup_hash, depth, engine, analyzed_at, acpl_white, acpl_black,
                 moves_white, moves_black, phase_json, blunders_json)
            SELECT dedup_hash, depth, engine, analyzed_at, acpl_white, acpl_black,
                   moves_white, moves_black, phase_json, blunders_json
            FROM GameAnalysis_legacy
            WHERE dedup_hash IS NOT NULL AND depth IS NOT NULL
        """)
        conn.execute("DROP TABLE GameAnalysis_legacy")
    for p in ROSTER:
        conn.execute(
            """INSERT INTO Roster (real_name, title, federation, fide, is_hero)
               VALUES (?,?,?,?,?)
               ON CONFLICT(real_name) DO UPDATE SET
                 title=excluded.title, federation=excluded.federation,
                 fide=excluded.fide, is_hero=excluded.is_hero""",
            (p["real_name"], p["title"], p["federation"], p["fide"], p["is_hero"]))
    # Prune roster rows no longer in ROSTER (e.g. players dropped from the pool);
    # their games cascade-delete and are re-added on the next scan if present.
    names = [p["real_name"] for p in ROSTER]
    conn.execute(
        f"DELETE FROM Roster WHERE real_name NOT IN ({','.join('?' * len(names))})",
        names)
    hero_id = conn.execute("SELECT player_id FROM Roster WHERE is_hero=1").fetchone()[0]
    for a in HERO_ALIASES:
        conn.execute("INSERT OR IGNORE INTO Aliases (alias, player_id, source) VALUES (?,?,'seed')",
                     (a, hero_id))
    for alias, real_name in ROSTER_ALIASES.items():
        row = conn.execute("SELECT player_id FROM Roster WHERE real_name=?", (real_name,)).fetchone()
        if row:
            conn.execute("INSERT OR IGNORE INTO Aliases (alias, player_id, source) VALUES (?,?,'seed')",
                         (alias, row[0]))
    conn.commit()
    conn.close()


# --- name matching --------------------------------------------------------
def name_tokens(s: str) -> list[str]:
    s = re.sub(r"[.,;()\"']", " ", s.lower())
    return [t for t in s.split() if t not in TITLE_WORDS]


_roster_tokens_cache: list[tuple[int, set]] | None = None


def roster_token_sets(conn) -> list[tuple[int, set]]:
    global _roster_tokens_cache
    if _roster_tokens_cache is None:
        _roster_tokens_cache = [
            (r["player_id"], set(name_tokens(r["real_name"])))
            for r in conn.execute("SELECT player_id, real_name FROM Roster")
        ]
    return _roster_tokens_cache


def auto_match(conn, name: str) -> int | None:
    toks = set(name_tokens(name))
    if not toks:
        return None
    scored = []
    for pid, rset in roster_token_sets(conn):
        inter = toks & rset
        if inter:
            scored.append((len(inter), pid))
    if not scored:
        return None
    scored.sort(reverse=True)
    best, pid = scored[0]
    second = scored[1][0] if len(scored) > 1 else 0
    if best >= 2 and best > second:
        return pid
    return None


def resolve_name(conn, name: str) -> int | None:
    key = name.strip().lower()
    if not key:
        return None
    row = conn.execute("SELECT player_id FROM Aliases WHERE alias=?", (key,)).fetchone()
    if row:
        return row["player_id"]
    pid = auto_match(conn, name)
    if pid is not None:
        conn.execute("INSERT OR IGNORE INTO Aliases (alias, player_id, source) VALUES (?,?,'auto')",
                     (key, pid))
        return pid
    return None


def presult_for(result: str, color: str) -> str:
    if result == "1/2-1/2":
        return "draw"
    if (result == "1-0" and color == "white") or (result == "0-1" and color == "black"):
        return "win"
    if result in ("1-0", "0-1"):
        return "loss"
    return "unknown"


def tc_label(tc: str) -> str:
    m = re.match(r"(\d+)\+(\d+)", tc or "")
    if not m:
        return tc or "?"
    total = int(m.group(1)) + 40 * int(m.group(2))
    if total < 30:
        return "ultrabullet"
    if total < 180:
        return "bullet"
    if total < 480:
        return "blitz"
    if total < 1500:
        return "rapid"
    return "classical"


def lichess_pool_rows() -> tuple[str, list[dict]]:
    """Read the Lichess scout games (tournament_pool_2026.db, or its CSV export)."""
    if LICHESS_DB.exists():
        try:
            src = sqlite3.connect(str(LICHESS_DB))
            src.row_factory = sqlite3.Row
            try:
                rows = [dict(r) for r in src.execute(
                    """SELECT p.real_name, g.lichess_game_id, g.date_utc, g.white,
                              g.black, g.result, g.player_color, g.player_result,
                              g.eco, g.opening, g.total_moves, g.time_control, g.variant
                       FROM Games g JOIN Players p ON p.player_id = g.player_id""")]
                return LICHESS_DB.name, rows
            finally:
                src.close()
        except sqlite3.Error:
            pass
    if LICHESS_CSV.exists():
        try:
            with open(LICHESS_CSV, newline="", encoding="utf-8-sig") as fh:
                return LICHESS_CSV.name, list(csv.DictReader(fh))
        except OSError:
            pass
    return "", []


def ingest_lichess_pool(conn, summary: dict):
    src_name, rows = lichess_pool_rows()
    if not rows:
        return
    cur = conn.execute(
        "INSERT INTO Files (filename, games_parsed, scanned_at) VALUES (?,?,?)",
        (f"{src_name} (Lichess scout)", 0,
         dt.datetime.now().isoformat(timespec="seconds")))
    file_id = cur.lastrowid
    parsed = 0
    for r in rows:
        if (r.get("variant") or "Standard") != "Standard":
            continue
        pid = resolve_name(conn, r.get("real_name") or "")
        if pid is None:
            continue
        parsed += 1
        summary["games_seen"] += 1
        eco = (r.get("eco") or "").strip()
        opening = (r.get("opening") or "").strip() or "(unclassified)"
        lid = (r.get("lichess_game_id") or "").strip()
        try:
            total_moves = int(r.get("total_moves") or 0)
        except (TypeError, ValueError):
            total_moves = 0
        tc = r.get("time_control") or ""
        dedup = f"lichess:{lid}" if lid else hashlib.md5(
            repr(sorted(r.items())).encode("utf-8", "replace")).hexdigest()
        cur = conn.execute(
            """INSERT OR IGNORE INTO Games
               (file_id, player_id, color, presult, white, black, result,
                date, event, round, eco, opening, total_moves, moves_json,
                source, lichess_id, dedup_hash)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (file_id, pid, r.get("player_color") or "unknown",
             r.get("player_result") or "unknown",
             r.get("white") or "?", r.get("black") or "?", r.get("result") or "*",
             r.get("date_utc") or "", f"Lichess {tc_label(tc)} ({tc})", "",
             eco, opening, total_moves, json.dumps([]), "lichess", lid, dedup))
        if cur.rowcount:
            summary["games_stored"] += 1
            gid = cur.lastrowid
            for fam in tag_families([], eco, opening):
                conn.execute("INSERT OR IGNORE INTO Tags (game_id, family) VALUES (?,?)",
                             (gid, fam))
    conn.execute("UPDATE Files SET games_parsed=? WHERE file_id=?", (parsed, file_id))
    summary["files"] += 1


def scan(conn) -> dict:
    """Full rebuild: re-ingest every *.pgn in the folder (aliases are kept)."""
    with _PLAYER_DATASET_LOCK:
        _PLAYER_DATASET_CACHE.clear()
    conn.execute("DELETE FROM Games")
    conn.execute("DELETE FROM Files")
    conn.execute("DELETE FROM UnmatchedNames")
    unmatched: Counter = Counter()
    summary = {"files": 0, "games_seen": 0, "games_stored": 0}

    for path in sorted(BASE_DIR.rglob("*.pgn")):  # recurse into subfolders (e.g. chessbasepgn/)
        try:
            raw = path.read_text(encoding="utf-8-sig", errors="replace")
        except OSError:
            continue
        blocks = split_pgn_stream(raw)
        cur = conn.execute(
            "INSERT INTO Files (filename, games_parsed, scanned_at) VALUES (?,?,?)",
            (path.name, 0, dt.datetime.now().isoformat(timespec="seconds")))
        file_id = cur.lastrowid
        parsed = 0
        for block in blocks:
            g = parse_pgn_game(block)
            if not g or not g["headers"]:
                continue
            h = g["headers"]
            moves = g["moves"]
            white = h.get("White", "?").strip()
            black = h.get("Black", "?").strip()
            result = h.get("Result", "*")
            parsed += 1
            summary["games_seen"] += 1
            # Opening: prefer the bundled ECO database (replay first ~36 plies and
            # look the position up), fall back to the hand-built BOOK. A PGN's own
            # ECO/Opening headers still win when present (unchanged precedence).
            db_cls = classify_opening_db(fens_for(moves[:36])[0])
            if db_cls:
                opening, eco_guess = db_cls
            else:
                opening, eco_guess = classify_opening(moves)
            eco = h.get("ECO", "").strip() or eco_guess
            if h.get("Opening"):
                opening = h["Opening"]
            fams = tag_families(moves, eco, opening)
            dedup = hashlib.md5(
                f"{white}|{black}|{h.get('Date','')}|{result}|{' '.join(moves[:40])}"
                .encode("utf-8", "replace")).hexdigest()
            for name, color in ((white, "white"), (black, "black")):
                pid = resolve_name(conn, name)
                if pid is None:
                    if name and name not in ("?", "NN"):
                        unmatched[name] += 1
                    continue
                cur = conn.execute(
                    """INSERT OR IGNORE INTO Games
                       (file_id, player_id, color, presult, white, black, result,
                        date, event, round, eco, opening, total_moves, moves_json, dedup_hash)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (file_id, pid, color, presult_for(result, color), white, black,
                     result, h.get("Date", ""), h.get("Event", ""), h.get("Round", ""),
                     eco, opening, (len(moves) + 1) // 2, json.dumps(moves), dedup))
                if cur.rowcount:
                    summary["games_stored"] += 1
                    gid = cur.lastrowid
                    for fam in fams:
                        conn.execute("INSERT OR IGNORE INTO Tags (game_id, family) VALUES (?,?)",
                                     (gid, fam))
        conn.execute("UPDATE Files SET games_parsed=? WHERE file_id=?", (parsed, file_id))
        summary["files"] += 1

    ingest_lichess_pool(conn, summary)

    ignored = {r["alias"] for r in conn.execute("SELECT alias FROM IgnoredNames")}
    for name, n in unmatched.items():
        if name.strip().lower() not in ignored:
            conn.execute("INSERT OR REPLACE INTO UnmatchedNames (name, games) VALUES (?,?)",
                         (name, n))
    conn.commit()
    return summary


# ===========================================================================
# ENGINE ANALYSIS — optional; powers the engine-backed blunder findings and the
# opponent "fingerprints". GET endpoints read cached results only (allow_engine
# = False); the heavy pass runs via analyze_all() (the Analyze button / --analyze).
# ===========================================================================
PHASE_KEYS = ("op", "mid", "end")
PHASE_LABEL = {"op": "opening", "mid": "middlegame", "end": "endgame"}

# Progress for the background analysis pass (read by /api/state).
ANALYZE_STATUS: dict = {"running": False, "current": 0, "total": 0,
                        "scope": "", "started": None}


def _phase_of(ply: int) -> str:
    return "op" if ply < 20 else ("mid" if ply < 40 else "end")


def _empty_phase() -> dict:
    return {"op": [0.0, 0], "mid": [0.0, 0], "end": [0.0, 0]}


def _mean(sum_cnt: list) -> float | None:
    return round(sum_cnt[0] / sum_cnt[1], 1) if sum_cnt[1] else None


def _score_impact(before_cp: int | float | None,
                  after_cp: int | float | None) -> float:
    """Expected-score loss from the mover's point of view, rounded for display."""
    return round(profile_engine.expected_points_drop(before_cp, after_cp), 3)


def _impact_pct(impact: int | float | None) -> float:
    return round(100.0 * float(impact or 0), 1)


def _practical_severity(loss_cp: int | float | None,
                        impact: int | float | None) -> str:
    """Prefer practical outcome damage over raw cp loss for training labels."""
    cp_loss = float(loss_cp or 0)
    ep_loss = float(impact or 0)
    if ep_loss >= EP_BLUNDER:
        return "blunder"
    if ep_loss >= EP_MISTAKE:
        return "mistake"
    if ep_loss >= EP_INACCURACY or cp_loss >= CP_INACCURACY:
        return "inaccuracy"
    return "good"


def _normalize_analysis_moves(moves: list[dict]) -> list[dict]:
    """Add current practical-impact fields to cached analysis rows."""
    out = []
    for move in moves:
        m = dict(move)
        impact = _score_impact(m.get("before"), m.get("after"))
        m["impact"] = impact
        m["impact_pct"] = _impact_pct(impact)
        m["sev"] = _practical_severity(m.get("loss"), impact)
        out.append(m)
    return out


def _rollup_from_row(row) -> dict:
    return {
        "depth": row["depth"], "engine": row["engine"],
        "acpl_white": row["acpl_white"], "acpl_black": row["acpl_black"],
        "moves_white": row["moves_white"], "moves_black": row["moves_black"],
        "phases": json.loads(row["phase_json"] or "{}"),
        "moves": _normalize_analysis_moves(json.loads(row["blunders_json"] or "[]")),
    }


def analyze_game(conn, dedup_hash: str, moves: list[str], depth: int = ENGINE_DEPTH,
                 allow_engine: bool = True, force: bool = False) -> dict | None:
    """Engine rollup for one game, cached by (dedup_hash, depth). Centipawn loss
    is measured per move vs the engine's best; results feed blunder findings and
    fingerprints. Returns None when not cached and analysis can't run."""
    if not force:
        row = conn.execute("SELECT * FROM GameAnalysis WHERE dedup_hash=? AND depth=?",
                           (dedup_hash, depth)).fetchone()
        # Cache-only callers (GET/export) display whatever analysis exists, even if
        # it was computed at a different depth. The analysis pass (allow_engine=True)
        # instead recomputes at its requested depth when the exact row is missing.
        if row is None and not allow_engine:
            row = conn.execute("SELECT * FROM GameAnalysis WHERE dedup_hash=? "
                               "ORDER BY depth DESC LIMIT 1", (dedup_hash,)).fetchone()
        if row is not None:
            return _rollup_from_row(row)
    if not allow_engine or (get_engine() is None and not ONLINE_ENABLED):
        return None

    fens, _ = fens_for(moves)
    n = len(fens)
    evals: dict[int, tuple[int, str | None] | None] = {}
    for k in range(ANALYZE_FROM_PLY, min(n, ANALYZE_TO_PLY + 1)):
        evals[k] = eval_position(conn, fens[k], depth)

    phases = {"white": _empty_phase(), "black": _empty_phase()}
    sums = {"white": [0.0, 0], "black": [0.0, 0]}
    sig: list[dict] = []
    for k in range(ANALYZE_FROM_PLY, min(n - 1, ANALYZE_TO_PLY)):
        eb, ea = evals.get(k), evals.get(k + 1)
        if eb is None or ea is None:
            continue
        white_moved = (k % 2 == 0)
        side = "white" if white_moved else "black"
        eb_cp, ea_cp = eb[0], ea[0]
        loss = (eb_cp - ea_cp) if white_moved else (ea_cp - eb_cp)
        loss = max(0, min(loss, 1500))      # cap so one disaster can't wreck the mean
        ph = _phase_of(k)
        phases[side][ph][0] += loss
        phases[side][ph][1] += 1
        sums[side][0] += loss
        sums[side][1] += 1
        before_cp = eb_cp if white_moved else -eb_cp
        after_cp = ea_cp if white_moved else -ea_cp
        impact = _score_impact(before_cp, after_cp)
        if loss >= CP_INACCURACY or impact >= EP_INACCURACY:
            sev = _practical_severity(loss, impact)
            sig.append({
                "ply": k, "mover": side, "move_no": k // 2 + 1,
                "san": moves[k] if k < len(moves) else "",
                "sev": sev, "loss": loss, "impact": impact,
                "impact_pct": _impact_pct(impact),
                "before": before_cp, "after": after_cp,
                "fen_before": fens[k],
                "fen_after": fens[k + 1],
                "move_uci": profile_engine.infer_move_uci(fens[k], fens[k + 1]) or "",
                "best_uci": eb[1] or "",
                "best": uci_to_long(fens[k], eb[1]),
            })
    sig.sort(key=lambda m: (-m.get("impact", 0), -m["loss"]))
    conn.execute(
        "INSERT OR REPLACE INTO GameAnalysis (dedup_hash, depth, engine, analyzed_at,"
        " acpl_white, acpl_black, moves_white, moves_black, phase_json, blunders_json)"
        " VALUES (?,?,?,?,?,?,?,?,?,?)",
        (dedup_hash, depth, engine_info()["name"] or "lichess-cloud",
         dt.datetime.now().isoformat(timespec="seconds"),
         _mean(sums["white"]), _mean(sums["black"]),
         sums["white"][1], sums["black"][1],
         json.dumps(phases), json.dumps(sig[:16])))
    conn.commit()
    return _rollup_from_row(conn.execute(
        "SELECT * FROM GameAnalysis WHERE dedup_hash=? AND depth=?",
        (dedup_hash, depth)).fetchone())


def analyze_all(conn, depth: int = ENGINE_DEPTH, scope: str = "all",
                pid: int | None = None, max_games: int | None = None,
                status: dict | None = None, progress=None) -> dict:
    """The heavy pass: run/refresh analysis over stored games (deduped by hash so
    each unique game is analysed once). scope: fast | all | losses (Dino) | player."""
    if scope == "player" and pid is None:
        raise ValueError("scope='player' requires a player id")
    hero = conn.execute("SELECT player_id FROM Roster WHERE is_hero=1").fetchone()
    hero_id = hero["player_id"] if hero else None
    rows = conn.execute(
        "SELECT game_id, dedup_hash, moves_json, presult, player_id, date FROM Games "
        "WHERE source!='lichess' ORDER BY date DESC, game_id DESC").fetchall()
    games, seen = [], set()
    recent_by_player: dict[int, int] = {}

    def add_game(r) -> None:
        if r["dedup_hash"] in seen:
            return
        seen.add(r["dedup_hash"])
        games.append(r)

    if scope == "fast":
        for r in rows:
            if r["player_id"] == hero_id and r["presult"] == "loss":
                add_game(r)
        for r in rows:
            if r["player_id"] == hero_id:
                continue
            n = recent_by_player.get(r["player_id"], 0)
            if n >= 10:
                continue
            add_game(r)
            recent_by_player[r["player_id"]] = n + 1
    else:
        for r in rows:
            if scope == "losses" and not (r["player_id"] == hero_id and r["presult"] == "loss"):
                continue
            if scope == "player" and pid is not None and r["player_id"] != pid:
                continue
            add_game(r)
    if max_games:
        games = games[:max_games]
    if status is not None:
        status.update(total=len(games), current=0, running=True, scope=scope,
                      started=dt.datetime.now().isoformat(timespec="seconds"))
    done = 0
    for r in games:
        analyze_game(conn, r["dedup_hash"], json.loads(r["moves_json"]), depth,
                     allow_engine=True)
        done += 1
        if status is not None:
            status["current"] = done
        if progress:
            progress(done, len(games))
    if status is not None:
        status["running"] = False
    return {"analyzed": done, "total": len(games)}


def hero_blunder_findings(conn, depth: int | None = None,
                          allow_engine: bool = False) -> dict:
    """Engine-pinpointed critical mistakes across Dino's losses + accuracy-by-phase.
    Reads cached analysis only by default (cheap on GET)."""
    if depth is None:
        depth = ENGINE_DEPTH
    out = {"available": engine_info()["available"] or ONLINE_ENABLED,
           "analyzed": 0, "pending": 0, "total": 0, "depth": depth,
           "findings": [], "phase_acpl": {}, "acpl": None}
    hero = conn.execute("SELECT * FROM Roster WHERE is_hero=1").fetchone()
    if not hero:
        return out
    rows = conn.execute(
        "SELECT game_id, dedup_hash, color, opening, eco, white, black, date, event,"
        " moves_json FROM Games WHERE player_id=? AND presult='loss' AND source!='lichess'"
        " ORDER BY date DESC", (hero["player_id"],)).fetchall()
    out["total"] = len(rows)
    phase_sum, tot, depths = _empty_phase(), [0.0, 0], set()
    for r in rows:
        roll = analyze_game(conn, r["dedup_hash"], json.loads(r["moves_json"]),
                            depth, allow_engine=allow_engine)
        if roll is None:
            out["pending"] += 1
            continue
        out["analyzed"] += 1
        depths.add(roll["depth"])
        color = r["color"]
        ph = roll["phases"].get(color, {})
        for key in PHASE_KEYS:
            s, c = ph.get(key, [0, 0])
            phase_sum[key][0] += s
            phase_sum[key][1] += c
            tot[0] += s
            tot[1] += c
        hero_moves = [m for m in roll["moves"] if m["mover"] == color]
        if hero_moves:
            crit = max(hero_moves, key=lambda m: (m.get("impact", 0), m.get("loss", 0)))
            out["findings"].append({
                "game_id": r["game_id"],
                "opponent": r["black"] if color == "white" else r["white"],
                "color": color, "opening": r["opening"], "eco": r["eco"],
                "date": r["date"], "event": r["event"], "ply": crit["ply"],
                "move_no": crit["move_no"], "san": crit["san"], "sev": crit["sev"],
                "loss": crit.get("loss", 0), "impact": crit.get("impact", 0),
                "impact_pct": crit.get("impact_pct", _impact_pct(crit.get("impact", 0))),
                "before": crit["before"], "after": crit["after"], "best": crit["best"]})
    out["findings"].sort(key=lambda f: (-f.get("impact", 0), -f.get("loss", 0)))
    out["phase_acpl"] = {k: _mean(phase_sum[k]) for k in PHASE_KEYS}
    out["acpl"] = _mean(tot)
    if depths:
        out["depth"] = max(depths)
    return out


def opponent_fingerprint(conn, pid: int, depth: int | None = None,
                         allow_engine: bool = False) -> dict:
    """An opponent's engine accuracy profile: overall/by-phase ACPL, blunder
    counts, and which openings/structure families they err in (target) vs play
    solidly (avoid). Cached-only on GET."""
    if depth is None:
        depth = ENGINE_DEPTH
    out = {"available": engine_info()["available"] or ONLINE_ENABLED,
           "analyzed": 0, "pending": 0, "total": 0, "depth": depth, "acpl": None,
           "phase_acpl": {}, "counts": {"blunder": 0, "mistake": 0, "inaccuracy": 0},
           "by_family": [], "by_opening": [], "targets": [], "solid": []}
    rows = conn.execute(
        "SELECT g.game_id, g.dedup_hash, g.color, g.opening, g.eco, g.moves_json,"
        " group_concat(t.family,'|') AS fams FROM Games g"
        " LEFT JOIN Tags t ON t.game_id=g.game_id"
        " WHERE g.player_id=? AND g.source!='lichess' GROUP BY g.game_id",
        (pid,)).fetchall()
    out["total"] = len(rows)
    tot, phase_sum, depths = [0.0, 0], _empty_phase(), set()
    fam_acc: dict[str, list] = {}
    op_acc: dict[str, list] = {}
    for r in rows:
        roll = analyze_game(conn, r["dedup_hash"], json.loads(r["moves_json"]),
                            depth, allow_engine=allow_engine)
        if roll is None:
            out["pending"] += 1
            continue
        out["analyzed"] += 1
        depths.add(roll["depth"])
        color = r["color"]
        ph = roll["phases"].get(color, {})
        gsum = [0.0, 0]
        for key in PHASE_KEYS:
            s, c = ph.get(key, [0, 0])
            phase_sum[key][0] += s
            phase_sum[key][1] += c
            tot[0] += s
            tot[1] += c
            gsum[0] += s
            gsum[1] += c
        own = [m for m in roll["moves"] if m["mover"] == color]
        for m in own:
            out["counts"][m["sev"]] = out["counts"].get(m["sev"], 0) + 1
        serious = sum(1 for m in own if m["sev"] != "inaccuracy")
        for fam in ((r["fams"] or "").split("|") if r["fams"] else []):
            a = fam_acc.setdefault(fam, [0.0, 0, 0])
            a[0] += gsum[0]
            a[1] += gsum[1]
            a[2] += serious
        op = r["opening"] or "(unclassified)"
        a = op_acc.setdefault(op, [0.0, 0, 0, r["eco"]])
        a[0] += gsum[0]
        a[1] += gsum[1]
        a[2] += serious
    out["acpl"] = _mean(tot)
    out["phase_acpl"] = {k: _mean(phase_sum[k]) for k in PHASE_KEYS}
    fam_rows = [{"family": f, "acpl": _mean([v[0], v[1]]), "moves": v[1], "blunders": v[2]}
                for f, v in fam_acc.items() if v[1]]
    fam_rows.sort(key=lambda x: -(x["acpl"] or 0))
    out["by_family"] = fam_rows
    op_rows = [{"opening": o, "eco": v[3], "acpl": _mean([v[0], v[1]]),
                "moves": v[1], "blunders": v[2]}
               for o, v in op_acc.items() if v[1] >= 4]
    op_rows.sort(key=lambda x: -(x["acpl"] or 0))
    out["by_opening"] = op_rows[:8]
    sig_fams = [x for x in fam_rows if x["moves"] >= 6]
    out["targets"] = [x["family"] for x in sig_fams[:2]]
    out["solid"] = [x["family"] for x in sorted(sig_fams, key=lambda x: (x["acpl"] or 0))[:2]]
    if depths:
        out["depth"] = max(depths)
    return out


def build_player_profile(conn, player_id: int, *, depth: int | None = None,
                         allow_engine: bool = False) -> dict:
    """Reusable player profile. Normal GET/export callers keep allow_engine=False
    so this reads cached GameAnalysis rows only and never blocks on Stockfish."""
    if depth is None:
        depth = ENGINE_DEPTH
    return profile_engine.build_player_profile(
        conn,
        player_id,
        depth=depth,
        allow_engine=allow_engine,
        analyze_game=analyze_game,
    )


# ===========================================================================
# ANALYSIS
# ===========================================================================
def confidence_label(n: int) -> str:
    if n >= 12:
        return "high"
    if n >= 4:
        return "medium"
    return "low"


def score_pct(w: int, d: int, l: int) -> float:
    n = w + d + l
    return round(100.0 * (w + 0.5 * d) / n, 1) if n else 0.0


def reliable_score_pct(w: int, d: int, l: int) -> float:
    """Conservative lower-bound score for ranking small samples."""
    n = w + d + l
    if not n:
        return 0.0
    p = (w + 0.5 * d) / n
    z = 1.0
    denom = 1 + z * z / n
    center = p + z * z / (2 * n)
    spread = z * math.sqrt((p * (1 - p) + z * z / (4 * n)) / n)
    return round(100.0 * max(0.0, (center - spread) / denom), 1)


def wdl(games: list[dict]) -> dict:
    w = sum(1 for g in games if g["presult"] == "win")
    d = sum(1 for g in games if g["presult"] == "draw")
    l = sum(1 for g in games if g["presult"] == "loss")
    result_n = w + d + l
    return {
        "n": len(games), "w": w, "d": d, "l": l,
        "score": score_pct(w, d, l),
        "reliable_score": reliable_score_pct(w, d, l),
        "confidence": confidence_label(result_n),
    }


def opening_table(games: list[dict]) -> list[dict]:
    by: dict[str, list[dict]] = {}
    for g in games:
        by.setdefault(g["opening"] or "(unclassified)", []).append(g)
    rows = []
    for op, gs in by.items():
        r = wdl(gs)
        r["opening"] = op
        r["eco"] = gs[0]["eco"]
        rows.append(r)
    rows.sort(key=lambda r: (-r["n"], r["opening"]))
    return rows


def player_games(conn, pid: int) -> list[dict]:
    rows = conn.execute(
        """SELECT g.*, group_concat(t.family, '|') AS fams
           FROM Games g LEFT JOIN Tags t ON t.game_id = g.game_id
           WHERE g.player_id = ? GROUP BY g.game_id
           ORDER BY g.date DESC, g.game_id DESC""", (pid,)).fetchall()
    out = []
    for r in rows:
        d = dict(r)
        d["families"] = (r["fams"] or "").split("|") if r["fams"] else []
        d.pop("fams", None)
        d.pop("moves_json", None)
        d["opponent"] = r["black"] if r["color"] == "white" else r["white"]
        out.append(d)
    return out


def family_table(games: list[dict]) -> list[dict]:
    rows = []
    for fam in ALL_FAMILIES:
        gs = [g for g in games if fam in g["families"]]
        r = wdl(gs)
        r["family"] = fam
        rows.append(r)
    return rows


def repeated_loss_lines(loss_rows: list, min_count: int = 2) -> list[dict]:
    """Find repeated losing prefixes, preferring the most specific useful line."""
    candidates = []
    for plies in (14, 12, 10, 8, 6):
        groups: dict[tuple[str, str], list] = {}
        for r in loss_rows:
            moves = json.loads(r["moves_json"] or "[]")
            if len(moves) < plies:
                continue
            key = (r["color"], " ".join(moves[:plies]))
            groups.setdefault(key, []).append(r)
        for (color, line), rows in groups.items():
            if len(rows) < min_count:
                continue
            openings = Counter((x["opening"] or "(unclassified)") for x in rows)
            candidates.append({
                "color": color, "line": line, "count": len(rows),
                "opening": openings.most_common(1)[0][0],
                "plies": plies,
                "game_ids": sorted(x["game_id"] for x in rows),
            })
    candidates.sort(key=lambda x: (-x["count"], -x["plies"], x["line"]))
    selected = []
    for cand in candidates:
        cand_ids = set(cand["game_ids"])
        if any(cand_ids == set(prev["game_ids"]) and prev["plies"] >= cand["plies"]
               for prev in selected):
            continue
        selected.append(cand)
    return selected


def player_dossier(conn, pid: int) -> dict:
    prof = conn.execute("SELECT * FROM Roster WHERE player_id=?", (pid,)).fetchone()
    games = player_games(conn, pid)
    wg = [g for g in games if g["color"] == "white"]
    bg = [g for g in games if g["color"] == "black"]
    return {
        "profile": dict(prof),
        "totals": wdl(games),
        "sources": {
            "pgn": sum(1 for g in games if g.get("source") != "lichess"),
            "lichess": sum(1 for g in games if g.get("source") == "lichess"),
        },
        "white": {**wdl(wg), "openings": opening_table(wg)},
        "black": {**wdl(bg), "openings": opening_table(bg)},
        "families": family_table(games),
        "games": games,
        # Engine accuracy profile (cached results only — see analyze_all()).
        "fingerprint": opponent_fingerprint(conn, pid, allow_engine=False),
        "player_profile": build_player_profile(conn, pid, allow_engine=False),
    }


def hero_improvement(conn) -> dict:
    hero = conn.execute("SELECT * FROM Roster WHERE is_hero=1").fetchone()
    pid = hero["player_id"]
    games = player_games(conn, pid)
    wg = [g for g in games if g["color"] == "white"]
    bg = [g for g in games if g["color"] == "black"]
    rec_w, rec_b, rec = wdl(wg), wdl(bg), wdl(games)
    op_w, op_b = opening_table(wg), opening_table(bg)
    fams = family_table(games)
    engine = hero_blunder_findings(conn, allow_engine=False)
    player_profile = build_player_profile(conn, pid, allow_engine=False)

    losses = [g for g in games if g["presult"] == "loss"]
    phases = {
        "opening (<=20 moves)": sum(1 for g in losses if (g["total_moves"] or 0) <= 20),
        "middlegame (21-40 moves)": sum(1 for g in losses if 20 < (g["total_moves"] or 0) <= 40),
        "endgame/conversion (>40 moves)": sum(1 for g in losses if (g["total_moves"] or 0) > 40),
    }

    # repeated problem lines: losses sharing the same first 8 plies
    loss_rows = conn.execute(
        """SELECT game_id, moves_json, color, opening FROM Games
           WHERE player_id=? AND presult='loss'""", (pid,)).fetchall()
    repeated = repeated_loss_lines(loss_rows)

    bullets: list[str] = []
    if not games:
        bullets.append("No games found for Dino Ballecer yet — make sure "
                       "CoachDinosaur_Games.pgn is in the folder and rescan.")
    else:
        if abs(rec_w["score"] - rec_b["score"]) >= 10 and rec_w["n"] >= 3 and rec_b["n"] >= 3:
            weaker = "Black" if rec_b["score"] < rec_w["score"] else "White"
            ws, bs = rec_w["score"], rec_b["score"]
            bullets.append(
                f"Colour imbalance: {ws}% with White vs {bs}% with Black "
                f"({abs(ws-bs):.0f}-point gap; conservative scores "
                f"{rec_w['reliable_score']}% vs {rec_b['reliable_score']}%). "
                f"The {weaker} repertoire is the top priority.")
        for color, table in (("White", op_w), ("Black", op_b)):
            weak = [r for r in table if r["n"] >= 2 and r["reliable_score"] < 45]
            weak.sort(key=lambda r: (r["reliable_score"], r["score"], -r["n"]))
            for r in weak[:3]:
                bullets.append(
                    f"As {color} — {r['opening']} ({r['eco']}): scoring only "
                    f"{r['score']}% over {r['n']} games "
                    f"(confidence-adjusted {r['reliable_score']}%, {r['confidence']} confidence) "
                    f"({r['w']}W {r['d']}D {r['l']}L). Needs dedicated repair work.")
        if losses:
            nl = len(losses)
            if phases["opening (<=20 moves)"] / nl >= 0.3:
                bullets.append(
                    f"{phases['opening (<=20 moves)']} of {nl} losses ended within 20 moves — "
                    "opening accidents. Tighten move-order knowledge in the lines flagged above.")
            if phases["endgame/conversion (>40 moves)"] / nl >= 0.35:
                bullets.append(
                    f"{phases['endgame/conversion (>40 moves)']} of {nl} losses went past move 40 — "
                    "long-game technique (conversion, defence, clock handling) needs training.")
        for rl in repeated[:3]:
            bullets.append(
                f"Repeated problem line as {rl['color'].capitalize()} "
                f"({rl['opening']}): lost {rl['count']} games sharing the first "
                f"{rl['plies']} plies "
                f"{rl['line']} — fix this exact sequence before the event.")
        if engine.get("analyzed"):
            usable = {k: v for k, v in (engine.get("phase_acpl") or {}).items() if v is not None}
            if usable:
                worst = max(usable, key=lambda k: usable[k])
                bullets.append(
                    f"Engine phase priority: {PHASE_LABEL[worst]} has the highest ACPL "
                    f"({usable[worst]}). Build training positions from the engine-flagged games.")
            if engine.get("findings"):
                top = engine["findings"][0]
                dots = "." if top["color"] == "white" else "..."
                bullets.append(
                    f"Highest practical mistake cost: {top['move_no']}{dots}{top['san']} "
                    f"vs {top['opponent']} in {top['opening']} lost "
                    f"{top.get('impact_pct', 0)} expected-score points; engine preferred {top['best']}.")
        for f in fams:
            if f["n"] == 0:
                bullets.append(
                    f"No practical games in the \"{f['family']}\" family — a core manual "
                    "structure with zero reps. Schedule focused training games in it.")
            elif f["n"] >= 2 and f["reliable_score"] < 45:
                bullets.append(
                    f"Underperforming in the \"{f['family']}\" family: "
                    f"{f['score']}% over {f['n']} games "
                    f"(confidence-adjusted {f['reliable_score']}%).")
        strong = [r for r in op_w + op_b if r["n"] >= 3 and r["reliable_score"] >= 65]
        strong.sort(key=lambda r: (-r["reliable_score"], -r["score"], -r["n"], r["opening"]))
        if strong:
            names = ", ".join(
                f"{r['opening']} ({r['score']}%, reliable {r['reliable_score']}%)"
                for r in strong[:3])
            bullets.append(f"Confidence weapons to keep sharp (not change): {names}.")

    return {
        "hero": dict(hero),
        "record": rec, "white": {**rec_w, "openings": op_w},
        "black": {**rec_b, "openings": op_b},
        "families": fams, "loss_phases": phases,
        "repeated_lines": repeated, "bullets": bullets,
        "losses": [g for g in games if g["presult"] == "loss"],
        # Engine-pinpointed critical mistakes + accuracy-by-phase (cached only).
        "engine": engine,
        "player_profile": player_profile,
    }


# ===========================================================================
# MARKDOWN EXPORT
# ===========================================================================
def md_wdl(r: dict) -> str:
    extra = f", reliable {r['reliable_score']}%" if r.get("n", 0) >= 2 else ""
    return f"{r['w']}W {r['d']}D {r['l']}L ({r['score']}%{extra})"


def md_opening_table(rows: list[dict], limit: int = 12) -> str:
    if not rows:
        return "_No games on file yet._\n"
    out = ["| Opening | ECO | Games | W-D-L | Score | Reliable | Confidence |",
           "|---|---|---:|---|---:|---:|---|"]
    for r in rows[:limit]:
        out.append(f"| {r['opening']} | {r['eco']} | {r['n']} | "
                   f"{r['w']}-{r['d']}-{r['l']} | {r['score']}% | "
                   f"{r.get('reliable_score', 0)}% | {r.get('confidence', 'low')} |")
    return "\n".join(out) + "\n"


def md_family_table(rows: list[dict]) -> str:
    out = ["| Core Structure Family | Games | W-D-L | Score | Reliable | Confidence |",
           "|---|---:|---|---:|---:|---|"]
    for r in rows:
        out.append(
            f"| {r['family']} | {r['n']} | {r['w']}-{r['d']}-{r['l']} | "
            f"{r['score']}% | {r.get('reliable_score', 0)}% | "
            f"{r.get('confidence', 'low')} |"
            if r["n"] else f"| {r['family']} | 0 | — | — | — | — |")
    return "\n".join(out) + "\n"


def safe_filename(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]+", "_", s).strip("_")


def md_fingerprint(fp: dict | None) -> str:
    """Opponent engine accuracy profile, as Markdown."""
    if not fp or not fp.get("available"):
        return ("_Engine fingerprint unavailable — no Stockfish binary configured "
                "(set PREP_STOCKFISH or drop one in ./stockfish/)._\n")
    if fp.get("analyzed", 0) == 0:
        return (f"_Not analysed yet ({fp.get('pending', 0)} games pending). Run "
                "`python prep_manual_app.py --analyze --scope all`, or click "
                "“Analyze with Stockfish” in the app._\n")
    ph = fp["phase_acpl"]
    c = fp["counts"]
    out = [f"*From {fp['analyzed']} analysed game(s) at depth {fp['depth']}. "
           "Average centipawn loss (ACPL) — lower is more accurate.*", "",
           f"- **Overall ACPL:** {fp['acpl']} "
           f"(opening {ph.get('op')}, middlegame {ph.get('mid')}, endgame {ph.get('end')})",
           f"- **Serious errors on file:** {c.get('blunder', 0)} blunders, "
           f"{c.get('mistake', 0)} mistakes, {c.get('inaccuracy', 0)} inaccuracies"]
    if fp.get("targets"):
        out.append("- **Target structures (least accurate):** "
                   + ", ".join(f"*{t}*" for t in fp["targets"]))
    if fp.get("solid"):
        out.append("- **Avoid — they are solid here (most accurate):** "
                   + ", ".join(f"*{t}*" for t in fp["solid"]))
    if fp.get("by_family"):
        out += ["", "| Structure family | Moves | ACPL | Serious errors |",
                "|---|---:|---:|---:|"]
        for r in fp["by_family"]:
            out.append(f"| {r['family']} | {r['moves']} | {r['acpl']} | {r['blunders']} |")
    return "\n".join(out) + "\n"


def md_engine_findings(eng: dict | None) -> str:
    """Dino's engine-pinpointed critical mistakes + accuracy-by-phase, as Markdown."""
    if not eng or not eng.get("available"):
        return ("_Engine analysis unavailable — no Stockfish binary configured._\n")
    if eng.get("analyzed", 0) == 0:
        return (f"_Losses not analysed yet ({eng.get('pending', 0)} pending). Run "
                "`python prep_manual_app.py --analyze --scope losses`._\n")
    ph = eng["phase_acpl"]
    out = [f"*From {eng['analyzed']} analysed loss(es) at depth {eng['depth']}. "
           f"Accuracy by phase (average centipawn loss): opening {ph.get('op')}, "
           f"middlegame {ph.get('mid')}, endgame {ph.get('end')} "
           f"(overall {eng['acpl']}).*", ""]
    if eng["findings"]:
        out += ["| Game | Opening | Critical move | Eval swing | Practical loss | Engine prefers |",
                "|---|---|---|---|---:|---|"]
        for f in eng["findings"]:
            dots = "." if f["color"] == "white" else "..."
            mv = f"{f['move_no']}{dots}{f['san']} ({f['sev']})"
            swing = f"{cp_to_pawns(f['before'])} → {cp_to_pawns(f['after'])}"
            out.append(f"| vs {f['opponent']} | {f['opening']} ({f['eco']}) | "
                       f"{mv} | {swing} | {f.get('impact_pct', 0)} pts | {f['best']} |")
    return "\n".join(out) + "\n"


def md_player_profile(pp: dict | None) -> str:
    if not pp:
        return "_Player profile unavailable._\n"
    phase = pp.get("phase_profile") or {}
    opening = pp.get("opening_profile") or {}
    out = []
    analyzed = phase.get("analyzed", 0)
    if analyzed:
        ph = phase.get("phase_acpl") or {}
        counts = phase.get("mistake_counts") or {}
        out += [
            f"*From {analyzed} analysed game(s) at depth {phase.get('depth')}. "
            f"Overall ACPL {phase.get('acpl')} — opening {ph.get('op')}, "
            f"middlegame {ph.get('mid')}, endgame {ph.get('end')}.*",
            "",
            f"- **Mistakes on file:** {counts.get('blunder', 0)} blunders, "
            f"{counts.get('mistake', 0)} mistakes, {counts.get('inaccuracy', 0)} inaccuracies",
        ]
    else:
        out += [
            f"_No cached engine profile yet ({phase.get('pending', 0)} games pending). "
            "Run the fast Stockfish pass from the app or CLI._",
            "",
        ]
    out.append(f"- **Opening breadth:** {opening.get('distinct_openings', 0)} distinct openings")
    if opening.get("strongest_lines"):
        lines = ", ".join(
            f"{r['opening']} ({r['score']}%, reliable {r.get('reliable_score', 0)}% "
            f"over {r['n']} games)"
            for r in opening["strongest_lines"][:3])
        out.append(f"- **Confidence lines:** {lines}")
    if opening.get("weak_lines"):
        lines = ", ".join(
            f"{r['opening']} ({r['score']}%, reliable {r.get('reliable_score', 0)}% "
            f"over {r['n']} games)"
            for r in opening["weak_lines"][:3])
        out.append(f"- **Repair lines:** {lines}")
    if pp.get("tendencies"):
        out += ["", "### Data-backed tendencies", ""]
        for t in pp["tendencies"]:
            out.append(f"- **{t['label']}** ({t['confidence']} confidence): {t['evidence']}")
    if pp.get("weakness_categories"):
        out += ["", "### Endgame / simplified-position weakness categories", "",
                "| Category | Samples | Evidence |",
                "|---|---:|---|"]
        for c in pp["weakness_categories"]:
            reason = "; ".join(c.get("reasons") or [])
            out.append(f"| {c['title']} | {c['count']} | {reason or 'Classified from engine samples.'} |")
    if pp.get("samples"):
        out += ["", "### Sample positions", "",
                "| Game | Move | Severity | Practical loss | Category | Engine prefers |",
                "|---|---|---|---:|---|---|"]
        for s in pp["samples"][:6]:
            cats = ", ".join(profile_engine.WEAKNESS_TITLES.get(c, c)
                             for c in s.get("categories", []))
            dots = "." if s.get("color") == "white" else "..."
            move = f"{s.get('move_no')}{dots}{s.get('san')}"
            out.append(f"| vs {s.get('opponent', '')} | {move} | {s.get('severity')} | "
                       f"{s.get('impact_pct', 0)} pts | {cats} | {s.get('best', '')} |")
    return "\n".join(out) + "\n"


def export_markdown(conn) -> list[str]:
    EXPORT_DIR.mkdir(exist_ok=True)
    today = dt.date.today().isoformat()
    written = []

    # --- opponent dossiers ---
    opp_rows = conn.execute(
        "SELECT player_id, real_name FROM Roster WHERE is_hero=0 ORDER BY fide DESC").fetchall()
    for r in opp_rows:
        d = player_dossier(conn, r["player_id"])
        p = d["profile"]
        src = d["sources"]
        lines = [f"# Opponent Dossier — {p['real_name']}", "",
                 f"*Generated {today} from {d['totals']['n']} games "
                 f"({src['pgn']} over-the-board PGN, {src['lichess']} Lichess online).*", "",
                 f"**Title:** {p['title'] or '—'} | **Federation:** {p['federation']} | "
                 f"**FIDE:** {p['fide'] or '—'}", "",
                 f"**Overall record on file:** {md_wdl(d['totals'])}", "",
                 f"## Repertoire as White ({d['white']['n']} games, {d['white']['score']}%)", "",
                 md_opening_table(d["white"]["openings"]), "",
                 f"## Repertoire as Black ({d['black']['n']} games, {d['black']['score']}%)", "",
                 md_opening_table(d["black"]["openings"]), "",
                 "## Core Structure Families", "",
                 md_family_table(d["families"]), "",
                 "## Engine fingerprint", "",
                 md_fingerprint(d.get("fingerprint")), "",
                 "## Player Profile", "",
                 md_player_profile(d.get("player_profile")), "",
                 "## Prep pointers", ""]
        pointers = []
        for f in d["families"]:
            if f["n"] >= 2 and f["score"] < 50:
                pointers.append(f"- **Target:** steer into *{f['family']}* — they score only "
                                f"{f['score']}% there ({f['n']} games).")
            elif f["n"] >= 3 and f["score"] >= 70:
                pointers.append(f"- **Avoid:** *{f['family']}* — they score {f['score']}% "
                                f"({f['n']} games).")
        for color_key, label in (("white", "White"), ("black", "Black")):
            weak = [x for x in d[color_key]["openings"] if x["n"] >= 2 and x["score"] < 50]
            for x in weak[:2]:
                pointers.append(f"- **Target as {('Black' if label=='White' else 'White')}:** "
                                f"their {x['opening']} as {label} scores {x['score']}% "
                                f"({x['n']} games).")
        if not pointers:
            pointers.append("- Not enough games on file yet for reliable pointers — "
                            "add their PGN database and re-export.")
        lines += pointers + ["", "## Recent losses (model games to study)", ""]
        losses = [g for g in d["games"] if g["presult"] == "loss"][:6]
        if losses:
            for g in losses:
                link = f" — [replay](https://lichess.org/{g['lichess_id']})" \
                    if g.get("lichess_id") else ""
                rnd = f" (R{g['round']})" if g["round"] else ""
                lines.append(f"- {g['date']} {g['event']}{rnd}: as {g['color']} vs "
                             f"{g['opponent']} — {g['opening']} ({g['eco']}), "
                             f"{g['result']} in {g['total_moves']} moves{link}")
        else:
            lines.append("_No losses on file._")
        lines.append("")
        out = EXPORT_DIR / f"Opponent_{safe_filename(p['real_name'])}.md"
        out.write_text("\n".join(lines), encoding="utf-8")
        written.append(out.name)

    # --- Dino: Needs Improvement ---
    imp = hero_improvement(conn)
    lines = [f"# Needs Improvement — {HERO_NAME} (Coach Dinosaur)", "",
             f"*Generated {today} from {imp['record']['n']} of his own games.*", "",
             f"**Overall:** {md_wdl(imp['record'])} — "
             f"White {md_wdl(imp['white'])}, Black {md_wdl(imp['black'])}", "",
             "## Priority work list", ""]
    lines += [f"{i}. {b}" for i, b in enumerate(imp["bullets"], 1)] or ["_No findings._"]
    lines += ["", "## Player Profile", "",
              md_player_profile(imp.get("player_profile")), "",
              f"## Openings as White ({imp['white']['n']} games)", "",
              md_opening_table(imp["white"]["openings"], 20), "",
              f"## Openings as Black ({imp['black']['n']} games)", "",
              md_opening_table(imp["black"]["openings"], 20), "",
              "## Core Structure Families (own games)", "",
              md_family_table(imp["families"]), "",
              "## Loss profile", ""]
    for k, v in imp["loss_phases"].items():
        lines.append(f"- Losses in {k}: **{v}**")
    lines += ["", "## Engine-detected critical mistakes", "",
              md_engine_findings(imp.get("engine"))]
    if imp["repeated_lines"]:
        lines += ["", "## Repeated problem lines (2+ losses, same first moves)", ""]
        for rl in imp["repeated_lines"]:
            lines.append(f"- As {rl['color']}: `{rl['line']}` — {rl['count']} losses "
                         f"({rl['opening']})")
    lines.append("")
    out = EXPORT_DIR / "Dino_Ballecer_Needs_Improvement.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    written.append(out.name)

    # --- index ---
    idx = ["# Tournament Prep Manual — generated sections", "",
           f"*Generated {today} by prep_manual_app.py*", ""]
    idx += [f"- {w}" for w in written]
    (EXPORT_DIR / "00_INDEX.md").write_text("\n".join(idx) + "\n", encoding="utf-8")
    written.append("00_INDEX.md")
    return written


# ===========================================================================
# HTTP SERVER
# ===========================================================================
class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def _json(self, obj, status=200):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _html(self, text: str):
        body = text.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _bytes(self, body: bytes, content_type: str, status=200):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _body_json(self) -> dict:
        n = int(self.headers.get("Content-Length") or 0)
        if not n:
            return {}
        try:
            return json.loads(self.rfile.read(n).decode("utf-8"))
        except Exception:
            return {}

    # ------------------------------------------------------------------ GET
    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        try:
            if u.path == "/":
                self._html(HTML_PAGE)
            elif u.path.startswith("/static/"):
                static_root = (BASE_DIR / "static").resolve()
                rel = urllib.parse.unquote(u.path[len("/static/"):])
                path = (static_root / rel).resolve()
                # Path-traversal guard: resolved path must stay under static/.
                if static_root not in path.parents or not path.is_file():
                    self._json({"error": "not found"}, 404)
                    return
                mime = {
                    ".js": "text/javascript; charset=utf-8",
                    ".svg": "image/svg+xml",
                    ".png": "image/png",
                    ".css": "text/css; charset=utf-8",
                    ".json": "application/json; charset=utf-8",
                }.get(path.suffix.lower(), "application/octet-stream")
                self._bytes(path.read_bytes(), mime)
            elif u.path == "/api/state":
                self._json(self.state())
            elif u.path == "/api/play/players":
                conn = db()
                try:
                    self._json(play_players_payload(conn))
                finally:
                    conn.close()
            elif u.path == "/api/player":
                conn = db()
                try:
                    self._json(player_dossier(conn, int(q["id"][0])))
                finally:
                    conn.close()
            elif u.path == "/api/improvement":
                conn = db()
                try:
                    self._json(hero_improvement(conn))
                finally:
                    conn.close()
            elif u.path == "/api/game":
                conn = db()
                try:
                    r = conn.execute("SELECT * FROM Games WHERE game_id=?",
                                     (int(q["id"][0]),)).fetchone()
                finally:
                    conn.close()
                if not r:
                    self._json({"error": "not found"}, 404)
                    return
                moves = json.loads(r["moves_json"])
                fens, err = fens_for(moves)
                self._json({
                    "white": r["white"], "black": r["black"], "result": r["result"],
                    "event": r["event"], "date": r["date"], "round": r["round"],
                    "opening": r["opening"], "eco": r["eco"],
                    "orientation": r["color"], "moves": moves, "fens": fens,
                    "replay_error": err})
            elif u.path == "/api/explorer":
                # Opt-in Lichess opening-explorer population stats for a position
                # (theory context for the analysis). Cached; only fetches when --online.
                if not ONLINE_ENABLED:
                    self._json({"error": "online disabled — start with --online"}, 400)
                    return
                conn = db()
                try:
                    data = explorer_lookup(conn, epd_key(q["fen"][0]),
                                           (q.get("scope", ["masters"])[0]))
                finally:
                    conn.close()
                self._json(data or {"error": "no data"})
            else:
                self._json({"error": "unknown route"}, 404)
        except Exception as exc:
            self._json({"error": str(exc)}, 500)

    # ----------------------------------------------------------------- POST
    def do_POST(self):
        u = urlparse(self.path)
        body = self._body_json()
        conn = db()
        try:
            if u.path == "/api/scan":
                self._json({"ok": True, "summary": scan(conn)})
            elif u.path == "/api/map":
                name = (body.get("name") or "").strip().lower()
                pid = int(body.get("player_id") or 0)
                if not name or not pid:
                    self._json({"error": "name and player_id required"}, 400)
                    return
                conn.execute("INSERT OR REPLACE INTO Aliases (alias, player_id, source) "
                             "VALUES (?,?,'manual')", (name, pid))
                conn.execute("DELETE FROM IgnoredNames WHERE alias=?", (name,))
                conn.commit()
                scan(conn)
                self._json({"ok": True})
            elif u.path == "/api/unmap":
                alias = (body.get("alias") or "").strip().lower()
                conn.execute("DELETE FROM Aliases WHERE alias=?", (alias,))
                conn.commit()
                scan(conn)
                self._json({"ok": True})
            elif u.path == "/api/ignore":
                name = (body.get("name") or "").strip()
                conn.execute("INSERT OR IGNORE INTO IgnoredNames (alias) VALUES (?)",
                             (name.lower(),))
                conn.execute("DELETE FROM UnmatchedNames WHERE name=?", (name,))
                conn.commit()
                self._json({"ok": True})
            elif u.path == "/api/paste":
                text = body.get("text") or ""
                stem = safe_filename(body.get("filename") or "pasted_games") or "pasted_games"
                if "[Event" not in text:
                    self._json({"error": "That does not look like PGN ([Event ...] not found)."}, 400)
                    return
                target = BASE_DIR / f"{stem}.pgn"
                i = 2
                while target.exists():
                    target = BASE_DIR / f"{stem}_{i}.pgn"
                    i += 1
                target.write_text(text, encoding="utf-8")
                scan(conn)
                self._json({"ok": True, "saved_as": target.name})
            elif u.path == "/api/export":
                files = export_markdown(conn)
                self._json({"ok": True, "dir": str(EXPORT_DIR), "files": files})
            elif u.path == "/api/play/move":
                if get_play_engine() is None:
                    self._json({"error": "No engine available — drop a Stockfish binary "
                                "in ./stockfish/ (or set PREP_STOCKFISH)."}, 400)
                    return
                try:
                    pid = int(body.get("player_id") or 0)
                    fen = _normalize_fen_full(body.get("fen") or "")
                    bot_color = (body.get("bot_color") or "").strip().lower()
                    if bot_color not in ("white", "black"):
                        raise ValueError("bot_color must be white or black")
                    if _fen_color_to_move(fen) != bot_color:
                        raise ValueError("bot_color must match the FEN side to move")
                    row = conn.execute(
                        """SELECT r.fide, COUNT(g.game_id) AS pgn_games
                           FROM Roster r LEFT JOIN Games g
                                ON g.player_id=r.player_id AND g.source='pgn'
                           WHERE r.player_id=?
                           GROUP BY r.player_id""", (pid,)).fetchone()
                    if not row or not row["pgn_games"]:
                        raise ValueError("eligible PGN-backed player_id required")
                    default_elo = row["fide"] if row["fide"] is not None else PLAY_DEFAULT_ELO
                    elo = clamp_play_elo(body.get("elo") if body.get("elo") is not None else default_elo)
                    self._json(select_bot_move(conn, pid, fen, elo=elo,
                                               engine=get_play_engine()))
                except ValueError as exc:
                    self._json({"error": str(exc)}, 400)
                    return
            elif u.path == "/api/analyze":
                # Kick off the heavy engine pass in the background; the UI polls
                # /api/state for progress. Results land in GameAnalysis and then
                # flow into dossiers, the self-audit, and the export.
                if ANALYZE_STATUS.get("running"):
                    self._json({"ok": False, "error": "analysis already running",
                                "status": dict(ANALYZE_STATUS)})
                    return
                if get_engine() is None and not ONLINE_ENABLED:
                    self._json({"error": "No engine available — drop a Stockfish binary "
                                "in ./stockfish/ (or set PREP_STOCKFISH), or use --online."},
                               400)
                    return
                scope = body.get("scope") or "fast"
                pid = body.get("player_id")
                if scope == "player" and not pid:
                    self._json({"error": "player_id required for player analysis"}, 400)
                    return
                depth = int(body.get("depth") or ENGINE_DEPTH)
                maxg = body.get("max_games")

                def _worker(scope=scope, pid=pid, depth=depth, maxg=maxg):
                    c = db()
                    try:
                        analyze_all(c, depth=depth, scope=scope,
                                    pid=int(pid) if pid else None,
                                    max_games=int(maxg) if maxg else None,
                                    status=ANALYZE_STATUS)
                    finally:
                        c.close()

                threading.Thread(target=_worker, daemon=True).start()
                self._json({"ok": True, "started": True, "status": dict(ANALYZE_STATUS)})
            else:
                self._json({"error": "unknown route"}, 404)
        except Exception as exc:
            self._json({"error": str(exc)}, 500)
        finally:
            conn.close()

    # ---------------------------------------------------------------- state
    def state(self) -> dict:
        conn = db()
        try:
            roster = []
            for r in conn.execute("SELECT * FROM Roster ORDER BY is_hero DESC, fide DESC"):
                g = conn.execute(
                    """SELECT
                         COUNT(*) n,
                         SUM(presult='win') w, SUM(presult='draw') d, SUM(presult='loss') l
                       FROM Games WHERE player_id=?""", (r["player_id"],)).fetchone()
                roster.append({**dict(r), "games": g["n"] or 0, "w": g["w"] or 0,
                               "d": g["d"] or 0, "l": g["l"] or 0,
                               "score": score_pct(g["w"] or 0, g["d"] or 0, g["l"] or 0)})
            files = []
            for f in conn.execute("SELECT * FROM Files ORDER BY filename"):
                stored = conn.execute("SELECT COUNT(DISTINCT dedup_hash) FROM Games WHERE file_id=?",
                                      (f["file_id"],)).fetchone()[0]
                files.append({**dict(f), "stored": stored})
            unmatched = [dict(r) for r in conn.execute(
                "SELECT * FROM UnmatchedNames ORDER BY games DESC, name")]
            aliases = [dict(r) for r in conn.execute(
                """SELECT a.alias, a.source, r.real_name FROM Aliases a
                   JOIN Roster r ON r.player_id = a.player_id ORDER BY r.real_name, a.alias""")]
            analyzed = conn.execute("SELECT COUNT(*) FROM GameAnalysis").fetchone()[0]
            return {"roster": roster, "files": files, "unmatched": unmatched,
                    "aliases": aliases, "folder": str(BASE_DIR),
                    "engine": engine_info(), "opening_db": opening_db_available(),
                    "online": ONLINE_ENABLED, "analyze": dict(ANALYZE_STATUS),
                    "analyzed_games": analyzed}
        finally:
            conn.close()


# ===========================================================================
# FRONT-END (single page, vanilla JS, offline)
# ===========================================================================
HTML_PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Tournament Prep Manual — Dino Ballecer 2026</title>
<style>
:root { --bg:#11151c; --panel:#1a2029; --panel2:#222a36; --text:#dde4ee; --dim:#8a97a8;
        --acc:#4da3ff; --good:#4ec77a; --bad:#e2645a; --warn:#e2b75a; --line:#2c3645;
        --shadow:0 2px 6px rgba(0,0,0,.3); --shadow-md:0 6px 20px rgba(0,0,0,.4); }
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--text);
       font:14px/1.45 "Segoe UI", system-ui, sans-serif; }
header { padding:10px 22px; background:var(--panel); border-bottom:1px solid var(--line);
         display:flex; flex-direction:column; gap:6px; }
header h1 { font-size:17px; margin:0; white-space:nowrap; }
.headerTop { display:flex; align-items:center; gap:16px; }
.headerActions { display:flex; gap:8px; margin-left:auto; flex-wrap:wrap; }
@media (max-width:760px){ .headerTop { flex-wrap:wrap; } .headerActions { margin-left:0; } }
.headerStatus { display:flex; gap:16px; flex-wrap:wrap; }
.headerStatus .sub { min-width:0; }
header .sub { color:var(--dim); font-size:12px; }
#folder { overflow:hidden; text-overflow:ellipsis; white-space:nowrap; max-width:min(60vw, 600px); }
button { background:var(--panel2); color:var(--text); border:1px solid var(--line);
         border-radius:6px; padding:6px 12px; cursor:pointer; font-size:13px;
         transition:background .15s ease, border-color .15s ease, transform .05s ease, opacity .15s ease; }
button:hover { border-color:var(--acc); }
button:active { transform:translateY(1px); }
button:disabled { opacity:.45; cursor:not-allowed; }
button:disabled:hover { border-color:var(--line); }
button.primary { background:var(--acc); color:#08121f; border-color:var(--acc); font-weight:600; }
button.primary:hover { background:#6db4ff; }
button.danger { background:#3a201d; color:var(--bad); border-color:#5a2e29; }
button.danger:hover { background:#4a2622; border-color:var(--bad); }
nav { display:flex; gap:4px; padding:10px 22px 0; background:var(--panel);
      border-bottom:1px solid var(--line); flex-wrap:wrap; position:sticky; top:0; z-index:5; }
nav button { border-radius:8px 8px 0 0; border-bottom:none; padding:8px 16px; }
nav button.on { background:var(--bg); color:var(--acc); font-weight:600; box-shadow:inset 0 2px 0 0 var(--acc); }
main { padding:18px 22px 60px; max-width:1280px; margin:0 auto; }
.card { background:var(--panel); border:1px solid var(--line); border-radius:10px;
        padding:14px 16px; margin-bottom:16px; box-shadow:var(--shadow); }
.card h2 { margin:0 0 12px; font-size:15px; color:var(--acc); padding-bottom:8px;
           border-bottom:1px solid var(--line); display:flex; align-items:center; gap:8px; }
.card h3 { margin:14px 0 6px; font-size:13.5px; }
table { border-collapse:collapse; width:100%; font-size:13px; }
th { text-align:left; color:var(--dim); font-weight:600; padding:6px 8px;
     border-bottom:1px solid var(--line); white-space:nowrap; }
td { padding:6px 8px; border-bottom:1px solid var(--line); }
table tr:nth-child(even) td { background:rgba(255,255,255,.025); }
table tr:hover td { background:rgba(255,255,255,.05); }
tr.click { cursor:pointer; }
tr.click:hover td { background:var(--panel2); }
.score-hi, .score-lo, .score-md { display:inline-block; padding:1px 8px; border-radius:10px; font-weight:600; }
.score-hi { background:#1d3a26; color:var(--good); }
.score-lo { background:#3a201d; color:var(--bad); }
.score-md { background:#37321d; color:var(--warn); }
.tag { display:inline-block; background:var(--panel2); border:1px solid var(--line);
       border-radius:10px; font-size:11px; padding:1px 8px; margin:1px 2px; color:var(--dim); }
.muted { color:var(--dim); }
.bullet { padding:8px 12px; border-left:3px solid var(--warn); background:var(--panel2);
          border-radius:0 6px 6px 0; margin-bottom:8px; }
.cols { display:grid; grid-template-columns:1fr 1fr; gap:16px; }
@media (max-width:900px){ .cols { grid-template-columns:1fr; } }
.opp-layout { display:grid; grid-template-columns:280px 1fr; gap:16px; }
@media (max-width:900px){ .opp-layout { grid-template-columns:1fr; } }
.plist div { padding:8px 10px; border-radius:6px; cursor:pointer; margin-bottom:3px; }
.plist div:hover { background:var(--panel2); }
.plist div.on { background:var(--panel2); border-left:3px solid var(--acc); }
.plist .meta { font-size:11px; color:var(--dim); }
select, input[type=text], textarea { background:var(--panel2); color:var(--text);
   border:1px solid var(--line); border-radius:6px; padding:6px 8px; font-size:13px; }
textarea { width:100%; font-family:Consolas, monospace; }
#modal { position:fixed; inset:0; background:rgba(0,0,0,.65); display:none;
         align-items:center; justify-content:center; z-index:50; }
#modal.open { display:flex; }
.viewer { background:var(--panel); border:1px solid var(--line); border-radius:12px;
          padding:18px; display:grid; grid-template-columns:auto 1fr; gap:18px; max-width:92vw; max-height:92vh;
          position:relative; box-shadow:var(--shadow-md); }
.modal-x { position:absolute; top:10px; right:10px; width:28px; height:28px; padding:0;
           border-radius:50%; font-size:18px; line-height:1; display:flex; align-items:center;
           justify-content:center; }
.board { display:grid; grid-template-columns:repeat(8, 58px); grid-template-rows:repeat(8, 58px);
         border:2px solid var(--line); border-radius:6px; overflow:hidden; box-shadow:var(--shadow-md); }
.sqL { background:#eeeed2; } .sqD { background:#769656; }
.board span { position:relative; display:flex; align-items:center; justify-content:center;
              background-size:88%; background-position:center; background-repeat:no-repeat;
              line-height:1; user-select:none; }
.coord { position:absolute; font-size:9px; font-weight:600; line-height:1; pointer-events:none;
         font-style:normal; opacity:.9; }
.coord.rank { top:2px; left:2px; } .coord.file { bottom:1px; right:3px; }
.coord.light { color:#eeeed2; } .coord.dark { color:#769656; }
.vside { display:flex; flex-direction:column; min-height:0; flex:1; }
.vmoves { display:flex; flex-wrap:wrap; gap:4px; overflow:auto; background:var(--panel2); border-radius:8px;
          padding:8px; font-size:13px; align-content:flex-start; }
.vmoves span.mv { cursor:pointer; padding:2px 6px; border-radius:4px; white-space:nowrap; }
.vmoves span.mv.cur { background:var(--acc); color:#08121f; font-weight:600; }
.vbtns { display:flex; gap:6px; }
.play-layout { display:grid; grid-template-columns:minmax(360px, 440px) auto minmax(220px, 1fr); gap:16px; align-items:start; }
@media (max-width:1024px){ .play-layout { grid-template-columns:1fr; } }
.play-board { display:grid; grid-template-columns:repeat(8, minmax(36px, 52px));
              grid-template-rows:repeat(8, minmax(36px, 52px)); border:2px solid var(--line);
              border-radius:6px; overflow:hidden; box-shadow:var(--shadow-md);
              width:min(100%, 420px); aspect-ratio:1; }
.play-board span { position:relative; display:flex; align-items:center; justify-content:center;
                   background-size:88%; background-position:center; background-repeat:no-repeat;
                   line-height:1; user-select:none; cursor:pointer; }
.play-board span.sel { outline:3px solid var(--acc); outline-offset:-3px; }
.play-board span.legal::after { content:""; width:28%; height:28%; border-radius:50%;
                                background:rgba(77,163,255,.55); }
.play-board span.last { box-shadow:inset 0 0 0 999px rgba(226,183,90,.22); }
.play-controls { display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin-bottom:10px; }
.play-controls label { display:flex; align-items:center; gap:5px; }
.clock-row { display:grid; grid-template-columns:1fr 1fr; gap:8px; margin:10px 0; }
.clock { background:var(--panel2); border:1px solid var(--line); border-radius:8px;
         padding:8px 10px; font-size:18px; font-weight:600; }
.clock .small { display:block; font-weight:400; }
.play-moves { max-height:220px; overflow:auto; background:var(--panel2); border-radius:8px;
              padding:8px; font-size:13px; }
.pill { font-size:11px; border-radius:10px; padding:2px 8px; }
.pill.w { background:#1d3a26; color:var(--good);} .pill.l { background:#3a201d; color:var(--bad);}
.pill.d { background:#37321d; color:var(--warn);} .pill.u { background:var(--panel2); color:var(--dim);}
#toast { position:fixed; bottom:18px; right:18px; background:var(--panel2);
         border:1px solid var(--line); border-left:3px solid var(--acc); color:var(--text); padding:10px 16px;
         border-radius:8px; z-index:60; max-width:420px; box-shadow:var(--shadow-md);
         opacity:0; transform:translateY(8px); pointer-events:none;
         transition:opacity .2s ease, transform .2s ease; }
#toast.show { opacity:1; transform:translateY(0); }
#toast.error { border-left-color:var(--bad); }
#toast.success { border-left-color:var(--good); }
.small { font-size:12px; }
.spinner { display:inline-block; width:14px; height:14px; border:2px solid var(--line);
           border-top-color:var(--acc); border-radius:50%; animation:spin .7s linear infinite;
           vertical-align:-2px; margin-right:6px; }
@keyframes spin { to { transform:rotate(360deg); } }
</style>
</head>
<body>
<header>
  <div class="headerTop">
    <h1>Tournament Prep Manual — Dino Ballecer 2026</h1>
    <div class="headerActions">
      <button id="analyzeBtn" onclick="runAnalyze()">⚙ Analyze selected player</button>
      <button class="primary" onclick="rescan()">⟳ Rescan PGN folder</button>
    </div>
  </div>
  <div class="headerStatus">
    <span class="sub" id="folder"></span>
    <span class="sub" id="engineStatus" title="Engine analysis powers the dossiers, the self-audit and the export — it is not an interactive board."></span>
  </div>
</header>
<nav>
  <button id="tb-overview" class="on" onclick="tab('overview')">Overview</button>
  <button id="tb-opponents" onclick="tab('opponents')">Opponents</button>
  <button id="tb-play" onclick="tab('play')">Play Bot</button>
  <button id="tb-dino" onclick="tab('dino')">Dino — Needs Improvement</button>
  <button id="tb-files" onclick="tab('files')">Files &amp; Names</button>
  <button id="tb-export" onclick="tab('export')">Export Manual Sections</button>
</nav>
<main>
  <div id="pg-overview"></div>
  <div id="pg-opponents" style="display:none"></div>
  <div id="pg-play" style="display:none"></div>
  <div id="pg-dino" style="display:none"></div>
  <div id="pg-files" style="display:none"></div>
  <div id="pg-export" style="display:none"></div>
</main>

<div id="modal" onclick="if(event.target===this) closeModal()">
  <div class="viewer">
    <button class="modal-x" onclick="closeModal()" aria-label="Close" title="Close">&times;</button>
    <div>
      <div class="board" id="board"></div>
      <div class="vbtns" style="margin-top:10px">
        <button onclick="goPly(0)">|&#9664;</button>
        <button onclick="goPly(curPly-1)">&#9664;</button>
        <button onclick="goPly(curPly+1)">&#9654;</button>
        <button onclick="goPly(viewer.fens.length-1)">&#9654;|</button>
        <button onclick="flip()">&#8645; Flip</button>
        <span style="flex:1"></span>
        <button onclick="closeModal()">Close</button>
      </div>
    </div>
    <div class="vside">
      <div id="vtitle" style="font-weight:600"></div>
      <div id="vsub" class="muted small"></div>
      <div class="vmoves" id="vmoves"></div>
      <div class="muted small" id="verr"></div>
    </div>
  </div>
</div>
<div id="toast"></div>

<script type="module">
import { Chess } from '/static/chess.js';
window.Chess = Chess;
window.dispatchEvent(new Event('chessjs-ready'));
</script>
<script>
let STATE=null, curTab='overview', curPlayer=null, viewer=null, curPly=0, orient='white';
// cburnett SVG pieces, bundled offline under /static/pieces/ (e.g. wN.svg, bQ.svg).
function pieceUrl(c){ return '/static/pieces/'+(c===c.toUpperCase()?'w':'b')+c.toUpperCase()+'.svg'; }
function pieceStyle(c){ return c?' style="background-image:url('+pieceUrl(c)+')"':''; }
// Subtle lichess-style coordinates: files (a-h) on the bottom displayed rank,
// ranks (1-8) on the left displayed file. Colored to contrast the square.
function coordLabels(ri,ci,rIdx,cIdx){
  const dark=(ri+ci)%2===1, tone=dark?'light':'dark'; let h='';
  if(ci===cIdx[0]) h+='<i class="coord rank '+tone+'">'+(8-ri)+'</i>';
  if(ri===rIdx[rIdx.length-1]) h+='<i class="coord file '+tone+'">'+FILES_STR_JS[ci]+'</i>';
  return h;
}

function toast(msg, type){ const t=document.getElementById('toast'); t.textContent=msg;
  t.className = 'show' + (type ? ' '+type : '');
  clearTimeout(t._h); t._h=setTimeout(()=>t.classList.remove('show'),4000); }
async function api(path,opts){ const r=await fetch(path,opts);
  const j=await r.json(); if(j.error) throw new Error(j.error); return j; }
async function post(path,body){ return api(path,{method:'POST',
  headers:{'Content-Type':'application/json'}, body:JSON.stringify(body||{})}); }
function esc(s){ return (s??'').toString().replace(/[&<>"]/g,
  c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c])); }
function scoreCls(s,n){ if(!n) return 'muted'; return s>=60?'score-hi':(s<45?'score-lo':'score-md'); }
function pill(p){ const m={win:'w',loss:'l',draw:'d'}; const c=m[p]||'u';
  return '<span class="pill '+c+'">'+esc(p)+'</span>'; }

function tab(name){ curTab=name;
  for(const t of ['overview','opponents','play','dino','files','export']){
    document.getElementById('pg-'+t).style.display = t===name?'':'none';
    document.getElementById('tb-'+t).classList.toggle('on', t===name); }
  if(name==='play') loadPlay();
  if(name==='dino') loadDino();
  if(name==='opponents') renderOpponents();
}

async function refresh(){ STATE=await api('/api/state');
  const folderEl=document.getElementById('folder');
  folderEl.textContent='watching: '+STATE.folder+'\\*.pgn';
  folderEl.title=folderEl.textContent;
  updateEngineStatus();
  renderOverview(); renderFiles(); renderExportTab();
  if(curTab==='opponents') renderOpponents(); }

/* ---------------- Engine analysis (powers the generated analysis only) ---- */
function fmtCp(cp){ if(cp>=9000) return '#'+(10000-cp); if(cp<=-9000) return '#-'+(10000+cp);
  return (cp>=0?'+':'')+(cp/100).toFixed(1); }
function updateEngineStatus(){
  if(!STATE) return; const e=STATE.engine||{}, a=STATE.analyze||{};
  const bits=[ e.available?('engine: '+esc(e.name||'Stockfish')):'engine: none',
    'openings DB: '+(STATE.opening_db?'on':'off') ];
  if(STATE.online) bits.push('online: on');
  bits.push('analysed: '+(STATE.analyzed_games||0));
  if(a.running) bits.push('analysing '+(a.current||0)+'/'+(a.total||0)+'…');
  const se=document.getElementById('engineStatus'); if(se) se.textContent=bits.join('  ·  ');
  const btn=document.getElementById('analyzeBtn');
  if(btn){ btn.disabled = !!a.running || !(e.available||STATE.online);
    btn.textContent = a.running ? ('⚙ Analysing '+(a.current||0)+'/'+(a.total||0))
                                : '⚙ Analyze selected player'; }
}
async function runAnalyze(){
  const pid=selectedAnalyzePlayerId();
  if(!pid){ toast('Open Dino or an opponent first, then analyze that player.'); return; }
  await analyzePlayer(pid);
}
function selectedAnalyzePlayerId(){
  if(!STATE) return null;
  if(curTab==='dino'){
    const hero=STATE.roster.find(r=>r.is_hero); return hero ? hero.player_id : null;
  }
  if(curTab==='opponents' && curPlayer) return curPlayer;
  return null;
}
function playerName(pid){
  const p=(STATE&&STATE.roster||[]).find(r=>r.player_id===pid);
  return p ? p.real_name : ('player '+pid);
}
async function analyzePlayer(pid){
  try{ const r=await post('/api/analyze',{scope:'player', player_id:pid});
    if(r.error){ toast(r.error, 'error'); return; }
    toast('Engine analysis started for '+playerName(pid)+' — all PGN games for this player.');
    pollAnalyze();
  }catch(e){ toast('Analyze failed: '+e.message, 'error'); }
}
function pollAnalyze(){ clearTimeout(window._ap);
  window._ap=setTimeout(async()=>{
    try{ STATE=await api('/api/state'); updateEngineStatus();
      if(STATE.analyze && STATE.analyze.running){ pollAnalyze(); }
      else { toast('Engine analysis complete.');
        if(curTab==='dino') loadDino(); if(curPlayer) selectPlayer(curPlayer); }
    }catch(e){ /* keep polling quietly */ pollAnalyze(); }
  }, 1500);
}

async function rescan(){ try{ const r=await post('/api/scan');
  toast('Scanned '+r.summary.files+' files — '+r.summary.games_stored+' games stored.');
  await refresh(); if(curTab==='dino') loadDino(); if(curPlayer) selectPlayer(curPlayer);
  if(curTab==='play'){ PLAY.loaded=false; loadPlay(); }
 }catch(e){ toast('Scan failed: '+e.message, 'error'); } }

/* ---------------- Overview ---------------- */
function renderOverview(){
  const opp=STATE.roster.filter(r=>!r.is_hero), hero=STATE.roster.find(r=>r.is_hero);
  let h='<div class="card"><h2>Round-robin pool — games loaded per player</h2>';
  h+='<table><tr><th>Player</th><th>Title</th><th>Fed</th><th>FIDE</th><th>Games in DB</th><th>W-D-L</th><th>Score</th></tr>';
  const row=r=>'<tr class="click" onclick="tab(\'opponents\');selectPlayer('+r.player_id+')">'+
    '<td>'+(r.is_hero?'&#11088; ':'')+esc(r.real_name)+'</td><td>'+esc(r.title||'—')+'</td>'+
    '<td>'+esc(r.federation)+'</td><td>'+(r.fide||'—')+'</td><td>'+r.games+'</td>'+
    '<td>'+r.w+'-'+r.d+'-'+r.l+'</td><td class="'+scoreCls(r.score,r.games)+'">'+
    (r.games?r.score+'%':'—')+'</td></tr>';
  h+=row(hero); for(const r of opp) h+=row(r);
  h+='</table></div>';
  const missing=opp.filter(r=>!r.games);
  if(missing.length){
    h+='<div class="card"><h2>Waiting for opponent PGN databases</h2>'+
       '<p class="muted">Drop the multi-game PGN file(s) into the folder above (any filename '+
       'ending in .pgn) and click <b>Rescan</b>. Player names inside the PGN are matched to the '+
       'roster automatically; anything unrecognised appears under <b>Files &amp; Names</b> for '+
       'manual mapping.</p><p>'+missing.map(r=>'<span class="tag">'+esc(r.real_name)+'</span>').join('')+
       '</p></div>'; }
  document.getElementById('pg-overview').innerHTML=h;
}

/* ---------------- Opponents ---------------- */
function renderOpponents(){
  const opp=STATE.roster.filter(r=>!r.is_hero);
  let list='<div class="card plist"><h2>Opponents</h2>';
  for(const r of opp){ list+='<div id="pl-'+r.player_id+'" class="'+(curPlayer===r.player_id?'on':'')+
    '" onclick="selectPlayer('+r.player_id+')"><b>'+esc(r.real_name)+'</b>'+
    '<div class="meta">'+esc(r.title||'')+' '+esc(r.federation)+' '+(r.fide||'')+
    ' &middot; '+r.games+' games</div></div>'; }
  list+='</div>';
  document.getElementById('pg-opponents').innerHTML=
    '<div class="opp-layout">'+list+'<div id="dossier"><div class="card muted">'+
    'Select an opponent to open their dossier.</div></div></div>';
  if(curPlayer) selectPlayer(curPlayer);
}

async function selectPlayer(pid){
  curPlayer=pid;
  document.querySelectorAll('.plist div').forEach(d=>d.classList.toggle('on', d.id==='pl-'+pid));
  const el=document.getElementById('dossier'); if(!el) return;
  el.innerHTML='<div class="card muted"><span class="spinner"></span> Loading…</div>';
  try{
    const d=await api('/api/player?id='+pid);
    el.innerHTML=dossierHtml(d);
  }catch(e){ el.innerHTML='<div class="card">Error: '+esc(e.message)+'</div>'; }
}

function openingTbl(rows){
  if(!rows.length) return '<p class="muted">No games.</p>';
  let h='<table><tr><th>Opening</th><th>ECO</th><th>N</th><th>W-D-L</th><th>Score</th><th>Reliable</th><th>Conf.</th></tr>';
  for(const r of rows) h+='<tr><td>'+esc(r.opening)+'</td><td>'+esc(r.eco)+'</td><td>'+r.n+
    '</td><td>'+r.w+'-'+r.d+'-'+r.l+'</td><td class="'+scoreCls(r.score,r.n)+'">'+r.score+
    '%</td><td class="'+scoreCls(r.reliable_score||0,r.n)+'">'+(r.reliable_score||0)+
    '%</td><td>'+esc(r.confidence||'low')+'</td></tr>';
  return h+'</table>';
}
function famTbl(rows){
  let h='<table><tr><th>Core Structure Family</th><th>N</th><th>W-D-L</th><th>Score</th><th>Reliable</th><th>Conf.</th></tr>';
  for(const r of rows) h+='<tr><td>'+esc(r.family)+'</td><td>'+r.n+'</td><td>'+
    (r.n?(r.w+'-'+r.d+'-'+r.l):'—')+'</td><td class="'+scoreCls(r.score,r.n)+'">'+
    (r.n?r.score+'%':'—')+'</td><td class="'+scoreCls(r.reliable_score||0,r.n)+'">'+
    (r.n?(r.reliable_score||0)+'%':'—')+'</td><td>'+(r.n?esc(r.confidence||'low'):'—')+'</td></tr>';
  return h+'</table>';
}
function gamesTbl(games){
  if(!games.length) return '<p class="muted">No games on file. Add a PGN database and rescan.</p>';
  let h='<table><tr><th>Date</th><th>Event</th><th>Clr</th><th>Opponent</th><th>Opening</th>'+
        '<th>Res</th><th>Mv</th><th>Families</th></tr>';
  for(const g of games){
    const act = g.lichess_id
      ? 'window.open(\'https://lichess.org/'+esc(g.lichess_id)+'\',\'_blank\')'
      : 'openGame('+g.game_id+')';
    const extra = g.lichess_id ? ' <span class="muted small" title="opens on lichess.org">&#8599;</span>' : '';
    h+='<tr class="click" onclick="'+act+'"><td>'+esc(g.date)+
    '</td><td>'+esc(g.event)+extra+'</td><td>'+(g.color==='white'?'W':'B')+'</td><td>'+esc(g.opponent)+
    '</td><td>'+esc(g.opening)+'</td><td>'+pill(g.presult)+'</td><td>'+g.total_moves+'</td><td>'+
    g.families.map(f=>'<span class="tag">'+esc(f)+'</span>').join('')+'</td></tr>'; }
  return h+'</table>';
}
function dossierHtml(d){
  const p=d.profile;
  return '<div class="card"><h2>'+esc(p.real_name)+'</h2><p class="muted">'+esc(p.title||'')+
    ' &middot; '+esc(p.federation)+' &middot; FIDE '+(p.fide||'—')+' &middot; '+d.totals.n+
    ' games on file ('+d.totals.w+'-'+d.totals.d+'-'+d.totals.l+', '+d.totals.score+'%)'+
    ' &middot; sources: '+d.sources.pgn+' OTB PGN / '+d.sources.lichess+' Lichess online</p>'+
    '<p><button class="primary" onclick="analyzePlayer('+p.player_id+')">Analyze all games for this player</button></p>'+
    '<div class="cols"><div><h3>As White — '+d.white.n+' games ('+d.white.score+'%)</h3>'+
    openingTbl(d.white.openings)+'</div><div><h3>As Black — '+d.black.n+' games ('+
    d.black.score+'%)</h3>'+openingTbl(d.black.openings)+'</div></div>'+
    '<h3>Core Structure Families</h3>'+famTbl(d.families)+'</div>'+
    fingerprintHtml(d.fingerprint)+
    playerProfileHtml(d.player_profile)+
    '<div class="card"><h2>Games ('+d.games.length+') — click to replay</h2>'+
    gamesTbl(d.games)+'</div>';
}
function fingerprintHtml(fp){
  if(!fp) return '';
  if(!fp.available) return '<div class="card"><h3>Engine fingerprint</h3><p class="muted">'+
    'No Stockfish engine configured — set PREP_STOCKFISH or drop a binary in ./stockfish/.</p></div>';
  if(!fp.analyzed) return '<div class="card"><h3>Engine fingerprint</h3><p class="muted">'+
    'Not analysed yet ('+fp.pending+' games pending). Click <b>Analyze with Stockfish</b> above.</p></div>';
  const ph=fp.phase_acpl||{}, c=fp.counts||{};
  let h='<div class="card"><h3>Engine fingerprint <span class="muted small">('+fp.analyzed+
    ' games, depth '+fp.depth+')</span></h3>'+
    '<p>Overall <b>ACPL '+fp.acpl+'</b> <span class="muted">(lower = more accurate)</span> · '+
    'opening '+ph.op+' / middlegame '+ph.mid+' / endgame '+ph.end+'<br>'+
    'Serious errors on file: <b>'+(c.blunder||0)+'</b> blunders, '+(c.mistake||0)+
    ' mistakes, '+(c.inaccuracy||0)+' inaccuracies</p>';
  if(fp.targets&&fp.targets.length) h+='<p>&#127919; <b>Target (least accurate):</b> '+
    fp.targets.map(esc).join(', ')+'</p>';
  if(fp.solid&&fp.solid.length) h+='<p>&#128737; <b>Avoid — solid here:</b> '+
    fp.solid.map(esc).join(', ')+'</p>';
  if(fp.by_family&&fp.by_family.length){
    h+='<table><tr><th>Structure family</th><th>Moves</th><th>ACPL</th><th>Serious errors</th></tr>';
    for(const r of fp.by_family) h+='<tr><td>'+esc(r.family)+'</td><td>'+r.moves+'</td><td>'+
      r.acpl+'</td><td>'+r.blunders+'</td></tr>';
    h+='</table>'; }
  return h+'</div>';
}
function playerProfileHtml(pp){
  if(!pp) return '';
  const phase=pp.phase_profile||{}, op=pp.opening_profile||{};
  let h='<div class="card"><h2>Player Profile</h2>';
  if(phase.analyzed){
    const ph=phase.phase_acpl||{}, c=phase.mistake_counts||{};
    h+='<p><b>'+phase.analyzed+'</b> analysed game(s), depth '+phase.depth+
       ' · ACPL '+phase.acpl+' <span class="muted">(opening '+ph.op+
       ' / middlegame '+ph.mid+' / endgame '+ph.end+')</span><br>'+
       'Errors: '+(c.blunder||0)+' blunders, '+(c.mistake||0)+
       ' mistakes, '+(c.inaccuracy||0)+' inaccuracies.</p>';
  } else {
    h+='<p class="muted">No cached engine profile yet ('+(phase.pending||0)+
       ' games pending). Run the fast Stockfish pass to unlock phase and weakness data.</p>';
  }
  h+='<p><b>Opening breadth:</b> '+(op.distinct_openings||0)+' distinct openings.</p>';
  if(op.strongest_lines&&op.strongest_lines.length){
    h+='<p><b>Confidence lines:</b> '+op.strongest_lines.slice(0,3).map(r=>
      esc(r.opening)+' ('+r.score+'%, reliable '+(r.reliable_score||0)+'% / '+r.n+'g)').join(', ')+'</p>';
  }
  if(op.weak_lines&&op.weak_lines.length){
    h+='<p><b>Repair lines:</b> '+op.weak_lines.slice(0,3).map(r=>
      esc(r.opening)+' ('+r.score+'%, reliable '+(r.reliable_score||0)+'% / '+r.n+'g)').join(', ')+'</p>';
  }
  if(pp.tendencies&&pp.tendencies.length){
    h+='<h3>Data-backed tendencies</h3><table><tr><th>Label</th><th>Evidence</th><th>Confidence</th></tr>';
    for(const t of pp.tendencies) h+='<tr><td>'+esc(t.label)+'</td><td>'+
      esc(t.evidence)+'</td><td>'+esc(t.confidence)+'</td></tr>';
    h+='</table>';
  }
  if(pp.weakness_categories&&pp.weakness_categories.length){
    h+='<h3>Endgame / simplified-position weakness categories</h3>'+
       '<table><tr><th>Category</th><th>Samples</th><th>Evidence</th></tr>';
    for(const c of pp.weakness_categories) h+='<tr><td>'+esc(c.title)+
      '</td><td>'+c.count+'</td><td>'+esc((c.reasons||[]).join('; '))+'</td></tr>';
    h+='</table>';
  }
  if(pp.samples&&pp.samples.length){
    h+='<h3>Sample positions</h3><table><tr><th>Game</th><th>Move</th><th>Severity</th>'+
       '<th>Practical loss</th><th>Category</th><th>Engine prefers</th></tr>';
    for(const s of pp.samples.slice(0,6)){
      const cats=(s.categories||[]).map(c=>esc(c.replaceAll('_',' '))).join(', ');
      const dots=s.color==='white'?'.':'…';
      const move=(s.move_no||'?')+dots+esc(s.san||'');
      h+='<tr class="click" onclick="openGame('+s.game_id+','+s.ply+')"><td>vs '+esc(s.opponent)+
        '</td><td>'+move+'</td><td>'+esc(s.severity)+'</td><td>'+
        Number(s.impact_pct||0).toFixed(1)+' pts</td><td>'+cats+
        '</td><td>'+esc(s.best||'')+'</td></tr>';
    }
    h+='</table>';
  }
  return h+'</div>';
}
function engineFindingsHtml(eng){
  if(!eng) return '';
  if(!eng.available) return '<div class="card"><h2>Engine-detected critical mistakes</h2>'+
    '<p class="muted">No Stockfish engine configured.</p></div>';
  if(!eng.analyzed) return '<div class="card"><h2>Engine-detected critical mistakes</h2>'+
    '<p class="muted">Losses not analysed yet ('+eng.pending+' pending). Click '+
    '<b>Analyze with Stockfish</b> above.</p></div>';
  const ph=eng.phase_acpl||{};
  let h='<div class="card"><h2>Engine-detected critical mistakes <span class="muted small">('+
    eng.analyzed+' losses, depth '+eng.depth+')</span></h2>'+
    '<p class="muted">Accuracy by phase (avg centipawn loss): opening '+ph.op+' · middlegame '+
    ph.mid+' · endgame '+ph.end+' · overall '+eng.acpl+'</p>';
  if(eng.findings.length){
    h+='<table><tr><th>Game</th><th>Opening</th><th>Critical move</th><th>Eval swing</th>'+
       '<th>Practical loss</th><th>Engine prefers</th></tr>';
    for(const f of eng.findings){
      const mv=f.move_no+(f.color==='white'?'.':'…')+esc(f.san)+
        ' <span class="pill l">'+esc(f.sev)+'</span>';
      h+='<tr class="click" onclick="openGame('+f.game_id+','+f.ply+')"><td>vs '+esc(f.opponent)+
        '</td><td>'+esc(f.opening)+' ('+esc(f.eco)+')</td><td>'+mv+'</td><td>'+fmtCp(f.before)+
        ' &rarr; '+fmtCp(f.after)+'</td><td>'+Number(f.impact_pct||0).toFixed(1)+
        ' pts</td><td>'+esc(f.best)+'</td></tr>'; }
    h+='</table>'; }
  return h+'</div>';
}

/* ---------------- Dino tab ---------------- */
async function loadDino(){
  const el=document.getElementById('pg-dino');
  el.innerHTML='<div class="card muted"><span class="spinner"></span> Analysing…</div>';
  try{
    const d=await api('/api/improvement');
    let h='<div class="card"><h2>&#11088; '+esc(d.hero.real_name)+' — own-game audit ('+
      d.record.n+' games)</h2><p>Overall <b>'+d.record.w+'-'+d.record.d+'-'+d.record.l+
      '</b> ('+d.record.score+'%) &middot; White '+d.white.score+'% ('+d.white.n+
      ') &middot; Black '+d.black.score+'% ('+d.black.n+')</p>'+
      '<p><button class="primary" onclick="analyzePlayer('+d.hero.player_id+')">Analyze all Dino games</button></p></div>';
    h+='<div class="card"><h2>Needs improvement — priority list</h2>';
    h+= d.bullets.length? d.bullets.map(b=>'<div class="bullet">'+esc(b)+'</div>').join('')
                        : '<p class="muted">No findings.</p>';
    h+='</div>';
    h+='<div class="cols"><div class="card"><h2>Openings as White</h2>'+
       openingTbl(d.white.openings)+'</div><div class="card"><h2>Openings as Black</h2>'+
       openingTbl(d.black.openings)+'</div></div>';
    h+='<div class="cols"><div class="card"><h2>Core Structure Families</h2>'+famTbl(d.families)+
       '</div><div class="card"><h2>Loss profile</h2><table><tr><th>Phase (by game length)</th>'+
       '<th>Losses</th></tr>';
    for(const k in d.loss_phases) h+='<tr><td>'+esc(k)+'</td><td>'+d.loss_phases[k]+'</td></tr>';
    h+='</table>';
    if(d.repeated_lines.length){
      h+='<h3>Repeated problem lines</h3>';
      for(const r of d.repeated_lines) h+='<div class="bullet">As '+r.color+': <code>'+
        esc(r.line)+'</code> — '+r.count+' losses ('+esc(r.opening)+')</div>'; }
    h+='</div></div>';
    h+=playerProfileHtml(d.player_profile);
    h+=engineFindingsHtml(d.engine);
    h+='<div class="card"><h2>All losses — click to replay</h2>'+gamesTbl(d.losses)+'</div>';
    el.innerHTML=h;
  }catch(e){ el.innerHTML='<div class="card">Error: '+esc(e.message)+'</div>'; }
}

/* ---------------- Files & names ---------------- */
function renderFiles(){
  let h='<div class="card"><h2>PGN files found in folder</h2>';
  if(STATE.files.length){
    h+='<table><tr><th>File</th><th>Games parsed</th><th>Games stored (roster matches)</th><th>Last scan</th></tr>';
    for(const f of STATE.files) h+='<tr><td>'+esc(f.filename)+'</td><td>'+f.games_parsed+
      '</td><td>'+f.stored+'</td><td class="muted">'+esc(f.scanned_at)+'</td></tr>';
    h+='</table>';
  } else h+='<p class="muted">No .pgn files found yet.</p>';
  h+='<p class="muted small">A game is stored once per roster player appearing in it. Names that '+
     'are not Dino or one of the 9 opponents (e.g. Dino’s past opponents in his own file) can '+
     'safely stay unmatched.</p></div>';

  h+='<div class="card"><h2>Unmatched player names ('+STATE.unmatched.length+')</h2>';
  if(STATE.unmatched.length){
    const opts=STATE.roster.map(r=>'<option value="'+r.player_id+'">'+esc(r.real_name)+'</option>').join('');
    h+='<p><input type="text" id="unmatchedFilter" placeholder="Filter by name…" oninput="filterUnmatched()" '+
       'style="width:240px"> <span class="muted small" id="unmatchedCount"></span></p>';
    h+='<table><tr><th>Name in PGN</th><th>Games</th><th>Map to roster player</th><th></th></tr><tbody id="unmatchedBody">';
    STATE.unmatched.forEach((u,i)=>{
      h+='<tr data-name="'+esc(u.name.toLowerCase())+'"><td>'+esc(u.name)+'</td><td>'+u.games+'</td>'+
         '<td><select id="map-'+i+'"><option value="">— choose —</option>'+opts+'</select> '+
         '<button onclick="mapName('+i+')">Map</button></td>'+
         '<td><button onclick="ignoreName('+i+')">Ignore</button></td></tr>'; });
    h+='</tbody></table>';
  } else h+='<p class="muted">Every name in the PGN files is either mapped or ignored.</p>';
  h+='</div>';

  h+='<div class="card"><h2>Active name mappings</h2><table><tr><th>PGN name (alias)</th>'+
     '<th>Roster player</th><th>How</th><th></th></tr>';
  for(const a of STATE.aliases) h+='<tr><td>'+esc(a.alias)+'</td><td>'+esc(a.real_name)+
    '</td><td class="muted">'+esc(a.source)+'</td><td><button onclick="unmap(\''+
    esc(a.alias).replace(/'/g,"\\'")+'\')">Remove</button></td></tr>';
  h+='</table></div>';

  h+='<div class="card"><h2>Paste a PGN database directly</h2>'+
     '<p class="muted small">Alternative to dropping a file in the folder: paste multi-game PGN '+
     'text here and it is saved as a .pgn file, then scanned.</p>'+
     '<p>Save as: <input type="text" id="pasteName" value="opponents_database" size="30">.pgn</p>'+
     '<textarea id="pasteText" rows="8" placeholder="[Event &quot;...&quot;] ..."></textarea>'+
     '<p><button class="primary" onclick="pastePgn()">Save &amp; scan</button></p></div>';
  document.getElementById('pg-files').innerHTML=h;
  if(STATE.unmatched.length) filterUnmatched();
}
function filterUnmatched(){
  const q=(document.getElementById('unmatchedFilter').value||'').toLowerCase();
  const rows=document.querySelectorAll('#unmatchedBody tr'); let shown=0;
  rows.forEach(r=>{ const match=r.dataset.name.includes(q); r.style.display=match?'':'none'; if(match) shown++; });
  document.getElementById('unmatchedCount').textContent='Showing '+shown+' of '+rows.length;
}
async function mapName(i){
  const u=STATE.unmatched[i]; const pid=document.getElementById('map-'+i).value;
  if(!pid){ toast('Choose a roster player first.', 'error'); return; }
  try{ await post('/api/map',{name:u.name, player_id:+pid});
       toast('Mapped "'+u.name+'" — rescanned.'); await refresh(); }
  catch(e){ toast('Failed: '+e.message, 'error'); }
}
async function ignoreName(i){
  try{ await post('/api/ignore',{name:STATE.unmatched[i].name}); await refresh(); }
  catch(e){ toast('Failed: '+e.message, 'error'); }
}
async function unmap(alias){
  try{ await post('/api/unmap',{alias}); toast('Removed mapping — rescanned.'); await refresh(); }
  catch(e){ toast('Failed: '+e.message, 'error'); }
}
async function pastePgn(){
  const text=document.getElementById('pasteText').value;
  const name=document.getElementById('pasteName').value;
  try{ const r=await post('/api/paste',{text, filename:name});
       toast('Saved as '+r.saved_as+' and scanned.');
       document.getElementById('pasteText').value=''; await refresh(); }
  catch(e){ toast('Failed: '+e.message, 'error'); }
}

/* ---------------- Export ---------------- */
function renderExportTab(){
  document.getElementById('pg-export').innerHTML=
   '<div class="card"><h2>Export Markdown sections for the manual</h2>'+
   '<p class="muted">Writes one dossier per opponent plus '+
   '<b>Dino_Ballecer_Needs_Improvement.md</b> into the <code>manual_sections</code> folder. '+
   'Open them in any editor and paste into Tournament_Preparation_Manual.docx. '+
   'Re-export any time after adding PGNs. Analyze each player first to include '+
   'the engine fingerprint, player profile, and critical-mistake sections.</p>'+
   '<p><button class="primary" onclick="doExport()">Generate manual sections</button></p>'+
   '<div id="exportResult"></div></div>';
}
async function doExport(){
  const el=document.getElementById('exportResult'); el.innerHTML='<p class="muted">Writing…</p>';
  try{ const r=await post('/api/export');
    el.innerHTML='<p>Written to <code>'+esc(r.dir)+'</code>:</p><ul>'+
      r.files.map(f=>'<li>'+esc(f)+'</li>').join('')+'</ul>';
  }catch(e){ el.innerHTML='<p>Failed: '+esc(e.message)+'</p>'; }
}

/* ---------------- Play Bot ---------------- */
let PLAY={loaded:false, info:null, players:[], game:null, human:'white', bot:'black',
  orient:'white', selectedSq:null, legalTargets:[], pending:false, result:null, reason:'',
  clocks:{white:3600, black:3600}, inc:30, timer:null, lastTick:0, lastMove:null, lastMeta:null};

window.addEventListener('chessjs-ready',()=>{ if(curTab==='play') loadPlay(); });

async function loadPlay(){
  const el=document.getElementById('pg-play');
  if(!window.Chess){ el.innerHTML='<div class="card muted"><span class="spinner"></span> Loading chess rules…</div>'; return; }
  if(!PLAY.loaded){
    el.innerHTML='<div class="card muted"><span class="spinner"></span> Loading players…</div>';
    try{ const data=await api('/api/play/players');
      PLAY.info=data; PLAY.players=data.players||[]; PLAY.loaded=true;
    }catch(e){ el.innerHTML='<div class="card">Error: '+esc(e.message)+'</div>'; return; }
  }
  renderPlayShell();
}

function playSelectedPlayer(){
  const pid=+(document.getElementById('playPlayer')?.value||0);
  return PLAY.players.find(p=>p.player_id===pid) || PLAY.players[0] || null;
}
function playOpponentChanged(){
  const p=playSelectedPlayer(); if(!p) return;
  const elo=document.getElementById('playElo'), out=document.getElementById('playEloVal');
  elo.value=p.default_elo; out.textContent=p.default_elo;
}
function renderPlayShell(){
  const el=document.getElementById('pg-play');
  if(!PLAY.players.length){
    el.innerHTML='<div class="card">No PGN-backed players are available. Add PGNs and rescan.</div>';
    return;
  }
  const info=PLAY.info||{}, p0=PLAY.players[0], engine=info.engine||{};
  const playerOpts=PLAY.players.map(p=>'<option value="'+p.player_id+'">'+
    esc((p.is_hero?'Dino — ':'')+p.real_name)+' ('+p.pgn_games+' PGNs)</option>').join('');
  const clockOpts=(info.clock_presets||['60+30']).map(c=>'<option value="'+esc(c)+'">'+esc(c)+'</option>').join('');
  const curElo=p0.default_elo || 2400;
  el.innerHTML='<div class="play-layout"><div class="card"><h2>Play Bot</h2>'+
    '<div class="play-controls">'+
    '<label>Opponent <select id="playPlayer" onchange="playOpponentChanged()">'+playerOpts+'</select></label>'+
    '<label>Play as <select id="playColor"><option value="white">White</option><option value="black">Black</option></select></label>'+
    '<label>Clock <select id="playClock">'+clockOpts+'</select></label>'+
    '<label>Strength <input id="playElo" type="range" min="'+info.elo_min+'" max="'+info.elo_max+
      '" value="'+curElo+'" oninput="document.getElementById(\'playEloVal\').textContent=this.value">'+
      ' <span id="playEloVal">'+curElo+'</span></label></div>'+
    '<div class="play-controls">'+
    '<button class="primary" onclick="playStart()" '+(engine.available?'':'disabled')+'>Start</button>'+
    '<button class="danger" onclick="playResign()">Resign</button><button onclick="playOfferDraw()">Offer Draw</button>'+
    '<button onclick="playFlip()">&#8645; Flip</button><button onclick="playCopyPgn()">Copy PGN</button>'+
    '<button onclick="playDownloadPgn()">Download PGN</button></div>'+
    (engine.available?'':'<p class="muted">No Stockfish engine found. Set PREP_STOCKFISH or add ./stockfish/.</p>')+
    '<div class="clock-row"><div class="clock" id="playWhiteClock"></div><div class="clock" id="playBlackClock"></div></div>'+
    '<div id="playStatus" class="muted"></div><div id="playMeta" class="muted small" style="margin-top:8px"></div></div>'+
    '<div class="card"><div class="play-board" id="playBoard"></div></div>'+
    '<div class="card"><h2>Moves</h2><div class="play-moves" id="playMoves"></div></div></div>';
  renderPlayState();
}

function playParseClock(tc){
  const m=(tc||'60+30').match(/^(\d+)\+(\d+)$/);
  return m ? {base:+m[1]*60, inc:+m[2]} : {base:3600, inc:30};
}
function playFmtClock(sec){
  sec=Math.max(0, Math.ceil(sec)); const m=Math.floor(sec/60), s=sec%60;
  return m+':'+String(s).padStart(2,'0');
}
function playTurnColor(){ return PLAY.game && PLAY.game.turn()==='w' ? 'white' : 'black'; }
function playStartClock(){
  clearInterval(PLAY.timer); PLAY.lastTick=Date.now();
  PLAY.timer=setInterval(playTick,250);
}
function playTick(){
  if(!PLAY.game || PLAY.result) return;
  const now=Date.now(), dt=(now-PLAY.lastTick)/1000; PLAY.lastTick=now;
  const side=playTurnColor(); PLAY.clocks[side]=Math.max(0, PLAY.clocks[side]-dt);
  if(side===PLAY.human && PLAY.clocks[side]<=0) playEnd(PLAY.human==='white'?'0-1':'1-0','Human flagged');
  renderPlayClocks();
}
function playAddInc(color){ PLAY.clocks[color]+=PLAY.inc; }

function playStart(){
  if(!window.Chess){ toast('Chess rules are still loading.'); return; }
  const p=playSelectedPlayer(); if(!p){ toast('Choose an opponent first.'); return; }
  const tc=playParseClock(document.getElementById('playClock').value);
  PLAY.game=new window.Chess(); PLAY.game.setHeader('White', document.getElementById('playColor').value==='white'?'Dino':p.real_name);
  PLAY.game.setHeader('Black', document.getElementById('playColor').value==='black'?'Dino':p.real_name);
  PLAY.game.setHeader('Event','Tournament prep bot game'); PLAY.game.setHeader('TimeControl', document.getElementById('playClock').value);
  PLAY.human=document.getElementById('playColor').value; PLAY.bot=PLAY.human==='white'?'black':'white'; PLAY.orient=PLAY.human;
  PLAY.clocks={white:tc.base, black:tc.base}; PLAY.inc=tc.inc; PLAY.result=null; PLAY.reason='';
  PLAY.pending=false; PLAY.selectedSq=null; PLAY.legalTargets=[]; PLAY.lastMove=null; PLAY.lastMeta=null;
  playStartClock(); renderPlayState();
  if(PLAY.bot==='white') playRequestBotMove();
}
function playEnd(result, reason){
  PLAY.result=result; PLAY.reason=reason||''; clearInterval(PLAY.timer);
  if(PLAY.game) PLAY.game.setHeader('Result', result);
  renderPlayState();
}
function playResign(){ if(PLAY.game && !PLAY.result) playEnd(PLAY.human==='white'?'0-1':'1-0','Resignation'); }
function playOfferDraw(){ if(PLAY.game && !PLAY.result) playEnd('1/2-1/2','Draw agreed'); }
function playFlip(){ PLAY.orient=PLAY.orient==='white'?'black':'white'; renderPlayBoard(); }
async function playCopyPgn(){
  if(!PLAY.game){ toast('Start a game first.'); return; }
  await navigator.clipboard.writeText(PLAY.game.pgn()); toast('PGN copied.');
}
function playDownloadPgn(){
  if(!PLAY.game){ toast('Start a game first.'); return; }
  const blob=new Blob([PLAY.game.pgn()],{type:'application/x-chess-pgn'});
  const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='prep-bot-game.pgn';
  a.click(); URL.revokeObjectURL(a.href);
}

function playCanMove(){ return PLAY.game && !PLAY.result && !PLAY.pending && playTurnColor()===PLAY.human; }
function playSquare(sq){
  if(!playCanMove()) return;
  if(PLAY.selectedSq && PLAY.legalTargets.includes(sq)){ playHumanMove(PLAY.selectedSq,sq); return; }
  const piece=PLAY.game.get(sq), want=PLAY.human==='white'?'w':'b';
  if(piece && piece.color===want){
    PLAY.selectedSq=sq; PLAY.legalTargets=PLAY.game.moves({square:sq, verbose:true}).map(m=>m.to);
  } else { PLAY.selectedSq=null; PLAY.legalTargets=[]; }
  renderPlayBoard();
}
function playHumanMove(from,to){
  const legal=PLAY.game.moves({square:from, verbose:true}).filter(m=>m.to===to);
  if(!legal.length){ PLAY.selectedSq=null; PLAY.legalTargets=[]; renderPlayBoard(); return; }
  let promotion='q';
  if(legal.some(m=>(m.flags||'').includes('p'))){
    promotion=(prompt('Promote to q, r, b, or n','q')||'q').toLowerCase();
    if(!['q','r','b','n'].includes(promotion)) promotion='q';
  }
  const mv=PLAY.game.move({from,to,promotion});
  if(!mv){ toast('Illegal move.'); return; }
  PLAY.lastMove={from:mv.from,to:mv.to}; PLAY.selectedSq=null; PLAY.legalTargets=[]; PLAY.lastMeta=null;
  playAddInc(PLAY.human); playCheckGameOver(); renderPlayState();
  if(!PLAY.result) playRequestBotMove();
}
async function playRequestBotMove(){
  if(!PLAY.game || PLAY.result) return;
  PLAY.pending=true; renderPlayState();
  try{
    const meta=await post('/api/play/move',{
      player_id:+document.getElementById('playPlayer').value,
      fen:PLAY.game.fen(), bot_color:PLAY.bot, elo:+document.getElementById('playElo').value
    });
    const u=meta.uci, move={from:u.slice(0,2), to:u.slice(2,4)};
    if(u.length>4) move.promotion=u[4];
    const mv=PLAY.game.move(move);
    if(!mv) throw new Error('Bot returned illegal move '+u);
    PLAY.lastMove={from:mv.from,to:mv.to}; PLAY.lastMeta=meta; playAddInc(PLAY.bot);
    PLAY.pending=false; playCheckGameOver(); renderPlayState();
  }catch(e){ PLAY.pending=false; toast('Bot move failed: '+e.message, 'error'); renderPlayState(); }
}
function playCheckGameOver(){
  if(!PLAY.game || PLAY.result) return;
  if(PLAY.game.isCheckmate()) playEnd(PLAY.game.turn()==='w'?'0-1':'1-0','Checkmate');
  else if(PLAY.game.isStalemate && PLAY.game.isStalemate()) playEnd('1/2-1/2','Stalemate');
  else if(PLAY.game.isDraw && PLAY.game.isDraw()) playEnd('1/2-1/2','Draw');
}

function renderPlayState(){ renderPlayClocks(); renderPlayBoard(); renderPlayMoves(); renderPlayStatus(); }
function renderPlayClocks(){
  const w=document.getElementById('playWhiteClock'), b=document.getElementById('playBlackClock');
  if(!w||!b) return;
  w.innerHTML=playFmtClock(PLAY.clocks.white)+'<span class="small">White'+(PLAY.human==='white'?' (you)':' (bot)')+'</span>';
  b.innerHTML=playFmtClock(PLAY.clocks.black)+'<span class="small">Black'+(PLAY.human==='black'?' (you)':' (bot)')+'</span>';
}
function renderPlayStatus(){
  const s=document.getElementById('playStatus'), m=document.getElementById('playMeta'); if(!s||!m) return;
  if(!PLAY.game){ s.textContent='Choose an opponent and start a game.'; m.textContent=''; return; }
  s.textContent=PLAY.result ? (PLAY.result+' — '+PLAY.reason) :
    (PLAY.pending ? 'Bot is thinking…' : (playTurnColor()==='white'?'White':'Black')+' to move');
  if(PLAY.lastMeta){
    m.textContent='Last bot move: '+PLAY.lastMeta.basis+' · confidence '+PLAY.lastMeta.confidence+
      ' · samples '+PLAY.lastMeta.matched_samples+' · share '+PLAY.lastMeta.matched_share+
      ' · source games '+PLAY.lastMeta.source_games+' · Elo '+PLAY.lastMeta.elo;
  } else m.textContent='';
}
function renderPlayMoves(){
  const el=document.getElementById('playMoves'); if(!el) return;
  if(!PLAY.game){ el.innerHTML='<span class="muted">No game started.</span>'; return; }
  const hist=PLAY.game.history();
  let h=''; hist.forEach((mv,i)=>{ if(i%2===0) h+='<span class="muted"> '+(i/2+1)+'.</span>'; h+=' '+esc(mv); });
  el.innerHTML=h||'<span class="muted">No moves yet.</span>';
}
function renderPlayBoard(){
  const el=document.getElementById('playBoard'); if(!el || !window.Chess) return;
  const fen=(PLAY.game||new window.Chess()).fen().split(' ')[0], rows=fen.split('/'), grid=[];
  for(const row of rows){ const r=[]; for(const ch of row){ if(/\d/.test(ch)) for(let k=0;k<+ch;k++) r.push(''); else r.push(ch); } grid.push(r); }
  const order=[...Array(8).keys()], rIdx=PLAY.orient==='white'?order:[...order].reverse(), cIdx=PLAY.orient==='white'?order:[...order].reverse();
  const legal=new Set(PLAY.legalTargets||[]); let cells='';
  for(const ri of rIdx){ for(const ci of cIdx){
    const sq=FILES_STR_JS[ci]+(8-ri), dark=(ri+ci)%2===1, pc=grid[ri][ci];
    const cls=[dark?'sqD':'sqL']; if(sq===PLAY.selectedSq) cls.push('sel'); if(legal.has(sq)) cls.push('legal');
    if(PLAY.lastMove && (sq===PLAY.lastMove.from || sq===PLAY.lastMove.to)) cls.push('last');
    cells+='<span class="'+cls.join(' ')+'"'+pieceStyle(pc)+' onclick="playSquare(\''+sq+'\')">'+coordLabels(ri,ci,rIdx,cIdx)+'</span>';
  }}
  el.innerHTML=cells;
}
const FILES_STR_JS='abcdefgh';

/* ---------------- Board viewer ---------------- */
async function openGame(id, jumpPly){
  try{
    viewer=await api('/api/game?id='+id);
    orient=viewer.orientation==='black'?'black':'white';
    curPly=0;
    document.getElementById('vtitle').textContent=viewer.white+' — '+viewer.black+'  '+viewer.result;
    document.getElementById('vsub').textContent=
      (viewer.event||'')+' · '+(viewer.date||'')+' · '+(viewer.opening||'')+' ('+(viewer.eco||'')+')';
    document.getElementById('verr').textContent=viewer.replay_error||'';
    renderMoves(); goPly(jumpPly||0);   // jump to the engine's flagged critical ply when given
    document.getElementById('modal').classList.add('open');
  }catch(e){ toast('Could not load game: '+e.message, 'error'); }
}
function closeModal(){ document.getElementById('modal').classList.remove('open'); }
function flip(){ orient = orient==='white'?'black':'white'; drawBoard(); }
function renderMoves(){
  let h='';
  viewer.moves.forEach((m,i)=>{
    if(i%2===0) h+='<span class="muted"> '+(i/2+1)+'.</span>';
    h+='<span class="mv" id="mv-'+(i+1)+'" onclick="goPly('+(i+1)+')"> '+esc(m)+'</span>';
  });
  document.getElementById('vmoves').innerHTML=h||'<span class="muted">No moves.</span>';
}
function goPly(p){
  if(!viewer) return;
  curPly=Math.max(0, Math.min(p, viewer.fens.length-1));
  drawBoard();
  document.querySelectorAll('.vmoves .mv').forEach(s=>s.classList.remove('cur'));
  const cur=document.getElementById('mv-'+curPly);
  if(cur){ cur.classList.add('cur'); cur.scrollIntoView({block:'nearest'}); }
}
function drawBoard(){
  const fen=viewer.fens[curPly].split(' ')[0];
  const rows=fen.split('/'); const grid=[];
  for(const row of rows){ const r=[];
    for(const ch of row){ if(/\d/.test(ch)) for(let k=0;k<+ch;k++) r.push('');
      else r.push(ch); }
    grid.push(r); }
  let cells='';
  const order=[...Array(8).keys()];
  const rIdx = orient==='white'? order : [...order].reverse();
  const cIdx = orient==='white'? order : [...order].reverse();
  for(const ri of rIdx){ for(const ci of cIdx){
    const dark=(ri+ci)%2===1;
    const pc=grid[ri][ci];
    cells+='<span class="'+(dark?'sqD':'sqL')+'"'+pieceStyle(pc)+'>'+coordLabels(ri,ci,rIdx,cIdx)+'</span>'; } }
  document.getElementById('board').innerHTML=cells;
}
document.addEventListener('keydown',e=>{
  if(!document.getElementById('modal').classList.contains('open')) return;
  if(e.key==='ArrowRight') goPly(curPly+1);
  else if(e.key==='ArrowLeft') goPly(curPly-1);
  else if(e.key==='Escape') closeModal();
});

refresh();
</script>
</body>
</html>
"""


# ===========================================================================
# ENTRY POINT
# ===========================================================================
def main():
    global ONLINE_ENABLED, ENGINE_DEPTH
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Tournament Prep Manual app (Dino Ballecer 2026)")
    ap.add_argument("--port", type=int, default=DEFAULT_PORT)
    ap.add_argument("--no-browser", action="store_true")
    ap.add_argument("--export", action="store_true",
                    help="headless: scan + write markdown sections, no server")
    ap.add_argument("--scan-only", action="store_true", help="headless: scan and exit")
    ap.add_argument("--engine-check", action="store_true",
                    help="probe Stockfish + opening DB, eval the start position, exit")
    ap.add_argument("--analyze", action="store_true",
                    help="run the engine analysis pass over stored games after scanning")
    ap.add_argument("--scope", choices=["fast", "all", "losses", "player"], default="fast",
                    help="--analyze scope (default: fast tournament pass)")
    ap.add_argument("--player", type=int, default=None,
                    help="player_id for --scope player")
    ap.add_argument("--depth", type=int, default=ENGINE_DEPTH,
                    help=f"engine search depth (default {ENGINE_DEPTH})")
    ap.add_argument("--max-games", type=int, default=None,
                    help="cap the number of games analysed (for a quick pass)")
    ap.add_argument("--online", action="store_true",
                    help="opt in to Lichess cloud-eval/explorer (off by default)")
    args = ap.parse_args()
    if args.analyze and args.scope == "player" and args.player is None:
        ap.error("--scope player requires --player PLAYER_ID")

    ONLINE_ENABLED = args.online
    ENGINE_DEPTH = args.depth

    if args.engine_check:
        path = find_stockfish()
        print(f"Stockfish binary : {path or 'NOT FOUND (set PREP_STOCKFISH or use ./stockfish/)'}")
        idx = load_opening_index()
        print(f"Opening database : {OPENING_INDEX_PATH if idx else 'NOT FOUND'}"
              + (f"  ({len(idx)} positions)" if idx else ""))
        eng = get_engine()
        if eng is None:
            print("Engine           : unavailable — engine analysis will be skipped.")
            return
        fen = MiniBoard().fen()
        with _ENGINE_LOCK:
            cp, mate, best = eng.analyse(fen, args.depth)
        sc = fold_score(cp, mate, True)
        print(f"Engine           : {eng.name}")
        print(f"Start position   : {cp_to_pawns(sc)} (White POV)  best "
              f"{uci_to_long(fen, best)} [{best}]")
        eng.close()
        return

    init_db()
    conn = db()
    summary = scan(conn)
    print(f"Scanned {summary['files']} PGN file(s): {summary['games_seen']} games seen, "
          f"{summary['games_stored']} stored for roster players.")
    for r in conn.execute("SELECT real_name, is_hero, "
                          "(SELECT COUNT(*) FROM Games g WHERE g.player_id=Roster.player_id) n "
                          "FROM Roster ORDER BY is_hero DESC, fide DESC"):
        mark = "*" if r["is_hero"] else " "
        print(f"  {mark} {r['real_name']:<30} {r['n']:>4} games")

    if args.analyze:
        if get_engine() is None and not ONLINE_ENABLED:
            print("\n--analyze: no engine found and --online not set; skipping analysis.")
        else:
            print(f"\nEngine analysis (depth {args.depth}, scope {args.scope}) — "
                  f"{engine_info()['name'] or 'lichess-cloud'}:")

            def _prog(done, total):
                print(f"\r  analyzing {done}/{total} games...", end="", flush=True)

            res = analyze_all(conn, depth=args.depth, scope=args.scope, pid=args.player,
                              max_games=args.max_games, status=ANALYZE_STATUS,
                              progress=_prog)
            print(f"\r  analysed {res['analyzed']}/{res['total']} games. "
                  f"PositionEval cache rows: "
                  f"{conn.execute('SELECT COUNT(*) FROM PositionEval').fetchone()[0]}")

    if args.export:
        files = export_markdown(conn)
        print(f"\nWrote {len(files)} markdown file(s) to {EXPORT_DIR}")
        conn.close()
        return
    if args.scan_only:
        conn.close()
        return
    conn.close()

    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    url = f"http://localhost:{args.port}"
    print(f"\nPrep app running at {url}   (Ctrl+C to stop)")
    print("Drop opponent PGN databases into this folder, then click 'Rescan' in the app.")
    if not args.no_browser:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
