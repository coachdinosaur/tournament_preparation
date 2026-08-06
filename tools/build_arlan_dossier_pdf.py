#!/usr/bin/env python3
"""Render the Arlan Cabe tournament preparation dossier as a polished PDF."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents


PAGE_W, PAGE_H = A4
MARGIN_X = 16 * mm
MARGIN_TOP = 17 * mm
MARGIN_BOTTOM = 15 * mm
CONTENT_W = PAGE_W - 2 * MARGIN_X

NAVY = colors.HexColor("#14283D")
NAVY_2 = colors.HexColor("#1D3A54")
TEAL = colors.HexColor("#1E7A78")
TEAL_LIGHT = colors.HexColor("#E7F3F1")
GOLD = colors.HexColor("#D8A93F")
GOLD_LIGHT = colors.HexColor("#FBF3DE")
RED = colors.HexColor("#A7473E")
RED_LIGHT = colors.HexColor("#F8EAE7")
BLUE_LIGHT = colors.HexColor("#EAF0F6")
INK = colors.HexColor("#202A34")
MUTED = colors.HexColor("#5E6A75")
LINE = colors.HexColor("#CCD4DA")
PAPER = colors.HexColor("#FAFBFC")
WHITE = colors.white

ROOT = Path(__file__).resolve().parents[1]
PIECE_IMAGE_DIR = ROOT / "assets" / "chess_pieces" / "mpchess" / "png"


PLANS: dict[str, dict[str, Any]] = {
    "Petr Kiriakov": {
        "tier": "B",
        "bottom": "No cheap target. Keep the opening familiar, make him solve a full game, and avoid a long Nimzo-Indian memory test when Arlan has Black.",
        "white_short": "Tarrasch French",
        "black_short": "QGD, no Nimzo",
        "as_white": {
            "weapon": "1.e4 e6 2.d4 d5 3.Nd2",
            "plan": "Use a Tarrasch French setup with Ngf3, Bd3, O-O and a timed e5 or exd5 decision. Be ready for an early ...h6 without reacting emotionally.",
            "avoid": "Do not switch to a Catalan only because the database score looks tempting unless that structure is already rehearsed.",
        },
        "as_black": {
            "weapon": "1.d4 d5 2.c4 e6",
            "plan": "Choose a QGD setup: Nf6, Be7, O-O, Nbd7 and ...c5. Meet 3.Nf3 with the same structure so the move order stays stable.",
            "avoid": "Avoid 1...Nf6 2.c4 e6 3.Nc3 Bb4. His recent and career Nimzo results are strong.",
        },
        "target": "Resistance and decision quality after move 30. Four of his 18 recent classical games were short draws, but that is a tendency, not an invitation to force matters.",
        "danger": "He played 1.d4 in every recent White game and has broad experience against every major Indian defense.",
        "drills": [
            "QGD move-order recall through move 12.",
            "French Tarrasch: one line versus ...Nf6 and one versus an early ...h6.",
            "Defensive rook positions: identify the most active rook square before taking material.",
        ],
        "model_notes": [
            "The decisive errors arrived only in an already difficult rook position. Study resistance: active rook first, material second.",
            "In the French loss, ...a5 missed a forcing capture. Train the forcing-move scan before a slow pawn move.",
        ],
    },
    "Tu Hoang Thong": {
        "tier": "A",
        "bottom": "The recent file is poor, especially in long games, but the opponent is still a GM with many opening choices over his career. Press patiently; do not play as if the point is owed.",
        "white_short": "1.e4, simple branches",
        "black_short": "Najdorf vs 2.d3/b3",
        "as_white": {
            "weapon": "1.e4",
            "plan": "Against 1...e5 use a quiet Italian; against 1...e6 use the Tarrasch French; against 1...c5 play a normal Open Sicilian. Keep one branch per reply.",
            "avoid": "Do not burn time trying to guess his first move response. His recent Black opening choices changed from game to game.",
        },
        "as_black": {
            "weapon": "1.e4 c5 2.Nf3 d6",
            "plan": "Expect 2.d3, 2.b3 or a Closed Sicilian. Develop with ...Nc6, ...g6, ...Bg7 and ...e6 or ...Nge7 before choosing a pawn break.",
            "avoid": "Do not treat a quiet anti-Sicilian as harmless and launch ...f5 or ...d5 before the king is safe.",
        },
        "target": "A long game. The recent classical score is lowest in 41-plus-move games, and the selected loss contains two costly knight decisions.",
        "danger": "Career evidence includes the Dutch, Sicilian, French, Slav and irregular first moves. Recent evidence should outweigh old frequency, but surprise value remains.",
        "drills": [
            "Defend 2.d3 and 2.b3 Sicilians without an early pawn lunge.",
            "Knight retreat exercise: list every safe retreat before occupying d5 or f4.",
            "One 45-minute technical ending from an equal position.",
        ],
        "model_notes": [
            "The game turned on knight placement: Ndf4 and later Nd5 allowed tactical swings. Compare every knight jump with the retreat square.",
            "The Dutch loss did not contain a single large blunder in the scan; the position worsened through small weaknesses in the pawn structure.",
        ],
    },
    "Cao Sang": {
        "tier": "A",
        "bottom": "His recent color split is sharp: strong as White, much softer as Black. With White, Arlan should make the French Advance the main target; with Black, prepare for 1.e4 only.",
        "white_short": "Advance French",
        "black_short": "Najdorf + Moscow",
        "as_white": {
            "weapon": "1.e4 e6 2.d4 d5 3.e5 c5 4.c3",
            "plan": "Develop with Nf3, Be2 or Bd3, O-O and Na3-c2 when needed. Keep the center intact until development is complete.",
            "avoid": "Do not rush f4-f5 or grab on c5 while the queenside pieces are undeveloped.",
        },
        "as_black": {
            "weapon": "1.e4 c5 2.Nf3 d6",
            "plan": "Use Arlan's Najdorf after 3.d4. Also rehearse one answer to 3.Bb5+; 3...Bd7 is the low-memory option.",
            "avoid": "Avoid choosing the French as a surprise. Cao's recent White score against the French is one of his strongest families.",
        },
        "target": "His Black French sample and the choice between piece and pawn recaptures. Make him commit to a structure before opening the position.",
        "danger": "He played 1.e4 in all 20 recent White games and scored well. Ten recent games involved queenside castling, so opposite-wing attacks are a real possibility.",
        "drills": [
            "Advance French: 10 minutes of c5/d4 pressure patterns.",
            "Moscow variation: choose and memorize one reply to Bb5+.",
            "Recapture-choice positions: compare queen, g-pawn and piece recaptures.",
        ],
        "model_notes": [
            "Bxd7 and Rc2 were passive exchange/rook choices. The training theme is preserving active pieces rather than simplifying automatically.",
            "In the French example, ...Qxf6 was inferior to ...gxf6. Do not assume the cleaner-looking recapture is best.",
        ],
    },
    "Rogelio Antonio Jr": {
        "tier": "A+",
        "bottom": "Highest preparation priority: a direct standings rival with a very current 75-game classical file. Attack his Caro-Kann with the Exchange setup; expect Bb5+ against Arlan's Sicilian.",
        "white_short": "Caro Exchange 4.Bd3",
        "black_short": "Moscow with ...Bd7",
        "as_white": {
            "weapon": "1.e4 c6 2.d4 d5 3.exd5 cxd5 4.Bd3",
            "plan": "Continue Nf3, c3, O-O, Re1 and Bf4 or Nd2. Keep queens on long enough to ask practical questions.",
            "avoid": "Do not drift into a random Advance Caro-Kann; his current file shows several successful setups there.",
        },
        "as_black": {
            "weapon": "1.e4 c5 2.Nf3 d6 3.Bb5+ Bd7",
            "plan": "After Bxd7+ Qxd7, use ...Nf6, ...g6, ...Bg7 and ...O-O. Accept a slightly quiet position and compete on the c-file and dark squares.",
            "avoid": "Do not improvise after 3.Bb5+. It is a repeated current choice for him against both ...Nc6 and ...d6.",
        },
        "target": "Caro-Kann Exchange structures and pawn-race calculation. His recent Black Caro sample scores below 50 percent and contains four losses.",
        "danger": "He played 1.e4 in every recent White game in the current file, with strong Rossolimo/Moscow and Petroff results.",
        "drills": [
            "Caro-Kann Exchange key opening position through move 10, from both sides.",
            "Moscow defense: one complete practice game with ...Bd7.",
            "King-and-pawn races: count the moves to promotion before moving the rook.",
        ],
        "model_notes": [
            "In the rook ending, Re5 missed the urgent h-pawn push. Advancing the passed pawn came before rook activity.",
            "As Black in the Catalan, Bxe2 grabbed material while ...Nc7 was the defensive priority. Decline material when a piece must regroup.",
        ],
    },
    "Enrique Paciencia": {
        "tier": "A+",
        "bottom": "Direct rating rival. Steer his White games into a Slav rather than his comfortable English; with White, use the Ruy Exchange to build a long technical game.",
        "white_short": "Ruy Exchange",
        "black_short": "...c6 and ...d5",
        "as_white": {
            "weapon": "1.e4 e5 2.Nf3 Nc6 3.Bb5 a6 4.Bxc6",
            "plan": "Use d3, O-O, Re1, Nbd2-f1-g3 and a kingside majority. The goal is a stable structure and repeated small decisions.",
            "avoid": "Do not choose the Scotch only because it is forcing; it is one of his most repeated current Black lines.",
        },
        "as_black": {
            "weapon": "1.c4 c6 and 1.d4 d5 2.c4 c6",
            "plan": "Force a Slav/Quiet Slav structure with ...Nf6, ...Bf5 or ...e6, ...Nbd7 and a prepared ...e5 or ...c5 break.",
            "avoid": "Avoid 1.c4 e5 unless it is deeply rehearsed. His recent English/Reti results are strong.",
        },
        "target": "Late decision-making. Seven of his 12 recent classical losses occurred after move 40, and the late-game score is below his overall recent score.",
        "danger": "He alternates 1.c4 and 1.d4 and can reach the same positions through different move orders. Identify the pawn structure, not the first-move label.",
        "drills": [
            "Ruy Exchange structure: kingside majority and good/bad bishop plan.",
            "Slav Quiet: one route to ...e5 and one route to ...c5.",
            "Convert a slightly better rook ending without rushing pawn captures.",
        ],
        "model_notes": [
            "In the Slav loss, Nd5 and an exposed king magnified the pressure. Exchange the dangerous attacker before placing a piece on a fixed central square.",
            "In the Philidor loss, quiet piece retreats repeatedly lost ground. Look for active captures and pawn breaks before accepting passivity.",
        ],
    },
    "Than Min Hlaing": {
        "tier": "A",
        "bottom": "A clear scoring opportunity, but the file has only 26 games. Use the clear pattern - Open Sicilian with White, immediate ...d5 against 1.Nf3 - without drawing detailed conclusions from too few games.",
        "white_short": "Open Sicilian",
        "black_short": "Immediate ...d5",
        "as_white": {
            "weapon": "1.e4 c5 2.Nf3 d6 3.d4 cxd4 4.Nxd4",
            "plan": "Choose a classical Be2/O-O setup and improve every piece before a kingside pawn push. Keep the center fluid.",
            "avoid": "Do not turn the game into a risky attack just because the rating is lower.",
        },
        "as_black": {
            "weapon": "1.Nf3 d5 2.d4 Nf6 3.c4 e6",
            "plan": "Use QGD development and contest e4. If he starts 1.c4, answer 1...e6 or 1...c6 with ...d5 next.",
            "avoid": "Do not allow a free King's Indian setup; that is the most repeated White family in the small file.",
        },
        "target": "The 20-30 move transition and Black-side Sicilians. The recent Black score is especially low, but the sample is small.",
        "danger": "No recent short draws: expect resistance. The file is limited enough that a first-move surprise is plausible.",
        "drills": [
            "Open Sicilian classical setup through move 12.",
            "QGD against Nf3 move orders.",
            "Forcing-move scan at moves 20-25: checks, captures, threats.",
        ],
        "model_notes": [
            "Be4 overlooked a better retreat square. Do not place a piece in the center when it becomes a tactical target.",
            "As Black in the Slav, Bg4 missed Nxe4. Scan central captures before developing while attacking another piece.",
        ],
    },
    "Lindri Juni Widjayanti": {
        "tier": "B",
        "bottom": "Low-confidence current report: only three recent classical games. The reliable broad tendency is 1.e4 as White; her Black opening choices require a flexible 1.e4 response sheet.",
        "white_short": "Flexible 1.e4",
        "black_short": "Mainline Najdorf",
        "as_white": {
            "weapon": "1.e4",
            "plan": "Against 1...e5 use a quiet Italian; against 1...e6 use the Tarrasch French; against a Pirc use Nf3, Be2 and O-O before expanding.",
            "avoid": "Avoid a mainline Ruy Lopez memory test. Her career Black results in that family are much stronger than in the French.",
        },
        "as_black": {
            "weapon": "1.e4 c5 2.Nf3 d6 3.d4 cxd4 4.Nxd4",
            "plan": "Play the rehearsed Najdorf. Her two 2024 White losses were Open Sicilians, including a Najdorf.",
            "avoid": "Do not mix Najdorf and Sveshnikov ideas. Pick the known structure and complete development.",
        },
        "target": "King-safety decisions and late rook/endgame calculation, with a strong low-sample warning.",
        "danger": "The career file reaches back to 1984. Old opening frequencies are context, not a prediction of the 2026 choice.",
        "drills": [
            "One Najdorf main line and one anti-Sicilian backup.",
            "Castle-side comparison: write three reasons before choosing O-O-O.",
            "Single-rook ending: active king versus pawn-grabbing.",
        ],
        "model_notes": [
            "The 2024 Sveshnikov loss includes O-O-O when O-O was safer, then a late king move. Make king safety an explicit decision.",
            "The Najdorf loss turned through Nc5 and Rb6 before the final Bxd5 blunder. Preserve rook activity and verify captures.",
        ],
    },
    "Angelo Young": {
        "tier": "A",
        "bottom": "A likely opponent in the Swiss with clear opening-sequence habits: d4/Nf3 as White, mixed Sicilian/Pirc as Black. Use 1.e4 with White and a strict ...d5 structure with Black.",
        "white_short": "1.e4, hit Sicilian",
        "black_short": "Slav/QGD vs d4",
        "as_white": {
            "weapon": "1.e4",
            "plan": "Against 1...c5 play 2.Nf3 and 3.d4; against 1...d6 use a quiet Classical setup with Nf3, Be2 and O-O.",
            "avoid": "Do not drift into a King's Indian as White. His recent Black results there are strong.",
        },
        "as_black": {
            "weapon": "1.d4 d5 2.Nf3 Nf6 3.g3 e6",
            "plan": "Use a QGD/Slav setup and prepare ...c5. Prevent long Catalan pressure by contesting the center early.",
            "avoid": "Do not answer 1.Nf3 with a vague bishop-on-g2 setup. He is comfortable when both sides develop their bishops to g2 and g7.",
        },
        "target": "Long technical pressure. Half of the recent games reached move 41, and most recent losses were late.",
        "danger": "His Black opening choices are broad; the Pirc/Czech system has scored better than his Sicilian in the current file.",
        "drills": [
            "Open Sicilian against 2...d6.",
            "QGD against Nf3-g3 move orders.",
            "Queen activity: compare a queen trade, a queen retreat and an active queen capture.",
        ],
        "model_notes": [
            "Qe1 missed the active Qxd4. The recurring theme is a passive queen retreat when central activity is available.",
            "The Black-side loss had no single 0.60-pawn error after move 5 in the depth-12 engine check. Study how several small decisions added up, not one large mistake.",
        ],
    },
    "Anjela Khegay": {
        "tier": "A",
        "bottom": "Her colors are predictable: 1.d4 as White and Modern/Pirc against 1.e4. Arlan should answer with the Slav and a controlled Be3 setup, not a race to opposite-side attacks.",
        "white_short": "Be3 vs Modern",
        "black_short": "Quiet Slav",
        "as_white": {
            "weapon": "1.e4 g6 2.d4 Bg7 3.Nc3 d6 4.Be3",
            "plan": "Add Nf3 and Qd2, then choose castling based on the center. Use h3 before g4 when Black's queen and bishop are active.",
            "avoid": "Do not castle long automatically. Her Modern positions reward active play against a king that has already committed to one side.",
        },
        "as_black": {
            "weapon": "1.d4 d5 2.Nf3 Nf6 3.c4 c6 4.e3 Bf5",
            "plan": "Use the Quiet Slav, complete ...e6 and ...Nbd7, and strike with ...c5. This also matches one of her recent White losses.",
            "avoid": "Avoid the King's Indian and Benoni. Those are among her best career White families.",
        },
        "target": "Middlegame piece coordination. Five of six recent losses occurred before move 41; her late-game score is comparatively strong.",
        "danger": "Do not simplify automatically. Her recent results are strongest in late games.",
        "drills": [
            "Modern Defense: Be3 setup with both castling options.",
            "Quiet Slav through the ...c5 break.",
            "Tactical center: compare Rxc5, retreat and pawn recapture.",
        ],
        "model_notes": [
            "Qd1 missed the active Rxc5. The theme is solving the center before retreating a major piece.",
            "As Black in the Benoni, three large swings came from move 30 onward. Keep checking checks, captures and threats when the position becomes tactical.",
        ],
    },
}


def register_fonts() -> None:
    candidates = {
        "Arial": Path("C:/Windows/Fonts/arial.ttf"),
        "Arial-Bold": Path("C:/Windows/Fonts/arialbd.ttf"),
        "Arial-Italic": Path("C:/Windows/Fonts/ariali.ttf"),
        "Arial-BoldItalic": Path("C:/Windows/Fonts/arialbi.ttf"),
    }
    for name, path in candidates.items():
        if path.exists():
            pdfmetrics.registerFont(TTFont(name, str(path)))
    pdfmetrics.registerFontFamily(
        "Arial",
        normal="Arial",
        bold="Arial-Bold",
        italic="Arial-Italic",
        boldItalic="Arial-BoldItalic",
    )


def make_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "Body": ParagraphStyle(
            "Body", parent=base["BodyText"], fontName="Arial", fontSize=8.6,
            leading=11.2, textColor=INK, spaceAfter=4.2, splitLongWords=False,
        ),
        "BodyTight": ParagraphStyle(
            "BodyTight", parent=base["BodyText"], fontName="Arial", fontSize=8.0,
            leading=10.0, textColor=INK, spaceAfter=2.5,
        ),
        "Small": ParagraphStyle(
            "Small", parent=base["BodyText"], fontName="Arial", fontSize=7.1,
            leading=8.8, textColor=MUTED, spaceAfter=2,
        ),
        "Tiny": ParagraphStyle(
            "Tiny", parent=base["BodyText"], fontName="Arial", fontSize=6.2,
            leading=7.5, textColor=MUTED,
        ),
        "SectionTitle": ParagraphStyle(
            "SectionTitle", parent=base["Heading1"], fontName="Arial-Bold",
            fontSize=18, leading=21, textColor=NAVY, spaceBefore=0, spaceAfter=8,
            keepWithNext=True,
        ),
        "OpponentTitle": ParagraphStyle(
            "OpponentTitle", parent=base["Heading1"], fontName="Arial-Bold",
            fontSize=17, leading=20, textColor=NAVY, spaceBefore=0, spaceAfter=6,
            keepWithNext=True,
        ),
        "H2": ParagraphStyle(
            "H2", parent=base["Heading2"], fontName="Arial-Bold", fontSize=11.5,
            leading=14, textColor=TEAL, spaceBefore=7, spaceAfter=4, keepWithNext=True,
        ),
        "H3": ParagraphStyle(
            "H3", parent=base["Heading3"], fontName="Arial-Bold", fontSize=9.3,
            leading=11.5, textColor=NAVY_2, spaceBefore=4, spaceAfter=2, keepWithNext=True,
        ),
        "TableHead": ParagraphStyle(
            "TableHead", parent=base["BodyText"], fontName="Arial-Bold",
            fontSize=7.2, leading=8.4, textColor=WHITE, alignment=TA_LEFT,
        ),
        "TableCell": ParagraphStyle(
            "TableCell", parent=base["BodyText"], fontName="Arial", fontSize=7.0,
            leading=8.6, textColor=INK,
        ),
        "TableCellSmall": ParagraphStyle(
            "TableCellSmall", parent=base["BodyText"], fontName="Arial", fontSize=6.4,
            leading=7.7, textColor=INK,
        ),
        "Callout": ParagraphStyle(
            "Callout", parent=base["BodyText"], fontName="Arial", fontSize=8.3,
            leading=10.5, textColor=INK,
        ),
        "CalloutSmall": ParagraphStyle(
            "CalloutSmall", parent=base["BodyText"], fontName="Arial", fontSize=7.6,
            leading=9.5, textColor=INK,
        ),
        "CoverKicker": ParagraphStyle(
            "CoverKicker", parent=base["BodyText"], fontName="Arial-Bold",
            fontSize=10, leading=12, textColor=GOLD, tracking=1.2, alignment=TA_LEFT,
        ),
        "CoverTitle": ParagraphStyle(
            "CoverTitle", parent=base["Title"], fontName="Arial-Bold",
            fontSize=32, leading=34, textColor=WHITE, alignment=TA_LEFT, spaceAfter=4,
        ),
        "CoverSub": ParagraphStyle(
            "CoverSub", parent=base["BodyText"], fontName="Arial",
            fontSize=14, leading=18, textColor=colors.HexColor("#DDE8EF"),
            alignment=TA_LEFT,
        ),
        "CoverMeta": ParagraphStyle(
            "CoverMeta", parent=base["BodyText"], fontName="Arial",
            fontSize=9.2, leading=12.2, textColor=WHITE,
        ),
        "TOC0": ParagraphStyle(
            "TOC0", parent=base["BodyText"], fontName="Arial-Bold", fontSize=9,
            leading=12, leftIndent=0, firstLineIndent=0, textColor=NAVY,
            spaceBefore=3,
        ),
    }


STYLES: dict[str, ParagraphStyle]


def p(text: str, style: str = "Body") -> Paragraph:
    return Paragraph(escape(str(text)).replace("\n", "<br/>"), STYLES[style])


def ph(html: str, style: str = "Body") -> Paragraph:
    return Paragraph(html, STYLES[style])


def label_text(label: str, text: str, style: str = "Body") -> Paragraph:
    return ph(f"<b>{escape(label)}</b> {escape(str(text))}", style)


def bullet_paragraph(text: str, style: str = "BodyTight") -> Paragraph:
    return Paragraph(
        f'<bullet color="#1E7A78">&#8226;</bullet>{escape(text)}',
        ParagraphStyle(
            f"{style}-bullet", parent=STYLES[style], leftIndent=10, firstLineIndent=0,
            bulletIndent=0, spaceAfter=2.5,
        ),
    )


def fmt_pct(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.1f}%"


def fmt_wdl(row: dict[str, Any]) -> str:
    if not row or not row.get("games"):
        return "0 games"
    return f"{row['wins']}-{row['draws']}-{row['losses']} | {fmt_pct(row['score_pct'])}"


def score_word(score: float) -> str:
    return "Win" if score == 1 else "Draw" if score == 0.5 else "Loss"


def result_for_subject(record: dict[str, Any]) -> str:
    return score_word(float(record["score"]))


def plain_engine_value(value: Any) -> str:
    text = str(value)
    if text.startswith("-M"):
        return "forced mate for Arlan"
    if text.startswith("+M") or text.startswith("M"):
        return "forced mate for them"
    return text


def evidence_grade(summary: dict[str, Any]) -> tuple[str, colors.Color]:
    n = summary["coverage"]["recent_classical"]["games"]
    if n >= 25:
        return ("HIGH", TEAL)
    if n >= 12:
        return ("MEDIUM", GOLD)
    return ("LOW", RED)


def callout(title: str, body: str, fill: colors.Color = BLUE_LIGHT, accent: colors.Color = TEAL) -> Table:
    content = ph(
        f'<font color="{accent.hexval()}"><b>{escape(title.upper())}</b></font><br/>{escape(body)}',
        "Callout",
    )
    table = Table([[content]], colWidths=[CONTENT_W], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), fill),
        ("BOX", (0, 0), (-1, -1), 0.6, colors.Color(accent.red, accent.green, accent.blue, alpha=0.55)),
        ("LINEBEFORE", (0, 0), (0, -1), 3.2, accent),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return table


def two_plan_boxes(plan: dict[str, Any]) -> Table:
    def cell(title: str, data: dict[str, str], color: colors.Color, fill: colors.Color) -> Table:
        content = [
            ph(f'<font color="{color.hexval()}"><b>{escape(title)}</b></font>', "H3"),
            label_text("Prepared line:", data["weapon"], "CalloutSmall"),
            label_text("Plan:", data["plan"], "CalloutSmall"),
            label_text("Avoid:", data["avoid"], "CalloutSmall"),
        ]
        inner = Table([[content]], colWidths=[(CONTENT_W - 6 * mm) / 2], hAlign="LEFT")
        inner.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), fill),
            ("BOX", (0, 0), (-1, -1), 0.6, color),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ]))
        return inner

    left = cell("ARLAN HAS WHITE", plan["as_white"], TEAL, TEAL_LIGHT)
    right = cell("ARLAN HAS BLACK", plan["as_black"], NAVY_2, BLUE_LIGHT)
    outer = Table([[left, right]], colWidths=[CONTENT_W / 2, CONTENT_W / 2], hAlign="LEFT")
    outer.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return outer


def styled_table(
    data: list[list[Any]],
    widths: list[float],
    header: bool = True,
    font_size_style: str = "TableCell",
    repeat_rows: int = 1,
) -> Table:
    converted: list[list[Any]] = []
    for r_index, row in enumerate(data):
        converted.append([
            value if isinstance(value, Flowable) else p(str(value), "TableHead" if header and r_index == 0 else font_size_style)
            for value in row
        ])
    table = Table(converted, colWidths=widths, repeatRows=repeat_rows if header else 0, hAlign="LEFT")
    commands = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("GRID", (0, 0), (-1, -1), 0.35, LINE),
    ]
    if header:
        commands += [
            ("BACKGROUND", (0, 0), (-1, 0), NAVY_2),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ]
        start = 1
    else:
        start = 0
    for row in range(start, len(converted)):
        if (row - start) % 2:
            commands.append(("BACKGROUND", (0, row), (-1, row), PAPER))
    table.setStyle(TableStyle(commands))
    return table


class ChessDiagram(Flowable):
    """Compact board using the project's mpchess piece artwork."""

    PIECE_FILES = {
        "K": "wK.png", "Q": "wQ.png", "R": "wR.png",
        "B": "wB.png", "N": "wN.png", "P": "wP.png",
        "k": "bK.png", "q": "bQ.png", "r": "bR.png",
        "b": "bB.png", "n": "bN.png", "p": "bP.png",
    }
    IMAGE_CACHE: dict[str, ImageReader] = {}

    def __init__(self, fen: str, orientation: str = "white", size: float = 55 * mm):
        super().__init__()
        self.fen = fen
        self.orientation = orientation
        self.width = size
        self.height = size + 5 * mm
        self.board_size = size - 5 * mm

    def wrap(self, avail_width: float, avail_height: float) -> tuple[float, float]:
        return (self.width, self.height)

    def draw(self) -> None:
        c = self.canv
        board_x = 5 * mm
        board_y = 5 * mm
        sq = self.board_size / 8
        placement = self.fen.split()[0]
        ranks = placement.split("/")
        pieces: dict[tuple[int, int], str] = {}
        for fen_rank, rank_text in enumerate(ranks):
            file_index = 0
            for ch in rank_text:
                if ch.isdigit():
                    file_index += int(ch)
                else:
                    pieces[(file_index, 7 - fen_rank)] = ch
                    file_index += 1
        for display_row in range(8):
            for display_col in range(8):
                if self.orientation == "white":
                    file_index = display_col
                    rank_index = 7 - display_row
                else:
                    file_index = 7 - display_col
                    rank_index = display_row
                light = (file_index + rank_index) % 2 == 1
                c.setFillColor(colors.HexColor("#E8D8B6") if light else colors.HexColor("#76918B"))
                x = board_x + display_col * sq
                y = board_y + (7 - display_row) * sq
                c.rect(x, y, sq, sq, stroke=0, fill=1)
                piece = pieces.get((file_index, rank_index))
                if piece:
                    piece_file = self.PIECE_FILES[piece]
                    if piece_file not in self.IMAGE_CACHE:
                        piece_path = PIECE_IMAGE_DIR / piece_file
                        if not piece_path.exists():
                            raise FileNotFoundError(f"Chess piece asset not found: {piece_path}")
                        self.IMAGE_CACHE[piece_file] = ImageReader(str(piece_path))
                    piece_size = sq * 1.02
                    c.drawImage(
                        self.IMAGE_CACHE[piece_file],
                        x + (sq - piece_size) / 2,
                        y + (sq - piece_size) / 2,
                        width=piece_size,
                        height=piece_size,
                        preserveAspectRatio=True,
                        anchor="c",
                        mask="auto",
                    )
        c.setStrokeColor(NAVY)
        c.setLineWidth(0.8)
        c.rect(board_x, board_y, self.board_size, self.board_size, stroke=1, fill=0)
        c.setFont("Arial", 4.5)
        c.setFillColor(MUTED)
        files = "abcdefgh" if self.orientation == "white" else "hgfedcba"
        ranks_label = "87654321" if self.orientation == "white" else "12345678"
        for idx, file_label in enumerate(files):
            c.drawCentredString(board_x + (idx + 0.5) * sq, board_y - 4.2, file_label)
        for idx, rank_label in enumerate(ranks_label):
            c.drawRightString(board_x - 2.2, board_y + (7.5 - idx) * sq - 1.7, rank_label)


