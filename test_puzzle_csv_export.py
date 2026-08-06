import unittest

import puzzle_csv_export


class PuzzleCsvExportTests(unittest.TestCase):
    def test_injection_adds_export_button_and_script(self):
        html = '<body><span id="puzzleStatus" class="muted"></span></body>'
        output = puzzle_csv_export._inject_csv_export(html)
        self.assertIn('id="puzzleExportCsv"', output)
        self.assertIn('function puzzleExportCsv()', output)
        self.assertIn("['fen',p=>p.fen]", output)
        self.assertIn("['best_move',p=>p.best_move]", output)

    def test_injection_is_idempotent(self):
        html = '<body><span id="puzzleStatus" class="muted"></span></body>'
        once = puzzle_csv_export._inject_csv_export(html)
        twice = puzzle_csv_export._inject_csv_export(once)
        self.assertEqual(once, twice)
        self.assertEqual(twice.count('id="puzzleExportCsv"'), 1)

    def test_missing_puzzle_lab_marker_fails_clearly(self):
        with self.assertRaisesRegex(RuntimeError, "status control"):
            puzzle_csv_export._inject_csv_export('<body></body>')


if __name__ == "__main__":
    unittest.main()
