import pygame
import random
from settings import *

class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE - 4, TILE_SIZE - 4))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * TILE_SIZE + 2, y * TILE_SIZE + 2)
        self.direction = random.choice(['x', 'y'])
        self.speed = GHOST_SPEED if self.direction == 'x' else -GHOST_SPEED

    def update(self):
        if self.direction == 'x':
            self.rect.x += self.speed
        else:
            self.rect.y += self.speed

        self.check_wall_collision()

    def check_wall_collision(self):
        current_col = self.rect.centerx // TILE_SIZE
        current_row = self.rect.centery // TILE_SIZE

        try:
            if self.direction == 'x':
                if self.speed > 0 and (maze[current_row][current_col + 1] == 1 or maze[current_row][current_col] == 1):
                    self.rect.right = (current_col + 1) * TILE_SIZE
                    self.speed *= -1 
                elif self.speed < 0 and (maze[current_row][current_col - 1] == 1 or maze[current_row][current_col] == 1):
                    self.rect.left = current_col * TILE_SIZE
                    self.speed *= -1 
            else:
                 if self.speed > 0 and (maze[current_row + 1][current_col] == 1 or maze[current_row][current_col] == 1):
                    self.rect.bottom = (current_row + 1) * TILE_SIZE
                    self.speed *= -1 
                 elif self.speed < 0 and (maze[current_row - 1][current_col] == 1 or maze[current_row][current_col] == 1):
                    self.rect.top = current_row * TILE_SIZE
                    self.speed *= -1 
        except IndexError:
            self.speed *= -1
