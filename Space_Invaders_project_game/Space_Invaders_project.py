

import math
import random
import json
import os
import sys
from dataclasses import dataclass

try:
    import pygame
    from pygame import mixer
except Exception:
    print("Pygame is required. Install it with: pip install pygame")
    raise

# ------------------------- Configuration -------------------------
WIDTH, HEIGHT = 1024, 768
FPS = 60
TITLE = "Space Invaders - Advanced"
ASSETS_DIR = "assets"
HIGHSCORE_FILE = "si_highscore.json"

# Gameplay tuning
PLAYER_SPEED = 360.0  # pixels/sec
BULLET_SPEED = 700.0
ENEMY_BASE_SPEED = 40.0
ENEMY_DROP_AMOUNT = 30
ENEMY_FIRE_CHANCE = 0.0025  # per attempt per enemy
POWERUP_RATE = 0.008  # per second spawn chance
BOSS_EVERY_N_LEVELS = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
UI_BG = (20, 20, 30)
BG_COLOR = (12, 18, 28)

# ------------------------- Utilities -------------------------
def load_highscore():
    try:
        if os.path.exists(HIGHSCORE_FILE):
            with open(HIGHSCORE_FILE, 'r') as f:
                return json.load(f).get('highscore', 0)
    except Exception:
        pass
    return 0


def save_highscore(score):
    try:
        with open(HIGHSCORE_FILE, 'w') as f:
            json.dump({'highscore': score}, f)
    except Exception:
        pass


def clamp(v, a, b):
    return max(a, min(b, v))


# ------------------------- Pygame Initialization -------------------------
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# Try to init audio
SOUND_ENABLED = True
try:
    mixer.init()
except Exception:
    SOUND_ENABLED = False

# Fonts
FONT = pygame.font.SysFont('consolas', 20)
BIG_FONT = pygame.font.SysFont('consolas', 44)
SMALL_FONT = pygame.font.SysFont('consolas', 16)

# ------------------------- Asset helpers -------------------------

def try_load_sound(name):
    if not SOUND_ENABLED:
        return None
    path = os.path.join(ASSETS_DIR, name)
    if os.path.exists(path):
        try:
            return mixer.Sound(path)
        except Exception:
            return None
    return None


def try_load_image(name):
    path = os.path.join(ASSETS_DIR, name)
    if os.path.exists(path):
        try:
            img = pygame.image.load(path).convert_alpha()
            return img
        except Exception:
            return None
    return None


SND_SHOOT = try_load_sound('shoot.wav')
SND_EXPLODE = try_load_sound('explode.wav')
SND_POWERUP = try_load_sound('powerup.wav')
SND_HIT = try_load_sound('hit.wav')

IMG_PLAYER = try_load_image('player.png')
IMG_ENEMY = try_load_image('enemy.png')
IMG_BOSS = try_load_image('boss.png')


# ------------------------- Game Objects -------------------------
@dataclass
class Vec2:
    x: float
    y: float

    def tuple(self):
        return (int(self.x), int(self.y))


class GameObject:
    def __init__(self, pos: Vec2):
        self.pos = pos
        self.dead = False

    def update(self, dt, game):
        pass

    def draw(self, surf):
        pass


class Bullet(GameObject):
    def __init__(self, pos, vel, owner='player', damage=1, radius=4):
        super().__init__(Vec2(pos.x, pos.y))
        self.vel = vel
        self.owner = owner
        self.damage = damage
        self.radius = radius

    def update(self, dt, game):
        self.pos.x += self.vel.x * dt
        self.pos.y += self.vel.y * dt
        if self.pos.y < -50 or self.pos.y > HEIGHT + 50 or self.pos.x < -50 or self.pos.x > WIDTH + 50:
            self.dead = True

    def draw(self, surf):
        pygame.draw.circle(surf, WHITE, self.pos.tuple(), self.radius)


class Particle(GameObject):
    def __init__(self, pos, vel, life, size=3):
        super().__init__(Vec2(pos.x, pos.y))
        self.vel = vel
        self.life = life
        self.max_life = life
        self.size = size

    def update(self, dt, game):
        self.life -= dt
        if self.life <= 0:
            self.dead = True
            return
        self.pos.x += self.vel.x * dt
        self.pos.y += self.vel.y * dt

    def draw(self, surf):
        alpha = max(0, int(255 * (self.life / self.max_life)))
        s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        s.fill((255, 180, 60, alpha))
        surf.blit(s, (self.pos.x - self.size, self.pos.y - self.size))


