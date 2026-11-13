---
unit: 5
title: Searching, Sorting, Search Trees & Hashing
short: Search, Sort & Hash
syllabus: Searching: sequential search, binary search, comparison and analysis. Internal sorting: insertion sort, selection, bubble sort, quick sort, two way merge sort, heap sort, radix sort, practical consideration for internal sorting. Search trees: binary search trees (BST), insertion and deletion in BST, complexity of search algorithm, AVL trees, introduction to m-way search trees, B trees & B+ trees. Hashing: hash function, collision resolution strategies. Storage management: garbage collection and compaction.
---

Unit V is the **biggest scoring unit**: sorting (quick, merge, heap) came in **every paper**, hashing in 7 of 8, and BST, B-tree and AVL questions are regular. Most questions are numericals: practise the traces in table form exactly as below.

### S u5s-seq | u5.search | What is the worst-case time complexity of sequential search?
Sequential (linear) search compares the key with each element one by one. In the **worst case** (key is the last element or not present) it makes **n comparisons**, so the worst case is **O(n)**. Best case O(1) (key at the first position); average about (n + 1)/2 comparisons, still O(n).

### S u5s-dc | u5.sortadv | What is the basic idea behind divide and conquer?
**Divide and conquer** solves a problem in three steps: **Divide** it into smaller subproblems of the same type, **Conquer** each subproblem recursively (solving tiny ones directly), and **Combine** their solutions into the solution of the original problem.

Examples: binary search, merge sort, quick sort, Strassen's matrix multiplication. Merge sort satisfies T(n) = 2T(n/2) + O(n) = O(n log n).

### S u5s-counting | u5.sortadv | What is a non-comparison sort? What is the basic idea behind counting sort?
A **non-comparison sort** orders keys without comparing them with each other, using their values directly. Examples: **counting sort, radix sort, bucket sort**. They beat the Ω(n log n) limit of comparison sorts.

**Counting sort**: for integers in range 0..k, count how many times each value occurs (array C), turn the counts into running totals (positions), then place each element at its position in the output array. Time **O(n + k)**; stable.

### S u5s-selection | u5.sortsimple | Apply selection sort on 5, 8, 6, 2, 1, 3.
Each pass selects the minimum of the unsorted part and swaps it to the front.

| Pass | Minimum | Array after swap |
|---|---|---|
| 1 | 1 | **1**, 8, 6, 2, 5, 3 |
| 2 | 2 | 1, **2**, 6, 8, 5, 3 |
| 3 | 3 | 1, 2, **3**, 8, 5, 6 |
| 4 | 5 | 1, 2, 3, **5**, 8, 6 |
| 5 | 6 | 1, 2, 3, 5, **6**, 8 |

Sorted: **1, 2, 3, 5, 6, 8**. Time O(n²).

### S u5s-quick-time | u5.sortadv | Write the time complexity of quick sort.
| Case | When | Time |
|---|---|---|
| Best | Pivot splits the array into two equal halves | O(n log n) |
| Average | Random data | O(n log n) |
| Worst | Pivot is always the smallest/largest (already sorted input) | O(n²) |

Space: O(log n) recursion stack on average, O(n) in the worst case. Quick sort is not stable but is in-place.

### S u5s-successor | u5.bst | Discuss inorder successor and inorder predecessor in a BST.
In a BST, inorder traversal lists keys in sorted order.
- **Inorder successor** of node X = the **next larger key**: if X has a right subtree, it is the **leftmost (minimum) node of the right subtree**; otherwise it is the nearest ancestor of which X is in the left subtree.
- **Inorder predecessor** = the **next smaller key**: the **rightmost (maximum) node of the left subtree**, or the nearest ancestor of which X is in the right subtree.

They are used when deleting a node with two children.

### S u5s-garbage | u5.storage | Explain garbage collection and compaction with example.
**Garbage collection** reclaims memory blocks that are no longer reachable by the program (e.g. after `p = NULL` the node p pointed to is garbage). It usually works in two phases: **mark** every block reachable from the program's pointers, then **sweep** (collect) every unmarked block into the free list.

