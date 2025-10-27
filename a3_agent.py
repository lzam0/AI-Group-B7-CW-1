from a1_state import State
import time
import random
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

    def move(self, state, mode, search_depth=3):
        """
            Have agent create 2 seperate active regions
            Methods used: Minimax and Alpha-Beta Pruning
        """

        # Get current number of regions
        current_regions = state.numRegions()
        best_move = None
        best_value = float('-inf')

        # Get all possible moves
        possible_moves = list(state.moves())
        if not possible_moves:
            return state

        # Evaluate each possible move
        for child in self.ordered_moves(state, parent_state=state):
            
            # Alpha Beta Pruning Strategy
            if mode.lower() == "alpha_beta":
                value = self.alphabeta(child, depth=search_depth, alpha=float('-inf'), beta=float('inf'),
                                    is_maximizing=False, parent_state=state)
            # Minimax Strategy
            if mode.lower() == "minimax":
                value = self.minimax(child, depth=search_depth, is_maximizing=False, parent_state=state)
            else:
                raise ValueError(f"Unknown mode '{mode}'")
            
            # If this move creates a new region, return it immediately
            if child.numRegions() > current_regions:
                return child
            
            # Update best move if curr move is better
            if value > best_value:
                best_value = value
                best_move = child
        return best_move

    # Order moves to prioritize those that increase regions and hingers
    def ordered_moves(self, state, parent_state=None):
        """Orders moves based on their evaluation scores."""
        moves = list(state.moves())
        return sorted(moves, key=lambda s: self.evaluate(s, parent_state), reverse=True)


    def evaluate(self, state, parent_state):
        """
        Evaluation function that rewards new region creation and penalizes hingers.
        """
        regions = state.numRegions()
        parent_regions = parent_state.numRegions() if parent_state else 0
        hingers = state.numHingers()

        # Reward *new* region creation more strongly
        region_diff = regions - parent_regions
        # Reward formula 
        reward = (15 * region_diff) - (0.5 * hingers)

        # Add a small random tie-breaker to diversify paths
        reward += random.uniform(-0.1, 0.1)
        return reward
    
    def minimax(self, state, depth, is_maximizing, parent_state=None):
        # Terminal state or max depth
        if depth == 0 or not list(state.moves()):
            # Utilise evaulation function
            return self.evaluate(state, parent_state)

        # Maximizing Agent Turn
        if is_maximizing:
            max_eval = float('-inf')

            # Iterate through all children states
            for child in state.moves():
                # recusive call to minimax
                eval = self.minimax(child, depth-1, False, parent_state=state)

                # update the maximum evaluation
                max_eval = max(max_eval, eval)
            return max_eval
        else: # Minimizing Agent Turn
            min_eval = float('inf')

            # Iterate through all children states
            for child in state.moves():
                # recursive call to minimax
                eval = self.minimax(child, depth-1, True, parent_state=state)

                # update the minimum evaluation
                min_eval = min(min_eval, eval)
            return min_eval

    def alphabeta(self, state, depth, alpha, beta, is_maximizing, parent_state=None):
        """
            Alpha–beta pruning’s goal is to avoid exploring parts of the 
            search tree that can’t affect the final decision.
        """
        # Terminal state or max depth
        if depth == 0 or not list(state.moves()):
            return self.evaluate(state, parent_state)

        # Move ordering improves alpha–beta efficiency 
        # by exploring strong moves first, causing
        # earlier pruning and fewer nodes to be evaluated.
        ordered_children = self.ordered_moves(state, parent_state)
        
        # Maximizing Agent Turn
        if is_maximizing:
            max_eval = float('-inf')

            # Iterate through all ordered children states
            for child in ordered_children:

                # recusive call to alphabeta pruning strategy
                eval = self.alphabeta(child, depth-1, alpha, beta, False, parent_state=state)

                # update the maximum evaluation
                max_eval = max(max_eval, eval)

                # Update alpha value for pruning
                alpha = max(alpha, eval)

                # Cuts off the remaining branches when the outcome won't get affected
                if beta <= alpha:
                    break
            return max_eval
        else: # Minimising Agent Turn
            min_eval = float('inf')

            # Iterate through all ordered children states
            for child in ordered_children:

                 # recusive call to alphabeta pruning strategy
                eval = self.alphabeta(child, depth-1, alpha, beta, True, parent_state=state)

                # update the minimum evaluation
                min_eval = min(min_eval, eval)
                
                # Update alpha value for pruning
                beta = min(beta, eval)

                # Cuts off the remaining branches when the outcome won't get affected
                if beta <= alpha:
                    break
            return min_eval

    def monte_carlo(self, state, simulations=100):
        """
        Monte Carlo Tree Search (MCTS) algorithm
        """
        pass

# Function for timing the agent's move
def time_strategy(agent, state, mode):
    start_time = time.time()
    next_state = agent.move(state, mode)
    end_time = time.time()
    elapsed = end_time - start_time
    return next_state, elapsed

def tester():
    """
    Demonstrates the Agent's behavior.
    Keeps making moves until a new active region is created.
    """
    print("Testing Agent class...")

    # Create a random initial state
    state1 = State(None)
    print("Initial State:")
    print(state1)
    initial_regions = state1.numRegions()
    print(f"Initial number of regions: {initial_regions}\n")

    # Create an agent
    agent = Agent(state=state1, modes=["minimax", "alpha_beta"], name="")
    print(agent)

    mode = "minimax"
    current_state = state1
    move_count = 0

    # Keep making moves until a new region is created
    while current_state.numRegions() <= initial_regions:
        next_state, elapsed = time_strategy(agent, current_state, mode)
        print(f"Evaluating move using {mode} strategy")
        move_count += 1

        print(f"\nMove {move_count}:")
        print(next_state)
        print(f"Regions: {next_state.numRegions()} | Time: {elapsed:.4f}s")

        # Stop if the move increases the number of regions
        if next_state.numRegions() > initial_regions:
            print("\n--- A new active region has been created! ---")
            break

        # Stop if no further progress is possible
        if str(next_state) == str(current_state):
            print("\n--- No further progress possible. Stopping. ---")
            break

        current_state = next_state

    print(f"\nTotal moves made until a new region was created: {move_count}")




if __name__ == "__main__":
    tester()