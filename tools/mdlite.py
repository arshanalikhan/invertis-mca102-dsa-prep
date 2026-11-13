"""A small Markdown converter plus two diagram languages, so answers can be written as plain text.

Markdown subset: # … ###### headings, paragraphs, - and 1. lists (one nesting level), pipe tables
(write \\| for a literal bar inside a cell), > blockquotes (rendered as exam-tip callouts), fenced code,
**bold**, *italic*, `code`, [text](url).

Diagrams are fenced blocks, drawn as inline SVG that follows the page theme:

```fig 560x240 | Caption
box   id x y w h [flags] | Label\\nsecond line      rectangle (rbox = rounded, diamond = decision)
circle id cx cy r [flags] | Label
ellipse id cx cy rx ry [flags] | Label
group x y w h | Label                                 dashed container with a corner label
text x y [left|right|bold|small|muted|hl] | Text
arrow A B [dash|both|hl|bend=N] | label               A and B: a shape id, id.t/.b/.l/.r, or x,y
line  A B [dash] | label                              same as arrow without a head
poly x,y x,y ... [dash|noarrow] | label               elbow connector, arrow at the last point
path [dash|hl|arrow] | M 0 0 C ...                    raw SVG path for curves
```
Shape flags: hl (accent), soft (muted fill), dash, bold, small.

```tree 520x260 [game] | Caption
@levels MAX,MIN,MAX                                   optional labels down the left edge
A | note                                              two spaces of indent per level
  B ~edge-label
    !D                                                ! = pruned, * = highlighted path
```
In a game tree, leaves are drawn as squares (values); otherwise every node is a circle.
"""
import html
import math
import re

FONT = 13
FLAGS = {"hl", "soft", "dash", "bold", "small", "left", "right", "muted", "both", "noarrow", "arrow", "fill", "bend"}


def esc(s):
    return html.escape(s, quote=False)


# ---------------------------------------------------------------- inline
def inline(s):
    out, i = [], 0
    for m in re.finditer(r"`([^`]+)`", s):
        out.append(_inline_plain(s[i:m.start()]))
        out.append(f"<code>{esc(m.group(1))}</code>")
        i = m.end()
    out.append(_inline_plain(s[i:]))
    return "".join(out)


def _inline_plain(s):
    s = esc(s)
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", lambda m: f'<a href="{m.group(2)}"{_ext(m.group(2))}>{m.group(1)}</a>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
    return s


def _ext(url):
    return ' target="_blank" rel="noopener"' if url.startswith("http") else ""


# ---------------------------------------------------------------- blocks
class Ctx:
    """Per-page state: figure numbering and unique SVG ids."""

    def __init__(self, prefix="1"):
        self.prefix, self.fig, self.uid = prefix, 0, 0

    def next_fig(self):
        self.fig += 1
        self.uid += 1
        return f"{self.prefix}.{self.fig}", f"{self.prefix.replace('.', '-')}-{self.uid}"


def render(md, ctx):
    lines = md.replace("\r", "").split("\n")
    out, i, para = [], 0, []

    def flush():
        if para:
            out.append(f"<p>{inline(' '.join(p.strip() for p in para))}</p>")
            para.clear()

    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if not s:
            flush(); i += 1; continue
        if s.startswith("```"):
            flush()
            head, body = s[3:].strip(), []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                body.append(lines[i]); i += 1
            i += 1
            if head.startswith("fig"):
                out.append(fig(head[3:].strip(), body, ctx))
            elif head.startswith("tree"):
                out.append(tree(head[4:].strip(), body, ctx))
            else:
                lang = f' class="lang-{esc(head)}"' if head else ""
                out.append(f"<pre{lang}><code>{esc(chr(10).join(body))}</code></pre>")
            continue
        m = re.match(r"(#{1,6})\s+(.*)", s)
        if m:
            flush()
            n = len(m.group(1))
            # page-level headings get an anchor id; answer sub-headings (####) repeat, so they do not
            slug = re.sub(r"[^a-z0-9]+", "-", m.group(2).lower()).strip("-")
            hid = f' id="{slug}"' if n <= 3 else ""
            out.append(f"<h{n}{hid}>{inline(m.group(2))}</h{n}>")
            i += 1; continue
        if s.startswith("|") and i + 1 < len(lines) and re.match(r"^\|?\s*:?-{2,}", lines[i + 1].strip()):
            flush()
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i].strip()); i += 1
            out.append(table(rows))
            continue
        if s.startswith(">"):
            flush()
            quote = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip()[1:].lstrip()); i += 1
            out.append(f'<blockquote class="tip">{render(chr(10).join(quote), ctx)}</blockquote>')
            continue
        if re.match(r"^\s*([-*]|\d+[.)])\s+", line):
            flush()
            block = []
            while i < len(lines) and lines[i].strip() and (re.match(r"^\s*([-*]|\d+[.)])\s+", lines[i]) or lines[i].startswith("  ")):
                block.append(lines[i]); i += 1
            out.append(lists(block))
            continue
        para.append(s); i += 1
    flush()
    return "\n".join(out)


