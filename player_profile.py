#!/usr/bin/env python3
"""
Evidence-based player profile helpers for prep_manual_app.py.

This module is deliberately stdlib-only. It ports the practical weakness
taxonomy from the sibling Endgame Trainer into Python and keeps the logic
independent from the web app so it can grow into a reusable profiler.
"""

from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Any, Callable

PHASE_KEYS = ("op", "mid", "end")
PHASE_LABELS = {"op": "opening", "mid": "middlegame", "end": "endgame"}

SEVERITY_ORDER = {
    "excellent": 0,
    "very_good": 1,
    "good": 2,
    "inaccuracy": 3,
    "mistake": 4,
    "blunder": 5,
}

WEAKNESS_TITLES = {
    "opposition": "Opposition",
    "key_squares": "Key squares",
    "pawn_push_timing": "Pawn push timing",
    "king_activity": "King activity",
    "passed_pawn_race": "Passed pawn race",
    "rook_activity": "Rook activity",
    "lucena": "Lucena",
    "philidor": "Philidor",
    "rook_behind_pawn": "Rook behind pawn",
    "wrong_corner": "Wrong corner",
    "fortress": "Fortress",
    "promotion_missed": "Promotion missed",
    "stalemate_trick": "Stalemate trick",
    "basic_checkmate": "Basic checkmate",
    "conversion_failure": "Conversion failure",
    "drawing_defense_failure": "Drawing defense failure",
}

PIECE_VALUE = {"P": 1, "N": 3, "B": 3, "R": 5, "Q": 9, "K": 0}


@dataclass(frozen=True)
class MaterialSnapshot:
    piece_count: int
    non_king_material: int
    queens_off: bool
    white_pieces: dict[str, str]
    black_pieces: dict[str, str]


def phase_of(ply: int) -> str:
    return "op" if ply < 20 else ("mid" if ply < 40 else "end")


def expected_points(cp: int | float | None) -> float:
    if cp is None:
        return 0.5
    if cp >= 9000:
        return 1.0
    if cp <= -9000:
        return 0.0
    return 1.0 / (1.0 + math.exp(-float(cp) / 300.0))


def practical_outcome(cp: int | float | None) -> str:
    ep = expected_points(cp)
    if ep >= 0.67:
        return "win"
    if ep <= 0.33:
        return "loss"
    return "draw"


def expected_points_drop(before_cp: int | float | None,
                         after_cp: int | float | None) -> float:
    return max(0.0, expected_points(before_cp) - expected_points(after_cp))


def severity_from_drop(drop: float) -> str:
    if drop >= 0.18:
        return "blunder"
    if drop >= 0.08:
        return "mistake"
    if drop >= 0.03:
        return "inaccuracy"
    if drop >= 0.01:
        return "good"
    return "very_good"


def severity_rank(severity: str) -> int:
    return SEVERITY_ORDER.get((severity or "").lower(), 0)


def board_map(fen: str) -> dict[str, str]:
    board = (fen or "").strip().split()[0] if (fen or "").strip() else ""
    pieces: dict[str, str] = {}
    rank, file_idx = 8, 0
    for ch in board:
        if ch == "/":
            rank -= 1
            file_idx = 0
            continue
        if ch.isdigit():
            file_idx += int(ch)
            continue
        if 0 <= file_idx <= 7 and 1 <= rank <= 8:
            pieces[f"{chr(97 + file_idx)}{rank}"] = ch
        file_idx += 1
    return pieces


def material_snapshot(fen: str) -> MaterialSnapshot:
    white: dict[str, str] = {}
    black: dict[str, str] = {}
    piece_count = 0
    non_king_material = 0
    queens_off = True
    for square, piece in board_map(fen).items():
        upper = piece.upper()
        piece_count += 1
        if upper == "Q":
            queens_off = False
        if upper != "K":
            non_king_material += PIECE_VALUE.get(upper, 0)
        if piece.isupper():
            white[square] = upper
        else:
            black[square] = upper
    return MaterialSnapshot(
        piece_count=piece_count,
        non_king_material=non_king_material,
        queens_off=queens_off,
        white_pieces=white,
        black_pieces=black,
    )


