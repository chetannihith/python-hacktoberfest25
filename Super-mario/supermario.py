import cv2
import numpy as np
import random
import time
import mediapipe as mp
from collections import deque
import threading

class OptimizedHandController:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.6,  
            min_tracking_confidence=0.4
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        self.gesture_history = deque(maxlen=5)  
        self.last_gesture = {
            'move_left': False,
            'move_right': False,
            'jump': False,
            'run': False
        }
        
        self.frame_skip = 0
        self.skip_frames = 2  
        
    def detect_gestures(self, frame):
        self.frame_skip += 1
        if self.frame_skip < self.skip_frames:
            return self.last_gesture, frame
        self.frame_skip = 0
        
        small_frame = cv2.resize(frame, (320, 240))
        rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        gestures = {
            'move_left': False,
            'move_right': False,
            'jump': False,
            'run': False
        }
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                h, w = frame.shape[:2]
                landmarks = []
                for lm in hand_landmarks.landmark:
                    x = lm.x * w / small_frame.shape[1] * frame.shape[1] / w
                    y = lm.y * h / small_frame.shape[0] * frame.shape[0] / h
                    landmarks.append([lm.x, lm.y])  
                
                gestures = self.analyze_hand_position(landmarks)
                
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        
        self.gesture_history.append(gestures)
        smoothed_gestures = self.smooth_gestures()
        self.last_gesture = smoothed_gestures
        
        return smoothed_gestures, frame
    
    def smooth_gestures(self):
        if len(self.gesture_history) < 3:
            return self.gesture_history[-1] if self.gesture_history else self.last_gesture
        
        gesture_counts = {
            'move_left': 0,
            'move_right': 0,
            'jump': 0,
            'run': 0
        }
        
        for gestures in self.gesture_history:
            for key, value in gestures.items():
                if value:
                    gesture_counts[key] += 1
        
        threshold = len(self.gesture_history) // 2
        return {key: count > threshold for key, count in gesture_counts.items()}
    
    def analyze_hand_position(self, landmarks):
        gestures = {
            'move_left': False,
            'move_right': False,
            'jump': False,
            'run': False
        }
        
        if len(landmarks) < 21:
            return gestures
        
        wrist = landmarks[0]
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]
        
        hand_x = wrist[0]
        if hand_x < 0.4:  
            gestures['move_left'] = True
        elif hand_x > 0.6:  
            gestures['move_right'] = True
        
        fingers_up = 0
        
        if thumb_tip[0] > landmarks[3][0]:  
            fingers_up += 1
            
        finger_tips = [8, 12, 16, 20]
        finger_joints = [6, 10, 14, 18]
        
        for tip, joint in zip(finger_tips, finger_joints):
            if landmarks[tip][1] < landmarks[joint][1]:  
                fingers_up += 1
        
        if fingers_up >= 3:  
            gestures['jump'] = True
        elif fingers_up <= 1:  
            gestures['run'] = True
            
        return gestures

class OptimizedParticle:
    def __init__(self, x, y, color, vel_x=0, vel_y=0, life=30):
        self.x = x
        self.y = y
        self.color = color
        self.vel_x = vel_x + random.uniform(-2, 2)
        self.vel_y = vel_y + random.uniform(-3, -1)
        self.life = life
        self.max_life = life
        self.gravity = 0.2
        
    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_y += self.gravity
        self.life -= 1
        
    def draw(self, frame):
        if self.life > 0:
            alpha = self.life / self.max_life
            size = max(1, int(4 * alpha))
            cv2.circle(frame, (int(self.x), int(self.y)), size, self.color, -1)

