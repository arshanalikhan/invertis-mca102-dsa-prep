---
unit: 2
title: Stacks, Recursion & Queues
short: Stacks & Queues
syllabus: Stacks: abstract data type, primitive stack operations push and pop, array and linked implementation of stack, application of stack: prefix and postfix expressions, evaluation of postfix expression, recursion, Tower of Hanoi. Queues: operations on queue: create, add, delete, full and empty, circular queues, array and linked implementation of queues in C, dequeue and priority queue.
---

Unit II is the **most-asked unit**: recursion and queues appeared in **every one of the 8 papers**, and stacks in 7. Practise infix → postfix/prefix conversion and postfix evaluation in table form, and the circular queue full/empty conditions.

### S u2s-pushpop | u2.stack | Define stack. Define PUSH and POP operations.
A **stack** is a linear data structure in which insertion and deletion take place at **one end, called TOP**. It follows **LIFO** (Last In, First Out).
- **PUSH(x)**: if TOP = MAX − 1 → overflow; else TOP = TOP + 1, STACK[TOP] = x.
- **POP()**: if TOP = −1 → underflow; else x = STACK[TOP], TOP = TOP − 1, return x.

Example: push 10, 20, 30 then pop → returns 30.

### S u2s-stack-ll | u2.stack | State the difference between stacks and linked lists.
| Stack | Linked list |
|---|---|
| Restricted: insert/delete only at TOP | Insert/delete at any position |
| LIFO order | No fixed order of access |
| An ADT; can be built with an array or a list | A concrete structure of nodes and pointers |
| Operations: push, pop, peek | Operations: insert, delete, traverse, search |

### S u2s-recursion | u2.recursion | Define recursion. What data structure is used to perform recursion?
**Recursion** is a technique in which a function **calls itself** to solve a smaller instance of the same problem. Every recursive function needs a **base case** (stops the calls) and a **recursive case** (moves towards the base case).

Example: fact(n) = 1 if n = 0, else n × fact(n − 1).

Recursion is implemented with a **stack** (the call stack): each call pushes an activation record (parameters, local variables, return address), popped when the call returns.

### S u2s-tail | u2.recursion | What is tail recursion?
A recursive function is **tail recursive** when the recursive call is the **last operation** of the function: nothing is left to do after the call returns. The compiler can then reuse the same stack frame (tail-call optimisation), so it uses O(1) stack space like a loop.

```
int fact(int n, int acc) { if (n == 0) return acc; return fact(n - 1, n * acc); }
```
fact(n) = n * fact(n − 1) is **not** tail recursive, because the multiplication happens after the call.

### S u2s-q47 | u2.recursion | Q(J,K) = 5 if J < K, and Q(J−K, K+3) + J if J ≥ K. Find Q(4,7).
Here J = 4 and K = 7, so **J < K** and the base case applies directly:

**Q(4, 7) = 5.**

(Had J ≥ K, e.g. Q(12, 2) = Q(10, 5) + 12 = (Q(5, 8) + 10) + 12 = 5 + 10 + 12 = 27.)

### S u2s-pq | u2.deque | Define priority queue.
A **priority queue** is a queue in which every element has a **priority**, and the element with the **highest priority is deleted first**; elements of equal priority are served in FIFO order. It can be implemented with an ordered array, a linked list, or most efficiently a **heap** (insert and delete in O(log n)). Uses: CPU scheduling, Dijkstra's and Prim's algorithms, Huffman coding.

### S u2s-cq-dq | u2.deque | Compare circular queue and deque.
| Circular queue | Deque (double-ended queue) |
|---|---|
| Insert at REAR, delete at FRONT only | Insert and delete at **both** ends |
| Last position connects to the first: rear = (rear + 1) % N | Can work as both stack and queue |
| Solves the wasted-space problem of linear queue | Variants: input-restricted, output-restricted |
| FIFO | Not strictly FIFO or LIFO |

### S u2s-linearq | u2.queue | A linear queue holds five elements; FRONT = 2, REAR = 4, queue: _, L, M, N, _. Show: add O, add P, delete two letters, add Q, R.
Positions 1–5 (FRONT = 2, REAR = 4):
1. **Add O**: REAR = 5 → _, L, M, N, O.
2. **Add P**: REAR = MAX → **overflow**, P not inserted (linear queue cannot reuse position 1).
3. **Delete two**: L and M removed, FRONT = 4 → _, _, _, N, O.
4. **Add Q, R**: REAR = 5 = MAX → **overflow** for both, although positions 1–3 are empty.

This waste is why a **circular queue** is used.

