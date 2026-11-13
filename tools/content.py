"""Load the unit notes (content/unit*.md) and the mock papers (content/mocks.txt).

Unit file format: a front-matter block between --- lines, an intro paragraph, then entries:
    ### S <id> | <topic ids> | <question>      short answer (Section A, 2 marks)
    ### L <id> | <topic ids> | <question>      long answer (Sections B and C, 7 marks)
    ### N <id> | <topic ids> | <question>      problem / numerical, written like a long answer
The answer body is Markdown (see tools/mdlite.py), with ```fig / ```tree diagrams.
"""
import glob
import os
import re

import mdlite

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
KINDS = {"S": "short", "L": "long", "N": "problem"}


def load_units():
    units = []
    for path in sorted(glob.glob(os.path.join(CONTENT, "unit*.md"))):
        text = open(path, encoding="utf-8").read().replace("\r", "")
        m = re.match(r"---\n(.*?)\n---\n", text, re.S)
        meta = dict(re.match(r"(\w+):\s*(.*)", ln).groups() for ln in m.group(1).split("\n") if ln.strip())
        rest = text[m.end():]
        parts = re.split(r"^### ", rest, flags=re.M)
        unit = {"n": int(meta["unit"]), "title": meta["title"], "short": meta["short"],
                "syllabus": meta["syllabus"], "intro_md": parts[0].strip(), "entries": [], "path": path}
        ctx = mdlite.Ctx(str(unit["n"]))
        unit["intro"] = mdlite.render(unit["intro_md"], ctx)
        for part in parts[1:]:
            head, _, body = part.partition("\n")
            hm = re.match(r"([SLN])\s+([\w-]+)\s*\|\s*([\w.,-]+)\s*\|\s*(.+)$", head.strip())
            if not hm:
                raise SystemExit(f"{os.path.basename(path)}: bad entry header: {head!r}")
            kind, eid, topics, q = hm.groups()
            try:
                html = mdlite.render(body.strip(), ctx)
            except Exception as e:  # report which answer has the broken diagram
                raise SystemExit(f"{os.path.basename(path)} {eid}: {e}")
            unit["entries"].append({"id": eid, "kind": KINDS[kind], "topics": topics.split(","), "q": q.strip(),
                                    "md": body.strip(), "html": html, "unit": unit["n"],
                                    "words": mdlite.words(body), "figs": html.count('<figure class="dg">')})
        units.append(unit)
    return units


def load_mocks():
    """content/mocks.txt: '@mock <slug> | <title> | <subtitle>' then '<qno> | <answer ids joined by +> | [question text]'."""
    mocks, path = [], os.path.join(CONTENT, "mocks.txt")
    for raw in open(path, encoding="utf-8"):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("@mock"):
            slug, title, sub = [p.strip() for p in line[5:].split("|")]
            mocks.append({"slug": slug, "title": title, "sub": sub, "qs": []})
            continue
        qno, ids, *text = [p.strip() for p in line.split("|", 2)]
        mocks[-1]["qs"].append({"qno": qno, "ids": ids.split("+"), "text": text[0] if text else ""})
    return mocks
