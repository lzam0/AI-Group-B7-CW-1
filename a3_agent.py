from a1_state import State

# Agent = Architecture + Program

class Agent:
    def __init__(self, size, modes=None, name=None):
        self.name = name if name else "B7"
        self.size = size
        self.modes = modes if modes is not None else []
        self.state = State([[0] * size for _ in range(size)])  # Initialize the board state

    def __str__(self):
        """
        Return a string representation of the Agent, including its name, board size, and available modes.
        """
        modes_str = ', '.join(self.modes) if self.modes else 'No modes available'
        return f"Agent Name: {self.name}\nBoard Size: {self.size}x{self.size}\nAvailable Modes: {modes_str}"

    def move(self, state, mode):

        # Check if mode is available in agent's modes
        if mode not in self.modes:
            raise ValueError(f"Mode '{mode}' is not available for this agent.")
        
        # 
    
    def minimax(self):
        pass
    
def tester():
    """
        This method is to demonstrate and validate 
        the agent’s behavior across scenarios.
    """
    
    print("Testing Agent class...")

if __name__ == "__main__":
    tester()