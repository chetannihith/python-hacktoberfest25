import pygame
from settings import *
from player import Player
from ghost import Ghost

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pac-Man")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = pygame.font.match_font(FONT_NAME)
        self.walls = []
        self.pellets = pygame.sprite.Group()

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.ghosts = pygame.sprite.Group()
        self.pellets.empty() 

        self.player = Player(1, 1) 
        self.all_sprites.add(self.player)

        self.ghost1 = Ghost(12, 1, RED)
        self.ghost2 = Ghost(7, 5, PINK)
        self.ghost3 = Ghost(1, 7, CYAN)
        self.all_sprites.add(self.ghost1, self.ghost2, self.ghost3)
        self.ghosts.add(self.ghost1, self.ghost2, self.ghost3)

        self.draw_maze_and_pellets()
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()

        pellet_hit = pygame.sprite.spritecollide(self.player, self.pellets, True)
        if pellet_hit:
            self.player.score += 10

        ghost_hit = pygame.sprite.spritecollide(self.player, self.ghosts, False)
        if ghost_hit:
            self.playing = False
            self.running = False


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw_maze_and_pellets(self):
        for row_index, row in enumerate(maze):
            for col_index, tile in enumerate(row):
                if tile == 1:
                    pygame.draw.rect(self.screen, BLUE, (col_index * TILE_SIZE, row_index * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                elif tile == 2:
                    pellet = pygame.sprite.Sprite()
                    pellet.image = pygame.Surface((TILE_SIZE // 4, TILE_SIZE // 4))
                    pellet.image.fill(WHITE)
                    pellet.rect = pellet.image.get_rect()
                    pellet.rect.center = (col_index * TILE_SIZE + TILE_SIZE // 2, row_index * TILE_SIZE + TILE_SIZE // 2)
                    self.all_sprites.add(pellet)
                    self.pellets.add(pellet)

    def draw_walls(self):
         for row_index, row in enumerate(maze):
            for col_index, tile in enumerate(row):
                if tile == 1:
                    pygame.draw.rect(self.screen, BLUE, (col_index * TILE_SIZE, row_index * TILE_SIZE, TILE_SIZE, TILE_SIZE))


    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_walls()
        self.all_sprites.draw(self.screen)
        self.draw_text(f"Score: {self.player.score}", FONT_SIZE, WHITE, WIDTH / 2, 10)
        pygame.display.flip()

    def show_start_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("Pac-Man", 48, YELLOW, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Arrow keys to move", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press any key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pygame.display.flip()
        self.wait_for_key()


    def show_go_screen(self):
        if not self.running:
            return
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", 48, RED, WIDTH / 2, HEIGHT / 4)
        self.draw_text(f"Score: {self.player.score}", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press any key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pygame.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pygame.quit()