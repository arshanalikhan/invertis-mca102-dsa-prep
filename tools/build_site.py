"""Build the static site from content/ and src/ into site/.

Usage:  python tools/build_site.py            (add --draft to skip the content checks while writing)

Pages: index.html (home), analysis.html (past-paper analysis), papers.html (every past question),
unit-1.html … unit-6.html (notes), guide.html (answer-writing guide).
site/ is generated: edit content/, src/ or this script instead.
"""
import hashlib
import html
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content as C   # noqa: E402
import mdlite         # noqa: E402
import pyqdata as P   # noqa: E402

ROOT = P.ROOT
SRC, OUT = os.path.join(ROOT, "src"), os.path.join(ROOT, "site")
REPO = "https://github.com/arshanalikhan/invertis-mca102-dsa-prep"
SITE_URL = "https://arshanalikhan.github.io/invertis-mca102-dsa-prep/"
ROMAN = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI"}
SEC_LABEL = {"A": "Section A", "B": "Section B", "C": "Section C"}
esc = lambda s: html.escape(str(s), quote=True)


# ------------------------------------------------------------------ data
class Data:
    def __init__(self):
        self.topics = P.load_topics()
        self.papers = P.load_papers()
        self.stats = P.stats(self.papers, self.topics)
        self.units = C.load_units()
        self.mocks = []
        self.entries = {e["id"]: e for u in self.units for e in u["entries"]}
        self.main = [p for p in self.papers if p["kind"] == "main"]
        self.latest = self.papers[0]
        latest_tags = {t for q in self.latest["qs"] for t in q["tags"]}
        self.in_latest = latest_tags
        by_topic = {}
        for e in self.entries.values():
            for t in e["topics"]:
                by_topic.setdefault(t, []).append(e)
        self.by_topic = by_topic

    def chance(self, entry):
        return max(self.stats[t]["chance"] for t in entry["topics"])

    def asked(self, entry):
        """Past questions on this entry's topics, newest first; short answers list Section A first."""
        out = []
        for p in self.papers:
            for q in p["qs"]:
                if set(q["tags"]) & set(entry["topics"]):
                    out.append((p, q))
        first = "A" if entry["kind"] == "short" else "BC"
        out.sort(key=lambda pq: (pq[1]["sec"] not in first, pq[0]["kind"] != "main"))
        return out

    def answers_for(self, q):
        """Best answers in the notes for a past question: short for Section A, long/problem for B and C."""
        found = []
        for t in q["tags"]:
            for e in self.by_topic.get(t, []):
                if e not in found:
                    found.append(e)
        want = ("short",) if q["sec"] == "A" else ("long", "problem")
        pref = [e for e in found if e["kind"] in want] or found
        return pref[:2]


def main_count(tid):
    """Number of main (CSE AI) papers that asked the topic."""
    ids = {P.paper_id(p) for p in DATA.main}
    return sum(1 for pid in DATA.stats[tid]["papers"] if pid in ids)


def qref(p, q):
    return f"q-{p['session']}-{p['code']}-{q['qno']}"


def qlabel(p, q):
    return f"{p['session']} {p['code']} Q{q['qno']}"


def band_class(ch):
    return {"Very high": "vh", "High": "hi", "Medium": "md", "Low": "lo"}[P.band(ch)]


def pages_estimate(e):
    md = e["md"]
    rows = sum(1 for ln in md.split("\n") if ln.strip().startswith("|"))
    pages = e["words"] / 190 + 0.35 * e["figs"] + 0.02 * rows
    return max(1.0, round(pages * 2) / 2)


def page_label(x):
    whole, half = int(x), x - int(x) >= 0.5
    return f"{whole}½" if half else f"{whole}"


# ------------------------------------------------------------------ page shell
NAV = [("index.html", "Home", "home"), ("analysis.html", "PYQ analysis", "chart"), ("papers.html", "Past papers", "file"),
       None,
       *[(f"unit-{n}.html", f"Unit {ROMAN[n]}", f"u{n}") for n in range(1, 7)],
       None,
       ("guide.html", "Answer-writing guide", "pen")]
