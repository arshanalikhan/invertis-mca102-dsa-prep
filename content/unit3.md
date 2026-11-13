---
unit: 3
title: Linked Lists
short: Linked Lists
syllabus: Linked lists: array implementation and dynamic implementation of singly linked lists, doubly linked list, circularly linked list, operations on a linked list: insertion, deletion, traversal, polynomial representation and addition, generalized linked list.
---

Linked lists are asked in nearly every paper, usually as **C functions** (insert after a node, delete the last node, reverse the list) or as **polynomial addition**. Always draw the node boxes with arrows before and after the operation.

### S u3s-array-ll | u3.sll | Differentiate between array and linked list.
| Array | Linked list |
|---|---|
| Contiguous memory | Nodes scattered, joined by pointers |
| Fixed size | Grows and shrinks at run time |
| Random access A[i] in O(1) | Sequential access, O(n) |
| Insert/delete needs shifting, O(n) | Insert/delete by changing pointers, O(1) once position is known |
| No extra memory | Extra memory for the pointer in each node |

### S u3s-apps | u3.sll | Write two applications of linked lists.
1. **Implementing stacks, queues and deques** of unknown size.
2. **Polynomial representation and arithmetic**: each node stores a coefficient and an exponent.
3. **Sparse matrices**, adjacency lists of graphs, hash-table chaining.
4. **Dynamic memory management**: the free-storage list of the operating system.

### S u3s-header | u3.dll | What is a header linked list?
A **header linked list** has a special **header node** at the beginning that holds no ordinary data; it may store information about the list (number of nodes, a pointer to the last node). START points to the header.

