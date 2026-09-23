#!/usr/bin/env python3
"""Render Ellie's improvement plan as a student-facing PDF with puzzle diagrams.

Content mirrors Ellie_Improvement_Plan.md, rewritten for Ellie herself. Board
diagrams reuse ChessDiagram and the mpchess artwork from build_arlan_dossier_pdf.
"""

from __future__ import annotations

import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle,
)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_arlan_dossier_pdf import (  # noqa: E402
    A4, CONTENT_W, GOLD, GOLD_LIGHT, INK, LINE, MARGIN_BOTTOM, MARGIN_TOP, MARGIN_X,
    MUTED, NAVY, RED, RED_LIGHT, TEAL, TEAL_LIGHT, WHITE, BLUE_LIGHT, ChessDiagram,
    register_fonts,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "Ellie_Chess_Power_Up_Plan.pdf"

S: dict[str, ParagraphStyle] = {}


def styles() -> None:
    S["Body"] = ParagraphStyle("Body", fontName="Arial", fontSize=10.5, leading=14.5, textColor=INK, spaceAfter=5)
    S["Small"] = ParagraphStyle("Small", parent=S["Body"], fontSize=9, leading=12, spaceAfter=2)
    S["H1"] = ParagraphStyle("H1", fontName="Arial-Bold", fontSize=19, leading=23, textColor=NAVY, spaceBefore=2, spaceAfter=8)
    S["H2"] = ParagraphStyle("H2", fontName="Arial-Bold", fontSize=13, leading=16, textColor=TEAL, spaceBefore=8, spaceAfter=4)
    S["Title"] = ParagraphStyle("Title", fontName="Arial-Bold", fontSize=32, leading=38, textColor=WHITE, alignment=TA_CENTER)
    S["Sub"] = ParagraphStyle("Sub", fontName="Arial", fontSize=13, leading=18, textColor=WHITE, alignment=TA_CENTER)
    S["Big"] = ParagraphStyle("Big", fontName="Arial-Bold", fontSize=24, leading=28, textColor=NAVY, alignment=TA_CENTER)
    S["BigLabel"] = ParagraphStyle("BigLabel", fontName="Arial", fontSize=9, leading=11, textColor=MUTED, alignment=TA_CENTER)
    S["Card"] = ParagraphStyle("Card", parent=S["Body"], fontSize=11, leading=15.5)
    S["Cap"] = ParagraphStyle("Cap", parent=S["Body"], fontSize=9.5, leading=12.5, spaceAfter=0)


def P(text: str, style: str = "Body") -> Paragraph:
    return Paragraph(text, S[style])


def box(flowables, fill=BLUE_LIGHT, accent=TEAL, width=CONTENT_W) -> Table:
    t = Table([[flowables]], colWidths=[width])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), fill),
        ("LINEBEFORE", (0, 0), (0, -1), 4, accent),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def grid(rows, widths, header=True) -> Table:
    t = Table(rows, colWidths=widths, repeatRows=1 if header else 0)
    st = [
        ("GRID", (0, 0), (-1, -1), 0.5, LINE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    if header:
        st += [("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE)]
    t.setStyle(TableStyle(st))
    return t


def checklist(items, width=CONTENT_W) -> Table:
    rows = [["", P(i, "Small")] for i in items]
    t = Table(rows, colWidths=[7 * mm, width - 7 * mm])
    st = [("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("BOTTOMPADDING", (0, 0), (-1, -1), 5), ("TOPPADDING", (0, 0), (-1, -1), 5)]
    for r in range(len(rows)):
        st.append(("BOX", (0, r), (0, r), 0.9, NAVY))
    t.setStyle(TableStyle(st))
    return t


# ---------------------------------------------------------------- puzzles
# (theme, fen, side to move, task, hint, answer). Verified with Stockfish 18.
PUZZLES = [
    ("Take away the defender", "r2qkb1r/ppp1pppp/2n2n2/8/2BPP1b1/2N2N2/PP3PPP/R1BQK2R b KQkq - 0 6",
     "Black", "Is 6...Nxd4 safe? What is the best way to win the d4 pawn?",
     "Look at 7.Qxd4 Bxf3. Can White play a check first?",
     "<b>6...Bxf3! 7.gxf3 Qxd4</b> wins the pawn safely. After 6...Nxd4? 7.Qxd4! Bxf3, White plays "
     "<b>8.Qxd8+</b> (check first!) and Black loses a piece. <i>Take away the defender, then take the pawn.</i>"),
    ("Free piece with check", "3r2kr/2p3p1/p4q1p/2Q5/4R3/PP4P1/5P1P/R5K1 b - - 0 25",
     "Black", "Win material.", "Look along the long diagonal from your queen.",
     "<b>25...Qxa1+</b> takes a free rook, and it is check! In the game you played 25...Kh7."),
    ("Hidden check", "3r3r/2p3pk/p4q1p/8/4R3/PP4P1/2Q2P1P/R5K1 b - - 2 26",
     "Black", "What is White threatening?", "What is the white queen on c2 looking at?",
     "If the rook on e4 moves, the queen on c2 gives a <b>discovered check</b> on h7. "
     "<b>26...Qg6!</b> blocks the line. In the game 26...Rhe8?? lost to 27.Rxe8+."),
    ("A check that wins", "5rk1/1p3pp1/7Q/p1p1P3/3p2R1/3q3P/5PP1/6K1 b - - 0 27",
     "Black", "Win material.", "Checks first! Which check also hits something?",
     "<b>27...Qd1+! 28.Kh2 Qxg4</b>. The check wins the rook on g4."),
    ("Guard your king", "8/1Q3pk1/6pp/2qp4/8/3P2P1/r6P/5R1K b - - 5 33",
     "Black", "What does White want to do to f7? Stop it!", "Count the attackers on f7.",
     "White wants <b>Qxf7+</b>, then Qf8+ and Rf7+. <b>33...Rf2!</b> blocks the f-file and you are still winning. "
     "In the game 33...Qc3?? got mated."),
    ("Guard your king", "1r3rk1/ppR3pp/3p1p2/5P2/3pP1Q1/5R2/3q2PP/6K1 b - - 0 21",
     "Black", "Find White's threat first. Then find your move.", "Look at g7.",
     "White threatens <b>Qxg7#</b>. <b>21...Qd1+</b> or <b>21...Rf7</b> stops it. In the game 21...Qa5?? 22.Qxg7#."),
    ("Where does the king go?", "3r2k1/8/1N5p/Q4p2/P1P5/3P1qp1/5P1K/5R2 w - - 0 40",
     "White", "Why is 40.Kh3 a disaster? Where should the king go?", "What does ...g2+ do?",
     "After 40.Kh3?? g2+ the pawn attacks the rook and becomes a queen. <b>40.Kg1</b> (or 40.fxg3) holds."),
    ("Watch out: stalemate!", "1Q6/8/8/8/4Q1Pk/6p1/6K1/5R2 w - - 1 48",
     "White", "Mate in one! Which natural move is stalemate?", "The black king has almost no squares.",
     "<b>48.Qd8#</b> is mate (so is 48.Qh7+ Kg5 49.Qh5#). In the game <b>48.Qg6??</b> was stalemate: "
     "Black had no legal move and was not in check, so it was a draw."),
    ("Pawn race", "3r4/4KP2/8/p6p/7k/8/8/8 b - - 1 47",
     "Black", "Push your a-pawn, or stop White's f-pawn?", "Who gets a queen first?",
     "<b>47...Rb8!</b> (then ...Rf8 and ...Rxf7) stops the f-pawn and Black wins. "
     "In the game 47...a4?? 48.Kxd8 let White queen first."),
    ("Queen vs rook: skewer!", "6R1/3k4/8/1K6/8/8/8/2q5 b - - 15 73",
     "Black", "Why does 73...Qc7 lose the queen? Find a safe move.", "Can the rook check your king AND hit the queen?",
     "73...Qc7?? 74.Rg7+ is a <b>skewer</b>: check, then Rxc7. Win with safe checks like "
     "<b>73...Qb2+ 74.Ka6 Qa2+ 75.Kb6 Qe6+ 76.Kc5 Qxg8</b>."),
    ("In-between move", "r1b1r1k1/ppB2pbp/2p2np1/4P3/8/2Nn1N2/PPP2PPP/R4RK1 w - - 0 14",
     "White", "Don't take on d3 yet! What's better?", "Captures: which one also attacks something?",
     "<b>14.exf6!</b> takes the knight first. After 14...Bxf6 15.cxd3 you are a piece up."),
    ("Is the knight stuck?", "3r1rk1/ppp1bppp/4pn2/4P1B1/2B5/2N2P2/PP3P1P/R4R1K b - - 0 13",
     "Black", "Your knight on f6 is attacked. Is it really pinned?", "What is behind the knight? Is it protected?",
     "<b>13...Nd5!</b> The knight is only pinned to a <i>protected</i> bishop. After 14.Bxe7 Nxe7 nothing is lost."),
]


def puzzle_cell(i: int, pz) -> list:
    theme, fen, side, task, hint, _ = pz
    return [
        P(f"<font color='#1E7A78'><b>Puzzle {i}</b></font>  ·  {theme}", "Cap"),
        ChessDiagram(fen, orientation="white" if side == "White" else "black", size=76 * mm),
        P(f"<b>{side} to move.</b> {task}", "Cap"),
        P(f"<font color='#5E6A75'>Hint: {hint}</font>", "Cap"),
    ]


def puzzle_pages() -> list:
    out = []
    half = CONTENT_W / 2
    for start in range(0, len(PUZZLES), 4):
        cells = [puzzle_cell(start + k + 1, PUZZLES[start + k]) for k in range(4)]
        t = Table([[cells[0], cells[1]], [cells[2], cells[3]]], colWidths=[half, half])
        t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("BOTTOMPADDING", (0, 0), (-1, -1), 10)]))
        out += [P("Puzzles From Your Own Games" + (" (continued)" if start else ""), "H1")]
        if not start:
            out.append(P("Every position below happened in one of your games. The boards are shown from "
                         "your side. Try each one before you look at the answers!"))
        out += [t, PageBreak()]
    return out


def on_page(c, doc) -> None:
    if doc.page == 1:
        return
    c.saveState()
    c.setFont("Arial", 8)
    c.setFillColor(MUTED)
    c.drawString(MARGIN_X, 9 * mm, "Ellie's Chess Power-Up Plan")
    c.drawRightString(A4[0] - MARGIN_X, 9 * mm, f"Page {doc.page}")
    c.restoreState()


def cover() -> list:
    banner = Table([[[
        Spacer(1, 28 * mm),
        P("Ellie's Chess<br/>Power-Up Plan", "Title"), Spacer(1, 8 * mm),
        P("What your games are teaching you,<br/>and how to become even stronger", "Sub"),
        Spacer(1, 28 * mm),
    ]]], colWidths=[CONTENT_W])
    banner.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), NAVY)]))
    stats = Table([[
        [P("873 → 990", "Big"), P("your rapid rating in 8 weeks", "BigLabel")],
        [P("15", "Big"), P("wins since July", "BigLabel")],
        [P("10", "Big"), P("winning positions to turn into wins", "BigLabel")],
    ]], colWidths=[CONTENT_W / 3] * 3)
    stats.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), GOLD_LIGHT), ("LINEABOVE", (0, 0), (-1, 0), 3, GOLD),
                               ("TOPPADDING", (0, 0), (-1, -1), 12), ("BOTTOMPADDING", (0, 0), (-1, -1), 12)]))
    return [banner, Spacer(1, 12 * mm), stats, Spacer(1, 12 * mm),
            P("Made on 24 September 2026 from your 31 Lichess games (30 July – 22 September), checked "
              "move by move by a chess engine. Go through it with your coach.", "Small"),
            PageBreak()]


