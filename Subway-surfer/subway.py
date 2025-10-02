import cv2
import numpy as np
import pygame
import random
import math
import sys
import time
import mediapipe as mp
import os
from pygame import mixer

pygame.init()
mixer.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
LANE_WIDTH = SCREEN_WIDTH // 3
PLAYER_SIZE = 60
OBSTACLE_WIDTH = 70
OBSTACLE_HEIGHT = 70
COIN_SIZE = 35
POWER_SIZE = 40
GRAVITY = 1.2
JUMP_FORCE = 18
SPEED_INCREASE = 0.3
MAX_SPEED = 18
FPS = 60


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (100, 100, 100)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Enhanced Hand-Controlled Subway Surfers")
clock = pygame.time.Clock()

if not os.path.exists('assets'):
    os.makedirs('assets')

def create_player_image():
    surf = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE), pygame.SRCALPHA)
    pygame.draw.rect(surf, BLUE, (5, 5, PLAYER_SIZE-10, PLAYER_SIZE-10), border_radius=8)
    pygame.draw.circle(surf, WHITE, (PLAYER_SIZE//3, PLAYER_SIZE//3), 5)
    pygame.draw.circle(surf, WHITE, (PLAYER_SIZE*2//3, PLAYER_SIZE//3), 5)
    pygame.draw.rect(surf, WHITE, (PLAYER_SIZE//4, PLAYER_SIZE*2//3, PLAYER_SIZE//2, 5), border_radius=3)
    return surf

def create_obstacle_image(obstacle_type):
    surf = pygame.Surface((OBSTACLE_WIDTH, OBSTACLE_HEIGHT), pygame.SRCALPHA)
    if obstacle_type == "train":
        pygame.draw.rect(surf, RED, (0, 0, OBSTACLE_WIDTH, OBSTACLE_HEIGHT), border_radius=5)
        pygame.draw.rect(surf, BLACK, (5, 15, OBSTACLE_WIDTH-10, 10))
        pygame.draw.rect(surf, BLACK, (5, 35, OBSTACLE_WIDTH-10, 10))
        pygame.draw.rect(surf, YELLOW, (OBSTACLE_WIDTH-15, 5, 10, 10))
    elif obstacle_type == "barrier":
        pygame.draw.rect(surf, ORANGE, (10, 0, OBSTACLE_WIDTH-20, OBSTACLE_HEIGHT), border_radius=3)
        pygame.draw.rect(surf, ORANGE, (0, OBSTACLE_HEIGHT//4, OBSTACLE_WIDTH, OBSTACLE_HEIGHT//2), border_radius=3)
    else:  
        pygame.draw.rect(surf, RED, (0, 0, OBSTACLE_WIDTH, OBSTACLE_HEIGHT), border_radius=8)
    return surf

def create_coin_image():
    surf = pygame.Surface((COIN_SIZE, COIN_SIZE), pygame.SRCALPHA)
    pygame.draw.circle(surf, YELLOW, (COIN_SIZE//2, COIN_SIZE//2), COIN_SIZE//2)
    pygame.draw.circle(surf, (218, 165, 32), (COIN_SIZE//2, COIN_SIZE//2), COIN_SIZE//2 - 4)
    font = pygame.font.SysFont(None, COIN_SIZE)
    dollar = font.render("$", True, YELLOW)
    surf.blit(dollar, (COIN_SIZE//2 - dollar.get_width()//2, COIN_SIZE//2 - dollar.get_height()//2))
    return surf

def create_power_image(power_type):
    surf = pygame.Surface((POWER_SIZE, POWER_SIZE), pygame.SRCALPHA)
    if power_type == "magnet":
        pygame.draw.circle(surf, PURPLE, (POWER_SIZE//2, POWER_SIZE//2), POWER_SIZE//2)
        pygame.draw.rect(surf, RED, (POWER_SIZE//4, 5, POWER_SIZE//2, POWER_SIZE//2), border_radius=3)
        pygame.draw.rect(surf, WHITE, (POWER_SIZE//4, POWER_SIZE//2, POWER_SIZE//2, POWER_SIZE//3), border_radius=3)
    elif power_type == "jetpack":
        pygame.draw.rect(surf, GRAY, (POWER_SIZE//4, 0, POWER_SIZE//2, POWER_SIZE), border_radius=5)
        pygame.draw.polygon(surf, ORANGE, [(POWER_SIZE//4, POWER_SIZE), (POWER_SIZE//2, POWER_SIZE*3//4), (POWER_SIZE*3//4, POWER_SIZE)])
    elif power_type == "shield":
        pygame.draw.circle(surf, (100, 200, 255, 150), (POWER_SIZE//2, POWER_SIZE//2), POWER_SIZE//2)
        pygame.draw.circle(surf, (150, 220, 255, 200), (POWER_SIZE//2, POWER_SIZE//2), POWER_SIZE//2 - 5, width=3)
    return surf

def create_background():
    surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    for y in range(SCREEN_HEIGHT):
        color_value = 200 - int(150 * y / SCREEN_HEIGHT)
        pygame.draw.line(surf, (100, 100, color_value), (0, y), (SCREEN_WIDTH, y))
    
    for i in range(15):
        height = random.randint(100, 300)
        width = random.randint(50, 100)
        x = random.randint(0, SCREEN_WIDTH - width)
        color = (70, 70, 70)
        pygame.draw.rect(surf, color, (x, SCREEN_HEIGHT - height - 100, width, height))
        
        for wy in range(5, height, 20):
            for wx in range(10, width-10, 20):
                window_color = (200, 200, 100) if random.random() > 0.5 else (50, 50, 50)
                pygame.draw.rect(surf, window_color, (x + wx, SCREEN_HEIGHT - height - 100 + wy, 10, 10))
    
    return surf

player_img = create_player_image()
train_img = create_obstacle_image("train")
barrier_img = create_obstacle_image("barrier")
coin_img = create_coin_image()
magnet_img = create_power_image("magnet")
jetpack_img = create_power_image("jetpack")
shield_img = create_power_image("shield")
background = create_background()

try:
    jump_sound = mixer.Sound('assets/jump.wav')
    coin_sound = mixer.Sound('assets/coin.wav')
    crash_sound = mixer.Sound('assets/crash.wav')
    power_up_sound = mixer.Sound('assets/power_up.wav')
except:
    jump_sound = mixer.Sound(buffer=np.sin(np.linspace(0, 3, 22050)).astype(np.float32).tobytes())
    coin_sound = mixer.Sound(buffer=np.sin(np.linspace(0, 10, 22050)).astype(np.float32).tobytes())
    crash_sound = mixer.Sound(buffer=np.sin(np.linspace(0, 1, 44100)).astype(np.float32).tobytes())
    power_up_sound = mixer.Sound(buffer=np.sin(np.linspace(0, 5, 33075)).astype(np.float32).tobytes())
    
    jump_sound.set_volume(0.3)
    coin_sound.set_volume(0.4)
    crash_sound.set_volume(0.5)
    power_up_sound.set_volume(0.4)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

class Player:
    def __init__(self):
        self.lane = 1  
        self.x = SCREEN_WIDTH // 2 - PLAYER_SIZE // 2
        self.y = SCREEN_HEIGHT - 2 * PLAYER_SIZE
        self.jumping = False
        self.y_velocity = 0
        self.has_shield = False
        self.shield_timer = 0
        self.has_magnet = False
        self.magnet_timer = 0
        self.has_jetpack = False
        self.jetpack_timer = 0
        self.animation_frame = 0
        self.animation_timer = 0
    
    def draw(self):
        if self.has_jetpack:
            flame_height = random.randint(20, 40)
            pygame.draw.polygon(screen, ORANGE, 
                                [(self.x + PLAYER_SIZE//4, self.y + PLAYER_SIZE),
                                 (self.x + PLAYER_SIZE//2, self.y + PLAYER_SIZE + flame_height),
                                 (self.x + PLAYER_SIZE*3//4, self.y + PLAYER_SIZE)])
        
        screen.blit(player_img, (self.x, self.y))
        
        if not self.jumping and not self.has_jetpack:
            self.animation_timer += 1
            if self.animation_timer >= 5:
                self.animation_timer = 0
                self.animation_frame = (self.animation_frame + 1) % 4
                if self.animation_frame < 2:
                    self.y += 2
                else:
                    self.y -= 2
                    
        if self.has_shield:
            pygame.draw.circle(screen, (100, 200, 255, 100), 
                            (self.x + PLAYER_SIZE//2, self.y + PLAYER_SIZE//2), 
                            PLAYER_SIZE, width=3)
        
        if self.has_magnet:
            for angle in range(0, 360, 45):
                start_x = self.x + PLAYER_SIZE//2
                start_y = self.y + PLAYER_SIZE//2
                end_x = start_x + int(PLAYER_SIZE * 0.8 * math.cos(math.radians(angle)))
                end_y = start_y + int(PLAYER_SIZE * 0.8 * math.sin(math.radians(angle)))
                pygame.draw.line(screen, PURPLE, (start_x, start_y), (end_x, end_y), 2)
        
    def update_position(self):
        self.x = (LANE_WIDTH * self.lane + LANE_WIDTH // 2) - PLAYER_SIZE // 2
        
        if self.has_jetpack:
            self.y -= 5  
            if self.y < PLAYER_SIZE:  
                self.y = PLAYER_SIZE
            self.jetpack_timer -= 1
            if self.jetpack_timer <= 0:
                self.has_jetpack = False
                self.jumping = True
                self.y_velocity = 0
        elif self.jumping:
            self.y -= self.y_velocity
            self.y_velocity -= GRAVITY
            
            if self.y >= SCREEN_HEIGHT - 2 * PLAYER_SIZE:
                self.y = SCREEN_HEIGHT - 2 * PLAYER_SIZE
                self.jumping = False
                self.y_velocity = 0
        
        if self.has_shield:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.has_shield = False
                
        if self.has_magnet:
            self.magnet_timer -= 1
            if self.magnet_timer <= 0:
                self.has_magnet = False
    
    def jump(self):
        if not self.jumping and not self.has_jetpack:
            self.jumping = True
            self.y_velocity = JUMP_FORCE
            jump_sound.play()

    def activate_shield(self):
        self.has_shield = True
        self.shield_timer = FPS * 8  
        power_up_sound.play()
        
    def activate_magnet(self):
        self.has_magnet = True
        self.magnet_timer = FPS * 10
        power_up_sound.play()
        
    def activate_jetpack(self):
        self.has_jetpack = True
        self.jetpack_timer = FPS * 5  #
        self.jumping = False  
        power_up_sound.play()

class Obstacle:
    def __init__(self, lane, speed):
        self.lane = lane
        self.x = (LANE_WIDTH * lane + LANE_WIDTH // 2) - OBSTACLE_WIDTH // 2
        self.y = -OBSTACLE_HEIGHT
        self.speed = speed
        self.type = random.choice(["train", "barrier"])
        self.image = train_img if self.type == "train" else barrier_img
        
    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        
    def update(self):
        self.y += self.speed
        
    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT
        
    def collides_with(self, player):
        collision_buffer = 10
        return (self.lane == player.lane and 
                self.y + OBSTACLE_HEIGHT - collision_buffer > player.y + collision_buffer and 
                self.y + collision_buffer < player.y + PLAYER_SIZE - collision_buffer)

class Coin:
    def __init__(self, lane, speed):
        self.lane = lane
        self.x = (LANE_WIDTH * lane + LANE_WIDTH // 2) - COIN_SIZE // 2
        self.y = -COIN_SIZE
        self.speed = speed
        self.collected = False
        self.image = coin_img
        self.angle = 0  
        self.magnet_pull = False
        
    def draw(self):
        if not self.collected:
            self.angle = (self.angle + 5) % 360
            rotated_img = pygame.transform.rotate(self.image, self.angle)
            rect = rotated_img.get_rect(center=(self.x + COIN_SIZE//2, self.y + COIN_SIZE//2))
            screen.blit(rotated_img, rect.topleft)
        
    def update(self, player):
        self.y += self.speed
        
        if player.has_magnet:
            player_center_x = player.x + PLAYER_SIZE//2
            player_center_y = player.y + PLAYER_SIZE//2
            coin_center_x = self.x + COIN_SIZE//2
            coin_center_y = self.y + COIN_SIZE//2
            
            dx = player_center_x - coin_center_x
            dy = player_center_y - coin_center_y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance < 200:
                self.magnet_pull = True
                pull_strength = (200 - distance) / 100
                self.x += dx * 0.1 * pull_strength
                self.y += dy * 0.1 * pull_strength
        
    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT
        
    def collides_with(self, player):
        if self.collected:
            return False
            
        player_center_x = player.x + PLAYER_SIZE//2
        player_center_y = player.y + PLAYER_SIZE//2
        coin_center_x = self.x + COIN_SIZE//2
        coin_center_y = self.y + COIN_SIZE//2
        
        distance = math.sqrt((player_center_x - coin_center_x)**2 + (player_center_y - coin_center_y)**2)
        return distance < (PLAYER_SIZE + COIN_SIZE) / 2 - 5

class PowerUp:
    def __init__(self, lane, speed):
        self.lane = lane
        self.x = (LANE_WIDTH * lane + LANE_WIDTH // 2) - POWER_SIZE // 2
        self.y = -POWER_SIZE
        self.speed = speed
        self.collected = False
        self.type = random.choice(["shield", "magnet", "jetpack"])
        if self.type == "shield":
            self.image = shield_img
        elif self.type == "magnet":
            self.image = magnet_img
        else:  # jetpack
            self.image = jetpack_img
        self.glow_timer = 0
        
    def draw(self):
        if not self.collected:
            self.glow_timer = (self.glow_timer + 1) % 60
            glow_size = 5 + int(3 * math.sin(self.glow_timer / 10))
            
            for i in range(glow_size, 0, -1):
                alpha = 100 - i * 10
                if alpha < 0:
                    alpha = 0
                s = pygame.Surface((POWER_SIZE + i*2, POWER_SIZE + i*2), pygame.SRCALPHA)
                if self.type == "shield":
                    color = (100, 200, 255, alpha)
                elif self.type == "magnet":
                    color = (PURPLE[0], PURPLE[1], PURPLE[2], alpha)
                else:  # jetpack
                    color = (ORANGE[0], ORANGE[1], ORANGE[2], alpha)
                pygame.draw.circle(s, color, (POWER_SIZE//2 + i, POWER_SIZE//2 + i), POWER_SIZE//2 + i)
                screen.blit(s, (self.x - i, self.y - i))
            
            screen.blit(self.image, (self.x, self.y))
        
    def update(self):
        self.y += self.speed
        
    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT
        
    def collides_with(self, player):
        if self.collected:
            return False
            
        return (self.lane == player.lane and 
                self.y + POWER_SIZE > player.y and 
                self.y < player.y + PLAYER_SIZE)

class Particle:
    def __init__(self, x, y, color, size=5, speed=3, lifetime=30):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.speed_x = random.uniform(-speed, speed)
        self.speed_y = random.uniform(-speed, speed)
        self.lifetime = lifetime
        self.age = 0
        
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.age += 1
        self.size = max(0, self.size - 0.1)
        
    def draw(self):
        alpha = int(255 * (1 - self.age / self.lifetime))
        if alpha < 0:
            alpha = 0
        color_with_alpha = (*self.color, alpha)
        
        s = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
        pygame.draw.circle(s, color_with_alpha, (int(self.size), int(self.size)), int(self.size))
        screen.blit(s, (int(self.x - self.size), int(self.y - self.size)))
        
    def is_dead(self):
        return self.age >= self.lifetime or self.size <= 0


player = Player()
obstacles = []
coins = []
power_ups = []
particles = []
score = 0
coins_collected = 0
distance = 0 
game_speed = 5
spawn_timer = 0
power_up_spawn_chance = 0.1 
game_over = False
pause = False
jumping_gesture_cooldown = 0
hand_history = []  

title_font = pygame.font.SysFont('Arial', 64, bold=True)
font = pygame.font.SysFont('Arial', 36)
small_font = pygame.font.SysFont('Arial', 24)

def detect_hand_gesture(frame):

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    results = hands.process(rgb_frame)
    
    gesture = {"lane": 1, "jump": False}  
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            

            landmarks = []
            for landmark in hand_landmarks.landmark:

                h, w, _ = frame.shape
                x, y = int(landmark.x * w), int(landmark.y * h)
                landmarks.append((x, y))
            

            wrist_x = landmarks[0][0]
            frame_width = frame.shape[1]
            

            hand_history.append(wrist_x)
            if len(hand_history) > 5:   
                hand_history.pop(0)
            

            avg_x = sum(hand_history) / len(hand_history)
            
            if avg_x < frame_width / 3:
                gesture["lane"] = 0   
            elif avg_x > 2 * frame_width / 3:
                gesture["lane"] = 2   
            else:
                gesture["lane"] = 1   
            
           
           
            index_tip_y = landmarks[8][1]
            wrist_y = landmarks[0][1]
            
             
            if wrist_y - index_tip_y > frame.shape[0] / 6:  
                gesture["jump"] = True
    

    cv2.imshow('Hand Detection', frame)
    
    return gesture


def create_particles(x, y, color, count=10, size=5, speed=3, lifetime=30):
    for _ in range(count):
        particles.append(Particle(x, y, color, size, speed, lifetime))


def show_tutorial():
    tutorial = True
    
    while tutorial:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    tutorial = False
                    

        screen.fill(WHITE)
        

        title_text = title_font.render("Hand Controls Tutorial", True, BLUE)
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 50))
        

        instructions = [
            "Use your hand to control the game:",
            "1. Move your hand LEFT/RIGHT to change lanes",
            "2. Raise your INDEX FINGER to JUMP",
            "3. Collect coins and power-ups",
            "4. Avoid obstacles",
            "",
            "Power-ups:",
            "- SHIELD: Protects from one collision",
            "- MAGNET: Attracts coins",
            "- JETPACK: Fly over obstacles",
            "",
            "Press SPACE to start"
        ]
        
        y_pos = 150
        for line in instructions:
            text = font.render(line, True, BLACK)
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, y_pos))
            y_pos += 40
        

        pygame.display.flip()
        clock.tick(FPS)


show_tutorial()


running = True
cap = cv2.VideoCapture(0) 


try:
    pygame.mixer.music.load('assets/background_music.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1) 
except:
    pass   

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.lane = max(0, player.lane - 1)
            elif event.key == pygame.K_RIGHT:
                player.lane = min(2, player.lane + 1)
            elif event.key == pygame.K_UP:
                player.jump()
            elif event.key == pygame.K_p:
                pause = not pause
            elif event.key == pygame.K_r and game_over:

                player = Player()
                obstacles = []
                coins = []
                power_ups = []
                particles = []
                score = 0
                coins_collected = 0
                distance = 0
                game_speed = 5
                game_over = False
    

    if not game_over and not pause:
        ret, frame = cap.read()
        if ret:

            frame = cv2.flip(frame, 1)
            

            gesture = detect_hand_gesture(frame)
            

            player.lane = gesture["lane"]
            

            if jumping_gesture_cooldown > 0:
                jumping_gesture_cooldown -= 1
            elif gesture["jump"] and not player.jumping:
                player.jump()
                jumping_gesture_cooldown = 20  
                

    screen.blit(background, (0, 0))
    

    for i in range(4):
        lane_x = i * LANE_WIDTH

        pygame.draw.line(screen, WHITE, 
                        (SCREEN_WIDTH//2 + (lane_x - SCREEN_WIDTH//2) * 0.8, 0), 
                        (lane_x, SCREEN_HEIGHT), 3)
    
    if not game_over and not pause:

        player.update_position()
        

        distance += game_speed / 50  
        

        spawn_timer += 1
        if spawn_timer >= int(60 / (game_speed / 5)):   
            spawn_timer = 0
            

            lane = random.randint(0, 2)
            

            spawn_roll = random.random()
            if spawn_roll < power_up_spawn_chance:

                power_ups.append(PowerUp(lane, game_speed))
            elif spawn_roll < 0.4:   
                coins.append(Coin(lane, game_speed))
            else:  
                obstacles.append(Obstacle(lane, game_speed))
                

                if random.random() < 0.3:
                    coins.append(Coin(lane, game_speed - 1))
                    coins[-1].y -= OBSTACLE_HEIGHT * 2
        

        for obstacle in obstacles[:]:
            obstacle.update()
            obstacle.draw()
            

            if obstacle.collides_with(player):
                if player.has_shield:
                    player.has_shield = False
                    player.shield_timer = 0
                    obstacles.remove(obstacle)
                    create_particles(player.x + PLAYER_SIZE//2, player.y + PLAYER_SIZE//2, 
                                    (100, 200, 255), count=20, size=8)
                    power_up_sound.play()
                else:
                    game_over = True
                    crash_sound.play()
                    create_particles(player.x + PLAYER_SIZE//2, player.y + PLAYER_SIZE//2, 
                                    RED, count=30, size=10, speed=5)
            

            if obstacle.is_off_screen():
                obstacles.remove(obstacle)
                score += 5
        
        for coin in coins[:]:
            coin.update(player)
            coin.draw()
            
            if coin.collides_with(player):
                coin.collected = True
                score += 10
                coins_collected += 1
                coin_sound.play()
                create_particles(coin.x + COIN_SIZE//2, coin.y + COIN_SIZE//2, 
                               YELLOW, count=15, size=5)
            
            if coin.is_off_screen() or coin.collected:
                coins.remove(coin)
        
        for power_up in power_ups[:]:
            power_up.update()
            power_up.draw()
            
            if power_up.collides_with(player):
                power_up.collected = True
                if power_up.type == "shield":
                    player.activate_shield()
                elif power_up.type == "magnet":
                    player.activate_magnet()
                elif power_up.type == "jetpack":
                    player.activate_jetpack()
                create_particles(power_up.x + POWER_SIZE//2, power_up.y + POWER_SIZE//2, 
                               PURPLE, count=20, size=8)
            
            if power_up.is_off_screen() or power_up.collected:
                power_ups.remove(power_up)
        
        for particle in particles[:]:
            particle.update()
            if particle.is_dead():
                particles.remove(particle)
        
        game_speed = min(MAX_SPEED, game_speed + SPEED_INCREASE / 60)
    


    player.draw()
    


    for particle in particles:
        particle.draw()
    
 
 
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (15, 15))
    
    coins_text = font.render(f"Coins: {coins_collected}", True, YELLOW)
    screen.blit(coins_text, (15, 60))
    
    distance_text = font.render(f"Distance: {int(distance)}m", True, WHITE)
    screen.blit(distance_text, (15, 105))
    

    power_up_y = 150
    if player.has_shield:
        shield_text = small_font.render(f"Shield: {player.shield_timer // FPS}s", True, (100, 200, 255))
        screen.blit(shield_text, (15, power_up_y))
        power_up_y += 35
    
    if player.has_magnet:
        magnet_text = small_font.render(f"Magnet: {player.magnet_timer // FPS}s", True, PURPLE)
        screen.blit(magnet_text, (15, power_up_y))
        power_up_y += 35
        
    if player.has_jetpack:
        jetpack_text = small_font.render(f"Jetpack: {player.jetpack_timer // FPS}s", True, ORANGE)
        screen.blit(jetpack_text, (15, power_up_y))
    

    if game_over:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))   
        screen.blit(overlay, (0, 0))
        
        game_over_text = title_font.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        
        final_score_text = font.render(f"Final Score: {score}", True, WHITE)
        screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 20))
        
        distance_text = font.render(f"Distance: {int(distance)}m", True, WHITE)
        screen.blit(distance_text, (SCREEN_WIDTH // 2 - distance_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
        
        coins_text = font.render(f"Coins: {coins_collected}", True, YELLOW)
        screen.blit(coins_text, (SCREEN_WIDTH // 2 - coins_text.get_width() // 2, SCREEN_HEIGHT // 2 + 60))
        
        restart_text = font.render("Press R to Restart", True, WHITE)
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 120))
    
    if pause:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))   
        screen.blit(overlay, (0, 0))
        
        pause_text = title_font.render("PAUSED", True, WHITE)
        screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        
        continue_text = font.render("Press P to Continue", True, WHITE)
        screen.blit(continue_text, (SCREEN_WIDTH // 2 - continue_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
    
    fps = clock.get_fps()
    fps_text = small_font.render(f"FPS: {int(fps)}", True, WHITE)
    screen.blit(fps_text, (SCREEN_WIDTH - fps_text.get_width() - 10, 10))
    
    pygame.display.flip()
    
    clock.tick(FPS)

cap.release()
cv2.destroyAllWindows()
pygame.quit()
sys.exit()