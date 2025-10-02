import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE - 4, TILE_SIZE - 4))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * TILE_SIZE + 2, y * TILE_SIZE + 2)
        self.speedx = 0
        self.speedy = 0
        self.score = 0

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -PLAYER_SPEED
        if keystate[pygame.K_RIGHT]:
            self.speedx = PLAYER_SPEED
        if keystate[pygame.K_UP]:
            self.speedy = -PLAYER_SPEED
        if keystate[pygame.K_DOWN]:
            self.speedy = PLAYER_SPEED

        self.rect.x += self.speedx
        self.check_wall_collision('x')

        self.rect.y += self.speedy
        self.check_wall_collision('y')

    def check_wall_collision(self, direction):
        if direction == 'x':
            current_col = self.rect.centerx // TILE_SIZE
            current_row = self.rect.centery // TILE_SIZE

            if self.speedx > 0: # Moving right
                if maze[current_row][current_col + 1] == 1:
                    self.rect.right = (current_col + 1) * TILE_SIZE
            if self.speedx < 0: # Moving left
                if maze[current_row][current_col - 1] == 1:
                    self.rect.left = current_col * TILE_SIZE

        if direction == 'y':
            current_col = self.rect.centerx // TILE_SIZE
            current_row = self.rect.centery // TILE_SIZE

            if self.speedy > 0: # Moving down
                if maze[current_row + 1][current_col] == 1:
                    self.rect.bottom = (current_row + 1) * TILE_SIZE
            if self.speedy < 0: # Moving up
                 if maze[current_row - 1][current_col] == 1:
                    self.rect.top = current_row * TILE_SIZE
