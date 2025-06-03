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
topcarX = 0
umcarX = 0
lmcarX = 0
bottomcarX = 0
newtopX = 0
newumX = 0
newlmX = 0
newbottomX = 0
#Constants
scrnX = 1280
scrnY = 300
fps = 60
print("2.1.1, non-lane constants")
#lanes/barriers (still constants)
topbarrier = [0, 1820, 0, 20]
bottombarrier = [0, 1280, 280, 300]
divider1 = [0, 1280, 70, 90]
divider2 = [0, 1270, 140, 160]
divider3 = [0, 1280, 210, 230]
print("2.1.2, lane constants")
#Initial values
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
#The car hitboxes
car1 = [1210, 1280, 23, 67]
car2 = [1210, 1280, 93, 137]
car3 = [1210, 1280, 163, 207]
car4 = [1210, 1280, 233, 277]


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
        pg.draw.polygon(screen, colour, ((self.coords[0], self.coords[2]), (self.coords[1], self.coords[2]), \
            (self.coords[1], self.coords[3]), (self.coords[0], self.coords[3])))

upperbarrier = Objects(topbarrier)
lowerbarrier = Objects(bottombarrier)
line1 = Objects(divider1)
line2 = Objects(divider2)
line3 = Objects(divider3)
topcar = Objects(car1)
umcar = Objects(car2)
lmcar = Objects(car3)
bottomcar = Objects(car4)

barriers = [upperbarrier, lowerbarrier]
roadlines = [line1, line2, line3]
cars = [topcar, umcar, lmcar, bottomcar]


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


    car1[0] -= (speedmod * 2)
    car1[1] -= (speedmod *2)
    print(car1[0], car1[1])
    if car1[1] <= 0:
        car1[0] = 1280
        car1[1] = 1350

    clock.tick(fps)
    pg.display.update()