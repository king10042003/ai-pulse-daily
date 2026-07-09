# DSA Exam — Last Night Crash Revision
*Amity DSA Syllabus | Section 1: Long Answers (4→2) | Section 2: Case Studies (2) | Section 3: MCQ (20)*

---

## HOW TO USE THIS TONIGHT
1. Read **Section A (Core Concepts)** below fully — this is what Section 1 (long answer) and Section 2 (case study) questions are drawn from.
2. Skim **Section B (MCQ Rapid-Fire Facts)** right before sleeping and again in the morning — this is pure recall, high ROI for Section 3.
3. If you only have 2 hours: read **Priority Topics** marked 🔥 first.

---

# SECTION A: CORE CONCEPTS (for Long Answer + Case Study)

## MODULE 1: Data Structures & Algorithm Basics

### 🔥 Stack
- LIFO (Last In First Out). Operations: `push`, `pop`, `peek/top`, `isEmpty`, `isFull`.
- Array implementation: use a `top` pointer, increment on push, decrement on pop.
- **Applications**: expression evaluation (infix→postfix), function call management (recursion), undo operations, balanced parentheses checking, backtracking (maze, DFS).

### 🔥 Postfix Expression Evaluation (very common exam Q)
**Infix → Postfix (Shunting Yard idea):**
- Scan left to right. Operands → output directly. Operators → push to stack after popping higher/equal precedence operators to output. `(` push to stack, `)` pop until `(`.

**Evaluating Postfix:**
- Scan left to right. Operand → push to stack. Operator → pop two operands (say `b` then `a`, since stack is LIFO), compute `a operator b`, push result back.
- Example: `5 3 4 * +` → push 5,3,4 → see `*` → pop 4,3 → 3*4=12 → push 12 → stack: 5,12 → see `+` → pop 12,5 → 5+12=17 → **Answer: 17**

### Tower of Hanoi
- Move `n` disks from source to destination using auxiliary peg, never place larger disk on smaller.
- Recurrence: `T(n) = 2T(n-1) + 1`, minimum moves = `2^n - 1`.
- Recursive solution: move top n-1 to aux, move nth disk to dest, move n-1 from aux to dest.

### Queue
- FIFO (First In First Out). Operations: `enqueue` (rear), `dequeue` (front).
- **Circular Queue**: solves wasted space problem of linear queue array implementation using modulo arithmetic `(rear+1) % size`.
- Types: Simple Queue, Circular Queue, Priority Queue, Deque (double-ended).

### 🔥 Linked List
- Nodes with `data` + `pointer to next`. No contiguous memory needed (unlike arrays).
- **Singly linked list**: one direction traversal.
- **Doubly linked list**: each node has `prev` and `next` pointers — allows backward traversal, easier deletion.
- **Circular linked list**: last node points back to first.
- Advantages over array: dynamic size, easy insertion/deletion (no shifting).
- Disadvantage: no random access, extra memory for pointers.

### 🔥 Algorithm Characteristics
Must be: **Input, Output, Definiteness, Finiteness, Effectiveness** (5 key properties — commonly asked as MCQ/short answer).

### 🔥 Asymptotic Notations (VERY high yield)
- **Big-O (O)**: upper bound — worst case. "Algorithm won't be slower than this."
- **Omega (Ω)**: lower bound — best case.
- **Theta (Θ)**: tight bound — average/exact case (both upper and lower).
- Common complexities (best to worst): `O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(2ⁿ) < O(n!)`

### Master Theorem (for Divide & Conquer recurrences)
For `T(n) = aT(n/b) + f(n)`, compare `f(n)` with `n^(log_b a)`:
- If `f(n) = O(n^(log_b a - ε))` → `T(n) = Θ(n^(log_b a))`
- If `f(n) = Θ(n^(log_b a))` → `T(n) = Θ(n^(log_b a) · log n)`
- If `f(n) = Ω(n^(log_b a + ε))` (regularity holds) → `T(n) = Θ(f(n))`

