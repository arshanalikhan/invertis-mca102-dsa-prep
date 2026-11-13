# How to write MCA102 answers

Data Structures is a **numerical-heavy** paper: examiners give most marks for correct, step-by-step working shown in a table, plus a clean diagram. This page sums up what scores.

## Time plan for a 3-hour, 70-mark paper

| Part | Marks | Time |
|---|---|---|
| Read the paper, choose questions | – | 10 min |
| Section A: 7 × 2 marks | 14 | 25 min (3–4 min each) |
| Section B: 3 × 7 marks | 21 | 55 min (about 18 min each) |
| Section C: 5 × 7 marks | 35 | 80 min (about 16 min each) |
| Check numericals and diagrams | – | 10 min |

Choose Section B questions you can answer with a numerical or a diagram: they are the easiest to score full marks on.

## The 2-mark answer

4–6 lines: a **definition**, one key **property or formula**, and a tiny **example** or a two-column difference table. Example: "Circular queue full: (REAR + 1) % MAX = FRONT".

## The 7-mark answer

1. **Definition / introduction** (3–4 lines).
2. **Algorithm or C function** in clear numbered steps.
3. **One labelled diagram**: nodes with arrows, the tree after insertion, the stack at a step, the hash table.
4. **Worked example in a table**, step by step (sorting passes, stack contents, BFS queue, Dijkstra distances).
5. **Complexity**: best, average and worst case.
6. **Comparison table** where the question says "compare" or "differentiate".
7. **Conclusion** (1–2 lines).

That is about 2–3 pages of an answer booklet.

## Which diagram to draw

| Question about | Draw |
|---|---|
| Array address, row/column major | The cells in memory order with indices |
| Stack, queue, circular queue | Array cells with TOP / FRONT / REAR marked |
| Linked list operations | Node boxes with arrows before and after (number the pointer changes) |
| Infix / postfix | Stack contents table at each symbol |
| Tree construction or traversal | The final binary tree |
| BST, AVL, B-tree | Tree after each insertion (at least the final tree and every rotation/split) |
| Sorting | One row per pass, sorted part marked |
| Heap sort | The max-heap as a tree and as an array |
| Hashing | The final table with slot numbers |
| BFS / DFS | The graph, then the queue/stack table and the traversal order |
| MST, Dijkstra | The graph with the chosen edges highlighted, plus the step table |

## Common mistakes that lose marks

- Not stating the **index assumption** (starting at 0 or 1) in address numericals.
- Popping operands in the wrong order in postfix evaluation (second popped ⊗ first popped).
- Forgetting that ^ is right-associative in infix conversion.
- Drawing BST/AVL trees without the intermediate steps when asked to "show all steps".
- Not checking the **full condition** of a circular queue, or the overflow case of a linear queue.
- Writing C code without handling **overflow/underflow** or the **empty list** case.
- In Kruskal's algorithm, not saying *why* an edge is rejected (it forms a cycle).

## Before the exam

Revise every **Very high** chance answer on the [PYQ analysis](analysis.html) page and redo each numerical once on paper without looking: address calculation, postfix evaluation, Tower of Hanoi, tree from traversals, BST, AVL, B-tree, quick/heap sort, hashing, BFS/DFS, MST and Dijkstra.
