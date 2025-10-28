"""
Hinger Project
Coursework 001 for: CMP-6058A Artificial Intelligence

Includes functions for algorithm pathways

@author: B7 (100385659, 100400087, and 89123)
@date:   29/09/2025
"""

from collections import deque
from typing import List, Optional
from copy import deepcopy
import heapq
import time
import matplotlib.pyplot as plt
import itertools
from a1_state import State 

def grids_equal(grid1, grid2) -> bool:
    """Check if two 2D grids are identical."""
    return all(row1 == row2 for row1, row2 in zip(grid1, grid2))

# BFS implememntation

def path_BFS(start: State, end: State) -> Optional[List[State]]:

    # Convert grids to tuples for hashing
    def grid_to_tuple(grid):
        return tuple(tuple(row) for row in grid)
    
    start_tuple = grid_to_tuple(start.grid)
    end_tuple = grid_to_tuple(end.grid)
    
    queue = deque([(start, [start])])
    visited = {start_tuple}
    
    while queue:
        current_state, path = queue.popleft()
        
        # Goal check
        if grids_equal(current_state.grid, end.grid):
            return path
        
        # Exploring possible moves
        for next_state in current_state.moves():
            next_tuple = grid_to_tuple(next_state.grid)
            
            if next_tuple not in visited:
                visited.add(next_tuple)
                queue.append((next_state, path + [next_state]))
    
    # No path found
    return None

# Test Harness for BFS

def test_path_BFS():
    grid_start = [
        [3, 0, 0, 2, 0],
        [0, 4, 0, 0, 0],
        [0, 0, 2, 0, 1],
        [0, 0, 0, 0, 0]
    ]
    
    grid_end = [
        [2, 0, 0, 1, 0],
        [0, 3, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0]
    ]

    start_state = State(grid_start)
    end_state = State(grid_end)

    path = path_BFS(start_state, end_state)

    if path is None:
        print("No safe path found.")
    else:
        print(f"Path found in {len(path) - 1} moves!")
        for step, state in enumerate(path):
            print(f"\nStep {step}:")
            print(state)

# DFS implementation

def path_DFS(start: State, end: State):

    def grids_equal(grid1, grid2) -> bool:
        # Check if two 2D grids are identical.
        return all(row1 == row2 for row1, row2 in zip(grid1, grid2))

    def grid_to_tuple(grid):
        # Convert grids to tuples to be hashed
        return tuple(tuple(row) for row in grid)

    visited = set()

    def dfs(current: State, path: list):
        current_tuple = grid_to_tuple(current.grid)
        visited.add(current_tuple)

        # Goal check
        if grids_equal(current.grid, end.grid):
            return path

        # Explore neighbors (possible moves)
        for next_state in current.moves():
            next_tuple = grid_to_tuple(next_state.grid)

            if next_tuple not in visited:
                result = dfs(next_state, path + [next_state])
                if result is not None:
                    return result

        # No path found
        return None 
    return dfs(start, [start])
    

# Test Harness for DFS

def test_path_DFS():
    grid_start = [
        [2, 0, 0, 0, 0],
        [0, 3, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0]
    ]

    grid_end = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]

    start_state = State(grid_start)
    end_state = State(grid_end)

    path = path_DFS(start_state, end_state)

    if path is None:
        print("No safe path found.")
    else:
        print(f"DFS Path found in {len(path) - 1} moves!")
        for step, state in enumerate(path):
            print(f"\nStep {step}:")
            print(state)


# IDDFS implememntation

def path_IDDFS(start: State, end: State) -> Optional[List[State]]:

    def grids_equal(grid1, grid2) -> bool:
        # Check if two 2D grids are identical.
        return all(row1 == row2 for row1, row2 in zip(grid1, grid2))

    def grid_to_tuple(grid):
        # Convert a grid into a tuple for hashing.
        return tuple(tuple(row) for row in grid)

    # Recursive DFS with depth limit
    def dls(current: State, end: State, limit: int, path: List[State], visited: set):
        """Depth-Limited Search (DLS) used by IDDFS."""
        if grids_equal(current.grid, end.grid):
            return path

        if limit == 0:
            return None

        current_tuple = grid_to_tuple(current.grid)
        visited.add(current_tuple)

        for next_state in current.moves():
            next_tuple = grid_to_tuple(next_state.grid)
            if next_tuple not in visited:
                result = dls(next_state, end, limit - 1, path + [next_state], visited)
                if result is not None:
                    return result
        return None

    # Iteratively deepen the search
    max_depth = 50
    for depth in range(max_depth):
        visited = set()
        result = dls(start, end, depth, [start], visited)
        if result is not None:
            return result

    return None
    
# Test harness for IDDFS