def intro() -> list:
    return [
        P("Look How Far You've Come", "H1"),
        P("You have gone up about <b>120 rating points in eight weeks</b>. You scored "
          "<b>15 wins, 5 draws and 11 losses</b>, and here is what you already do well:"),
        grid([
            [P("<font color='white'><b>What you do well</b></font>", "Small"), P("<font color='white'><b>Proof</b></font>", "Small")],
            [P("<b>You start games well.</b> You develop your knights, castle and fight for the center.", "Small"),
             P("Your opening moves are your most accurate moves.", "Small")],
            [P("<b>You get winning positions all the time.</b>", "Small"),
             P("You were winning in 10 of the games you didn't win!", "Small")],
            [P("<b>You can play really clean games.</b>", "Small"),
             P("18 Sep (London) and 9 Sep (Four Knights): zero big mistakes.", "Small")],
            [P("<b>You spot mates.</b>", "Small"),
             P("20 Sep: after 14...Bxd1 you played <b>15.Bxf7#</b>!", "Small")],
            [P("<b>Your basic mates are strong.</b>", "Small"),
             P("King + queen vs king: 5 out of 5 in your drills.", "Small")],
        ], [CONTENT_W * 0.5, CONTENT_W * 0.5]),
        Spacer(1, 6 * mm),
        box([P("<b>The big secret in your games</b>", "H2"),
             P("You are already good enough to get winning positions. The next step is "
               "<b>finishing them</b>. If you had won just half of those 10 games, your rating would be a lot higher "
               "already, and you wouldn't need to learn anything new. You just need a few new habits.")],
            fill=GOLD_LIGHT, accent=GOLD),
        PageBreak(),
    ]


