#Setting up the absolute baseline: imports, initialisation, the game display
import pygame as pg
import math as mths
import json
import time
import easygui as box
import random as rndm
pg.init()
print("1")

#Constants
scrnX = 1280
scrnY = 350
fps = 60
moveleft = False
moveright = False
movedown = False
moveup = False
print("2.1, non-lane constants")
#The screen display
screen = pg.display.set_mode((scrnX, scrnY),pg.RESIZABLE)
print("2.2, screen display")
#lanes/barriers (constants)
topbarrier = [0, 1820, 0, 20]
bottombarrier = [0, 1280, 280, 300]
#Road lane dividers
divider1 = [0, 1280, 75, 85]
divider2 = [0, 1280, 145, 155]
divider3 = [0, 1280, 215, 225]
#Imitates movement on the road
moveline1 = [0, 128, 70, 230]
moveline2 = [256, 384, 70, 230]
moveline3 = [512, 640, 70, 230]
moveline4 = [768, 896, 70, 230]
moveline5 = [1024, 1152, 70, 230]
print("2.3, lane constants")
#The clock for counting the fps
clock = pg.time.Clock()
print("2.4, clock")
#The external display (image, game name)
gameicon = pg.image.load('amogusicon.png')
pg.display.set_icon(gameicon)
pg.display.set_caption("It's like a real freeway")
print("2.5, displayed info")
#Road themes
roadcolours = {
    "day":{"car":(255, 255, 0), "lane":(30, 30, 30), "barrier":(200, 200, 200), "lines":(255, 255, 255)},
    "night":{"car":(255, 255, 0), "lane":(15, 15, 15), "barrier":(30, 30, 30), "lines":(50, 50, 50)},
    "fog":{"car":(255, 255, 0), "lane":(20, 15, 10), "barrier":(25, 25, 25), "lines":(255, 255, 255)},
    "jank":{"car":(255, 255, 0), "lane":(0, 0, 0), "barrier":(0, 255, 200), "lines":(255, 0, 255)}
}
print("2.6, colour themes")
#Player name and score
score = ["Johnus", "difficulty", 0]
print("2.7, default player score")


#Variables
#Base variable values
speedmod = 1 #Default speed
name = "Johnus" #Default name
theme = roadcolours["day"] #Default theme
highscore = ["Johnus", "easy", 0] #Default highscore
quitgame = False
debug = False
Xcoll = False
Ycoll = False
crash = False
drawboxes = False
print("3.1, initial variables")
#The car hitboxes
cartop1 = [1210, 1280, 23, 67, 'redcar.png']
cartop2 = [1850, 1920, 23, 67, 'greencar.png']
car2 = [1210, 1280, 93, 137, 'bluecar.png']
car3 = [1210, 1280, 163, 207, 'orangecar.png']
car4 = [1210, 1280, 233, 277, 'tealcar.png']
pcar = [10, 80, 23, 67, 'playercar.png']
print("3.2, the cars' hitboxes' initial values")
#Displaying the actual car pngs
displaycars = ['redcar.png', 'greencar.png', 'tealcar.png', 'purpcar.png', 'orangecar.png']
print("3.3, the cars' png display options")
#The font
font = pg.font.SysFont("arial.ttf", 50)
print("3.4, font loaded")


#The function for saving the player's score
def save(thing, file):
    with open (file, "w") as file:
        json.dump(thing, file, indent=4)
    print("saving")

#The function for loading the player's score
def load(thing, file):
    with open (file, "r") as file:
        highscore = json.load(file)
    return highscore
    print(highscore)
    print("loaded")

#The function for displaying text
def message(msg, txt_colour, bkgd_colour, txtX, txtY):
    txt = font.render(msg, True, txt_colour, bkgd_colour)
    textbox=txt.get_rect(center = (txtX, txtY))
    screen.blit(txt, textbox)