def table(rows):
    def cells(r):
        r = r.strip()
        if r.startswith("|"):
            r = r[1:]
        if r.endswith("|") and not r.endswith("\\|"):
            r = r[:-1]
        return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", r)]

    head, body = cells(rows[0]), [cells(r) for r in rows[2:]]
    h = "".join(f"<th>{inline(c)}</th>" for c in head)
    b = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body)
    return f'<div class="tbl"><table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'


def lists(block):
    items = []   # (indent, ordered, text)
    for ln in block:
        m = re.match(r"^(\s*)([-*]|\d+[.)])\s+(.*)", ln)
        if m:
            items.append([len(m.group(1)), m.group(2)[0].isdigit(), m.group(3).strip()])
        elif items:
            items[-1][2] += " " + ln.strip()
    base = items[0][0]
    html_out, open_sub = [], None
    tag = "ol" if items[0][1] else "ul"
    html_out.append(f"<{tag}>")
    for k, (ind, ordered, text) in enumerate(items):
        if ind > base:
            if open_sub is None:
                open_sub = "ol" if ordered else "ul"
                html_out[-1] = html_out[-1][:-5] + f"<{open_sub}>"   # reopen the last <li>
            html_out.append(f"<li>{inline(text)}</li>")
            continue
        if open_sub:
            html_out.append(f"</{open_sub}></li>")
            open_sub = None
        html_out.append(f"<li>{inline(text)}</li>")
    if open_sub:
        html_out.append(f"</{open_sub}></li>")
    html_out.append(f"</{tag}>")
    return "".join(html_out)


# ---------------------------------------------------------------- diagrams
def _num(t):
    return float(t)


def _label_svg(x, y, text, cls="t", anchor="middle", lh=15):
    parts = text.split("\\n")
    y0 = y - (len(parts) - 1) * lh / 2
    spans = "".join(f'<tspan x="{x:.1f}" y="{y0 + k * lh:.1f}">{esc(p)}</tspan>' for k, p in enumerate(parts))
    return f'<text class="{cls}" text-anchor="{anchor}" dominant-baseline="central">{spans}</text>'


def _clip(shape, px, py):
    cx, cy = shape["cx"], shape["cy"]
    dx, dy = px - cx, py - cy
    if dx == 0 and dy == 0:
        return cx, cy
    k = shape["kind"]
    if k == "circle":
        t = shape["r"] / math.hypot(dx, dy)
    elif k == "ellipse":
        t = 1 / math.sqrt((dx / shape["rx"]) ** 2 + (dy / shape["ry"]) ** 2)
    elif k == "diamond":
        t = 1 / (abs(dx) / shape["hw"] + abs(dy) / shape["hh"])
    else:
        tx = shape["hw"] / abs(dx) if dx else math.inf
        ty = shape["hh"] / abs(dy) if dy else math.inf
        t = min(tx, ty)
    t = min(t, 1)
    return cx + dx * t, cy + dy * t


def _point(tok, shapes):
    """Return (x, y, shape-or-None). A shape is returned when the point should be clipped to it."""
    if "," in tok and tok.replace(",", "").replace(".", "").replace("-", "").isdigit():
        x, y = tok.split(",")
        return float(x), float(y), None
    sid, _, side = tok.partition(".")
    if sid not in shapes:
        raise ValueError(f"diagram: unknown shape id {sid!r}")
    s = shapes[sid]
    if not side:
        return s["cx"], s["cy"], s
    hw, hh = s["hw"], s["hh"]
    off = {"t": (0, -hh), "b": (0, hh), "l": (-hw, 0), "r": (hw, 0),
           "tl": (-hw, -hh), "tr": (hw, -hh), "bl": (-hw, hh), "br": (hw, hh)}[side]
    return s["cx"] + off[0], s["cy"] + off[1], None


