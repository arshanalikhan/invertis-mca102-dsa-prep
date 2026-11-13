---
unit: 4
title: Trees
short: Trees
syllabus: Trees: basic terminology, binary trees, binary tree representation: array representation and dynamic representation, complete binary tree, algebraic expressions, extended binary trees, array and linked representation of binary trees, tree traversal algorithms: inorder, preorder and postorder, threaded binary trees, traversing threaded binary trees, Huffman algorithm.
---

The surest question here is **constructing a binary tree from inorder + preorder (or postorder)** and writing the three traversals. Short questions on **complete/extended binary trees** and **threaded binary trees** come almost every year. Huffman coding is less frequent but is a full 7-mark numerical when it comes.

### S u4s-complete | u4.bintree | Define complete binary tree and extended binary tree. Give example.
- **Complete binary tree**: every level except possibly the last is completely filled, and the last level's nodes are as **far left as possible**. A complete tree with n nodes has height ⌊log₂ n⌋; it is stored in an array without gaps (children of i at 2i and 2i + 1).
- **Extended binary tree (2-tree)**: every node has **0 or 2 children**. Obtained by replacing each empty subtree with a special **external node** (square); original nodes become internal nodes. If there are n internal nodes, there are n + 1 external nodes.

### S u4s-bt-cbt | u4.bintree | Differentiate between binary tree and complete binary tree.
| Binary tree | Complete binary tree |
|---|---|
| Each node has at most 2 children | Binary tree with all levels full except the last |
| Nodes may be anywhere | Last level filled from left to right |
| Height can be up to n − 1 | Height is ⌊log₂ n⌋ |
| Array representation may waste space | Array representation has no gaps |

### S u4s-threaded | u4.threaded | Define threaded binary tree.
In a binary tree with n nodes, n + 1 of the 2n link fields are NULL. A **threaded binary tree** replaces these NULL links by **threads**: the NULL right link points to the node's **inorder successor**, and the NULL left link to its **inorder predecessor**. A flag bit in each node tells whether a link is a child pointer or a thread. Inorder traversal then needs **no stack and no recursion**.

### S u4s-repr | u4.bintree | Give static and dynamic memory representation of a binary tree.
- **Static (array/sequential)**: root at TREE[1]; for a node at index i, the left child is at **2i**, the right child at **2i + 1** and the parent at **⌊i/2⌋**. Good for complete trees; wastes space for skewed trees.
- **Dynamic (linked)**: each node has three fields: `struct node { struct node *left; int info; struct node *right; };` ROOT points to the root; empty subtrees are NULL. Memory is used only for existing nodes.

### S u4s-expr | u4.traversal | Draw the binary tree for the expression a + b / c * d + e + f.
Precedence: / and * first (left to right), then + left to right: ((a + ((b / c) * d)) + e) + f.

```tree 340x230 | Expression tree for a + b/c*d + e + f
+
  +
    +
      a
      *
        /
          b
          c
        d
    e
  f
```
Inorder gives back the infix; postorder gives **a b c / d * + e + f +**.

### N u4-construct | u4.traversal | Draw the binary tree with Inorder: D B H E A I F J C G and Preorder: A B D E H C F I J G. Write the recursive traversal algorithms.
#### Method
1. The **first element of preorder** is the root.
2. Find it in inorder: elements to its **left form the left subtree**, elements to the **right form the right subtree**.
3. Repeat recursively with the next preorder elements.

#### Construction
| Step | Root (from preorder) | Left (inorder) | Right (inorder) |
|---|---|---|---|
| 1 | A | D B H E | I F J C G |
| 2 | B | D | H E |
| 3 | D | – | – |
| 4 | E | H | – |
| 5 | C | I F J | G |
| 6 | F | I | J |
| 7 | G | – | – |

```tree 560x250 | Binary tree built from the inorder and preorder sequences
A
  B
    D
    E
      H
  C
    F
      I
      J
    G
```
(H is the **left** child of E, since H comes before E in inorder.)

**Check:** postorder = D H E B I J F G C A.

#### Recursive traversal algorithms
```
void inorder(struct node *t)  { if (t) { inorder(t->left); printf("%c ", t->info); inorder(t->right); } }
void preorder(struct node *t) { if (t) { printf("%c ", t->info); preorder(t->left); preorder(t->right); } }
void postorder(struct node *t){ if (t) { postorder(t->left); postorder(t->right); printf("%c ", t->info); } }
```