**Compaction** moves all used blocks to one end of memory so the free space forms one large contiguous block, removing external fragmentation (e.g. free holes of 10 KB, 20 KB and 30 KB become one 60 KB block). Pointers to moved blocks must be updated.

### S u5s-balanced | u5.avl | Write a short note on balanced binary tree.
A **balanced binary tree** is one whose height stays **O(log n)**: for every node, the heights of the left and right subtrees differ by at most a fixed amount. Example: an **AVL tree**, where the balance factor = height(left) − height(right) ∈ {−1, 0, +1} at every node. Balance keeps search, insertion and deletion at O(log n), unlike a skewed BST that degrades to O(n). Other examples: red-black trees, B-trees.

### L u5-search | u5.search | Explain linear search and binary search with algorithms, examples and complexities. How does binary search follow divide and conquer?
#### Linear (sequential) search
Compare the key with each element from the first to the last until it is found or the list ends. Works on **unsorted** data.
```
LINEAR(A, n, key)
1. for i = 0 to n − 1
2.   if A[i] = key then return i
3. return −1
```

#### Binary search
Works only on a **sorted** array. Compare the key with the **middle** element; if equal, stop; if smaller, search the left half; otherwise the right half. This is **divide and conquer**: the problem is divided into one half, conquered recursively, and no combine step is needed.
```
BINARY(A, low, high, key)          (recursive)
1. if low > high return −1
2. mid = (low + high) / 2
3. if A[mid] = key return mid
4. if key < A[mid] return BINARY(A, low, mid − 1, key)
5. else return BINARY(A, mid + 1, high, key)
```

#### Example
A = [3, 9, 14, 22, 31, 45, 58, 70, 81], key = 58.

| Step | low | high | mid | A[mid] | Action |
|---|---|---|---|---|---|
| 1 | 0 | 8 | 4 | 31 | 58 > 31 → right half |
| 2 | 5 | 8 | 6 | 58 | **found at index 6** |

Linear search would need 7 comparisons; binary search needs 2.

```fig 600x130 | Binary search for 58: the search space halves every step
box c0 30 30 60 32 dash | 3
box c1 90 30 60 32 dash | 9
box c2 150 30 60 32 dash | 14
box c3 210 30 60 32 dash | 22
box c4 270 30 60 32 | 31
box c5 330 30 60 32 | 45
box c6 390 30 60 32 hl | 58
box c7 450 30 60 32 | 70
box c8 510 30 60 32 | 81
text 300 85 small | mid 1 = index 4
text 420 85 small hl | mid 2 = index 6 (found)
text 300 115 small muted | grey = discarded after step 1
```

#### Complexity
Recurrence: T(n) = T(n/2) + c → **T(n) = O(log n)**.

| | Linear search | Binary search |
|---|---|---|
| Data required | Any order | Sorted array |
| Best case | O(1) | O(1) |
| Worst/average case | O(n) | O(log n) |
| Method | Sequential | Divide and conquer |
| Data structure | Array or linked list | Array (random access) |
| For n = 1,000,000 | up to 10⁶ comparisons | about 20 |

#### Largest and second largest in one pass
```
max1 = max2 = −∞
for each x in A: if x > max1 { max2 = max1; max1 = x } else if x > max2 and x ≠ max1 { max2 = x }
```

#### Conclusion
Linear search is simple and works on any list; binary search needs sorted data but is far faster, O(log n), because it halves the search space each step.

### N u5-insertion | u5.sortsimple | Write the insertion sort algorithm and analyse it. Illustrate it on A = <16, 4, 13, 5, 2, 10, 30, 17, 6>. Compare bubble, selection and insertion sort.
#### Idea
Insertion sort builds the sorted list one element at a time, like arranging playing cards in the hand: take the next element (key) and **insert it into its correct place** among the already sorted elements on its left, shifting larger elements one step right.

#### Algorithm and C function
```
void insertionSort(int a[], int n) {
    for (int i = 1; i < n; i++) {
        int key = a[i], j = i - 1;
        while (j >= 0 && a[j] > key) { a[j + 1] = a[j]; j--; }
        a[j + 1] = key;
    }
}
```

