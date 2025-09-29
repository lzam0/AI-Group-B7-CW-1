import List

class State:
    def __init__(self, board: List[List[int]]):
        self.board = board
        self.size = len(board)

    def __str__():
        """
        Return a readable string
        """
        rows = []
        for row in self.board:
            rows.append(" ".join(f"{x:2d}" if x != 0 else " ." for x in row))
        return "\n".join(rows)
    
    def moves():
        """
            A generator method named moves() that yields all possible states reachable 
            in one move (i.e., removing one counter from any active cell). 
        """
        return None

    def numRegions():
        """
            A method numRegions() that calculates and returns the number of active 
            regions on the board.  
        """
        active_regions = 0

        return active_regions
    
    def numHingers():
        """
            Returns the number of hinger cells in the current state
            """
        return None
    
    def tester():
        return None
    