| Traversal | Order | Result for this tree |
|---|---|---|
| Inorder | Left, Root, Right | D B H E A I F J C G |
| Preorder | Root, Left, Right | A B D E H C F I J G |
| Postorder | Left, Right, Root | D H E B I J F G C A |

#### Non-recursive inorder (using a stack)
1. Set PTR = ROOT, stack empty.
2. While PTR ≠ NULL: push PTR, PTR = PTR→left.
3. If the stack is empty, stop. Pop PTR, visit it, set PTR = PTR→right, go to step 2.

#### Notes
- Preorder + inorder, or postorder + inorder, always identify a unique binary tree. Preorder + postorder do not (unless every node has 0 or 2 children).
- Each traversal visits each node once: O(n) time, O(h) stack space.

#### Conclusion
The root comes from preorder (or the last of postorder), and inorder splits the remaining nodes into left and right subtrees.

### L u4-bintree | u4.bintree | Explain basic tree terminology, binary trees and their array and linked representations, with complete and extended binary trees.
#### Terminology
- **Tree**: a finite set of nodes with one special node, the **root**; the remaining nodes form disjoint subtrees.
- **Parent, child, sibling**: B and C are children of A and siblings of each other.
- **Leaf (terminal node)**: a node with no children. **Internal node**: has at least one child.
- **Degree**: number of children of a node. **Level**: root is level 0 (or 1); children are one level lower.
- **Height/depth**: number of levels (longest root-to-leaf path).
- **Path, ancestor, descendant, edge, forest** (a set of disjoint trees).

#### Binary tree
A **binary tree** is a tree in which each node has **at most two children**, called the left and right child. Properties: maximum nodes at level i = 2ⁱ; a tree of height h has at most 2ʰ⁺¹ − 1 nodes; with n nodes there are n + 1 NULL links.

Types: **strictly binary** (0 or 2 children), **complete** (all levels full except the last, filled left to right), **full/perfect** (all levels full), **skewed** (every node has one child), **extended** (NULL links replaced by external nodes).

#### Array (sequential) representation
Store the root in TREE[1]; for node at index K: left child at **2K**, right child at **2K + 1**, parent at **⌊K/2⌋**.

```fig 600x220 | A binary tree and its array representation (index starts at 1)
circle a 150 30 18 hl | A
circle b 90 90 18 | B
circle c 210 90 18 | C
circle d 60 150 18 | D
circle e 120 150 18 | E
circle f 240 150 18 | F
line a b
line a c
line b d
line b e
line c f
box t1 300 80 40 30 | A
box t2 340 80 40 30 | B
box t3 380 80 40 30 | C
box t4 420 80 40 30 | D
box t5 460 80 40 30 | E
box t6 500 80 40 30 dash | –
box t7 540 80 40 30 | F
text 320 125 small | 1
text 360 125 small | 2
text 400 125 small | 3
text 440 125 small | 4
text 480 125 small | 5
text 520 125 small | 6
text 560 125 small | 7
text 440 165 small muted | F is the right child of C (3): index 2·3 + 1 = 7
```

#### Linked representation
```
struct node { struct node *left; char info; struct node *right; };
```
Each node holds LEFT, INFO and RIGHT; ROOT points to the root; an empty subtree is NULL.

| Array representation | Linked representation |
|---|---|
| No pointers; parent and children found by index | Needs two pointers per node |
| Wastes space for skewed trees (up to 2ⁿ − 1 cells) | Uses memory only for existing nodes |
| Fixed size | Grows dynamically |
| Best for complete trees and heaps | Best for general trees |

#### Algebraic expressions
An expression is stored as a binary tree: operators are internal nodes and operands are leaves. Inorder gives infix, preorder gives prefix and postorder gives postfix.

#### Conclusion
Binary trees are stored as arrays when they are complete (heaps) and as linked nodes otherwise.

### L u4-threaded | u4.threaded | What is a threaded binary tree? Explain its traversal, operations, advantages and disadvantages.
#### Idea
A binary tree with n nodes has 2n link fields but only n − 1 are used; **n + 1 links are NULL**. A **threaded binary tree** (Perlis and Thornton) stores useful pointers, called **threads**, in these NULL fields:
- A NULL **right** link points to the node's **inorder successor**.
- A NULL **left** link points to its **inorder predecessor**.