def is_strict_endgame(fen: str) -> bool:
    snap = material_snapshot(fen)
    return len(snap.white_pieces) <= 4 and len(snap.black_pieces) <= 4


def fullmove_number(fen: str) -> int:
    parts = (fen or "").strip().split()
    if len(parts) < 6:
        return 1
    try:
        return int(parts[5])
    except ValueError:
        return 1


def is_middlegame_review_candidate(fen: str) -> bool:
    snap = material_snapshot(fen)
    if is_strict_endgame(fen):
        return False
    if fullmove_number(fen) < 30:
        return False
    return snap.piece_count <= 14 or snap.queens_off or snap.non_king_material <= 14


def infer_move_uci(fen_before: str, fen_after: str) -> str | None:
    before = board_map(fen_before)
    after = board_map(fen_after)
    side = "w"
    parts = (fen_before or "").strip().split()
    if len(parts) >= 2:
        side = parts[1].lower()
    own_is_upper = side != "b"

    removed = [(sq, pc) for sq, pc in before.items() if after.get(sq) != pc]
    added = [(sq, pc) for sq, pc in after.items() if before.get(sq) != pc]

    own_removed = [(sq, pc) for sq, pc in removed if pc.isupper() == own_is_upper]
    own_added = [(sq, pc) for sq, pc in added if pc.isupper() == own_is_upper]
    if not own_removed or not own_added:
        return None

    # Castling changes king and rook; the king move is the SAN move.
    king_removed = [(sq, pc) for sq, pc in own_removed if pc.upper() == "K"]
    king_added = [(sq, pc) for sq, pc in own_added if pc.upper() == "K"]
    if king_removed and king_added:
        return king_removed[0][0] + king_added[0][0]

    src, src_piece = own_removed[0]
    dst, dst_piece = own_added[0]
    promo = ""
    if src_piece.upper() == "P" and dst_piece.upper() != "P":
        promo = dst_piece.lower()
    return src + dst + promo


def classify_weakness(
    *,
    fen_before: str,
    fen_after: str = "",
    move_uci: str | None = None,
    best_move_uci: str | None = None,
    side: str,
    before_cp: int | float | None,
    after_cp: int | float | None,
    severity: str | None = None,
) -> tuple[list[str], list[str]]:
    drop = expected_points_drop(before_cp, after_cp)
    sev = severity or severity_from_drop(drop)
    before_outcome = practical_outcome(before_cp)
    after_outcome = practical_outcome(after_cp)
    if before_outcome == "win" and after_outcome != "win":
        practical_worsened = True
    elif before_outcome == "draw" and after_outcome == "loss":
        practical_worsened = True
    else:
        practical_worsened = False
    if not practical_worsened and drop < 0.08 and severity_rank(sev) < SEVERITY_ORDER["mistake"]:
        return [], []

    cats: list[str] = []
    reasons: list[str] = []

    def add(cat: str, reason: str):
        if cat in cats:
            return
        cats.append(cat)
        reasons.append(reason)

    before = material_snapshot(fen_before)
    after = material_snapshot(fen_after or fen_before)
    own_before = before.white_pieces if side == "white" else before.black_pieces
    enemy_before = before.black_pieces if side == "white" else before.white_pieces
    own_after = after.white_pieces if side == "white" else after.black_pieces
    moved_piece = _moved_piece(fen_before, move_uci, side)

    if best_move_uci and len(best_move_uci) == 5 and best_move_uci != (move_uci or ""):
        add("promotion_missed", "The engine preferred a direct promotion move.")

    if _only_kings_and_pawns(before):
        if moved_piece == "P":
            add("pawn_push_timing",
                "This was a king-and-pawn endgame and the mistake was a pawn push.")
        if moved_piece == "K" and _kings_in_opposition(before):
            add("opposition", "The kings were in an opposition-sensitive setup.")
        if moved_piece == "K":
            add("key_squares", "A king move changed access to key pawn squares.")
        if _king_became_less_active(own_before, own_after):
            add("king_activity", "The king moved farther from the center.")
        if _has_passed_pawn(before, "white") and _has_passed_pawn(before, "black"):
            add("passed_pawn_race", "Both sides had passed pawns, so geometry mattered.")

    if _has_piece(before, "R") and not _has_piece(before, "Q"):
        if _lucena_like(own_before, enemy_before, side):
            add("lucena", "The rook-and-pawn structure resembles a Lucena conversion.")
        if _philidor_like(own_before, enemy_before, side):
            add("philidor", "The rook-and-pawn structure resembles a Philidor defense.")
        if moved_piece == "R" and _rook_is_passive(own_after, side):
            add("rook_activity", "The rook became passive after the move.")
        if _has_passed_pawn(before, side) and not _rook_behind_any_passed_pawn(own_after, side):
            add("rook_behind_pawn", "A passed pawn was present but the rook was not behind it.")

    if _wrong_corner_pattern(before, side):
        add("wrong_corner", "The material matches a rook-pawn wrong-corner pattern.")

    if _fortress_like(before) and before_outcome == "draw" and after_outcome == "loss":
        add("fortress", "The position had low-material fortress characteristics.")

    if before_outcome == "win" and after_outcome != "win":
        add("conversion_failure", "The move turned a winning position into a non-winning one.")
    elif before_outcome == "draw" and after_outcome == "loss":
        add("drawing_defense_failure", "The move turned a drawable position into a losing one.")

    if not cats and practical_worsened:
        if before_outcome == "win":
            add("conversion_failure", "A winning position was not converted.")
        else:
            add("drawing_defense_failure", "A defensive resource was missed.")

    return cats, reasons