#The class for displaying the lanes and the lines on the road.
class Objects:
    
    #Initialises the class
    def __init__(self, coords):
        self.coords = coords

    #Draws the cars' hitboxes
    def drawobjects(self, coords, colour, type):
        if type == "vehicle" and drawboxes == False:
            poly = pg.Rect((self.coords[0]), (self.coords[2]), 70, 44)
            #print(self.coords[4])
            rawcar = pg.image.load(self.coords[4]).convert_alpha()
            sizedcar = pg.transform.smoothscale(rawcar, [70, 44])
            screen.blit(sizedcar, poly)
        elif drawboxes == True or type != "vehicle":
            pg.draw.polygon(screen, colour, ((self.coords[0], self.coords[2]), (self.coords[1], self.coords[2]), \
            (self.coords[1], self.coords[3]), (self.coords[0], self.coords[3])))

    def carchange(self, coords):
        if self.coords[0] > 1280 and self.coords[0] < 1300:
            rancar = rndm.choice(displaycars)
            self.coords[4] = rancar
            print(self.coords[4])
   
    #Collision detection
    def collcheck(self, coords):
        global quitgame
        Xcoll = False
        Ycoll = False
        crash = False
        if pcar[0] >= self.coords[0] and pcar[0] <= self.coords[1]:
            Xcoll = True
        elif pcar[1] >= self.coords[0] and pcar[1] <= self.coords[0]:
            Xcoll = True
        #Y collision
        if pcar[2] >= self.coords[2] and pcar[2] <= self.coords[3]:
            Ycoll = True
        elif pcar[3] >= self.coords[2] and pcar[3] <= self.coords[3]:
            Ycoll = True
        if Xcoll == True and Ycoll == True:
            print("Full collision")
            quitgame = True
        elif Xcoll == True:
            print("X collision")
            score[2] += (speedmod * 2)
        #elif Ycoll == True:
            print("Y collision")
        

#Allowing the variables for the cars, lanes, barriers, to be read as Objects
upperbarrier = Objects(topbarrier)
lowerbarrier = Objects(bottombarrier)
line1 = Objects(divider1)
line2 = Objects(divider2)
line3 = Objects(divider3)
topcar1 = Objects(cartop1)
topcar2 = Objects(cartop2)
umcar = Objects(car2)
lmcar = Objects(car3)
bottomcar = Objects(car4)
playercar = Objects(pcar)
movelineA = Objects(moveline1)
movelineB = Objects(moveline2)
movelineC = Objects(moveline3)
movelineD = Objects(moveline4)
movelineE = Objects(moveline5)
#Grouping the objects to have them separate for drawing/collision checking
barriers = [upperbarrier, lowerbarrier]
roadlines = [line1, line2, line3]
cars = [topcar1, topcar2, umcar, lmcar, bottomcar]
player = [playercar]
moveillusion = [movelineA, movelineB, movelineC, movelineD, movelineE]


#Difficulty and theme selection using easygui
name = box.enterbox(msg="What is your name?", title="player name selection")
score[0] = name
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
score[1] = diff
print("4.2, difficulty chosen")

#Setting the theme based on selected theme
#"Sully" with "Hard" sets the debug mode
if diff == "hard" and name == "Sully":
    theme = roadcolours["jank"]
    debug = True
else:
    conditions = box.choicebox(msg="What driving conditions do you want to try?", title="road selection",\
    choices=["daytime", "nighttime", "foggy"])
    if conditions == "daytime":
        theme = roadcolours["day"]
    elif conditions == "nighttime":
        theme = roadcolours["night"]
    elif conditions == "foggy":
        theme = roadcolours["fog"]
#If player is called "hitboxes" or "Hitboxes", or is in debug, makes the hitboxes visible
if name == "Hitboxes" or name == "hitboxes" or debug == True:
    drawboxes = True
print("4.3, theme set")
load(highscore, "highscore.json")