#### Trace
| Pass | Key | Array after the pass (sorted part in bold) |
|---|---|---|
| 1 | 4 | **4, 16**, 13, 5, 2, 10, 30, 17, 6 |
| 2 | 13 | **4, 13, 16**, 5, 2, 10, 30, 17, 6 |
| 3 | 5 | **4, 5, 13, 16**, 2, 10, 30, 17, 6 |
| 4 | 2 | **2, 4, 5, 13, 16**, 10, 30, 17, 6 |
| 5 | 10 | **2, 4, 5, 10, 13, 16**, 30, 17, 6 |
| 6 | 30 | **2, 4, 5, 10, 13, 16, 30**, 17, 6 |
| 7 | 17 | **2, 4, 5, 10, 13, 16, 17, 30**, 6 |
| 8 | 6 | **2, 4, 5, 6, 10, 13, 16, 17, 30** |

```fig 600x120 | Pass 3: key 5 is inserted after 4; 13 and 16 shift right
box a0 60 40 60 34 | 4
box a1 120 40 60 34 hl | 5
box a2 180 40 60 34 | 13
box a3 240 40 60 34 | 16
box a4 300 40 60 34 dash | 2
box a5 360 40 60 34 dash | 10
arrow 210,30 270,30 bend=-15 | shift
text 390 100 small muted | unsorted part
text 150 100 small muted | sorted part
```

#### Analysis
- **Best case** (already sorted): one comparison per pass → n − 1 comparisons → **O(n)**.
- **Worst case** (reverse sorted): pass i makes i comparisons → 1 + 2 + … + (n − 1) = n(n − 1)/2 → **O(n²)**.
- **Average case**: about n²/4 comparisons → **O(n²)**.
- Space **O(1)** (in-place); **stable**; good for small or nearly sorted data.

#### Bubble sort
Repeatedly compares adjacent elements and swaps them if out of order; after pass i the i-th largest element "bubbles" to the end. With a swapped-flag the best case is O(n); worst/average O(n²).

#### Comparison of simple sorts
| | Bubble | Selection | Insertion |
|---|---|---|---|
| Best | O(n) (with flag) | O(n²) | O(n) |
| Worst | O(n²) | O(n²) | O(n²) |
| Swaps (worst) | O(n²) | O(n), fewest | O(n²) shifts |
| Stable | Yes | No | Yes |
| In-place | Yes | Yes | Yes |

#### Practical considerations for internal sorting
Size of data, whether it is nearly sorted, stability needed, memory available and cost of moving records. Insertion sort is used for small n (even inside quick sort/Timsort); merge sort when stability and guaranteed O(n log n) are needed; quick sort for average speed; heap sort for O(1) extra space with a guaranteed O(n log n); radix sort for fixed-length integer keys.

#### Conclusion
Insertion sort is simple, stable and adaptive: linear on sorted input and quadratic otherwise.

### N u5-quick-merge | u5.sortadv | Explain divide and conquer. Write quick sort and apply it on 36, 15, 40, 1, 60, 20, 55, 25, 50, 20. How do merge sort and quick sort differ?
#### Divide and conquer
Divide the problem into subproblems, conquer them recursively, and combine the results.
- **Merge sort**: easy divide (split in the middle), hard combine (merge two sorted halves).
- **Quick sort**: hard divide (partition around a pivot), no combine step.

#### Quick sort algorithm (first element as pivot)
```
QUICKSORT(A, low, high)
1. if low < high
2.   p = PARTITION(A, low, high)
3.   QUICKSORT(A, low, p − 1)
4.   QUICKSORT(A, p + 1, high)

PARTITION(A, low, high)
1. pivot = A[low]; i = low; j = high
2. while i < j
3.   while A[i] ≤ pivot and i < high: i = i + 1
4.   while A[j] > pivot: j = j − 1
5.   if i < j: swap A[i], A[j]
6. swap A[low], A[j]; return j
```