def fig(header, body, ctx):
    m = re.match(r"(\d+)x(\d+)\s*(?:\|\s*(.*))?$", header)
    if not m:
        raise ValueError(f"bad fig header: {header!r}")
    W, H, caption = int(m.group(1)), int(m.group(2)), (m.group(3) or "").strip()
    num, uid = ctx.next_fig()
    shapes, back, front = {}, [], []
    for raw in body:
        if not raw.strip() or raw.strip().startswith("//"):
            continue
        left, _, label = raw.partition("|")
        label = label.strip()
        toks = left.split()
        kind, args = toks[0], toks[1:]
        is_flag = lambda a: a.split("=")[0] in FLAGS and (a in FLAGS or re.match(r"^bend=-?[\d.]+$", a))
        flags = {a.split("=")[0]: (a.split("=")[1] if "=" in a else True) for a in args if is_flag(a)}
        args = [a for a in args if not is_flag(a)]
        cls = "n" + "".join(f" {f}" for f in ("hl", "soft", "dash", "bold") if f in flags)
        tcls = "t" + (" small" if "small" in flags else "") + (" bold" if "bold" in flags else "")
        if kind in ("box", "rbox", "diamond"):
            sid, x, y, w, h = args[0], *map(_num, args[1:5])
            shapes[sid] = {"kind": kind, "cx": x + w / 2, "cy": y + h / 2, "hw": w / 2, "hh": h / 2}
            if kind == "diamond":
                pts = f"{x + w / 2},{y} {x + w},{y + h / 2} {x + w / 2},{y + h} {x},{y + h / 2}"
                back.append(f'<polygon class="{cls}" points="{pts}"/>')
            else:
                rx = ' rx="10"' if kind == "rbox" else ' rx="2"'
                back.append(f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}"{rx}/>')
            if label:
                front.append(_label_svg(x + w / 2, y + h / 2, label, tcls))
        elif kind == "circle":
            sid, cx, cy, r = args[0], *map(_num, args[1:4])
            shapes[sid] = {"kind": "circle", "cx": cx, "cy": cy, "r": r, "hw": r, "hh": r}
            back.append(f'<circle class="{cls}" cx="{cx}" cy="{cy}" r="{r}"/>')
            if label:
                front.append(_label_svg(cx, cy, label, tcls))
        elif kind == "ellipse":
            sid, cx, cy, rx, ry = args[0], *map(_num, args[1:5])
            shapes[sid] = {"kind": "ellipse", "cx": cx, "cy": cy, "rx": rx, "ry": ry, "hw": rx, "hh": ry}
            back.append(f'<ellipse class="{cls}" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}"/>')
            if label:
                front.append(_label_svg(cx, cy, label, tcls))
        elif kind == "group":
            x, y, w, h = map(_num, args[:4])
            back.insert(0, f'<rect class="grp" x="{x}" y="{y}" width="{w}" height="{h}" rx="12"/>')
            if label:
                front.append(f'<text class="t small muted" x="{x + 10}" y="{y + 16}">{esc(label)}</text>')
        elif kind == "text":
            x, y = map(_num, args[:2])
            anchor = "start" if "left" in flags else "end" if "right" in flags else "middle"
            c = tcls + (" muted" if "muted" in flags else "") + (" hl" if "hl" in flags else "")
            front.append(_label_svg(x, y, label, c, anchor))
        elif kind in ("arrow", "line"):
            ax, ay, sa = _point(args[0], shapes)
            bx, by, sb = _point(args[1], shapes)
            bend = float(flags.get("bend", 0)) if flags.get("bend", 0) is not True else 0
            ecls = "e" + (" dash" if "dash" in flags else "") + (" hl" if "hl" in flags else "")
            if bend:
                mx, my = (ax + bx) / 2, (ay + by) / 2
                ln = math.hypot(bx - ax, by - ay) or 1
                qx, qy = mx - (by - ay) / ln * bend, my + (bx - ax) / ln * bend
                if sa: ax, ay = _clip(sa, qx, qy)
                if sb: bx, by = _clip(sb, qx, qy)
                d = f"M{ax:.1f},{ay:.1f} Q{qx:.1f},{qy:.1f} {bx:.1f},{by:.1f}"
                lx, ly = 0.25 * ax + 0.5 * qx + 0.25 * bx, 0.25 * ay + 0.5 * qy + 0.25 * by
            else:
                if sa: ax, ay = _clip(sa, bx, by)
                if sb: bx, by = _clip(sb, ax, ay)
                d = f"M{ax:.1f},{ay:.1f} L{bx:.1f},{by:.1f}"
                lx, ly = (ax + bx) / 2, (ay + by) / 2
            heads = ""
            if kind == "arrow":
                heads = f' marker-end="url(#ah{uid})"' + (f' marker-start="url(#as{uid})"' if "both" in flags else "")
            back.append(f'<path class="{ecls}" d="{d}"{heads}/>')
            if label:
                ln = math.hypot(bx - ax, by - ay) or 1
                nx, ny = -(by - ay) / ln, (bx - ax) / ln
                if ny > 0 or (ny == 0 and nx > 0):
                    nx, ny = -nx, -ny
                front.append(_label_svg(lx + nx * 9, ly + ny * 9, label, "el"))
        elif kind == "poly":
            pts = [tuple(map(float, a.split(","))) for a in args]
            ecls = "e" + (" dash" if "dash" in flags else "") + (" hl" if "hl" in flags else "")
            head = "" if "noarrow" in flags else f' marker-end="url(#ah{uid})"'
            back.append(f'<polyline class="{ecls}" points="{" ".join(f"{x},{y}" for x, y in pts)}"{head}/>')
            if label:
                k = len(pts) // 2
                (x1, y1), (x2, y2) = pts[k - 1], pts[k]
                front.append(_label_svg((x1 + x2) / 2 + 4, (y1 + y2) / 2 - 9, label, "el"))
        elif kind == "path":
            ecls = "e" + (" dash" if "dash" in flags else "") + (" hl" if "hl" in flags else "") + (" fillsoft" if "fill" in flags else "")
            head = f' marker-end="url(#ah{uid})"' if "arrow" in flags else ""
            back.append(f'<path class="{ecls}" d="{esc(label)}"{head}/>')
        else:
            raise ValueError(f"diagram: unknown element {kind!r}")
    return _svg(W, H, uid, back + front, num, caption)


