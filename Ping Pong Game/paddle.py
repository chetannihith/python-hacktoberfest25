from turtle import Turtle

PADDLE_COLOR = "black"
PADDLE_SHAPE = "square"
PADDLE_WIDTH = 5
PADDLE_LENGTH = 1
MOVE_DISTANCE = 20
UPPER_LIMIT = 250
LOWER_LIMIT = -250

class Paddle(Turtle):
    
    def __init__(self, position):
        super().__init__()
        self.shape(PADDLE_SHAPE)
        self.color(PADDLE_COLOR)
        self.shapesize(stretch_wid=PADDLE_WIDTH, stretch_len=PADDLE_LENGTH)
        self.penup()
        self.goto(position)

    def go_up(self):
        if self.ycor() <= UPPER_LIMIT:
            new_y = self.ycor() + MOVE_DISTANCE
            self.goto(self.xcor(), new_y)

    def go_down(self):
        if self.ycor() >= LOWER_LIMIT:
            new_y = self.ycor() - MOVE_DISTANCE
            self.goto(self.xcor(), new_y)