#### Trace on 36, 15, 40, 1, 60, 20, 55, 25, 50, 20
First partition, pivot = 36:
- i stops at 40, j stops at 20 (last) → swap: 36, 15, **20**, 1, 60, 20, 55, 25, 50, **40**
- i stops at 60, j stops at 25 → swap: 36, 15, 20, 1, **25**, 20, 55, **60**, 50, 40
- i stops at 55 (index 6), j stops at 20 (index 5); i > j → swap pivot with A[5].

Result: **[20, 15, 20, 1, 25] 36 [55, 60, 50, 40]**

| Sub-array | Pivot | After partition |
|---|---|---|
| 20, 15, 20, 1, 25 | 20 | [1, 15, 20] **20** [25] |
| 1, 15, 20 | 1 | **1** [15, 20] |
| 15, 20 | 15 | **15** [20] |
| 55, 60, 50, 40 | 55 | [50, 40] **55** [60] |
| 50, 40 | 50 | [40] **50** |

**Sorted: 1, 15, 20, 20, 25, 36, 40, 50, 55, 60**

```tree 560x230 | Recursion tree of quick sort (pivots in each call)
36
  20
    1
      15
    25
  55
    50
      40
    60
```

#### Merge sort
```
MERGESORT(A, l, r)
1. if l < r
2.   m = (l + r) / 2
3.   MERGESORT(A, l, m); MERGESORT(A, m + 1, r)
4.   MERGE(A, l, m, r)      (merge two sorted halves using a temporary array)
```
Example: 38 27 43 3 → (38 27)(43 3) → (27 38)(3 43) → **3 27 38 43**.
Recurrence T(n) = 2T(n/2) + n → **O(n log n)** in all cases; extra space O(n).

#### Comparison
| | Merge sort | Quick sort |
|---|---|---|
| Divide | Split in the middle (trivial) | Partition around pivot (main work) |
| Combine | Merge (main work) | Nothing |
| Best / average | O(n log n) | O(n log n) |
| Worst | O(n log n) | O(n²) (sorted input, bad pivot) |
| Extra space | O(n) | O(log n) stack, in-place |
| Stable | Yes | No |
| Used for | Linked lists, external sorting | Fast in-memory sorting |

#### Conclusion
Both are divide-and-conquer O(n log n) sorts on average; merge sort guarantees it at the cost of extra memory, quick sort is in-place and usually faster but can degrade to O(n²).

### N u5-heap | u5.sortadv | What is a heap? Write the heap sort algorithm. Build the max-heap for 1, 2, 3, …, 10 and explain how it sorts the array.
#### Heap
A **max-heap** is a **complete binary tree** in which every node's key is **≥ the keys of its children**, so the maximum is at the root. (Min-heap: ≤.) Being complete, it is stored in an array: children of index i (0-based) are at 2i + 1 and 2i + 2.

#### Algorithm
```
HEAPSORT(A, n)
1. BUILD-MAX-HEAP(A, n):  for i = n/2 − 1 down to 0: HEAPIFY(A, n, i)
2. for last = n − 1 down to 1:
3.     swap A[0], A[last]          (largest goes to its final place)
4.     HEAPIFY(A, last, 0)          (restore heap on the remaining elements)

HEAPIFY(A, n, i)
1. largest = i; l = 2i + 1; r = 2i + 2
2. if l < n and A[l] > A[largest]: largest = l
3. if r < n and A[r] > A[largest]: largest = r
4. if largest ≠ i: swap A[i], A[largest]; HEAPIFY(A, n, largest)
```

#### Building the max-heap for 1, 2, …, 10
Start: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]. Heapify from i = 4 down to 0:

| i (value) | Action | Array |
|---|---|---|
| 4 (5) | swap with child 10 | 1, 2, 3, 4, 10, 6, 7, 8, 9, 5 |
| 3 (4) | swap with child 9 | 1, 2, 3, 9, 10, 6, 7, 8, 4, 5 |
| 2 (3) | swap with child 7 | 1, 2, 7, 9, 10, 6, 3, 8, 4, 5 |
| 1 (2) | swap with 10, then with 5 | 1, 10, 7, 9, 5, 6, 3, 8, 4, 2 |
| 0 (1) | swap with 10, then 9, then 8 | **10, 9, 7, 8, 5, 6, 3, 1, 4, 2** |

