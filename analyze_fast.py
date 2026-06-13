#!/usr/bin/env python3
"""Parallel deep-analysis pass for prep_manual_app.

The app's own analysis (`--analyze`) runs every Stockfish search through ONE
shared engine behind a single lock, so it can't use more than one core. This
runner fans the same work out across N worker processes and writes the results
into the SAME `GameAnalysis` cache the app reads — so once it finishes, the
dossiers / self-audit / Markdown export pick the numbers up with no other change.

Why scratch DBs?
----------------
`analyze_game` writes `PositionEval` rows incrementally and only commits once,
at the end of a game, so a single game holds a write transaction for its whole
(~30s at depth 16) analysis. Pointing several workers at one SQLite file just
serialises them (and trips `database is locked` past the busy-timeout). So each
worker analyses against its OWN throwaway SQLite file (zero contention, real
parallelism); the parent then MERGES every `GameAnalysis` row into the real
`prep_manual.db` from a single connection. `PositionEval` is only a recompute
cache and is not needed downstream, so it is left in the scratch files.

It reuses `prep_manual_app.analyze_game` verbatim — no chess/eval logic is
duplicated here. Pure stdlib.

Usage
-----
  python analyze_fast.py                          # all OTB games, depth 16
  python analyze_fast.py --scope losses           # only Dino's losses
  python analyze_fast.py --scope player --player 3
  python analyze_fast.py --depth 18 --workers 3 --max-games 50
  python analyze_fast.py --force                  # re-analyse even if cached

Resumable: games already in `GameAnalysis` at the requested depth are skipped
unless --force, so stopping and re-running never repeats work.
"""
from __future__ import annotations
import argparse
import atexit
import json
import multiprocessing as mp
import os
import sys
import tempfile
import time
from pathlib import Path

import prep_manual_app as pm

_GA_COLS = ("dedup_hash", "depth", "engine", "analyzed_at", "acpl_white",
            "acpl_black", "moves_white", "moves_black", "phase_json",
            "blunders_json")


# --------------------------------------------------------------------------- #
# Game selection (mirrors analyze_all's scope logic; adds a resume filter)
# --------------------------------------------------------------------------- #
def select_games(scope: str, pid: int | None, max_games: int | None,
                 depth: int, force: bool) -> list[tuple[str, str]]:
    conn = pm.db()
    try:
        hero = conn.execute("SELECT player_id FROM Roster WHERE is_hero=1").fetchone()
        hero_id = hero["player_id"] if hero else None
        rows = conn.execute(
            "SELECT dedup_hash, moves_json, presult, player_id FROM Games "
            "WHERE source!='lichess'").fetchall()
        done = set()
        if not force:
            done = {r[0] for r in conn.execute(
                "SELECT dedup_hash FROM GameAnalysis WHERE depth=?", (depth,))}
    finally:
        conn.close()

    games: list[tuple[str, str]] = []
    seen: set[str] = set()
    for r in rows:
        if scope == "losses" and not (r["player_id"] == hero_id and r["presult"] == "loss"):
            continue
        if scope == "player" and pid is not None and r["player_id"] != pid:
            continue
        h = r["dedup_hash"]
        if h in seen or h in done:
            continue
        seen.add(h)
        games.append((h, r["moves_json"]))
    if max_games:
        games = games[:max_games]
    return games


# --------------------------------------------------------------------------- #
# Worker: own Stockfish + own throwaway SQLite file, reused across its tasks
# --------------------------------------------------------------------------- #
_W: dict = {}


def _cleanup_scratch(path: Path) -> None:
    for p in (path, Path(str(path) + "-wal"), Path(str(path) + "-shm")):
        try:
            p.unlink()
        except OSError:
            pass


def _sweep_scratch() -> None:
    """Remove any leftover worker scratch files. Pool workers are terminated (not
    exited) when the pool closes, so their atexit cleanup may not fire — the
    parent sweeps as a backstop."""
    import glob
    for f in glob.glob(str(Path(tempfile.gettempdir()) / "prep_scratch_*.db*")):
        try:
            os.unlink(f)
        except OSError:
            pass


def _winit(depth: int, threads: int, hash_mb: int, force: bool) -> None:
    pm.ENGINE_THREADS = threads          # tune BEFORE the engine is lazily started
    pm.ENGINE_HASH_MB = hash_mb

    scratch = Path(tempfile.gettempdir()) / f"prep_scratch_{os.getpid()}.db"
    _cleanup_scratch(scratch)            # start clean if a stale file lingers
    pm.DB_PATH = scratch                 # redirect pm.db() to this worker's file
    conn = pm.db()
    conn.executescript(pm.SCHEMA)        # create the cache tables (empty)
    atexit.register(_cleanup_scratch, scratch)

    eng = pm.get_engine()                # this process's own Stockfish (or None)
    _W.update(conn=conn, depth=depth, force=force, ok=eng is not None)


