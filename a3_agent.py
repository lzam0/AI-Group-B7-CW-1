from a1_state import State

# Agent = Architecture + Program

class Agent:
    def __init__(self, state=None, modes=None, name=None):
        """
        Initialize the Agent.
        :param state: A State object representing the initial game state.
        :param modes: List of game-playing strategies (optional).
        :param name: Agent's name (optional, defaults to 'B7').
        """
        self.name = name if name else "B7"
        self.state = state if state else State(None)  # Use provided state or create a default one
        self.modes = modes if modes is not None else []

    def __str__(self):
        """
        Return a string representation of the Agent, including its name and available modes.
        """
        modes_str = ', '.join(self.modes) if self.modes else 'No modes available'
        return f"Agent Name: {self.name}\nBoard Size: {len(self.state.grid)}x{len(self.state.grid[0])}\nAvailable Modes: {modes_str}"

    def move(self, state, mode):
        """
            Perform a move based on the given state and playing mode. 
        """
        # Minimax Mode
        if mode == "minimax":
            # Initialize variables to track the best move and its value
            best_move = None

            # Start with the lowest possible value - cannot use 0 or another value as the algorithm may return incorrect values
            best_value = float('-inf')

            # Iterate through all possible moves from the current state
            for child in state.moves():
                # Evaluate the move using the Minimax algorithm with a depth limit of 3
                move_value = self.minimax(child, depth=3, is_maximizing=False)

                # Update the best move if the current move has a higher value
                if move_value > best_value:
                    best_value = move_value
                    best_move = child

            # Return the move that leads to the best evaluated state
            return best_move
    
    def minimax(self, state, depth, is_maximizing):
        """
            Minimax recusive algorithm
            consider all possible moves up to a certain depth
            Utilising the Game Tree to evaluate the best move
        """
        if depth == 0 or not list(state.moves()):  # Terminal state or max depth
            return state.numHingers() - state.numRegions()  # Example evaluation function

        if is_maximizing:
            max_eval = float('-inf')
            for child in state.moves():
                eval = self.minimax(child, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for child in state.moves():
                eval = self.minimax(child, depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval
    
def tester():

    """
        This method is to demonstrate and validate 
        the agent’s behavior across scenarios.
    """

    print("Testing Agent class...")

    # Create a random initial state
    initial_state = State(None)
    print("Initial State:")
    print(initial_state)

    # Create an agent with the minimax mode
    agent = Agent(state=initial_state, modes=["minimax"], name="TestAgent")
    print("\nAgent Details:")
    print(agent)

    # Test the minimax method by making a move
    print("\nTesting Minimax Move:")
    next_state = agent.move(initial_state, "minimax")
    print("Next State:")
    print(next_state)

    # Validate the evaluation function
    print("\nEvaluation of Initial State:")
    evaluation = agent.minimax(initial_state, depth=3, is_maximizing=True)
    print(f"Evaluation Score: {evaluation}")

if __name__ == "__main__":
    tester()