```tree 560x240 | Max-heap built from 1 … 10
10
  9
    8
      1
      4
    5
      2
  7
    6
    3
```

#### Sorting phase
1. Swap root 10 with the last element 2 → 10 is in place; heapify the first 9 → root 9.
2. Swap 9 with the last of the heap → heapify → root 8, and so on.
After n − 1 swaps the array is **1, 2, 3, …, 10** in ascending order.

#### Complexity
- Build-heap: **O(n)**. Each of the n − 1 heapify calls: O(log n).
- Heap sort: **O(n log n)** in best, average and worst cases; **in-place** (O(1) extra); **not stable**.

#### Radix sort (related non-comparison sort)
Sort numbers digit by digit from the least significant digit using a stable bucket/counting pass per digit. Example 170, 45, 75, 90, 802, 24, 2, 66 → after units: 170 90 802 2 24 45 75 66 → tens: 802 2 24 45 66 170 75 90 → hundreds: **2 24 45 66 75 90 170 802**. Time O(d(n + k)).

#### Conclusion
Heap sort uses the max-heap to pick the largest remaining element in O(log n), giving a guaranteed O(n log n) in-place sort; it also powers priority queues.

### N u5-bst | u5.bst | Define binary search tree. Create a BST for 20, 10, 25, 5, 15, 22, 30, 3, 14, 13 and explain insertion, deletion and search with their complexity.
#### BST
A **binary search tree** is a binary tree in which, for every node, **all keys in the left subtree are smaller** and **all keys in the right subtree are larger** than the node's key. Its inorder traversal gives the keys in sorted order.

#### Insertion (recursive)
```
struct node *insert(struct node *t, int key) {
    if (t == NULL) { t = malloc(sizeof *t); t->info = key; t->left = t->right = NULL; }
    else if (key < t->info) t->left = insert(t->left, key);
    else if (key > t->info) t->right = insert(t->right, key);   /* duplicates ignored */
    return t;
}
```

#### Construction for 20, 10, 25, 5, 15, 22, 30, 3, 14, 13
| Key | Path taken | Placed as |
|---|---|---|
| 20 | – | root |
| 10 | 10 < 20 | left of 20 |
| 25 | 25 > 20 | right of 20 |
| 5 | < 20, < 10 | left of 10 |
| 15 | < 20, > 10 | right of 10 |
| 22 | > 20, < 25 | left of 25 |
| 30 | > 20, > 25 | right of 25 |
| 3 | < 20, < 10, < 5 | left of 5 |
| 14 | < 20, > 10, < 15 | left of 15 |
| 13 | < 20, > 10, < 15, < 14 | left of 14 |

```tree 560x260 | BST for 20, 10, 25, 5, 15, 22, 30, 3, 14, 13
20
  10
    5
      3
    15
      14
        13
  25
    22
    30
```
(3, 14 and 13 are left children.) Inorder: 3 5 10 13 14 15 20 22 25 30.

#### Search
```
SEARCH(t, key): while t ≠ NULL: if key = t.info return t; t = (key < t.info) ? t.left : t.right; return NULL
```

#### Deletion: three cases
1. **Leaf** (e.g. 13): just remove it.
2. **One child** (e.g. 5, child 3): link the parent directly to the child.
3. **Two children** (e.g. 10): replace its key with its **inorder successor** (smallest in the right subtree, 13) or predecessor (5), then delete that successor node, which has at most one child.

#### Complexity
| | Balanced BST | Skewed BST |
|---|---|---|
| Search / insert / delete | O(log n) | O(n) |

Inserting already sorted keys (e.g. 9, 2, 3, 4, 5, … mostly increasing) gives a skewed tree; this is why AVL trees are used.

#### Conclusion
A BST keeps keys ordered so that search, insertion and deletion follow one root-to-leaf path: O(h), where h is the height.