def power_ups() -> list:
    def pu(n, title, what, example, habit, fill, accent):
        return KeepTogether([box([
            P(f"Power-Up {n}: {title}", "H2"),
            P(what),
            P(f"<b>From your games:</b> {example}"),
            P(f"<b>Your new habit:</b> {habit}"),
        ], fill=fill, accent=accent), Spacer(1, 4 * mm)])
    return [
        P("Your 4 Power-Ups", "H1"),
        P("These are the four things that cost you the most points. Each one can be fixed with practice."),
        pu(1, "Finish the job", "When you're winning, the game isn't over yet. You gave away wins with "
           "stalemate, pawn races and queen tricks.",
           "on 30 Aug you had <b>two queens and a rook</b> and played 48.Qg6?? which was stalemate. "
           "48.Qd8 was checkmate!",
           "when you're winning, <b>trade pieces, keep your king safe, and check for stalemate on every move</b> "
           "once your opponent only has a king left.", GOLD_LIGHT, GOLD),
        pu(2, "Guard your king", "Sometimes your queen goes on a pawn hunt far away while your opponent "
           "attacks your king.",
           "on 30 Aug your queen took pawns on a2, c2 and d3, and then 21...Qa5?? allowed Qxg7#. "
           "You still had 8 minutes on your clock.",
           "<b>one pawn is not worth my king.</b> Before your queen grabs a pawn, look at "
           "which enemy pieces can reach your king.", RED_LIGHT, RED),
        pu(3, "Checks, captures, threats", "Your opponents make lots of mistakes, and sometimes you miss them. "
           "Sometimes you also miss your own winning checks.",
           "on 21 Sep, <b>25...Qxa1+</b> would have taken a free rook with check.",
           "before every move, say <b>CCT</b>: my Checks, Captures and Threats, and then my opponent's.",
           TEAL_LIGHT, TEAL),
        pu(4, "Slow down at stop signs", "Most of your big mistakes were played in <b>under 10 seconds</b>. "
           "In the games you lost, you still had about <b>5½ minutes</b> left on your clock.",
           "you move in about 5 seconds, even in dangerous positions.",
           "think <b>20 seconds or more</b> at every stop sign (next page). You have plenty of time!",
           BLUE_LIGHT, NAVY),
        PageBreak(),
    ]