ICONS = {
    "home": '<path d="M3 11l9-7 9 7v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/>',
    "chart": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    "file": '<path d="M14 3H6a1 1 0 0 0-1 1v16a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>',
    "check": '<path d="M9 12l2 2 4-4"/><rect x="4" y="3" width="16" height="18" rx="2"/>',
    "clock": '<circle cx="12" cy="13" r="8"/><path d="M12 9v4l2.5 2.5M9 2h6"/>',
    "pen": '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/>',
    "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
    "theme": '<path d="M12 3a9 9 0 1 0 9 9 7 7 0 0 1-9-9z"/>',
    "star": '<path d="M12 3l2.8 5.7 6.2.9-4.5 4.4 1 6.2L12 17.3 6.5 20.2l1-6.2L3 9.6l6.2-.9z"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
}


def icon(name):
    if name[0] == "u" and name[1:].isdigit():
        return f'<span class="ubadge">{ROMAN[int(name[1])]}</span>'
    return f'<svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'


def shell(slug, title, body, desc, css_url, js_url, wide=False):
    nav = []
    for item in NAV:
        if item is None:
            nav.append('<hr>')
            continue
        href, label, ic = item
        on = ' class="on" aria-current="page"' if href == slug else ""
        nav.append(f'<a href="{href}"{on}>{icon(ic)}<span>{label}</span></a>')
    nav = "".join(nav)
    full_title = "MCA102 DSA Prep" if slug == "index.html" else f"{title} · MCA102 DSA Prep"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{SITE_URL}{'' if slug == 'index.html' else slug}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="MCA102 DSA Prep">
<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{SITE_URL}{'' if slug == 'index.html' else slug}">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#f3f5f9" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0b0f17" media="(prefers-color-scheme: dark)">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 32 32%27%3E%3Crect width=%2732%27 height=%2732%27 rx=%277%27 fill=%27%231f4fa3%27/%3E%3Ccircle cx=%2710%27 cy=%2711%27 r=%273%27 fill=%27%23fff%27/%3E%3Ccircle cx=%2722%27 cy=%2711%27 r=%273%27 fill=%27%23fff%27/%3E%3Ccircle cx=%2716%27 cy=%2722%27 r=%273%27 fill=%27%23fff%27/%3E%3Cpath d=%27M10 11L16 22L22 11%27 stroke=%27%23fff%27 stroke-width=%271.6%27 fill=%27none%27/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans+Condensed:wght@500;600;700&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap">
<link rel="stylesheet" href="{css_url}">
<script>try {{ var t0 = localStorage.getItem("mca102-theme"); if (t0 === "light" || t0 === "dark") document.documentElement.setAttribute("data-theme", t0); }} catch (e) {{}}</script>
</head>
<body data-page="{slug[:-5]}">
<a class="skip" href="#main">Skip to content</a>
<aside class="sidebar" id="sidebar" aria-label="Pages">
  <a class="brand" href="index.html"><span class="logo" aria-hidden="true">DS</span><span>MCA102 DSA Prep<small>Invertis University · MCA · Sem I</small></span></a>
  <nav class="side-nav">{nav}</nav>
  <div class="side-foot">
    <a class="side-star" href="{REPO}" target="_blank" rel="noopener">{icon('star')}<span>Star on GitHub</span></a>
    <button class="themebtn" type="button">{icon('theme')}<span>Theme: system</span></button>
  </div>
</aside>
<div class="scrim" id="scrim" hidden></div>
<header class="topbar">
  <button class="menubtn" id="menuBtn" type="button" aria-label="Open menu" aria-controls="sidebar" aria-expanded="false">{icon('menu')}</button>
  <a class="brand" href="index.html"><span class="logo" aria-hidden="true">DS</span><span>MCA102 DSA Prep</span></a>
  <button class="themebtn icon-only" type="button" aria-label="Switch theme">{icon('theme')}</button>
</header>
<main id="main" class="{'wide' if wide else ''}">
{body}
</main>
<footer class="foot"><div class="wrap">
  <p>Built by <a href="https://github.com/arshanalikhan" target="_blank" rel="noopener">Arshan Ali Khan</a> from the Invertis University MCA102 syllabus (MCA 2025-27 and 2026-28) and {len(DATA.main)} past AKTU MCA Data Structures papers. Not an official Invertis or AKTU resource: if anything here disagrees with your teacher or textbook, follow them. Revision progress is saved only in this browser.</p>
  <a class="btn" href="{REPO}" target="_blank" rel="noopener">{icon('star')} Star on GitHub</a>
