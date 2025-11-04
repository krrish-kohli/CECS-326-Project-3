"""
Banker's Algorithm Implementation
CECS 326 - Operating Systems

This program implements the Banker's Algorithm for deadlock avoidance.
It includes both the Safety Algorithm and the Resource-Request Algorithm.
"""


class BankersAlgorithm:
    def __init__(self, n_processes, n_resources, available, maximum, allocation):
        """
        Initialize the Banker's Algorithm with system state.

        Parameters:
        - n_processes: Number of processes in the system
        - n_resources: Number of resource types
        - available: List of available instances of each resource type
        - maximum: 2D list representing maximum demand of each process
        - allocation: 2D list representing current allocation to each process
        """
        self.n_processes = n_processes
        self.n_resources = n_resources
        self.available = available.copy()
        self.maximum = [row.copy() for row in maximum]
        self.allocation = [row.copy() for row in allocation]

        # Calculate the Need matrix (Need = Max - Allocation)
        self.need = self.calculate_need()

    def calculate_need(self):
        """
        Calculate the Need matrix.
        Need[i][j] = Maximum[i][j] - Allocation[i][j]

        Returns: 2D list representing remaining resource needs
        """
        need = []
        for i in range(self.n_processes):
            need_row = []
            for j in range(self.n_resources):
                need_row.append(self.maximum[i][j] - self.allocation[i][j])
            need.append(need_row)
        return need

    def is_safe(self):
        """
        Safety Algorithm: Check if the system is in a safe state.

        A safe state means there exists a sequence of process execution
        that allows all processes to complete without deadlock.

        Returns: (is_safe: bool, safe_sequence: list)
        """
        # Work is a copy of Available (simulates available resources)
        work = self.available.copy()

        # Finish tracks which processes have finished
        finish = [False] * self.n_processes

        # Safe sequence stores the order of process completion
        safe_sequence = []

        # Keep trying to find processes that can complete
        while len(safe_sequence) < self.n_processes:
            found = False

            for i in range(self.n_processes):
                # Check if process i is not finished and its needs can be met
                if not finish[i]:
                    # Check if Need[i] <= Work for all resources
                    can_allocate = True
                    for j in range(self.n_resources):
                        if self.need[i][j] > work[j]:
                            can_allocate = False
                            break

                    # If process i can finish
                    if can_allocate:
                        # Add allocated resources back to work
                        for j in range(self.n_resources):
                            work[j] += self.allocation[i][j]

                        # Mark process as finished
                        finish[i] = True
                        safe_sequence.append(i)
                        found = True

            # If no process could be found in this iteration, system is unsafe
            if not found:
                return False, []

        return True, safe_sequence

    def request_resources(self, process_id, request):
        """
        Resource-Request Algorithm: Handle a resource request from a process.

        Parameters:
        - process_id: ID of the requesting process
        - request: List of requested resources for each resource type

        Returns: (granted: bool, message: str)
        """
        print(f"\nProcess P{process_id} requests: {request}")

        # Step 1: Check if request <= need
        for j in range(self.n_resources):
            if request[j] > self.need[process_id][j]:
                return False, f"Error: Process P{process_id} has exceeded its maximum claim!"

        # Step 2: Check if request <= available
        for j in range(self.n_resources):
            if request[j] > self.available[j]:
                return False, f"Resources not available. Process P{process_id} must wait."

        # Step 3: Simulate allocation (pretend to allocate)
        # Save the current state
        old_available = self.available.copy()
        old_allocation = [row.copy() for row in self.allocation]
        old_need = [row.copy() for row in self.need]

        # Try the allocation
        for j in range(self.n_resources):
            self.available[j] -= request[j]
            self.allocation[process_id][j] += request[j]
            self.need[process_id][j] -= request[j]

        # Step 4: Run safety algorithm to check if system remains safe
        is_safe, safe_seq = self.is_safe()

        if is_safe:
            # Allocation is permanent
            return True, f"Request granted. Safe sequence: {self.format_sequence(safe_seq)}"
        else:
            # Rollback the allocation
            self.available = old_available
            self.allocation = old_allocation
            self.need = old_need
            return False, "Request denied. System would be in an unsafe state."

    def format_sequence(self, sequence):
        """Helper function to format the safe sequence for display."""
        return " -> ".join([f"P{i}" for i in sequence])

    def print_state(self):
        """Print the current system state in a formatted manner."""
        print("\n" + "=" * 60)
        print("CURRENT SYSTEM STATE")
        print("=" * 60)

        print("\nAvailable Resources:")
        print(self.available)

        print("\nMaximum Matrix:")
        print("Process  ", end="")
        for j in range(self.n_resources):
            print(f"R{j}  ", end="")
        print()
        for i in range(self.n_processes):
            print(f"P{i}       ", end="")
            for j in range(self.n_resources):
                print(f"{self.maximum[i][j]}   ", end="")
            print()

        print("\nAllocation Matrix:")
        print("Process  ", end="")
        for j in range(self.n_resources):
            print(f"R{j}  ", end="")
        print()
        for i in range(self.n_processes):
            print(f"P{i}       ", end="")
            for j in range(self.n_resources):
                print(f"{self.allocation[i][j]}   ", end="")
            print()

        print("\nNeed Matrix:")
        print("Process  ", end="")
        for j in range(self.n_resources):
            print(f"R{j}  ", end="")
        print()
        for i in range(self.n_processes):
            print(f"P{i}       ", end="")
            for j in range(self.n_resources):
                print(f"{self.need[i][j]}   ", end="")
            print()

        print("=" * 60)


