"""Read content/pyqs.txt and content/topics.txt, and compute topic statistics.

Used by tools/build_site.py (analysis page) and runnable on its own:
    python tools/pyqdata.py      prints the topic table
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
LATEST = 2025          # exam year of the newest paper (session 2024-25)
DECAY = 0.8            # weight of a paper = DECAY ** (years before LATEST)


def lines(name):
    for raw in open(os.path.join(CONTENT, name), encoding="utf-8"):
        line = raw.strip()
        if line and not line.startswith("#"):
            yield line


def load_topics():
    topics = {}
    for line in lines("topics.txt"):
        tid, unit, name = [p.strip() for p in line.split("|")]
        topics[tid] = {"id": tid, "unit": int(unit), "name": name}
    return topics


def load_papers():
    papers = []
    for line in lines("pyqs.txt"):
        if line.startswith("@paper"):
            session, code, marks, kind, month, url = [p.strip() for p in line[6:].split("|")]
            papers.append({"session": session, "code": code, "marks": int(marks), "kind": kind,
                           "month": month, "url": url, "year": int(session[:4]) + 1, "qs": []})
            continue
        qno, tags, text = [p.strip() for p in line.split("|", 2)]
        p = papers[-1]
        sec = "A" if qno[0] == "1" else "B" if qno[0] == "2" else "C"
        big = 7 if p["marks"] == 70 else 10
        p["qs"].append({"qno": qno, "sec": sec, "tags": tags.split(","), "text": text,
                        "marks": 2 if sec == "A" else big})
    return papers


def paper_id(p):
    return f"{p['session']}-{p['code']}"


def stats(papers, topics):
    """Per topic: papers it appeared in, recency-weighted score, counts by section."""
    out = {t: {"papers": [], "score": 0.0, "A": 0, "BC": 0, "recent": 0, "last": None} for t in topics}
    main = [p for p in papers if p["kind"] == "main"]
    total_w = sum(DECAY ** (LATEST - p["year"]) for p in main)
    for p in papers:
        w = DECAY ** (LATEST - p["year"])
        seen = set()
        for q in p["qs"]:
            for t in q["tags"]:
                s = out[t]
                if q["sec"] == "A":
                    s["A"] += 1
                else:
                    s["BC"] += 1
                if t not in seen:
                    seen.add(t)
                    s["papers"].append(paper_id(p))
                    if p["kind"] == "main":
                        s["score"] += w
                        if p["year"] >= LATEST - 4:
                            s["recent"] += 1
                    if s["last"] is None or p["year"] > s["last"]:
                        s["last"] = p["year"]
    for s in out.values():
        s["chance"] = s["score"] / total_w     # share of (weighted) papers that asked it
    return out


def band(chance):
    return "Very high" if chance >= 0.75 else "High" if chance >= 0.5 else "Medium" if chance >= 0.25 else "Low"


if __name__ == "__main__":
    T, P = load_topics(), load_papers()
    S = stats(P, T)
    print(f"{len(P)} papers, {sum(len(p['qs']) for p in P)} questions")
    for t in sorted(T, key=lambda t: -S[t]["chance"]):
        s = S[t]
        print(f"{t:16} u{T[t]['unit']} chance {s['chance']:.2f} {band(s['chance']):9} papers {len(s['papers']):2} "
              f"recent5y {s['recent']} A {s['A']:2} B/C {s['BC']:2} last {s['last']}")