class Player(GameObject):
    def __init__(self, pos):
        super().__init__(pos)
        self.speed = PLAYER_SPEED
        self.width = 48
        self.height = 30
        self.cooldown = 0.0
        self.fire_rate = 0.18  # seconds
        self.lives = 3
        self.score = 0
        self.powerups = {}  # name -> time left
        self.respawn_invuln = 0.0

    def move(self, dir, dt):
        self.pos.x += dir * self.speed * dt
        self.pos.x = clamp(self.pos.x, self.width / 2, WIDTH - self.width / 2)

    def shoot(self, game):
        if self.cooldown > 0:
            return
        spread = 'spread' in self.powerups
        rapid = 'rapid' in self.powerups
        shots = [Vec2(0, -BULLET_SPEED)]
        if spread:
            shots = [Vec2(-180, -BULLET_SPEED), Vec2(0, -BULLET_SPEED), Vec2(180, -BULLET_SPEED)]
        for s in shots:
            b = Bullet(Vec2(self.pos.x, self.pos.y - 22), s, owner='player', damage=1, radius=4)
            game.add(b)
        if SND_SHOOT and game.sound_on:
            SND_SHOOT.play()
        self.cooldown = self.fire_rate * (0.4 if rapid else 1.0)

    def apply_powerup(self, name, duration=8.0):
        self.powerups[name] = duration

    def update(self, dt, game):
        if self.cooldown > 0:
            self.cooldown -= dt
        to_remove = []
        for k in list(self.powerups.keys()):
            self.powerups[k] -= dt
            if self.powerups[k] <= 0:
                to_remove.append(k)
        for k in to_remove:
            del self.powerups[k]
        if self.respawn_invuln > 0:
            self.respawn_invuln -= dt

    def draw(self, surf):
        x, y = int(self.pos.x), int(self.pos.y)
        if IMG_PLAYER:
            img = pygame.transform.smoothscale(IMG_PLAYER, (64, 48))
            surf.blit(img, (x - img.get_width() // 2, y - img.get_height() // 2))
        else:
            hull = [(x - 24, y + 12), (x, y - 18), (x + 24, y + 12)]
            pygame.draw.polygon(surf, (100, 200, 255), hull)
        if self.respawn_invuln > 0:
            alpha = 120 + int(135 * (self.respawn_invuln % 0.6) / 0.6)
            s = pygame.Surface((80, 80), pygame.SRCALPHA)
            pygame.draw.circle(s, (80, 160, 255, alpha), (40, 40), 38, 3)
            surf.blit(s, (x - 40, y - 40))


class Enemy(GameObject):
    def __init__(self, pos, etype=0):
        super().__init__(pos)
        self.etype = etype
        self.width = 40
        self.height = 30
        self.max_hp = 1 + etype // 2
        self.hp = self.max_hp
        self.base_y = pos.y
        self.osc = random.uniform(0, math.pi * 2)

    def hit(self, dmg, game):
        self.hp -= dmg
        if SND_HIT and game.sound_on:
            SND_HIT.play()
        if self.hp <= 0:
            self.dead = True
            game.player.score += 10 + self.etype * 5
            game.create_explosion(self.pos)

    def update(self, dt, game):
        self.osc += dt * (1 + self.etype * 0.2)
        self.pos.y = self.base_y + math.sin(self.osc) * (4 + self.etype * 2)

    def draw(self, surf):
        x, y = int(self.pos.x), int(self.pos.y)
        if IMG_ENEMY:
            img = pygame.transform.smoothscale(IMG_ENEMY, (48, 36))
            surf.blit(img, (x - img.get_width() // 2, y - img.get_height() // 2))
        else:
            color = (200 - self.etype * 20, 100 + self.etype * 30, 120 + self.etype * 8)
            pygame.draw.rect(surf, color, (x - self.width // 2, y - self.height // 2, self.width, self.height))
            pygame.draw.line(surf, BLACK, (x, y - self.height // 2), (x, y - self.height), 2)


class Boss(GameObject):
    def __init__(self, pos, level):
        super().__init__(pos)
        self.level = level
        self.width = 160
        self.height = 80
        self.hp = 20 + (level - 1) * 10
        self.dir = 1
        self.speed = 80 + (level - 1) * 10
        self.fire_timer = 0.0

    def update(self, dt, game):
        self.pos.x += self.dir * self.speed * dt
        if self.pos.x < 100 or self.pos.x > WIDTH - 100:
            self.dir *= -1
        self.fire_timer += dt
        if self.fire_timer > 0.6:
            # fire fan bullets
            for ang in (-0.6, -0.3, 0, 0.3, 0.6):
                vx = math.sin(ang) * BULLET_SPEED * 0.6
                vy = math.cos(ang) * BULLET_SPEED * 0.6
                b = Bullet(Vec2(self.pos.x, self.pos.y + 40), Vec2(vx, vy), owner='enemy', damage=1, radius=6)
                game.add(b)
            self.fire_timer = 0.0

    def hit(self, dmg, game):
        self.hp -= dmg
        if self.hp <= 0:
            self.dead = True
            game.player.score += 500
            game.create_explosion(self.pos)

    def draw(self, surf):
        x, y = int(self.pos.x), int(self.pos.y)
        if IMG_BOSS:
            img = pygame.transform.smoothscale(IMG_BOSS, (self.width, self.height))
            surf.blit(img, (x - img.get_width() // 2, y - img.get_height() // 2))
        else:
            pygame.draw.rect(surf, (180, 40, 40), (x - self.width//2, y - self.height//2, self.width, self.height))
            # health bar
            w = int((self.hp / (20 + (game.level - 1) * 10)) * (self.width - 20)) if hasattr(game, 'level') else self.width - 20
            pygame.draw.rect(surf, (50, 200, 50), (x - (self.width - 20)//2, y - self.height//2 - 12, w, 8))


class ShieldBlock(GameObject):
    def __init__(self, pos):
        super().__init__(pos)
        self.size = 14
        self.hp = 4

    def hit(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.dead = True

    def draw(self, surf):
        color = (40 + self.hp * 40, 100 + self.hp * 20, 70)
        pygame.draw.rect(surf, color, (int(self.pos.x - self.size/2), int(self.pos.y - self.size/2), self.size, self.size))


class Powerup(GameObject):
    TYPES = ['rapid', 'spread', 'shield', 'score']

    def __init__(self, pos, ptype=None):
        super().__init__(pos)
        self.ptype = ptype if ptype is not None else random.choice(self.TYPES)
        self.radius = 12
        self.vel = Vec2(0, 80)

    def update(self, dt, game):
        self.pos.x += self.vel.x * dt
        self.pos.y += self.vel.y * dt
        if self.pos.y > HEIGHT + 40:
            self.dead = True
        dx = self.pos.x - game.player.pos.x
        dy = self.pos.y - game.player.pos.y
        if dx*dx + dy*dy < (self.radius + 30)**2:
            self.dead = True
            if self.ptype == 'score':
                game.player.score += 200
            elif self.ptype == 'shield':
                game.player.respawn_invuln = 6.0
            else:
                game.player.apply_powerup(self.ptype, duration=10.0)
            if SND_POWERUP and game.sound_on:
                SND_POWERUP.play()

    def draw(self, surf):
        x, y = int(self.pos.x), int(self.pos.y)
        pygame.draw.circle(surf, (255, 220, 80), (x, y), self.radius)
        small = SMALL_FONT.render(self.ptype[0].upper(), True, BLACK)
        surf.blit(small, (x - small.get_width()/2, y - small.get_height()/2))


# ------------------------- Game Controller -------------------------
class Game:
    def __init__(self):
        self.running = True
        self.entities = []
        self.player = Player(Vec2(WIDTH/2, HEIGHT - 80))
        self.entities.append(self.player)
        self.bullets = []
        self.particles = []
        self.enemies = []
        self.shields = []
        self.powerups = []
        self.enemy_direction = 1
        self.enemy_speed = ENEMY_BASE_SPEED
        self.enemy_timer = 0.0
        self.level = 1
        self.kills = 0
        self.boss = None
        self.spawn_enemy_wave()
        self.create_shields()
        self.paused = False
        self.sound_on = SOUND_ENABLED
        self.highscore = load_highscore()
        self.game_over = False
        self.start_screen = True
        self.spawn_accum = 0.0

    def add(self, obj):
        if isinstance(obj, Bullet):
            self.bullets.append(obj)
        elif isinstance(obj, Particle):
            self.particles.append(obj)
        elif isinstance(obj, Enemy):
            self.enemies.append(obj)
        elif isinstance(obj, ShieldBlock):
            self.shields.append(obj)
        elif isinstance(obj, Powerup):
            self.powerups.append(obj)
        else:
            self.entities.append(obj)

    def spawn_enemy_wave(self):
        self.enemies.clear()
        if self.level % BOSS_EVERY_N_LEVELS == 0:
            # spawn boss
            self.boss = Boss(Vec2(WIDTH/2, 140), self.level)
            return
        rows = 3 + (self.level // 2)
        cols = 10
        margin_x = 80
        spacing_x = (WIDTH - margin_x * 2) / (cols - 1)
        for r in range(rows):
            for c in range(cols):
                x = margin_x + c * spacing_x
                y = 80 + r * 60
                etype = (r + (self.level - 1)) % 3
                e = Enemy(Vec2(x, y), etype=etype)
                self.enemies.append(e)
        self.enemy_speed = ENEMY_BASE_SPEED + (self.level - 1) * 8

    def create_shields(self):
        self.shields.clear()
        shield_count = 4
        spacing = WIDTH / (shield_count + 1)
        for i in range(shield_count):
            cx = spacing * (i + 1)
            for rx in range(-2, 3):
                for ry in range(0, 3):
                    pos = Vec2(cx + rx * 16, HEIGHT - 180 + ry * 16)
                    self.add(ShieldBlock(pos))

    def create_explosion(self, pos):
        for _ in range(18):
            ang = random.random() * math.pi * 2
            spd = random.uniform(40, 320)
            v = Vec2(math.cos(ang) * spd, math.sin(ang) * spd)
            p = Particle(Vec2(pos.x, pos.y), v, life=random.uniform(0.4, 1.0), size=random.randint(2, 5))
            self.add(p)
        if SND_EXPLODE and self.sound_on:
            SND_EXPLODE.play()

    def spawn_powerup(self):
        x = random.uniform(60, WIDTH - 60)
        self.add(Powerup(Vec2(x, -20)))

    def fire_enemy_bullets(self):
        if self.boss:
            # boss fires handled in boss.update
            return
        columns = {}
        for e in self.enemies:
            col = int(e.pos.x // 64)
            if col not in columns or e.pos.y > columns[col].pos.y:
                columns[col] = e
        for e in columns.values():
            if random.random() < ENEMY_FIRE_CHANCE * (1 + self.level * 0.05):
                v = Vec2(random.uniform(-30, 30), BULLET_SPEED * 0.6)
                b = Bullet(Vec2(e.pos.x, e.pos.y + 18), v, owner='enemy', damage=1, radius=6)
                self.add(b)

    def update(self, dt):
        if self.paused or self.game_over or self.start_screen:
            return
        # boss handling
        if self.boss:
            self.boss.update(dt, self)
            if self.boss.dead:
                self.boss = None
                self.level += 1
                self.spawn_enemy_wave()
                self.create_shields()
            return
        # move enemy block
        if self.enemies:
            minx = min(e.pos.x for e in self.enemies)
            maxx = max(e.pos.x for e in self.enemies)
            step = self.enemy_direction * self.enemy_speed * dt
            if maxx + step + 40 > WIDTH or minx + step - 40 < 0:
                for e in self.enemies:
                    e.pos.y += ENEMY_DROP_AMOUNT
                    e.base_y += ENEMY_DROP_AMOUNT
                self.enemy_direction *= -1
            else:
                for e in self.enemies:
                    e.pos.x += step
        # update entities
        for obj in list(self.entities):
            obj.update(dt, self)
            if obj.dead and obj in self.entities:
                self.entities.remove(obj)
        for arr in (self.bullets, self.particles, self.enemies, self.shields, self.powerups):
            for obj in list(arr):
                obj.update(dt, self)
                if obj.dead:
                    arr.remove(obj)
        # collisions
        self.resolve_collisions()
        # enemy firing
        self.enemy_timer += dt
        if self.enemy_timer > 0.2:
            self.fire_enemy_bullets()
            self.enemy_timer = 0.0
        # powerup spawn
        if random.random() < POWERUP_RATE * dt * (1 + self.level * 0.1):
            self.spawn_powerup()
        # level progress
        if not self.enemies and not self.boss:
            self.level += 1
            self.spawn_enemy_wave()
            self.create_shields()

    def resolve_collisions(self):
        # bullets vs enemies
        for b in list(self.bullets):
            if b.owner == 'player':
                # boss hit
                if self.boss:
                    dx = abs(b.pos.x - self.boss.pos.x)
                    dy = abs(b.pos.y - (self.boss.pos.y + 20))
                    if dx < self.boss.width/2 and dy < self.boss.height/2:
                        self.boss.hit(b.damage, self)
                        b.dead = True
                        continue
                for e in list(self.enemies):
                    dx = b.pos.x - e.pos.x
                    dy = b.pos.y - e.pos.y
                    if abs(dx) < e.width/2 and abs(dy) < e.height/2:
                        e.hit(b.damage, self)
                        b.dead = True
                        self.kills += 1
                        break
            else:
                # enemy bullet hits player
                dx = b.pos.x - self.player.pos.x
                dy = b.pos.y - self.player.pos.y
                if dx*dx + dy*dy < (b.radius + 18)**2 and self.player.respawn_invuln <= 0:
                    b.dead = True
                    self.player.lives -= 1
                    self.create_explosion(self.player.pos)
                    self.player.respawn_invuln = 2.5
                    if self.player.lives <= 0:
                        self.game_over = True
                        if self.player.score > self.highscore:
                            self.highscore = self.player.score
                            save_highscore(self.highscore)
        # bullets vs shields
        for b in list(self.bullets):
            for s in list(self.shields):
                dx = b.pos.x - s.pos.x
                dy = b.pos.y - s.pos.y
                if abs(dx) < s.size/2 + b.radius and abs(dy) < s.size/2 + b.radius:
                    s.hit(b.damage)
                    b.dead = True
                    break
        # enemies reaching bottom
        for e in list(self.enemies):
            if e.pos.y >= self.player.pos.y - 30:
                self.game_over = True

    def draw_ui(self, surf):
        pygame.draw.rect(surf, UI_BG, (0, 0, WIDTH, 48))
        txt = FONT.render(f'Score: {self.player.score}   Lives: {self.player.lives}   Level: {self.level}   High: {self.highscore}', True, WHITE)
        surf.blit(txt, (12, 12))
        if self.paused:
            pa = BIG_FONT.render('-- PAUSED --', True, WHITE)
            surf.blit(pa, (WIDTH/2 - pa.get_width()/2, HEIGHT/2 - pa.get_height()/2))
        if self.game_over:
            go = BIG_FONT.render('GAME OVER', True, WHITE)
            surf.blit(go, (WIDTH/2 - go.get_width()/2, HEIGHT/2 - 80))
            sub = FONT.render('Press R to restart or ESC to quit', True, WHITE)
            surf.blit(sub, (WIDTH/2 - sub.get_width()/2, HEIGHT/2 - 30))

    def draw(self, surf):
        surf.fill(BG_COLOR)
        for i in range(120):
            pygame.draw.circle(surf, (20, 20, 40), (i * 23 % WIDTH, (i * 47) % HEIGHT), 1)
        for s in self.shields:
            s.draw(surf)
        for e in self.enemies:
            e.draw(surf)
        if self.boss:
            self.boss.draw(surf)
        for b in self.bullets:
            b.draw(surf)
        for p in self.particles:
            p.draw(surf)
        self.player.draw(surf)
        for pu in self.powerups:
            pu.draw(surf)
        self.draw_ui(surf)

    def restart(self):
        self.__init__()


# ------------------------- Main Loop -------------------------

def draw_start_screen(surf):
    surf.fill(BG_COLOR)
    title = BIG_FONT.render('SPACE INVADERS - Advanced', True, WHITE)
    instr = FONT.render('←/→ or A/D to move   SPACE to shoot   P to pause   M to mute', True, WHITE)
    start = FONT.render('Press ENTER to start', True, WHITE)
    surf.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 120))
    surf.blit(instr, (WIDTH//2 - instr.get_width()//2, HEIGHT//2 - 40))
    surf.blit(start, (WIDTH//2 - start.get_width()//2, HEIGHT//2 + 10))
    pygame.display.flip()


def main():
    game = Game()
    key_left = key_right = False
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game.start_screen:
                    if event.key == pygame.K_RETURN:
                        game.start_screen = False
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                    continue
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    key_left = True
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    key_right = True
                if event.key == pygame.K_SPACE:
                    game.player.shoot(game)
                if event.key == pygame.K_p:
                    game.paused = not game.paused
                if event.key == pygame.K_m:
                    game.sound_on = not game.sound_on
                if event.key == pygame.K_r and game.game_over:
                    game.restart()
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    key_left = False
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    key_right = False

        if game.start_screen:
            draw_start_screen(screen)
            continue

        if key_left and not key_right:
            game.player.move(-1, dt)
        elif key_right and not key_left:
            game.player.move(1, dt)

        game.update(dt)
        game.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