### L u5-avl | u5.avl | What is an AVL tree? What is the balance factor? Explain LL, RR, LR and RL rotations with examples.
#### AVL tree
An **AVL tree** (Adelson-Velsky and Landis, 1962) is a **height-balanced binary search tree**: for every node,
**Balance factor (BF) = height(left subtree) − height(right subtree) ∈ {−1, 0, +1}**.
Its height is O(log n), so search, insertion and deletion take **O(log n)**.

After an insertion, if some node's BF becomes +2 or −2, the tree is rebalanced by a **rotation** at the nearest unbalanced ancestor (the pivot).

#### The four cases
| Case | New node inserted in | Fix |
|---|---|---|
| **LL** | Left subtree of the left child (BF = +2, child +1) | Single **right** rotation |
| **RR** | Right subtree of the right child (BF = −2, child −1) | Single **left** rotation |
| **LR** | Right subtree of the left child (BF = +2, child −1) | Left rotation on child, then right rotation |
| **RL** | Left subtree of the right child (BF = −2, child +1) | Right rotation on child, then left rotation |

#### Examples
- **LL**: insert 30, 20, 10 → 30 has BF +2 → rotate right → **20 (10, 30)**.
- **RR**: insert 10, 20, 30 → 10 has BF −2 → rotate left → **20 (10, 30)**.
- **LR**: insert 30, 10, 20 → rotate 10 left (20 becomes left child of 30), then rotate 30 right → **20 (10, 30)**.
- **RL**: insert 10, 30, 20 → rotate 30 right, then rotate 10 left → **20 (10, 30)**.

```fig 600x200 | LL case: right rotation at 30 (BF +2)
circle a 80 30 20 hl | 30
circle b 50 90 20 | 20
circle c 20 150 20 | 10
line a b
line b c
text 130 30 small hl | BF +2
text 105 90 small | BF +1
arrow 200,90 330,90 | rotate right
circle d 450 50 20 hl | 20
circle e 390 130 20 | 10
circle f 510 130 20 | 30
line d e
line d f
text 450 185 small muted | balanced: all BF = 0
```

#### Worked insertion: 10, 20, 30, 40, 50, 25
1. 10, 20, 30 → RR at 10 → 20 (10, 30).
2. 40 → right of 30 (balanced).
3. 50 → 30 gets BF −2 (RR) → left rotation at 30 → 20 (10, 40 (30, 50)).
4. 25 → goes left of 30; the root 20 gets BF −2 and its right child 40 has BF +1 → **RL**: right rotate 40, then left rotate 20.

```tree 520x200 | Final AVL tree after inserting 10, 20, 30, 40, 50, 25
30
  20
    10
    25
  40
    50
```
(50 is the right child of 40.) All balance factors are within −1 … +1.

#### Comparison with a plain BST
| | BST | AVL |
|---|---|---|
| Height | up to n − 1 | ≤ 1.44 log₂ n |
| Search | O(n) worst | O(log n) |
| Insert/delete | Simple | Needs rotations |

#### Conclusion
AVL trees keep a BST balanced with at most two rotations per insertion, guaranteeing O(log n) operations.

### N u5-btree | u5.btree | What is a B-tree? Write its properties. Construct a B-tree of order 3 for 10, 20, 30, 40, 50, 60, 70, 80, 90. Differentiate between B-tree and B+ tree.
#### m-way search tree and B-tree
An **m-way search tree** lets each node have up to m children and m − 1 keys in sorted order. A **B-tree of order m** is a balanced m-way search tree, designed for disks, with these properties:
1. Every node has at most **m children** and **m − 1 keys**.
2. Every internal node except the root has at least **⌈m/2⌉ children**.
3. The root has at least 2 children (unless it is a leaf).
4. **All leaves are at the same level.**
5. Keys in a node are sorted, and separate the key ranges of the children.

**Insertion**: insert into the proper leaf; if it overflows (m keys), **split** it: the middle key moves up to the parent, the left and right halves become two nodes. A split can propagate up to the root, which is how the tree grows in height.

