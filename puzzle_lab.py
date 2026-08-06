#!/usr/bin/env python3
"""Puzzle Lab extension for prep_manual_app.py.

Install this extension through prep_manual_app_puzzle.py. Everything remains
stdlib-only and offline except for the app's existing optional Stockfish link.
"""

from __future__ import annotations

import difflib
import hashlib
import re
from email.parser import BytesParser
from email.policy import default as email_policy
from urllib.parse import urlparse

DEFAULT_PLAYER_NAME = "Lin Yi Christopher"
MAX_UPLOAD_BYTES = 12 * 1024 * 1024
MAX_PUZZLES = 10


def _name_key(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", " ", (value or "").casefold())
    return " ".join(value.split())


def _name_tokens(core, value: str) -> set[str]:
    fn = getattr(core, "name_tokens", None)
    return set(fn(value)) if callable(fn) else set(_name_key(value).split())


def _name_matches(core, requested: str, candidate: str) -> bool:
    req_key, cand_key = _name_key(requested), _name_key(candidate)
    if not req_key or not cand_key:
        return False
    if req_key == cand_key:
        return True
    req_tokens = _name_tokens(core, requested)
    cand_tokens = _name_tokens(core, candidate)
    if req_tokens and cand_tokens:
        overlap = req_tokens & cand_tokens
        if len(overlap) >= 2 and (
            req_tokens <= cand_tokens
            or cand_tokens <= req_tokens
            or len(overlap) / max(len(req_tokens), len(cand_tokens)) >= 0.67
        ):
            return True
    return difflib.SequenceMatcher(None, req_key, cand_key).ratio() >= 0.78


def _parse_pgn_text(core, raw: str) -> list[dict]:
    parser = getattr(core, "parse_pgn_text", None)
    if callable(parser):
        parsed = parser(raw)
        if isinstance(parsed, dict):
            return [parsed]
        return [g for g in (parsed or []) if isinstance(g, dict)]
    games = []
    for block in core.split_pgn_stream(raw):
        game = core.parse_pgn_game(block)
        if game:
            games.append(game)
    return games


def _format_eval(cp) -> str:
    try:
        cp = int(cp)
    except (TypeError, ValueError):
        return "?"
    if cp >= 9000:
        return f"#+{max(1, 10000 - cp)}"
    if cp <= -9000:
        return f"#-{max(1, 10000 + cp)}"
    return f"{cp / 100:+.1f}"


def _severity(core, cp_loss: int) -> str:
    if cp_loss >= int(getattr(core, "CP_BLUNDER", 200)):
        return "blunder"
    if cp_loss >= int(getattr(core, "CP_MISTAKE", 100)):
        return "mistake"
    return "inaccuracy"


def _dedup_hash(headers: dict, moves: list[str]) -> str:
    seed = "|".join([
        str(headers.get("White", "")), str(headers.get("Black", "")),
        str(headers.get("Date", "")), str(headers.get("Round", "")),
        str(headers.get("Result", "")), " ".join(moves),
    ])
    return "puzzle-lab:" + hashlib.sha256(seed.encode("utf-8", "replace")).hexdigest()


def generate_puzzles(core, pgn_text: str, player_name: str) -> dict:
    player_name = (player_name or "").strip()
    pgn_text = (pgn_text or "").strip()
    if not player_name:
        raise ValueError("Enter the player name exactly as it appears in the PGN headers.")
    if not pgn_text:
        raise ValueError("Choose a PGN file or paste PGN text first.")
    if core.get_engine() is None:
        raise RuntimeError(
            "No Stockfish engine was found. Set PREP_STOCKFISH or place a Stockfish "
            "binary in the app's ./stockfish/ folder, then restart the app."
        )

    parsed_games = _parse_pgn_text(core, pgn_text)
    if not parsed_games:
        raise ValueError("No valid PGN games were found in the supplied text.")

    matches = []
    for game in parsed_games:
        headers = game.get("headers") or {}
        white = str(headers.get("White", "")).strip()
        black = str(headers.get("Black", "")).strip()
        if _name_matches(core, player_name, white):
            matches.append((game, "white", white))
        elif _name_matches(core, player_name, black):
            matches.append((game, "black", black))
    if not matches:
        raise ValueError(f'No games matched "{player_name}" in the White or Black PGN headers.')

    conn = core.db()
    collected = []
    games_analyzed = 0
    replay_warnings = []
    display_player = matches[0][2] or player_name
    try:
        for game, player_color, _matched_header_name in matches:
            headers = game.get("headers") or {}
            moves = list(game.get("moves") or [])
            if not moves:
                continue
            rollup = core.analyze_game(
                conn, _dedup_hash(headers, moves), moves,
                min(getattr(core, "ENGINE_DEPTH", 16), 12), allow_engine=True, force=True,
            )
            if not rollup:
                continue
            games_analyzed += 1
            opponent = str(headers.get("Black" if player_color == "white" else "White", "?"))
            for finding in rollup.get("moves", []):
                if finding.get("mover") != player_color:
                    continue
                cp_loss = int(round(float(finding.get("loss") or 0)))
                if cp_loss < int(getattr(core, "CP_INACCURACY", 50)):
                    continue
                fen = str(finding.get("fen_before") or "")
                if not fen:
                    continue
                collected.append({
                    "fen": fen,
                    "player_move": str(finding.get("san") or ""),
                    "player_move_uci": str(finding.get("move_uci") or ""),
                    "best_move": str(finding.get("best") or finding.get("best_uci") or ""),
                    "best_move_uci": str(finding.get("best_uci") or ""),
                    "cp_loss": cp_loss,
                    "severity": _severity(core, cp_loss),
                    "eval_before": _format_eval(finding.get("before")),
                    "eval_after": _format_eval(finding.get("after")),
                    "game_context": {
                        "white": str(headers.get("White", "?")),
                        "black": str(headers.get("Black", "?")),
                        "opponent": opponent,
                        "result": str(headers.get("Result", "*")),
                        "event": str(headers.get("Event", "")),
                        "round": str(headers.get("Round", "")),
                    },
                    "move_number": int(finding.get("move_no") or 0),
                    "player_color": player_color,
                    "impact": float(finding.get("impact") or 0),
                })
            _fens, replay_error = core.fens_for(moves)
            if replay_error:
                replay_warnings.append(replay_error)
    finally:
        conn.close()

    rank = {"blunder": 3, "mistake": 2, "inaccuracy": 1}
    collected.sort(key=lambda p: (-rank.get(p["severity"], 0), -p["cp_loss"], -p.get("impact", 0)))
    unique = []
    seen_positions = set()
    epd_key = getattr(core, "epd_key", lambda fen: " ".join(fen.split()[:4]))
    for puzzle in collected:
        key = epd_key(puzzle["fen"])
        if key in seen_positions:
            continue
        seen_positions.add(key)
        puzzle.pop("impact", None)
        puzzle["puzzle_id"] = len(unique) + 1
        unique.append(puzzle)
        if len(unique) >= MAX_PUZZLES:
            break
    return {
        "ok": True, "player": display_player, "games_matched": len(matches),
        "games_analyzed": games_analyzed, "puzzles": unique,
        "warnings": replay_warnings[:5],
    }


def _body_multipart(self) -> dict:
    content_type = self.headers.get("Content-Type", "")
    if "multipart/form-data" not in content_type.lower():
        return {}
    try:
        length = int(self.headers.get("Content-Length") or 0)
    except ValueError:
        length = 0
    if length <= 0:
        return {}
    if length > MAX_UPLOAD_BYTES:
        raise ValueError("PGN upload is too large (maximum 12 MB).")
    raw = self.rfile.read(length)
    message = BytesParser(policy=email_policy).parsebytes(
        (f"Content-Type: {content_type}\r\nMIME-Version: 1.0\r\n\r\n").encode("ascii") + raw
    )
    fields = {}
    if not message.is_multipart():
        return fields
    for part in message.iter_parts():
        name = part.get_param("name", header="content-disposition")
        if not name:
            continue
        payload = part.get_payload(decode=True) or b""
        fields[name] = payload.decode(part.get_content_charset() or "utf-8", errors="replace")
    return fields


def _handle_generate(self, core) -> None:
    content_type = self.headers.get("Content-Type", "").lower()
    if content_type.startswith("application/json"):
        body = self._body_json()
    elif "multipart/form-data" in content_type:
        body = self._body_multipart()
    else:
        self._json({"error": "Use application/json or multipart/form-data for Puzzle Lab."}, 415)
        return
    try:
        result = generate_puzzles(core, str(body.get("pgn_text") or ""), str(body.get("player_name") or ""))
    except (ValueError, RuntimeError) as exc:
        self._json({"error": str(exc)}, 400)
        return
    self._json(result)


PUZZLE_CSS = r"""
.puzzle-form{display:grid;grid-template-columns:minmax(220px,.8fr) minmax(320px,1.5fr);gap:14px}
@media(max-width:800px){.puzzle-form{grid-template-columns:1fr}}
.puzzle-form label{display:flex;flex-direction:column;gap:6px;color:var(--dim)}
.puzzle-form input[type=file]{color:var(--text)}.puzzle-form textarea{min-height:180px;resize:vertical}
.puzzle-actions{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-top:12px}
.puzzle-shell{display:grid;grid-template-columns:minmax(300px,460px) minmax(280px,1fr);gap:18px;align-items:start}
@media(max-width:900px){.puzzle-shell{grid-template-columns:1fr}}
.puzzle-board{display:grid;grid-template-columns:repeat(8,minmax(34px,1fr));width:min(100%,460px);aspect-ratio:1;border:2px solid var(--line);border-radius:7px;overflow:hidden;box-shadow:var(--shadow-md)}
.puzzle-board span{position:relative;display:flex;align-items:center;justify-content:center;background-size:88%;background-position:center;background-repeat:no-repeat;user-select:none}
.puzzle-board span.puzzle-bad{box-shadow:inset 0 0 0 999px rgba(226,100,90,.4)}
.puzzle-board span.puzzle-bad-to{outline:4px solid rgba(226,100,90,.92);outline-offset:-4px}
.puzzle-board span.puzzle-best{box-shadow:inset 0 0 0 999px rgba(78,199,122,.4)}
.puzzle-board span.puzzle-best-to{outline:4px solid rgba(78,199,122,.95);outline-offset:-4px}
.puzzle-head{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-bottom:10px}
.puzzle-badge{display:inline-flex;align-items:center;gap:5px;border-radius:999px;padding:4px 10px;font-size:12px;font-weight:700;text-transform:capitalize}
.puzzle-badge.inaccuracy{background:#4a421d;color:#ffe36e}.puzzle-badge.mistake{background:#4a2f1d;color:#ffad62}.puzzle-badge.blunder{background:#4a2020;color:#ff8078}
.puzzle-meta{display:grid;grid-template-columns:auto 1fr;gap:7px 12px;margin:12px 0}.puzzle-meta dt{color:var(--dim)}.puzzle-meta dd{margin:0;overflow-wrap:anywhere}
.puzzle-nav{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-top:14px}.puzzle-counter{color:var(--dim);margin-right:auto}.puzzle-eval{padding:9px 11px;border-radius:7px;background:var(--panel2);margin:10px 0}
"""

PUZZLE_PANEL = rf"""
  <div id="pg-puzzle" style="display:none">
    <div class="card"><h2>Puzzle Lab</h2>
      <p class="muted">Upload or paste PGN games, identify the player, and turn their engine-detected errors into up to 10 review positions.</p>
      <div class="puzzle-form"><div>
        <label>PGN file<input id="puzzleFile" type="file" accept=".pgn,application/x-chess-pgn,text/plain"></label>
        <label style="margin-top:12px">Player name in PGN headers<input id="puzzlePlayer" type="text" value="{DEFAULT_PLAYER_NAME}" placeholder="Lin Yi Christopher"></label>
        <p class="muted small">The upload is analyzed in memory. It is not saved to disk and generated puzzles are not added to the database.</p>
      </div><label>Or paste raw PGN<textarea id="puzzlePgn" placeholder='[Event "..."]&#10;[White "Lin Yi Christopher"]&#10;[Black "Opponent"]&#10;&#10;1. e4 ...'></textarea></label></div>
      <div class="puzzle-actions"><button id="puzzleGenerate" class="primary" onclick="puzzleGenerate()">Generate Puzzles</button><span id="puzzleStatus" class="muted"></span></div>
    </div><div id="puzzleResults"></div>
  </div>
"""

PUZZLE_JS = r"""
const PUZZLE={items:[],index:0,reveal:false,busy:false};
function puzzleEnsureReady(){const s=document.getElementById('puzzleStatus');if(s&&STATE&&STATE.engine&&!STATE.engine.available)s.textContent='Stockfish is not configured. Set PREP_STOCKFISH or add ./stockfish/.';}
async function puzzleGenerate(){
 if(PUZZLE.busy)return;const player=(document.getElementById('puzzlePlayer').value||'').trim(),file=document.getElementById('puzzleFile').files[0],pasted=document.getElementById('puzzlePgn').value||'',status=document.getElementById('puzzleStatus'),btn=document.getElementById('puzzleGenerate');
 if(!player){toast('Enter the player name from the PGN headers.','error');return}if(!file&&!pasted.trim()){toast('Choose a PGN file or paste PGN text.','error');return}
 PUZZLE.busy=true;btn.disabled=true;status.innerHTML='<span class="spinner"></span>Analyzing games at depth 12…';document.getElementById('puzzleResults').innerHTML='';
 try{let opts;if(file){const f=new FormData();f.append('pgn_text',file,file.name);f.append('player_name',player);opts={method:'POST',body:f}}else opts={method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({pgn_text:pasted,player_name:player})};
  const data=await api('/api/puzzle/generate',opts);PUZZLE.items=data.puzzles||[];PUZZLE.index=0;PUZZLE.reveal=false;status.textContent='Analyzed '+data.games_analyzed+' of '+data.games_matched+' matched game(s); generated '+PUZZLE.items.length+' puzzle(s).';
  if(!PUZZLE.items.length)document.getElementById('puzzleResults').innerHTML='<div class="card"><p>No moves crossed the 50 cp inaccuracy threshold in the analyzed range.</p></div>';else puzzleRender();
  if(data.warnings&&data.warnings.length)toast('Some PGN moves could not be replayed; valid games were still used.');
 }catch(e){status.textContent='';document.getElementById('puzzleResults').innerHTML='<div class="card"><p class="score-lo">'+esc(e.message)+'</p></div>';toast('Puzzle generation failed: '+e.message,'error')}finally{PUZZLE.busy=false;btn.disabled=false}}
function puzzleSeverityLabel(s){return s==='blunder'?'🔴 Blunder':(s==='mistake'?'🟠 Mistake':'🟡 Inaccuracy')}
function puzzleMoveSquares(u){return(u&&u.length>=4)?{from:u.slice(0,2),to:u.slice(2,4)}:{from:'',to:''}}
function puzzleBoardHtml(p){const board=(p.fen||'').split(' ')[0],rows=board.split('/'),grid=[];for(const row of rows){const rank=[];for(const ch of row){if(/\d/.test(ch))for(let k=0;k<+ch;k++)rank.push('');else rank.push(ch)}grid.push(rank)}const order=[...Array(8).keys()],rIdx=p.player_color==='black'?[...order].reverse():order,cIdx=p.player_color==='black'?[...order].reverse():order,bad=puzzleMoveSquares(p.player_move_uci),best=puzzleMoveSquares(p.best_move_uci);let cells='';for(const ri of rIdx)for(const ci of cIdx){const sq=FILES_STR_JS[ci]+(8-ri),cls=[(ri+ci)%2?'sqD':'sqL'];if(sq===bad.from||sq===bad.to)cls.push('puzzle-bad');if(sq===bad.to)cls.push('puzzle-bad-to');if(PUZZLE.reveal&&(sq===best.from||sq===best.to))cls.push('puzzle-best');if(PUZZLE.reveal&&sq===best.to)cls.push('puzzle-best-to');cells+='<span class="'+cls.join(' ')+'"'+pieceStyle(grid[ri][ci])+'>'+coordLabels(ri,ci,rIdx,cIdx)+'</span>'}return cells}
function puzzleRender(){const p=PUZZLE.items[PUZZLE.index];if(!p)return;const c=p.game_context||{},dots=p.player_color==='white'?'.':'…',reveal=PUZZLE.reveal,evalHtml=reveal?'<div class="puzzle-eval"><b>Engine best:</b> '+esc(p.best_move||p.best_move_uci||'—')+'<br><b>Evaluation swing:</b> '+esc(p.eval_before)+' → '+esc(p.eval_after)+'</div>':'';document.getElementById('puzzleResults').innerHTML='<div class="card"><div class="puzzle-head"><h2 style="margin:0;border:0;padding:0">Puzzle '+p.puzzle_id+'</h2><span class="puzzle-badge '+esc(p.severity)+'">'+puzzleSeverityLabel(p.severity)+'</span></div><div class="puzzle-shell"><div class="puzzle-board">'+puzzleBoardHtml(p)+'</div><div><p><b>'+p.move_number+dots+esc(p.player_move)+'</b> lost <b>'+p.cp_loss+' cp</b>.</p>'+evalHtml+'<dl class="puzzle-meta"><dt>White</dt><dd>'+esc(c.white)+'</dd><dt>Black</dt><dd>'+esc(c.black)+'</dd><dt>Result</dt><dd>'+esc(c.result)+'</dd><dt>Event</dt><dd>'+esc(c.event||'—')+'</dd><dt>Round</dt><dd>'+esc(c.round||'—')+'</dd><dt>FEN</dt><dd><code>'+esc(p.fen)+'</code></dd></dl><button onclick="puzzleToggleBest()">'+(reveal?'Hide Best Move':'Show Best Move')+'</button><div class="puzzle-nav"><span class="puzzle-counter">Puzzle '+(PUZZLE.index+1)+' of '+PUZZLE.items.length+'</span><button onclick="puzzlePrev()" '+(PUZZLE.index===0?'disabled':'')+'>Previous</button><button onclick="puzzleNext()" '+(PUZZLE.index===PUZZLE.items.length-1?'disabled':'')+'>Next</button></div></div></div></div>'}
function puzzleToggleBest(){PUZZLE.reveal=!PUZZLE.reveal;puzzleRender()}function puzzlePrev(){if(PUZZLE.index>0){PUZZLE.index--;PUZZLE.reveal=false;puzzleRender()}}function puzzleNext(){if(PUZZLE.index<PUZZLE.items.length-1){PUZZLE.index++;PUZZLE.reveal=false;puzzleRender()}}
"""


def _inject_ui(html: str) -> str:
    if 'id="tb-puzzle"' in html:
        return html
    html = html.replace("</style>", PUZZLE_CSS + "\n</style>", 1)
    html = html.replace(
        '  <button id="tb-export" onclick="tab(\'export\')">Export</button>',
        '  <button id="tb-puzzle" onclick="tab(\'puzzle\')">Puzzle Lab</button>\n  <button id="tb-export" onclick="tab(\'export\')">Export</button>', 1)
    html = html.replace('  <div id="pg-export" style="display:none"></div>', PUZZLE_PANEL + '\n  <div id="pg-export" style="display:none"></div>', 1)
    html = html.replace("for(const t of ['overview','schedule','opponents','play','dino','files','export'])", "for(const t of ['overview','schedule','opponents','play','dino','files','puzzle','export'])", 1)
    html = html.replace("  if(name==='play') loadPlay();", "  if(name==='play') loadPlay();\n  if(name==='puzzle') puzzleEnsureReady();", 1)
    html = html.replace("\nrefresh();\n</script>", "\n" + PUZZLE_JS + "\nrefresh();\n</script>", 1)
    return html


def install(core) -> None:
    core.Handler._body_multipart = _body_multipart
    original_do_post = core.Handler.do_POST
    def do_post(self):
        if urlparse(self.path).path == "/api/puzzle/generate":
            try:
                _handle_generate(self, core)
            except Exception as exc:
                self._json({"error": str(exc)}, 500)
            return
        return original_do_post(self)
    core.Handler.do_POST = do_post
    core.HTML_PAGE = _inject_ui(core.HTML_PAGE)
