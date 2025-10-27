"""
a3_agent.py

Author: Leihl Zambrano
Student ID: 100385659
Creation Date: 29th September 2025
Last Modified: 27th October 2025

Description:
    This module defines the Agent class used for decision-making in the Hingers game.
    The Agent supports multiple strategies including:
        - Minimax
        - Alpha-Beta Pruning
        - Monte Carlo Tree Search (MCTS)
        - Hybrid (combination of Alpha-Beta and Monte Carlo)

    The Agent interacts with a State object (from a1_state.py), generating moves and
    evaluating board states based on active regions and hingers.

Classes:
    Agent: Implements the game-playing agent with evaluation, move selection, and search strategies.

Functions:
    time_strategy(agent, state, mode): Measures execution time of a move by the agent.
    test_all_strategies(): Demonstrates all strategies and compares their performance.
    tester(): Continuously plays moves until a new active region is created.

"""

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

        if mode.lower() == "monte_carlo":
            best_move = self.monte_carlo(state, simulations=20)
            # If the best move creates a new region, return it immediately
            if best_move.numRegions() < state.numRegions():
                return state

            return best_move
        
        # For minimax and alpha-beta pruning strategies
        best_move = None
        best_value = float('-inf')

        # Get all possible moves
        possible_moves = list(state.moves())
        if not possible_moves:
            return state

        # Evaluate each possible move
        for child in self.ordered_moves(state, parent_state=state):
            
            # Minimax Strategy
            if mode.lower() == "minimax":
                value = self.minimax(child, depth=search_depth, is_maximizing=False, parent_state=state)

            # Alpha Beta Pruning Strategy
            elif mode.lower() == "alpha_beta":
                value = self.alphabeta(child, depth=search_depth, alpha=float('-inf'), beta=float('inf'),
                                    is_maximizing=False, parent_state=state)
                
            elif mode.lower() == "hybrid":
                value = self.hybrid(child, depth=search_depth, alpha=float('-inf'), beta=float('inf'),
                                               is_maximizing=False, parent_state=state, sims=10)
                
            else: # Ideally it will be the human player
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
        
        if parent_state:
            parent_regions = parent_state.numRegions()
        else:
            parent_regions = 0

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

                # Max Turn: recusive call to alphabeta pruning strategy
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

                 # Min Turn: recursive call to alphabeta pruning strategy
                eval = self.alphabeta(child, depth-1, alpha, beta, True, parent_state=state)

                # update the minimum evaluation
                min_eval = min(min_eval, eval)
                
                # Update beta value for pruning
                beta = min(beta, eval)

                # Cuts off the remaining branches when the outcome won't get affected
                if beta <= alpha:
                    break
            return min_eval

    def monte_carlo(self, state, simulations, max_depth=10):
        """
        Monte Carlo Tree Search (MCTS) algorithm
        Performs random simulations to evaluate the potential of moves.
        """
        # Get all possible moves
        possible_moves = list(state.moves())

        # if no possible moves, return current state
        if not possible_moves:
            return state
    
        move_scores = {}

        # Perform simulations for each move
        for move in possible_moves:
            total_score = 0
            for _ in range(simulations):
                # simulate a radnom playout from the move
                total_score += self.simulate_random_playout(move, max_depth)

            # Accumulate scores by obtaining the average
            move_scores[move] = total_score / simulations

        # Pick the move with the highest average score
        best_move = max(move_scores, key=move_scores.get)

        # Prevent Monte Carlo from picking a move that reduces active regions
        if best_move.numRegions() < state.numRegions():
            return state 
    
        return best_move
    
    def hybrid(self, state, depth, alpha, beta, is_maximizing, parent_state=None, sims=10):
        """
        A Hybrid between Monte Carlo and Alpha-Beta pruning strategies.
        Uses Alpha-Beta pruning for pruning and structure,
        but Monte Carlo simulations for evaluating leaf nodes
        """
        if depth == 0 or not list(state.moves()):
            total_score = 0
            for _ in range(sims):
                total_score += self.simulate_random_playout(state, max_depth=5)
            return total_score / sims

        ordered_children = self.ordered_moves(state, parent_state)

        # Maximizing Agent Turn
        if is_maximizing:
            max_eval = float('-inf')

            # Iterate through all ordered children states
            for child in ordered_children:

                # Max Turn: recusive call to alphabeta pruning strategy
                eval = self.hybrid(child, depth-1, alpha, beta, True, parent_state=state, sims=sims)

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

                 # Min Turn: recursive call to alphabeta pruning strategy
                eval = self.hybrid(child, depth-1, alpha, beta, True, parent_state=state, sims=sims)

                # update the minimum evaluation
                min_eval = min(min_eval, eval)
                
                # Update beta value for pruning
                beta = min(beta, eval)

                # Cuts off the remaining branches when the outcome won't get affected
                if beta <= alpha:
                    break
            return min_eval
        

    def simulate_random_playout(self, state, max_depth=10):
        """
        Simulates a random playout from the given state until the end or max depth.
        Returns a score based on the final state's evaluation.
        """
        current_state = state
        initial_regions = state.numRegions()

        # Play randomly until no moves left or depth reached
        for depth in range(max_depth):

            # Get all possible moves
            moves = list(current_state.moves())
            if not moves:
                break

            # Choose a random move
            next_state = random.choice(moves)

            # Stop immediately if a new region is found
            if next_state.numRegions() > state.numRegions():
                current_state = next_state
                break
        # Use your existing evaluation function
        return self.evaluate(current_state, parent_state=state)

def time_strategy(agent, state, mode):
    """Timing strategies move time"""
    # utilise time library time
    start_time = time.time()

    # agent move operation
    next_state = agent.move(state, mode)

    # end timer
    end_time = time.time()

    # calculate time taken
    elapsed = end_time - start_time
    return next_state, elapsed

def test_all_strategies():
    """Demonstrates all strategies implemented"""
    print("Demonstrating all strategies to compare to each other\n")

    start_board = State(None)
    print("Initial State:")
    print(start_board)
    initial_regions = start_board.numRegions()
    print(f"Initial number of regions: {initial_regions}\n")

    # Create an agent
    agent = Agent(state=start_board, modes=["minimax", "alpha_beta", "monte_carlo", "hybrid"], name="Strategy Testing")
    print(agent)

    strategies = ["minimax", "alpha_beta", "monte_carlo", "hybrid"]

    # Iterate through all strategies
    for mode in strategies:
        print(f"--- Testing {mode} ---")
        current_state = start_board
        move_count = 0

        # iterate through the board until loop broken
        while current_state.numRegions() <= initial_regions:
            next_state, elapsed = time_strategy(agent, current_state, mode)
            move_count += 1

            print(f"Move {move_count}: Regions: {next_state.numRegions()} | Time: {elapsed:.4f}s")

            # Stop if region count increased
            if next_state.numRegions() > initial_regions:
                print(f"SUCCESS: {mode} created a new region in {move_count} move(s)!\n")
                break

            # Stop if no further progress
            if str(next_state) == str(current_state):
                print(f"STOPPED: {mode} cannot make further progress.\n")
                break

            current_state = next_state

        # If none created new regions
        if current_state.numRegions() < initial_regions:
            print(f"FAILED: {mode} did not create a new region.\n")

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
    agent = Agent(state=state1, modes=["minimax", "alpha_beta", "monte_carlo", "hybrid"], name="")
    print(agent)

    mode = "hybrid"
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
        
        # update current board for next iteration
        current_state = next_state

    print(f"\nTotal moves made until a new region was created: {move_count}")

if __name__ == "__main__":
    test_all_strategies()
    # tester()