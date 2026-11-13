"""Content checks, run by CI and by every build:  python tests/check_content.py

Fails when a past-paper tag or an answer topic is unknown, an answer id repeats, a long answer has no
diagram or is far too short/long, or a mock paper breaks the BCS701 pattern (7 short questions,
5 Section B questions one per unit, Section C Q3-Q7 each with two parts from units I-V).
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LONG_WORDS = (150, 1000)   # code blocks are not counted
SHORT_WORDS = 130


def check(D):
    problems = []
    seen = {}
    for u in D.units:
        for e in u["entries"]:
            if e["id"] in seen:
                problems.append(f"duplicate answer id {e['id']} (units {seen[e['id']]} and {u['n']})")
            seen[e["id"]] = u["n"]
            for t in e["topics"]:
                if t not in D.topics:
                    problems.append(f"{e['id']}: unknown topic {t}")
                elif D.topics[t]["unit"] != u["n"]:
                    problems.append(f"{e['id']}: topic {t} belongs to unit {D.topics[t]['unit']}, not {u['n']}")
            if e["kind"] == "short":
                if e["words"] > SHORT_WORDS:
                    problems.append(f"{e['id']}: short answer has {e['words']} words (max {SHORT_WORDS})")
            else:
                if e["figs"] < 1:
                    problems.append(f"{e['id']}: long answer has no diagram")
                if not LONG_WORDS[0] <= e["words"] <= LONG_WORDS[1]:
                    problems.append(f"{e['id']}: long answer has {e['words']} words (want {LONG_WORDS[0]}-{LONG_WORDS[1]})")
    for t, info in D.topics.items():
        if t == "old":
            continue
        kinds = {e["kind"] for e in D.by_topic.get(t, [])}
        if not kinds & {"long", "problem"}:
            problems.append(f"topic {t} has no long answer")
    for p in D.papers:
        for q in p["qs"]:
            for t in q["tags"]:
                if t not in D.topics:
                    problems.append(f"{p['session']} {p['code']} Q{q['qno']}: unknown topic {t}")
    want = [f"1{c}" for c in "abcdefg"] + [f"2{c}" for c in "abcde"] + [f"{n}{c}" for n in range(3, 8) for c in "ab"]
    c_units = {"3": {1}, "4": {2}, "5": {3, 4}, "6": {5}, "7": {6}}
    for m in D.mocks:
        qnos = [q["qno"] for q in m["qs"]]
        if qnos != want:
            problems.append(f"mock {m['slug']}: question numbers {qnos} do not follow the 1a-1g, 2a-2e, 3a-7b pattern")
        used = []
        for q in m["qs"]:
            for i in q["ids"]:
                e = D.entries.get(i)
                if not e:
                    problems.append(f"mock {m['slug']} Q{q['qno']}: unknown answer id {i}")
                    continue
                used.append(i)
                if q["qno"][0] == "1" and e["kind"] != "short":
                    problems.append(f"mock {m['slug']} Q{q['qno']}: Section A needs a short answer, got {i}")
                if q["qno"][0] != "1" and e["kind"] == "short":
                    problems.append(f"mock {m['slug']} Q{q['qno']}: Sections B/C need a long answer, got {i}")
                if q["qno"][0] in c_units and e["unit"] not in c_units[q["qno"][0]]:
                    problems.append(f"mock {m['slug']} Q{q['qno']}: should come from unit(s) {sorted(c_units[q['qno'][0]])}, got unit {e['unit']}")
        dup = {i for i in used if used.count(i) > 1}
        if dup:
            problems.append(f"mock {m['slug']}: answers used twice in one paper: {sorted(dup)}")
        if len({D.entries[i]["unit"] for i in used if i in D.entries}) < 6:
            problems.append(f"mock {m['slug']}: does not cover all six units")
    return problems


if __name__ == "__main__":
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    import build_site
    D = build_site.Data()
    probs = check(D)
    longs = [e for e in D.entries.values() if e["kind"] != "short"]
    used = {i for m in D.mocks for q in m["qs"] for i in q["ids"]}
    print(f"{len(D.entries)} answers ({len(longs)} long), {sum(len(p['qs']) for p in D.papers)} past questions, "
          f"{len(D.mocks)} papers; {len([e for e in longs if e['id'] in used])}/{len(longs)} long answers used in a paper")
    if probs:
        print("FAILED:\n  " + "\n  ".join(probs))
        sys.exit(1)
    print("All content checks passed.")
