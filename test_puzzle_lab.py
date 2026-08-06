import sqlite3
import unittest

import puzzle_lab


SAMPLE_PGN = '''[Event "Test Event"]
[Round "3"]
[White "Lin, Yi Christopher"]
[Black "Opponent, One"]
[Result "0-1"]

1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 0-1
'''


class FakeCore:
    CP_INACCURACY = 50
    CP_MISTAKE = 100
    CP_BLUNDER = 200
    ENGINE_DEPTH = 16

    @staticmethod
    def get_engine():
        return object()

    @staticmethod
    def name_tokens(value):
        import re
        return re.sub(r"[^a-z0-9]+", " ", value.lower()).split()

    @staticmethod
    def split_pgn_stream(raw):
        return [raw]

    @staticmethod
    def parse_pgn_game(raw):
        import re
        headers = dict(re.findall(r'^\[(\w+)\s+"(.*)"\]$', raw, re.M))
        return {"headers": headers, "moves": ["e4", "e5", "Nf3", "Nc6"]}

    @staticmethod
    def db():
        conn = sqlite3.connect(":memory:")
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def analyze_game(conn, dedup, moves, depth, allow_engine=True, force=False):
        return {"moves": [
            {
                "mover": "white", "loss": 280, "san": "Nxe5", "move_no": 24,
                "fen_before": "8/8/8/8/8/8/4K3/7k w - - 0 24",
                "move_uci": "f3e5", "best_uci": "a1a2", "best": "Ka2",
                "before": 30, "after": -250, "impact": 0.4,
            },
            {
                "mover": "black", "loss": 400, "san": "Qh4", "move_no": 24,
                "fen_before": "8/8/8/8/8/8/4K3/7k b - - 0 24",
                "move_uci": "d8h4", "best_uci": "d8d1", "best": "Qd1",
                "before": 20, "after": -380, "impact": 0.5,
            },
        ]}

    @staticmethod
    def fens_for(moves):
        return [], None

    @staticmethod
    def epd_key(fen):
        return " ".join(fen.split()[:4])


class PuzzleLabTests(unittest.TestCase):
    def test_fuzzy_name_matching(self):
        self.assertTrue(puzzle_lab._name_matches(
            FakeCore, "Lin Yi Christopher", "Lin, Yi Christopher"))
        self.assertFalse(puzzle_lab._name_matches(
            FakeCore, "Lin Yi Christopher", "Christopher Columbus"))

    def test_generate_filters_to_players_moves(self):
        result = puzzle_lab.generate_puzzles(
            FakeCore, SAMPLE_PGN, "Lin Yi Christopher")
        self.assertEqual(result["games_analyzed"], 1)
        self.assertEqual(len(result["puzzles"]), 1)
        puzzle = result["puzzles"][0]
        self.assertEqual(puzzle["severity"], "blunder")
        self.assertEqual(puzzle["cp_loss"], 280)
        self.assertEqual(puzzle["player_color"], "white")

    def test_ui_injection(self):
        html = '''<style></style><nav>  <button id="tb-export" onclick="tab('export')">Export</button></nav><main>  <div id="pg-export" style="display:none"></div></main><script>function tab(name){for(const t of ['overview','schedule','opponents','play','dino','files','export']){}}\n  if(name==='play') loadPlay();\nrefresh();\n</script>'''
        output = puzzle_lab._inject_ui(html)
        self.assertIn('tb-puzzle', output)
        self.assertIn('pg-puzzle', output)
        self.assertIn("'puzzle','export'", output)
        self.assertIn('puzzleGenerate', output)


if __name__ == "__main__":
    unittest.main()
