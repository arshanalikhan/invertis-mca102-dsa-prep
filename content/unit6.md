---
unit: 6
title: Graphs
short: Graphs
syllabus: Graphs: terminology, sequential and linked representations of graphs: adjacency matrices, adjacency list, adjacency multi list, graph traversal: depth first search and breadth first search, connected component, spanning trees, minimum cost spanning trees: Prim's and Kruskal's algorithm, transitive closure and shortest path algorithm: Warshall algorithm and Dijkstra algorithm, introduction to activity networks.
---

Graph questions are almost always **numericals on a drawn graph**: BFS/DFS order, Prim/Kruskal MST, and Dijkstra. Show the table of steps, then draw the final tree. Graph representation (matrix vs list) is a common short and long question.

### S u6s-graph | u6.graphrep | Define graph, connected graph, complete (fully connected) graph and weighted graph.
- **Graph** G = (V, E): a set of vertices V and a set of edges E connecting pairs of vertices.
- **Connected graph**: there is a path between every pair of vertices.
- **Complete (fully connected) graph**: every pair of distinct vertices is joined by an edge; Kₙ has n(n − 1)/2 edges.
- **Weighted graph**: each edge carries a number (cost, distance, time).
- **Planar graph**: can be drawn on a plane with no crossing edges.

### S u6s-directed | u6.graphrep | Differentiate between directed and undirected graph.
| Directed graph (digraph) | Undirected graph |
|---|---|
| Edges have a direction: (u, v) ≠ (v, u) | Edges have no direction: (u, v) = (v, u) |
| Drawn with arrows | Drawn with plain lines |
| In-degree and out-degree | Only degree |
| Adjacency matrix may be unsymmetric | Adjacency matrix is symmetric |
| Example: web links, task dependencies | Example: road network, friendships |

### S u6s-cycle | u6.graphrep | Explain cycle and Hamiltonian cycle in a graph.
- **Cycle**: a path of length ≥ 3 that starts and ends at the same vertex with no other repeated vertex, e.g. A–B–C–A. A graph with no cycle is **acyclic** (a tree, if connected).
- **Hamiltonian cycle**: a cycle that visits **every vertex exactly once** and returns to the start. Example in a square A–B–C–D–A. (An **Euler circuit** instead uses every **edge** exactly once.)

### S u6s-mst | u6.mst | What is a minimum spanning tree (MST)?
A **spanning tree** of a connected graph with n vertices is a subgraph that is a tree containing **all n vertices and exactly n − 1 edges** (no cycles). A **minimum spanning tree** is a spanning tree whose **total edge weight is the smallest** possible. It is found with **Prim's** or **Kruskal's** algorithm and used in network (cable, road, circuit) design.

### S u6s-graph-tree | u6.graphrep | Differentiate between graph and tree.
| Graph | Tree |
|---|---|
| May contain cycles | No cycles |
| No root | One root node |
| Any number of edges | Exactly n − 1 edges |
| May be disconnected | Always connected |
| Network model | Hierarchical model |
| Traversed by BFS/DFS | Traversed by in/pre/post order (and BFS/DFS) |

### L u6-represent | u6.graphrep | What are the different ways to represent a graph in memory? Explain adjacency matrix, adjacency list and adjacency multilist with an example.
#### Example graph
Undirected graph with V = {A, B, C, D} and E = {A–B, A–C, B–C, C–D}.

```fig 600x220 | Example graph (left) and its adjacency list (right)
circle a 60 50 22 | A
circle b 200 50 22 | B
circle c 60 170 22 | C
circle d 200 170 22 | D
line a b
line a c
line b c
line c d
box la 300 20 40 28 bold | A
box la1 370 20 40 28 | B
box la2 440 20 50 28 | C ⁄
box lb 300 70 40 28 bold | B
box lb1 370 70 40 28 | A
box lb2 440 70 50 28 | C ⁄
box lc 300 120 40 28 bold | C
box lc1 370 120 40 28 | A
box lc2 440 120 40 28 | B
box lc3 510 120 50 28 | D ⁄
box ld 300 170 40 28 bold | D
box ld1 370 170 50 28 | C ⁄
arrow la la1
arrow la1 la2
arrow lb lb1
arrow lb1 lb2
arrow lc lc1
arrow lc1 lc2
arrow lc2 lc3
arrow ld ld1
```

#### 1. Adjacency matrix (sequential representation)
An n × n matrix with **A[i][j] = 1 if there is an edge from i to j**, else 0 (or the weight for a weighted graph).

| | A | B | C | D |
|---|---|---|---|---|
| A | 0 | 1 | 1 | 0 |
| B | 1 | 0 | 1 | 0 |
| C | 1 | 1 | 0 | 1 |
| D | 0 | 0 | 1 | 0 |

Symmetric for undirected graphs. Space **O(V²)**; checking an edge is O(1); good for **dense** graphs.

