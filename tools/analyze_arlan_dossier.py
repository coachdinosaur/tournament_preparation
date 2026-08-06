#!/usr/bin/env python3
"""Build a reproducible evidence pack for Arlan Cabe's opponent dossier.

The script deliberately keeps career, recent-classical, and fast/online games
separate.  Stockfish is used only on the selected model games; those results
are a critical-position screen, not a whole-career accuracy profile.
"""

from __future__ import annotations

import argparse
import collections
import io
import json
import math
import re
import statistics
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import chess
import chess.engine
import chess.pgn


ROOT = Path(__file__).resolve().parents[1]
RECENT_YEAR = 2022


OPPONENTS: list[dict[str, Any]] = [
    {
        "file_token": "Kiriakov_Petr",
        "name": "Petr Kiriakov",
        "pgn_name": "Kiriakov,Petr",
        "terms": ["kiriakov", "petr"],
        "title": "GM",
        "fed": "FID",
        "rating": 2459,
        "seed": 1,
        "fide_id": "4119231",
    },
    {
        "file_token": "Tu_Hoang_20Thong",
        "name": "Tu Hoang Thong",
        "pgn_name": "Tu,Hoang Thong",
        "terms": ["tu", "hoang", "thong"],
        "title": "GM",
        "fed": "VIE",
        "rating": 2346,
        "seed": 2,
        "fide_id": "12400076",
    },
    {
        "file_token": "Cao_Sang",
        "name": "Cao Sang",
        "pgn_name": "Cao,Sang",
        "terms": ["cao", "sang"],
        "title": "GM",
        "fed": "VIE",
        "rating": 2344,
        "seed": 3,
        "fide_id": "725056",
    },
    {
        "file_token": "Antonio_Rogelio_20Jr",
        "name": "Rogelio Antonio Jr",
        "pgn_name": "Antonio,Rogelio Jr",
        "terms": ["antonio", "rogelio"],
        "title": "GM",
        "fed": "PHI",
        "rating": 2333,
        "seed": 4,
        "fide_id": "5200032",
    },
    {
        "file_token": "Paciencia_Enrique_20Rivas",
        "name": "Enrique Paciencia",
        "pgn_name": "Paciencia,Enrique Rivas",
        "terms": ["paciencia", "enrique"],
        "title": "IM",
        "fed": "SGP",
        "rating": 2259,
        "seed": 6,
        "fide_id": "5201322",
    },
    {
        "file_token": "Than_Min_20Hlaing",
        "name": "Than Min Hlaing",
        "pgn_name": "Than,Min Hlaing",
        "terms": ["than", "min", "hlaing"],
        "title": "",
        "fed": "MYA",
        "rating": 2140,
        "seed": 7,
        "fide_id": "13001353",
    },
    {
        "file_token": "Lindri_Juni_20Wijayanti",
        "name": "Lindri Juni Widjayanti",
        "pgn_name": "Wijayanti,Lindri Juni",
        "terms": ["lindri", "juni"],
        "title": "WIM",
        "fed": "INA",
        "rating": 2127,
        "seed": 8,
        "fide_id": "7100361",
    },
    {
        "file_token": "Young_Angelo",
        "name": "Angelo Young",
        "pgn_name": "Young,Angelo",
        "terms": ["young", "angelo"],
        "title": "IM",
        "fed": "PHI",
        "rating": 2119,
        "seed": 9,
        "fide_id": "5200490",
    },
    {
        "file_token": "Khegay_Anjela",
        "name": "Anjela Khegay",
        "pgn_name": "Khegay,Anjela",
        "terms": ["khegay", "anjela"],
        "title": "WIM",
        "fed": "SGP",
        "rating": 2012,
        "seed": 10,
        "fide_id": "14200473",
    },
]


HERO = {
    "name": "Arlan Cabe",
    "pgn_name": "Cabe,Arlan",
    "terms": ["cabe", "arlan"],
    "title": "FM",
    "fed": "PHI",
    "rating": 2298,
    "seed": 5,
    "fide_id": "5203627",
}


