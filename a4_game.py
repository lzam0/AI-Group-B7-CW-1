import pygame
import sys

from a1_state import State
from a3_agent import Agent

def play(state, agentA, agentB):
    """
    Simulates the entire Hinger game session between 2 plasyers (agents or humans)
    """

    # Setup screen dimensions and title
    pygame.init()
    width, height = 800,600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Hinger Game")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    running = True
    current_agent = "A"  # agentA starts
    winner = None
    background = (30,30,30)

    while running:
        screen.fill(background)

        # --- Handle events (for human input or exit) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # --- Render state on screen ---
        draw_board(screen, state, font)
        pygame.display.flip()
        clock.tick(30)

        # --- End of game display ---
    end_screen(screen, winner)
    pygame.quit()
    sys.exit()

def draw_board(screen, state, font):
    """
    Draws the current game state to the screen.
    """
    text = font.render("Screen", True, (200, 200, 200))
    screen.blit(text, (50, 50))

def end_screen(screen, winner):
    """
    Displays the winner at the end of the game.
    """
    pass



def main():
    """
    Run Hinger Game
    """
    initial_state = State(None)
    
    # Example: human vs human
    agentA = None
    agentB = None

    # Start the game session
    play(initial_state, agentA, agentB)


if __name__ == "__main__":
    main()