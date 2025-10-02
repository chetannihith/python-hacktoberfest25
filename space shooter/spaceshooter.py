# main.py

import tkinter as tk
import random

# Game constants
WIDTH = 400
HEIGHT = 600
SHIP_WIDTH = 40
SHIP_HEIGHT = 20
BULLET_WIDTH = 5
BULLET_HEIGHT = 10
ENEMY_WIDTH = 40
ENEMY_HEIGHT = 20
BULLET_SPEED = 10
ENEMY_SPEED = 5
DELAY = 30

class SpaceShooter:
    def __init__(self, master):
        self.master = master
        self.master.title("Space Shooter")
        self.canvas = tk.Canvas(master, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()
        
        # Player ship
        self.ship_x = WIDTH//2 - SHIP_WIDTH//2
        self.ship_y = HEIGHT - SHIP_HEIGHT - 10
        
        # Bullets and enemies
        self.bullets = []
        self.enemies = []
        self.score = 0
        self.running = True
        
        self.master.bind("<Left>", self.move_left)
        self.master.bind("<Right>", self.move_right)
        self.master.bind("<space>", self.shoot)
        
        self.spawn_enemy()
        self.update()
    
    def move_left(self, event):
        if self.ship_x - 10 >= 0:
            self.ship_x -= 10
    
    def move_right(self, event):
        if self.ship_x + SHIP_WIDTH + 10 <= WIDTH:
            self.ship_x += 10
    
    def shoot(self, event):
        self.bullets.append([self.ship_x + SHIP_WIDTH//2 - BULLET_WIDTH//2, self.ship_y])
    
    def spawn_enemy(self):
        x = random.randint(0, WIDTH - ENEMY_WIDTH)
        self.enemies.append([x, 0])
    
    def move_bullets(self):
        for bullet in self.bullets:
            bullet[1] -= BULLET_SPEED
        # Remove bullets that go off-screen
        self.bullets = [b for b in self.bullets if b[1] > 0]
    
    def move_enemies(self):
        for enemy in self.enemies:
            enemy[1] += ENEMY_SPEED
        # Remove enemies that go off-screen
        self.enemies = [e for e in self.enemies if e[1] < HEIGHT]
        # Spawn new enemy randomly
        if random.randint(0, 20) == 0:
            self.spawn_enemy()
    
    def check_collision(self):
        for bullet in self.bullets:
            for enemy in self.enemies:
                if (bullet[0] < enemy[0] + ENEMY_WIDTH and
                    bullet[0] + BULLET_WIDTH > enemy[0] and
                    bullet[1] < enemy[1] + ENEMY_HEIGHT and
                    bullet[1] + BULLET_HEIGHT > enemy[1]):
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.score += 1
                    return
    
    def draw(self):
        self.canvas.delete("all")
        # Draw ship
        self.canvas.create_rectangle(self.ship_x, self.ship_y, 
                                     self.ship_x + SHIP_WIDTH, self.ship_y + SHIP_HEIGHT, fill="blue")
        # Draw bullets
        for b in self.bullets:
            self.canvas.create_rectangle(b[0], b[1], b[0] + BULLET_WIDTH, b[1] + BULLET_HEIGHT, fill="yellow")
        # Draw enemies
        for e in self.enemies:
            self.canvas.create_rectangle(e[0], e[1], e[0] + ENEMY_WIDTH, e[1] + ENEMY_HEIGHT, fill="red")
        # Draw score
        self.canvas.create_text(50, 20, text=f"Score: {self.score}", font=("Arial", 16), fill="white")
    
    def update(self):
        if self.running:
            self.move_bullets()
            self.move_enemies()
            self.check_collision()
            # Check collision with player
            for e in self.enemies:
                if (e[0] < self.ship_x + SHIP_WIDTH and e[0] + ENEMY_WIDTH > self.ship_x and
                    e[1] + ENEMY_HEIGHT > self.ship_y):
                    self.running = False
                    self.canvas.create_text(WIDTH//2, HEIGHT//2, text="Game Over!", font=("Arial", 32), fill="red")
            self.draw()
            self.master.after(DELAY, self.update)

if __name__ == "__main__":
    root = tk.Tk()
    game = SpaceShooter(root)
    root.mainloop()
