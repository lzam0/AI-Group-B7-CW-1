from a1_state import State

class Agent:
    def __init__(self, name, modes, size):
        self.name = name if name else "B7"
        self.modes = modes 
        self.size = size

    def __str__(self):
        pass

    def move(self, state, mode):
        return None
    
    def minimax(self):
        pass
    
def tester():
    pass

