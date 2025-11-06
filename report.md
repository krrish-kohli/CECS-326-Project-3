# CECS 326 — Group Project 3 Report
- **Program:** `bankers.py`
- **Group Members:**
  - Krrish Kohli, 031530055
  - Beau Cordero, 029378347

---

## 1. Objective
The goal of this program is to implement the **Banker’s Algorithm** in Python to avoid deadlock by:
- Determining whether a given system state is **safe** (Safety Algorithm).
- Handling **resource requests** so they are **granted only if** the system remains safe after the tentative allocation (Resource-Request Algorithm).

This implementation is designed for clarity and classroom use, featuring a readable state printer, a built-in demonstration (textbook-style example), and an optional interactive mode.

---

## 2. Design of the Program

### a) Program structure
The project centers on a single class that encapsulates all algorithmic behavior:

1. **`class BankersAlgorithm`** — Maintains system state and provides algorithm operations.
   - **Core data**
     - `self.available` — vector of free instances for each resource type.
     - `self.maximum` — maximum demand matrix.
     - `self.allocation` — current allocation matrix.
     - `self.need` — computed as `maximum - allocation`.
   - **Core methods**
     - `calculate_need()` — constructs `need` from `maximum` and `allocation`.
     - `is_safe()` — Safety Algorithm; checks if a safe sequence exists.
     - `request_resources(process_id, request)` — Resource-Request Algorithm; simulates, validates with `is_safe()`, and commits or rolls back.
     - `print_state()` — formatted dump of `Available`, `Maximum`, `Allocation`, and `Need`.
     - `format_sequence(sequence)` — helper to render sequences like `P1 -> P3 -> P4`.

2. **Driver / entry points**
   - `main()` — runs a classic example with **5 processes** and **3 resource types** and performs three sample requests.
   - `interactive_mode()` — optional menu to enter custom matrices and issue requests.

The code is self-contained (no external packages) and targets Python ≥ 3.8.

---

### b) State representation
The system state follows the standard Banker’s Algorithm notation for **n** processes and **m** resource types:

- **`Available[m]`** — free instances for each resource type.
- **`Maximum[n][m]`** — each process’ declared maximum.
- **`Allocation[n][m]`** — what each process currently holds.
- **`Need[n][m]`** — remaining demand, computed by:
Need[i][j] = Maximum[i][j] - Allocation[i][j]

These structures are stored as Python lists of `int`. The constructor takes deep copies to avoid aliasing with caller data.

---

### c) Safety Algorithm (`is_safe()`)
**Purpose.** Determine if the current state is safe, i.e., there exists an order of process completion that allows all processes to finish without deadlock.

**Data used.**
- `work` — a local copy of `available`.
- `finish[n]` — tracks whether each process can (eventually) finish.
- `safe_sequence` — the discovered completion order.

**Procedure.**
1. Initialize `work = available[:]` and `finish = [False] * n`.
2. Repeatedly search for an unfinished process `i` such that:
Need[i] <= work (component-wise)
3. If found:
- Mark `finish[i] = True`.
- Append `i` to `safe_sequence`.
- Release its allocation back to `work`:
  ```
  work = work + Allocation[i]
  ```
4. If during a full pass no such process exists while some remain unfinished, the state is **unsafe**.
5. Return `(True, safe_sequence)` if all processes finish; otherwise `(False, [])`.

---

### d) Resource-Request Algorithm (`request_resources(process_id, request)`)
**Purpose.** Decide whether to grant a specific request `request[m]` from process `process_id`.

**Guard checks.**
1. **Maximum claim:** Reject immediately if any `request[j] > need[process_id][j]`.
2. **Availability:** Reject if any `request[j] > available[j]`.

**Tentative allocation and validation.**

3. Save the old state: copies of `available`, `allocation`, and `need`.
4. Apply the **tentative** allocation:
```
available[j] -= request[j]
allocation[i][j] += request[j]
need[i][j] -= request[j]
```

6. Run `is_safe()`:
- **If safe:** keep changes and return `True` with the safe sequence in the message.
- **If unsafe:** **rollback** to the saved state and return `False` with a denial message.

---

### e) Helper / I/O utilities
- **`print_state()`** — prints the four structures in aligned tables, helping verify inputs and step-throughs during demos.
- **`format_sequence(sequence)`** — renders indices as `P0`, `P1`, … for readability.
- **`interactive_mode()`** — prompts for `n`, `m`, and row-wise entry of `Available`, `Maximum`, and `Allocation`; supports repeated requests and re-checks without restarting the program.

---

### f) Complexity
Let `n` be the number of processes and `m` the number of resource types.

- **Safety check `is_safe()`**: worst-case **O(n² · m)**  
(each pass can finish at most one new process; for each candidate, we compare across `m` resources).
- **Resource request**: dominated by a call to `is_safe()` → **O(n² · m)** per request.

The implementation favors clarity and correctness over micro-optimizations.

---

### g) Output and execution
- **Default demo (`main`)**:
1. Prints the initial matrices.
2. Reports whether the initial state is safe and shows a safe sequence if one exists.
3. Processes three sample requests in sequence, printing grant/deny decisions and (when granted) the new safe sequence.
- **Interactive mode**:
- Users can test custom matrices, issue arbitrary requests, reprint state, and recheck safety in one session.

---

### h) Correctness & deadlock avoidance
- **Soundness of `is_safe()`**: A state is declared safe **only** when the algorithm constructs an explicit order that finishes all processes; if no such order exists, the method returns unsafe.
- **Safety preservation in `request_resources()`**: Requests are **tentatively** applied and committed **only if** the resulting state passes `is_safe()`. Otherwise, the state is rolled back exactly, ensuring the system never transitions into an unsafe state.


---

## 3. How to Run
```bash
python3 bankers.py
```
