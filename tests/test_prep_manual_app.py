import sqlite3
import tempfile
import threading
import unittest
from http.client import HTTPConnection
from pathlib import Path
from unittest.mock import patch

import prep_manual_app as pm


class PrepManualCoreTests(unittest.TestCase):
    def test_parse_pgn_and_replay_fens(self):
        pgn = """[Event "Unit Test"]
[Site "?"]
[Date "2026.06.13"]
[White "Dino Ballecer"]
[Black "Example Opponent"]
[Result "1-0"]

1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 1-0
"""
        game = pm.parse_pgn_game(pgn)

        self.assertIsNotNone(game)
        self.assertEqual(
            game["moves"],
            ["e4", "e5", "Nf3", "Nc6", "Bb5", "a6"],
        )
        fens, err = pm.fens_for(game["moves"])
        self.assertIsNone(err)
        self.assertEqual(len(fens), len(game["moves"]) + 1)
        self.assertNotEqual(fens[-1], fens[0])

    def test_tag_families_detects_anti_sicilian(self):
        families = pm.tag_families(
            ["e4", "c5", "c3"],
            "B22",
            "Sicilian Defense: Alapin Variation",
        )

        self.assertIn(pm.FAM_ANTISIC, families)

    def test_name_matching_is_conservative_but_handles_full_names(self):
        original_db = pm.DB_PATH
        with tempfile.TemporaryDirectory() as td:
            pm.DB_PATH = Path(td) / "prep_manual.db"
            try:
                pm.init_db()
                conn = pm.db()
                try:
                    self.assertEqual(
                        pm.resolve_name(conn, "Morris, James"),
                        conn.execute(
                            "SELECT player_id FROM Roster WHERE real_name=?",
                            ("IM Morris, James",),
                        ).fetchone()[0],
                    )
                    self.assertIsNone(pm.auto_match(conn, "Morris"))
                finally:
                    conn.close()
            finally:
                pm.DB_PATH = original_db

    def test_init_db_migrates_game_analysis_to_depth_key(self):
        original_db = pm.DB_PATH
        with tempfile.TemporaryDirectory() as td:
            db_path = Path(td) / "prep_manual.db"
            seed = sqlite3.connect(db_path)
            try:
                seed.executescript(
                    """
                    CREATE TABLE GameAnalysis (
                        dedup_hash TEXT PRIMARY KEY,
                        depth INTEGER,
                        engine TEXT,
                        analyzed_at TEXT,
                        acpl_white REAL,
                        acpl_black REAL,
                        moves_white INTEGER,
                        moves_black INTEGER,
                        phase_json TEXT,
                        blunders_json TEXT
                    );
                    INSERT INTO GameAnalysis VALUES (
                        'abc', 12, 'Stockfish', '2026-06-13T00:00:00',
                        10.0, 12.0, 20, 20, '{}', '[]'
                    );
                    """
                )
                seed.commit()
            finally:
                seed.close()

            pm.DB_PATH = db_path
            try:
                pm.init_db()
                conn = pm.db()
                try:
                    pk = [
                        r[1]
                        for r in sorted(
                            (r for r in conn.execute("PRAGMA table_info(GameAnalysis)") if r[5]),
                            key=lambda r: r[5],
                        )
                    ]
                    self.assertEqual(pk, ["dedup_hash", "depth"])
                    self.assertEqual(
                        conn.execute(
                            "SELECT engine FROM GameAnalysis WHERE dedup_hash=? AND depth=?",
                            ("abc", 12),
                        ).fetchone()[0],
                        "Stockfish",
                    )
                finally:
                    conn.close()
            finally:
                pm.DB_PATH = original_db

    def test_moves_uci_for_special_moves(self):
        replay, err = pm.moves_uci_for(["e4", "e5", "Nf3", "Nc6", "Bb5", "a6"])
        self.assertIsNone(err)
        self.assertEqual([r[1] for r in replay], ["e2e4", "e7e5", "g1f3", "b8c6", "f1b5", "a7a6"])

        replay, err = pm.moves_uci_for(["O-O"])
        self.assertIsNone(err)
        self.assertEqual(replay[0][1], "e1g1")

        replay, err = pm.moves_uci_for(["e4", "h5", "e5", "d5", "exd6"])
        self.assertIsNone(err)
        self.assertEqual(replay[-1][1], "e5d6")

        bd = pm.MiniBoard()
        bd.b = ["."] * 64
        bd.b[pm._parse_sq("a7")] = "P"
        bd.b[pm._parse_sq("e1")] = "K"
        bd.b[pm._parse_sq("h8")] = "k"
        bd.castle = set()
        bd.push_san("a8=Q")
        self.assertEqual(bd.last_uci, "a7a8q")

    def test_player_dataset_uses_pgn_source_and_player_ply_parity(self):
        original_db = pm.DB_PATH
        with tempfile.TemporaryDirectory() as td:
            pm.DB_PATH = Path(td) / "prep_manual.db"
            try:
                pm.init_db()
                conn = pm.db()
                try:
                    pid = conn.execute(
                        "SELECT player_id FROM Roster WHERE real_name=?",
                        (pm.HERO_NAME,),
                    ).fetchone()[0]
                    conn.execute("INSERT INTO Files (filename) VALUES ('unit.pgn')")
                    file_id = conn.execute("SELECT file_id FROM Files").fetchone()[0]
                    conn.execute(
                        """INSERT INTO Games
                           (file_id, player_id, color, presult, white, black, result,
                            moves_json, source, dedup_hash)
                           VALUES (?,?,?,?,?,?,?,?,?,?)""",
                        (file_id, pid, "white", "win", "Dino", "Opponent", "1-0",
                         json_dumps(["e4", "c5", "Nf3"]), "pgn", "pgn1"),
                    )
                    conn.execute(
                        """INSERT INTO Games
                           (file_id, player_id, color, presult, white, black, result,
                            moves_json, source, dedup_hash)
                           VALUES (?,?,?,?,?,?,?,?,?,?)""",
                        (file_id, pid, "black", "draw", "Opponent", "Dino", "1/2-1/2",
                         json_dumps(["d4", "Nf6"]), "pgn", "pgn2"),
                    )
                    conn.execute(
                        """INSERT INTO Games
                           (file_id, player_id, color, presult, white, black, result,
                            moves_json, source, dedup_hash)
                           VALUES (?,?,?,?,?,?,?,?,?,?)""",
                        (file_id, pid, "white", "win", "Dino", "Online", "1-0",
                         json_dumps(["c4"]), "lichess", "lichess1"),
                    )
                    conn.commit()

                    with pm._PLAYER_DATASET_LOCK:
                        pm._PLAYER_DATASET_CACHE.clear()
                    ds = pm.build_player_dataset(conn, pid)
                    start = pm.epd_key(pm.MiniBoard().fen())
                    self.assertIn("e2e4", ds["positions"][start]["moves"])
                    self.assertNotIn("c2c4", ds["positions"][start]["moves"])
                    after_d4 = pm.epd_key(pm.moves_uci_for(["d4"])[0][0][2])
                    self.assertIn("g8f6", ds["positions"][after_d4]["moves"])
                    self.assertIn(start, ds["opening"])
                finally:
                    conn.close()
            finally:
                pm.DB_PATH = original_db
                with pm._PLAYER_DATASET_LOCK:
                    pm._PLAYER_DATASET_CACHE.clear()

    def test_scan_clears_player_dataset_cache(self):
        original_db, original_base = pm.DB_PATH, pm.BASE_DIR
        original_lichess_db, original_lichess_csv = pm.LICHESS_DB, pm.LICHESS_CSV
        with tempfile.TemporaryDirectory() as td:
            pm.DB_PATH = Path(td) / "prep_manual.db"
            pm.BASE_DIR = Path(td)
            pm.LICHESS_DB = Path(td) / "missing.db"
            pm.LICHESS_CSV = Path(td) / "missing.csv"
            try:
                pm.init_db()
                conn = pm.db()
                try:
                    with pm._PLAYER_DATASET_LOCK:
                        pm._PLAYER_DATASET_CACHE[1] = {"stale": True}
                    pm.scan(conn)
                    self.assertFalse(pm._PLAYER_DATASET_CACHE)
                finally:
                    conn.close()
            finally:
                pm.DB_PATH = original_db
                pm.BASE_DIR = original_base
                pm.LICHESS_DB = original_lichess_db
                pm.LICHESS_CSV = original_lichess_csv

    def test_select_bot_move_exact_and_blunder_fallback(self):
        fen = pm.MiniBoard().fen()
        key = pm.epd_key(fen)
        dataset = {
            "opening": {key: {"total": 1, "moves": {
                "e2e4": {"count": 1, "score_sum": 1.0, "game_ids": {1}, "min_ply": 1}},
                "games": {1}, "min_ply": 1}},
            "positions": {},
        }

        class FakeEngine:
            def __init__(self, persona_score):
                self.persona_score = persona_score

            def top_moves(self, *_args):
                return [{"uci": "d2d4", "score": 50}, {"uci": "g1f3", "score": 10}]

            def score_move(self, *_args):
                return self.persona_score

        with patch("random.random", return_value=0):
            ok = pm.select_bot_move(None, 1, fen, dataset=dataset, engine=FakeEngine(0))
            self.assertEqual(ok["uci"], "e2e4")
            self.assertEqual(ok["basis"], "opening")

            bad = pm.select_bot_move(None, 1, fen, dataset=dataset, engine=FakeEngine(-500))
            self.assertEqual(bad["uci"], "d2d4")
            self.assertEqual(bad["basis"], "engine")

    def test_play_endpoints(self):
        original_db = pm.DB_PATH
        with tempfile.TemporaryDirectory() as td:
            pm.DB_PATH = Path(td) / "prep_manual.db"
            try:
                pm.init_db()
                conn = pm.db()
                try:
                    pid = conn.execute(
                        "SELECT player_id FROM Roster WHERE real_name=?",
                        (pm.HERO_NAME,),
                    ).fetchone()[0]
                    conn.execute("INSERT INTO Files (filename) VALUES ('unit.pgn')")
                    file_id = conn.execute("SELECT file_id FROM Files").fetchone()[0]
                    conn.execute(
                        """INSERT INTO Games
                           (file_id, player_id, color, presult, white, black, result,
                            moves_json, source, dedup_hash)
                           VALUES (?,?,?,?,?,?,?,?,?,?)""",
                        (file_id, pid, "white", "win", "Dino", "Opponent", "1-0",
                         json_dumps(["e4"]), "pgn", "pgn1"),
                    )
                    conn.commit()
                finally:
                    conn.close()

                class FakeEngine:
                    def top_moves(self, *_args):
                        return [{"uci": "e2e4", "score": 20}]

                    def score_move(self, *_args):
                        return 20

                server = pm.ThreadingHTTPServer(("127.0.0.1", 0), pm.Handler)
                thread = threading.Thread(target=server.serve_forever, daemon=True)
                thread.start()
                try:
                    port = server.server_address[1]
                    http = HTTPConnection("127.0.0.1", port, timeout=5)
                    http.request("GET", "/api/play/players")
                    res = http.getresponse()
                    players = json_loads(res.read())
                    self.assertEqual(res.status, 200)
                    self.assertTrue(players["players"])

                    with patch("prep_manual_app.get_play_engine", return_value=FakeEngine()):
                        http.request(
                            "POST", "/api/play/move",
                            body=json_dumps({
                                "player_id": pid,
                                "fen": pm.MiniBoard().fen(),
                                "bot_color": "white",
                                "elo": 2372,
                            }),
                            headers={"Content-Type": "application/json"},
                        )
                        res = http.getresponse()
                        move = json_loads(res.read())
                    self.assertEqual(res.status, 200)
                    self.assertEqual(move["uci"], "e2e4")
                finally:
                    server.shutdown()
                    server.server_close()
            finally:
                pm.DB_PATH = original_db


def json_dumps(obj):
    import json
    return json.dumps(obj)


def json_loads(data):
    import json
    return json.loads(data.decode("utf-8"))


if __name__ == "__main__":
    unittest.main()
