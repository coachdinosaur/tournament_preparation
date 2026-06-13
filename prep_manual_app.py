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

No third-party packages required (Python 3.10+ standard library only).
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import re
import sqlite3
import sys
import threading
import webbrowser
from collections import Counter
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "prep_manual.db"
EXPORT_DIR = BASE_DIR / "manual_sections"
DEFAULT_PORT = 8765

# Lichess scout data produced by lichess_tournament_prep.py (metadata only,
# no moves — games link out to lichess.org instead of the built-in board).
LICHESS_DB = BASE_DIR / "tournament_pool_2026.db"
LICHESS_CSV = BASE_DIR / "tournament_pool_2026_Games.csv"

# ---------------------------------------------------------------------------
# ROSTER — Dino + the 9 opponents (same pool as lichess_tournament_prep.py)
# ---------------------------------------------------------------------------
HERO_NAME = "Dino Ballecer"
HERO_ALIASES = ["coach dinosaur", "ballecer, dino", "dino ballecer", "ballecer dino"]

ROSTER: list[dict] = [
    {"real_name": HERO_NAME,                  "title": "",   "federation": "PHI", "fide": None, "is_hero": 1},
    {"real_name": "GM Vignesh, N R",          "title": "GM", "federation": "IND", "fide": 2515, "is_hero": 0},
    {"real_name": "GM Shyaam, Nikhil P",      "title": "GM", "federation": "IND", "fide": 2435, "is_hero": 0},
    {"real_name": "IM Vignesh, Advaith Vemula","title": "IM","federation": "IND", "fide": 2421, "is_hero": 0},
    {"real_name": "IM Tan, Jun Ying",         "title": "IM", "federation": "MAS", "fide": 2404, "is_hero": 0},
    {"real_name": "IM Chan, Kim Yew",         "title": "IM", "federation": "MAS", "fide": 2360, "is_hero": 0},
    {"real_name": "IM Susilodinata, Andrean", "title": "IM", "federation": "INA", "fide": 2360, "is_hero": 0},
    {"real_name": "GM Thejkumar, M. S.",      "title": "GM", "federation": "IND", "fide": 2358, "is_hero": 0},
    {"real_name": "FM Ang, Ern Jie Anderson", "title": "FM", "federation": "MAS", "fide": 2309, "is_hero": 0},
    {"real_name": "FM Arlan Cabe",            "title": "FM", "federation": "PHI", "fide": 2298, "is_hero": 0},
]

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
        self._make(cands[0], to, (promo if self.white else promo.lower()) if promo else None)


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
"""


def db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = db()
    conn.executescript(SCHEMA)
    cols = {r[1] for r in conn.execute("PRAGMA table_info(Games)")}
    if "lichess_id" not in cols:  # migrate pre-Lichess databases (scan() refills)
        conn.executescript("DROP TABLE IF EXISTS Tags; DROP TABLE IF EXISTS Games;")
        conn.executescript(SCHEMA)
    for p in ROSTER:
        conn.execute(
            """INSERT INTO Roster (real_name, title, federation, fide, is_hero)
               VALUES (?,?,?,?,?)
               ON CONFLICT(real_name) DO UPDATE SET
                 title=excluded.title, federation=excluded.federation,
                 fide=excluded.fide, is_hero=excluded.is_hero""",
            (p["real_name"], p["title"], p["federation"], p["fide"], p["is_hero"]))
    hero_id = conn.execute("SELECT player_id FROM Roster WHERE is_hero=1").fetchone()[0]
    for a in HERO_ALIASES:
        conn.execute("INSERT OR IGNORE INTO Aliases (alias, player_id, source) VALUES (?,?,'seed')",
                     (a, hero_id))
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
    conn.execute("DELETE FROM Games")
    conn.execute("DELETE FROM Files")
    conn.execute("DELETE FROM UnmatchedNames")
    unmatched: Counter = Counter()
    summary = {"files": 0, "games_seen": 0, "games_stored": 0}

    for path in sorted(BASE_DIR.glob("*.pgn")):
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
# ANALYSIS
# ===========================================================================
def score_pct(w: int, d: int, l: int) -> float:
    n = w + d + l
    return round(100.0 * (w + 0.5 * d) / n, 1) if n else 0.0


def wdl(games: list[dict]) -> dict:
    w = sum(1 for g in games if g["presult"] == "win")
    d = sum(1 for g in games if g["presult"] == "draw")
    l = sum(1 for g in games if g["presult"] == "loss")
    return {"n": len(games), "w": w, "d": d, "l": l, "score": score_pct(w, d, l)}


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
    line_groups: dict[tuple, list] = {}
    for r in loss_rows:
        mv = json.loads(r["moves_json"])[:8]
        if len(mv) >= 6:
            line_groups.setdefault((r["color"], " ".join(mv)), []).append(r)
    repeated = [{"color": k[0], "line": k[1], "count": len(v),
                 "opening": v[0]["opening"], "game_ids": [x["game_id"] for x in v]}
                for k, v in line_groups.items() if len(v) >= 2]
    repeated.sort(key=lambda x: -x["count"])

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
                f"({abs(ws-bs):.0f}-point gap). The {weaker} repertoire is the top priority.")
        for color, table in (("White", op_w), ("Black", op_b)):
            weak = [r for r in table if r["n"] >= 2 and r["score"] < 50]
            weak.sort(key=lambda r: (r["score"], -r["n"]))
            for r in weak[:3]:
                bullets.append(
                    f"As {color} — {r['opening']} ({r['eco']}): scoring only "
                    f"{r['score']}% over {r['n']} games "
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
                f"({rl['opening']}): lost {rl['count']} games starting "
                f"{rl['line']} — fix this exact sequence before the event.")
        for f in fams:
            if f["n"] == 0:
                bullets.append(
                    f"No practical games in the \"{f['family']}\" family — a core manual "
                    "structure with zero reps. Schedule training games in it.")
            elif f["n"] >= 2 and f["score"] < 50:
                bullets.append(
                    f"Underperforming in the \"{f['family']}\" family: "
                    f"{f['score']}% over {f['n']} games.")
        strong = [r for r in op_w + op_b if r["n"] >= 3 and r["score"] >= 70]
        if strong:
            names = ", ".join(f"{r['opening']} ({r['score']}%)" for r in strong[:3])
            bullets.append(f"Confidence weapons to keep sharp (not change): {names}.")

    return {
        "hero": dict(hero),
        "record": rec, "white": {**rec_w, "openings": op_w},
        "black": {**rec_b, "openings": op_b},
        "families": fams, "loss_phases": phases,
        "repeated_lines": repeated, "bullets": bullets,
        "losses": [g for g in games if g["presult"] == "loss"],
    }


# ===========================================================================
# MARKDOWN EXPORT
# ===========================================================================
def md_wdl(r: dict) -> str:
    return f"{r['w']}W {r['d']}D {r['l']}L ({r['score']}%)"


def md_opening_table(rows: list[dict], limit: int = 12) -> str:
    if not rows:
        return "_No games on file yet._\n"
    out = ["| Opening | ECO | Games | W-D-L | Score |",
           "|---|---|---:|---|---:|"]
    for r in rows[:limit]:
        out.append(f"| {r['opening']} | {r['eco']} | {r['n']} | "
                   f"{r['w']}-{r['d']}-{r['l']} | {r['score']}% |")
    return "\n".join(out) + "\n"


def md_family_table(rows: list[dict]) -> str:
    out = ["| Core Structure Family | Games | W-D-L | Score |",
           "|---|---:|---|---:|"]
    for r in rows:
        out.append(f"| {r['family']} | {r['n']} | {r['w']}-{r['d']}-{r['l']} | "
                   f"{r['score']}% |" if r["n"] else f"| {r['family']} | 0 | — | — |")
    return "\n".join(out) + "\n"


def safe_filename(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]+", "_", s).strip("_")


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
    lines += ["", f"## Openings as White ({imp['white']['n']} games)", "",
              md_opening_table(imp["white"]["openings"], 20), "",
              f"## Openings as Black ({imp['black']['n']} games)", "",
              md_opening_table(imp["black"]["openings"], 20), "",
              "## Core Structure Families (own games)", "",
              md_family_table(imp["families"]), "",
              "## Loss profile", ""]
    for k, v in imp["loss_phases"].items():
        lines.append(f"- Losses in {k}: **{v}**")
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
            elif u.path == "/api/state":
                self._json(self.state())
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
            return {"roster": roster, "files": files, "unmatched": unmatched,
                    "aliases": aliases, "folder": str(BASE_DIR)}
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
        --acc:#4da3ff; --good:#4ec77a; --bad:#e2645a; --warn:#e2b75a; --line:#2c3645; }
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--text);
       font:14px/1.45 "Segoe UI", system-ui, sans-serif; }
header { padding:14px 22px; background:var(--panel); border-bottom:1px solid var(--line);
         display:flex; align-items:center; gap:16px; flex-wrap:wrap; }
header h1 { font-size:17px; margin:0; }
header .sub { color:var(--dim); font-size:12px; }
button { background:var(--panel2); color:var(--text); border:1px solid var(--line);
         border-radius:6px; padding:6px 12px; cursor:pointer; font-size:13px; }
button:hover { border-color:var(--acc); }
button.primary { background:var(--acc); color:#08121f; border-color:var(--acc); font-weight:600; }
nav { display:flex; gap:4px; padding:10px 22px 0; background:var(--panel);
      border-bottom:1px solid var(--line); flex-wrap:wrap; }
nav button { border-radius:8px 8px 0 0; border-bottom:none; padding:8px 16px; }
nav button.on { background:var(--bg); color:var(--acc); font-weight:600; }
main { padding:18px 22px 60px; max-width:1280px; margin:0 auto; }
.card { background:var(--panel); border:1px solid var(--line); border-radius:10px;
        padding:14px 16px; margin-bottom:16px; }
.card h2 { margin:0 0 10px; font-size:15px; color:var(--acc); }
.card h3 { margin:14px 0 6px; font-size:13.5px; }
table { border-collapse:collapse; width:100%; font-size:13px; }
th { text-align:left; color:var(--dim); font-weight:600; padding:5px 8px;
     border-bottom:1px solid var(--line); white-space:nowrap; }
td { padding:5px 8px; border-bottom:1px solid var(--line); }
tr.click:hover { background:var(--panel2); cursor:pointer; }
.score-hi { color:var(--good); font-weight:600; }
.score-lo { color:var(--bad); font-weight:600; }
.score-md { color:var(--warn); }
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
          padding:18px; display:flex; gap:18px; max-width:92vw; max-height:92vh; }
.board { display:grid; grid-template-columns:repeat(8, 52px); grid-template-rows:repeat(8, 52px);
         border:2px solid var(--line); }
.sqL { background:#e9d7b7; } .sqD { background:#a87e58; }
.board span { display:flex; align-items:center; justify-content:center;
              font-size:38px; line-height:1; user-select:none; }
.vside { width:330px; display:flex; flex-direction:column; min-height:0; }
.vmoves { flex:1; overflow:auto; background:var(--panel2); border-radius:8px;
          padding:8px; font-size:13px; margin:10px 0; }
.vmoves span.mv { cursor:pointer; padding:1px 4px; border-radius:4px; }
.vmoves span.mv.cur { background:var(--acc); color:#08121f; }
.vbtns { display:flex; gap:6px; }
.pill { font-size:11px; border-radius:10px; padding:2px 8px; }
.pill.w { background:#1d3a26; color:var(--good);} .pill.l { background:#3a201d; color:var(--bad);}
.pill.d { background:#37321d; color:var(--warn);} .pill.u { background:var(--panel2); color:var(--dim);}
#toast { position:fixed; bottom:18px; right:18px; background:var(--panel2);
         border:1px solid var(--acc); color:var(--text); padding:10px 16px;
         border-radius:8px; display:none; z-index:60; max-width:420px; }
.small { font-size:12px; }
</style>
</head>
<body>
<header>
  <h1>Tournament Prep Manual — Dino Ballecer 2026</h1>
  <span class="sub" id="folder"></span>
  <span style="flex:1"></span>
  <button class="primary" onclick="rescan()">⟳ Rescan PGN folder</button>
</header>
<nav>
  <button id="tb-overview" class="on" onclick="tab('overview')">Overview</button>
  <button id="tb-opponents" onclick="tab('opponents')">Opponents</button>
  <button id="tb-dino" onclick="tab('dino')">Dino — Needs Improvement</button>
  <button id="tb-files" onclick="tab('files')">Files &amp; Names</button>
  <button id="tb-export" onclick="tab('export')">Export Manual Sections</button>
</nav>
<main>
  <div id="pg-overview"></div>
  <div id="pg-opponents" style="display:none"></div>
  <div id="pg-dino" style="display:none"></div>
  <div id="pg-files" style="display:none"></div>
  <div id="pg-export" style="display:none"></div>
</main>

<div id="modal" onclick="if(event.target===this) closeModal()">
  <div class="viewer">
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

<script>
let STATE=null, curTab='overview', curPlayer=null, viewer=null, curPly=0, orient='white';
const PIECES={K:'♔',Q:'♕',R:'♖',B:'♗',N:'♘',P:'♙',
              k:'♚',q:'♛',r:'♜',b:'♝',n:'♞',p:'♟'};

function toast(msg){ const t=document.getElementById('toast'); t.textContent=msg;
  t.style.display='block'; clearTimeout(t._h); t._h=setTimeout(()=>t.style.display='none',4000); }
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
  for(const t of ['overview','opponents','dino','files','export']){
    document.getElementById('pg-'+t).style.display = t===name?'':'none';
    document.getElementById('tb-'+t).classList.toggle('on', t===name); }
  if(name==='dino') loadDino();
  if(name==='opponents') renderOpponents();
}

async function refresh(){ STATE=await api('/api/state');
  document.getElementById('folder').textContent='watching: '+STATE.folder+'\\*.pgn';
  renderOverview(); renderFiles(); renderExportTab();
  if(curTab==='opponents') renderOpponents(); }

async function rescan(){ try{ const r=await post('/api/scan');
  toast('Scanned '+r.summary.files+' files — '+r.summary.games_stored+' games stored.');
  await refresh(); if(curTab==='dino') loadDino(); if(curPlayer) selectPlayer(curPlayer);
 }catch(e){ toast('Scan failed: '+e.message); } }

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
  el.innerHTML='<div class="card muted">Loading…</div>';
  try{
    const d=await api('/api/player?id='+pid);
    el.innerHTML=dossierHtml(d);
  }catch(e){ el.innerHTML='<div class="card">Error: '+esc(e.message)+'</div>'; }
}

function openingTbl(rows){
  if(!rows.length) return '<p class="muted">No games.</p>';
  let h='<table><tr><th>Opening</th><th>ECO</th><th>N</th><th>W-D-L</th><th>Score</th></tr>';
  for(const r of rows) h+='<tr><td>'+esc(r.opening)+'</td><td>'+esc(r.eco)+'</td><td>'+r.n+
    '</td><td>'+r.w+'-'+r.d+'-'+r.l+'</td><td class="'+scoreCls(r.score,r.n)+'">'+r.score+'%</td></tr>';
  return h+'</table>';
}
function famTbl(rows){
  let h='<table><tr><th>Core Structure Family</th><th>N</th><th>W-D-L</th><th>Score</th></tr>';
  for(const r of rows) h+='<tr><td>'+esc(r.family)+'</td><td>'+r.n+'</td><td>'+
    (r.n?(r.w+'-'+r.d+'-'+r.l):'—')+'</td><td class="'+scoreCls(r.score,r.n)+'">'+
    (r.n?r.score+'%':'—')+'</td></tr>';
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
    '<div class="cols"><div><h3>As White — '+d.white.n+' games ('+d.white.score+'%)</h3>'+
    openingTbl(d.white.openings)+'</div><div><h3>As Black — '+d.black.n+' games ('+
    d.black.score+'%)</h3>'+openingTbl(d.black.openings)+'</div></div>'+
    '<h3>Core Structure Families</h3>'+famTbl(d.families)+'</div>'+
    '<div class="card"><h2>Games ('+d.games.length+') — click to replay</h2>'+
    gamesTbl(d.games)+'</div>';
}

/* ---------------- Dino tab ---------------- */
async function loadDino(){
  const el=document.getElementById('pg-dino');
  el.innerHTML='<div class="card muted">Analysing…</div>';
  try{
    const d=await api('/api/improvement');
    let h='<div class="card"><h2>&#11088; '+esc(d.hero.real_name)+' — own-game audit ('+
      d.record.n+' games)</h2><p>Overall <b>'+d.record.w+'-'+d.record.d+'-'+d.record.l+
      '</b> ('+d.record.score+'%) &middot; White '+d.white.score+'% ('+d.white.n+
      ') &middot; Black '+d.black.score+'% ('+d.black.n+')</p></div>';
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
    h+='<table><tr><th>Name in PGN</th><th>Games</th><th>Map to roster player</th><th></th></tr>';
    STATE.unmatched.forEach((u,i)=>{
      h+='<tr><td>'+esc(u.name)+'</td><td>'+u.games+'</td>'+
         '<td><select id="map-'+i+'"><option value="">— choose —</option>'+opts+'</select> '+
         '<button onclick="mapName('+i+')">Map</button></td>'+
         '<td><button onclick="ignoreName('+i+')">Ignore</button></td></tr>'; });
    h+='</table>';
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
}
async function mapName(i){
  const u=STATE.unmatched[i]; const pid=document.getElementById('map-'+i).value;
  if(!pid){ toast('Choose a roster player first.'); return; }
  try{ await post('/api/map',{name:u.name, player_id:+pid});
       toast('Mapped "'+u.name+'" — rescanned.'); await refresh(); }
  catch(e){ toast('Failed: '+e.message); }
}
async function ignoreName(i){
  try{ await post('/api/ignore',{name:STATE.unmatched[i].name}); await refresh(); }
  catch(e){ toast('Failed: '+e.message); }
}
async function unmap(alias){
  try{ await post('/api/unmap',{alias}); toast('Removed mapping — rescanned.'); await refresh(); }
  catch(e){ toast('Failed: '+e.message); }
}
async function pastePgn(){
  const text=document.getElementById('pasteText').value;
  const name=document.getElementById('pasteName').value;
  try{ const r=await post('/api/paste',{text, filename:name});
       toast('Saved as '+r.saved_as+' and scanned.');
       document.getElementById('pasteText').value=''; await refresh(); }
  catch(e){ toast('Failed: '+e.message); }
}

/* ---------------- Export ---------------- */
function renderExportTab(){
  document.getElementById('pg-export').innerHTML=
   '<div class="card"><h2>Export Markdown sections for the manual</h2>'+
   '<p class="muted">Writes one dossier per opponent plus '+
   '<b>Dino_Ballecer_Needs_Improvement.md</b> into the <code>manual_sections</code> folder. '+
   'Open them in any editor and paste into Tournament_Preparation_Manual.docx. '+
   'Re-export any time after adding PGNs.</p>'+
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

/* ---------------- Board viewer ---------------- */
async function openGame(id){
  try{
    viewer=await api('/api/game?id='+id);
    orient=viewer.orientation==='black'?'black':'white';
    curPly=0;
    document.getElementById('vtitle').textContent=viewer.white+' — '+viewer.black+'  '+viewer.result;
    document.getElementById('vsub').textContent=
      (viewer.event||'')+' · '+(viewer.date||'')+' · '+(viewer.opening||'')+' ('+(viewer.eco||'')+')';
    document.getElementById('verr').textContent=viewer.replay_error||'';
    renderMoves(); goPly(0);
    document.getElementById('modal').classList.add('open');
  }catch(e){ toast('Could not load game: '+e.message); }
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
    cells+='<span class="'+(dark?'sqD':'sqL')+'">'+(pc?PIECES[pc]:'')+'</span>'; } }
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
    args = ap.parse_args()

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