def _work(task: tuple[str, str]) -> tuple[str, tuple | None, str | None]:
    dedup_hash, moves_json = task
    if not _W.get("ok"):
        return (dedup_hash, None, "no-engine")
    try:
        conn, depth = _W["conn"], _W["depth"]
        roll = pm.analyze_game(conn, dedup_hash, json.loads(moves_json),
                               depth, allow_engine=True, force=_W["force"])
        if roll is None:
            return (dedup_hash, None, "not-analysed")
        row = conn.execute(
            f"SELECT {','.join(_GA_COLS)} FROM GameAnalysis "
            "WHERE dedup_hash=? AND depth=?", (dedup_hash, depth)).fetchone()
        return (dedup_hash, tuple(row), None)
    except Exception as e:               # one bad game shouldn't kill the pass
        return (dedup_hash, None, repr(e))


# --------------------------------------------------------------------------- #
# Driver
# --------------------------------------------------------------------------- #
def main() -> int:
    ap = argparse.ArgumentParser(description="Parallel Stockfish analysis pass.")
    ap.add_argument("--scope", choices=["all", "losses", "player"], default="all")
    ap.add_argument("--player", type=int, default=None, help="player_id for --scope player")
    ap.add_argument("--depth", type=int, default=pm.ENGINE_DEPTH)
    ap.add_argument("--workers", type=int, default=max(2, (os.cpu_count() or 2) - 1))
    ap.add_argument("--threads", type=int, default=1, help="UCI threads per worker engine")
    ap.add_argument("--hash", type=int, default=128, help="UCI hash (MB) per worker engine")
    ap.add_argument("--max-games", type=int, default=None)
    ap.add_argument("--force", action="store_true", help="re-analyse even if cached")
    args = ap.parse_args()

    if not pm.find_stockfish():
        print("No Stockfish binary found (set PREP_STOCKFISH or place one). Aborting.")
        return 2

    pm.init_db()  # ensure the real DB's cache tables exist
    games = select_games(args.scope, args.player, args.max_games, args.depth, args.force)
    total = len(games)
    if total == 0:
        print(f"Nothing to do: every game in scope={args.scope} is already analysed "
              f"at depth {args.depth} (use --force to redo).")
        return 0

    workers = max(1, min(args.workers, total))
    print(f"Stockfish: {pm.find_stockfish()}")
    print(f"Analysing {total} game(s) | scope={args.scope} depth={args.depth} "
          f"| {workers} workers x {args.threads} thread(s) x {args.hash}MB"
          f"{' | FORCE' if args.force else ''}", flush=True)

    # Single-writer connection into the REAL db for merging results.
    main_conn = pm.db()
    insert_sql = (f"INSERT OR REPLACE INTO GameAnalysis ({','.join(_GA_COLS)}) "
                  f"VALUES ({','.join('?' * len(_GA_COLS))})")

    t0 = time.time()
    done = ok = failed = 0
    ctx = mp.get_context("spawn")  # Windows-safe
    with ctx.Pool(workers, initializer=_winit,
                  initargs=(args.depth, args.threads, args.hash, args.force)) as pool:
        for dedup_hash, row, err in pool.imap_unordered(_work, games, chunksize=1):
            done += 1
            if row is not None:
                main_conn.execute(insert_sql, row)
                ok += 1
                if ok % 25 == 0:
                    main_conn.commit()
            else:
                failed += 1
                if err and err not in ("no-engine", "not-analysed"):
                    print(f"  ! {dedup_hash[:12]}: {err}", flush=True)
            if done % 10 == 0 or done == total:
                rate = done / max(1e-6, time.time() - t0)
                eta = (total - done) / max(1e-6, rate)
                print(f"  {done}/{total}  ok={ok} fail={failed}  "
                      f"{rate:.2f} games/s  ETA {eta:5.0f}s", flush=True)
    main_conn.commit()
    main_conn.close()
    _sweep_scratch()

    dt = time.time() - t0
    print(f"Done: {ok} merged, {failed} failed, {total} total in {dt:.0f}s "
          f"({total / max(1e-6, dt):.2f} games/s).")
    return 0


if __name__ == "__main__":
    mp.freeze_support()
    sys.exit(main())
