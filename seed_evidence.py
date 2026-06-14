#!/usr/bin/env python
"""One-shot per-seed evidence pack for the report workflow.

Usage:
    python seed_evidence.py <player_id> [--depth 12]

Prints, in one pass, every result-only and engine field the curated report needs, so the
scattered ad-hoc queries in seed_analysis_report_workflow.md no longer have to be re-typed and
re-adapted per seed. Read-only: it never writes to prep_manual.db, so it is safe to run while an
--analyze pass for a *different* player is in flight (SQLite busy_timeout handles the brief reads).

Designed around the real schema in this workspace:
  Roster(player_id, real_name, title, federation, fide, is_hero)
  Games(game_id, file_id, player_id, color, presult, white, black, result, date, event, round,
        eco, opening, total_moves, moves_json, source, lichess_id, dedup_hash)   # no time_control col
  GameAnalysis(dedup_hash, depth, engine, analyzed_at, acpl_white, acpl_black,
               moves_white, moves_black, phase_json, blunders_json)
  Tags(game_id, family)

Verdict rule (from the fifth/seventh-seed patches): base accuracy/structure on the CLASSICAL subset;
all-games numbers are shown only to expose online/rapid inflation. "0 Lichess online" does NOT mean
classical-only — Titled Tuesday / rapid events live inside the ChessBase PGNs, so always split by the
event regex below, regardless of the Lichess count.
"""
import sqlite3, json, re, sys, argparse
from collections import defaultdict

ONLINE_RE = re.compile(r'titled tuesday|blitz|rapid|online|lichess|chess\.com|bullet|arena', re.I)
def is_online(ev): return bool(ONLINE_RE.search(ev or ""))
def score(w, d, l):
    n = w + d + l
    return 100.0 * (w + 0.5 * d) / n if n else 0.0