def build_player_profile(
    conn,
    player_id: int,
    *,
    depth: int = 16,
    allow_engine: bool = False,
    analyze_game: Callable[..., dict | None] | None = None,
) -> dict:
    games = [dict(r) for r in conn.execute(
        """SELECT g.*, group_concat(t.family,'|') AS fams
           FROM Games g LEFT JOIN Tags t ON t.game_id=g.game_id
           WHERE g.player_id=? GROUP BY g.game_id
           ORDER BY g.date DESC, g.game_id DESC""",
        (player_id,),
    )]
    for g in games:
        g["families"] = (g.get("fams") or "").split("|") if g.get("fams") else []

    profile = {
        "opening_profile": _opening_profile(games),
        "phase_profile": {
            "available": True,
            "analyzed": 0,
            "pending": 0,
            "total": sum(1 for g in games if g.get("source") != "lichess"),
            "depth": depth,
            "acpl": None,
            "phase_acpl": {},
            "mistake_counts": {"blunder": 0, "mistake": 0, "inaccuracy": 0},
        },
        "weakness_categories": [],
        "tendencies": [],
        "samples": [],
    }

    phase_sum = {k: [0.0, 0] for k in PHASE_KEYS}
    total_sum = [0.0, 0]
    category_samples: dict[str, list[dict]] = defaultdict(list)
    category_reasons: dict[str, Counter] = defaultdict(Counter)
    depths: set[int] = set()

    for g in games:
        if g.get("source") == "lichess":
            continue
        moves_json = g.get("moves_json") or "[]"
        try:
            moves = json.loads(moves_json)
        except json.JSONDecodeError:
            moves = []
        roll = None
        if analyze_game is not None:
            roll = analyze_game(
                conn, g.get("dedup_hash"), moves, depth, allow_engine=allow_engine
            )
        else:
            roll = _cached_rollup(conn, g.get("dedup_hash"), depth)
        if roll is None:
            profile["phase_profile"]["pending"] += 1
            continue
        profile["phase_profile"]["analyzed"] += 1
        if roll.get("depth"):
            depths.add(int(roll["depth"]))
        color = g.get("color") or "white"
        phases = (roll.get("phases") or {}).get(color, {})
        for key in PHASE_KEYS:
            s, c = phases.get(key, [0, 0])
            phase_sum[key][0] += float(s or 0)
            phase_sum[key][1] += int(c or 0)
            total_sum[0] += float(s or 0)
            total_sum[1] += int(c or 0)

        for move in roll.get("moves", []):
            if move.get("mover") != color:
                continue
            sev = move.get("sev") or "inaccuracy"
            profile["phase_profile"]["mistake_counts"][sev] = (
                profile["phase_profile"]["mistake_counts"].get(sev, 0) + 1
            )
            sample = _sample_from_move(g, move)
            fen_before = sample.get("fen_before") or ""
            fen_after = sample.get("fen_after") or ""
            if fen_before and not (is_strict_endgame(fen_before) or
                                   is_middlegame_review_candidate(fen_before)):
                # Keep tactical samples out of endgame/late-simplified reports.
                continue
            cats, reasons = classify_weakness(
                fen_before=fen_before,
                fen_after=fen_after,
                move_uci=sample.get("move_uci"),
                best_move_uci=sample.get("best_move_uci"),
                side=color,
                before_cp=sample.get("before_cp"),
                after_cp=sample.get("after_cp"),
                severity=sev,
            ) if fen_before else _outcome_only_categories(sample)
            if not cats:
                continue
            sample["categories"] = cats
            sample["reasons"] = reasons
            sample["phase"] = phase_of(int(sample.get("ply") or 0))
            profile["samples"].append(sample)
            for cat in cats:
                category_samples[cat].append(sample)
            for reason in reasons:
                for cat in cats:
                    category_reasons[cat][reason] += 1

    profile["phase_profile"]["phase_acpl"] = {
        k: _mean(phase_sum[k]) for k in PHASE_KEYS
    }
    profile["phase_profile"]["acpl"] = _mean(total_sum)
    if depths:
        profile["phase_profile"]["depth"] = max(depths)
    profile["samples"].sort(
        key=lambda s: (s.get("impact", 0), s.get("loss_cp", 0)),
        reverse=True,
    )
    profile["samples"] = profile["samples"][:10]
    profile["weakness_categories"] = _summarize_categories(
        category_samples, category_reasons
    )
    profile["tendencies"] = _tendencies(profile, games)
    return profile