### Divide and Conquer
- Break problem into subproblems (divide), solve recursively (conquer), merge results (combine).
- Examples: Merge Sort, Quick Sort, Binary Search, Strassen's Matrix Multiplication.

### 🔥 Sorting Techniques (ALWAYS asked — know all complexities cold)

| Algorithm | Best | Average | Worst | Space | Stable? |
|---|---|---|---|---|---|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) | No |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) | No |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) | No |

- **Bubble Sort**: repeatedly swap adjacent elements if out of order.
- **Insertion Sort**: build sorted array one element at a time, inserting into correct position.
- **Selection Sort**: repeatedly find minimum from unsorted part, swap to front.
- **Merge Sort**: divide array in half recursively, merge sorted halves. Uses extra space.
- **Quick Sort**: pick pivot, partition array so smaller elements left, larger right, recurse. In-place but worst case O(n²) when pivot is always smallest/largest (already sorted array with bad pivot choice).
- **Heap Sort**: build max-heap, repeatedly extract max and put at end.

---

## MODULE 2: Trees & Graphs

### 🔥 Tree Terminology
- **Root, Node, Edge, Leaf** (no children), **Height** (longest path root→leaf), **Depth** (path from root to node), **Degree** (number of children).

### 🔥 Binary Tree
- Each node has at most 2 children (left, right).
- **Traversals**:
  - **Inorder** (Left, Root, Right) — gives sorted order for BST
  - **Preorder** (Root, Left, Right) — used to copy tree
  - **Postorder** (Left, Right, Root) — used to delete tree
  - **Level order** (BFS, using queue)

### 🔥 Binary Search Tree (BST)
- Left subtree < Root < Right subtree (for all nodes).
- Search/Insert/Delete: O(log n) average, O(n) worst case (skewed tree).
- **Deletion cases**: leaf node (simply remove), one child (replace with child), two children (replace with inorder successor/predecessor).

### AVL Tree
- Self-balancing BST. **Balance factor** = height(left) − height(right), must be in {-1, 0, 1}.
- Rebalancing via **rotations**: LL, RR, LR, RL rotations.
- Guarantees O(log n) for all operations always (unlike plain BST).

### Red-Black Tree
- Self-balancing BST with color property (red/black nodes).
- Rules: root is black, red node can't have red child, every path root→null has same number of black nodes.
- Used in practice (e.g., Java TreeMap, Linux kernel schedulers).

### B-Trees
- Generalization of BST allowing multiple keys per node — used in databases/file systems for disk-based storage (minimizes disk reads).

### 🔥 Spanning Tree / MST (Minimum Spanning Tree)
- Subgraph connecting all vertices with minimum total edge weight, no cycles.
- **Prim's Algorithm**: grow tree from a starting vertex, always add cheapest edge connecting tree to a new vertex. Uses priority queue. O(E log V).
- **Kruskal's Algorithm**: sort all edges by weight, add edge if it doesn't form a cycle (use Union-Find/Disjoint Set). O(E log E).
- Both are **greedy algorithms**.

### 🔥 Graph Traversals
- **DFS (Depth-First Search)**: uses stack (or recursion), goes deep before wide. Good for detecting cycles, topological sort, connected components.
- **BFS (Breadth-First Search)**: uses queue, explores neighbors level by level. Good for shortest path in unweighted graphs.

### Shortest Path Algorithms
- **Dijkstra's Algorithm** (Single-Source Shortest Path): greedy, works with non-negative weights, uses priority queue. O((V+E) log V).
- **Bellman-Ford**: handles negative weights, detects negative cycles. O(VE).
- **Floyd-Warshall** (All-Pair Shortest Path): dynamic programming, O(V³), computes shortest paths between all pairs.

---

## MODULE 3: Dynamic Programming & Greedy