class HorizontalScoreChart(Flowable):
    def __init__(self, rows: list[dict[str, Any]], width: float = CONTENT_W, row_h: float = 7.2 * mm):
        super().__init__()
        self.rows = rows
        self.width = width
        self.row_h = row_h
        self.height = row_h * len(rows) + 11 * mm

    def wrap(self, avail_width: float, avail_height: float) -> tuple[float, float]:
        return (self.width, self.height)

    def draw(self) -> None:
        c = self.canv
        label_w = 46 * mm
        value_w = 27 * mm
        bar_w = self.width - label_w - value_w
        top = self.height - 7 * mm
        c.setFont("Arial", 6.3)
        c.setFillColor(MUTED)
        for tick in (0, 25, 50, 75, 100):
            x = label_w + bar_w * tick / 100
            c.drawCentredString(x, self.height - 4 * mm, str(tick))
            c.setStrokeColor(colors.HexColor("#D8DEE3"))
            c.setLineWidth(0.35 if tick != 50 else 0.8)
            c.line(x, 0, x, top)
        for idx, row in enumerate(self.rows):
            y = top - (idx + 1) * self.row_h + 1.5 * mm
            score = row["score"] or 0
            c.setFont("Arial-Bold", 7.2)
            c.setFillColor(INK)
            c.drawString(0, y + 1.4 * mm, row["name"])
            c.setFillColor(colors.HexColor("#E4E9ED"))
            c.roundRect(label_w, y, bar_w, 3.6 * mm, 1.8 * mm, stroke=0, fill=1)
            fill = TEAL if score >= 50 else GOLD if score >= 40 else RED
            c.setFillColor(fill)
            c.roundRect(label_w, y, bar_w * score / 100, 3.6 * mm, 1.8 * mm, stroke=0, fill=1)
            c.setFont("Arial-Bold", 7.0)
            c.setFillColor(INK)
            star = "*" if row["n"] < 12 else ""
            c.drawRightString(self.width, y + 1.2 * mm, f"{score:.1f}% | {row['n']} games{star}")


