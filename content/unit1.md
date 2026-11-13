---
unit: 1
title: Introduction to Algorithms, Data Structures & Arrays
short: Algorithms & Arrays
syllabus: Abstract data types, fundamental and derived data types, representation, primitive data structures. Algorithm definition, analysis of algorithms, comparison of algorithms, top-down and bottom-up approaches, complexity (time and space), structured approach to programming. Arrays: representation of single and multidimensional arrays, address calculation using row and column major ordering, operations on arrays, applications: matrix multiplication, sparse matrix.
---

Unit I is the easiest scoring unit. Every paper asks either **asymptotic notations** or **"define data structure, types"**, and almost every paper has a **row/column-major address numerical** or a **sparse matrix** question. Learn the address formula by heart: it is a sure 7 marks.

### S u1s-ds | u1.intro | Define data structure. Differentiate primitive and non-primitive data structures.
A **data structure** is a way of organising and storing data in memory so that it can be accessed and modified efficiently.

| Primitive | Non-primitive |
|---|---|
| Basic types directly operated on by machine instructions | Built from primitive types |
| int, float, char, double, pointer | Arrays, lists, stacks, queues, trees, graphs |
| Hold a single value | Hold a group of values |

### S u1s-adt | u1.intro | Define abstract data type (ADT).
An **abstract data type** is a mathematical model of a data type defined only by its **values and the operations** on them, without saying how they are implemented. The user knows *what* each operation does, not *how*.

Example: the **Stack ADT** has the operations push, pop, peek and isEmpty; it can be implemented with an array or a linked list without changing how it is used.

### S u1s-ops | u1.intro | What are the operations performed on data structures?
1. **Traversing**: visiting each element once.
2. **Searching**: finding the location of a given value.
3. **Insertion**: adding a new element.
4. **Deletion**: removing an element.
5. **Sorting**: arranging elements in order.
6. **Merging**: combining two sorted structures into one.

### S u1s-algo | u1.algo | Define algorithm. Give its characteristics. How is it different from a program?
An **algorithm** is a finite sequence of well-defined steps that solves a problem. Characteristics (Knuth): **input** (zero or more), **output** (at least one), **definiteness** (each step is clear), **finiteness** (ends after finite steps) and **effectiveness** (each step is basic enough to be carried out).

An algorithm is language-independent and must terminate; a **program** is its implementation in a programming language and may run forever (e.g. an operating system).

### S u1s-bigo | u1.algo | Describe the Big Oh notation.
**f(n) = O(g(n))** if there exist positive constants c and n₀ such that **0 ≤ f(n) ≤ c·g(n) for all n ≥ n₀**. It gives an **upper bound** on the growth rate, so it is used for the **worst-case** running time.

Example: 3n² + 5n + 2 ≤ 10n² for n ≥ 1, so 3n² + 5n + 2 = O(n²).

### S u1s-sparse | u1.matrix | What is a sparse matrix? Give its properties.
A **sparse matrix** is a matrix in which **most elements are zero** (commonly, more than half). Properties: (1) storing it as a full 2-D array wastes memory; (2) only non-zero elements need to be stored, as **(row, column, value) triples** or in a linked list; (3) special forms are lower-triangular, upper-triangular and tridiagonal matrices.

### S u1s-arrays | u1.array | Differentiate between single and multidimensional arrays.
| One-dimensional array | Multidimensional array |
|---|---|
| Elements accessed with one index: A[i] | Need two or more indices: A[i][j] |
| Represents a list | Represents a table/matrix |
| Size = n elements | Size = m × n (2-D) elements |
| Address = B + w(i − L) | Address uses row- or column-major formula |

### L u1-ds-types | u1.intro | Define data structure. Describe its need and classify the types of data structures with examples.
#### Definition
A **data structure** is a particular way of organising data in the computer's memory so that it can be used efficiently. Data structure = organised data + allowed operations. Niklaus Wirth summed up its role as: **Algorithms + Data Structures = Programs**.

#### Need for data structures
1. **Efficiency**: the right structure makes searching, inserting and deleting fast (e.g. a BST searches in O(log n), a plain list in O(n)).
2. **Handling large data**: real applications store millions of records; they must be organised.
3. **Reusability**: ADTs like stack and queue are written once and reused.
4. **Abstraction**: the user works with operations (push, pop) and not with memory details.
5. **Memory management**: dynamic structures (linked lists) grow and shrink at run time.