FAST_RE = re.compile(
    r"\b(blitz|rapid|bullet|titled\s*tuesday|online|internet|playchess|lichess|"
    r"chess\.com|speed\s*chess|quickplay|world\s*rapid|world\s*blitz)\b",
    re.I,
)


def norm_name(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.lower()))


def name_matches(value: str, terms: Iterable[str]) -> bool:
    tokens = set(norm_name(value).split())
    return all(term.lower() in tokens for term in terms)


def parse_date(value: str) -> tuple[int, int, int]:
    parts = (value or "").replace("-", ".").split(".")
    try:
        year = int(parts[0]) if parts and parts[0].isdigit() else 0
        month = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
        day = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 0
        return (year, month, day)
    except (TypeError, ValueError):
        return (0, 0, 0)


def result_for_color(result: str, color: chess.Color) -> float | None:
    if result == "1-0":
        return 1.0 if color == chess.WHITE else 0.0
    if result == "0-1":
        return 1.0 if color == chess.BLACK else 0.0
    if result == "1/2-1/2":
        return 0.5
    return None


def is_fast(headers: dict[str, str]) -> bool:
    haystack = " ".join(
        headers.get(k, "")
        for k in ("Event", "Site", "TimeControl", "EventDate", "Annotator")
    )
    return bool(FAST_RE.search(haystack))


def position_key(board: chess.Board) -> str:
    # En-passant is intentionally omitted: opening names should survive a
    # harmless EP-field difference while retaining turn and castling rights.
    return f"{board.board_fen()} {int(board.turn)} {board.castling_xfen()}"


def load_opening_book(openings_dir: Path) -> dict[str, tuple[int, str, str]]:
    book: dict[str, tuple[int, str, str]] = {}
    for tsv in sorted(openings_dir.glob("*.tsv")):
        with tsv.open("r", encoding="utf-8-sig", errors="replace") as handle:
            next(handle, None)
            for raw in handle:
                parts = raw.rstrip("\n").split("\t", 2)
                if len(parts) != 3:
                    continue
                eco, name, pgn_moves = parts
                pgn_text = f'[Result "*"]\n\n{pgn_moves} *\n'
                try:
                    game = chess.pgn.read_game(io.StringIO(pgn_text))
                    if game is None:
                        continue
                    board = game.board()
                    ply = 0
                    for move in game.mainline_moves():
                        board.push(move)
                        ply += 1
                    key = position_key(board)
                    if ply >= book.get(key, (-1, "", ""))[0]:
                        book[key] = (ply, eco, name)
                except Exception:
                    continue
    return book


def san_line(game: chess.pgn.Game, max_plies: int | None = None) -> list[str]:
    board = game.board()
    sans: list[str] = []
    for index, move in enumerate(game.mainline_moves()):
        if max_plies is not None and index >= max_plies:
            break
        try:
            sans.append(board.san(move))
            board.push(move)
        except Exception:
            break
    return sans


def format_line(sans: list[str], plies: int = 8) -> str:
    out: list[str] = []
    for index, san in enumerate(sans[:plies]):
        move_no = index // 2 + 1
        if index % 2 == 0:
            out.append(f"{move_no}.{san}")
        else:
            out[-1] += f" {san}"
    return " ".join(out)


def classify_opening(game: chess.pgn.Game, book: dict[str, tuple[int, str, str]]) -> tuple[str, str, int]:
    header_eco = game.headers.get("ECO", "")
    header_opening = game.headers.get("Opening", "")
    header_variation = game.headers.get("Variation", "")
    best: tuple[int, str, str] | None = None
    board = game.board()
    for ply, move in enumerate(game.mainline_moves(), start=1):
        try:
            board.push(move)
        except Exception:
            break
        hit = book.get(position_key(board))
        if hit is not None and (best is None or hit[0] >= best[0]):
            best = hit
        if ply >= 32:
            break
    if best:
        depth, eco, name = best
        return (eco, name, depth)
    name = header_opening
    if header_variation:
        name = f"{name}: {header_variation}" if name else header_variation
    return (header_eco, name or "Unclassified", 0)


