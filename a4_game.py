"""
Authors: [100464021]
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

#Constants for move history
move_history = []
MAX_LOGS = 2

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
        try:
            
            screen.fill(background)
            draw_board(screen, state, font)
            draw_text(screen, f"Turn: {turn+1}", 20, height - 60, font)
            draw_text(screen, f"Turn {turn + 1}: {current_agent.name if current_agent else 'Human'}'s turn", 10, 40, font)
            pygame.display.set_caption(f"Hinger Game - Turn {turn+1}")

            pygame.display.flip()
            
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
            move = None
        # --- Handle human player (if current_agent is None) ---
        
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if current_agent is None and event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = event.pos
                        grid_offset_y = 90  # offset for grid drawing
                        i = (y - grid_offset_y) // (CELL_SIZE + MARGIN)
                        j = x // (CELL_SIZE + MARGIN)

                        if i < 0 or i >= len(state.grid) or j < 0 or j >= len(state.grid[0]):
                            print("Click outside grid; try again.")
                            continue  # click outside grid

                        if 0 <= i < len(state.grid) and 0 <= j < len(state.grid[0]):
                            if state.grid[i][j] == 0:
                                print("Invalid move — cell contains no current counters")
                                continue  # just ignore invalid clicks
                            else:
                                before_regions = state.numRegions()
                                state.grid[i][j] -= 1
                                after_regions = state.numRegions()

                                if after_regions > before_regions:
                                    print("Human found the hinger and wins!")
                                    winner = "Human"
                                    running = False
                                else:
                                    move_history.append(f"Human moved at ({i}, {j})")
                                    if len(move_history) > MAX_LOGS:
                                        move_history.pop(0)
                                    current_agent, other_agent = other_agent, current_agent
                                    turn += 1
                        break

            # Handle AI player
            if current_agent is not None:
                    pygame.time.delay(500)
                    new_state = current_agent.move(state, mode=current_agent.mode)

                    if not isinstance(new_state, State):
                        print("AI returned invalid state; skipping turn.")
                        continue

                    before_regions = state.numRegions()
                    after_regions = new_state.numRegions()

                    if after_regions > before_regions:
                        print(f"{current_agent.name} found the hinger and wins...")
                        winner = current_agent.name
                        running = False
                    else:
                        state = new_state  #update to AI’s new board
                        move_history.append(f"{current_agent.name} moved.")
                        if len(move_history) > MAX_LOGS:
                            move_history.pop(0)
                        current_agent, other_agent = other_agent, current_agent
                        turn += 1
                        clock.tick(30)  # save CPU resources
                        

        except Exception as e:
            print(f"Error occurred: {e}")
            pygame.time.wait(2000)
        # End of game display
    end_screen(screen, winner, font)
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
            y = 90 + MARGIN + i * (CELL_SIZE + MARGIN)
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


def select_mode(agent):
    """
    Allows user to select the AI mode for the agent.
    """
    modes = ["minimax", "alpha_beta", "monte_carlo", "hybrid"]
    print("Select AI mode:")
    for i, mode in enumerate(modes):
        print(f"{i + 1}. {mode}")
    choice = int(input("Enter choice number: ")) - 1
    if 0 <= choice < len(modes):
        agent.mode = modes[choice]
        print(f"Selected mode: {agent.mode}")
    else:
        print("Invalid choice. Defaulting to minimax.")
        agent.mode = "minimax"


def select_mode_pygame(screen, font, agent):
    """
    Displays a simple mode selection screen using Pygame.
    """
    modes = ["minimax", "alpha_beta", "monte_carlo", "hybrid"]
    selected_mode = None
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((180, 180, 180))
        title = font.render("Select AI Mode:", True, (20, 20, 20))
        screen.blit(title, (100, 80))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        for i, mode in enumerate(modes):
            color = (240, 240, 240)
            rect = pygame.Rect(100, 150 + i * 70, 250, 50)

            # Highlight hover
            if rect.collidepoint(mouse_pos):
                color = (100, 180, 255)
                if mouse_click:
                    selected_mode = mode
                    agent.mode = mode
                    running = False

            pygame.draw.rect(screen, color, rect, border_radius=8)
            text = font.render(mode, True, (60, 60, 60))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)


            display_move_history(screen, font, move_history, start_x=600, start_y=150)

        pygame.display.flip()
        clock.tick(30)

    print(f"Selected mode: {selected_mode}")


def display_move_history(screen, font, move_history, start_x = 600, start_y = 100):
    """
    Displays the move history on the screen.
    """
    title = font.render("Move Log:", True, TEXT_COLOR)
    screen.blit(title, (start_x, start_y - 40))
    log_font = pygame.font.SysFont(None, 28)
    
    for i, log in enumerate(reversed(move_history)):
        text = log_font.render(log, True, TEXT_COLOR)
        screen.blit(text, (start_x, start_y + i * 30))

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
        [2, 1, 0, 2, 1],
        [1, 2, 4, 2, 1],
        [0, 0, 0, 4, 1],
        [1, 1, 1, 0, 0]
    ]

    # grid to test draw gameplay
    grid2 = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [1, 0, 1, 0, 0]
    ]

    state = State(grid)


    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.SysFont(None, 36)

    # You can set either agent to None for human play
    agentA = None
    agentB = Agent(state=state, modes=["minimax", "alpha_beta", "monte_carlo", "hybrid"], name="Agent B")

    select_mode_pygame(screen, font, agentB)
    #select_mode(agentB) commented out to avoid console input during pygame run. But can be used for non-pygame testing.

    pygame.event.clear()
    pygame.time.wait(300)

    # Start the game session
    play(state, agentA, agentB)
    


if __name__ == "__main__":
    main()