</div></footer>
<button class="totop" id="totop" type="button" aria-label="Back to top">{icon('up')}</button>
<div class="tooltip" id="tip" role="tooltip" hidden></div>
<script src="{js_url}"></script>
</body>
</html>
"""


# ------------------------------------------------------------------ components
def entry_html(e, with_meta=True, anchor=True):
    ch = DATA.chance(e)
    marks = "2 marks" if e["kind"] == "short" else "7 marks · problem" if e["kind"] == "problem" else "7 marks"
    meta = ""
    if with_meta:
        bits = [f'<span class="pill">{marks}</span>',
                f'<span class="chance {band_class(ch)}" data-tip="Recency-weighted share of past MCA data structures papers that asked this topic">{P.band(ch)} chance</span>']
        if set(e["topics"]) & DATA.in_latest:
            bits.append('<span class="pill new" data-tip="This topic was asked in the latest paper (2024-25)">In 2024-25 paper</span>')
        if e["kind"] != "short":
            pg = pages_estimate(e)
            bits.append(f'<span class="pill ghost" data-tip="Rough length when handwritten in an answer booklet">≈ {page_label(pg)} pages · {e["figs"]} diagram{"s" if e["figs"] != 1 else ""}</span>')
        asked = DATA.asked(e)
        links = "".join(f'<a href="papers.html#{qref(p, q)}" data-tip="{esc(q["text"][:140])}">{esc(qlabel(p, q))}</a>' for p, q in asked[:6])
        more = f'<span class="more">+{len(asked) - 6} more</span>' if len(asked) > 6 else ""
        asked_html = f'<div class="asked"><span>Topic asked in</span>{links}{more}</div>' if asked else '<div class="asked"><span>Not asked in the papers analysed yet</span></div>'
        meta = f'<div class="qmeta">{"".join(bits)}</div>'
    else:
        asked_html = ""
    idattr = f' id="{e["id"]}"' if anchor else ""
    done = "" if not with_meta or e["kind"] == "short" else f'<button class="donebtn" type="button" data-done="{e["id"]}" aria-pressed="false">Mark as revised</button>'
    cls = "qa " + e["kind"]
    return (f'<article class="{cls}"{idattr}>{meta}<h3 class="q"><a class="qlink" href="unit-{e["unit"]}.html#{e["id"]}">Q.</a> {esc(e["q"])}</h3>'
            f'{asked_html}<div class="ans">{e["html"]}</div>{done}</article>')


def unit_page(u):
    longs = [e for e in u["entries"] if e["kind"] == "long"]
    probs = [e for e in u["entries"] if e["kind"] == "problem"]
    shorts = [e for e in u["entries"] if e["kind"] == "short"]
    topics = sorted([t for t in DATA.topics.values() if t["unit"] == u["n"]], key=lambda t: -DATA.stats[t["id"]]["chance"])
    radar = []
    for t in topics:
        s = DATA.stats[t["id"]]
        first = next((e for e in DATA.by_topic.get(t["id"], []) if e["kind"] != "short"), None)
        link = f'<a href="#{first["id"]}">Answer</a>' if first else ""
        new = ' <span class="pill new sm">2024-25</span>' if t["id"] in DATA.in_latest else ""
        radar.append(f'<tr><td>{esc(t["name"])}{new}</td>'
                     f'<td class="num">{main_count(t["id"])}/{len(DATA.main)}</td><td><span class="chance {band_class(s["chance"])}">{P.band(s["chance"])}</span></td><td>{link}</td></tr>')
    toc = "".join(f'<li><a href="#{e["id"]}">{esc(e["q"])}</a> <span class="chance dot {band_class(DATA.chance(e))}" title="{P.band(DATA.chance(e))} chance"></span><span class="tick" data-tick="{e["id"]}"></span></li>' for e in longs + probs)
    ids = ",".join(e["id"] for e in longs + probs)
    body = f"""