def card() -> list:
    signs = grid([
        [P("<font color='white'><b>STOP SIGN</b></font>", "Small"), P("<font color='white'><b>Ask yourself</b></font>", "Small")],
        [P("My opponent just <b>captured</b> or gave <b>check</b>.", "Small"), P("Can I take back? Is there something better?", "Small")],
        [P("An enemy piece moved <b>toward my king</b>.", "Small"), P("What is it threatening? Do I need to defend?", "Small")],
        [P("I want to take a pawn with my <b>queen</b>.", "Small"), P("Is my king safe if my queen goes away?", "Small")],
        [P("I think <b>I'm winning</b>.", "Small"), P("How could I lose from here? Can I trade pieces?", "Small")],
        [P("There are <b>only a few pieces left</b>.", "Small"), P("Is this stalemate? Whose pawn queens first?", "Small")],
    ], [CONTENT_W * 0.45, CONTENT_W * 0.55])
    tcard = box([
        P("My Tournament Card: keep this next to your scoresheet", "H2"),
        P("<b>1. Every move: CCT.</b> Checks, Captures, Threats. Mine first, then my opponent's.", "Card"),
        P("<b>2. Stop signs mean 20+ seconds.</b> Capture or check · piece coming at my king · queen grabbing a pawn · "
          "I'm winning · few pieces left.", "Card"),
        P("<b>3. When I'm winning:</b> trade pieces · keep my king safe · stop their passed pawn · "
          "check for stalemate.", "Card"),
        P("<b>4. Use my clock.</b> Losing with lots of time left is the worst way to lose.", "Card"),
    ], fill=WHITE, accent=GOLD)
    tcard.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 1.2, GOLD), ("LINEBEFORE", (0, 0), (0, -1), 4, GOLD)]))
    return [P("Stop Signs", "H1"),
            P("At a stop sign, take your hands off the pieces and think for <b>at least 20 seconds</b>. "
              "In a 10-minute game you can do that about 10 times and still have lots of time left."),
            signs, Spacer(1, 10 * mm), tcard, PageBreak()]


