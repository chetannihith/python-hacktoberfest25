

import tkinter as tk
import random

# Game constants
WIDTH = 400
HEIGHT = 600
BIRD_SIZE = 20
PIPE_WIDTH = 60
GAP_HEIGHT = 150
GRAVITY = 3
FLAP_STRENGTH = -8
DELAY = 30

class FlappyBird:
    def __init__(self, master):
        self.master = master
        self.master.title("Flappy Bird Clone")
        self.canvas = tk.Canvas(master, width=WIDTH, height=HEIGHT, bg="skyblue")
        self.canvas.pack()
        
        # Bird properties
        self.bird_x = 100
        self.bird_y = HEIGHT//2
        self.bird_velocity = 0
        
        # Pipes: list of [x, top_height, bottom_height]
        self.pipes = []
        self.score = 0
        self.running = True
        
        self.canvas.bind("<space>", self.flap)
        self.spawn_pipe()
        self.update()
    
    def flap(self, event):
        if self.running:
            self.bird_velocity = FLAP_STRENGTH
    
    def spawn_pipe(self):
        top_height = random.randint(50, HEIGHT - GAP_HEIGHT - 50)
        bottom_height = HEIGHT - GAP_HEIGHT - top_height
        pipe_x = WIDTH
        self.pipes.append([pipe_x, top_height, bottom_height])
    
    def move_pipes(self):
        for pipe in self.pipes:
            pipe[0] -= 5
        # Remove off-screen pipes
        if self.pipes and self.pipes[0][0] + PIPE_WIDTH < 0:
            self.pipes.pop(0)
            self.score += 1
        # Spawn new pipe
        if self.pipes[-1][0] < WIDTH - 200:
            self.spawn_pipe()
    
    def check_collision(self):
        if self.bird_y < 0 or self.bird_y + BIRD_SIZE > HEIGHT:
            return True
        for pipe in self.pipes:
            px, top, bottom = pipe
            if self.bird_x + BIRD_SIZE > px and self.bird_x < px + PIPE_WIDTH:
                if self.bird_y < top or self.bird_y + BIRD_SIZE > HEIGHT - bottom:
                    return True
        return False
    
    def draw(self):
        self.canvas.delete("all")
        # Draw bird
        self.canvas.create_oval(self.bird_x, self.bird_y, 
                                self.bird_x + BIRD_SIZE, self.bird_y + BIRD_SIZE,
                                fill="yellow")
        # Draw pipes
        for pipe in self.pipes:
            px, top, bottom = pipe
            self.canvas.create_rectangle(px, 0, px + PIPE_WIDTH, top, fill="green")
            self.canvas.create_rectangle(px, HEIGHT - bottom, px + PIPE_WIDTH, HEIGHT, fill="green")
        # Draw score
        self.canvas.create_text(WIDTH//2, 30, text=f"Score: {self.score}", font=("Arial", 20), fill="white")
    
    def update(self):
        if self.running:
            self.bird_velocity += GRAVITY
            self.bird_y += self.bird_velocity
            self.move_pipes()
            if self.check_collision():
                self.running = False
                self.canvas.create_text(WIDTH//2, HEIGHT//2, text="Game Over!", font=("Arial", 32), fill="red")
            self.draw()
            self.master.after(DELAY, self.update)

if __name__ == "__main__":
    root = tk.Tk()
    game = FlappyBird(root)
    root.mainloop()