def test_path_IDDFS():

    grid_start = [
        [2, 0, 0, 0, 0],
        [0, 3, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0]
    ]

    grid_end = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]

    start_state = State(grid_start)
    end_state = State(grid_end)

    path = path_IDDFS(start_state, end_state)

    if path is None:
        print("No safe path found.")
    else:
        print(f"IDDFS Path found in {len(path) - 1} moves!")
        for step, state in enumerate(path):
            print(f"\nStep {step}:")
            print(state)


# A* implementation

# Heuristic justification:
# The heuristic h(n) is the number of active (non-zero) cells in the grid.
# Each move removes one counter, so this never overestimates the true cost,
# making it admissible and consistent.

def path_astar(start: State, end: State) -> Optional[List[State]]:
    def grids_equal(grid1, grid2) -> bool:
        # Check if two grids are identical.
        return all(row1 == row2 for row1, row2 in zip(grid1, grid2))

    def grid_to_tuple(grid):
        # Convert grid to tuple for hashing.
        return tuple(tuple(row) for row in grid)

    def heuristic(state: State) -> int:
        return sum(1 for row in state.grid for cell in row if cell != 0)

    # Priority queue for A* (min-heap)
    # Use a tie-breaker counter to avoid comparing State objects when f and g tie.
    open_set = []
    counter = itertools.count()
    start_tuple = grid_to_tuple(start.grid)
    end_tuple = grid_to_tuple(end.grid)

    # heap entries: (f, g, counter, state_tuple, State, path)
    heapq.heappush(open_set, (heuristic(start), 0, next(counter), start_tuple, start, [start]))
    visited = {start_tuple: 0}

    while open_set:
        f, g, _, current_tuple, current, path = heapq.heappop(open_set)

        # Skip stale entries: if we have already found a better g for this state
        if visited.get(current_tuple, float('inf')) < g:
            continue

        if grids_equal(current.grid, end.grid):
            return path

        # Explore next states
        for next_state in current.moves():
            next_tuple = grid_to_tuple(next_state.grid)
            new_g = g + 1
            new_f = new_g + heuristic(next_state)

            # If we haven't seen this state or found a cheaper path to it
            if next_tuple not in visited or new_g < visited[next_tuple]:
                visited[next_tuple] = new_g
                heapq.heappush(open_set, (new_f, new_g, next(counter), next_tuple, next_state, path + [next_state]))

    return None

# Test harness for A*

def test_path_astar():

    grid_start = [
        [2, 0, 0, 0, 0],
        [0, 3, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0]
    ]

    grid_end = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]

    start_state = State(grid_start)
    end_state = State(grid_end)

    path = path_astar(start_state, end_state)

    if path is None:
        print("No safe path found.")
    else:
        print(f"A* Path found in {len(path) - 1} moves!")
        for step, state in enumerate(path):
            print(f"\nStep {step}:")
            print(state)

# UCS implementation

# We use Uniform Cost Search (UCS) because it guarantees finding the
# least-cost path between two states when all move costs are non-negative.
# In this version of Hinger, the move cost is proportional to the
# value of the hinge being removed, so UCS is ideal for minimizing
# the total hinge removal cost.

def min_safe(start: State, end: State): 
 
    from heapq import heappush, heappop
    import itertools

    def grid_to_tuple(grid):
        return tuple(tuple(row) for row in grid)

    start_tuple = grid_to_tuple(start.grid)
    end_tuple = grid_to_tuple(end.grid)

    counter = itertools.count()
    # heap entries: (total_cost, tie_counter, state_tuple, State, path)
    pq = [(0, next(counter), start_tuple, start, [start])]
    visited = {start_tuple: 0}

    while pq:
        cost, _, current_tuple, current, path = heappop(pq)

        # Skip stale entries where we've already found a better cost
        if visited.get(current_tuple, float('inf')) < cost:
            continue

        if current_tuple == end_tuple:
            return path

        for (i, j) in current.getPositions():  # all active cells
            next_grid = [row[:] for row in current.grid]
            # Since State.moves() decrements by 1, the cost per such move is 1
            move_cost = 1
            next_grid[i][j] -= 1
            next_state = State(next_grid)
            next_tuple = grid_to_tuple(next_grid)
            new_cost = cost + move_cost

            if next_tuple not in visited or new_cost < visited[next_tuple]:
                visited[next_tuple] = new_cost
                heappush(pq, (new_cost, next(counter), next_tuple, next_state, path + [next_state]))

    return None

# Test Harness for UCS

