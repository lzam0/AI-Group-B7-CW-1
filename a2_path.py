from collections import deque
from typing import List, Optional
from copy import deepcopy
from a1_state import State 

def grids_equal(grid1, grid2) -> bool:
    """Check if two 2D grids are identical."""
    return all(row1 == row2 for row1, row2 in zip(grid1, grid2))

def path_BFS(start: State, end: State) -> Optional[List[State]]:

    # Convert grids to immutable tuples for hashing
    def grid_to_tuple(grid):
        return tuple(tuple(row) for row in grid)
    
    start_tuple = grid_to_tuple(start.grid)
    end_tuple = grid_to_tuple(end.grid)
    
    # BFS setup
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
    # Example test
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



def path_DFS(start: State, end: State):

    def grids_equal(grid1, grid2) -> bool:
        """Check if two 2D grids are identical."""
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


# def path_IDDFS(start, end):
#     return None



# Run tests    
if __name__ == "__main__":
    print("~ BFS Test ~")
    test_path_BFS()
    print("\n~ DFS Test ~")
    test_path_DFS()