### L u2-stack-impl | u2.stack | What is a stack? Describe array and linked list implementation of a stack in C. Compare both in memory usage and flexibility.
#### Stack
A **stack** is a linear list where all insertions and deletions happen at one end called **TOP**: **Last In First Out (LIFO)**. Real-life example: a pile of plates. Operations: **push**, **pop**, **peek/top**, **isEmpty**, **isFull**.

#### 1. Array implementation
An array STACK[MAX] and an integer top = −1.
```
#define MAX 100
int stack[MAX], top = -1;
void push(int x) {
    if (top == MAX - 1) { printf("Overflow\n"); return; }
    stack[++top] = x;
}
int pop() {
    if (top == -1) { printf("Underflow\n"); return -1; }
    return stack[top--];
}
```

#### 2. Linked list implementation
Each node holds data and a pointer; **top** points to the first node. Push and pop work at the head.
```
struct node { int data; struct node *next; } *top = NULL;
void push(int x) {
    struct node *p = malloc(sizeof(struct node));
    p->data = x; p->next = top; top = p;
}
int pop() {
    if (top == NULL) { printf("Underflow\n"); return -1; }
    struct node *p = top; int x = p->data;
    top = top->next; free(p); return x;
}
```

```fig 600x200 | Stack after push 10, 20, 30: array form (left) and linked form (right)
box s0 60 150 90 30 | 10
box s1 60 120 90 30 | 20
box s2 60 90 90 30 hl | 30
box s3 60 60 90 30 dash |
box s4 60 30 90 30 dash |
text 30 165 small | [0]
text 30 105 small | [2]
text 200 105 small hl | ← top = 2
box t 300 30 60 30 bold | top
box n3 300 90 100 34 hl | 30 | •
box n2 300 150 100 34 | 20 | •
box n1 450 150 100 34 | 10 | NULL
arrow t n3
arrow n3 n2
arrow n2 n1
```

Both versions do push and pop in **O(1)** time.

#### Comparison
| Basis | Array stack | Linked stack |
|---|---|---|
| Size | Fixed at compile time (MAX) | Grows and shrinks at run time |
| Overflow | When top = MAX − 1 | Only when memory (heap) is full |
| Memory per element | Only the data | Data + one pointer |
| Wasted memory | Unused array cells | None, but pointer overhead |
| Speed | Faster, cache-friendly, no malloc | Slightly slower (malloc/free) |
| Flexibility | Low | High |

#### Applications of stack
Expression conversion (infix → postfix/prefix) and postfix evaluation, function calls and recursion, undo in editors, browser back button, balancing parentheses, reversing a string, DFS of a graph, Tower of Hanoi.

#### Conclusion
Use an array stack when the maximum size is known and speed matters; use a linked stack when the size is unpredictable.

### N u2-infix | u2.expr | Write an algorithm to convert an infix expression to postfix. Convert (A−B)/((D+E)*F) to postfix and A*(B+D)/E−F*(G+H/K) to prefix.
#### Notations
- **Infix**: operator between operands: A + B.
- **Prefix (Polish)**: operator before operands: + A B.
- **Postfix (reverse Polish)**: operator after operands: A B +. Postfix and prefix need **no brackets** and no precedence rules, so computers evaluate them easily with a stack.

Precedence: ^ (highest, right to left) > * / > + − (left to right).

#### Algorithm INFIX-TO-POSTFIX
1. Push "(" on the stack and add ")" at the end of the infix expression.
2. Scan the expression left to right. For each symbol:
   - **Operand** → add to postfix.
   - **"("** → push.
   - **Operator ⊗** → pop and output every operator on top with precedence **higher than or equal to** ⊗ (for ^ only higher), then push ⊗.
   - **")"** → pop and output until "(" is found; discard "(".
3. Stop when the stack is empty.