#### Classification
```fig 600x250 | Classification of data structures
rbox ds 230 10 140 34 bold | Data structures
rbox p 60 80 140 34 | Primitive
rbox np 400 80 160 34 | Non-primitive
box p1 20 160 220 40 small | int, float, char, double, pointer
rbox l 300 160 120 34 | Linear
rbox nl 450 160 130 34 | Non-linear
text 360 225 small | Array, stack, queue, linked list
text 515 225 small | Tree, graph
arrow ds p
arrow ds np
arrow p p1
arrow np l
arrow np nl
```

- **Primitive**: basic types supported directly by the machine: int, float, char, double, pointer.
- **Non-primitive**: derived from primitive types.
  - **Linear**: elements form a sequence; each element has one predecessor and one successor. Examples: array, stack (LIFO), queue (FIFO), linked list.
  - **Non-linear**: an element can be connected to many others, forming a hierarchy or network. Examples: tree, graph.
- **Static vs dynamic**: arrays have a fixed size (static); linked lists grow at run time (dynamic).

| Linear | Non-linear |
|---|---|
| Single level, sequential | Multiple levels |
| Traversed in one run | Needs special traversals (BFS, DFS, inorder) |
| Easy to implement | More complex |
| Array, stack, queue | Tree, graph |

#### Operations
Traversing, searching, inserting, deleting, sorting and merging.

#### Choosing a data structure
Depends on the operations needed most often, the size of data, memory available and the time limits.

#### Conclusion
Data structures decide how efficiently a program runs. Choosing a stack for undo, a queue for scheduling, a tree for searching or a graph for networks is the first step in designing a good algorithm.

### L u1-asymptotic | u1.algo | Explain the concept of asymptotic notations. Compare Big O, Theta and Omega notations with examples.
#### Introduction
The **complexity** of an algorithm measures the resources it needs as a function of input size n: **time complexity** (number of basic steps) and **space complexity** (memory). Exact counts depend on the machine, so we compare algorithms by their **rate of growth** for large n. Asymptotic notations describe this growth and ignore constants and lower-order terms.

#### 1. Big O: upper bound
f(n) = O(g(n)) if there are constants c > 0 and n₀ such that **f(n) ≤ c·g(n) for all n ≥ n₀**. It says f grows **no faster** than g and is used for the **worst case**.
Example: f(n) = 3n + 2 ≤ 4n for n ≥ 2, so f(n) = O(n).

#### 2. Big Omega (Ω): lower bound
f(n) = Ω(g(n)) if **f(n) ≥ c·g(n) for all n ≥ n₀**. f grows **at least as fast** as g; used for the **best case**.
Example: 3n + 2 ≥ 3n for all n ≥ 1, so f(n) = Ω(n).

#### 3. Theta (Θ): tight bound
f(n) = Θ(g(n)) if **c₁·g(n) ≤ f(n) ≤ c₂·g(n) for all n ≥ n₀**. f grows **exactly as fast** as g.
Example: 3n ≤ 3n + 2 ≤ 4n for n ≥ 2, so f(n) = Θ(n).

```fig 600x230 | Big O, Omega and Theta: f(n) is bounded above, below, or both by multiples of g(n) after n₀
line 30,200 280,200
line 30,200 30,20
path | M 30 190 C 110 150 170 80 270 30
path dash | M 30 195 C 120 170 190 120 270 85
text 255 20 small hl | c₂·g(n)
text 255 75 small | f(n)
line 110,200 110,30 dash
text 110 215 small | n₀
text 150 225 small muted | f(n) = O(g(n)): f stays below c·g(n)
line 330,200 580,200
line 330,200 330,20
path | M 330 190 C 420 160 480 100 570 40
path dash | M 330 195 C 430 180 500 150 570 110
path dash | M 330 185 C 410 130 470 60 560 20
text 545 105 small | c₁·g(n)
text 555 50 small | f(n)
text 520 15 small | c₂·g(n)
text 455 225 small muted | f(n) = Θ(g(n)): sandwiched between c₁g and c₂g
```

#### Comparison
| Notation | Bound | Meaning | Used for | Example for 3n² + 2n |
|---|---|---|---|---|
| O | Upper | grows no faster than | Worst case | O(n²), also O(n³) |
| Ω | Lower | grows at least as fast | Best case | Ω(n²), also Ω(n) |
| Θ | Tight | grows exactly as | Exact order | Θ(n²) only |