def answers() -> list:
    rows = [[P("<font color='white'><b>#</b></font>", "Small"), P("<font color='white'><b>Answer</b></font>", "Small")]]
    rows += [[P(f"<b>{i}</b>", "Small"), P(pz[5], "Small")] for i, pz in enumerate(PUZZLES, 1)]
    return [P("Answers", "H1"), P("Only look after you have really tried!"),
            grid(rows, [10 * mm, CONTENT_W - 10 * mm]), PageBreak()]


def practice() -> list:
    daily = grid([
        [P("<font color='white'><b>Time</b></font>", "Small"), P("<font color='white'><b>What to do</b></font>", "Small")],
        [P("10 min", "Small"), P("Lichess puzzles by theme. Change the theme each day: <b>Hanging piece · Mate in 1 · "
                                 "Mate in 2 · Discovered attack · Intermezzo · Defensive move · Queen endgame</b>", "Small")],
        [P("10 min", "Small"), P("Before solving a puzzle, say out loud: <b>what is my opponent threatening?</b>", "Small")],
        [P("5–10 min", "Small"), P("Replay one of your own games and find the move you missed.", "Small")],
    ], [22 * mm, CONTENT_W - 22 * mm])
    weeks = checklist([
        "<b>Week 1: CCT.</b> Puzzles 1–4 with your coach. Say \"CCT\" before every move in 2 practice games.",
        "<b>Week 2: Guard your king.</b> Puzzles 5–7. Replay your 6 Aug and 30 Aug games with your coach.",
        "<b>Week 3: Finish the job I.</b> Puzzles 8–9. Win a winning position against the computer without stalemate.",
        "<b>Week 4: Finish the job II.</b> Queen vs knight drill (your trickiest one!) and Puzzle 10.",
        "<b>Week 5: Tricky moves.</b> Puzzles 11–12. Intermezzo and discovered attack puzzles.",
        "<b>Week 6: Check-up.</b> Look at your last 10 games with your coach. Were the mistakes at stop signs?",
    ])
    goals = grid([
        [P("<font color='white'><b>My goal</b></font>", "Small"), P("<font color='white'><b>Now</b></font>", "Small"),
         P("<font color='white'><b>In 6 weeks</b></font>", "Small")],
        [P("Big mistakes per game", "Small"), P("about 3", "Small"), P("under 2", "Small")],
        [P("Winning positions I don't win", "Small"), P("10 in 31 games", "Small"), P("almost none!", "Small")],
        [P("Queen vs knight drill", "Small"), P("2 out of 6", "Small"), P("5 out of 6", "Small")],
        [P("Clock left when I lose", "Small"), P("5½ minutes", "Small"), P("I used my time", "Small")],
    ], [CONTENT_W * 0.44, CONTENT_W * 0.28, CONTENT_W * 0.28])
    lines = Table([[P("Game / date", "Small"), P("I lost (or drew) because I missed...", "Small")]] + [["", ""]] * 7,
                  colWidths=[35 * mm, CONTENT_W - 35 * mm], rowHeights=[None] + [9 * mm] * 7)
    lines.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.5, LINE), ("TEXTCOLOR", (0, 0), (-1, 0), MUTED)]))
    return [
        P("My Practice Plan", "H1"),
        P("Every day (25–30 minutes)", "H2"), daily,
        P("With my coach, one week at a time", "H2"), weeks,
        P("For the next 4 weeks, play practice games at <b>15+10</b> instead of 10+0 so you can practise stopping "
          "at stop signs.", "Small"),
        P("My goals", "H2"), goals,
        PageBreak(),
        P("My Mistake Notebook", "H1"),
        P("After every loss or draw, write one line. When the same line keeps coming back, that's what "
          "to practise next with your coach."),
        lines,
        Spacer(1, 12 * mm),
        box([P("<b>Remember:</b> every strong player lost games exactly like these. You are already getting "
               "winning positions. Now let's finish them. You've got this, Ellie!", "Card")], fill=TEAL_LIGHT, accent=TEAL),
    ]


def main() -> None:
    register_fonts()
    styles()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4, leftMargin=MARGIN_X, rightMargin=MARGIN_X,
                            topMargin=MARGIN_TOP, bottomMargin=MARGIN_BOTTOM,
                            title="Ellie's Chess Power-Up Plan", author="Chess coach")
    story = cover() + intro() + power_ups() + card() + puzzle_pages() + answers() + practice()
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print("saved ->", OUTPUT)


if __name__ == "__main__":
    main()