def test_min_safe():
    """Test the min_safe() function using Uniform Cost Search."""
    grid_start = [
        [3, 0, 0, 1, 0],
        [0, 2, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0]
    ]

    grid_end = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]

    start_state = State(grid_start)
    end_state = State(grid_end)

    path = min_safe(start_state, end_state)

    if path is None:
        print(" No safe path found.")
    else:
        total_cost = 0
        # Calculate total cost based on your move cost function
        for i in range(len(path) - 1):
            total_cost += sum(
                abs(path[i].grid[r][c] - path[i + 1].grid[r][c])
                for r in range(len(path[i].grid))
                for c in range(len(path[i].grid[0]))
            )

        print(f" Path found in {len(path) - 1} moves! (Total cost: {total_cost})\n")
        for step, state in enumerate(path):
            print(f"Step {step}:")
            print(state)
            print()

def compare():
    """
    Function to compare the performance of the search algorithms
    (BFS, DFS, IDDFS, and A*).

    Start grid size:
    - 4x5
    - 3x3
    - 6x7
    """

    # List of test grids (each entry is a tuple of start and goal)
    test_cases = [
        
        ( # Compare Case 1 - Smaller Grid 3x3
            [ # Start Grid
                [1, 2, 3],
                [3, 3, 1],
                [2, 2, 2]
            ],
            [ # Goal Grid
                [0, 2, 1],
                [3, 2, 1],
                [0, 0, 2]
            ]),
        ( # Compare Case 2 - Default Game Grid 4x5
            [ # Start Grid
                [0, 0, 0, 3, 3],
                [0, 3, 2, 2, 0],
                [0, 0, 2, 0, 2],
                [0, 1, 0, 1, 0]
            ],
            [ # Goal Grid
                [0, 0, 0, 0, 3],
                [0, 1, 1, 2, 0],
                [0, 0, 0, 0, 2],
                [0, 0, 0, 1, 0]
            ]
        ),
        ( # Compare Case 3 - Large Grid 6x7
            [  # Start Grid
                [0, 0, 1, 0, 0, 2, 0],
                [0, 0, 0, 3, 0, 0, 0],
                [0, 0, 2, 0, 2, 0, 0],
                [0, 0, 3, 0, 0, 1, 0],
                [0, 0, 0, 0, 3, 0, 3],
                [0, 2, 0, 0, 0, 0, 0]
            ],
            [ # End Grid
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]
            ]
        )
    ]

    # Map algorithm names to their corresponding functions
    search_algorithms = {
        "BFS": path_BFS,
        "DFS": path_DFS,
        "IDDFS": path_IDDFS,
        "A*": path_astar
    }

    # Record times for each algorithm
    times = {name: [] for name in search_algorithms.keys()}

    for i, (start_grid, goal_grid) in enumerate(test_cases, start=1):
        start_state = State(start_grid)
        goal_state = State(goal_grid)

        print(f"\n--- Test Case {i} ---")
        print("Start Grid:")
        print(start_state)
        print("\nGoal Grid:")
        print(goal_state)

        for name, func in search_algorithms.items():
            start_time = time.time()
            result = func(start_state, goal_state)
            elapsed_time = time.time() - start_time
            # If algorithm exceeds 20 seconds, stop and mark as >20
            if elapsed_time > 20:
                print(f"{name} exceeded 20 seconds, skipping further execution.")
                times[name].append(20.1)  # Use 20.1 to indicate it exceeded
            else:
                times[name].append(elapsed_time)
                print(f"{name} took {elapsed_time:.6f} seconds")

    # Compute averages (ignoring values >20 for realistic average if desired)
    avg_times = {}
    for name, lst in times.items():
        # Compute average, treating >20 as 20 for average
        adjusted = [min(t, 20) for t in lst]
        avg_times[name] = sum(adjusted) / len(adjusted)

    print("\n--- Average Times ---")
    for name, avg in avg_times.items():
        print(f"{name}: {avg:.6f} seconds")

    # Plotting
    test_labels = [f"Case {i}" for i in range(1, len(test_cases)+1)]
    plt.figure(figsize=(10,6))

    for name, lst in times.items():
        plt.plot(test_labels, lst, marker='o', label=name)

    for name, avg in avg_times.items():
        plt.hlines(avg, xmin=0, xmax=len(test_cases)-1, colors='gray', linestyles='dashed', alpha=0.5)

    plt.title("Algorithm Performance Comparison")
    plt.xlabel("Test Cases")
    plt.ylabel("Time (seconds)")
    plt.legend()
    plt.grid(True)
    plt.show()

    
# Tester function

def tester():
    print("=== Testing Algorithms ===")

    print("\n~ BFS Test ~")
    test_path_BFS()

    print("\n~ DFS Test ~")
    test_path_DFS()

    print("\n~ IDDFS Test ~")
    test_path_IDDFS()

    print("\n~ A* Test ~")
    test_path_astar()

    print("\n=== All tests completed ===")


# Run tests
 
if __name__ == "__main__":
    compare()
