# space_invaders.py
import pygame
import random
import math
from collections import deque

# ---------- Config ----------
WIDTH, HEIGHT = 900, 700
FPS = 60
PLAYER_SPEED = 420       # px/sec
BULLET_SPEED = 700
ENEMY_BASE_SPEED = 40   # px/sec
WAVE_GAP = 1.2          # seconds between enemy spawn rows
BOSS_EVERY = 5          # boss every N waves
POWERUP_DURATION = 8.0  # seconds
# ----------------------------

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders - Advanced (Pygame)")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)
big_font = pygame.font.SysFont("Arial", 40)

# Colors
WHITE = (255, 255, 255)
GREY  = (180, 180, 180)
BLACK = (0, 0, 0)
RED   = (220, 60, 60)
GREEN = (60, 200, 80)
YELLOW= (240, 220, 60)
BLUE  = (70, 130, 240)
PURPLE= (170, 80, 200)

# ---------- Utility ----------
def draw_text(surf, text, size, x, y, color=WHITE):
    f = pygame.font.SysFont("Arial", size)
    r = f.render(text, True, color)
    surf.blit(r, (x, y))

# ---------- Sprites ----------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.w, self.h = 54, 28
        self.surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        pygame.draw.polygon(self.surf, BLUE, [(0,self.h),(self.w/2,0),(self.w,self.h)])
        self.rect = self.surf.get_rect(midbottom=(WIDTH//2, HEIGHT - 24))
        self.speed = PLAYER_SPEED
        self.shoot_cooldown = 0.22
        self.shoot_timer = 0.0
        self.lives = 3
        self.invulnerable = 0.0
        self.shield = False
        self.powerups = {}  # name: expiry_time
        self.score = 0

    def update(self, dt, keys):
        move = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            move -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            move += 1
        self.rect.x += move * self.speed * dt
        self.rect.x = max(6, min(WIDTH - self.rect.width - 6, self.rect.x))

        self.shoot_timer = max(0, self.shoot_timer - dt)
        if self.invulnerable > 0:
            self.invulnerable -= dt

        now = pygame.time.get_ticks() / 1000.0
        expired = [p for p,e in self.powerups.items() if e <= now]
        for p in expired:
            del self.powerups[p]
        self.shield = 'shield' in self.powerups

    def can_shoot(self):
        return self.shoot_timer <= 0

    def shoot(self, bullets_group):
        now = pygame.time.get_ticks() / 1000.0
        rapid = 'rapid' in self.powerups
        spread = 'spread' in self.powerups

        if not self.can_shoot():
            return
        self.shoot_timer = 0.08 if rapid else self.shoot_cooldown

        if spread:
            angles = [-12, 0, 12]
            for a in angles:
                bullets_group.add(Bullet(self.rect.centerx, self.rect.top-8, a, is_player=True))
        else:
            bullets_group.add(Bullet(self.rect.centerx, self.rect.top-8, 0, is_player=True))

    def hit(self):
        if self.invulnerable > 0:
            return False
        if self.shield:
            if 'shield' in self.powerups:
                del self.powerups['shield']
                self.shield = False
                self.invulnerable = 0.5
                return False
        self.lives -= 1
        self.invulnerable = 1.0
        return True


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle_deg, is_player=True):
        super().__init__()
        self.is_player = is_player
        self.surf = pygame.Surface((4, 12), pygame.SRCALPHA)
        color = YELLOW if is_player else RED
        pygame.draw.rect(self.surf, color, (0,0,4,12))
        self.rect = self.surf.get_rect(center=(x,y))
        self.angle = math.radians(angle_deg)
        direction = -1 if is_player else 1
        self.vx = math.sin(self.angle) * BULLET_SPEED * (1 if is_player else 0.7)
        self.vy = math.cos(self.angle) * BULLET_SPEED * direction

    def update(self, dt):
        self.rect.x += int(self.vx * dt)
        self.rect.y += int(self.vy * dt)
        if self.rect.bottom < -10 or self.rect.top > HEIGHT + 10 or self.rect.right < -40 or self.rect.left > WIDTH + 40:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    COLORS = [(200,80,80),(80,200,120),(200,180,60)]
    def __init__(self, x, y, row, speed=ENEMY_BASE_SPEED):
        super().__init__()
        self.size = 36
        self.surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.rect(self.surf, Enemy.COLORS[row % len(Enemy.COLORS)], (0,0,self.size,self.size), border_radius=6)
        pygame.draw.rect(self.surf, BLACK, (6,8, self.size-12,8))
        self.rect = self.surf.get_rect(topleft=(x,y))
        self.row = row
        self.speed = speed
        self.direction = 1
        self.hp = 1

    def update(self, dt, sway):
        dx, dy = sway
        self.rect.x += int(dx * dt)
        self.rect.y += int(dy * dt)


class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, hp):
        super().__init__()
        self.w = 220
        self.h = 90
        self.surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        self.rect = self.surf.get_rect(center=(x,y))
        self.max_hp = hp
        self.hp = hp
        self.phase = 1
        self.attack_timer = 0.0
        self.vx = 80
        self.dir = 1

    def update(self, dt):
        self.rect.x += int(self.dir * self.vx * dt)
        if self.rect.left < 30:
            self.rect.left = 30
            self.dir *= -1
        if self.rect.right > WIDTH - 30:
            self.rect.right = WIDTH - 30
            self.dir *= -1
        ratio = self.hp / max(1, self.max_hp)
        self.phase = 1 if ratio > 0.66 else (2 if ratio > 0.33 else 3)

    def draw(self, surface):
        surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        pygame.draw.rect(surf, PURPLE, (0, 0, self.w, self.h), border_radius=14)
        for i in range(3):
            pygame.draw.circle(surf, (30,30,30), (40 + i*60, 34), 12)
        surface.blit(surf, self.rect.topleft)
        hp_w = int((self.hp / self.max_hp) * (self.w - 10))
        pygame.draw.rect(surface, (80,80,80), (self.rect.left+5, self.rect.top-12, self.w-10, 8))
        pygame.draw.rect(surface, (200,40,40), (self.rect.left+5, self.rect.top-12, hp_w, 8))