<div class="wrap page">
  <p class="eyebrow">Unit {ROMAN[u['n']]} · MCA102 Advanced Data Structure and Algorithms</p>
  <h1>{esc(u['title'])}</h1>
  <div class="syl"><b>Syllabus:</b> {esc(u['syllabus'])}</div>
  <div class="lede">{u['intro']}</div>
  <div class="unitprog" data-ids="{ids}"><div class="bar"><i></i></div><span class="lbl">0 of {len(longs) + len(probs)} long answers revised</span></div>
  <div class="grid2">
    <section class="card">
      <h2 class="h3">What the papers ask from this unit</h2>
      <p class="muted sm">Out of {len(DATA.main)} past MCA data structures papers (2016-17 to 2024-25). Chance weights recent papers more.</p>
      <div class="tbl"><table class="radar"><thead><tr><th>Topic</th><th>Papers</th><th>Chance</th><th></th></tr></thead><tbody>{''.join(radar)}</tbody></table></div>
    </section>
    <section class="card">
      <h2 class="h3">Long answers in this unit</h2>
      <ol class="toc">{toc}</ol>
      <p class="sm"><a href="#short">Jump to {len(shorts)} short answers (2 marks) ↓</a></p>
    </section>
  </div>
  <h2 class="sech" id="long">Long answers <small>7 marks · write 2–3 pages with one diagram</small></h2>
  {''.join(entry_html(e) for e in longs)}
  {f'<h2 class="sech" id="problems">Problems <small>numericals and traces asked as 7-mark questions</small></h2>' + ''.join(entry_html(e) for e in probs) if probs else ''}
  <h2 class="sech" id="short">Short answers <small>Section A · 2 marks · 4–6 lines each</small></h2>
  <div class="shorts">{''.join(entry_html(e) for e in shorts)}</div>
  {pager(u['n'])}
</div>"""
    return body


def pager(n):
    prev = f'<a class="btn" href="unit-{n - 1}.html">← Unit {ROMAN[n - 1]}</a>' if n > 1 else '<span></span>'
    nxt = f'<a class="btn primary" href="unit-{n + 1}.html">Unit {ROMAN[n + 1]} →</a>' if n < 6 else '<a class="btn primary" href="analysis.html">See the PYQ analysis →</a>'
    return f'<nav class="pager">{prev}{nxt}</nav>'


def paper_page(m, solved=False):
    secs = {"A": [], "B": [], "C": []}
    for q in m["qs"]:
        sec = "A" if q["qno"][0] == "1" else "B" if q["qno"][0] == "2" else "C"
        secs[sec].append(q)
    ans_count = 0

    def qrow(q):
        nonlocal ans_count
        ents = [DATA.entries[i] for i in q["ids"]]
        text = q["text"] or ents[0]["q"]
        unit = ents[0]["unit"]
        parts = []
        for e in ents:
            head = f'<p class="subq">Answer part: <b>{esc(e["q"])}</b></p>' if len(ents) > 1 else ""
            parts.append(head + f'<div class="ans">{e["html"]}</div>')
        note = '<p class="muted sm">This question asks for two short notes: write about one page on each, with a small diagram for each.</p>' if len(ents) > 1 else ""
        link = " · ".join(f'<a href="unit-{e["unit"]}.html#{e["id"]}">open in Unit {ROMAN[e["unit"]]} notes</a>' for e in ents)
        ans_count += 1
        return (f'<li class="mq" data-unit="{unit}"><div class="mqh"><span class="qno">{q["qno"][1:] if q["qno"][0] in "12" else q["qno"]}.</span>'
                f'<p>{esc(text)}</p><span class="co">U{ROMAN[unit]}</span></div>'
                f'<details class="mans"><summary>Show answer</summary>{note}{"".join(parts)}<p class="sm muted">{link}</p></details></li>')

    def section(sec, title, rule):
        qs = secs[sec]
        if not qs:
            return ""
        if sec == "C":
            groups, order = {}, []
            for q in qs:
                g = q["qno"][0]
                if g not in groups:
                    groups[g] = []
                    order.append(g)
                groups[g].append(q)
            inner = "".join(f'<div class="cgroup"><p class="cg"><b>{g}.</b> Attempt any <i>one</i> part of the following: <span class="mk">7 × 1 = 7</span></p><ol class="mqs">{"".join(qrow(q) for q in groups[g])}</ol></div>' for g in order)
            return f'<section class="psec"><h2>{title}</h2>{inner}</section>'
        return f'<section class="psec"><h2>{title}</h2><p class="cg"><b>{"1" if sec == "A" else "2"}.</b> {rule}</p><ol class="mqs">{"".join(qrow(q) for q in qs)}</ol></section>'

    session = "2025-26" if solved else "2026-27 (mock)"
    body = f"""