#The game loop
while not quitgame:
    #detecting inputs
    for event in pg.event.get():
        if event.type == pg.QUIT:
            quitgame = True

        #Player input detection
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                moveleft = True
            if event.key == pg.K_RIGHT:
                moveright = True
            if event.key == pg.K_DOWN:
                movedown = True
            if event.key == pg.K_UP:
                moveup = True
        #End of input
        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT:
                moveleft = False
            if event.key == pg.K_RIGHT:
                moveright = False
            if event.key == pg.K_DOWN:
                movedown = False
            if event.key == pg.K_UP:
                moveup = False


    #Displaying the screen, road lanes, barriers
    screen.fill(theme["lane"])
    for x in barriers:
        x.drawobjects(screen, colour=(theme["barrier"]), type=("road"))
    for x in roadlines:
        x.drawobjects(screen, colour=(theme["lines"]), type=("road"))
    for x in moveillusion:
        x.drawobjects(screen, colour=(theme["lane"]), type=("road"))
    for x in cars:
        x.drawobjects(screen, colour=(theme["car"]), type=("vehicle"))
    for x in player:
        x.drawobjects(screen, colour=(theme["car"]), type=("vehicle"))

    for x in cars:
        x.carchange(screen)

    #Displaying the highscore text
    message("bees", (255, 255, 255), roadcolours["jank"]["lane"], 300, 325)


    #Moving the player car based on input
    if moveleft == True and pcar[0] >= 5:
        pcar[0] -= 1
        pcar[1] -= 1
    if moveright == True and pcar[1] <= 1275:
        pcar[0] += 1
        pcar[1] += 1
    if moveup == True and pcar[2] > 23:
        pcar[2] -= 3
        pcar[3] -= 3
    if movedown == True and pcar[3] < 277:
        pcar[2] += 3
        pcar[3] += 3
    cartop1[0] -= (speedmod * 2)
    cartop1[1] -= (speedmod *2)
    cartop2[0] -= (speedmod * 2)
    cartop2[1] -= (speedmod *2)
    car2[0] -= (speedmod * 4)
    car2[1] -= (speedmod *4)
    car3[0] -= (speedmod * 6)
    car3[1] -= (speedmod *6)
    car4[0] -= (speedmod * 8)
    car4[1] -= (speedmod *8)
    moveline1[0] -= (speedmod * 12)
    moveline1[1] -= (speedmod * 12)
    moveline2[0] -= (speedmod * 12)
    moveline2[1] -= (speedmod * 12)
    moveline3[0] -= (speedmod * 12)
    moveline3[1] -= (speedmod * 12)
    moveline4[0] -= (speedmod * 12)
    moveline4[1] -= (speedmod * 12)
    moveline5[0] -= (speedmod * 12)
    moveline5[1] -= (speedmod * 12)

    if cartop1[1] <= 0:
        cartop1[0] = 1280
        cartop1[1] = 1350
    if cartop2[1] <= 0:
        cartop2[0] = 1280
        cartop2[1] = 1350
    if car2[1] <= 0:
        car2rand = (rndm.randint(10, 40)*10)
        car2[0] = 1280+car2rand
        car2[1] = 1350+car2rand
    if car3[1] <= 0:
        car3rand = (rndm.randint(15, 50)*10)
        car3[0] = 1280+car3rand
        car3[1] = 1350+car3rand
    if car4[1] <= 0:
        car4rand = (rndm.randint(20, 60)*10)
        car4[0] = 1280+car4rand
        car4[1] = 1350+car4rand
    if moveline1[1] <= 0:
        moveline1[0] = 1280
        moveline1[1] = 1350
    if moveline2[1] <= 0:
        moveline2[0] = 1280
        moveline2[1] = 1350
    if moveline3[1] <= 0:
        moveline3[0] = 1280
        moveline3[1] = 1350
    if moveline4[1] <= 0:
        moveline4[0] = 1280
        moveline4[1] = 1350
    if moveline5[1] <= 0:
        moveline5[0] = 1280
        moveline5[1] = 1350
    
    #Checking collision
    for x in cars:
        x.collcheck(pcar)
    score[2] = round(score[2], 0)
    print(score[2])
    

    clock.tick(fps)
    pg.display.update()


print(score[0], " scored ", score[2], " on ", score[1])
if score[2] > highscore[2]: 
    save(score, "highscore.json")

quit()