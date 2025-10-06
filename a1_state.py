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
    
    def moves():
        """
            A generator method named moves() that yields all possible states reachable 
            in one move (i.e., removing one counter from any active cell). 
        """
        return None

    def numRegions(self):
        """
        A method numRegions() that calculates and returns the number of active
        nodes on the board

        This is done by checking each position of the active nodes on the board
        then it checks if the position of the nodes are connected
        CONNECTED nodes MUST be either diaginal or next to opposing nodes

        Utilise Depth First Search or Breadth First Search to traverse the grid
        to find connected clusters together
        """

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

    
    

def tester():
    sa = State(None)  # random board with 5–15 active cells
    print(sa)

    active_hingers = sa.numHingers()
    print("Active Hingers on Board: ",active_hingers)

if __name__ == "__main__":
    tester()