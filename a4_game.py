"""
Authors: [Your group ID + student IDs]
"""

import pygame
import sys

from a1_state import State
from a3_agent import Agent


# Constants for GUI
CELL_SIZE = 90
MARGIN = 8
BACKGROUND = (30, 30, 30)
ACTIVE_COLOR = (70, 130, 180)
HINGER_COLOR = (225, 180, 50)
EMPTY_COLOR = (50, 50, 50)
TEXT_COLOR = (220, 220, 220)

def play(state, agentA, agentB):
    """
    Simulates the entire Hinger game session between 2 players (AI or humans)
    Parameters:
        state (State): The starting game state (grid of counters).
        agentA : Player A (None = human).
        agentB : Player B (None = human).
    Returns:
        The name of the winner, or None if draw
    """

    # Setup screen dimensions and title
    pygame.init()
    width, height = 800,600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Hinger Game")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    
    current_agent = agentA  # agentA starts
    other_agent = agentB
    turn = 0
    winner = None
    background = (30,30,30)
    running = True

    print("Starting Hinger game!")

    while running:
        screen.fill(background)
        draw_board(screen, state, font)
        draw_text(screen, f"Turn: {turn+1}", 20, height - 60, font)
        draw_text(screen, f"Turn {turn + 1}: {current_agent.name if current_agent else 'Human'}'s turn", 20, 20, font)
        
        #define move before event loop
        move = None

        # check if any counters are left
        active_cells = [(i, j) for i in range(len(state.grid))
                        for j in range(len(state.grid[0]))
                        if state.grid[i][j] > 0]
        if not active_cells:
            winner = None
            print("No counters left - draw")
            break

        # Ask current player for move
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if current_agent is None and event.type == pygame.MOUSEBUTTONDOWN:
                # Human player input
                x, y = event.pos
                i = y // (height // len(state.grid))
                j = x // (width // len(state.grid[0]))
                if 0 <= i < len(state.grid) and 0 <= j < len(state.grid[0]):
                    move = (i, j)
                    break
        if current_agent is not None:
                pygame.time.delay(500)  # Small delay for better UX
                move = current_agent.move(state, mode="minimax")
            
        
        if not move:
            clock.tick(30)
            continue
        i, j = move
            
                # Validate the move
        if i < 0 or i >= len(state.grid) or j < 0 or j >= len(state.grid[0]):
                    print("Invalid move")
                    winner = other_agent.name if other_agent else "Human"
                    running = False
                    break

        if state.grid[i][j] == 0:
                    print("Invalid move — cell contains no current counters")
                    winner = other_agent.name if other_agent else "Human"
                    running = False
                    break
        
        #check if move is on a hinger cell and perform the move
        before_regions = state.numRegions()

        state.grid[i][j] -= 1

        after_regions = state.numRegions()
       

        if after_regions > before_regions:
            print(f"{current_agent.name if current_agent else 'Human'} found the hinger and wins...")
            winner = current_agent.name if current_agent else "Human"
            break

        # switch players
        current_agent, other_agent = other_agent, current_agent
        turn += 1
        clock.tick(30)


        # End of game display
    end_screen(screen, winner)
    pygame.quit()
    sys.exit()

def draw_board(screen, state, font):
    """
    Draws the current game state to the screen.
    """
    for i in range(len(state.grid)):
         for j in range(len(state.grid[0])):
            value = state.grid[i][j]
            x = MARGIN + j * (CELL_SIZE + MARGIN)
            y = MARGIN + i * (CELL_SIZE + MARGIN)
            color = EMPTY_COLOR if value == 0 else ACTIVE_COLOR
            
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE), border_radius=8)
            if value > 0:
                text = font.render(str(value), True, TEXT_COLOR)
                text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                screen.blit(text, text_rect)
    
def draw_text(screen, text, x, y, font):
    """
    Draws text on the screen at specified coordinates.
    """
    rendered_text = font.render(text, True, TEXT_COLOR)
    screen.blit(rendered_text, (x, y))

def end_screen(screen, winner, font):
    """
    Displays the winner at the end of the game.
    """
    screen.fill(BACKGROUND)
    if winner:
         msg = f"{winner} wins..."
    else:
         msg = "It's a draw..."
    text = font.render(msg, True, (200, 200, 200))
    screen.blit(text, (100, 250))
    pygame.display.flip()
    pygame.time.wait(3000)



def main():
    """
    Run Hinger Game
    """

    grid = [
        [2, 1, 0, 1, 0],
        [1, 2, 1, 1, 1],
        [0, 0, 0, 1, 1],
        [1, 1, 1, 0, 0]
    ]
    state = State(grid)

    # You can set either agent to None for human play
    agentA = None
    agentB = Agent(size=(4, 5), name="Agent B")

  
    # Start the game session
    play(state, agentA, agentB)
    


if __name__ == "__main__":
    main()