class DossierDocTemplate(BaseDocTemplate):
    def __init__(self, filename: str, **kwargs: Any):
        super().__init__(filename, **kwargs)
        self._heading_seq = 0

    def beforeDocument(self) -> None:
        self._heading_seq = 0

    def afterFlowable(self, flowable: Flowable) -> None:
        if isinstance(flowable, Paragraph) and flowable.style.name in {"SectionTitle", "OpponentTitle"}:
            text = flowable.getPlainText()
            key = f"heading-{self._heading_seq}"
            self._heading_seq += 1
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(text, key, level=0, closed=False)
            self.notify("TOCEntry", (0, text, self.page, key))


def on_page(canvas: Any, doc: BaseDocTemplate) -> None:
    page = canvas.getPageNumber()
    canvas.saveState()
    canvas.setTitle("Arlan Cabe - 24th ASEAN+ Tournament Preparation")
    canvas.setAuthor("Tournament preparation team")
    canvas.setSubject("Opponent scouting and practical chess preparation")
    if page == 1:
        canvas.setFillColor(NAVY)
        canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
        # Subtle chessboard motif.
        sq = 12 * mm
        start_x = PAGE_W - 8.5 * sq
        start_y = PAGE_H - 9.0 * sq
        for rank in range(8):
            for file_index in range(8):
                if (rank + file_index) % 2 == 0:
                    canvas.setFillColor(colors.Color(1, 1, 1, alpha=0.035))
                    canvas.rect(start_x + file_index * sq, start_y + rank * sq, sq, sq, stroke=0, fill=1)
    else:
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.45)
        canvas.line(MARGIN_X, PAGE_H - 10.5 * mm, PAGE_W - MARGIN_X, PAGE_H - 10.5 * mm)
        canvas.setFont("Arial-Bold", 6.6)
        canvas.setFillColor(NAVY)
        canvas.drawString(MARGIN_X, PAGE_H - 8.1 * mm, "FM ARLAN CABE | S50/W50 STANDARD")
        canvas.setFont("Arial", 6.5)
        canvas.setFillColor(MUTED)
        canvas.drawRightString(PAGE_W - MARGIN_X, PAGE_H - 8.1 * mm, "SINGAPORE | 8-14 AUGUST 2026")
        canvas.setStrokeColor(LINE)
        canvas.line(MARGIN_X, 10.2 * mm, PAGE_W - MARGIN_X, 10.2 * mm)
        canvas.setFont("Arial", 6.2)
        canvas.setFillColor(MUTED)
        canvas.drawString(MARGIN_X, 6.9 * mm, "PRIVATE PREPARATION | BASED ON SUPPLIED GAMES | VERIFY AT PAIRING")
        canvas.drawRightString(PAGE_W - MARGIN_X, 6.9 * mm, f"PAGE {page}")
    canvas.restoreState()