class PowerUp(pygame.sprite.Sprite):
    TYPES = ['shield','rapid','spread']
    ICON = {'shield': GREEN, 'rapid': YELLOW, 'spread': PURPLE}
    def __init__(self, x, y, kind=None):
        super().__init__()
        self.kind = kind or random.choice(self.TYPES)
        self.surf = pygame.Surface((26,26), pygame.SRCALPHA)
        pygame.draw.circle(self.surf, PowerUp.ICON[self.kind], (13,13), 12)
        self.rect = self.surf.get_rect(center=(x,y))
        self.vy = 80

    def update(self, dt):
        self.rect.y += int(self.vy * dt)
        if self.rect.top > HEIGHT + 10:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, color=YELLOW):
        super().__init__()
        self.particles = []
        self.timer = 0.5
        self.x, self.y = x, y
        self.color = color
        for _ in range(12):
            angle = random.random()*math.pi*2
            speed = random.uniform(60,220)
            life = random.uniform(0.3,0.7)
            self.particles.append([x,y,math.cos(angle)*speed,math.sin(angle)*speed,life])

    def update(self, dt):
        self.timer -= dt
        for p in self.particles:
            p[0] += p[2] * dt
            p[1] += p[3] * dt
            p[4] -= dt
        if self.timer <= 0:
            self.kill()

    def draw(self, surf):
        for p in self.particles:
            if p[4] > 0:
                alpha = int(max(0, p[4])*255)
                s = pygame.Surface((6,6), pygame.SRCALPHA)
                s.fill((*self.color, alpha))
                surf.blit(s, (p[0]-3,p[1]-3))


# ---------- Wave Manager ----------
class WaveManager:
    def __init__(self):
        self.wave = 0
        self.enemies_group = pygame.sprite.Group()
        self.enemy_spawn_queue = deque()
        self.sway_dir = 1
        self.sway_dy = 10
        self.enemy_speed = ENEMY_BASE_SPEED

    def start_next_wave(self):
        self.wave += 1
        self.enemies_group.empty()
        self.enemy_spawn_queue.clear()
        self.enemy_speed = ENEMY_BASE_SPEED + (self.wave - 1) * 6
        if self.wave % BOSS_EVERY == 0:
            return 'boss'
        rows = min(5, 2 + self.wave // 2)
        cols = min(12, 6 + self.wave)
        margin_x, margin_y = 60, 80
        spacing_x = (WIDTH - 2*margin_x) // cols
        for r in range(rows):
            y = margin_y + r * 56
            for c in range(cols):
                x = margin_x + c * spacing_x + random.randint(-6,6)
                e = Enemy(x, y, r, speed=self.enemy_speed)
                e.hp = 1 + (r // 2)
                self.enemies_group.add(e)
        return 'normal'

    def update(self, dt):
        if self.enemies_group:
            left = min(e.rect.left for e in self.enemies_group)
            right = max(e.rect.right for e in self.enemies_group)
            move_dx = self.enemy_speed * self.sway_dir * 0.6
            move_dy = 0
            if left < 20 and self.sway_dir < 0:
                self.sway_dir *= -1
                move_dx = 0
                move_dy = self.sway_dy * 4
            if right > WIDTH-20 and self.sway_dir > 0:
                self.sway_dir *= -1
                move_dx = 0
                move_dy = self.sway_dy * 4
            for e in list(self.enemies_group):
                e.update(dt, (move_dx, move_dy))


# ---------- Game ----------
class Game:
    def __init__(self):
        self.player = Player()
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.wave_manager = WaveManager()
        self.boss = None
        self.boss_group = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.running = True
        self.paused = False
        self.state = 'playing'
        self.wave_manager.start_next_wave()

    def update(self, dt, keys):
        if self.paused or not self.running:
            return

        self.player.update(dt, keys)
        if keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]:
            self.player.shoot(self.bullets)

        self.bullets.update(dt)
        self.enemy_bullets.update(dt)
        self.powerups.update(dt)
        self.explosions.update(dt)

        if self.state == 'playing':
            self.wave_manager.update(dt)

            for e in list(self.wave_manager.enemies_group):
                shoot_chance = 0.0009 + self.wave_manager.wave * 0.0007 + (e.row * 0.0004)
                if random.random() < shoot_chance * (60 * dt):
                    self.enemy_bullets.add(Bullet(e.rect.centerx, e.rect.bottom + 6, 0, is_player=False))


# ---------- Main Loop ----------
def main():
    game = Game()
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)
        game.update(dt, keys)

        game.player_group.draw(screen)
        game.wave_manager.enemies_group.draw(screen)
        game.bullets.draw(screen)
        game.enemy_bullets.draw(screen)
        game.powerups.draw(screen)
        game.explosions.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