<div class="wrap page">
  <p class="eyebrow">{esc(m['sub'])}</p>
  <h1>{esc(m['title'])}</h1>
  <div class="paperbar">
    <button class="btn primary" type="button" data-timer="{m['slug']}">Start 3-hour timer</button>
    <span class="timer" data-timer-out="{m['slug']}" hidden></span>
    <button class="btn" type="button" data-openall>Show all answers</button>
    <button class="btn" type="button" onclick="window.print()">Print paper</button>
  </div>
  <div class="paper">
    <div class="phead">
      <div class="pcode">Subject Code: BCS701</div>
      <p class="pt">B.TECH<br>(SEM VII) THEORY EXAMINATION {session}<br><b>ARTIFICIAL INTELLIGENCE</b></p>
      <div class="prow"><span>TIME: 3 HRS</span><span>M.MARKS: 70</span></div>
      <p class="pnote">Note: Attempt all Sections. In case of any missing data, choose suitably.</p>
    </div>
    {section('A', 'SECTION A', 'Attempt <i>all</i> questions in brief. <span class="mk">2 × 7 = 14</span>')}
    {section('B', 'SECTION B', 'Attempt any <i>three</i> of the following. <span class="mk">7 × 3 = 21</span>')}
    {section('C', 'SECTION C', '')}
  </div>
  <div class="card tipcard"><b>How to use this paper:</b> set the timer, write your answers on paper first, then open each answer and compare. Long answers here are written the way AKTU examiners like them: headings, points, one labelled diagram, a table where it helps, and a conclusion, about 2–3 pages each.</div>
</div>"""
    return body


def papers_page():
    rows = []
    for p in DATA.papers:
        qs = []
        for q in p["qs"]:
            tags = q["tags"]
            unit = DATA.topics[tags[0]]["unit"]
            links = DATA.answers_for(q) if tags[0] != "old" else []
            ltxt = "".join(f'<a class="go" href="unit-{e["unit"]}.html#{e["id"]}">Answer →</a>' for e in links[:1])
            badge = '<span class="pill old sm">Not in MCA102 syllabus</span>' if tags[0] == "old" else f'<span class="ubadge sm">{ROMAN[unit]}</span>'
            tnames = ", ".join(DATA.topics[t]["name"].split(":")[0] for t in tags if t != "old")
            qs.append(f'<li class="pq" id="{qref(p, q)}" data-unit="{unit}" data-sec="{q["sec"]}"><span class="qno">{q["qno"]}</span>'
                      f'<div><p>{esc(q["text"])}</p><p class="tags">{badge} <span class="muted sm">{esc(tnames)}</span> <span class="muted sm">· {q["marks"]} marks</span></p></div>{ltxt}</li>')
        label = "Related paper: AI for the CSE (AI) branch, same new scheme" if p["kind"] == "related" else f"{p['marks']} marks"
        rows.append(f'<section class="ppaper" id="p-{p["session"]}-{p["code"]}"><h2>{p["session"]} <span>{p["code"]}</span></h2>'
                    f'<p class="muted sm">{label} · exam {esc(p["month"])} · <a href="{esc(p["url"])}" target="_blank" rel="noopener">source</a></p>'
                    f'<ol class="pqs">{"".join(qs)}</ol></section>')
    chips = "".join(f'<button type="button" class="chip" data-f="{n}">Unit {ROMAN[n]}</button>' for n in range(1, 7))
    nq = sum(len(p["qs"]) for p in DATA.papers)
    return f"""
<div class="wrap page">
  <p class="eyebrow">{len(DATA.papers)} papers · {nq} questions · each one tagged to an MCA102 topic</p>
  <h1>Past papers</h1>
  <p class="lede">Invertis University does not publish its MCA102 papers, so this page collects the closest match: every question from the <b>AKTU MCA (Sem II) Data Structures</b> papers, whose syllabus is nearly the same as MCA102 (arrays, stacks, queues, linked lists, trees, sorting, search trees, hashing, graphs) and whose paper uses the same CO-based Section A/B/C pattern. Papers: BMC205 (2024-25), KCA205 (2022-23, 2023-24), RCA202 (2016-17 to 2018-19) and NMCA213 (2017-18, 2018-19). <b>Answer →</b> opens the matching answer in the notes.</p>
  <div class="filters"><input type="search" id="pqSearch" placeholder="Search questions, e.g. AVL, postfix, Dijkstra" aria-label="Search questions">
    <div class="chips"><button type="button" class="chip on" data-f="all">All</button>{chips}<button type="button" class="chip" data-f="0">Not in syllabus</button></div>
    <p class="muted sm" id="pqCount" aria-live="polite"></p></div>
  {''.join(rows)}
