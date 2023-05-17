import sys
import pygame as py
import time
import random

width = 640
height = 320
window = py.display.set_mode((width, height))
py.display.set_caption("Snake Game")
clock = py.time.Clock()

score = 0

#Initializing pygame
init_status = py.init()
if init_status[1] > 0:
    print("(!) Had {0} initialising errors, exiting... ".format(init_status[1]))
    sys.exit()
else:
    print("(+) Pygame initialised successfully ")

class Snake():
    def __init__(self):
        self.position = [100,50]
        self.body = [[100,50],[90,50],[80,50],[70,50]]
        self.direction = "RIGHT"
        self.changeDirectionTo = self.direction

    # Make sure that snake cannot change direction directly from
    # left to right, right to left, up to down, or down to up
    def changeDirTo(self, dir):
        if dir=="RIGHT" and self.direction!="LEFT":
            self.direction = "RIGHT"
        if dir=="LEFT" and self.direction!="RIGHT":
            self.direction = "LEFT"
        if dir=="UP" and self.direction!="DOWN":
            self.direction = "UP"
        if dir=="DOWN" and self.direction!="UP":
            self.direction = "DOWN"

    # Snake can move either right, left, up, or down the board
    def move(self,foodPos):
        if self.direction == "RIGHT":
            self.position[0] += 10
        if self.direction == "LEFT":
            self.position[0] -= 10
        if self.direction == "UP":
            self.position[1] -= 10
        if self.direction == "DOWN":
            self.position[1] += 10
        self.body.insert(0,list(self.position))
        if self.position == foodPos:
            return True
        else:
            self.body.pop()
            return False

    # Collide if snake's head hit the walls
    # at the edge of the screen or hit its body
    def checkCollision(self):
        if self.position[0] > width - 10 or self.position[0] < 0 or self.position[1] > height - 10 or self.position[1] < 0:
            return True
        for bodyPart in self.body[1:]:
            if self.position == bodyPart:
                return True
        return False

class FoodSpawner():
    def __init__(self):
        self.position = [random.randrange(1,width/10)*10, random.randrange(1,height/10)*10]
        self.isFoodOnScreen = True

    # Spawn food randomly on the board if no food is present
    def spawnFood(self):
        if self.isFoodOnScreen == False:
            self.position = [random.randrange(1,width/10)*10, random.randrange(1,height/10)*10]
            self.isFoodOnScreen = True
        return self.position

snake = Snake()
foodSpawner = FoodSpawner()

# Display message when game is over
def gameOver():
    myFont = py.font.SysFont('monaco', 72)
    GOsurf = myFont.render("Game Over", True, py.Color(255,0,0))
    GOrect = GOsurf.get_rect()
    GOrect.midtop = (height, 25)
    window.blit(GOsurf, GOrect)
    py.display.flip()
    time.sleep(4)

while True:
    for event in py.event.get():
        if event.type == py.QUIT:
            gameOver()
        elif event.type == py.KEYDOWN:
            if event.key == py.K_RIGHT:
                snake.changeDirTo("RIGHT")
            if event.key == py.K_LEFT:
                snake.changeDirTo("LEFT")
            if event.key == py.K_UP:
                snake.changeDirTo("UP")
            if event.key == py.K_DOWN:
                snake.changeDirTo("DOWN")
    foodPos = foodSpawner.spawnFood()
    if(snake.move(foodPos)==True):
        score+=1
        foodSpawner.isFoodOnScreen = False

    window.fill(py.Color(87, 65, 47))
    for pos in snake.body:
        py.draw.rect(window,py.Color(50,205,50), py.Rect(pos[0],pos[1],10, 10))
    py.draw.rect(window,py.Color(255,255,0), py.Rect(foodPos[0],foodPos[1],10, 10))
    if(snake.checkCollision()==True):
       gameOver()
    py.display.set_caption("Snake Game | Score : " + str(score))
    py.display.flip()
    clock.tick(10)