def _cached_rollup(conn, dedup_hash: str | None, depth: int) -> dict | None:
    if not dedup_hash:
        return None
    row = conn.execute(
        "SELECT * FROM GameAnalysis WHERE dedup_hash=? AND depth=?",
        (dedup_hash, depth),
    ).fetchone()
    if row is None:
        row = conn.execute(
            "SELECT * FROM GameAnalysis WHERE dedup_hash=? ORDER BY depth DESC LIMIT 1",
            (dedup_hash,),
        ).fetchone()
    if row is None:
        return None
    return {
        "depth": row["depth"],
        "engine": row["engine"],
        "acpl_white": row["acpl_white"],
        "acpl_black": row["acpl_black"],
        "moves_white": row["moves_white"],
        "moves_black": row["moves_black"],
        "phases": json.loads(row["phase_json"] or "{}"),
        "moves": json.loads(row["blunders_json"] or "[]"),
    }


def _opening_profile(games: list[dict]) -> dict:
    all_rows = _opening_rows(games)
    white_rows = _opening_rows([g for g in games if g.get("color") == "white"])
    black_rows = _opening_rows([g for g in games if g.get("color") == "black"])
    strong = [r for r in all_rows if r["n"] >= 3 and r["reliable_score"] >= 55]
    weak = [r for r in all_rows if r["n"] >= 2 and r["reliable_score"] < 45]
    strong.sort(key=lambda r: (-r["reliable_score"], -r["score"], -r["n"], r["opening"]))
    weak.sort(key=lambda r: (r["reliable_score"], r["score"], -r["n"], r["opening"]))
    return {
        "distinct_openings": len(all_rows),
        "strongest_lines": strong[:5],
        "weak_lines": weak[:5],
        "color_split": {
            "white": _record([g for g in games if g.get("color") == "white"]),
            "black": _record([g for g in games if g.get("color") == "black"]),
        },
        "white": white_rows[:8],
        "black": black_rows[:8],
    }