def opening_family(record: dict[str, Any]) -> str:
    name = record["opening"].lower()
    first = record["sans"][:6]
    joined = " ".join(move.rstrip("+#") for move in first)
    rules = [
        ("sicilian", "Sicilian"),
        ("caro-kann", "Caro-Kann"),
        ("french", "French"),
        ("ruy lopez", "Ruy Lopez"),
        ("italian", "Italian"),
        ("petrov", "Petroff"),
        ("scotch", "Scotch"),
        ("pirc", "Pirc / Modern"),
        ("modern defense", "Pirc / Modern"),
        ("scandinavian", "Scandinavian"),
        ("alekhine", "Alekhine"),
        ("nimzo-indian", "Nimzo-Indian"),
        ("queen's indian", "Queen's Indian"),
        ("king's indian", "King's Indian"),
        ("grünfeld", "Grunfeld"),
        ("grunfeld", "Grunfeld"),
        ("slav", "Slav / Semi-Slav"),
        ("semi-slav", "Slav / Semi-Slav"),
        ("queen's gambit declined", "QGD"),
        ("queen's gambit accepted", "QGA"),
        ("catalan", "Catalan"),
        ("dutch", "Dutch"),
        ("benoni", "Benoni / Benko"),
        ("benko", "Benoni / Benko"),
        ("english", "English / Reti"),
        ("réti", "English / Reti"),
        ("reti", "English / Reti"),
        ("london", "London"),
    ]
    for needle, family in rules:
        if needle in name:
            return family
    if joined.startswith("e4 e5"):
        return "1.e4 e5"
    if joined.startswith("d4 d5"):
        return "Queen's Pawn / 1...d5"
    if joined.startswith("d4 Nf6"):
        return "Indian Game"
    if first:
        return f"Other {first[0]}"
    return "Unclassified"


def game_to_record(
    game: chess.pgn.Game,
    subject: dict[str, Any],
    book: dict[str, tuple[int, str, str]],
    source: Path,
) -> dict[str, Any] | None:
    white = game.headers.get("White", "")
    black = game.headers.get("Black", "")
    if name_matches(white, subject["terms"]):
        color = chess.WHITE
        opponent = black
        subject_elo = game.headers.get("WhiteElo", "")
        opponent_elo = game.headers.get("BlackElo", "")
    elif name_matches(black, subject["terms"]):
        color = chess.BLACK
        opponent = white
        subject_elo = game.headers.get("BlackElo", "")
        opponent_elo = game.headers.get("WhiteElo", "")
    else:
        return None
    result = result_for_color(game.headers.get("Result", "*"), color)
    if result is None:
        return None
    sans = san_line(game)
    eco, opening, opening_depth = classify_opening(game, book)
    date_tuple = parse_date(game.headers.get("Date", ""))
    plies = len(sans)
    record = {
        "source": str(source.relative_to(ROOT)).replace("\\", "/"),
        "white": white,
        "black": black,
        "subject_color": "white" if color == chess.WHITE else "black",
        "opponent": opponent,
        "subject_elo": int(subject_elo) if str(subject_elo).isdigit() else None,
        "opponent_elo": int(opponent_elo) if str(opponent_elo).isdigit() else None,
        "result_header": game.headers.get("Result", "*"),
        "score": result,
        "date": game.headers.get("Date", ""),
        "date_tuple": list(date_tuple),
        "year": date_tuple[0],
        "event": game.headers.get("Event", ""),
        "site": game.headers.get("Site", ""),
        "round": game.headers.get("Round", ""),
        "fast": is_fast(dict(game.headers)),
        "plies": plies,
        "moves": math.ceil(plies / 2),
        "sans": sans,
        "line": format_line(sans, 10),
        "eco": eco,
        "opening": opening,
        "opening_depth": opening_depth,
    }
    record["family"] = opening_family(record)
    return record