def cover_story() -> list[Flowable]:
    return [
        Spacer(1, 24 * mm),
        p("TOURNAMENT PREPARATION GUIDE", "CoverKicker"),
        Spacer(1, 5 * mm),
        p("FM ARLAN CABE", "CoverTitle"),
        p("24th ASEAN+ Age-Group Chess Championships 2026", "CoverSub"),
        p("Standard S50 & W50 Open and Women", "CoverSub"),
        Spacer(1, 18 * mm),
        Table(
            [[
                ph("<b>9 ROUNDS</b><br/>Swiss system", "CoverMeta"),
                ph("<b>90 + 30</b><br/>Standard time control", "CoverMeta"),
                ph("<b>8-14 AUG</b><br/>Our Tampines Hub", "CoverMeta"),
            ]],
            colWidths=[CONTENT_W / 3] * 3,
            style=TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.Color(1, 1, 1, alpha=0.07)),
                ("BOX", (0, 0), (-1, -1), 0.6, colors.Color(1, 1, 1, alpha=0.25)),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.Color(1, 1, 1, alpha=0.18)),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]),
        ),
        Spacer(1, 23 * mm),
        ph(
            '<font color="#D8A93F"><b>PURPOSE</b></font><br/>'
            '<font color="#FFFFFF">Fast, color-specific decisions when a Swiss pairing is posted: one opening plan, one position type to seek, one danger to avoid.</font>',
            "CoverMeta",
        ),
        Spacer(1, 26 * mm),
        ph(
            '<font color="#DDE8EF">Prepared 1 August 2026 from the supplied opponent PGNs, Arlan\'s local game file, the tournament starting list, and a limited Stockfish check of critical positions at depth 12.</font>',
            "CoverMeta",
        ),
        Spacer(1, 6 * mm),
        ph('<font color="#D8A93F"><b>PRIVATE COACHING MATERIAL</b></font>', "CoverMeta"),
        PageBreak(),
    ]


