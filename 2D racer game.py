#Setting up the absolute baseline: imports, initialisation, the game display
import pygame as pg
import math as mths
import json
import time
import easygui as box
pg.init()
print("1")


#Setups
#Base variable values to prevent breaking
speedmod = 1
name = "Johnus"
quitgame = False
road = None
#Constants
scrnX = 1280
scrnY = 300
fps = 60
print("2.1.1, non-lane constants")
#lanes/barriers (still constants)
topbarrier = [(0,0), (1280, 0), (1280, 20), (0, 20)]
bottombarrier = [(0, 280), (1280, 280), (1280, 300), (0, 300)]
divider1 = [(0,70), (1280,70), (1280,90), (0,90)]
divider2 = [(0,140), (1280,140), (1280,160), (0,160)]
divider3 = [(0,210), (1280,210), (1280,230), (0,230)]
print("2.1.2, lane constants")
#Car initial values
topcar = [(1210,23), (1280, 23), (1280, 67), (1210, 67)]
umcar = [(1210,93), (1280, 93), (1280, 137), (1210, 137)]
lmcar = [(1210,163), (1280, 163), (1280, 207), (1210, 207)]
bottomcar = [(1210,233), (1280, 233), (1280, 277), (1210, 277)]
#The screen display
screen = pg.display.set_mode((scrnX, scrnY),pg.RESIZABLE)
print("2.2, screen display")
#The clock for counting the fps
clock = pg.time.Clock()
print("2.3, clock")
#The external display (image, game name)
gameicon = pg.image.load('amogusicon.png')
pg.display.set_icon(gameicon)
pg.display.set_caption("It's like a real freeway")
print("2.4, displayed info")


#Road themes
roadcolours = {
    "day":{"car":(190, 66, 72), "lane":(30, 30, 30), "barrier":(200, 200, 200), "lines":(255, 255, 255)},
    "night":{"car":(63, 22, 23), "lane":(15, 15, 15), "barrier":(30, 30, 30), "lines":(50, 50, 50)},
    "fog":{"car":(42, 15, 16), "lane":(20, 15, 10), "barrier":(75, 50, 20), "lines":(255, 255, 255)},
    "jank":{"car":(255, 100, 100), "lane":(0, 0, 0), "barrier":(0, 255, 200), "lines":(255, 0, 255)}
}


#Setting up the class for displaying the lanes and the lines on the road.
class Objects:
    def __init__(self, coords):
        self.coords = coords

    def drawobjects(self, coords, colour):
        pg.draw.polygon(screen, colour, self.coords)

upperbarrier = Objects(topbarrier)
lowerbarrier = Objects(bottombarrier)
line1 = Objects(divider1)
line2 = Objects(divider2)
line3 = Objects(divider3)
car1 = Objects(topcar)
car2 = Objects(umcar)
car3 = Objects(lmcar)
car4 = Objects(bottomcar)

barriers=[upperbarrier, lowerbarrier]
roadlines=[line1, line2, line3]
cars = [car1, car2, car3, car4]


#Difficulty and theme selection using pygame
name = box.enterbox(msg="What is your name?", title="player name selection")
diff = box.choicebox(msg="Please pick your preferred difficulty (higher difficulties gain more points)",\
    title="Difficulty selection", choices=["easy", "medium", "hard"])
print("4.1, name, choices, colour")
#Difficulty selection
if diff == "easy":
    speedmod = (2/3)
elif diff == "medium":
    speedmod = 1   
elif diff == "hard":
    speedmod = 1.5
print("4.2, difficulty chosen")

#Setting the theme based on selections
if diff == "hard" and name == "Sully":
    theme = roadcolours["jank"]
else:
    conditions = box.choicebox(msg="What driving conditions do you want to try?", title="road selection",\
    choices=["daytime", "nighttime", "foggy"])
    if conditions == "daytime":
        theme = roadcolours["day"]
    elif conditions == "nighttime":
        theme = roadcolours["night"]
    elif conditions == "foggy":
        theme = roadcolours["fog"]
print("4.3, theme set")


#The game loop
while not quitgame:
    #detecting inputs
    for event in pg.event.get():
        if event.type == pg.QUIT:
            quitgame = True

    #Displaying the screen, road lanes, barriers
    screen.fill(theme["lane"])

    for x in barriers:
        x.drawobjects(screen, colour=(theme["barrier"]))
    for x in roadlines:
        x.drawobjects(screen, colour=(theme["lines"]))
    for x in cars:
        x.drawobjects(screen, colour=(theme["car"]))

    pg.display.update()

    clock.tick(fps)