### 🔥 Dynamic Programming (DP) — Core Idea
- Break problem into overlapping subproblems, store results (memoization/tabulation) to avoid recomputation.
- **Principle of Optimality**: an optimal solution to a problem contains optimal solutions to its subproblems.

### 🔥 0/1 Knapsack Problem (DP) — very common
- Given items with weight/value, maximize value within weight capacity W, each item used 0 or 1 times (can't fraction it).
- Recurrence: `dp[i][w] = max(dp[i-1][w], dp[i-1][w-wt[i]] + val[i])` if `wt[i] <= w`, else `dp[i][w] = dp[i-1][w]`.
- Time: O(n × W).

### Matrix Chain Multiplication
- Find optimal order to multiply matrices to minimize scalar multiplications. Classic DP problem, O(n³).

### Longest Common Subsequence (LCS)
- Find longest subsequence common to two strings (not necessarily contiguous).
- `dp[i][j] = dp[i-1][j-1]+1` if chars match, else `max(dp[i-1][j], dp[i][j-1])`.

### Strassen's Matrix Multiplication
- Divide and conquer approach to multiply 2 matrices in O(n^2.81) instead of standard O(n³), using 7 multiplications instead of 8.

### 🔥 Greedy Approach
- Make locally optimal choice at each step, hoping for global optimum. Doesn't always give optimal solution (unlike DP) but is faster.

### Activity Selection Problem
- Select maximum number of non-overlapping activities. Greedy: sort by finish time, pick activity if it starts after last selected activity's finish.

### 🔥 Huffman Coding
- Greedy algorithm for lossless data compression. Build binary tree bottom-up: repeatedly merge two lowest-frequency nodes. More frequent characters get shorter codes.

### Fractional Knapsack
- Same as 0/1 knapsack but items can be broken into fractions. Greedy: sort by value/weight ratio, take as much as possible of highest ratio items first. (Unlike 0/1, greedy WORKS optimally here.)

### Branch and Bound
- Used for optimization problems (TSP, Knapsack) — systematically explores solution space, "bounds" (prunes) branches that can't beat the current best solution.
- **Traveling Salesman Problem (TSP)**: visit all cities exactly once, minimize total distance, return to start. NP-Hard.
- **Job Sequencing with Deadlines**: each job has deadline + profit, maximize profit by scheduling jobs before their deadlines (greedy, one job per time slot).

---

## MODULE 4: String Matching & Approximation Algorithms

### 🔥 Naïve String Matching
- Check every possible position in text for pattern match. O((n-m+1)×m) — slow for large text.

### 🔥 KMP (Knuth-Morris-Pratt) Algorithm
- Preprocesses pattern to build **LPS array (Longest Prefix Suffix)**, avoids re-checking characters already matched. O(n+m) — much faster than naive.
- Key idea: when mismatch occurs, use LPS array to skip ahead intelligently instead of restarting.

### 🔥 Rabin-Karp Algorithm
- Uses **hashing** to find pattern matches — computes hash of pattern and hash of each substring of text, compares hashes first (fast), only compares strings char-by-char if hashes match. Good for multiple pattern search.

### Approximation Algorithms (used when exact solution is NP-Hard/too slow)
- **Vertex Cover**: find minimum set of vertices covering all edges. Approximation: repeatedly pick an edge, add both endpoints to cover, remove all edges covered — gives 2-approximation.
- **Set Covering Problem**: choose minimum number of sets that cover a universe of elements.
- **Subset-Sum Problem**: determine if subset of numbers sums to a target value. NP-Complete in general, has pseudo-polynomial DP solution.

---

## MODULE 5: NP-Completeness

### 🔥 P vs NP vs NP-Complete vs NP-Hard (guaranteed concept Q)
- **P**: problems solvable in polynomial time.
- **NP**: problems whose solution can be *verified* in polynomial time (not necessarily solved quickly).
- **NP-Complete**: problems in NP that every other NP problem can be reduced to in polynomial time (hardest problems in NP). Example: SAT, TSP (decision version), Knapsack (decision version).
- **NP-Hard**: at least as hard as NP-Complete problems, but may not be in NP themselves (may not even be decidable).
- **Open question**: whether P = NP (unsolved, one of the Millennium Prize Problems).

### NP-Completeness Proofs
- To prove a problem X is NP-Complete: (1) show X is in NP (solution verifiable in poly time), (2) reduce a known NP-Complete problem to X in polynomial time.

### Hamiltonian Cycle
- A cycle that visits every vertex exactly once and returns to start. Deciding if one exists is NP-Complete.

### SAT (Boolean Satisfiability)
- First problem proven NP-Complete (Cook-Levin theorem). Determine if there's an assignment of true/false to variables making a boolean formula true.

---

# SECTION B: MCQ RAPID-FIRE FACTS (Section 3 — 20 MCQs)

Quick true facts likely tested as MCQs:

- Stack: LIFO | Queue: FIFO
- Postfix evaluation uses a **stack**
- Recursion uses **stack** internally (call stack)
- Binary Search requires a **sorted** array, complexity O(log n)
- Merge Sort & Quick Sort both use **Divide and Conquer**
- Merge Sort is **stable**, Quick Sort is **not stable**, Heap Sort is **not stable**
- Best sorting algorithm for nearly-sorted data: **Insertion Sort**
- BST inorder traversal gives **sorted (ascending)** order
- AVL Tree balance factor range: **-1, 0, +1**
- Prim's & Kruskal's are used for **Minimum Spanning Tree**
- Kruskal's uses **Union-Find (Disjoint Set)**; Prim's uses **Priority Queue**
- DFS uses **Stack**; BFS uses **Queue**
- Dijkstra's algorithm fails with **negative edge weights** (use Bellman-Ford instead)
- Floyd-Warshall solves **All-Pairs Shortest Path**, uses **Dynamic Programming**
- Dynamic Programming = "optimal substructure + overlapping subproblems"
- Greedy ≠ always optimal (0/1 Knapsack fails with greedy; Fractional Knapsack works with greedy)
- Huffman Coding is used for **data compression**
- KMP algorithm complexity: **O(n+m)**; Naive: **O(n·m)**
- P = polynomial time solvable; NP = verifiable in polynomial time
- SAT was the first problem proven **NP-Complete**
- TSP, Knapsack (decision version), Vertex Cover, Hamiltonian Cycle — all **NP-Complete/NP-Hard**
- Big-O = worst case (upper bound); Big-Omega = best case (lower bound); Big-Theta = average/tight bound
- Array: fixed size, random access O(1) | Linked List: dynamic size, no random access, O(n) access
- Doubly linked list allows **both direction** traversal
- Circular Queue solves the problem of **wasted space** in simple queue array implementation
- 2^n − 1 = minimum moves in **Tower of Hanoi** for n disks
- Master Theorem is used to solve **divide-and-conquer recurrence relations**

---

# LAST-MINUTE STRATEGY

**Section 1 (Long Answer, attempt 2 of 4):** Pick the 2 topics you know best after reading Section A — sorting algorithms, DP (Knapsack/LCS), or graph algorithms (Prim's/Kruskal's/Dijkstra's) are usually safest bets since they have clear step-by-step explanations + a worked example you can write out.

**Section 2 (Case Study, 2 questions):** These usually give a scenario (e.g., "a company needs to find shortest delivery routes" → apply Dijkstra's/BFS; "optimize resource allocation" → apply DP/Greedy; "detect duplicate data" → hashing/string matching). Read the scenario carefully, identify which *category* of problem it maps to (sorting/searching/graph/DP/greedy), then explain the algorithm + why it fits.

**Section 3 (MCQ):** Time-box yourself — don't get stuck, mark and move on. The facts in Section B above cover the most commonly tested points.

Good luck! You know more than you think once it's organized like this — go get some sleep after one read-through.