def tournament_overview_story(data: dict[str, Any]) -> list[Flowable]:
    toc = TableOfContents()
    toc.levelStyles = [STYLES["TOC0"]]
    schedule = [
        ["Round", "Date", "Start", "Preparation note"],
        ["R1", "Sat 8 Aug", "15:30", "Full morning; stop opening work by lunch"],
        ["R2", "Sun 9 Aug", "09:00", "Night-before card only"],
        ["R3", "Mon 10 Aug", "09:00", "First double-round day"],
        ["R4", "Mon 10 Aug", "15:30", "Recovery beats new opening study"],
        ["R5", "Tue 11 Aug", "09:00", "Second double-round day"],
        ["R6", "Tue 11 Aug", "15:30", "Use the backup line if pairing is late"],
        ["-", "Wed 12 Aug", "Free day", "Review only patterns that appeared"],
        ["R7", "Thu 13 Aug", "09:00", "Third double-round day"],
        ["R8", "Thu 13 Aug", "15:30", "Energy and clock discipline"],
        ["R9", "Fri 14 Aug", "09:00", "Simple, familiar opening only"],
    ]
    return [
        p("Contents", "SectionTitle"),
        toc,
        PageBreak(),
        p("Tournament schedule and key facts", "SectionTitle"),
        callout(
            "Event facts",
            "24th ASEAN+ Age-Group Chess Championships 2026, Standard S50 & W50 Open and Women. Nine-round Swiss, 90 minutes plus 30 seconds per move, Our Tampines Hub, Singapore. Manila and Singapore are both UTC+8.",
            GOLD_LIGHT,
            GOLD,
        ),
        Spacer(1, 3 * mm),
        callout(
            "How to read the game data",
            "Recent means standard games dated 2022-2026. Career means all standard games in the supplied file. Percentages are scores from the named opponent's point of view. Asterisked chart samples have fewer than 12 recent games.",
            BLUE_LIGHT,
            NAVY_2,
        ),
        Spacer(1, 4 * mm),
        p("Standard schedule", "H2"),
        styled_table(schedule, [14 * mm, 27 * mm, 22 * mm, CONTENT_W - 63 * mm]),
        Spacer(1, 4 * mm),
        p("Double-round rule", "H2"),
        bullet_paragraph("For afternoon rounds, review only the assigned opponent card, the first 8-10 moves, and one practice position."),
        bullet_paragraph("No new branch after the morning game. If the opponent surprises, use the tournament-wide backup structure."),
        bullet_paragraph("Eat, walk, reset, then spend no more than 35 minutes on chess before the afternoon round."),
        p("90+30 time checkpoints", "H2"),
        styled_table(
            [
                ["Checkpoint", "Minimum time left", "Decision rule"],
                ["After move 10", "75 min", "Opening recall ends; calculate independently"],
                ["After move 20", "55 min", "Name the worst piece and the opponent's break"],
                ["After move 30", "35 min", "Keep a 3-minute reserve for every difficult calculation"],
                ["After move 40", "20 min", "Use increment; do not blitz a technical ending"],
            ],
            [31 * mm, 28 * mm, CONTENT_W - 59 * mm],
        ),
        Spacer(1, 2 * mm),
        p("Schedule source: event invitation schedule summarized by Chessqueen; tournament format and starting list cross-checked on Chess-Results. Links are listed in Sources and method.", "Small"),
        PageBreak(),
    ]