#### Common growth rates
O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(n³) < O(2ⁿ) < O(n!).
Examples: array access O(1), binary search O(log n), linear search O(n), merge sort O(n log n), bubble sort O(n²).

#### Conclusion
Asymptotic notations let us compare algorithms independent of machine and language. f(n) = Θ(g(n)) holds exactly when f(n) = O(g(n)) and f(n) = Ω(g(n)).

### N u1-address | u1.array | Explain row-major and column-major representation of a 2-D array. Data[20][50] has 4 bytes per element and base address 2000; find the address of Data[10][10] in both orders.
#### Representation of 2-D arrays
Memory is one-dimensional, so a 2-D array A[m][n] must be **linearised**:
- **Row-major order** (used by C): the elements are stored **row by row**: all of row 0, then row 1, …
- **Column-major order** (used by FORTRAN): the elements are stored **column by column**.

For A[2][3] with elements a₀₀ … a₁₂:

```fig 600x170 | Storage of A[2][3] in row-major (top) and column-major (bottom) order
box r1 20 30 90 34 hl | a00
box r2 110 30 90 34 hl | a01
box r3 200 30 90 34 hl | a02
box r4 290 30 90 34 | a10
box r5 380 30 90 34 | a11
box r6 470 30 90 34 | a12
text 300 18 small muted | row 0 first, then row 1
box c1 20 110 90 34 hl | a00
box c2 110 110 90 34 | a10
box c3 200 110 90 34 hl | a01
box c4 290 110 90 34 | a11
box c5 380 110 90 34 hl | a02
box c6 470 110 90 34 | a12
text 300 98 small muted | column 0 first, then column 1, column 2
```

#### Address formulas
For an array A[m][n] with base address B, element size w bytes and lower bounds 0:
- **Row-major:** Loc(A[i][j]) = B + w × (i × n + j)
- **Column-major:** Loc(A[i][j]) = B + w × (j × m + i)

With lower bounds L_r and L_c: Row-major = B + w[(i − L_r)·n + (j − L_c)], Column-major = B + w[(j − L_c)·m + (i − L_r)].

#### Numerical
Given: Data[20][50], so m = 20 rows, n = 50 columns; w = 4; B = 2000; i = 10, j = 10 (indices start at 0).

**(i) Row-major**
Loc = 2000 + 4 × (10 × 50 + 10) = 2000 + 4 × 510 = 2000 + 2040 = **4040**

**(ii) Column-major**
Loc = 2000 + 4 × (10 × 20 + 10) = 2000 + 4 × 210 = 2000 + 840 = **2840**

> If the question says indices start at 1, use (i − 1) and (j − 1) instead. Always state the assumption in the exam.

#### Second example (AKTU 2022-23)
Arr[50][100], row-major, w = 4, B = 1000: Loc(Arr[20][50]) = 1000 + 4 × (20 × 100 + 50) = 1000 + 8200 = **9200**.

#### Operations on arrays
Traversal O(n), insertion and deletion O(n) (elements must be shifted), access by index O(1), search O(n) or O(log n) if sorted.

#### Conclusion
Row-major stores rows contiguously and column-major stores columns; the formula is chosen to match the order, and any element is reached in O(1) time.

### L u1-sparse | u1.matrix | What is a sparse matrix? How can sparse matrices be represented efficiently in memory?
#### Definition
A matrix is **sparse** when most of its elements are **zero**. Storing it as an ordinary m × n array wastes memory and time on zeros. Example: a 1000 × 1000 matrix with 2000 non-zeros needs 10⁶ cells, but only 2000 are useful.

Example matrix (4 × 5, 5 non-zeros):

| | c0 | c1 | c2 | c3 | c4 |
|---|---|---|---|---|---|
| r0 | 0 | 0 | 3 | 0 | 4 |
| r1 | 0 | 0 | 5 | 7 | 0 |
| r2 | 0 | 0 | 0 | 0 | 0 |
| r3 | 0 | 2 | 0 | 0 | 0 |

#### 1. Array (triplet) representation
Store each non-zero as a triple (row, column, value). Row 0 of the table holds the dimensions and the count.

| Row | Column | Value |
|---|---|---|
| 4 | 5 | 5 |
| 0 | 2 | 3 |
| 0 | 4 | 4 |
| 1 | 2 | 5 |
| 1 | 3 | 7 |
| 3 | 1 | 2 |