#### Order 3 (max 2 keys per node): 10, 20, …, 90
| Insert | Action | Tree |
|---|---|---|
| 10, 20 | leaf [10 20] | [10 20] |
| 30 | [10 20 30] overflows → 20 up | [20] → [10] [30] |
| 40 | added to leaf | [20] → [10] [30 40] |
| 50 | [30 40 50] splits → 40 up | [20 40] → [10] [30] [50] |
| 60 | added | [20 40] → [10] [30] [50 60] |
| 70 | [50 60 70] splits → 60 up; root [20 40 60] splits → 40 up | [40] → [20], [60] |
| 80 | added to leaf [70 80] | |
| 90 | [70 80 90] splits → 80 up to [60 80] | final |

```fig 600x200 | Final B-tree of order 3
box r 260 20 80 32 hl | 40
box l 120 85 80 32 | 20
box m 380 85 110 32 | 60 | 80
box l1 60 155 60 30 | 10
box l2 160 155 60 30 | 30
box l3 320 155 60 30 | 50
box l4 400 155 60 30 | 70
box l5 480 155 60 30 | 90
arrow r l
arrow r m
arrow l l1
arrow l l2
arrow m l3
arrow m l4
arrow m l5
```

#### B-tree vs B+ tree
In a **B+ tree**, **all keys and data are stored in the leaves**; internal nodes hold only copies of keys as an index, and the **leaves are linked** in a sequential list.

| B-tree | B+ tree |
|---|---|
| Data pointers in all nodes | Data only in leaf nodes |
| Keys are not repeated | Internal keys are repeated in the leaves |
| Leaves are not linked | Leaves linked for sequential access |
| Search may end at an internal node | Every search ends at a leaf |
| Range queries are slower | Range queries and full scans are fast |

**Prefer a B+ tree** when range queries and sequential access are frequent, as in database indexes and file systems; internal nodes hold more keys, so the tree is shorter.

#### Conclusion
B-trees stay perfectly balanced by splitting full nodes upward, giving O(log n) disk accesses; B+ trees add linked leaves for fast sequential access.

### N u5-hash | u5.hash | What is hashing? Explain hash functions and collision resolution techniques. Insert 76, 26, 37, 59, 21, 65, 88 into a table of size 11 with quadratic probing (c1 = 1, c2 = 3, h'(k) = k mod 11).
#### Hashing
**Hashing** maps a key directly to a table position (bucket) with a **hash function h(k)**, so search, insert and delete take **O(1) on average**, independent of n. It is used for symbol tables, database indexing, caches and dictionaries.

#### A good hash function
Easy to compute, spreads keys **uniformly** over the table, minimises **collisions**, and uses all of the key.

#### Hash functions
1. **Division**: h(k) = k mod m (m a prime). 76 mod 11 = 10.
2. **Mid-square**: square the key and take the middle digits. 3205² = 10272025 → "72".
3. **Folding**: split the key into parts and add them. 123456 → 12 + 34 + 56 = 102.
4. **Multiplication**: h(k) = ⌊m (kA mod 1)⌋ with 0 < A < 1.

