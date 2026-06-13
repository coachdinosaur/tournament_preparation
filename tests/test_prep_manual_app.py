import sqlite3
import tempfile
import unittest
from pathlib import Path

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


if __name__ == "__main__":
    unittest.main()
