# MCA102 Advanced Data Structure and Algorithms: prep site

Study site for **Invertis University · MCA (2025-27) · Semester I · MCA102 Advanced Data Structure and Algorithms**.

**[Open the site](https://arshanalikhan.github.io/invertis-mca102-dsa-prep/)**

## What's inside

| Page | What it gives you |
|---|---|
| Unit notes I–VI | Long answers (theory, one labelled diagram, worked example, complexity, conclusion) and 2-mark answers for every syllabus topic |
| PYQ analysis | 8 past MCA Data Structures papers (2016-17 to 2024-25) tagged by MCA102 topic: heatmap, chance ranking, word-for-word repeats, expected questions |
| Past papers | All 183 past questions, filterable by unit, each linked to its answer |
| Mock tests | Three timed 70-mark papers (3-hour timer, question palette, mark-for-review), then model answers and self-marking scored the way the examiner counts |
| Answer-writing guide | Time plan, the 7-mark answer layout, which diagram to draw |

Invertis University does not publish its MCA102 question papers, so the analysis uses AKTU's MCA Data Structures papers (BMC205, KCA205, RCA202, NMCA213), which cover nearly the same syllabus in the same CO-based format.

## Build

Needs Python 3.10+, nothing to install.

```bash
python tests/check_content.py      # content checks (CI runs them too)
python tools/build_site.py         # builds content/ and src/ into site/
python -m http.server 8794 --directory site
```

Edit `content/` (notes, papers, topics) or `src/` (CSS/JS); `site/` is generated. Every push to `main` builds and deploys to GitHub Pages.

Not an official Invertis University or AKTU resource; if anything here disagrees with your teacher or textbook, follow them.