</div>"""


# ------------------------------------------------------------------ analysis
def heatmap():
    main = DATA.main
    head = "".join(f'<th scope="col"><span>{p["session"]}</span><small>{p["code"]}</small></th>' for p in main)
    body = []
    for n in range(1, 7):
        body.append(f'<tr class="ugroup"><th colspan="{len(main) + 2}">Unit {ROMAN[n]}</th></tr>')
        for t in [t for t in DATA.topics.values() if t["unit"] == n]:
            cells = []
            for p in main:
                qs = [q for q in p["qs"] if t["id"] in q["tags"]]
                k = len(qs)
                tip = f'{t["name"]} · {p["session"]} {p["code"]}: ' + ("not asked" if not k else "; ".join(f'Q{q["qno"]} ({q["marks"]} marks)' for q in qs))
                cells.append(f'<td class="hm{min(k, 3)}" data-tip="{esc(tip)}">{k or ""}</td>')
            body.append(f'<tr><th scope="row">{esc(t["name"])}</th>{"".join(cells)}<td class="num">{main_count(t["id"])}</td></tr>')
    old = []
    for p in main:
        k = sum(1 for q in p["qs"] if "old" in q["tags"])
        old.append(f'<td class="hm{min(k, 3)} oldc" data-tip="{p["session"]} {p["code"]}: {k} questions on topics no longer in the syllabus">{k or ""}</td>')
    body.append(f'<tr class="ugroup"><th colspan="{len(main) + 2}">Dropped from the syllabus</th></tr><tr><th scope="row">Dynamic programming, LCS, Strassen, file organisation</th>{"".join(old)}<td></td></tr>')
    legend = ('<div class="hlegend"><span>Questions on the topic in that paper:</span><i class="hm1"></i>1<i class="hm2"></i>2<i class="hm3"></i>3+'
              '<span class="muted">· blank = not asked · newest paper first</span></div>')
    return f'{legend}<div class="heatwrap"><table class="heat"><thead><tr><th></th>{head}<th>Papers</th></tr></thead><tbody>{"".join(body)}</tbody></table></div>'


def ranking(limit=24):
    ts = [t for t in DATA.topics if t != "old"]
    ts.sort(key=lambda t: -DATA.stats[t]["chance"])
    rows = []
    for t in ts[:limit]:
        s, info = DATA.stats[t], DATA.topics[t]
        pct = round(100 * s["chance"])
        first = next((e for e in DATA.by_topic.get(t, []) if e["kind"] != "short"), None)
        name = f'<a href="unit-{first["unit"]}.html#{first["id"]}">{esc(info["name"])}</a>' if first else esc(info["name"])
        new = ' <span class="pill new sm">2024-25</span>' if t in DATA.in_latest else ""
        rows.append(f'<li data-tip="{esc(info["name"])}: asked in {len(s["papers"])} of {len(DATA.papers)} papers (incl. related); weighted chance {pct}%">'
                    f'<span class="rn"><span class="ubadge sm">{ROMAN[info["unit"]]}</span>{name}{new}</span>'
                    f'<span class="rbar"><i style="width:{pct}%"></i></span><span class="rv">{pct}%</span></li>')
    return f'<ol class="rank">{"".join(rows)}</ol>'


def always():
    """Names of the topics asked in every main paper, e.g. "Forward & backward chaining, …"."""
    names = [DATA.topics[t]["name"].split(":")[0] for t in DATA.topics if t != "old" and main_count(t) == len(DATA.main)]
    return ", ".join(names[:-1]) + " and " + names[-1] if len(names) > 1 else "".join(names)


def predicted(limit=18):
    """Most expected long questions: one per topic, highest chance first."""
    picks, seen = [], set()
    for e in sorted((e for e in DATA.entries.values() if e["kind"] != "short"), key=lambda e: -DATA.chance(e)):
        if any(t in seen for t in e["topics"]):
            continue
        seen.update(e["topics"])
        picks.append(e)
    items = "".join(f'<li><span class="ubadge sm">{ROMAN[e["unit"]]}</span><a href="unit-{e["unit"]}.html#{e["id"]}">{esc(e["q"])}</a> <span class="chance {band_class(DATA.chance(e))}">{P.band(DATA.chance(e))}</span></li>' for e in picks[:limit])
    return f'<ol class="pred">{items}</ol>'


def new_topics():
    """Topics of the 2025-26 BCS701 paper that older papers rarely or never asked: the setters' new favourites."""
    rows = []
    for t in sorted(DATA.in_latest, key=lambda t: (DATA.topics[t]["unit"], t)):
        if t == "old" or main_count(t) > 3:
            continue
        ents = [e for e in DATA.by_topic.get(t, []) if e["kind"] != "short"]
        links = ", ".join(f'<a href="unit-{e["unit"]}.html#{e["id"]}">{esc(e["q"].split("?")[0].split(".")[0])}</a>' for e in ents)
        rows.append(f'<li><span class="ubadge sm">{ROMAN[DATA.topics[t]["unit"]]}</span><b>{esc(DATA.topics[t]["name"])}</b> ({main_count(t)} of {len(DATA.main)} papers): {links}</li>')
    return f'<ul class="pred newt">{"".join(rows)}</ul>'