def arlan_baseline_story(data: dict[str, Any]) -> list[Flowable]:
    hero = data["hero"]
    s = hero["summary"]
    recent = s["coverage"]["recent_classical"]
    cw = s["colors"]["recent_white"]
    cb = s["colors"]["recent_black"]
    rows = []
    for item in data["opponents"]:
        rs = item["summary"]["coverage"]["recent_classical"]
        rows.append({"name": item["name"], "score": rs["score_pct"], "n": rs["games"]})
    return [
        p("Arlan's tournament-wide plan", "SectionTitle"),
        callout(
            "Main strategic fact",
            f"In the local recent classical sample Arlan scores {fmt_pct(cw['score_pct'])} with White but {fmt_pct(cb['score_pct'])} with Black. The preparation should protect the Black games and use White to create the winning chances.",
            TEAL_LIGHT,
            TEAL,
        ),
        Spacer(1, 4 * mm),
        styled_table(
            [
                ["Sample", "Games", "W-D-L", "Score"],
                ["All recent classical", recent["games"], f"{recent['wins']}-{recent['draws']}-{recent['losses']}", fmt_pct(recent["score_pct"])],
                ["White", cw["games"], f"{cw['wins']}-{cw['draws']}-{cw['losses']}", fmt_pct(cw["score_pct"])],
                ["Black", cb["games"], f"{cb['wins']}-{cb['draws']}-{cb['losses']}", fmt_pct(cb["score_pct"])],
                ["Games reaching move 41", s["style"]["recent_late_games"]["games"], fmt_wdl(s["style"]["recent_late_games"]), "Use as strength"],
            ],
            [52 * mm, 25 * mm, 43 * mm, CONTENT_W - 120 * mm],
        ),
        p("Opening choices to keep", "H2"),
        bullet_paragraph("White: 1.e4 is the default. Keep one answer ready for Sicilian, Caro-Kann, French, 1...e5 and Modern/Pirc."),
        bullet_paragraph("Black versus 1.e4: the rehearsed Sicilian/Najdorf is the primary prepared choice. Use a solid backup only when the opponent's anti-Sicilian is a known comfort line."),
        bullet_paragraph("Black versus 1.d4, 1.Nf3 or 1.c4: one ...d5 family only - Slav or QGD by move order. Do not improvise a King's Indian or Benoni mid-event."),
        bullet_paragraph("Endgames: Arlan's recent long-game result is a relative strength. Keep rooks active and preserve clock for move 35 onward."),
        p("What not to memorize", "H2"),
        bullet_paragraph("Do not memorize all of an opponent's opening choices. Learn the first decision point and the intended pawn structure."),
        bullet_paragraph("Do not turn a small database score into a claim of weakness. Samples below eight games only suggest possible directions."),
        bullet_paragraph("Do not abandon a familiar opening because one opponent card contains a different opening line."),
        PageBreak(),
        p("Recent classical form in the supplied files", "SectionTitle"),
        HorizontalScoreChart(rows),
        Spacer(1, 3 * mm),
        p("Score is from the opponent's point of view. The chart measures only the supplied recent classical sample; it is not a rating forecast. An asterisk marks fewer than 12 games.", "Small"),
        Spacer(1, 4 * mm),
        callout(
            "How to read the chart",
            "Tu and Than have weak recent files, but that does not justify risky play. Antonio, Cao and Kiriakov have enough current or consistent opening evidence to justify detailed work. Widjayanti's recent sample is too small for a confident form claim.",
            GOLD_LIGHT,
            GOLD,
        ),
        PageBreak(),
    ]


def opponent_matrix_story(data: dict[str, Any]) -> list[Flowable]:
    rows: list[list[Any]] = [["Rank", "Seed / opponent", "Recent classical", "Arlan White", "Arlan Black"]]
    tier_order = {"A+": 0, "A": 1, "B": 2}
    items = sorted(data["opponents"], key=lambda item: (tier_order[PLANS[item["name"]]["tier"]], item["seed"]))
    for item in items:
        rs = item["summary"]["coverage"]["recent_classical"]
        plan = PLANS[item["name"]]
        rows.append([
            plan["tier"],
            f"{item['seed']} | {item['title']} {item['name']} ({item['rating']})",
            f"{rs['games']} games | {fmt_wdl(rs)}",
            plan["white_short"],
            plan["black_short"],
        ])
    return [
        p("Opponent preparation priorities", "SectionTitle"),
        p("A+ means prepare first; A means complete a full card; B means keep the card ready but spend less opening-study time. Priority combines rating proximity, pairing likelihood, how recent the games are, and clarity of the target.", "Body"),
        styled_table(rows, [12 * mm, 48 * mm, 41 * mm, 41 * mm, CONTENT_W - 142 * mm], font_size_style="TableCellSmall"),
        Spacer(1, 5 * mm),
        p("Tournament-wide backup choices", "H2"),
        styled_table(
            [
                ["Color / opponent first move", "Backup structure", "First objective"],
                ["Arlan White", "1.e4", "Reach a known pawn structure by move 6"],
                ["Arlan Black vs 1.e4", "Sicilian / Najdorf", "Complete development before a pawn race"],
                ["Arlan Black vs 1.d4", "QGD or Slav", "Contest e4 and prepare ...c5"],
                ["Arlan Black vs 1.Nf3/c4", "...d5 or ...c6 then ...d5", "Prevent long Catalan/English pressure"],
            ],
            [45 * mm, 55 * mm, CONTENT_W - 100 * mm],
        ),
        Spacer(1, 5 * mm),
        callout(
            "When pairings are posted",
            "1) confirm color and opponent identity; 2) read the bottom line; 3) replay the prepared line once without notes; 4) solve the two practice positions; 5) write one sentence: pawn structure, opponent break, worst piece; 6) stop.",
            TEAL_LIGHT,
            TEAL,
        ),
        PageBreak(),
    ]


def first_move_text(rows: list[dict[str, Any]], limit: int = 4) -> str:
    if not rows:
        return "No sample"
    return ", ".join(f"{row['label']} {row['games']} ({row['pct']:.0f}%)" for row in rows[:limit])


def response_text(rows: list[dict[str, Any]], limit: int = 4) -> str:
    if not rows:
        return "No sample"
    return ", ".join(f"{row['label']} {row['games']} / {fmt_pct(row['score_pct'])}" for row in rows[:limit])


