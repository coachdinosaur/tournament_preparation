import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

import player_profile as pp
import prep_manual_app as pm


class PlayerProfileHeuristicTests(unittest.TestCase):
    def test_endgame_detector_accepts_four_pieces_per_side_only(self):
        self.assertTrue(pp.is_strict_endgame(
            "3rk3/4pp2/8/8/8/4P3/4KP2/3R4 w - - 0 1"
        ))
        self.assertFalse(pp.is_strict_endgame(
            "rnb1kbnr/pppppppp/8/8/8/8/PPPPPPPP/RNB1KBNR w KQkq - 0 1"
        ))

    def test_middlegame_review_candidate_requires_late_simplification(self):
        fen = "rnb1kbnr/pppppppp/8/8/8/8/PPPPPPPP/RNB1KBNR w KQkq - 0 {}"
        self.assertFalse(pp.is_middlegame_review_candidate(fen.format(29)))
        self.assertTrue(pp.is_middlegame_review_candidate(fen.format(30)))

    def test_expected_points_drop_maps_to_severity(self):
        self.assertEqual(pp.severity_from_drop(pp.expected_points_drop(50, 0)), "inaccuracy")
        self.assertEqual(pp.severity_from_drop(pp.expected_points_drop(100, 0)), "mistake")
        self.assertEqual(pp.severity_from_drop(pp.expected_points_drop(300, -300)), "blunder")

    def test_classifier_identifies_key_squares_and_conversion_failure(self):
        cats, reasons = pp.classify_weakness(
            fen_before="8/8/8/8/8/4k3/4P3/4K3 w - - 0 1",
            fen_after="8/8/8/8/8/4k3/4P3/5K2 b - - 1 1",
            move_uci="e1f1",
            best_move_uci="e1d1",
            side="white",
            before_cp=300,
            after_cp=0,
            severity="mistake",
        )
        self.assertIn("key_squares", cats)
        self.assertIn("conversion_failure", cats)
        self.assertTrue(reasons)

    def test_classifier_identifies_rook_activity_and_lucena_like_positions(self):
        rook_cats, _ = pp.classify_weakness(
            fen_before="8/8/8/4k3/4P3/8/4K3/R7 w - - 0 1",
            fen_after="8/8/8/4k3/4P3/8/R3K3/8 b - - 1 1",
            move_uci="a1a2",
            best_move_uci="a1a8",
            side="white",
            before_cp=200,
            after_cp=-100,
            severity="mistake",
        )
        self.assertIn("rook_activity", rook_cats)

        lucena_cats, _ = pp.classify_weakness(
            fen_before="4k3/4P3/8/8/8/8/4K3/R6r w - - 0 1",
            fen_after="4k3/4P3/8/8/8/8/5K2/R6r b - - 1 1",
            move_uci="e2f2",
            best_move_uci="a1a8",
            side="white",
            before_cp=300,
            after_cp=0,
            severity="mistake",
        )
        self.assertIn("lucena", lucena_cats)

        philidor_cats, _ = pp.classify_weakness(
            fen_before="4k3/8/8/4p3/8/8/4K3/R6r w - - 0 1",
            fen_after="4k3/8/8/4p3/8/8/5K2/R6r b - - 1 1",
            move_uci="e2f2",
            best_move_uci="a1a6",
            side="white",
            before_cp=0,
            after_cp=-300,
            severity="mistake",
        )
        self.assertIn("philidor", philidor_cats)

    def test_infer_move_uci_handles_simple_moves_and_castling(self):
        self.assertEqual(
            pp.infer_move_uci(
                "8/8/8/8/8/8/4P3/4K3 w - - 0 1",
                "8/8/8/8/8/4P3/8/4K3 b - - 0 1",
            ),
            "e2e3",
        )
        self.assertEqual(
            pp.infer_move_uci(
                "r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1",
                "r3k2r/8/8/8/8/8/8/R4RK1 b kq - 1 1",
            ),
            "e1g1",
        )


class PlayerProfileAppIntegrationTests(unittest.TestCase):
    def test_player_dossier_includes_profile_without_live_engine(self):
        original_db = pm.DB_PATH
        with tempfile.TemporaryDirectory() as td:
            pm.DB_PATH = Path(td) / "prep_manual.db"
            try:
                pm.init_db()
                conn = pm.db()
                try:
                    pid = conn.execute(
                        "SELECT player_id FROM Roster WHERE is_hero=0 ORDER BY fide DESC"
                    ).fetchone()[0]
                    self._insert_game(conn, pid)
                    dossier = pm.player_dossier(conn, pid)
                    self.assertIn("player_profile", dossier)
                    self.assertEqual(
                        dossier["player_profile"]["phase_profile"]["analyzed"],
                        0,
                    )
                    self.assertIn("opening_profile", dossier["player_profile"])
                finally:
                    conn.close()
            finally:
                pm.DB_PATH = original_db

    def test_player_scope_analysis_requires_player_id(self):
        original_db = pm.DB_PATH
        with tempfile.TemporaryDirectory() as td:
            pm.DB_PATH = Path(td) / "prep_manual.db"
            try:
                pm.init_db()
                conn = pm.db()
                try:
                    with self.assertRaises(ValueError):
                        pm.analyze_all(conn, scope="player", pid=None, max_games=1)
                finally:
                    conn.close()
            finally:
                pm.DB_PATH = original_db

    def test_export_markdown_writes_player_profile_section(self):
        original_db = pm.DB_PATH
        original_export = pm.EXPORT_DIR
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            pm.DB_PATH = root / "prep_manual.db"
            pm.EXPORT_DIR = root / "manual_sections"
            try:
                pm.init_db()
                conn = pm.db()
                try:
                    pid = conn.execute(
                        "SELECT player_id FROM Roster WHERE is_hero=0 ORDER BY fide DESC"
                    ).fetchone()[0]
                    self._insert_game(conn, pid)
                    written = pm.export_markdown(conn)
                    self.assertIn("00_INDEX.md", written)
                    text = (pm.EXPORT_DIR / "Dino_Ballecer_Needs_Improvement.md").read_text(
                        encoding="utf-8"
                    )
                    self.assertIn("## Player Profile", text)
                finally:
                    conn.close()
            finally:
                pm.DB_PATH = original_db
                pm.EXPORT_DIR = original_export

    def _insert_game(self, conn: sqlite3.Connection, pid: int) -> None:
        conn.execute(
            """INSERT INTO Games
               (player_id, color, presult, white, black, result, date, event,
                round, eco, opening, total_moves, moves_json, source, dedup_hash)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                pid,
                "white",
                "win",
                "GM Vignesh, N R",
                "Example Opponent",
                "1-0",
                "2026.06.01",
                "Unit",
                "1",
                "B12",
                "Caro-Kann Defense",
                3,
                json.dumps(["e4", "c6", "d4"]),
                "pgn",
                "unit-game",
            ),
        )
        conn.commit()


if __name__ == "__main__":
    unittest.main()