def _opening_rows(games: list[dict]) -> list[dict]:
    by_opening: dict[str, list[dict]] = defaultdict(list)
    for g in games:
        by_opening[g.get("opening") or "(unclassified)"].append(g)
    rows = []
    for opening, group in by_opening.items():
        rec = _record(group)
        rows.append({
            **rec,
            "opening": opening,
            "eco": group[0].get("eco") or "",
        })
    rows.sort(key=lambda r: (-r["n"], r["opening"]))
    return rows


def _record(games: list[dict]) -> dict:
    w = sum(1 for g in games if g.get("presult") == "win")
    d = sum(1 for g in games if g.get("presult") == "draw")
    l = sum(1 for g in games if g.get("presult") == "loss")
    n = len(games)
    result_n = w + d + l
    score = round(100.0 * (w + 0.5 * d) / result_n, 1) if result_n else 0.0
    return {
        "n": n, "w": w, "d": d, "l": l, "score": score,
        "reliable_score": _reliable_score_pct(w, d, l),
        "confidence": _confidence(result_n),
    }


def _reliable_score_pct(w: int, d: int, l: int) -> float:
    n = w + d + l
    if not n:
        return 0.0
    p = (w + 0.5 * d) / n
    z = 1.0
    denom = 1 + z * z / n
    center = p + z * z / (2 * n)
    spread = z * math.sqrt((p * (1 - p) + z * z / (4 * n)) / n)
    return round(100.0 * max(0.0, (center - spread) / denom), 1)


def _sample_from_move(game: dict, move: dict) -> dict:
    return {
        "game_id": game.get("game_id"),
        "date": game.get("date") or "",
        "event": game.get("event") or "",
        "opponent": game.get("black") if game.get("color") == "white" else game.get("white"),
        "opening": game.get("opening") or "",
        "eco": game.get("eco") or "",
        "color": game.get("color") or "",
        "ply": move.get("ply"),
        "move_no": move.get("move_no"),
        "san": move.get("san") or "",
        "severity": move.get("sev") or "inaccuracy",
        "loss_cp": move.get("loss") or 0,
        "impact": move.get("impact") or expected_points_drop(move.get("before"), move.get("after")),
        "impact_pct": move.get("impact_pct") or round(
            100.0 * expected_points_drop(move.get("before"), move.get("after")), 1
        ),
        "before_cp": move.get("before"),
        "after_cp": move.get("after"),
        "best": move.get("best") or "",
        "best_move_uci": move.get("best_uci") or "",
        "move_uci": move.get("move_uci") or "",
        "fen_before": move.get("fen_before") or "",
        "fen_after": move.get("fen_after") or "",
    }


def _outcome_only_categories(sample: dict) -> tuple[list[str], list[str]]:
    before = practical_outcome(sample.get("before_cp"))
    after = practical_outcome(sample.get("after_cp"))
    if before == "win" and after != "win":
        return ["conversion_failure"], ["The engine score changed from winning to non-winning."]
    if before == "draw" and after == "loss":
        return ["drawing_defense_failure"], ["The engine score changed from drawable to losing."]
    return [], []


def _summarize_categories(
    samples_by_category: dict[str, list[dict]],
    reasons_by_category: dict[str, Counter],
) -> list[dict]:
    rows = []
    for cat, samples in samples_by_category.items():
        rows.append({
            "id": cat,
            "title": WEAKNESS_TITLES.get(cat, cat.replace("_", " ").title()),
            "count": len(samples),
            "sample_moves": sorted(
                samples,
                key=lambda s: (s.get("impact", 0), s.get("loss_cp", 0)),
                reverse=True,
            )[:3],
            "reasons": [r for r, _ in reasons_by_category[cat].most_common(3)],
        })
    rows.sort(key=lambda r: (-r["count"], r["title"]))
    return rows


