from collections import deque
from typing import List, Optional
from copy import deepcopy
import heapq
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
    open_set = []
    start_tuple = grid_to_tuple(start.grid)
    end_tuple = grid_to_tuple(end.grid)

    heapq.heappush(open_set, (heuristic(start), 0, start, [start]))
    visited = {start_tuple: 0}

    while open_set:
        f, g, current, path = heapq.heappop(open_set)

        if grids_equal(current.grid, end.grid):
            return path

        # Explore next states
        for next_state in current.moves():
            next_tuple = grid_to_tuple(next_state.grid)
            new_g = g + 1
            new_f = new_g + heuristic(next_state)

            if next_tuple not in visited or new_g < visited[next_tuple]:
                visited[next_tuple] = new_g
                heapq.heappush(open_set, (new_f, new_g, next_state, path + [next_state]))

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
   tester()