def main():
    """
    Main function with example test cases.

    Example from classic textbook (Silberschatz):
    5 processes (P0-P4), 3 resource types (A, B, C)
    """
    print("BANKER'S ALGORITHM SIMULATION")
    print("=" * 60)

    # System configuration
    n_processes = 5
    n_resources = 3

    # Available resources: [A, B, C]
    available = [3, 3, 2]

    # Maximum demand matrix
    maximum = [
        [7, 5, 3],  # P0
        [3, 2, 2],  # P1
        [9, 0, 2],  # P2
        [2, 2, 2],  # P3
        [4, 3, 3]  # P4
    ]

    # Current allocation matrix
    allocation = [
        [0, 1, 0],  # P0
        [2, 0, 0],  # P1
        [3, 0, 2],  # P2
        [2, 1, 1],  # P3
        [0, 0, 2]  # P4
    ]

    # Create Banker's Algorithm instance
    banker = BankersAlgorithm(n_processes, n_resources, available, maximum, allocation)

    # Display initial state
    banker.print_state()

    # Check if initial state is safe
    print("\n" + "=" * 60)
    print("CHECKING INITIAL SAFETY")
    print("=" * 60)
    is_safe, safe_seq = banker.is_safe()

    if is_safe:
        print(f"System is in a SAFE state!")
        print(f"Safe sequence: {banker.format_sequence(safe_seq)}")
    else:
        print("System is in an UNSAFE state!")

    # Test some resource requests
    print("\n" + "=" * 60)
    print("TESTING RESOURCE REQUESTS")
    print("=" * 60)

    # Request 1: P1 requests [1, 0, 2]
    success, message = banker.request_resources(1, [1, 0, 2])
    print(f"Result: {message}")

    if success:
        banker.print_state()

    # Request 2: P4 requests [3, 3, 0]
    success, message = banker.request_resources(4, [3, 3, 0])
    print(f"Result: {message}")

    # Request 3: P0 requests [0, 2, 0]
    success, message = banker.request_resources(0, [0, 2, 0])
    print(f"Result: {message}")

    if success:
        banker.print_state()


def interactive_mode():
    """
    Interactive mode for custom testing.
    """
    print("\n" + "=" * 60)
    print("INTERACTIVE MODE")
    print("=" * 60)

    # Get system configuration from user
    n_processes = int(input("\nEnter number of processes: "))
    n_resources = int(input("Enter number of resource types: "))

    # Get available resources
    print(f"\nEnter available resources ({n_resources} values):")
    available = list(map(int, input().split()))

    # Get maximum matrix
    print(f"\nEnter Maximum matrix ({n_processes} rows, {n_resources} columns):")
    maximum = []
    for i in range(n_processes):
        row = list(map(int, input(f"P{i}: ").split()))
        maximum.append(row)

    # Get allocation matrix
    print(f"\nEnter Allocation matrix ({n_processes} rows, {n_resources} columns):")
    allocation = []
    for i in range(n_processes):
        row = list(map(int, input(f"P{i}: ").split()))
        allocation.append(row)

    # Create banker instance
    banker = BankersAlgorithm(n_processes, n_resources, available, maximum, allocation)
    banker.print_state()

    # Check safety
    is_safe, safe_seq = banker.is_safe()
    if is_safe:
        print(f"\nSystem is SAFE! Sequence: {banker.format_sequence(safe_seq)}")
    else:
        print("\nSystem is UNSAFE!")

    # Handle requests
    while True:
        print("\nOptions:")
        print("1. Make a resource request")
        print("2. Display current state")
        print("3. Check safety")
        print("4. Exit")

        choice = input("\nEnter choice: ")

        if choice == '1':
            process_id = int(input("Enter process ID: "))
            print(f"Enter request for P{process_id} ({n_resources} values):")
            request = list(map(int, input().split()))
            success, message = banker.request_resources(process_id, request)
            print(f"Result: {message}")

        elif choice == '2':
            banker.print_state()

        elif choice == '3':
            is_safe, safe_seq = banker.is_safe()
            if is_safe:
                print(f"System is SAFE! Sequence: {banker.format_sequence(safe_seq)}")
            else:
                print("System is UNSAFE!")

        elif choice == '4':
            break


if __name__ == "__main__":
    # Run the main example
    main()

    # Uncomment the line below to run in interactive mode
    # interactive_mode()