def repertoire_rows(item: dict[str, Any]) -> list[list[Any]]:
    s = item["summary"]
    recent_n = s["coverage"]["recent_classical"]["games"]
    recent_first = first_move_text(s["recent_white_first_moves"])
    career_first = first_move_text(s.get("classical_white_first_moves", []))
    recent_e4 = response_text(s["recent_responses"]["e4"])
    career_e4 = response_text(s.get("classical_responses", {}).get("e4", []))
    return [
        ["Question", f"Recent 2022+ ({recent_n} games)", "Career reference"],
        ["Opponent has White: first move", recent_first, career_first],
        ["Opponent has Black vs 1.e4", recent_e4, career_e4],
    ]


def trigger_rows(item: dict[str, Any]) -> list[list[Any]]:
    s = item["summary"]
    recent_n = s["coverage"]["recent_classical"]["games"]
    source = s["recent_lines"] if recent_n >= 8 else s.get("classical_lines", s["recent_lines"])
    rows: list[list[Any]] = [["Opponent has", "Recorded opening sequence", "Games / score"]]
    for label, key in (("White", "white"), ("Black vs 1.e4", "black_e4")):
        for row in source[key][:2]:
            rows.append([label, row["label"], f"{row['games']} / {fmt_pct(row['score_pct'])}"])
    if len(rows) == 1:
        rows.append(["-", "No stable sequence in the file", "-"])
    return rows


def profile_header(item: dict[str, Any]) -> list[Flowable]:
    s = item["summary"]
    recent = s["coverage"]["recent_classical"]
    grade, grade_color = evidence_grade(s)
    meta = Table(
        [[
            ph(f'<b>SEED {item["seed"]}</b><br/><font color="#5E6A75">{escape(item["fed"])} | FIDE {escape(item["fide_id"])}</font>', "TableCell"),
            ph(f'<b>{item["title"]} {escape(item["name"])}</b><br/><font color="#5E6A75">Rating {item["rating"]}</font>', "TableCell"),
            ph(f'<font color="{grade_color.hexval()}"><b>{grade} EVIDENCE</b></font><br/><font color="#5E6A75">Recent games: {recent["games"]}</font>', "TableCell"),
        ]],
        colWidths=[33 * mm, CONTENT_W - 69 * mm, 36 * mm],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), PAPER),
            ("BOX", (0, 0), (-1, -1), 0.6, LINE),
            ("INNERGRID", (0, 0), (-1, -1), 0.35, LINE),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]),
    )
    return [p(f"{item['title']} {item['name']} - color plan", "OpponentTitle"), meta, Spacer(1, 4 * mm)]


def opponent_page_one(item: dict[str, Any]) -> list[Flowable]:
    plan = PLANS[item["name"]]
    s = item["summary"]
    cov = s["coverage"]
    rw = s["colors"]["recent_white"]
    rb = s["colors"]["recent_black"]
    late = s["style"]["recent_late_games"]
    stats = [
        ["Game sample", "Games", "W-D-L", "Score"],
        [f"Career classical ({cov['year_min']}-{cov['year_max']})", cov["classical"]["games"], f"{cov['classical']['wins']}-{cov['classical']['draws']}-{cov['classical']['losses']}", fmt_pct(cov["classical"]["score_pct"])],
        ["Recent classical (2022+)", cov["recent_classical"]["games"], f"{cov['recent_classical']['wins']}-{cov['recent_classical']['draws']}-{cov['recent_classical']['losses']}", fmt_pct(cov["recent_classical"]["score_pct"])],
        ["Recent as White", rw["games"], f"{rw['wins']}-{rw['draws']}-{rw['losses']}", fmt_pct(rw["score_pct"])],
        ["Recent as Black", rb["games"], f"{rb['wins']}-{rb['draws']}-{rb['losses']}", fmt_pct(rb["score_pct"])],
        ["Recent games 41+ moves", late["games"], f"{late['wins']}-{late['draws']}-{late['losses']}", fmt_pct(late["score_pct"])],
    ]
    return [
        *profile_header(item),
        callout(f"Priority {plan['tier']} - bottom line", plan["bottom"], GOLD_LIGHT if plan["tier"] != "A+" else RED_LIGHT, GOLD if plan["tier"] != "A+" else RED),
        Spacer(1, 4 * mm),
        two_plan_boxes(plan),
        p("Games and results", "H2"),
        styled_table(stats, [57 * mm, 22 * mm, 36 * mm, CONTENT_W - 115 * mm]),
        p("Opening tendencies", "H2"),
        styled_table(repertoire_rows(item), [48 * mm, 63 * mm, CONTENT_W - 111 * mm], font_size_style="TableCellSmall"),
        p("Recorded opening sequences", "H2"),
        styled_table(trigger_rows(item), [31 * mm, CONTENT_W - 61 * mm, 30 * mm], font_size_style="TableCellSmall"),
        p("Practical notes", "H2"),
        bullet_paragraph(f"Aim: {plan['target']}", "BodyTight"),
        bullet_paragraph(f"Watch for: {plan['danger']}", "BodyTight"),
        p("Percentages above are opponent scores, not Arlan scores. Small line samples are preparation prompts, not predictions.", "Small"),
        PageBreak(),
    ]