def _svg(W, H, uid, parts, num, caption):
    defs = (f'<defs><marker id="ah{uid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
            f'<path class="ah" d="M0,0 L10,5 L0,10 z"/></marker>'
            f'<marker id="as{uid}" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
            f'<path class="ah" d="M10,0 L0,5 L10,10 z"/></marker></defs>')
    cap = f"<figcaption><b>Fig. {num}</b> {inline(caption)}</figcaption>" if caption else f"<figcaption><b>Fig. {num}</b></figcaption>"
    return (f'<figure class="dg"><svg viewBox="0 0 {W} {H}" style="max-width:{W}px" role="img" aria-label="{esc(caption)}">'
            f'{defs}{"".join(parts)}</svg>{cap}</figure>')


def tree(header, body, ctx):
    m = re.match(r"(\d+)x(\d+)\s*(game)?\s*(?:\|\s*(.*))?$", header)
    if not m:
        raise ValueError(f"bad tree header: {header!r}")
    W, H, game, caption = int(m.group(1)), int(m.group(2)), bool(m.group(3)), (m.group(4) or "").strip()
    num, uid = ctx.next_fig()
    levels, nodes, stack = [], [], []
    for raw in body:
        if not raw.strip():
            continue
        if raw.strip().startswith("@levels"):
            levels = [x.strip() for x in raw.strip()[7:].split(",")]
            continue
        depth = (len(raw) - len(raw.lstrip(" "))) // 2
        text, _, note = raw.strip().partition("|")
        text = text.strip()
        pruned, hl = text.startswith("!"), text.startswith("*")
        text = text.lstrip("!*").strip()
        text, _, edge = text.partition("~")
        node = {"label": text.strip(), "edge": edge.strip(), "note": note.strip(), "depth": depth,
                "pruned": pruned, "hl": hl, "kids": []}
        while stack and stack[-1]["depth"] >= depth:
            stack.pop()
        if stack:
            stack[-1]["kids"].append(node)
            node["pruned"] = node["pruned"] or stack[-1]["pruned"]
        nodes.append(node)
        stack.append(node)
    leaves = [n for n in nodes if not n["kids"]]
    maxd = max(n["depth"] for n in nodes) or 1

    def size(n):
        lab = n["label"]
        if game and not n["kids"]:
            return ("rect", max(26, 8 * len(lab) + 12) / 2, 13)
        if len(lab) > 3:
            return ("rect", (8 * len(lab) + 16) / 2, 14)
        return ("circle", 15, 15)

    # leave room for wide labels on the outermost leaves
    left = (64 if levels else 24) + max(0, size(leaves[0])[1] - 15)
    span = W - left - 30 - max(0, size(leaves[-1])[1] - 15)
    for k, n in enumerate(leaves):
        n["x"] = left + (span * k / (len(leaves) - 1) if len(leaves) > 1 else span / 2)

    def place(n):
        if n["kids"]:
            for c in n["kids"]:
                place(c)
            n["x"] = sum(c["x"] for c in n["kids"]) / len(n["kids"])
        n["y"] = 26 + (H - 52) * n["depth"] / maxd

    place(nodes[0])
    back, front = [], []
    for d, name in enumerate(levels):
        front.append(f'<text class="t small muted" x="6" y="{26 + (H - 52) * d / maxd:.1f}" dominant-baseline="central">{esc(name)}</text>')

    for n in nodes:
        kind, hw, hh = size(n)
        n["shape"] = {"kind": "circle" if kind == "circle" else "box", "cx": n["x"], "cy": n["y"], "r": hw, "hw": hw, "hh": hh}
    for n in nodes:
        for c in n["kids"]:
            x1, y1 = _clip(n["shape"], c["x"], c["y"])
            x2, y2 = _clip(c["shape"], n["x"], n["y"])
            cls = "e" + (" pr" if c["pruned"] else "") + (" hl" if c["hl"] and n["hl"] else "")
            back.append(f'<path class="{cls}" d="M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}"/>')
            if c["edge"]:
                mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                dx = -10 if c["x"] < n["x"] else 10 if c["x"] > n["x"] else 10
                front.append(_label_svg(mx + dx, my, c["edge"], "el"))
            if c["pruned"] and not n["pruned"]:
                mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                front.append(f'<text class="cut" x="{mx:.1f}" y="{my:.1f}" text-anchor="middle" dominant-baseline="central">✂</text>')
    for n in nodes:
        s = n["shape"]
        cls = "n" + (" hl" if n["hl"] else "") + (" pr" if n["pruned"] else "") + (" soft" if game and not n["kids"] else "")
        if s["kind"] == "circle":
            back.append(f'<circle class="{cls}" cx="{n["x"]:.1f}" cy="{n["y"]:.1f}" r="{s["r"]}"/>')
        else:
            back.append(f'<rect class="{cls}" x="{n["x"] - s["hw"]:.1f}" y="{n["y"] - s["hh"]:.1f}" width="{2 * s["hw"]:.1f}" height="{2 * s["hh"]:.1f}" rx="4"/>')
        front.append(_label_svg(n["x"], n["y"], n["label"], "t" + (" pr" if n["pruned"] else "")))
        if n["note"]:
            if n["kids"]:
                front.append(f'<text class="t small hl" x="{n["x"] + s["hw"] + 5:.1f}" y="{n["y"] - 6:.1f}">{esc(n["note"])}</text>')
            else:
                front.append(f'<text class="t small hl" x="{n["x"]:.1f}" y="{n["y"] + s["hh"] + 12:.1f}" text-anchor="middle">{esc(n["note"])}</text>')
    return _svg(W, H, uid, back + front, num, caption)


def words(md):
    """Rough word count of the prose (diagram and code blocks left out)."""
    text = re.sub(r"```.*?```", " ", md, flags=re.S)
    return len(re.findall(r"[A-Za-z0-9∀∃¬∧∨⇒]+", text))