#### 2. Adjacency list (linked representation)
An array of V head pointers; list i holds all vertices adjacent to i (figure above). Space **O(V + E)**; finding all neighbours is fast; good for **sparse** graphs. Each undirected edge appears twice.

#### 3. Adjacency multilist
For undirected graphs, each **edge is stored once** as a node shared by the lists of both its end-vertices:
`[mark | vertex1 | vertex2 | link for vertex1 | link for vertex2]`
The mark bit records whether the edge has been visited. Useful when edges themselves must be processed or marked (e.g. finding an Euler circuit).

#### Comparison
| | Adjacency matrix | Adjacency list | Multilist |
|---|---|---|---|
| Space | O(V²) | O(V + E) | O(V + E), each edge once |
| Is (u, v) an edge? | O(1) | O(degree) | O(degree) |
| All neighbours of u | O(V) | O(degree) | O(degree) |
| Best for | Dense graphs | Sparse graphs | Edge-based processing |

Other forms: **incidence matrix** (V × E) and **edge list**.

#### Conclusion
The matrix gives instant edge lookup at O(V²) space; lists store only existing edges and are the usual choice for large, sparse graphs.

### N u6-bfs-dfs | u6.traverse | Explain BFS and DFS algorithms with an example. How are they used to find connected components?
#### Example graph
Edges: A–B, A–C, B–D, B–E, C–F, E–F, and a separate component G–H.

```fig 600x220 | Graph for BFS and DFS (two components)
circle a 120 30 20 hl | A
circle b 60 100 20 | B
circle c 180 100 20 | C
circle d 30 180 20 | D
circle e 110 180 20 | E
circle f 200 180 20 | F
circle g 420 80 20 soft | G
circle h 520 80 20 soft | H
line a b
line a c
line b d
line b e
line c f
line e f
line g h
text 470 140 small muted | second component
```

#### Breadth First Search (uses a QUEUE)
Visit the start vertex, then **all its neighbours**, then their neighbours, level by level.
```
BFS(G, s)
1. mark s visited; ENQUEUE(s)
2. while queue not empty:
3.    u = DEQUEUE(); visit u
4.    for each neighbour v of u (alphabetical): if v not visited: mark v; ENQUEUE(v)
```

| Step | Dequeued | Queue after |
|---|---|---|
| 1 | A | B, C |
| 2 | B | C, D, E |
| 3 | C | D, E, F |
| 4 | D | E, F |
| 5 | E | F |
| 6 | F | – |

**BFS order: A B C D E F.** BFS gives shortest paths (in edges) in unweighted graphs.

#### Depth First Search (uses a STACK / recursion)
Go **as deep as possible** along one path, then backtrack.
```
DFS(G, u)
1. mark u visited; visit u
2. for each neighbour v of u (alphabetical): if v not visited: DFS(G, v)
```
Trace: A → B → D (dead end, back to B) → E → F → C (back up to A, done).
**DFS order: A B D E F C.** The edges used (A–B, B–D, B–E, E–F, F–C) form the **DFS tree**.

#### Connected components
Run BFS or DFS from any unvisited vertex; everything it reaches is **one connected component**. Repeat from the next unvisited vertex:
```
count = 0
for each vertex v: if v not visited: count = count + 1; DFS(G, v)   (label all reached vertices "count")
```
Here: DFS(A) reaches {A, B, C, D, E, F} → component 1; G is still unvisited → DFS(G) reaches {G, H} → component 2. **The graph has 2 connected components.**

#### Comparison
| | BFS | DFS |
|---|---|---|
| Data structure | Queue | Stack / recursion |
| Order | Level by level | Deep first, then backtrack |
| Shortest path (unweighted) | Yes | No |
| Uses | Shortest path, broadcasting, web crawling | Cycle detection, topological sort, components, maze solving |
| Time | O(V + E) with lists | O(V + E) with lists |

#### Conclusion
BFS and DFS both visit every vertex in O(V + E); BFS explores by distance, DFS by depth, and either one finds connected components.

### N u6-mst | u6.mst | Define spanning tree. Explain Prim's and Kruskal's algorithms to find a minimum cost spanning tree with an example.
#### Spanning tree
A **spanning tree** of a connected graph G with n vertices is a tree that contains all n vertices and **n − 1 edges** of G. A **minimum cost spanning tree (MST)** has the least total weight.

#### Example graph
Edges: A–B 4, A–C 3, B–C 1, B–D 2, C–D 4, C–E 6, D–E 5.

```fig 600x220 | Weighted graph; highlighted edges form the MST (cost 11)
circle a 60 110 22 | A
circle b 220 40 22 | B
circle c 220 180 22 | C
circle d 380 110 22 | D
circle e 540 110 22 | E
line a b | 4
line a c hl | 3
line b c hl | 1
line b d hl | 2
line c d | 4
line c e | 6
line d e hl | 5
```

#### Kruskal's algorithm (edge-based, greedy)
1. Sort all edges by weight.
2. Take the next lightest edge; **add it if it does not form a cycle** (check with union-find); else reject it.
3. Stop when n − 1 edges are chosen.