def _tendencies(profile: dict, games: list[dict]) -> list[dict]:
    tendencies = []
    opening = profile["opening_profile"]
    total_games = len(games)
    distinct = opening["distinct_openings"]
    if total_games:
        breadth = "Broad" if distinct >= 12 else ("Focused" if distinct <= 5 else "Moderate")
        tendencies.append({
            "label": "Opening breadth",
            "evidence": f"{breadth}: {distinct} distinct openings across {total_games} games.",
            "confidence": _confidence(total_games),
        })

    phase = profile["phase_profile"]
    analyzed = phase.get("analyzed", 0)
    counts = phase.get("mistake_counts", {})
    serious = counts.get("blunder", 0) + counts.get("mistake", 0)
    if analyzed:
        rate = serious / analyzed
        risk = "High tactical volatility" if rate >= 1.0 else (
            "Moderate tactical volatility" if rate >= 0.35 else "Stable tactical profile")
        tendencies.append({
            "label": "Risk tendency",
            "evidence": f"{risk}: {serious} blunders/mistakes in {analyzed} analysed games.",
            "confidence": _confidence(analyzed),
        })
        phase_acpl = phase.get("phase_acpl") or {}
        usable = {k: v for k, v in phase_acpl.items() if v is not None}
        if usable:
            worst_key = max(usable, key=lambda k: usable[k])
            best_key = min(usable, key=lambda k: usable[k])
            tendencies.append({
                "label": "Phase stability",
                "evidence": (
                    f"Least accurate phase: {PHASE_LABELS[worst_key]} ACPL {usable[worst_key]}; "
                    f"best phase: {PHASE_LABELS[best_key]} ACPL {usable[best_key]}."
                ),
                "confidence": _confidence(analyzed),
            })

    cats = {c["id"]: c["count"] for c in profile.get("weakness_categories", [])}
    conversion = cats.get("conversion_failure", 0)
    drawing = cats.get("drawing_defense_failure", 0)
    endgame_samples = sum(cats.values())
    if endgame_samples or analyzed:
        tendencies.append({
            "label": "Conversion reliability",
            "evidence": (
                f"{conversion} conversion-failure sample(s) among "
                f"{endgame_samples} classified endgame/late-simplified samples."
            ),
            "confidence": _confidence(endgame_samples),
        })
        tendencies.append({
            "label": "Drawing-defense reliability",
            "evidence": (
                f"{drawing} drawing-defense failure sample(s) among "
                f"{endgame_samples} classified endgame/late-simplified samples."
            ),
            "confidence": _confidence(endgame_samples),
        })

    strong = opening.get("strongest_lines") or []
    if strong:
        labels = ", ".join(
            f"{r['opening']} ({r['score']}%, reliable {r['reliable_score']}%/{r['n']}g)"
            for r in strong[:3])
        tendencies.append({
            "label": "Confidence lines",
            "evidence": labels,
            "confidence": _confidence(sum(r["n"] for r in strong[:3])),
        })
    return tendencies


def _confidence(n: int) -> str:
    if n >= 20:
        return "high"
    if n >= 6:
        return "medium"
    return "low"


def _mean(sum_cnt: list[Any]) -> float | None:
    return round(float(sum_cnt[0]) / int(sum_cnt[1]), 1) if int(sum_cnt[1]) else None


def _moved_piece(fen: str, uci: str | None, side: str) -> str | None:
    if not uci or len(uci) < 4:
        return None
    square = uci[:2]
    snap = material_snapshot(fen)
    own = snap.white_pieces if side == "white" else snap.black_pieces
    return own.get(square)


def _all_pieces(snapshot: MaterialSnapshot) -> list[str]:
    return list(snapshot.white_pieces.values()) + list(snapshot.black_pieces.values())


def _only_kings_and_pawns(snapshot: MaterialSnapshot) -> bool:
    return all(p in ("K", "P") for p in _all_pieces(snapshot))


def _has_piece(snapshot: MaterialSnapshot, piece: str) -> bool:
    return piece in _all_pieces(snapshot)


def _square_of(pieces: dict[str, str], piece: str) -> str | None:
    for sq, pc in pieces.items():
        if pc == piece:
            return sq
    return None


def _file(square: str) -> int:
    return ord(square[0]) - 97


def _rank(square: str) -> int:
    return int(square[1])


def _kings_in_opposition(snapshot: MaterialSnapshot) -> bool:
    wk = _square_of(snapshot.white_pieces, "K")
    bk = _square_of(snapshot.black_pieces, "K")
    if not wk or not bk:
        return False
    if _file(wk) == _file(bk):
        return abs(_rank(wk) - _rank(bk)) % 2 == 1
    if _rank(wk) == _rank(bk):
        return abs(_file(wk) - _file(bk)) % 2 == 1
    return False