def analysis_page():
    md = open(os.path.join(ROOT, "content", "analysis.md"), encoding="utf-8").read()
    ctx = mdlite.Ctx("A")
    html_out = mdlite.render(md, ctx)
    nq = sum(len(p["qs"]) for p in DATA.papers)
    stats = (f'<div class="stats"><div class="stat"><b>{len(DATA.main)}</b><span>AKTU MCA data structures papers (2016-17 to 2024-25)</span></div>'
             f'<div class="stat"><b>{nq}</b><span>questions tagged by MCA102 topic</span></div>'
             f'<div class="stat"><b>{len([t for t in DATA.topics if t != "old"])}</b><span>syllabus topics tracked</span></div>'
             f'<div class="stat"><b>{sum(1 for t in DATA.topics if t != "old" and DATA.stats[t]["chance"] >= 0.75)}</b><span>topics with a very high chance</span></div></div>')
    for key, val in {"{{stats}}": stats, "{{heatmap}}": heatmap(), "{{ranking}}": ranking(), "{{predicted}}": predicted(), "{{newtopics}}": new_topics()}.items():
        html_out = html_out.replace(f"<p>{key}</p>", val)
    return f'<div class="wrap page prose-page">{html_out}</div>'


def guide_page():
    md = open(os.path.join(ROOT, "content", "guide.md"), encoding="utf-8").read()
    return f'<div class="wrap page prose-page">{mdlite.render(md, mdlite.Ctx("G"))}</div>'