Types: **grounded header list** (last node's link = NULL) and **circular header list** (last node points back to the header). Advantage: insertion and deletion at the front need no special case, because the list is never physically empty.

### S u3s-ll-ops | u3.sll | Define non-linear data structure. List the basic operations carried out in a linked list.
A **non-linear data structure** arranges elements hierarchically or as a network, so an element can be linked to several others (tree, graph); it cannot be traversed in a single sequential pass.

Basic linked-list operations: **creation**, **traversal**, **insertion** (at beginning, end, after a given node), **deletion** (first, last, given node), **searching**, **reversing**, **sorting**, **concatenation**.

### L u3-sll-ops | u3.sll | Define linked list. Write C functions to create a singly linked list, insert a node after a given node, delete the last node, and reverse the list.
#### Singly linked list
A **linked list** is a linear collection of **nodes**, where each node has two parts: **INFO** (data) and **LINK** (address of the next node). START points to the first node; the last node's link is NULL. It is a **dynamic** data structure created at run time with malloc().

```
struct node { int info; struct node *next; };
struct node *start = NULL;
```

#### Create (insert at end)
```
void create(int n) {
    struct node *p, *last = NULL;
    for (int i = 0; i < n; i++) {
        p = malloc(sizeof(struct node));
        scanf("%d", &p->info); p->next = NULL;
        if (start == NULL) start = p; else last->next = p;
        last = p;
    }
}
```

#### Insert after a given node (value key)
```
void insertAfter(int key, int x) {
    struct node *ptr = start;
    while (ptr != NULL && ptr->info != key) ptr = ptr->next;
    if (ptr == NULL) { printf("Key not found\n"); return; }
    struct node *p = malloc(sizeof(struct node));
    p->info = x;
    p->next = ptr->next;     /* 1: new node points to successor */
    ptr->next = p;           /* 2: given node points to new node */
}
```

```fig 600x170 | Insert 25 after node 20: set NEW→next first, then 20→next
box s 10 30 70 30 bold | START
box a 40 80 100 36 | 10 | •
box b 200 80 100 36 hl | 20 | •
box c 440 80 110 36 | 30 | NULL
box n 320 10 100 36 hl | 25 | •
arrow s a
arrow a b
line b c dash
arrow b n hl | 2
arrow n c hl | 1
text 370 130 small muted | old link (removed)
```

#### Delete the last node
```
void deleteLast() {
    if (start == NULL) { printf("Underflow\n"); return; }
    if (start->next == NULL) { free(start); start = NULL; return; }
    struct node *ptr = start;
    while (ptr->next->next != NULL) ptr = ptr->next;   /* second-last node */
    free(ptr->next);
    ptr->next = NULL;
}
```

#### Reverse the list
```
void reverse() {
    struct node *prev = NULL, *cur = start, *nxt;
    while (cur != NULL) {
        nxt = cur->next; cur->next = prev;
        prev = cur; cur = nxt;
    }
    start = prev;
}
```
Example: 10 → 20 → 30 becomes 30 → 20 → 10.

#### Traversal and finding the maximum
```
int maxValue() {
    int max = start->info;
    for (struct node *p = start->next; p != NULL; p = p->next) if (p->info > max) max = p->info;
    return max;
}
```

#### Complexity
| Operation | Time |
|---|---|
| Insert at beginning | O(1) |
| Insert after a given node (once found) | O(1); search O(n) |
| Delete last | O(n) |
| Traverse, search, reverse | O(n) |

#### Array implementation
Without pointers, a list can be kept in two parallel arrays INFO[ ] and LINK[ ], where LINK[i] is the index of the next node (−1 for end) and a separate AVAIL list holds free cells.

#### Conclusion
A singly linked list allows fast insertion and deletion by changing two pointers, at the cost of sequential access.

### L u3-types | u3.dll | Explain the representation of singly, doubly, circular doubly and header linked lists with their self-referential structures and diagrams.
#### Self-referential structure
A structure that contains a pointer to a structure of the **same type** is self-referential; it is the building block of every linked list.

#### 1. Singly linked list
```
struct node { int info; struct node *next; };
```
Each node points only to the next one; traversal is one-way. Last node → NULL.

#### 2. Doubly linked list
```
struct dnode { struct dnode *prev; int info; struct dnode *next; };
```
Each node points to both its **predecessor and successor**, so the list can be traversed both ways and a node can be deleted when only its address is known.

**Insert X after node P:** X->prev = P; X->next = P->next; if (P->next) P->next->prev = X; P->next = X.
**Delete node P:** P->prev->next = P->next; if (P->next) P->next->prev = P->prev; free(P).

#### 3. Circular linked list
The last node points back to the **first node** instead of NULL. There is no NULL end, so any node can be the starting point; useful for round-robin scheduling. In a **circular doubly linked list**, the last node's next is the first node and the first node's prev is the last node.

#### 4. Header linked list
Has an extra **header node** at the start that stores no regular data (often the count of nodes). Grounded header list ends in NULL; circular header list ends at the header.

```fig 600x320 | The four kinds of linked lists
text 10 20 left bold | Singly
box a1 90 8 90 28 | 10 | •
box a2 220 8 90 28 | 20 | •
box a3 350 8 100 28 | 30 | NULL
arrow a1 a2
arrow a2 a3
text 10 95 left bold | Doubly
box b1 90 80 120 30 | NULL|10|•
box b2 250 80 110 30 | •|20|•
box b3 400 80 120 30 | •|30|NULL
arrow b1 b2 bend=-12
arrow b2 b1 bend=-12
arrow b2 b3 bend=-12
arrow b3 b2 bend=-12
text 10 170 left bold | Circular doubly
box c1 120 155 100 30 | •|10|•
box c2 260 155 100 30 | •|20|•
box c3 400 155 100 30 | •|30|•
arrow c1 c2 bend=-12
arrow c2 c1 bend=-12
arrow c2 c3 bend=-12
arrow c3 c2 bend=-12
arrow c3.b c1.b bend=-40
text 10 270 left bold | Header
box h 90 255 100 30 hl | H: 3 | •
box d1 230 255 90 30 | 10 | •
box d2 350 255 90 30 | 20 | •
box d3 470 255 100 30 | 30 | NULL
arrow h d1
arrow d1 d2
arrow d2 d3
```

#### Comparison
| Type | Links per node | Traversal | Special feature |
|---|---|---|---|
| Singly | 1 | Forward only | Least memory |
| Doubly | 2 | Both directions | Easy deletion of a given node |
| Circular | 1 or 2 | Loops back | No NULL; good for round robin |
| Header | 1 or 2 | From the header | No empty-list special case |

#### Conclusion
All four use self-referential nodes; the choice depends on whether backward traversal, circular access or simpler boundary handling is needed.

### N u3-poly | u3.poly | How can a polynomial like 5x³ + 4x² + 3x + 2 be represented using a linked list? Write an algorithm to add two polynomials.
#### Representation
Each term is a node with three fields: **COEF**, **EXP** and **LINK**. Terms are kept in **decreasing order of exponent**; zero terms are not stored.
```
struct poly { int coef; int exp; struct poly *next; };
```

5x³ + 4x² + 3x + 2:

```fig 600x180 | P = 5x³ + 4x² + 3x + 2 and Q = 6x³ − 2x + 7 as linked lists
box p 10 20 50 30 bold | P
box p1 90 20 100 30 | 5 | 3 | •
box p2 220 20 100 30 | 4 | 2 | •
box p3 350 20 100 30 | 3 | 1 | •
box p4 480 20 110 30 | 2 | 0 | NULL
arrow p p1
arrow p1 p2
arrow p2 p3
arrow p3 p4
box q 10 110 50 30 bold | Q
box q1 90 110 100 30 | 6 | 3 | •
box q2 220 110 100 30 | −2 | 1 | •
box q3 350 110 110 30 | 7 | 0 | NULL
arrow q q1
arrow q1 q2
arrow q2 q3
text 300 170 small muted | node = coefficient | exponent | link
```

#### Algorithm POLYADD(P, Q)
1. Set p = P, q = Q, R = NULL (result).
2. While p ≠ NULL and q ≠ NULL:
   - If p.exp = q.exp: sum = p.coef + q.coef; if sum ≠ 0, append (sum, p.exp) to R; advance p and q.
   - Else if p.exp > q.exp: append (p.coef, p.exp) to R; advance p.
   - Else: append (q.coef, q.exp) to R; advance q.
3. Append the remaining terms of p or q to R.
4. Return R.

#### C function
```
struct poly *add(struct poly *p, struct poly *q) {
    struct poly *r = NULL, *last = NULL, *t;
    while (p || q) {
        t = malloc(sizeof(struct poly)); t->next = NULL;
        if (q == NULL || (p && p->exp > q->exp)) { t->coef = p->coef; t->exp = p->exp; p = p->next; }
        else if (p == NULL || q->exp > p->exp) { t->coef = q->coef; t->exp = q->exp; q = q->next; }
        else { t->coef = p->coef + q->coef; t->exp = p->exp; p = p->next; q = q->next;
               if (t->coef == 0) { free(t); continue; } }
        if (r == NULL) r = t; else last->next = t;
        last = t;
    }
    return r;
}
```

#### Example
P = 5x³ + 4x² + 3x + 2, Q = 6x³ − 2x + 7

| Step | Compare | Result term |
|---|---|---|
| 1 | x³ = x³ | 11x³ |
| 2 | x² > x¹ | 4x² |
| 3 | x¹ = x¹ | 1x |
| 4 | x⁰ = x⁰ | 9 |

**R = 11x³ + 4x² + x + 9.** Time O(m + n) for m and n terms.

#### Generalized linked list
A **generalized list** is a list whose elements may be atoms **or other lists**, e.g. L = (a, (b, c), d). Each node has a **flag** (atom or sublist), a **data/down-pointer** and a **next** pointer. Multi-variable polynomials such as 3x²y + 2xy² are stored this way: each coefficient of x is itself a polynomial in y.

#### Conclusion
Linked lists store only the non-zero terms of a polynomial in exponent order, so two polynomials are added in one merge-like pass.
