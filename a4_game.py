import pygame
import sys

class Game:
    def __init__(self, width=800, height=600, title="Hinger Game"):
        # Initialize Pygame
        pygame.init()

        # Set up window properties
        self.width = width
        self.height = height
        self.title = title
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)

        # Clock for frame rate control
        self.clock = pygame.time.Clock()
        self.FPS = 60

        # Game state variables
        self.running = True

        # Example attributes (you can expand)
        self.bg_color = (30, 30, 30)  # dark grey background

    def handle_events(self):
        """Handle all events such as keyboard and mouse input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        """Update game logic."""
        # Example: could move objects, check collisions, etc.
        pass

    def draw(self):
        """Draw everything to the screen."""
        self.screen.fill(self.bg_color)

        pygame.display.flip()  # Update the display

    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.FPS)  # Limit to 60 FPS

        self.quit()

    def quit(self):
        """Clean up and close the game."""
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game(800, 600, "Hinger Game")
    game.run()
