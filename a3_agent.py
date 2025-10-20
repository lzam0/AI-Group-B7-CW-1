from a1_state import State
import time
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

                # Update best move if curr move is greater
                if move_value > best_value:
                    best_value = move_value
                    best_move = child

            # Return best move found
            return best_move
        
        # Alpha-Beta Pruning Mode
        if mode == "alpha_beta":
            # Initilize varbiables to track the best move and its value
            best_move = None

            # Start with the lowest possible value
            best_value = float('-inf')

            # Iterate through all possible moves from the current sttate
            for child in state.moves():
                # Evaluate the move using the Alpha-Beta Pruning algorithm with a depth limit of 3
                move_value = self.alphabeta(child, depth=3, alpha=float('-inf'), beta=float('inf'), is_maximizing=False)

                # Update best move if curr move is greater
                if move_value > best_value:
                    best_value = move_value
                    best_move = child

            # Return best move found
            return best_move
    
    def minimax(self, state, depth, is_maximizing):
        """
            Minimax recusive algorithm
            consider all possible moves up to a certain depth
            Utilising the Game Tree to evaluate the best move
        """
        if depth == 0 or not list(state.moves()):  # Terminal state or max depth
            return state.numHingers() - state.numRegions()  # Example evaluation function

        # Turn of Maximizing player
        if is_maximizing:
            max_eval = float('-inf')

            # Iterate through all children states
            for child in state.moves():
                # recusive call to minimax
                eval = self.minimax(child, depth - 1, False)

                # update the maximum evaluation
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            # Turn of Minimising Player
            min_eval = float('inf')

            # Iterate through all children states
            for child in state.moves():
                # Recurisve call to minimax
                eval = self.minimax(child, depth - 1, True)
                # Update the minimum evaluation
                min_eval = min(min_eval, eval)
            return min_eval
        
    def alphabeta(self, state, depth, alpha, beta, is_maximizing):
        """
            Alpha-Beta Pruning algorithm
            An optimized version of Minimax that eliminates branches in the game tree that won't be selected
        """
        if depth == 0 or not list(state.moves()):  # Terminal state or max depth
            return state.numHingers() - state.numRegions()  # Example evaluation function

        # Turn of Maximizing player
        if is_maximizing:
            max_eval = float('-inf')

            # Iterate through all children states
            for child in state.moves():
                # recusive call to minimax
                eval = self.alphabeta(child, depth - 1, alpha, beta, False)

                # update the maximum evaluation
                max_eval = max(max_eval, eval)

                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta cut-off
            return max_eval
        else:
            # Turn of Minimising Player
            min_eval = float('inf')

            # Iterate through all children states
            for child in state.moves():
                # Recurisve call to minimax
                eval = self.alphabeta(child, depth - 1,alpha, beta, True)
                # Update the minimum evaluation
                min_eval = min(min_eval, eval)

                beta = min(beta, eval)
            return min_eval

def time_strategy(agent, state, mode):
    start_time = time.time()
    next_state = agent.move(state, mode)
    end_time = time.time()
    elapsed = end_time - start_time
    return next_state, elapsed

def tester():

    """
        This method is to demonstrate and validate 
        the agent’s behavior across scenarios.
    """

    print("Testing Agent class...")

    # Create a random initial state
    state1 = State(None)
    print("Initial State:")
    print(state1)

    # Create an agent with the modes implemented
    agent = Agent(state=state1, modes=["minimax", "alpha_beta"], name="TestAgent")
    print("\nAgent Details:")
    print(agent)

    # ------------------------------------------------------------------------------

    # Scenario 2: Compare move outcome and time between modes
    print("\n--- Scenario: Performance Comparison | Move Outcome & Time Taken ---")

    # Utilise time_strategy function
    next_state_minimax, t_minimax = time_strategy(agent, state1, "minimax")
    next_state_alpha, t_alpha = time_strategy(agent, state1, "alpha_beta")

    print("Minimax Move:\n", next_state_minimax)
    print(f"⏱️ Minimax took {t_minimax:.4f}s")

    print("\nAlpha-Beta Move:\n", next_state_alpha)
    print(f"⏱️ Alpha-Beta took {t_alpha:.4f}s")

    # Check if they produced the same result (optional)
    if str(next_state_minimax) == str(next_state_alpha):
        print("-> Both strategies chose the same move.")
    else:
        print("-> Strategies produced different moves.")

    # ------------------------------------------------------------------------------


if __name__ == "__main__":
    tester()