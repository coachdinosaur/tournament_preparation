#!/usr/bin/env python3
"""Launch the Tournament Prep app with Puzzle Lab installed."""

import prep_manual_app as app
import puzzle_lab

puzzle_lab.install(app)

if __name__ == "__main__":
    app.main()
