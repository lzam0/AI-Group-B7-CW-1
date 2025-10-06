class Agent:
    def __init__(self, name, modes, size):
        self.name = name if name else "B7"  # Our Group name is B7
        self.modes = modes  # List of game-playing strategies
        self.size = size  # Size of the board (e.g., 4 for 4x4)

    def move(self, state, mode):
        return None
    
    