| Edge | Weight | Decision |
|---|---|---|
| B–C | 1 | accept |
| B–D | 2 | accept |
| A–C | 3 | accept |
| A–B | 4 | reject (cycle A–B–C) |
| C–D | 4 | reject (cycle B–C–D) |
| D–E | 5 | accept: 4 edges, stop |

**MST = {B–C, B–D, A–C, D–E}, cost = 1 + 2 + 3 + 5 = 11.** Time O(E log E).

#### Prim's algorithm (vertex-based, greedy)
1. Start from any vertex (say A); the tree contains A.
2. Repeatedly add the **cheapest edge joining a tree vertex to a non-tree vertex**.
3. Stop when all vertices are in the tree.

| Step | Tree vertices | Cheapest crossing edge |
|---|---|---|
| 1 | A | A–C (3) |
| 2 | A, C | C–B (1) |
| 3 | A, B, C | B–D (2) |
| 4 | A, B, C, D | D–E (5) |
| 5 | A, B, C, D, E | done |

Same MST, **cost 11**. Time O(V²) with a matrix, O(E log V) with a heap.

#### Prim vs Kruskal
| Prim | Kruskal |
|---|---|
| Grows one tree from a start vertex | Joins a forest of trees |
| Picks cheapest edge from the tree | Picks cheapest edge overall without cycle |
| Better for dense graphs | Better for sparse graphs |
| Uses a priority queue | Uses sorting + union-find |

#### Conclusion
Both greedy algorithms give a minimum spanning tree (the weight is unique even if the tree is not); MSTs are used for designing cheapest networks.

### N u6-dijkstra | u6.shortest | Explain Dijkstra's algorithm with an example. Also explain Warshall's algorithm for transitive closure and introduce activity networks.
#### Dijkstra's algorithm
Finds the **shortest path from a single source to all vertices** of a weighted graph with **non-negative** edge weights (greedy).
```
DIJKSTRA(G, s)
1. dist[v] = ∞ for all v; dist[s] = 0; S = ∅
2. while some vertex is not in S:
3.    u = vertex not in S with the smallest dist; add u to S
4.    for each edge (u, v) with weight w:
5.        if dist[u] + w < dist[v]: dist[v] = dist[u] + w; prev[v] = u     (relaxation)
```

#### Example (directed graph)
Edges: S→A 4, S→B 1, B→A 2, B→C 5, A→C 1, A→D 5, C→D 3.

```fig 600x210 | Graph for Dijkstra; highlighted = shortest-path tree from S
circle s 50 105 22 hl | S
circle a 230 40 22 | A
circle b 230 170 22 | B
circle c 400 105 22 | C
circle d 550 105 22 | D
arrow s a | 4
arrow s b hl | 1
arrow b a hl | 2
arrow b c | 5
arrow a c hl | 1
arrow a d | 5
arrow c d hl | 3
```

| Step | Vertex chosen | S | A | B | C | D |
|---|---|---|---|---|---|---|
| Init | – | 0 | ∞ | ∞ | ∞ | ∞ |
| 1 | S | **0** | 4 | 1 | ∞ | ∞ |
| 2 | B | | 3 | **1** | 6 | ∞ |
| 3 | A | | **3** | | 4 | 8 |
| 4 | C | | | | **4** | 7 |
| 5 | D | | | | | **7** |

Shortest distances: **A = 3 (S→B→A), B = 1, C = 4 (S→B→A→C), D = 7 (S→B→A→C→D).**
Time O(V²) with an array, O((V + E) log V) with a heap. It fails with negative edges (use Bellman-Ford).

#### Warshall's algorithm (transitive closure)
The **transitive closure** of a digraph is the matrix T with T[i][j] = 1 if there is **any path** from i to j. Warshall builds it from the adjacency matrix:
```
for k = 1 to n
  for i = 1 to n
    for j = 1 to n
      T[i][j] = T[i][j] OR (T[i][k] AND T[k][j])
```
After step k, T[i][j] = 1 if a path exists using only intermediate vertices 1…k. Time **O(n³)**. Example: edges 1→2, 2→3 → closure adds 1→3.
**Floyd-Warshall** is the same triple loop with D[i][j] = min(D[i][j], D[i][k] + D[k][j]), giving **all-pairs shortest paths**.

#### Activity networks
- **AOV network (Activity On Vertex)**: vertices are tasks, directed edges are precedence ("must finish before"). A valid order of tasks is a **topological sort**; the network must be acyclic.
- **AOE network (Activity On Edge)**: edges are activities with durations, vertices are events. The longest path from start to finish is the **critical path**; its activities cannot be delayed without delaying the project (CPM/PERT).

#### Conclusion
Dijkstra greedily fixes the nearest vertex each step to give single-source shortest paths; Warshall's triple loop gives reachability (and, as Floyd-Warshall, all-pairs distances).