#### Example 1: (A−B)/((D+E)*F)
| Symbol | Stack | Postfix |
|---|---|---|
| ( | ( | |
| A | ( | A |
| − | (− | A |
| B | (− | AB |
| ) | | AB− |
| / | / | AB− |
| ( | /( | AB− |
| ( | /(( | AB− |
| D | /(( | AB−D |
| + | /((+ | AB−D |
| E | /((+ | AB−DE |
| ) | /( | AB−DE+ |
| * | /(* | AB−DE+ |
| F | /(* | AB−DE+F |
| ) | / | AB−DE+F* |
| end | | **AB−DE+F*/** |

```fig 600x120 | Stack contents while scanning (A−B)/((D+E)*F) at the symbol E
box b1 200 70 60 34 | /
box b2 200 40 60 30 | (
box b3 200 10 60 30 hl | (+
text 330 55 left | Postfix so far: AB−DE
text 120 87 small | bottom
text 120 25 small hl | top
```

#### Example 2: infix to prefix, A*(B+D)/E−F*(G+H/K)
Method: reverse the expression (swapping "(" and ")"), convert to postfix (pop only operators of **strictly higher** precedence), then reverse the result.
Steps by hand with brackets of precedence:
1. H/K → /HK; G + H/K → +G/HK; F*(…) → *F+G/HK
2. B+D → +BD; A*(B+D) → *A+BD; …/E → /*A+BDE
3. Whole: **− / * A + B D E * F + G / H K**

**Prefix: −/*A+BDE*F+G/HK**

#### Conclusion
A stack holds operators until their operands have been output, which turns infix expressions into bracket-free postfix or prefix form in O(n) time.

### N u2-postfix-eval | u2.expr | Write an algorithm to evaluate a postfix expression using a stack and evaluate 6 2 3 + − 3 8 2 / + * 2 ^ 3 +.
#### Algorithm EVAL-POSTFIX(P)
1. Add a sentinel ")" at the end of P; create an empty stack.
2. Scan P from left to right until ")":
   - If the symbol is an **operand**, push it.
   - If it is an **operator ⊗**: pop A (top) and B (next), compute **B ⊗ A**, and push the result.
3. The value of the expression is the single element left on the stack.

```fig 600x170 | Evaluating at operator '+' after 8 2 / : pop 4 and 3, push 7
box s1 60 120 80 30 | 1
box s2 60 90 80 30 | 3
box s3 60 60 80 30 hl | 4
text 100 30 small muted | before '+'
arrow 150,90 260,90 | pop 4, pop 3
box t1 290 120 80 30 | 1
box t2 290 90 80 30 hl | 7
text 330 60 small muted | after '+'
text 470 100 | 3 + 4 = 7
```

#### Trace
| Symbol | Action | Stack (bottom → top) |
|---|---|---|
| 6 | push | 6 |
| 2 | push | 6, 2 |
| 3 | push | 6, 2, 3 |
| + | 2 + 3 = 5 | 6, 5 |
| − | 6 − 5 = 1 | 1 |
| 3 | push | 1, 3 |
| 8 | push | 1, 3, 8 |
| 2 | push | 1, 3, 8, 2 |
| / | 8 / 2 = 4 | 1, 3, 4 |
| + | 3 + 4 = 7 | 1, 7 |
| * | 1 × 7 = 7 | 7 |
| 2 | push | 7, 2 |
| ^ | 7² = 49 | 49 |
| 3 | push | 49, 3 |
| + | 49 + 3 = 52 | **52** |

**Value = 52.**

> AKTU 2018-19 printed this expression without the "^" (6 2 3 + − 3 8 2 / + * 2 3 +). That version leaves **two values (7 and 5)** on the stack, so it is not a valid postfix expression; mention this and solve the standard version above. Similarly 10 7 + 30 6 / 8 − (2022-23) leaves 17 and −3: one operator is missing.

#### Complexity
Each symbol is pushed or popped once: **O(n)** time and O(n) stack space.

#### Conclusion
Postfix expressions are evaluated in a single left-to-right scan with a stack, which is how compilers and calculators evaluate expressions.

### N u2-hanoi | u2.recursion | Explain recursion. What is the Tower of Hanoi problem? Write its recursive function and solve it for 3 disks.
#### Recursion
A function that calls itself is **recursive**. It has a **base case** that stops the recursion and a **recursive step** that reduces the problem. Each call is stored on the **system stack** as an activation record.

**Good**: natural for problems defined recursively (factorial, trees, Tower of Hanoi, quick sort), short code. **Bad**: extra stack space and call overhead; a missing base case causes stack overflow; naïve recursion may repeat work (Fibonacci is O(2ⁿ)).

#### Tower of Hanoi
Three pegs A (source), B (auxiliary), C (destination) and n disks of different sizes on A, largest at the bottom. Move all disks to C so that: (1) only one disk moves at a time, (2) only the top disk of a peg can be moved, (3) a larger disk is never placed on a smaller one.

#### Recursive solution
1. Move n − 1 disks from A to B using C.
2. Move disk n from A to C.
3. Move n − 1 disks from B to C using A.

```
void toh(int n, char src, char aux, char dst) {
    if (n == 0) return;
    toh(n - 1, src, dst, aux);
    printf("Move disk %d from %c to %c\n", n, src, dst);
    toh(n - 1, aux, src, dst);
}
```

```fig 600x170 | Tower of Hanoi with 3 disks: initial state
line 30,150 570,150
line 110,50 110,150
line 300,50 300,150
line 490,50 490,150
box d3 50 128 120 20 hl | 3
box d2 70 106 80 20 hl | 2
box d1 85 84 50 20 hl | 1
text 110 165 bold | A (source)
text 300 165 bold | B (aux)
text 490 165 bold | C (destination)
```

#### Solution for n = 3: 2³ − 1 = 7 moves
| Move | Disk | From → To |
|---|---|---|
| 1 | 1 | A → C |
| 2 | 2 | A → B |
| 3 | 1 | C → B |
| 4 | 3 | A → C |
| 5 | 1 | B → A |
| 6 | 2 | B → C |
| 7 | 1 | A → C |

#### Complexity
T(n) = 2T(n − 1) + 1, T(1) = 1, so **T(n) = 2ⁿ − 1 = O(2ⁿ)** moves; stack depth O(n).

#### Factorial example
fact(n) = 1 if n ≤ 1 else n × fact(n − 1). T(n) = T(n − 1) + c = **O(n)**.

#### Conclusion
Tower of Hanoi shows how recursion splits a problem into smaller copies of itself; the minimum number of moves is 2ⁿ − 1.

### L u2-circular | u2.queue | What is a circular queue? Implement it using an array with insertion, deletion and display. What is the condition for a full circular queue?
#### Queue and its problem
A **queue** is a linear list where insertion happens at the **REAR** and deletion at the **FRONT**: **FIFO**. In a linear array queue, once REAR reaches MAX − 1 no insertion is possible even if the front cells are empty after deletions.

#### Circular queue
In a **circular queue** the last position is connected back to the first, so positions are reused. Indices move with **(index + 1) % MAX**.

```fig 600x230 | Circular queue of size 8: FRONT = 2, REAR = 5
circle q0 300 40 26 | 0
circle q1 390 78 26 | 1
circle q2 430 120 26 hl | 2: A
circle q3 390 162 26 hl | 3: B
circle q4 300 200 26 hl | 4: C
circle q5 210 162 26 hl | 5: D
circle q6 170 120 26 | 6
circle q7 210 78 26 | 7
arrow q0 q1
arrow q1 q2
arrow q2 q3
arrow q3 q4
arrow q4 q5
arrow q5 q6
arrow q6 q7
arrow q7 q0
text 510 120 small hl | ← FRONT
text 100 175 small hl | REAR →
```

#### Conditions
- **Empty:** FRONT = −1.
- **Full:** **(REAR + 1) % MAX == FRONT** (equivalently FRONT = 0 and REAR = MAX − 1, or FRONT = REAR + 1).

#### Implementation
```
#define MAX 8
int q[MAX], front = -1, rear = -1;
void insert(int x) {
    if ((rear + 1) % MAX == front) { printf("Overflow\n"); return; }
    if (front == -1) front = 0;
    rear = (rear + 1) % MAX;
    q[rear] = x;
}
int delete() {
    if (front == -1) { printf("Underflow\n"); return -1; }
    int x = q[front];
    if (front == rear) front = rear = -1;     /* queue becomes empty */
    else front = (front + 1) % MAX;
    return x;
}
void display() {
    if (front == -1) { printf("Empty\n"); return; }
    for (int i = front; ; i = (i + 1) % MAX) {
        printf("%d ", q[i]);
        if (i == rear) break;
    }
}
```

#### Example (MAX = 5)
Insert 10, 20, 30, 40, 50 → full (front 0, rear 4). Delete twice → front 2. Insert 60 → rear = (4 + 1) % 5 = 0: the free cell 0 is reused. A linear queue would report overflow here.

#### Linear vs circular
| Linear queue | Circular queue |
|---|---|
| rear = rear + 1 | rear = (rear + 1) % MAX |
| Full when rear = MAX − 1 | Full when (rear + 1) % MAX = front |
| Wastes space after deletions | Reuses freed space |

#### Conclusion
A circular queue keeps O(1) insertion and deletion and uses every cell of the array; it is used in CPU scheduling, buffers and traffic systems.

### L u2-queue-impl | u2.queue | Define queue. Write algorithms for insertion and deletion and give the array and linked implementation of a queue. Can a queue be implemented with two stacks?
#### Queue
A **queue** is a linear data structure that follows **FIFO**: insertion (enqueue) at the **REAR**, deletion (dequeue) at the **FRONT**. Example: a ticket line. Operations: create, add (enqueue), delete (dequeue), isFull, isEmpty.

#### Array implementation
```
INSERT(Q, x)
1. if REAR = MAX − 1 then print "Overflow" and exit
2. if FRONT = −1 then FRONT = 0
3. REAR = REAR + 1
4. Q[REAR] = x

DELETE(Q)
1. if FRONT = −1 or FRONT > REAR then print "Underflow" and exit
2. x = Q[FRONT]
3. FRONT = FRONT + 1
4. return x
```

#### Linked implementation in C
```
struct node { int data; struct node *next; } *front = NULL, *rear = NULL;
void enqueue(int x) {
    struct node *p = malloc(sizeof(struct node));
    p->data = x; p->next = NULL;
    if (rear == NULL) front = rear = p;
    else { rear->next = p; rear = p; }
}
int dequeue() {
    if (front == NULL) { printf("Underflow\n"); return -1; }
    struct node *p = front; int x = p->data;
    front = front->next;
    if (front == NULL) rear = NULL;
    free(p); return x;
}
```

```fig 600x130 | Linked queue holding 10, 20, 30
box f 20 20 70 30 bold | FRONT
box r 480 20 70 30 bold | REAR
box n1 60 75 110 36 hl | 10 | •
box n2 240 75 110 36 | 20 | •
box n3 420 75 110 36 hl | 30 | NULL
arrow f n1
arrow r n3
arrow n1 n2
arrow n2 n3
text 300 125 small muted | delete at FRONT · insert at REAR
```

#### Queue using two stacks
Yes. Use stacks S1 (input) and S2 (output).
- **Enqueue(x)**: push x on S1.
- **Dequeue()**: if S2 is empty, pop every element of S1 and push it on S2 (this reverses the order); then pop S2.

Example: enqueue 1, 2, 3 → S1 = [1, 2, 3]. Dequeue: move to S2 = [3, 2, 1], pop → **1** (FIFO preserved). Each element is moved at most once, so the **amortised cost is O(1)**.

#### Applications
CPU and disk scheduling, printer spooling, BFS of graphs, buffering in I/O and networks.

#### Conclusion
A queue can be built with an array (fixed size), a linked list (dynamic size) or even two stacks; all give FIFO behaviour.

### L u2-deque-pq | u2.deque | Explain double-ended queue (deque) and priority queue with examples. Write algorithms for insertion and deletion in a priority queue.
#### Deque
A **deque** (double-ended queue) allows **insertion and deletion at both ends**, FRONT and REAR. It generalises both stack and queue.

Types:
1. **Input-restricted deque**: insertion at one end only, deletion at both ends.
2. **Output-restricted deque**: deletion at one end only, insertion at both ends.

Operations: insertFront, insertRear, deleteFront, deleteRear. In a circular array: insertFront sets front = (front − 1 + MAX) % MAX; insertRear sets rear = (rear + 1) % MAX.

```fig 600x120 | Deque: insert and delete at both ends
box d1 150 45 75 36 | 10
box d2 225 45 75 36 | 20
box d3 300 45 75 36 | 30
box d4 375 45 75 36 | 40
arrow 60,55 145,55 | insert
arrow 145,75 60,75 | delete
arrow 540,55 455,55 | insert
arrow 455,75 540,75 | delete
text 190 105 small hl | FRONT
text 410 105 small hl | REAR
```

#### Priority queue
A **priority queue** is a collection in which each element has a priority. **The element with the highest priority is deleted first**; equal priorities are served in arrival order. Example: emergency patients in a hospital, OS process scheduling.

Implementations:
| Method | Insert | Delete-max |
|---|---|---|
| Unsorted array/list | O(1) | O(n) |
| Sorted linked list | O(n) | O(1) |
| Binary heap | O(log n) | O(log n) |

#### Algorithms (sorted linked list, smaller number = higher priority)
```
INSERT(x, p)
1. Create node N with info = x, prn = p
2. if START = NULL or p < START.prn: N.next = START, START = N; exit
3. PTR = START
4. while PTR.next ≠ NULL and PTR.next.prn ≤ p: PTR = PTR.next
5. N.next = PTR.next; PTR.next = N

DELETE()
1. if START = NULL: print "Underflow"; exit
2. ITEM = START.info; START = START.next
3. return ITEM
```

Example: insert (A,3), (B,1), (C,2) → list B(1) → C(2) → A(3); delete returns **B**.

#### Comparison
| Queue | Deque | Priority queue |
|---|---|---|
| FIFO, two ends fixed | Both ends for both operations | Order by priority |
| Ticket line | Undo/redo, palindrome check | Scheduling, Dijkstra, Huffman |

#### Conclusion
A deque gives flexibility at both ends; a priority queue serves by importance and is best built on a heap.