def load_subject_games(
    paths: list[Path],
    subject: dict[str, Any],
    book: dict[str, tuple[int, str, str]],
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    seen: set[tuple[Any, ...]] = set()
    for path in paths:
        with path.open("r", encoding="utf-8-sig", errors="replace") as handle:
            while True:
                try:
                    game = chess.pgn.read_game(handle)
                except Exception as exc:
                    print(f"warning: PGN parser error in {path.name}: {exc}", file=sys.stderr)
                    continue
                if game is None:
                    break
                record = game_to_record(game, subject, book, path)
                if record is None:
                    continue
                signature = (
                    record["date"],
                    norm_name(record["white"]),
                    norm_name(record["black"]),
                    record["result_header"],
                    tuple(record["sans"][:16]),
                    record["plies"],
                )
                if signature in seen:
                    continue
                seen.add(signature)
                records.append(record)
    records.sort(key=lambda r: (r["date_tuple"], r["event"], r["round"]), reverse=True)
    return records


def wdl(records: list[dict[str, Any]]) -> dict[str, Any]:
    wins = sum(1 for r in records if r["score"] == 1.0)
    draws = sum(1 for r in records if r["score"] == 0.5)
    losses = sum(1 for r in records if r["score"] == 0.0)
    total = len(records)
    return {
        "games": total,
        "wins": wins,
        "draws": draws,
        "losses": losses,
        "score_pct": round(100 * (wins + 0.5 * draws) / total, 1) if total else None,
    }


def counter_rows(counter: collections.Counter[str], total: int, limit: int = 6) -> list[dict[str, Any]]:
    return [
        {"label": label, "games": count, "pct": round(100 * count / total, 1) if total else 0.0}
        for label, count in counter.most_common(limit)
    ]


def grouped_stats(records: list[dict[str, Any]], key: str, limit: int = 8) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for record in records:
        groups[str(record.get(key) or "Unknown")].append(record)
    rows: list[dict[str, Any]] = []
    for label, items in groups.items():
        row = {"label": label, **wdl(items)}
        rows.append(row)
    rows.sort(key=lambda row: (row["games"], row["score_pct"] or 0), reverse=True)
    return rows[:limit]


def response_stats(records: list[dict[str, Any]], first_move: str) -> list[dict[str, Any]]:
    selected = [
        record
        for record in records
        if record["subject_color"] == "black"
        and len(record["sans"]) >= 2
        and record["sans"][0].rstrip("+#") == first_move
    ]
    groups: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for record in selected:
        groups[record["sans"][1].rstrip("+#")].append(record)
    rows = []
    for response, games in groups.items():
        rows.append({"label": response, **wdl(games)})
    rows.sort(key=lambda row: (row["games"], row["score_pct"] or 0), reverse=True)
    return rows


def line_stats(records: list[dict[str, Any]], mode: str, limit: int = 5) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for record in records:
        sans = [s.rstrip("+#") for s in record["sans"]]
        if mode == "white" and record["subject_color"] == "white":
            key = format_line(sans, min(6, len(sans)))
        elif mode == "black_e4" and record["subject_color"] == "black" and sans and sans[0] == "e4":
            key = format_line(sans, min(8, len(sans)))
        elif mode == "black_d4" and record["subject_color"] == "black" and sans and sans[0] == "d4":
            key = format_line(sans, min(8, len(sans)))
        else:
            continue
        if key:
            groups[key].append(record)
    rows = [{"label": label, **wdl(items)} for label, items in groups.items()]
    rows.sort(key=lambda row: (row["games"], row["score_pct"] or 0), reverse=True)
    return rows[:limit]


def castling_profile(records: list[dict[str, Any]]) -> dict[str, Any]:
    counts = collections.Counter()
    for record in records:
        target_parity = 0 if record["subject_color"] == "white" else 1
        castle = "none"
        for index, san in enumerate(record["sans"]):
            if index % 2 != target_parity:
                continue
            clean = san.replace("+", "").replace("#", "")
            if clean == "O-O":
                castle = "king"
                break
            if clean == "O-O-O":
                castle = "queen"
                break
        counts[castle] += 1
    total = len(records)
    return {
        "kingside": counts["king"],
        "queenside": counts["queen"],
        "none": counts["none"],
        "queenside_pct": round(100 * counts["queen"] / total, 1) if total else 0.0,
    }


def select_model_games(records: list[dict[str, Any]], count: int = 2) -> list[dict[str, Any]]:
    classical = [r for r in records if not r["fast"]]
    recent = [r for r in classical if r["year"] >= RECENT_YEAR]
    pool = recent or classical
    selected: list[dict[str, Any]] = []
    for color in ("white", "black"):
        candidates = [r for r in pool if r["subject_color"] == color and r["score"] == 0.0]
        if candidates:
            selected.append(candidates[0])
    if len(selected) < count:
        extras = [r for r in pool if r["score"] == 0.0 and r not in selected]
        selected.extend(extras[: count - len(selected)])
    if len(selected) < count:
        extras = sorted(
            [r for r in pool if r not in selected],
            key=lambda r: (r["score"], -(r["opponent_elo"] or 0), r["date_tuple"]),
        )
        selected.extend(extras[: count - len(selected)])
    return selected[:count]


def summarize_subject(records: list[dict[str, Any]]) -> dict[str, Any]:
    classical = [r for r in records if not r["fast"]]
    fast = [r for r in records if r["fast"]]
    recent_classical = [r for r in classical if r["year"] >= RECENT_YEAR]
    white = [r for r in classical if r["subject_color"] == "white"]
    black = [r for r in classical if r["subject_color"] == "black"]
    recent_white = [r for r in recent_classical if r["subject_color"] == "white"]
    recent_black = [r for r in recent_classical if r["subject_color"] == "black"]
    dated_years = [r["year"] for r in records if r["year"]]
    lengths = [r["moves"] for r in classical]
    white_first = [r for r in recent_classical if r["subject_color"] == "white" and r["sans"]]
    first_counter = collections.Counter(r["sans"][0].rstrip("+#") for r in white_first)
    career_white_first = [r for r in classical if r["subject_color"] == "white" and r["sans"]]
    career_first_counter = collections.Counter(r["sans"][0].rstrip("+#") for r in career_white_first)
    late = [r for r in recent_classical if r["moves"] >= 41]
    short_draws = [r for r in recent_classical if r["score"] == 0.5 and r["moves"] <= 25]
    losses = [r for r in recent_classical if r["score"] == 0.0]
    loss_phase = collections.Counter(
        "opening / early" if r["moves"] <= 25 else "middlegame" if r["moves"] <= 40 else "late"
        for r in losses
    )
    years = collections.Counter(r["year"] for r in records if r["year"])
    return {
        "coverage": {
            "all": wdl(records),
            "classical": wdl(classical),
            "fast": wdl(fast),
            "recent_classical": wdl(recent_classical),
            "year_min": min(dated_years) if dated_years else None,
            "year_max": max(dated_years) if dated_years else None,
            "by_year": [{"year": year, "games": count} for year, count in sorted(years.items(), reverse=True)],
        },
        "colors": {
            "classical_white": wdl(white),
            "classical_black": wdl(black),
            "recent_white": wdl(recent_white),
            "recent_black": wdl(recent_black),
        },
        "recent_white_first_moves": counter_rows(first_counter, len(white_first), 6),
        "classical_white_first_moves": counter_rows(
            career_first_counter, len(career_white_first), 6
        ),
        "recent_responses": {
            "e4": response_stats(recent_classical, "e4"),
            "d4": response_stats(recent_classical, "d4"),
            "c4": response_stats(recent_classical, "c4"),
            "Nf3": response_stats(recent_classical, "Nf3"),
        },
        "classical_responses": {
            "e4": response_stats(classical, "e4"),
            "d4": response_stats(classical, "d4"),
            "c4": response_stats(classical, "c4"),
            "Nf3": response_stats(classical, "Nf3"),
        },
        "recent_families": {
            "white": grouped_stats(recent_white, "family", 8),
            "black": grouped_stats(recent_black, "family", 8),
        },
        "classical_families": {
            "white": grouped_stats(white, "family", 8),
            "black": grouped_stats(black, "family", 8),
        },
        "recent_openings": {
            "white": grouped_stats(recent_white, "opening", 8),
            "black": grouped_stats(recent_black, "opening", 8),
        },
        "recent_lines": {
            "white": line_stats(recent_classical, "white"),
            "black_e4": line_stats(recent_classical, "black_e4"),
            "black_d4": line_stats(recent_classical, "black_d4"),
        },
        "classical_lines": {
            "white": line_stats(classical, "white"),
            "black_e4": line_stats(classical, "black_e4"),
            "black_d4": line_stats(classical, "black_d4"),
        },
        "style": {
            "median_classical_length": round(statistics.median(lengths), 1) if lengths else None,
            "recent_late_games": wdl(late),
            "recent_short_draws": len(short_draws),
            "recent_loss_phase": dict(loss_phase),
            "castling": castling_profile(recent_classical),
        },
        "model_games": select_model_games(records),
    }


def game_from_record(record: dict[str, Any]) -> chess.pgn.Game:
    board = chess.Board()
    game = chess.pgn.Game()
    node: chess.pgn.GameNode = game
    for san in record["sans"]:
        move = board.parse_san(san)
        node = node.add_variation(move)
        board.push(move)
    return game


def score_cp(info: dict[str, Any], color: chess.Color) -> int:
    return int(info["score"].pov(color).score(mate_score=100000))


def pv_to_san(board: chess.Board, pv: list[chess.Move], plies: int = 5) -> str:
    probe = board.copy()
    sans: list[str] = []
    for move in pv[:plies]:
        if move not in probe.legal_moves:
            break
        sans.append(probe.san(move))
        probe.push(move)
    return format_line(sans, plies)


def eval_label(cp: int) -> str:
    if abs(cp) >= 99000:
        return "+M" if cp > 0 else "-M"
    return f"{cp / 100:+.2f}"


def move_label(board: chess.Board, san: str) -> str:
    return f"{board.fullmove_number}.{san}" if board.turn == chess.WHITE else f"{board.fullmove_number}...{san}"


def analyze_model_game(
    engine: chess.engine.SimpleEngine,
    record: dict[str, Any],
    depth: int,
) -> dict[str, Any]:
    subject_color = chess.WHITE if record["subject_color"] == "white" else chess.BLACK
    game = game_from_record(record)
    board = game.board()
    moments: list[dict[str, Any]] = []
    losses: list[int] = []
    for move in game.mainline_moves():
        played_san = board.san(move)
        if board.turn == subject_color and board.fullmove_number >= 6:
            try:
                best_info = engine.analyse(board, chess.engine.Limit(depth=depth))
                played_info = engine.analyse(
                    board,
                    chess.engine.Limit(depth=depth),
                    root_moves=[move],
                )
                before = score_cp(best_info, subject_color)
                after = score_cp(played_info, subject_color)
                best_move = best_info.get("pv", [None])[0]
                # Independent depth-limited searches can occasionally assign
                # different scores to the same root move.  A played move that
                # is Stockfish's first choice is never an error.
                loss = 0 if move == best_move else max(0, before - after)
                # Mate scores are represented near 1000 pawns.  Cap them for
                # human-readable loss/ACPL reporting while retaining the mate
                # label in eval_after.
                capped_loss = min(loss, 1000)
                losses.append(capped_loss)
                if loss >= 60:
                    best_san = board.san(best_move) if best_move else ""
                    phase = (
                        "opening" if board.fullmove_number <= 12 else
                        "middlegame" if board.fullmove_number <= 30 else
                        "late game"
                    )
                    moments.append(
                        {
                            "move": move_label(board, played_san),
                            "played": played_san,
                            "best": best_san,
                            "best_line": pv_to_san(board, best_info.get("pv", []), 5),
                            "loss_cp": capped_loss,
                            "severity": "blunder" if loss >= 250 else "serious error" if loss >= 120 else "inaccuracy",
                            "phase": phase,
                            "fen": board.fen(),
                            "eval_before": eval_label(before),
                            "eval_after": eval_label(after),
                        }
                    )
            except (chess.engine.EngineError, chess.engine.EngineTerminatedError, ValueError) as exc:
                print(f"warning: engine skipped {record['date']} {played_san}: {exc}", file=sys.stderr)
        board.push(move)
    moments.sort(key=lambda item: item["loss_cp"], reverse=True)
    return {
        "depth": depth,
        "subject_moves_scanned": len(losses),
        "screening_acpl": round(sum(losses) / len(losses), 1) if losses else None,
        "critical_moments": moments[:3],
    }


def find_pgn_for_profile(profile: dict[str, Any]) -> Path:
    candidates = list((ROOT / "arlan_opponents").glob(f"*{profile['file_token']}*.pgn"))
    if len(candidates) != 1:
        raise FileNotFoundError(f"expected one PGN for {profile['name']}, found {candidates}")
    return candidates[0]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--engine", type=Path)
    parser.add_argument("--depth", type=int, default=12)
    parser.add_argument("--no-engine", action="store_true")
    args = parser.parse_args()

    print("Loading opening reference...", flush=True)
    book = load_opening_book(ROOT / "openings")
    print(f"Opening positions: {len(book):,}", flush=True)

    pack: dict[str, Any] = {
        "generated": "2026-08-01",
        "recent_cutoff": RECENT_YEAR,
        "opening_book_positions": len(book),
        "hero": dict(HERO),
        "opponents": [],
    }

    hero_paths = [ROOT / "chessbasepgn" / "https___players.chessbase.com_games_Cabe_Arlan.pgn"]
    hero_paths.extend(sorted(ROOT.glob("2nd_DAV*.pgn")))
    hero_records = load_subject_games(hero_paths, HERO, book)
    pack["hero"]["sources"] = [str(p.relative_to(ROOT)).replace("\\", "/") for p in hero_paths]
    pack["hero"]["summary"] = summarize_subject(hero_records)
    print(f"Arlan: {len(hero_records)} unique games", flush=True)

    for profile in OPPONENTS:
        pgn_path = find_pgn_for_profile(profile)
        records = load_subject_games([pgn_path], profile, book)
        item = dict(profile)
        item["source"] = str(pgn_path.relative_to(ROOT)).replace("\\", "/")
        item["summary"] = summarize_subject(records)
        pack["opponents"].append(item)
        recent_n = item["summary"]["coverage"]["recent_classical"]["games"]
        print(f"{profile['name']}: {len(records)} games, {recent_n} recent classical", flush=True)

    if not args.no_engine:
        if not args.engine or not args.engine.exists():
            raise FileNotFoundError("Stockfish path is required unless --no-engine is used")
        print(f"Starting Stockfish at depth {args.depth}...", flush=True)
        engine = chess.engine.SimpleEngine.popen_uci(str(args.engine))
        try:
            available = engine.options
            settings: dict[str, Any] = {}
            if "Threads" in available:
                # One thread keeps the depth-limited screen reproducible.
                settings["Threads"] = 1
            if "Hash" in available:
                settings["Hash"] = 128
            if settings:
                engine.configure(settings)
            for item in pack["opponents"]:
                print(f"Engine scan: {item['name']}", flush=True)
                for model in item["summary"]["model_games"]:
                    model["engine"] = analyze_model_game(engine, model, args.depth)
        finally:
            engine.quit()

    # Keep the evidence pack lean: full SAN is needed for diagrams and model
    # positions, but career records are not included outside the selected games.
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(pack, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {args.output}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
