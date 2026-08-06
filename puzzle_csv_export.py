#!/usr/bin/env python3
"""Browser-side CSV export extension for the Puzzle Lab UI."""

from __future__ import annotations


CSV_BUTTON = (
    '<button id="puzzleExportCsv" type="button" '
    'onclick="puzzleExportCsv()" disabled>Export CSV</button>'
)

CSV_JS = r"""
function puzzleCsvEscape(value){
  const text=value===null||value===undefined?'':String(value);
  return '"'+text.replace(/"/g,'""')+'"';
}
function puzzleCsvFilename(){
  const input=document.getElementById('puzzlePlayer');
  const raw=(input&&input.value?input.value:'puzzles').trim().toLowerCase();
  const stem=(raw.normalize?raw.normalize('NFKD'):raw)
    .replace(/[^a-z0-9]+/g,'-').replace(/^-+|-+$/g,'')||'puzzles';
  return stem+'-puzzles-'+new Date().toISOString().slice(0,10)+'.csv';
}
function puzzleCsvRows(items){
  const playerInput=document.getElementById('puzzlePlayer');
  const player=playerInput&&playerInput.value?playerInput.value.trim():'';
  const columns=[
    ['puzzle_id',p=>p.puzzle_id],
    ['player',()=>player],
    ['player_color',p=>p.player_color],
    ['fen',p=>p.fen],
    ['player_move',p=>p.player_move],
    ['player_move_uci',p=>p.player_move_uci],
    ['best_move',p=>p.best_move],
    ['best_move_uci',p=>p.best_move_uci],
    ['cp_loss',p=>p.cp_loss],
    ['severity',p=>p.severity],
    ['eval_before',p=>p.eval_before],
    ['eval_after',p=>p.eval_after],
    ['move_number',p=>p.move_number],
    ['white',p=>(p.game_context||{}).white],
    ['black',p=>(p.game_context||{}).black],
    ['opponent',p=>(p.game_context||{}).opponent],
    ['result',p=>(p.game_context||{}).result],
    ['event',p=>(p.game_context||{}).event],
    ['round',p=>(p.game_context||{}).round]
  ];
  const rows=[columns.map(column=>puzzleCsvEscape(column[0])).join(',')];
  for(const puzzle of items){
    rows.push(columns.map(column=>puzzleCsvEscape(column[1](puzzle))).join(','));
  }
  return rows;
}
function puzzleExportCsv(){
  const items=typeof PUZZLE!=='undefined'&&Array.isArray(PUZZLE.items)?PUZZLE.items:[];
  if(!items.length){
    if(typeof toast==='function')toast('Generate puzzles before exporting CSV.','error');
    return;
  }
  const csv='\uFEFF'+puzzleCsvRows(items).join('\r\n')+'\r\n';
  const blob=new Blob([csv],{type:'text/csv;charset=utf-8'});
  const url=URL.createObjectURL(blob);
  const link=document.createElement('a');
  link.href=url;
  link.download=puzzleCsvFilename();
  document.body.appendChild(link);
  link.click();
  link.remove();
  setTimeout(()=>URL.revokeObjectURL(url),0);
  if(typeof toast==='function')toast('Exported '+items.length+' puzzle(s) as CSV.','success');
}
function puzzleCsvSyncButton(){
  const button=document.getElementById('puzzleExportCsv');
  if(button)button.disabled=!(typeof PUZZLE!=='undefined'&&Array.isArray(PUZZLE.items)&&PUZZLE.items.length);
}
window.addEventListener('DOMContentLoaded',()=>{
  puzzleCsvSyncButton();
  const results=document.getElementById('puzzleResults');
  if(results)new MutationObserver(puzzleCsvSyncButton).observe(results,{childList:true,subtree:true});
});
"""


def _inject_csv_export(html: str) -> str:
    """Add the export control and browser-side serializer once."""
    if 'id="puzzleExportCsv"' in html:
        return html
    status_marker = '<span id="puzzleStatus"'
    if status_marker not in html:
        raise RuntimeError("Puzzle Lab status control was not found in the generated HTML.")
    html = html.replace(status_marker, CSV_BUTTON + status_marker, 1)
    script = f"\n<script>\n{CSV_JS}\n</script>\n"
    if "</body>" in html:
        return html.replace("</body>", script + "</body>", 1)
    return html + script


def install(core) -> None:
    """Install CSV export after puzzle_lab.install(core)."""
    core.HTML_PAGE = _inject_csv_export(core.HTML_PAGE)
