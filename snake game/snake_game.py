# main.py

import tkinter as tk
import random

# Game constants
WIDTH = 400
HEIGHT = 400
SIZE = 20
DELAY = 100

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        self.canvas = tk.Canvas(master, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()
        
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = "Right"
        self.food = None
        self.running = True
        
        self.score = 0
        
        self.create_food()
        self.draw_snake()
        
        self.master.bind("<KeyPress>", self.change_direction)
        self.update()
        
    def create_food(self):
        while True:
            x = random.randint(0, (WIDTH-SIZE)//SIZE) * SIZE
            y = random.randint(0, (HEIGHT-SIZE)//SIZE) * SIZE
            if (x, y) not in self.snake:
                self.food = (x, y)
                break
        self.canvas.create_rectangle(x, y, x+SIZE, y+SIZE, fill="red", tag="food")
    
    def draw_snake(self):
        self.canvas.delete("snake")
        for x, y in self.snake:
            self.canvas.create_rectangle(x, y, x+SIZE, y+SIZE, fill="green", tag="snake")
    
    def change_direction(self, event):
        key = event.keysym
        if key == "Up" and self.direction != "Down":
            self.direction = "Up"
        elif key == "Down" and self.direction != "Up":
            self.direction = "Down"
        elif key == "Left" and self.direction != "Right":
            self.direction = "Left"
        elif key == "Right" and self.direction != "Left":
            self.direction = "Right"
    
    def move_snake(self):
        head_x, head_y = self.snake[0]
        if self.direction == "Up":
            head_y -= SIZE
        elif self.direction == "Down":
            head_y += SIZE
        elif self.direction == "Left":
            head_x -= SIZE
        elif self.direction == "Right":
            head_x += SIZE
        
        new_head = (head_x, head_y)
        
        # Check collisions
        if (head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT or new_head in self.snake):
            self.running = False
            self.canvas.create_text(WIDTH//2, HEIGHT//2, text="Game Over!", fill="white", font=("Arial", 24))
            return
        
        self.snake = [new_head] + self.snake
        if new_head == self.food:
            self.score += 1
            self.canvas.delete("food")
            self.create_food()
        else:
            self.snake.pop()
    
    def update(self):
        if self.running:
            self.move_snake()
            self.draw_snake()
            self.master.after(DELAY, self.update)

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