#### Collision resolution
A **collision** occurs when two keys hash to the same slot.
- **Separate chaining**: each slot holds a linked list of all keys hashing there.
- **Open addressing**: find another empty slot in the table:
  - **Linear probing**: h(k, i) = (h'(k) + i) mod m (suffers primary clustering).
  - **Quadratic probing**: h(k, i) = (h'(k) + c₁i + c₂i²) mod m.
  - **Double hashing**: h(k, i) = (h₁(k) + i·h₂(k)) mod m.
- **Rehashing**: build a bigger table when the load factor grows.

#### Numerical: quadratic probing, h(k, i) = (k mod 11 + i + 3i²) mod 11
| Key | k mod 11 | Probes | Slot |
|---|---|---|---|
| 76 | 10 | i = 0 → 10 | **10** |
| 26 | 4 | i = 0 → 4 | **4** |
| 37 | 4 | i = 0 → 4 (full); i = 1 → 4 + 1 + 3 = 8 | **8** |
| 59 | 4 | 4 full; 8 full; i = 2 → 4 + 2 + 12 = 18 mod 11 = 7 | **7** |
| 21 | 10 | 10 full; i = 1 → 10 + 4 = 14 mod 11 = 3 | **3** |
| 65 | 10 | 10 full; 3 full; i = 2 → 10 + 14 = 24 mod 11 = 2 | **2** |
| 88 | 0 | i = 0 → 0 | **0** |

```fig 600x110 | Final hash table (size 11)
box h0 10 40 52 34 hl | 88
box h1 62 40 52 34 |
box h2 114 40 52 34 hl | 65
box h3 166 40 52 34 hl | 21
box h4 218 40 52 34 hl | 26
box h5 270 40 52 34 |
box h6 322 40 52 34 |
box h7 374 40 52 34 hl | 59
box h8 426 40 52 34 hl | 37
box h9 478 40 52 34 |
box h10 530 40 52 34 hl | 76
text 36 90 small | 0
text 140 90 small | 2
text 296 90 small | 5
text 556 90 small | 10
```

#### Comparison
| Chaining | Open addressing |
|---|---|
| Table never "fills"; lists grow | Load factor must stay < 1 |
| Extra memory for pointers | No pointers |
| Deletion is easy | Deletion needs "deleted" markers |

#### Conclusion
A good hash function plus a collision strategy (chaining or probing) gives average O(1) search, which is why hashing is used wherever fast lookup matters.

### L u5-storage | u5.storage | Explain various garbage collection and compaction techniques in storage management.
#### Storage management
Dynamic structures (linked lists, trees) take memory from the **heap** with malloc and release it with free. Over time the heap gets **garbage** (blocks no longer reachable) and **fragmentation** (free memory split into small holes). The system keeps free blocks in an **AVAIL (free) list**.

#### Garbage
A block becomes garbage when no pointer refers to it, e.g.
```
p = malloc(100); p = NULL;    /* the 100-byte block can no longer be used */
```
If not reclaimed, the program eventually runs out of memory (memory leak).

#### Garbage collection techniques
1. **Mark and sweep** (two phases):
   - *Mark*: starting from all **root pointers** (program variables, stack), traverse every reachable node and set its mark bit.
   - *Sweep (collection)*: scan the whole heap; every unmarked block is garbage and is returned to the free list; clear the marks.
   Runs when free memory gets low; the program pauses while it runs.
2. **Reference counting**: each block keeps a count of pointers to it; when the count drops to 0 it is freed immediately. Cannot reclaim **cyclic** structures.
3. **Copying collector**: the heap is split into two halves; live blocks are copied from the "from" half to the "to" half, which also compacts them.

```fig 600x200 | Mark and sweep, then compaction
box m1 20 30 70 34 hl | A ✓
box m2 90 30 70 34 dash | free
box m3 160 30 70 34 | G
box m4 230 30 70 34 hl | B ✓
box m5 300 30 70 34 | G
box m6 370 30 70 34 hl | C ✓
text 200 15 small muted | ✓ = marked reachable; G = garbage
arrow 220,75 220,105 | sweep + compact
box c1 20 115 70 34 hl | A
box c2 90 115 70 34 hl | B
box c3 160 115 70 34 hl | C
box c4 230 115 210 34 soft | one large free block
text 230 175 small muted | all live blocks moved to one end; pointers updated
```

#### Compaction
Even after garbage collection, free memory may be scattered in small holes (**external fragmentation**), so a large request can fail although total free memory is enough. **Compaction** moves all allocated blocks to one end of memory and merges the free space into **one contiguous block**.
Steps: (1) compute the new address of each live block, (2) update every pointer to point to the new addresses, (3) move the blocks.
It is costly (all pointers must be found and updated), so it is done only when needed.

#### Comparison
| | Garbage collection | Compaction |
|---|---|---|
| Problem solved | Unreachable blocks (leaks) | Fragmentation |
| Action | Returns garbage to the free list | Moves live blocks together |
| Result | More free blocks | One large free block |

#### Conclusion
Garbage collection recovers unused nodes and compaction removes fragmentation; together they let dynamic data structures run for a long time without exhausting memory.
