from typing import List, Tuple, Generator
import copy
import random

class State:
    def __init__(self, grid):

        if grid is None:
            self.grid = [[0 for _ in range(5)] for _ in range(4)] # Create a 4x5 grid of zeros
            self.fillGrid((random.randint(5,15)))  # fill the grid with 5-15 active cells
        else:
            self.grid = grid


    def __str__(self):
        """
        Return a readable string of the board
        """
        return "\n".join(" ".join(str(cell) for cell in row) for row in self.grid)
    
    def moves(self):
        """
            A generator method named moves() that yields all possible states reachable 
            in one move (i.e., removing one counter from any active cell). 
        """
        # Get all active positions on the board
        active_pos = self.getPositions()

        # Iterate through each active cell
        for (i,j) in active_pos:
            # Make a copy of the grid
            new_grid = [row[:] for row in self.grid]
            
            # Remove the counter at that position
            new_grid[i][j] -= 1

            # Create a new yield
            yield State(new_grid)

    def numRegions(self):
        """
        Calculates and returns the number of connected regions of active nodes.
        Active nodes are non-zero cells. 
        Connectivity includes diagonal, horizontal, and vertical neighbors.
        """

        rows = len(self.grid)
        cols = len(self.grid[0])
        visited = [[False for _ in range(cols)] for _ in range(rows)]
        region_count = 0

        # Example of what visited looks like initally
        """ 4x5 grid
        [False, False, False, False, False]
        [False, False, False, False, False]
        [False, False, False, False, False]
        [False, False, False, False, False]
        """

        # Directions for all 8 neighboring cells
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1),  (1, 0), (1, 1)
        ]

        def dfs(r, c):
            """Depth-first search to mark connected cells."""
            stack = [(r, c)]
            while stack:
                x, y = stack.pop()
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols:
                        if not visited[nx][ny] and self.grid[nx][ny] != 0:
                            visited[nx][ny] = True
                            stack.append((nx, ny))

        # Iterate over all cells
        for i in range(rows):
            for j in range(cols):
                if self.grid[i][j] != 0 and not visited[i][j]:
                    visited[i][j] = True
                    dfs(i, j)
                    region_count += 1

        return region_count

    def numHingers(self):
        """
            A method numHingers() that calculates and returns the number of active 
            "Hingers" nodes on the board.  
        """
        # Amount of active nodes
        active_nodes = 0

        # Iterte through the grid
        for row in self.grid:

            # Iterate through the values in the row
            for value in row:

                # If value is a value other than 0 - It is considered an active node
                if value != 0:
                    active_nodes += 1 # Increment
        return active_nodes
    
    
    def fillGrid(self, count=15, max_value=9):
        total_cells = 4*5

        # Ensure we do not try to fill more cells than exist in the grid
        count = min(count, total_cells)

        # Choose with cells to fill randomly
        chosen_positions = random.sample(range(total_cells), count)

        for pos in chosen_positions:
            row, col = divmod(pos, 5)

            # Fill the chosen cell with a random value
            self.grid[row][col] = random.randint(1, max_value)

    def getPositions(self, value=None):
        """
        Return all positions of a given value in the grid.
        If value is 0 (None), return all non-zero positions
        """
        positions = []
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if value is None:
                    if cell != 0:
                        positions.append((i, j))
                    else:
                        positions.append((i,j))
        return positions

    
    

def tester():
    sa = State(None)  # random board with 5–15 active cells
    print(sa)

    active_hingers = sa.numHingers()
    print("Active Hingers on Board: ",active_hingers)
    print("Active Regions:", sa.numRegions())
    # for next_state in sa.moves():
    #     print(next_state)
    #     print("\n")



if __name__ == "__main__":
    tester()