def _center_distance(square: str) -> float:
    f = _file(square)
    r = _rank(square) - 1
    return float(min(abs(f - 3), abs(f - 4)) + min(abs(r - 3), abs(r - 4)))


def _king_became_less_active(before: dict[str, str], after: dict[str, str]) -> bool:
    kb = _square_of(before, "K")
    ka = _square_of(after, "K")
    if not kb or not ka:
        return False
    return _center_distance(ka) > _center_distance(kb)


def _has_passed_pawn(snapshot: MaterialSnapshot, side: str) -> bool:
    own = snapshot.white_pieces if side == "white" else snapshot.black_pieces
    enemy = snapshot.black_pieces if side == "white" else snapshot.white_pieces
    for sq, pc in own.items():
        if pc != "P":
            continue
        if _is_passed_pawn(sq, enemy, side):
            return True
    return False


def _is_passed_pawn(square: str, enemy: dict[str, str], side: str) -> bool:
    f, r = _file(square), _rank(square)
    for enemy_sq, pc in enemy.items():
        if pc != "P":
            continue
        ef, er = _file(enemy_sq), _rank(enemy_sq)
        if abs(ef - f) > 1:
            continue
        if side == "white" and er > r:
            return False
        if side == "black" and er < r:
            return False
    return True


def _lucena_like(own: dict[str, str], enemy: dict[str, str], side: str) -> bool:
    if list(own.values()).count("R") != 1 or list(enemy.values()).count("R") != 1:
        return False
    for sq, pc in own.items():
        if pc != "P":
            continue
        if side == "white" and _rank(sq) == 7:
            return True
        if side == "black" and _rank(sq) == 2:
            return True
    return False


def _philidor_like(own: dict[str, str], enemy: dict[str, str], side: str) -> bool:
    if list(own.values()).count("R") != 1 or list(enemy.values()).count("R") != 1:
        return False
    for sq, pc in enemy.items():
        if pc != "P":
            continue
        r = _rank(sq)
        if side == "white" and 4 <= r <= 6:
            return True
        if side == "black" and 3 <= r <= 5:
            return True
    return False


def _rook_is_passive(own_after: dict[str, str], side: str) -> bool:
    for sq, pc in own_after.items():
        if pc != "R":
            continue
        if side == "white" and _rank(sq) <= 2:
            return True
        if side == "black" and _rank(sq) >= 7:
            return True
    return False


def _rook_behind_any_passed_pawn(own_after: dict[str, str], side: str) -> bool:
    rooks = [sq for sq, pc in own_after.items() if pc == "R"]
    pawns = [sq for sq, pc in own_after.items() if pc == "P"]
    for rook in rooks:
        for pawn in pawns:
            if _file(rook) != _file(pawn):
                continue
            if side == "white" and _rank(rook) < _rank(pawn):
                return True
            if side == "black" and _rank(rook) > _rank(pawn):
                return True
    return False


def _wrong_corner_pattern(snapshot: MaterialSnapshot, side: str) -> bool:
    own = snapshot.white_pieces if side == "white" else snapshot.black_pieces
    enemy = snapshot.black_pieces if side == "white" else snapshot.white_pieces
    bishops = [sq for sq, pc in own.items() if pc == "B"]
    pawns = [sq for sq, pc in own.items() if pc == "P"]
    if len(bishops) != 1 or len(pawns) != 1:
        return False
    if any(pc != "K" for pc in enemy.values()):
        return False
    pawn = pawns[0]
    if pawn[0] not in ("a", "h"):
        return False
    corner = pawn[0] + ("8" if side == "white" else "1")
    return _square_color(corner) != _square_color(bishops[0])


def _square_color(square: str) -> bool:
    return (_file(square) + _rank(square)) % 2 == 0


def _fortress_like(snapshot: MaterialSnapshot) -> bool:
    non_kings = [p for p in _all_pieces(snapshot) if p != "K"]
    return len(non_kings) <= 4 and "Q" not in non_kings and snapshot.non_king_material <= 6