def norm_name(s):  # normalise "Ghosh, Aronyak" / "Aronyak,Ghosh" for duplicate detection
    return "".join(sorted(re.sub(r'[^a-z]', '', (s or "").lower())))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("player_id", type=int)
    ap.add_argument("--depth", type=int, default=12)
    ap.add_argument("--db", default="prep_manual.db")
    ap.add_argument("--recent-since", default="2023",
                    help="games dated >= this year are 'recent' (default 2023); also flags pre-2010 junior games")
    a = ap.parse_args()
    P, D = a.player_id, a.depth
    conn = sqlite3.connect(a.db); conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    who = cur.execute("select player_id, real_name, title, federation, fide from Roster where player_id=?",
                      (P,)).fetchone()
    if not who:
        print(f"!! no Roster row for player_id={P}"); return
    print(f"=== {who['real_name']}  ({who['title']} {who['federation']} {who['fide']})  player_id={P}  depth={D} ===")

    rows = cur.execute("""select color, presult, event, eco, opening, date, round,
                                 white, black, total_moves, dedup_hash, game_id
                          from Games where player_id=?""", (P,)).fetchall()
    otb = [r for r in rows if (r["event"] or "") or True]  # all OTB+lichess rows for this player
    classical = [r for r in rows if not is_online(r["event"])]
    online = [r for r in rows if is_online(r["event"])]

    # ---- 1. coverage ----
    ana = cur.execute("""select count(*) from GameAnalysis ga join Games g on g.dedup_hash=ga.dedup_hash
                         where g.player_id=? and ga.depth=?""", (P, D)).fetchone()[0]
    otb_n = cur.execute("select count(*) from Games where player_id=? and (source is null or source not like '%lichess%')",
                        (P,)).fetchone()[0]
    print(f"\n[1] COVERAGE: total={len(rows)}  OTB={otb_n}  analysed@{D}={ana}  "
          f"pending={otb_n-ana}  -> {'RUN ANALYSIS' if ana < otb_n else 'ok'}")
    print("    depth distribution:", dict(cur.execute(
        """select ga.depth, count(*) from GameAnalysis ga join Games g on g.dedup_hash=ga.dedup_hash
           where g.player_id=? group by ga.depth""", (P,)).fetchall()))

    # ---- 2. time-control split ----
    print(f"\n[2] TIME-CONTROL SPLIT: classical={len(classical)}  online/rapid={len(online)}")
    ev = defaultdict(int)
    for r in online: ev[r["event"]] += 1
    for e, c in sorted(ev.items(), key=lambda x: -x[1]):
        print(f"      online {c:3}  {e}")

    # ---- 3. recency ----
    by_year = defaultdict(int)
    for r in rows: by_year[(r["date"] or "")[:4] or "?"] += 1
    pre2010 = [r for r in rows if (r["date"] or "") < "2010"]
    recent = [r for r in classical if (r["date"] or "") >= a.recent_since]
    print(f"\n[3] RECENCY: span {min((r['date'] or '' for r in rows), default='?')} -> "
          f"{max((r['date'] or '' for r in rows), default='?')}  |  pre-2010 junior-era={len(pre2010)}  |  "
          f"classical since {a.recent_since}={len(recent)}")
    print("      by year:", {y: by_year[y] for y in sorted(by_year)})

    # ---- 4. records ----
    def rec(subset):
        agg = {"white": [0,0,0], "black": [0,0,0], "both": [0,0,0]}
        for r in subset:
            i = 0 if r["presult"]=="win" else 1 if r["presult"]=="draw" else 2
            agg[r["color"]][i] += 1; agg["both"][i] += 1
        return agg
    for label, sub in (("all", rows), ("classical", classical)):
        g = rec(sub); b, w, bl = g["both"], g["white"], g["black"]
        print(f"\n[4] RECORD ({label}): {b[0]}W {b[1]}D {b[2]}L ({score(*b):.1f}%)/{sum(b)} | "
              f"White {w[0]}-{w[1]}-{w[2]} ({score(*w):.1f}%/{sum(w)}) | "
              f"Black {bl[0]}-{bl[1]}-{bl[2]} ({score(*bl):.1f}%/{sum(bl)})")

    # ---- 5. opening tables by color (classical, >=2g) ----
    for color in ("white", "black"):
        op = defaultdict(lambda: [0,0,0])
        for r in classical:
            if r["color"] != color: continue
            op[(r["opening"] or "?", r["eco"] or "?")][0 if r["presult"]=="win" else 1 if r["presult"]=="draw" else 2] += 1
        print(f"\n[5] OPENINGS as {color.upper()} (classical, >=2g):")
        for (o, eco), wdl in sorted(op.items(), key=lambda x: -sum(x[1])):
            if sum(wdl) >= 2:
                print(f"      {sum(wdl):2}g {wdl[0]}-{wdl[1]}-{wdl[2]} {score(*wdl):5.1f}%  {eco:4} {o}")

    # ---- 6/7/8. engine-dependent (classical) ----
    arows = cur.execute("""select g.game_id, g.color, g.presult, g.event, g.date, g.white, g.black,
                                  g.eco, g.opening, ga.phase_json, ga.blunders_json
                           from GameAnalysis ga join Games g on g.dedup_hash=ga.dedup_hash
                           where g.player_id=? and ga.depth=?""", (P, D)).fetchall()
    fam_tags = defaultdict(list)  # a game can carry several structure families; count it in each (dossier convention)
    for r in cur.execute("select t.game_id, t.family from Tags t join Games g on g.game_id=t.game_id where g.player_id=?", (P,)):
        fam_tags[r["game_id"]].append(r["family"])

    def phase_split(subset_pred):
        a_ = {"g":0,"w":0,"d":0,"l":0,"op":[0.0,0],"mid":[0.0,0],"end":[0.0,0],"b":0,"m":0}
        for r in arows:
            if not subset_pred(r): continue
            a_["g"]+=1; a_["w"]+=r["presult"]=="win"; a_["d"]+=r["presult"]=="draw"; a_["l"]+=r["presult"]=="loss"
            s = (json.loads(r["phase_json"]) if r["phase_json"] else {}).get(r["color"], {})
            for ph in ("op","mid","end"):
                a_[ph][0]+=s.get(ph,[0,0])[0]; a_[ph][1]+=s.get(ph,[0,0])[1]
            for x in (json.loads(r["blunders_json"]) if r["blunders_json"] else []):
                if x.get("mover")==r["color"]:
                    if x["sev"]=="blunder": a_["b"]+=1
                    elif x["sev"]=="mistake": a_["m"]+=1
        return a_
    def acpl(a_, ph): return a_[ph][0]/a_[ph][1] if a_[ph][1] else 0
    def overall(a_):
        cp=sum(a_[p][0] for p in("op","mid","end")); mv=sum(a_[p][1] for p in("op","mid","end"))
        return cp/mv if mv else 0
    print(f"\n[6] PHASE ACCURACY (analysed@{D}):")
    for label, pred in (("classical", lambda r: not is_online(r["event"])),
                        ("online   ", lambda r: is_online(r["event"]))):
        a_ = phase_split(pred)
        if a_["g"]:
            print(f"      {label} {a_['g']:3}g ({a_['w']}-{a_['d']}-{a_['l']}, {score(a_['w'],a_['d'],a_['l']):.1f}%) | "
                  f"overall {overall(a_):.1f} (op {acpl(a_,'op'):.1f}, mid {acpl(a_,'mid'):.1f}, end {acpl(a_,'end'):.1f}) "
                  f"| {a_['b']}b {a_['m']}m")

    fam = {}
    for r in arows:
        if is_online(r["event"]): continue
        families = fam_tags.get(r["game_id"], [])
        if not families: continue
        s = (json.loads(r["phase_json"]) if r["phase_json"] else {}).get(r["color"], {})
        bj = json.loads(r["blunders_json"]) if r["blunders_json"] else []
        nb = sum(1 for x in bj if x.get("mover")==r["color"] and x["sev"]=="blunder")
        nm = sum(1 for x in bj if x.get("mover")==r["color"] and x["sev"]=="mistake")
        for family in families:
            d = fam.setdefault((family, r["color"]), {"g":0,"w":0,"d":0,"l":0,"cp":0.0,"mv":0,"b":0,"m":0})
            d["g"]+=1; d["w"]+=r["presult"]=="win"; d["d"]+=r["presult"]=="draw"; d["l"]+=r["presult"]=="loss"
            for ph in ("op","mid","end"): d["cp"]+=s.get(ph,[0,0])[0]; d["mv"]+=s.get(ph,[0,0])[1]
            d["b"]+=nb; d["m"]+=nm
    print(f"\n[7] STRUCTURE ACPL by family/color (classical):")
    for (family, color), d in sorted(fam.items(), key=lambda x: -x[1]["g"]):
        print(f"      {d['g']:2}g {d['w']}-{d['d']}-{d['l']} {score(d['w'],d['d'],d['l']):5.1f}% [{color:5}] "
              f"ACPL {(d['cp']/d['mv'] if d['mv'] else 0):5.1f} {d['b']}b/{d['m']}m  {family}")

    print(f"\n[8] LATE BLUNDERS (classical, move>=30), recent first:")
    samp = []
    for r in arows:
        if is_online(r["event"]): continue
        for x in (json.loads(r["blunders_json"]) if r["blunders_json"] else []):
            if x.get("mover")==r["color"] and x["sev"]=="blunder" and x.get("move_no",0)>=30:
                opp = r["black"] if r["color"]=="white" else r["white"]
                samp.append((r["date"], opp, r["color"], x["move_no"], x["san"], x.get("best"),
                             x.get("loss"), r["opening"], r["eco"]))
    for s in sorted(samp, key=lambda r: r[0] or "", reverse=True)[:12]:
        print(f"      {s[0]} vs {s[1]:24} as {s[2]:5} mv{s[3]} {s[4]:7} (best {s[5]}, loss {s[6]})  {s[7]} ({s[8]})")

    # ---- 9. classical model losses, recent first ----
    print(f"\n[9] CLASSICAL LOSSES (model games), recent first:")
    for r in sorted([r for r in classical if r["presult"]=="loss"], key=lambda r: r["date"] or "", reverse=True):
        opp = r["black"] if r["color"]=="white" else r["white"]
        print(f"      {r['date']} {r['event']} ({r['round']}) as {r['color']} vs {opp}  {r['opening']} ({r['eco']}) in {r['total_moves']}")

    # ---- 10. duplicate-candidate detection ----
    dups = defaultdict(list)
    for r in rows:
        opp = r["black"] if r["color"]=="white" else r["white"]
        dups[(r["date"], norm_name(opp), r["total_moves"])].append(r)
    flagged = {k: v for k, v in dups.items() if len(v) > 1 and k[0]}
    print(f"\n[10] DUPLICATE-CANDIDATE games (same date+opponent+move-count, different dedup_hash): {len(flagged)}")
    for (date, _, tm), v in flagged.items():
        opp = v[0]["black"] if v[0]["color"]=="white" else v[0]["white"]
        print(f"      {date} vs {opp} ({tm} moves) x{len(v)}: events " + " | ".join(sorted({x['event'] or '?' for x in v})))

if __name__ == "__main__":
    main()
