import pygame as pg
import time
pg.init()

carX = 0
fps = 10
quitgame = False

scrnX = 1280
scrnY = 50
clock = pg.time.Clock()
screen = pg.display.set_mode((scrnX, scrnY), pg.RESIZABLE)
white = (255, 255, 255)
grey = (100, 100, 100)

class Objects:
    def __init__(self, coords):
        self.coords = coords

    def drawobject(self, coords, colour):
        pg.draw.polygon(screen, colour, self.coords)

car = ((([((1210-carX),5), ((1280-carX), 5), ((1280-carX), 45), ((1210-carX), 45)])))
drawncar = Objects(car)

cars = [drawncar]

while not quitgame:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            quitgame = True

    screen.fill(white)

    for x in cars:
        x.drawobject(screen, grey)
    
    newcarX = (carX + 5)
    carX = newcarX
    print(carX, newcarX)

    pg.display.update()