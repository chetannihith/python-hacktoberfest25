import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# --- Game Constants ---
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Plafy Bird")

# Colors
BACKGROUND_COLOR = (135, 206, 235)  # Sky Blue
BIRD_COLOR = (255, 255, 0)         # Yellow
PIPE_COLOR = (0, 150, 0)           # Dark Green
TEXT_COLOR = (0, 0, 0)             # Black

# Game physics
GRAVITY = 0.8
FLAP_STRENGTH = -10
PIPE_SPEED = 4
PIPE_GAP = 175
PIPE_SPAWN_FREQUENCY = 1500  # milliseconds

# Font setup
FONT = pygame.font.Font(None, 60)
SMALL_FONT = pygame.font.Font(None, 40)

# --- Bird Class ---
class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 30
        self.velocity = 0
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def jump(self):
        # Only allow jumping if the bird is not too high
        if self.y > 0:
            self.velocity = FLAP_STRENGTH

    def move(self):
        # Apply gravity to velocity
        self.velocity += GRAVITY
        
        # Limit max downward velocity
        if self.velocity > 15:
            self.velocity = 15
            
        # Apply velocity to y position
        self.y += self.velocity
        self.rect.y = int(self.y)

    def draw(self):
        # Draw the yellow bird (represented as a rectangle)
        pygame.draw.rect(SCREEN, BIRD_COLOR, self.rect, border_radius=8)
        # Simple eye/beak detail
        pygame.draw.circle(SCREEN, TEXT_COLOR, (self.x + self.size - 8, self.y + 8), 4)
        pygame.draw.polygon(SCREEN, (255, 140, 0), [
            (self.x + self.size, self.y + 10),
            (self.x + self.size + 10, self.y + 15),
            (self.x + self.size, self.y + 20)
        ])

    def get_rect(self):
        return self.rect

# --- Pipe Class ---
class Pipe:
    def __init__(self, x, screen_height):
        self.x = x
        self.passed = False  # Track if the bird has passed this pipe for scoring
        self.pipe_width = 70
        
        # Randomly determine the height of the gap
        min_pipe_height = 80
        max_pipe_height = screen_height - PIPE_GAP - min_pipe_height
        
        # Height of the top pipe (randomized)
        self.top_height = random.randint(min_pipe_height, max_pipe_height)
        
        # Height and y-position of the bottom pipe
        self.bottom_height = screen_height - self.top_height - PIPE_GAP
        self.bottom_y = self.top_height + PIPE_GAP

        # Rectangles for collision detection and drawing
        self.top_rect = pygame.Rect(self.x, 0, self.pipe_width, self.top_height)
        self.bottom_rect = pygame.Rect(self.x, self.bottom_y, self.pipe_width, self.bottom_height)

    def move(self):
        self.x -= PIPE_SPEED
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self):
        # Draw the top pipe
        pygame.draw.rect(SCREEN, PIPE_COLOR, self.top_rect, border_radius=8)
        # Draw the bottom pipe
        pygame.draw.rect(SCREEN, PIPE_COLOR, self.bottom_rect, border_radius=8)

    def collide(self, bird_rect):
        # Check for collision between the bird and either pipe
        return bird_rect.colliderect(self.top_rect) or bird_rect.colliderect(self.bottom_rect)

    def get_x(self):
        return self.x

# --- Game Functions ---

def draw_score(score):
    score_surface = FONT.render(str(score), True, TEXT_COLOR)
    SCREEN.blit(score_surface, (SCREEN_WIDTH // 2 - score_surface.get_width() // 2, 50))

def game_over_screen(score):
    # Overlay the game screen with a transparent layer
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(180) 
    overlay.fill((255, 255, 255))
    SCREEN.blit(overlay, (0, 0))

    title_text = FONT.render("GAME OVER", True, (255, 0, 0))
    score_text = SMALL_FONT.render(f"Final Score: {score}", True, TEXT_COLOR)
    restart_text = SMALL_FONT.render("Press SPACE or Click to Restart", True, TEXT_COLOR)

    SCREEN.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 3))
    SCREEN.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 3 + 70))
    SCREEN.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 3 + 140))
    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting_for_input = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting_for_input = False
        pygame.time.Clock().tick(30)
    
    # Restart the main game loop
    main_game()


def main_game():
    # --- Game State Variables ---
    bird = Bird(50, SCREEN_HEIGHT // 2)
    pipes = []
    score = 0
    game_active = True
    
    # Timer for pipe generation
    pipe_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(pipe_timer, PIPE_SPAWN_FREQUENCY)

    clock = pygame.time.Clock()

    # --- Main Game Loop ---
    running = True
    while running:
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if game_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bird.jump()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    bird.jump()

                if event.type == pipe_timer:
                    pipes.append(Pipe(SCREEN_WIDTH, SCREEN_HEIGHT))
            else:
                # If game is not active (Game Over), clicking or spacebar triggers restart
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or event.type == pygame.MOUSEBUTTONDOWN:
                    game_over_screen(score)
                    return # Exit the function after calling game_over_screen

        # --- Game Logic (Only runs if game is active) ---
        if game_active:
            bird.move()

            # Move and clean up pipes
            for pipe in pipes:
                pipe.move()
                
                # Check for collision
                if pipe.collide(bird.get_rect()):
                    game_active = False

                # Check if pipe has been passed for scoring
                if pipe.get_x() + pipe.pipe_width < bird.x and not pipe.passed:
                    score += 1
                    pipe.passed = True
            
            # Remove pipes that have moved off screen
            pipes = [pipe for pipe in pipes if pipe.get_x() + pipe.pipe_width > 0]

            # Check for ground or ceiling collision
            if bird.y > SCREEN_HEIGHT or bird.y < -bird.size:
                game_active = False

        # --- Drawing ---
        SCREEN.fill(BACKGROUND_COLOR)
        
        # Draw all pipes
        for pipe in pipes:
            pipe.draw()

        # Draw the bird
        bird.draw()

        # Draw the score
        draw_score(score)

        # Draw the ground (simple brown rectangle)
        pygame.draw.rect(SCREEN, (160, 82, 45), (0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20))


        # Update the display
        pygame.display.flip()
        
        # Cap the framerate
        clock.tick(60)

    # --- Exit Game ---
    pygame.quit()
    sys.exit()

# Start the game
if __name__ == "__main__":
    main_game()