def model_card(model: dict[str, Any], note: str) -> Table:
    engine = model.get("engine", {})
    moments = engine.get("critical_moments", [])
    moment = moments[0] if moments else None
    screening_acpl = engine.get("screening_acpl")
    average_loss = (
        f"{float(screening_acpl) / 100:.2f} pawns"
        if isinstance(screening_acpl, (int, float))
        else "not available"
    )
    title = f"{model['date']} | {model['subject_color'].title()} vs {model['opponent']} | {result_for_subject(model)}"
    context: list[Flowable] = [
        ph(f"<b>{escape(title)}</b>", "H3"),
        label_text("Opening:", f"{model['opening']} ({model['eco']})", "BodyTight"),
        label_text("Recorded line:", model["line"], "Small"),
    ]
    if moment:
        context.extend([
            label_text("Critical moment:", f"{moment['move']} - played {moment['played']}; Stockfish preferred {moment['best']}", "BodyTight"),
            label_text("Engine check:", f"{moment['severity']}, {moment['loss_cp']/100:.2f} pawns; evaluation for the opponent {plain_engine_value(moment['eval_before'])} to {plain_engine_value(moment['eval_after'])}", "Small"),
            label_text("Best line:", moment["best_line"], "Small"),
        ])
    else:
        context.append(p("No single change of 0.60 pawns or more appeared after move 5 in the selected depth-12 engine check.", "BodyTight"))
    context.append(label_text("Study theme:", note, "BodyTight"))
    context.append(p(f"Selected-game engine check: average estimated loss {average_loss} over {engine.get('subject_moves_scanned', 0)} moves. This is not a career accuracy measure.", "Tiny"))
    if moment:
        diagram: Flowable = ChessDiagram(moment["fen"], model["subject_color"], 57 * mm)
    else:
        small_content = ph(
            '<font color="#1D3A54"><b>SMALL ERRORS ADDED UP</b></font><br/>'
            'Replay the full game and mark the first position where the plan became passive.',
            "CalloutSmall",
        )
        diagram = Table([[small_content]], colWidths=[55 * mm], hAlign="LEFT")
        diagram.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), BLUE_LIGHT),
            ("BOX", (0, 0), (-1, -1), 0.6, NAVY_2),
            ("LINEBEFORE", (0, 0), (0, -1), 3.0, NAVY_2),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ]))
    card = Table([[diagram, context]], colWidths=[61 * mm, CONTENT_W - 61 * mm], hAlign="LEFT")
    card.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PAPER),
        ("BOX", (0, 0), (-1, -1), 0.6, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return card


def opponent_page_two(item: dict[str, Any], is_last: bool = False) -> list[Flowable]:
    plan = PLANS[item["name"]]
    models = item["summary"]["model_games"]
    story: list[Flowable] = [
        p(f"{item['title']} {item['name']} - practice positions", "SectionTitle"),
        p("Use these games to train decisions, not to memorize the opponent's mistakes. Recreate each critical position, set five minutes, and write three possible moves before checking the engine line. Positive engine values favor the opponent; negative values favor Arlan.", "Body"),
    ]
    for index, model in enumerate(models):
        note = plan["model_notes"][index] if index < len(plan["model_notes"]) else "Replay the position and compare forcing moves with the quiet move played."
        story.append(KeepTogether([model_card(model, note), Spacer(1, 4 * mm)]))
    story.extend([
        p("Three drills before the event", "H2"),
        *[bullet_paragraph(drill) for drill in plan["drills"]],
        p("Pairing-day final check", "H2"),
        styled_table(
            [
                ["Check", "Write one answer"],
                ["Expected pawn structure", "________________________________________"],
                ["Opponent's main break", "________________________________________"],
                ["My worst piece after development", "________________________________________"],
                ["Clock floor at move 20", "55 minutes"],
            ],
            [57 * mm, CONTENT_W - 57 * mm],
        ),
    ])
    if not is_last:
        story.append(PageBreak())
    return story


def training_plan_story() -> list[Flowable]:
    return [
        PageBreak(),
        p("Seven-day preparation sequence", "SectionTitle"),
        callout(
            "Rule",
            "Opening work ends with a position, not a move list. Every session must finish with: pawn structure, good and bad piece, opponent break, and the first move into an endgame.",
            TEAL_LIGHT,
            TEAL,
        ),
        Spacer(1, 4 * mm),
        styled_table(
            [
                ["Date", "Primary work", "Output"],
                ["1 Aug", "Lock White branches; Antonio Caro, Cao French", "Two 10-move recall cards"],
                ["2 Aug", "Lock Black vs 1.e4; Moscow, Open Sicilian, quiet anti-Sicilian", "Three key opening positions from memory"],
                ["3 Aug", "Lock Black vs d4/Nf3/c4; Slav-QGD move order", "One structure, three move orders"],
                ["4 Aug", "Paciencia, Young, Khegay game plans", "Six practice positions"],
                ["5 Aug", "Kiriakov, Tu, Than, Widjayanti cards", "Backup line confirmed"],
                ["6 Aug", "One 90+30 simulation; start from a likely key opening position", "Review of time use"],
                ["7 Aug", "Travel / technical meeting; light recall only", "Sleep and logistics"],
            ],
            [22 * mm, 91 * mm, CONTENT_W - 113 * mm],
        ),
        p("Daily workload", "H2"),
        bullet_paragraph("Opening recall: 35 minutes maximum per color."),
        bullet_paragraph("Practice positions: 4 positions x 8 minutes, then compare with the note."),
        bullet_paragraph("Endgame: 25 minutes, active-rook or Ruy Exchange structure."),
        bullet_paragraph("Physical reset: 30 minutes walking; no screen in the final hour before sleep."),
        p("During the tournament", "H2"),
        bullet_paragraph("After each game, record only the opening surprise and one critical decision. Full analysis waits until the free day or after the event."),
        bullet_paragraph("On 10, 11 and 13 August, recovery takes priority between rounds. Use the opponent card; do not reopen the entire PGN file."),
        bullet_paragraph("If a lower seed appears, keep the same clock and structure discipline. The plan is to outplay, not to force."),
        Spacer(1, 4 * mm),
        callout(
            "What the coach should send",
            "When the pairing is posted, the coach should send only: color, prepared line, one recorded opening sequence, one diagram, and the avoid note. More information is not automatically better preparation.",
            GOLD_LIGHT,
            GOLD,
        ),
        PageBreak(),
    ]


def sources_story(data: dict[str, Any]) -> list[Flowable]:
    rows = [["Opponent", "File", "All", "Classical", "Recent"]]
    for item in data["opponents"]:
        cov = item["summary"]["coverage"]
        file_label = (
            Path(item["source"]).name
            .replace("https___players.chessbase.com_games_", "")
            .replace(".pgn", "")
            .replace("_20", " ")
            .replace("_", " ")
        )
        rows.append([
            item["name"],
            file_label,
            cov["all"]["games"],
            cov["classical"]["games"],
            cov["recent_classical"]["games"],
        ])
    return [
        p("Sources and method", "SectionTitle"),
        p("Games included", "H2"),
        styled_table(rows, [41 * mm, CONTENT_W - 95 * mm, 16 * mm, 20 * mm, 18 * mm], font_size_style="TableCellSmall"),
        p("How this guide was built", "H2"),
        bullet_paragraph("PGN game files were read by player name, duplicate games were removed, and openings were matched against a local reference containing 3,662 positions."),
        bullet_paragraph("Games marked in their event or site details as blitz, rapid, online, or similar were kept out of the standard-game sample."),
        bullet_paragraph("Recent means 2022-2026. When the recent sample was thin, the report shows career evidence as an older reference and clearly labels the limited confidence."),
        bullet_paragraph("Two recent classical losses per opponent were selected where possible. Stockfish checked only the opponent's moves in those games at depth 12. The reported critical positions are quick checks, not complete measures of playing accuracy."),
        bullet_paragraph("Recommendations were matched to Arlan's local game file and prior opening notes. They favor familiar 1.e4, Sicilian/Najdorf and Slav-QGD structures."),
        p("Event references", "H2"),
        ph('<b>Starting list and tournament details:</b> <link href="https://chess-results.com/tnr1424547.aspx?lan=1" color="#1E7A78">Chess-Results event page</link>', "Body"),
        ph('<b>Invitation schedule summary:</b> <link href="https://www.chessqueen.kr/2b527f52-bbd5-808f-94c6-efa8cab602c3" color="#1E7A78">24th ASEAN+ event schedule</link>', "Body"),
        p("Limitations", "H2"),
        bullet_paragraph("The supplied files are not complete career databases. Missing games and errors in names or game details can change the percentages."),
        bullet_paragraph("Opening classification follows the deepest matched position. A position reached through a different move order may receive a different label from a commercial database."),
        bullet_paragraph("A current starting list can change. Recheck entries and pairings before each round."),
        bullet_paragraph("Engine depth 12 is adequate for a quick check, not for proving a new opening idea. Analyze any specific tactical line more deeply before using it."),
        Spacer(1, 5 * mm),
        callout(
            "Final coaching rule",
            "This guide helps with decisions. Arlan should enter every round with one familiar structure, one opponent-specific reminder, and enough clock to play chess after preparation ends.",
            TEAL_LIGHT,
            TEAL,
        ),
    ]


def build_pdf(data: dict[str, Any], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    frame = Frame(
        MARGIN_X,
        MARGIN_BOTTOM,
        CONTENT_W,
        PAGE_H - MARGIN_TOP - MARGIN_BOTTOM,
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
        id="main",
    )
    doc = DossierDocTemplate(
        str(output),
        pagesize=A4,
        leftMargin=MARGIN_X,
        rightMargin=MARGIN_X,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOTTOM,
        title="Arlan Cabe - Tournament Preparation",
        author="Tournament preparation team",
    )
    doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=on_page)])

    story: list[Flowable] = []
    story.extend(cover_story())
    story.extend(tournament_overview_story(data))
    story.extend(arlan_baseline_story(data))
    story.extend(opponent_matrix_story(data))
    for index, item in enumerate(sorted(data["opponents"], key=lambda row: row["seed"])):
        story.extend(opponent_page_one(item))
        story.extend(opponent_page_two(item, is_last=index == len(data["opponents"]) - 1))
    story.extend(training_plan_story())
    story.extend(sources_story(data))
    doc.multiBuild(story)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--analysis", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    register_fonts()
    global STYLES
    STYLES = make_styles()
    data = json.loads(args.analysis.read_text(encoding="utf-8"))
    build_pdf(data, args.output)
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