Space: 3(t + 1) instead of m × n, where t = number of non-zeros.

#### 2. Linked list representation
Each non-zero becomes a node **(row, col, value, next)**; the nodes are linked in row-major order. A better form uses **header nodes** for each row and column, with each node linked both to the next node in its row and the next in its column (orthogonal list).

```fig 600x150 | Linked list representation of the sparse matrix: one node per non-zero (row, col, value)
box h 10 55 70 40 bold | START
box n1 110 55 80 40 | 0,2,3
box n2 220 55 80 40 | 0,4,4
box n3 330 55 80 40 | 1,2,5
box n4 440 55 80 40 | 1,3,7
box n5 520 110 70 34 | 3,1,2
arrow h n1
arrow n1 n2
arrow n2 n3
arrow n3 n4
arrow n4 n5
text 555 160 small muted | next = NULL
```

#### Special sparse matrices
- **Lower triangular**: A[i][j] = 0 for j > i; store n(n+1)/2 elements in a 1-D array, index = i(i+1)/2 + j.
- **Upper triangular**: A[i][j] = 0 for i > j.
- **Tridiagonal**: non-zeros only on the main diagonal and the two next to it: 3n − 2 elements.

#### Advantages
1. Saves memory. 2. Operations (addition, transpose, multiplication) skip zeros and run faster. 3. Linked form handles changes in the number of non-zeros.

#### Conclusion
Sparse matrices are stored as triplets or linked lists so that memory and time depend on the number of non-zeros, not on m × n. They are used in graphs, scientific computing and machine learning.

### N u1-matmul | u1.matrix | Write an algorithm/C code to multiply two matrices and find its time complexity. Also write an algorithm to transpose a matrix.
#### Matrix multiplication
If A is m × n and B is n × p, then C = A × B is m × p with
**C[i][j] = Σ (k = 0 to n − 1) A[i][k] × B[k][j]**.
Multiplication is possible only when columns of A = rows of B.

```fig 600x170 | Element C[i][j] = row i of A · column j of B
box a 30 40 150 100 | A (m × n)
box ar 30 75 150 22 hl | row i
box b 230 20 110 140 | B (n × p)
box bc 275 20 26 140 hl | j
box c 420 40 150 100 | C (m × p)
box cc 485 75 26 22 hl | Cij
text 205 90 bold | ×
text 385 90 bold | =
```

#### Algorithm
```
MATMUL(A, B, C, m, n, p)
1. for i = 0 to m − 1
2.   for j = 0 to p − 1
3.     C[i][j] = 0
4.     for k = 0 to n − 1
5.       C[i][j] = C[i][j] + A[i][k] * B[k][j]
6. return C
```

#### C code for 3 × 3 matrices
```
#include <stdio.h>
int main() {
    int a[3][3], b[3][3], c[3][3], i, j, k;
    for (i = 0; i < 3; i++) for (j = 0; j < 3; j++) scanf("%d", &a[i][j]);
    for (i = 0; i < 3; i++) for (j = 0; j < 3; j++) scanf("%d", &b[i][j]);
    for (i = 0; i < 3; i++)
        for (j = 0; j < 3; j++) {
            c[i][j] = 0;
            for (k = 0; k < 3; k++) c[i][j] += a[i][k] * b[k][j];
        }
    for (i = 0; i < 3; i++) { for (j = 0; j < 3; j++) printf("%d ", c[i][j]); printf("\n"); }
    return 0;
}
```

#### Example
A = [[1, 2], [3, 4]], B = [[5, 6], [7, 8]]
C[0][0] = 1·5 + 2·7 = 19, C[0][1] = 1·6 + 2·8 = 22, C[1][0] = 3·5 + 4·7 = 43, C[1][1] = 3·6 + 4·8 = 50.
**C = [[19, 22], [43, 50]]**

#### Time complexity
Three nested loops: m × p × n multiplications. For square n × n matrices, **T(n) = n³ = O(n³)**; extra space O(n²) for C.

#### Transpose
```
TRANSPOSE(A, T, m, n)
1. for i = 0 to m − 1
2.   for j = 0 to n − 1
3.     T[j][i] = A[i][j]
```
Time O(m × n). For a sparse matrix in triplet form, swap the row and column of each triple and sort by the new row.

#### Conclusion
Matrix multiplication is the classic application of 2-D arrays; the straightforward method takes O(n³) time.
