"""
a4_game.py
Core gameplay loop for the Hinger game.

Authors: [Your group ID + student IDs]
Module: CMP-6058A / 7058A Artificial Intelligence
Task 4: Implement the game loop between two agents or a human player.
"""

from a1_state import State
from a3_agent import Agent

def play(state, agentA, agentB):
    """
    Simulates a full Hinger game between two players.
    Parameters:
        state (State): The starting game state (grid of counters).
        agentA (Agent or None): Player A (None = human).
        agentB (Agent or None): Player B (None = human).
    Returns:
        str: The name of the winner, or None if draw.
    """

    current_agent = agentA
    other_agent = agentB
    turn = 0

    print("🎮 Starting Hinger game!")
    print("Initial state:")
    print(state)

    while True:
        print(f"\nTurn {turn + 1}: {current_agent.name if current_agent else 'Human'}'s turn")
        print(state)

        # --- Step 1: Check if any counters are left ---
        active_cells = [(i, j) for i in range(len(state.grid))
                        for j in range(len(state.grid[0]))
                        if state.grid[i][j] > 0]
        if not active_cells:
            print("No counters left — it's a draw!")
            return None

        # --- Step 2: Ask current player for move ---
        if current_agent is None:
            # Human player
            try:
                i = int(input("Enter row: "))
                j = int(input("Enter column: "))
                move = (i, j)
            except ValueError:
                print("Invalid input. Try again.")
                continue
        else:
            # Agent move
            move = current_agent.move(state, mode="minimax")

        i, j = move

        # --- Step 3: Validate the move ---
        if i < 0 or i >= len(state.grid) or j < 0 or j >= len(state.grid[0]):
            print("❌ Invalid move — out of bounds!")
            print(f"{other_agent.name if other_agent else 'Human'} wins!")
            return other_agent.name if other_agent else "Human"

        if state.grid[i][j] == 0:
            print("❌ Invalid move — cell already empty!")
            print(f"{other_agent.name if other_agent else 'Human'} wins!")
            return other_agent.name if other_agent else "Human"

        # --- Step 4: Check if move is on a hinger cell ---
        before_regions = state.numRegions()
        before_hingers = state.numHingers()

        # Perform the move: remove one counter
        state.grid[i][j] -= 1

        after_regions = state.numRegions()
        after_hingers = state.numHingers()

        # --- Step 5: Check if this move hits a hinger ---
        # A "hinger" move increases the number of active regions
        if after_regions > before_regions:
            print(f"🏆 {current_agent.name if current_agent else 'Human'} made a hinger move and wins!")
            print(state)
            return current_agent.name if current_agent else "Human"

        # --- Step 6: Switch players ---
        current_agent, other_agent = other_agent, current_agent
        turn += 1


def tester():
    """Simple test run for play() with two AI agents."""
    grid = [
        [2, 1, 0],
        [1, 2, 0],
        [0, 0, 0]
    ]
    state = State(grid)

    agentA = Agent(size=(3, 3), name="Agent A")
    agentB = Agent(size=(3, 3), name="Agent B")

    winner = play(state, agentA, agentB)
    print(f"\nGame Over! Winner: {winner}")


if __name__ == "__main__":
    tester()
