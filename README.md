# CECS-326 - Group Project 3: Banker's Algorithm

This project demonstrates **deadlock avoidance using the Banker's Algorithm** in Python. The system models multiple processes and resource types, verifying safety and handling resource requests only when they keep the system in a **safe state**.

---
## Requirements
- **OS:** Linux, macOS, or Windows (standard Python runtime)
- **Python:** Version 3.8 or newer

---
## How to Run
Run the program directly using Python. No command-line arguments are required.

```bash
python3 bankers.py
```

To try custom inputs, open the file and uncomment the interactive_mode() call at the bottom, then run again.

---
## Example Output

```text

BANKER'S ALGORITHM SIMULATION
============================================================

CURRENT SYSTEM STATE
============================================================

Available Resources:
[3, 3, 2]

Maximum Matrix:
Process  R0  R1  R2  
P0       7   5   3   
P1       3   2   2   
P2       9   0   2   
P3       2   2   2   
P4       4   3   3   

Allocation Matrix:
Process  R0  R1  R2  
P0       0   1   0   
P1       2   0   0   
P2       3   0   2   
P3       2   1   1   
P4       0   0   2   

Need Matrix:
Process  R0  R1  R2  
P0       7   4   3   
P1       1   2   2   
P2       6   0   0   
P3       0   1   1   
P4       4   3   1   
============================================================

============================================================
CHECKING INITIAL SAFETY
============================================================
System is in a SAFE state!
Safe sequence: P1 -> P3 -> P4 -> P0 -> P2

============================================================
TESTING RESOURCE REQUESTS
============================================================

Process P1 requests: [1, 0, 2]
Result: Request granted. Safe sequence: P1 -> P3 -> P4 -> P0 -> P2

Process P4 requests: [3, 3, 0]
Result: Resources not available. Process P4 must wait.

Process P0 requests: [0, 2, 0]
Result: Request denied. System would be in an unsafe state.
```