def home_page():
    units = []
    for u in DATA.units:
        longs = [e for e in u["entries"] if e["kind"] != "short"]
        shorts = [e for e in u["entries"] if e["kind"] == "short"]
        ids = ",".join(e["id"] for e in longs)
        units.append(f'<a class="ucard" href="unit-{u["n"]}.html" data-ids="{ids}"><span class="ubadge">{ROMAN[u["n"]]}</span>'
                     f'<h3>{esc(u["title"])}</h3><p>{len(longs)} long answers · {len(shorts)} short answers</p>'
                     f'<div class="bar"><i></i></div><span class="lbl sm muted">0 revised</span></a>')
    nlong = sum(1 for e in DATA.entries.values() if e["kind"] != "short")
    nshort = sum(1 for e in DATA.entries.values() if e["kind"] == "short")
    nfig = sum(e["figs"] for e in DATA.entries.values())
    nq = sum(len(p["qs"]) for p in DATA.papers)
    return f"""
<div class="wrap page">
  <section class="hero">
    <div>
      <p class="eyebrow">Invertis University · MCA (2025-27 &amp; 2026-28) · Semester I · 4 credits</p>
      <h1>MCA102 Advanced Data Structure and Algorithms</h1>
      <p class="lede">Unit-wise notes for all six units, built from an analysis of {len(DATA.main)} past university papers on the same subject. Every long answer is written to score: <b>2–3 pages of theory with one labelled diagram</b>, a table and a conclusion, and every numerical is worked step by step.</p>
      <div class="cta"><a class="btn primary big" href="unit-1.html">Start with Unit I</a><a class="btn big" href="analysis.html">See what repeats</a><a class="btn big" href="papers.html">Past papers</a></div>
    </div>
    <div class="herofacts">
      <div><b>{nlong}</b><span>long answers</span></div>
      <div><b>{nshort}</b><span>short answers</span></div>
      <div><b>{nfig}</b><span>exam diagrams</span></div>
      <div><b>{nq}</b><span>past questions tagged</span></div>
    </div>
  </section>
  <section class="insights">
    <h2>How this exam is set</h2>
    <div class="kits">
      <div class="kit plain"><span class="k">Marks</span><h3>70 end-sem + 30 internal</h3><p>End Semester Exam 70 marks. Internal: Mid Term 12, Teacher's Assessment 6, Attendance 12. L-T-P 3-1-4, 4 credits.</p></div>
      <div class="kit plain"><span class="k">Pattern</span><h3>CO-based, 3 sections</h3><p>Invertis papers are CO based, like AKTU's: short answers in Section A, a choice of long answers in B, and a choice within each unit's question in C.</p></div>
      <div class="kit plain"><span class="k">Repeats</span><h3>Same topics every year</h3><p>{always()} were asked in every one of the {len(DATA.main)} papers analysed; hashing in {main_count("u5.hash")} and stacks in {main_count("u2.stack")}.</p></div>
    </div>
  </section>
  <section>
    <h2>Unit-wise notes</h2>
    <div class="units">{''.join(units)}</div>
  </section>
  <section class="grid2">
    <div class="card"><h2 class="h3">Most expected long questions</h2><p class="muted sm">Highest-chance topic first, one question per topic. <a href="analysis.html#most-expected-long-questions">Full list →</a></p>{predicted(10)}</div>
    <div class="card"><h2 class="h3">About the past papers</h2><p>Invertis University does not publish its MCA102 question papers online. The closest public papers are <b>AKTU's MCA Data Structures</b> papers (BMC205, KCA205, RCA202, NMCA213): the same subject, almost the same units and the same CO-based Section A/B/C format. Every question was tagged to an MCA102 topic to find what repeats.</p>
      <a class="kit" href="papers.html"><span class="k">Papers</span><h3>{len(DATA.papers)} papers · {nq} questions</h3><p>Filter by unit and jump to the answer.</p></a>
      <a class="kit" href="guide.html"><span class="k">Guide</span><h3>How to write the answers</h3><p>Time plan, answer layout and which diagram to draw.</p></a>
    </div>
  </section>
</div>"""


# ------------------------------------------------------------------ build
def write(rel, text):
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8", newline="\n").write(text)
    return f"{rel.replace(os.sep, '/')}?v={hashlib.sha1(text.encode()).hexdigest()[:10]}"


DATA = None


def main():
    global DATA
    DATA = Data()
    import check_content   # the same checks CI runs; a broken reference stops the build
    problems = [] if "--draft" in sys.argv else check_content.check(DATA)
    if problems:
        raise SystemExit("Content check failed:\n  " + "\n  ".join(problems))
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    css = open(os.path.join(SRC, "site.css"), encoding="utf-8").read()
    js = open(os.path.join(SRC, "app.js"), encoding="utf-8").read()
    css_url, js_url = write("assets/style.css", css), write("assets/app.js", js)
    pages = {
        "index.html": ("Home", home_page(), "Unit-wise notes and past-paper analysis for Invertis University MCA102 Advanced Data Structure and Algorithms."),
        "analysis.html": ("PYQ analysis", analysis_page(), "Which data structures topics repeat in university papers: heatmap, topic ranking and the most expected questions for MCA102."),
        "papers.html": ("Past papers", papers_page(), "Past MCA Data Structures questions (2016-17 to 2024-25), tagged by MCA102 unit and linked to answers."),
        "guide.html": ("Answer-writing guide", guide_page(), "How to write 2-mark and 7-mark answers that score in the MCA102 data structures exam."),
    }
    for u in DATA.units:
        pages[f"unit-{u['n']}.html"] = (f"Unit {ROMAN[u['n']]}: {u['short']}", unit_page(u), f"MCA102 Unit {ROMAN[u['n']]} notes: {u['title']}. Long answers with diagrams and 2-mark answers.")
    for slug, (title, body, desc) in pages.items():
        write(slug, shell(slug, title, body, desc, css_url, js_url))
    open(os.path.join(OUT, ".nojekyll"), "w").close()
    nfig = sum(e["figs"] for e in DATA.entries.values())
    print(f"site/: {len(pages)} pages, {len(DATA.entries)} answers, {nfig} diagrams, {sum(len(p['qs']) for p in DATA.papers)} past questions")


if __name__ == "__main__":
    sys.path.insert(0, os.path.join(ROOT, "tests"))
    main()
