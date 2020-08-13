#Snake Python

import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

# 2 main objects, cube and snake, the snake object (the whole grid) will contain each cube object
class cube(object):
    rows = 20
    w = 500
    def __init__(self, start, dirnx=1, dirny=0, colour=(255,0,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.colour = colour
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
    def draw(self, surface, eyes=False):
        # cube size
        dis = self.w // self.rows
        i = self.pos[0]
        j= self.pos[1]
        # draw cubes
        pygame.draw.rect(surface, self.colour, (i * dis+1, j * dis+1, dis-2, dis-2))
        # draw eyes on head
        if eyes:
            centre = dis // 2
            radius = 3
            circleMiddle = (i *dis+centre-radius, j*dis+8)
            circleMiddle2 = (i*dis + dis - radius*2, j*dis +8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)
class snake(object):
    # creating a class variable, the body will contain a list of cube
    body = []
    turns = {} # reuired to remember the postion of where a move was made
    
    def __init__(self, colour, pos):
        self.colour = colour
        self.head = cube(pos)
        self.body.append(self.head)
        # give a sense of direction, can only move in one direction at one time
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
            
            keys = pygame.key.get_pressed() # gives all keys in a dictonary

            for key in keys:
                if  keys[pygame.K_LEFT]:

                    self.dirnx = -1
                    self.dirny = 0
                    # this will add a new key to the dictionary giving the position where the snake head turned
                    self. turns[self.head.pos[ : ]] = [self.dirnx, self.dirny]
                    
                elif  keys[pygame.K_RIGHT]:

                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[ : ]] = [self.dirnx, self.dirny]
                    
                elif  keys[pygame.K_UP]:

                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[ : ]] = [self.dirnx, self.dirny]

                elif  keys[pygame.K_DOWN]:

                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[ : ]] = [self.dirnx, self.dirny]
        # ensuring rest of body turns at the postion using dictionary
        # first get index, i and cube object c in the snake body
        #all these cube objects have a postion, we check if the postion is in the turns list
        for i, c in enumerate(self.body):
            p = c.pos[ : ]
            if p in self.turns:
                 turn = self.turns[p]
                 # c.move is a method in the cube class requres the the dirnx and dirny postion from turn dictionary
                 c.move(turn[0], turn[1])
                 # what we are doing here is if it is the last cube we are going to then remove that key value pair fromt eh dictionary
                 if i == len(self.body) - 1:
                     self.turns.pop(p)
            # now if the cube is not at that postioon still need to allow it to move straight, must ensure when it reaches an edge it goes to the other side of the screen
            else:
              # if we are going left and reach the left edge, it must pass through to the right side, pos[1] is constant only x postion changes
                 if c.dirnx == -1 and c.pos[0] <= 0:
                     c.pos = (c.rows-1, c.pos[1])
                 # similarly if we going right, up or down
                 elif c.dirnx == 1 and c.pos[0] >= c.rows-1:
                     c.pos = (0, c.pos[1])
                 elif c.dirny == 1 and c.pos[1] >= c.rows-1:
                     c.pos = (c.pos[0], 0)
                 elif c.dirny == -1 and c.pos[1] <= 0:
                     c.pos = (c.pos[0], c.rows-1)
                 # if no edge being hit can move normally
                 else:
                     c.move(c.dirnx, c.dirny)
    def reset(self, pos):
        global score_value
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self): # add new cube to the head of body, must ensure it moves in same direction as head
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0: # moving right
            self.body.append(cube((tail.pos[0]-1, tail.pos[1]))) #want it to add one behind to the left to the one in front at the same y level
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            # will give the head eyes
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)
            
            
# need draw the grid
def drawGrid(w, rows, surface):
    # when drwaing grid need to first think about the size of square
    sizeBtwn = w // rows

    x= 0
    y=0
    for l in range(rows):
        x += sizeBtwn
        y += sizeBtwn

        # drawn line each time, this draws two lines every loop, th window, colour, start and end postion of the line
        pygame.draw.line(surface, (255, 255, 255), (x,0), (x,w))# vertical line
        pygame.draw.line(surface, (255, 255, 255), (0,y), (w,y))# horizontal line
# need to update window with grid drawn and fill screen black
def redrawWindow(surface):
    global width, rows, s, snack
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    # calls drawGrid function
    drawGrid(width, rows, surface)
    pygame.display.update()

def randomSnack(rows, items): # items is gonna be our snake object parameter function takes the postions and ensure the random snack doesnt collide on the the nsake 
    postions = items.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), postions))) > 0:
            continue
        else:
            break
    return (x,y)

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass
    
# main loop
def main():
    # make these varible accessible in this function without having to call it
    global width, rows, s, snack
    score_value = 0
    # first make a surface
    width = 500
    # set rows make sure it is divisible by 500, number of rows make game harder or easier
    rows = 20
    win = pygame.display.set_mode((width, width))
    # set up snake object, parameters: colour and row postion
    s = snake((255, 0, 0), (10,10))
    # create a new cube object that will be the snack
    snack = cube(randomSnack(rows, s), colour = (0, 255, 0))
    flag = True
    # intialise the clock variable
    clock = pygame.time.Clock()
    while flag:
        
        # create a pygame dely each time program runs, delayed by 50 ms to ensure program dont run too fast, sorts out the movement
        # both clock and .delay are inversely propotional, lower the delay is faster it runs, lower clock is slower it runs
        pygame.time.delay(80)
        # this ensures game doesnt run faster then 10 frames per second
        clock.tick(10)

        # allow movement call snake move method
        s.move()
        if s.body[0].pos == snack.pos:
            score_value += 1
            s.addCube()
            snack = cube(randomSnack(rows, s), colour = (0, 255, 0))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1: ])):
                with open("score_log.txt", "r") as file:
                    top_score = int(file.readline())
                if score_value > top_score:
                    adf = score_value  
                    top_score = adf
                    with open("score_log.txt", "w") as file:
                      file.write(str(top_score))
                message_box("You Lost!", "Your score was {}\nThe High Score is {}\nPlay Again...".format(score_value, top_score))
                score_value = 0
                s.reset((10, 10))
                break 
                

        # calls redrawWindow function
        redrawWindow(win)
main()