Two flag bits tell whether a link is a real child or a thread:
```
struct tnode { int lthread; struct tnode *left; char info; struct tnode *right; int rthread; };
```
A **header (dummy) node** is usually used: the leftmost node's left thread and the rightmost node's right thread point to the header.

#### Types
1. **One-way (right) threaded**: only right NULL links become successor threads.
2. **Two-way threaded**: both left and right NULL links are threads.

```fig 600x240 | Two-way threaded tree for inorder D B E A C (dashed = threads)
circle a 300 40 20 hl | A
circle b 180 110 20 | B
circle c 420 110 20 | C
circle d 110 190 20 | D
circle e 250 190 20 | E
box h 500 20 80 30 bold | Header
line a b
line a c
line b d
line b e
arrow e.r a dash bend=-30
arrow d.r b dash bend=-20
arrow e.l b dash bend=20
arrow c.r h dash bend=-20
arrow c.l a dash bend=20
arrow d.l 30,30 dash
text 70 30 small muted | → header
```

#### Inorder traversal without stack
```
INORDER(header)
1. p = leftmost node (keep following left links from the root)
2. while p ≠ header:
3.   visit p
4.   if p.rthread = 1: p = p.right          (thread: successor directly)
5.   else: p = p.right; while p.lthread = 0: p = p.left   (leftmost of right subtree)
```
For the tree above: D → (thread) B → E (leftmost of B's right subtree) → (thread) A → C → header. Output **D B E A C**.

#### Operations
- **Insertion** of node T as the right child of P: T.right = P.right, T.rthread = P.rthread, T.left = P, T.lthread = 1 (thread to P), then P.right = T, P.rthread = 0. If T has a successor S, S.left (a thread) now points to T.
- **Deletion** must re-adjust the threads of the predecessor and successor.

#### Advantages
1. Inorder traversal is **faster and needs no stack or recursion**.
2. The inorder **successor and predecessor** of any node are found directly.
3. Uses the NULL link fields that would otherwise be wasted.

#### Disadvantages
1. Each node needs **two extra flag bits**.
2. **Insertion and deletion are more complex**, because threads must be updated.
3. Preorder/postorder are not made simpler in the same way.

#### Conclusion
Threading turns the wasted NULL links into successor/predecessor pointers, allowing O(n) inorder traversal with O(1) extra space.

### N u4-huffman | u4.huffman | Write a short note on the Huffman algorithm with an example.
#### Idea
**Huffman coding** builds an optimal **prefix code** for compressing data: frequent characters get **short codes**, rare ones get **long codes**. No code is a prefix of another, so the encoded bit string is decoded without separators. The tree built is an **extended binary tree with minimum weighted path length**.

#### Algorithm HUFFMAN(C)
1. Create a leaf node for every character with its frequency as weight; insert all into a **min-priority queue**.
2. Repeat n − 1 times:
   - Remove the two nodes with the **smallest weights**, x and y.
   - Create a new internal node z with weight w(x) + w(y), left child x and right child y.
   - Insert z into the queue.
3. The remaining node is the root. Label left edges 0 and right edges 1; the code of a character is the path from the root to its leaf.

#### Example
Frequencies: A = 5, B = 9, C = 12, D = 13, E = 16, F = 45 (total 100).

| Step | Merge | New node |
|---|---|---|
| 1 | A(5) + B(9) | 14 |
| 2 | C(12) + D(13) | 25 |
| 3 | 14 + E(16) | 30 |
| 4 | 25 + 30 | 55 |
| 5 | F(45) + 55 | 100 |

```tree 560x270 | Huffman tree (left edge 0, right edge 1)
100
  F:45 ~0
  55 ~1
    25 ~0
      C:12 ~0
      D:13 ~1
    30 ~1
      14 ~0
        A:5 ~0
        B:9 ~1
      E:16 ~1
```

| Character | Frequency | Code | Bits |
|---|---|---|---|
| F | 45 | 0 | 45 |
| C | 12 | 100 | 36 |
| D | 13 | 101 | 39 |
| A | 5 | 1100 | 20 |
| B | 9 | 1101 | 36 |
| E | 16 | 111 | 48 |
| **Total** | 100 | | **224 bits** |

A fixed 3-bit code would need 3 × 100 = 300 bits, so Huffman saves about 25%.

#### Complexity
With a heap, each of the n − 1 merges costs O(log n): **O(n log n)**.

#### Conclusion
Huffman's greedy algorithm always merges the two lightest trees, giving the minimum total code length. It is used in ZIP, JPEG and MP3 compression.