class PowerUp:
    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.start_y = y
        self.width = 25
        self.height = 25
        self.type = power_type
        self.collected = False
        self.vel_x = 1.5 if random.random() > 0.5 else -1.5
        self.bounce = random.uniform(0, 6.28)
        
    def update(self, platforms):
        if self.collected:
            return
            
        self.x += self.vel_x
        self.bounce += 0.1
        
        self.y = self.start_y + np.sin(self.bounce) * 8
        
        if self.x < 0 or self.x > 4800:
            self.vel_x *= -1
    
    def check_collision(self, rect1, rect2):
        x1, y1, w1, h1 = rect1
        x2, y2, w2, h2 = rect2
        return (x1 < x2 + w2 and x1 + w1 > x2 and 
                y1 < y2 + h2 and y1 + h1 > y2)
    
    def draw(self, frame, camera_x):
        if self.collected:
            return
            
        screen_x = int(self.x - camera_x)
        if screen_x < -50 or screen_x > 850:
            return
            
        if self.type == 'mushroom':
            cv2.circle(frame, (screen_x + self.width//2, int(self.y + self.height//2)), 
                      self.width//2, (0, 0, 200), -1)
            cv2.rectangle(frame, (screen_x + 6, int(self.y + self.height - 6)), 
                         (screen_x + self.width - 6, int(self.y + self.height)), (139, 69, 19), -1)
            
        elif self.type == 'fire_flower':
            center_x, center_y = screen_x + self.width//2, int(self.y + self.height//2)
            cv2.circle(frame, (center_x, center_y), self.width//2, (0, 165, 255), -1)
            cv2.circle(frame, (center_x, center_y), self.width//3, (0, 255, 255), -1)
            
        elif self.type == 'star':
            center_x, center_y = screen_x + self.width//2, int(self.y + self.height//2)
            color_shift = int(self.bounce * 30) % 255
            star_color = (color_shift, 255 - color_shift//2, 255)
            cv2.circle(frame, (center_x, center_y), self.width//2, star_color, -1)

class Fireball:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 10
        self.vel_x = 8 * direction
        self.vel_y = -2
        self.gravity = 0.3
        self.bounces = 0
        self.active = True
        
    def update(self, platforms):
        if not self.active:
            return
            
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_y += self.gravity
        
        fireball_rect = (self.x, self.y, self.width, self.height)
        for platform in platforms:
            if self.check_collision(fireball_rect, platform):
                if self.vel_y > 0:
                    self.y = platform[1] - self.height
                    self.vel_y = -8
                    self.bounces += 1
                    if self.bounces > 3:
                        self.active = False
        
        if self.x < -50 or self.x > 5050 or self.y > 650:
            self.active = False
    
    def check_collision(self, rect1, rect2):
        x1, y1, w1, h1 = rect1
        x2, y2, w2, h2 = rect2
        return (x1 < x2 + w2 and x1 + w1 > x2 and 
                y1 < y2 + h2 and y1 + h1 > y2)
    
    def draw(self, frame, camera_x):
        if self.active:
            screen_x = int(self.x - camera_x)
            if -20 < screen_x < 820:
                cv2.circle(frame, (screen_x, int(self.y)), self.width//2 + 1, (0, 100, 255), -1)
                cv2.circle(frame, (screen_x, int(self.y)), self.width//2, (0, 200, 255), -1)

class Mario:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.width = 32
        self.height = 42
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.facing_right = True
        self.max_speed = 5  
        self.jump_strength = -14  
        self.gravity = 0.7  
        self.state = 'small'
        self.invincible_timer = 0
        self.animation_frame = 0
        self.running = False
        self.fireballs = []
        self.coyote_time = 0  
        self.jump_buffer = 0  
        
    def update(self, platforms, particles):
        if self.on_ground:
            self.coyote_time = 8  
        else:
            self.coyote_time = max(0, self.coyote_time - 1)
            
        if self.jump_buffer > 0:
            self.jump_buffer -= 1
            
        if not self.on_ground:
            self.vel_y = min(12, self.vel_y + self.gravity)  
            
        self.x += self.vel_x
        self.y += self.vel_y
        
        for fireball in self.fireballs[:]:
            fireball.update(platforms)
            if not fireball.active:
                self.fireballs.remove(fireball)
        
        self.on_ground = False
        mario_rect = (self.x, self.y, self.width, self.height)
        
        for platform in platforms:
            if self.check_collision(mario_rect, platform):
                if self.vel_y > 0 and self.y < platform[1]:
                    self.y = platform[1] - self.height
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0 and self.y > platform[1]:
                    self.y = platform[1] + platform[3]
                    self.vel_y = 1  
                else:
                    if self.vel_x > 0:
                        self.x = platform[0] - self.width
                    else:
                        self.x = platform[0] + platform[2]
                    self.vel_x *= 0.5  
        
        self.x = max(0, min(self.x, 4850))
            
        if self.y > 620:
            return 'death'
        
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
        
        if abs(self.vel_x) > 0.1:
            self.animation_frame += 1
            if self.animation_frame > 6:
                self.animation_frame = 0
                
        return 'alive'
    
    def check_collision(self, rect1, rect2):
        x1, y1, w1, h1 = rect1
        x2, y2, w2, h2 = rect2
        return (x1 < x2 + w2 and x1 + w1 > x2 and 
                y1 < y2 + h2 and y1 + h1 > y2)
    
    def jump(self):
        self.jump_buffer = 5
        
        if self.coyote_time > 0 or self.on_ground:
            self.vel_y = self.jump_strength
            self.on_ground = False
            self.coyote_time = 0
            self.jump_buffer = 0
    
    def move_left(self):
        acceleration = 1.0 if self.running else 0.7
        max_vel = self.max_speed * (1.4 if self.running else 1.0)
        self.vel_x = max(-max_vel, self.vel_x - acceleration)
        self.facing_right = False
        
    def move_right(self):
        acceleration = 1.0 if self.running else 0.7
        max_vel = self.max_speed * (1.4 if self.running else 1.0)
        self.vel_x = min(max_vel, self.vel_x + acceleration)
        self.facing_right = True
        
    def stop_horizontal(self):
        friction = 0.8
        self.vel_x *= friction
        if abs(self.vel_x) < 0.1:
            self.vel_x = 0
    
    def power_up(self, power_type):
        if power_type == 'mushroom' and self.state == 'small':
            self.state = 'big'
            self.height = 48
        elif power_type == 'fire_flower':
            self.state = 'fire'
            self.height = 48
        elif power_type == 'star':
            self.invincible_timer = 300
    
    def shoot_fireball(self):
        if self.state == 'fire' and len(self.fireballs) < 2:  
            direction = 1 if self.facing_right else -1
            fireball = Fireball(self.x + self.width//2, self.y + self.height//2, direction)
            self.fireballs.append(fireball)
    
    def take_damage(self):
        if self.invincible_timer > 0:
            return False
            
        if self.state == 'big' or self.state == 'fire':
            self.state = 'small'
            self.height = 42
            self.invincible_timer = 120
            return False
        else:
            return True
    
    def reset_position(self):
        self.x = self.start_x
        self.y = self.start_y
        self.vel_x = 0
        self.vel_y = 0
        self.state = 'small'
        self.height = 42
        self.fireballs.clear()
        self.invincible_timer = 120
    
    def draw(self, frame, camera_x):
        screen_x = int(self.x - camera_x)
        
        if screen_x < -50 or screen_x > 850:
            return
        
        if self.invincible_timer > 0 and self.invincible_timer % 6 < 3:
            return
            
        if self.state == 'fire':
            body_color = (255, 255, 255)
            hat_color = (0, 0, 200)
        else:
            body_color = (0, 0, 255)
            hat_color = (0, 0, 150)
        
        cv2.rectangle(frame, (screen_x, int(self.y)), 
                     (screen_x + self.width, int(self.y + self.height)), body_color, -1)
        
        cv2.rectangle(frame, (screen_x, int(self.y)), 
                     (screen_x + self.width, int(self.y + 12)), hat_color, -1)
        
        cv2.circle(frame, (screen_x + 8, int(self.y + 18)), 3, (255, 255, 255), -1)
        cv2.circle(frame, (screen_x + 24, int(self.y + 18)), 3, (255, 255, 255), -1)
        
        if self.facing_right:
            cv2.circle(frame, (screen_x + 26, int(self.y + 18)), 1, (0, 0, 0), -1)
            cv2.circle(frame, (screen_x + 10, int(self.y + 18)), 1, (0, 0, 0), -1)
        else:
            cv2.circle(frame, (screen_x + 6, int(self.y + 18)), 1, (0, 0, 0), -1)
            cv2.circle(frame, (screen_x + 22, int(self.y + 18)), 1, (0, 0, 0), -1)
        
        for fireball in self.fireballs:
            fireball.draw(frame, camera_x)

class Enemy:
    def __init__(self, x, y, enemy_type='goomba'):
        self.x = x
        self.y = y
        self.start_x = x
        self.type = enemy_type
        self.width = 30
        self.height = 30
        self.vel_x = -1.5  
        self.alive = True
        self.death_timer = 0
        self.animation_frame = 0
        
    def update(self, platforms):
        if not self.alive:
            self.death_timer += 1
            return self.death_timer > 30
            
        self.animation_frame += 1
        if self.animation_frame > 30:
            self.animation_frame = 0
            
        self.x += self.vel_x
        
        if self.x < self.start_x - 80 or self.x > self.start_x + 80:
            self.vel_x *= -1
            
        return False
    
    def kill(self):
        self.alive = False
        self.death_timer = 0
    
    def draw(self, frame, camera_x):
        screen_x = int(self.x - camera_x)
        
        if screen_x < -50 or screen_x > 850:
            return
            
        if not self.alive:
            cv2.ellipse(frame, (screen_x + self.width//2, int(self.y + self.height - 3)),
                       (self.width//2, 4), 0, 0, 360, (100, 50, 0), -1)
            return
        
        if self.type == 'goomba':
            body_color = (139, 69, 19)
            cv2.rectangle(frame, (screen_x, int(self.y)), 
                         (screen_x + self.width, int(self.y + self.height)), body_color, -1)
            cv2.circle(frame, (screen_x + 8, int(self.y + 10)), 3, (255, 255, 255), -1)
            cv2.circle(frame, (screen_x + 22, int(self.y + 10)), 3, (255, 255, 255), -1)
        
        elif self.type == 'koopa':
            shell_color = (0, 200, 0)
            cv2.ellipse(frame, (screen_x + self.width//2, int(self.y + self.height//2)),
                       (self.width//2, self.height//2), 0, 0, 360, shell_color, -1)

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.start_y = y
        self.width = 20
        self.height = 20
        self.collected = False
        self.spin_angle = 0
        self.float_offset = random.uniform(0, 6.28)
        
    def update(self):
        if not self.collected:
            self.spin_angle += 8
            self.float_offset += 0.08
            if self.spin_angle >= 360:
                self.spin_angle = 0
            
    def draw(self, frame, camera_x):
        if self.collected:
            return
            
        screen_x = int(self.x - camera_x)
        if screen_x < -30 or screen_x > 830:
            return
            
        float_y = self.start_y + np.sin(self.float_offset) * 3
        
        width_factor = abs(np.cos(np.radians(self.spin_angle)))
        coin_width = max(3, int(self.width * width_factor))
            
        cv2.ellipse(frame, (screen_x + self.width//2, int(float_y + self.height//2)),
                   (coin_width//2, self.height//2), 0, 0, 360, (0, 215, 255), -1)

class Flag:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 15
        self.height = 250
        self.flag_height = 60
        self.mario_reached = False
        
    def draw(self, frame, camera_x):
        screen_x = int(self.x - camera_x)
        
        if screen_x < -50 or screen_x > 850:
            return
        
        cv2.rectangle(frame, (screen_x, int(self.y)), 
                     (screen_x + 6, int(self.y + self.height)), (139, 69, 19), -1)
        
        flag_color = (0, 255, 0) if not self.mario_reached else (255, 215, 0)
        cv2.rectangle(frame, (screen_x + 6, int(self.y)), 
                     (screen_x + 6 + self.flag_height, int(self.y + 40)), flag_color, -1)
        
        if self.mario_reached:
            cv2.putText(frame, "VICTORY!", (screen_x - 60, int(self.y - 20)), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

class Game:
    def __init__(self):
        self.mario = Mario(100, 450)
        self.score = 0
        self.lives = 5  
        self.coins_collected = 0
        self.enemies_defeated = 0
        self.game_over = False
        self.level_complete = False
        self.particles = []
        self.camera_x = 0
        self.world_width = 4000  
        self.start_time = time.time()
        
        self.hand_controller = OptimizedHandController()
        self.gesture_cooldown = {'jump': 0, 'fireball': 0}
        
        self.create_easier_world()
        
    def create_easier_world(self):
        
        self.platforms = [
            (0, 550, 400, 20),        
            (450, 480, 120, 15),      
            (620, 420, 120, 15),      
            (780, 360, 100, 15),      
            
            (930, 300, 150, 15),      
            (1130, 250, 100, 15),     
            (1280, 200, 120, 15),     
            (1450, 280, 100, 15),     
            
            (1600, 350, 150, 15),     
            (1800, 300, 100, 15),     
            (1950, 250, 120, 15),     
            
            (2120, 320, 200, 15),     
            (2370, 280, 100, 15),     
            (2520, 240, 100, 15),     
            (2670, 200, 100, 15),     
            (2820, 160, 150, 15),     
            
            (400, 550, 300, 20),      
            (1550, 550, 300, 20),     
            (2100, 550, 200, 20),     
            (2800, 550, 200, 20),     
        ]
        
        self.enemies = [
            Enemy(480, 450, 'goomba'),
            Enemy(650, 390, 'goomba'),
            Enemy(960, 270, 'koopa'),
            Enemy(1160, 220, 'goomba'),
            Enemy(1630, 320, 'koopa'),
            Enemy(1980, 220, 'goomba'),
            Enemy(2150, 290, 'koopa'),
            Enemy(2400, 250, 'goomba'),
            Enemy(2700, 170, 'koopa'),
        ]
        
        self.coins = [
            Coin(320, 510), Coin(360, 510), Coin(500, 440),
            Coin(560, 440), Coin(660, 380), Coin(700, 380),
            Coin(820, 320), Coin(860, 320),
            
            Coin(980, 260), Coin(1020, 260), Coin(1060, 260),
            Coin(1170, 210), Coin(1210, 210),
            Coin(1320, 160), Coin(1360, 160),
            Coin(1490, 240), Coin(1530, 240),
            
            Coin(1640, 310), Coin(1680, 310), Coin(1720, 310),
            Coin(1840, 260), Coin(1880, 260),
            Coin(1990, 210), Coin(2030, 210),
            
            Coin(2160, 280), Coin(2200, 280), Coin(2240, 280), Coin(2280, 280),
            Coin(2410, 240), Coin(2450, 240),
            Coin(2560, 200), Coin(2600, 200),
            Coin(2710, 160), Coin(2750, 160),
            Coin(2860, 120), Coin(2900, 120), Coin(2940, 120),
        ]
        
        self.powerups = [
            PowerUp(540, 440, 'mushroom'),
            PowerUp(1000, 260, 'fire_flower'),
            PowerUp(1320, 160, 'star'),
            PowerUp(1680, 310, 'mushroom'),
            PowerUp(2200, 280, 'fire_flower'),
            PowerUp(2860, 120, 'star'),
        ]
        
        self.flag = Flag(3100, 120)
        
    def update(self, gestures, webcam_frame):
        if self.game_over or self.level_complete:
            return
        
        for key in self.gesture_cooldown:
            if self.gesture_cooldown[key] > 0:
                self.gesture_cooldown[key] -= 1
        
        if gestures['move_left']:
            self.mario.move_left()
        elif gestures['move_right']:
            self.mario.move_right()
        else:
            self.mario.stop_horizontal()
        
        if gestures['jump'] and self.gesture_cooldown['jump'] == 0:
            self.mario.jump()
            self.gesture_cooldown['jump'] = 10  
        
        if self.mario.jump_buffer > 0 and (self.mario.on_ground or self.mario.coyote_time > 0):
            self.mario.vel_y = self.mario.jump_strength
            self.mario.on_ground = False
            self.mario.coyote_time = 0
            self.mario.jump_buffer = 0
        
        self.mario.running = gestures['run']
        if gestures['run'] and self.mario.state == 'fire' and self.gesture_cooldown['fireball'] == 0:
            self.mario.shoot_fireball()
            self.gesture_cooldown['fireball'] = 20  
        
        mario_status = self.mario.update(self.platforms, self.particles)
        
        if mario_status == 'death':
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
            else:
                self.mario.reset_position()
                for _ in range(10):
                    self.particles.append(OptimizedParticle(
                        self.mario.x + self.mario.width//2,
                        self.mario.y + self.mario.height//2,
                        (255, 100, 100), 0, 0, 30
                    ))
        
        for enemy in self.enemies[:]:
            should_remove = enemy.update(self.platforms)
            if should_remove:
                self.enemies.remove(enemy)
        
        for coin in self.coins:
            coin.update()
        
        for powerup in self.powerups:
            powerup.update(self.platforms)
        
        for particle in self.particles[:]:
            particle.update()
            if particle.life <= 0:
                self.particles.remove(particle)
        
        if len(self.particles) > 50:
            self.particles = self.particles[-50:]
        
        self.check_collisions()
        
        target_camera_x = self.mario.x - 350
        self.camera_x += (target_camera_x - self.camera_x) * 0.1
        self.camera_x = max(0, min(self.camera_x, self.world_width - 800))
        
        if self.mario.x > self.flag.x and not self.flag.mario_reached:
            self.flag.mario_reached = True
            self.level_complete = True
            for _ in range(30):
                self.particles.append(OptimizedParticle(
                    self.flag.x + random.uniform(-30, 30),
                    self.flag.y + random.uniform(0, 80),
                    (255, 255, 0), 0, 0, 60
                ))
    
    def check_collisions(self):
        mario_rect = (self.mario.x, self.mario.y, self.mario.width, self.mario.height)
        
        for enemy in self.enemies:
            if not enemy.alive:
                continue
                
            enemy_rect = (enemy.x, enemy.y, enemy.width, enemy.height)
            if self.mario.check_collision(mario_rect, enemy_rect):
                if self.mario.vel_y > 0 and self.mario.y < enemy.y - 5:
                    enemy.kill()
                    self.mario.vel_y = -10  
                    self.score += 150 if enemy.type == 'koopa' else 100
                    self.enemies_defeated += 1
                    
                    for _ in range(8):
                        color = (0, 200, 0) if enemy.type == 'koopa' else (139, 69, 19)
                        self.particles.append(OptimizedParticle(
                            enemy.x + enemy.width//2, enemy.y + enemy.height//2,
                            color, 0, 0, 25
                        ))
                else:
                    if self.mario.take_damage():
                        self.lives -= 1
                        if self.lives <= 0:
                            self.game_over = True
                        else:
                            self.mario.reset_position()
        
        for fireball in self.mario.fireballs:
            if not fireball.active:
                continue
            fireball_rect = (fireball.x, fireball.y, fireball.width, fireball.height)
            
            for enemy in self.enemies:
                if not enemy.alive:
                    continue
                enemy_rect = (enemy.x, enemy.y, enemy.width, enemy.height)
                
                if fireball.check_collision(fireball_rect, enemy_rect):
                    enemy.kill()
                    fireball.active = False
                    self.score += 200
                    self.enemies_defeated += 1
                    
                    for _ in range(8):
                        self.particles.append(OptimizedParticle(
                            enemy.x + enemy.width//2, enemy.y + enemy.height//2,
                            (255, 150, 0), 0, 0, 30
                        ))
        
        for coin in self.coins:
            if coin.collected:
                continue
                
            coin_rect = (coin.x, coin.y, coin.width, coin.height)
            if self.mario.check_collision(mario_rect, coin_rect):
                coin.collected = True
                self.coins_collected += 1
                self.score += 200
                
                for _ in range(6):
                    self.particles.append(OptimizedParticle(
                        coin.x + coin.width//2, coin.y + coin.height//2,
                        (255, 215, 0), 0, -1, 20
                    ))
        
        for powerup in self.powerups:
            if powerup.collected:
                continue
                
            powerup_rect = (powerup.x, powerup.y, powerup.width, powerup.height)
            if self.mario.check_collision(mario_rect, powerup_rect):
                powerup.collected = True
                self.mario.power_up(powerup.type)
                
                bonus_score = 400 if powerup.type == 'star' else 300
                self.score += bonus_score
                
                colors = {
                    'mushroom': (255, 0, 0),
                    'fire_flower': (255, 165, 0),
                    'star': (255, 255, 0)
                }
                color = colors.get(powerup.type, (255, 255, 255))
                
                for _ in range(12):
                    self.particles.append(OptimizedParticle(
                        powerup.x + powerup.width//2, powerup.y + powerup.height//2,
                        color, 0, -1, 40
                    ))
    
    def draw(self, webcam_frame_input, webcam_with_landmarks):
        frame = np.zeros((600, 800, 3), dtype=np.uint8)
        
        progress = min(self.mario.x / self.world_width, 1.0)
        
        if progress < 0.5:
            sky_color = [135, 206, 235]  
        else:
            sky_color = [255, 165, 100]  
        
        frame[:] = sky_color
        
        self.draw_platforms(frame)
        
        for coin in self.coins:
            if not coin.collected:
                coin_x = coin.x - self.camera_x
                if -50 < coin_x < 850:
                    coin.draw(frame, self.camera_x)
            
        for powerup in self.powerups:
            if not powerup.collected:
                powerup_x = powerup.x - self.camera_x
                if -50 < powerup_x < 850:
                    powerup.draw(frame, self.camera_x)
        
        for enemy in self.enemies:
            enemy_x = enemy.x - self.camera_x
            if -50 < enemy_x < 850:
                enemy.draw(frame, self.camera_x)
        
        for particle in self.particles:
            particle_x = particle.x - self.camera_x
            if -20 < particle_x < 820:
                temp_particle = OptimizedParticle(particle_x, particle.y, particle.color)
                temp_particle.life = particle.life
                temp_particle.max_life = particle.max_life
                temp_particle.draw(frame)
        
        self.mario.draw(frame, self.camera_x)
        
        self.flag.draw(frame, self.camera_x)
        
        self.draw_ui(frame)
        
        return self.create_combined_display(frame, webcam_with_landmarks)
    
    def draw_platforms(self, frame):
        platform_color = (0, 150, 0)
        
        for platform in self.platforms:
            x1 = int(platform[0] - self.camera_x)
            y1 = int(platform[1])
            x2 = int(platform[0] + platform[2] - self.camera_x)
            y2 = int(platform[1] + platform[3])
            
            if x2 > -50 and x1 < 850:
                cv2.rectangle(frame, (max(-50, x1), y1), (min(850, x2), y2), platform_color, -1)
                cv2.rectangle(frame, (max(-50, x1), y1), (min(850, x2), y1 + 2), (0, 200, 0), -1)
    
    def create_combined_display(self, game_frame, webcam_frame):
        combined_frame = np.zeros((600, 1200, 3), dtype=np.uint8)
        combined_frame[:, :800] = game_frame
        
        try:
            if webcam_frame is not None and webcam_frame.size > 0:
                webcam_resized = cv2.resize(webcam_frame, (350, 260))
                h, w = webcam_resized.shape[:2]
                y_start, x_start = 60, 820
                y_end = min(y_start + h, 600)
                x_end = min(x_start + w, 1200)
                
                combined_frame[y_start:y_end, x_start:x_end] = webcam_resized[:y_end-y_start, :x_end-x_start]
                
                cv2.rectangle(combined_frame, (x_start-2, y_start-2), (x_end+2, y_end+2), (255, 255, 255), 2)
                cv2.putText(combined_frame, "Hand Control", (x_start, y_start-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        except:
            cv2.putText(combined_frame, "Camera Loading...", (830, 200), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
        
        instructions = [
            "HAND GESTURES:",
            "Left/Right - Move Mario",
            "3+ Fingers - JUMP (easier!)",
            "Closed Fist - RUN/SHOOT", 
            "",
            "REACH THE CASTLE!",
            "Collect coins & power-ups",
            "",
            "BACKUP KEYS:",
            "A/D-Move W-Jump S-Run",
            "Q-Quit R-Restart"
        ]
        
        for i, instruction in enumerate(instructions):
            if instruction:
                color = (255, 255, 0) if instruction.isupper() else (200, 200, 200)
                cv2.putText(combined_frame, instruction, (830, 350 + i * 18), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
        
        return combined_frame
    
    def draw_ui(self, frame):
        cv2.putText(frame, f"Score: {self.score:,}", (15, 35), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(frame, f"Lives: {self.lives}", (15, 65), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(frame, f"Coins: {self.coins_collected}", (15, 95), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        state_colors = {'small': (255, 255, 255), 'big': (0, 255, 0), 'fire': (255, 100, 0)}
        state_color = state_colors.get(self.mario.state, (255, 255, 255))
        cv2.putText(frame, f"Power: {self.mario.state.upper()}", (15, 125), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, state_color, 2)
        
        progress = min(self.mario.x / self.world_width, 1.0)
        bar_width = 250
        cv2.rectangle(frame, (500, 25), (500 + bar_width, 45), (100, 100, 100), -1)
        cv2.rectangle(frame, (500, 25), (int(500 + bar_width * progress), 45), (0, 255, 0), -1)
        cv2.putText(frame, f"Progress: {int(progress * 100)}%", (500, 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        if self.game_over:
            overlay = frame.copy()
            cv2.rectangle(overlay, (200, 220), (600, 380), (0, 0, 0), -1)
            cv2.addWeighted(frame, 0.8, overlay, 0.2, 0, frame)
            
            cv2.putText(frame, "GAME OVER", (280, 280), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 50, 50), 3)
            cv2.putText(frame, f"Score: {self.score:,}", (320, 320), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            cv2.putText(frame, "R-Restart  Q-Quit", (280, 350), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        elif self.level_complete:
            overlay = frame.copy()
            cv2.rectangle(overlay, (150, 180), (650, 420), (0, 100, 0), -1)
            cv2.addWeighted(frame, 0.8, overlay, 0.2, 0, frame)
            
            cv2.putText(frame, "VICTORY!", (280, 240), 
                       cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 3)
            cv2.putText(frame, f"Final Score: {self.score:,}", (280, 290), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
            
            completion_time = time.time() - self.start_time
            cv2.putText(frame, f"Time: {completion_time:.1f}s", (320, 330), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            cv2.putText(frame, f"Coins: {self.coins_collected}", (340, 360), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            cv2.putText(frame, "R-Restart  Q-Quit", (290, 390), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    def restart_game(self):
        self.mario = Mario(100, 450)
        self.score = 0
        self.lives = 5
        self.coins_collected = 0
        self.enemies_defeated = 0
        self.game_over = False
        self.level_complete = False
        self.particles = []
        self.camera_x = 0
        self.start_time = time.time()
        self.create_easier_world()

def main():
    print("🎮 Smooth Hand-Controlled Mario Game!")
    print("✨ IMPROVEMENTS:")
    print("   • Smoother hand detection with gesture smoothing")
    print("   • Easier controls (3+ fingers to jump)")
    print("   • Better jump mechanics with coyote time")
    print("   • Reduced lag with optimized rendering")
    print("   • More forgiving gameplay")
    print("   • Shorter, more focused level")
    print("\n📋 Controls:")
    print("   • Move hand LEFT/RIGHT to move Mario")
    print("   • Show 3+ fingers to JUMP")
    print("   • Make a fist to RUN/SHOOT")
    print("\n⌨️  Backup keyboard controls:")
    print("   • A/D - Move, W - Jump, S - Run/Shoot")
    print("   • Q - Quit, R - Restart")
    print("\nPress any key in the game window to start...")
    
    cap = None
    try:
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            cap.set(cv2.CAP_PROP_FPS, 30)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  
            print("📷 Camera initialized successfully!")
        else:
            cap = None
            print("⚠️  Camera not available - using keyboard mode")
    except Exception as e:
        cap = None
        print(f"⚠️  Camera error: {e} - using keyboard mode")
    
    game = Game()
    
    fps_counter = 0
    fps_timer = time.time()
    target_fps = 60
    frame_time = 1.0 / target_fps
    
    print("🚀 Game ready! Show your hand to camera and start playing!")
    
    try:
        while True:
            loop_start = time.time()
            
            gestures = {
                'move_left': False,
                'move_right': False, 
                'jump': False,
                'run': False
            }
            
            webcam_frame = None
            webcam_with_landmarks = None
            
            if cap is not None:
                try:
                    ret, webcam_frame = cap.read()
                    if ret and webcam_frame is not None:
                        webcam_frame = cv2.flip(webcam_frame, 1)
                        gestures, webcam_with_landmarks = game.hand_controller.detect_gestures(webcam_frame)
                    else:
                        webcam_with_landmarks = None
                except Exception as e:
                    webcam_with_landmarks = webcam_frame
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:
                break
            elif key == ord('r'):
                game.restart_game()
                continue
            elif key == ord('a'):
                gestures['move_left'] = True
            elif key == ord('d'):
                gestures['move_right'] = True
            elif key == ord('w'):
                gestures['jump'] = True
            elif key == ord('s'):
                gestures['run'] = True
            
            game.update(gestures, webcam_frame)
            
            display_frame = game.draw(webcam_frame, webcam_with_landmarks)
            
            fps_counter += 1
            if time.time() - fps_timer >= 1.0:
                actual_fps = fps_counter
                cv2.putText(display_frame, f"FPS: {actual_fps}", (700, 580), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                fps_counter = 0
                fps_timer = time.time()
            
            cv2.imshow('Smooth Mario Adventure', display_frame)
            
            loop_time = time.time() - loop_start
            if loop_time < frame_time:
                time.sleep(frame_time - loop_time)
    
    except KeyboardInterrupt:
        print("\n🛑 Game interrupted by user")
    except Exception as e:
        print(f"\n❌ Game error: {e}")
    finally:
        if cap is not None:
            cap.release()
        cv2.destroyAllWindows()
        
        print("🎯 Game Statistics:")
        print(f"   Final Score: {game.score:,}")
        print(f"   Coins Collected: {game.coins_collected}")
        print(f"   Enemies Defeated: {game.enemies_defeated}")
        if game.level_complete:
            completion_time = time.time() - game.start_time
            print(f"   Completion Time: {completion_time:.1f}s")
            print("🏆 CONGRATULATIONS! You completed the adventure!")
        
        print("👋 Thanks for playing Smooth Mario Adventure!")

if __name__ == "__main__":
    main()