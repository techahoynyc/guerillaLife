#!/usr/bin/python
import sys, random, copy
from time import sleep
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from guerillaClockDisplay import *

# AnextY live cell with fewer than two live neighbors dies, as if by underpopulation.
# AnextY live cell with two or three live neighbors lives on to the next generation.
# AnextY live cell with more than three live neighbors dies, as if by overpopulation.
# AnextY dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.

def getNeighbors(generation, x, y):
    upperX = len(generation[0])-1
    upperY = len(generation)-1
    neighborCount = 0
    nextX = 0
    nextY = 0
    #n1 = x-1;y-1
    if x == 0:
        #!n1
        pass
    else:
        nextX = x - 1
        nextY = y - 1
        neighborCount += generation[nextY][nextX] #n1

    #n2 = x;y-1
    if x == 0:
        #!n2
        pass
    else:
        nextX = x
        nextY = y - 1
        neighborCount += generation[nextY][nextX] #n2

    #n3 = x+1;y-1
    if x == upperX or y == 0:
        #!n3
        pass
    elif y == upperY:
        #!n3
        pass
    else:
        nextX = x + 1
        nextY = y - 1
        neighborCount += generation[nextY][nextX] #n3

    #n4 = x+1;y
    if y == upperY or x == upperX:
        #!n4
        pass
    else:
        nextX = x + 1
        nextY = y
        neighborCount += generation[nextY][nextX] #n4

    #n5 = x+1;y+1
    if y == upperY or x == upperX:
        #!n5
        pass
    else:
        nextX = x + 1
        nextY = y + 1
        neighborCount += generation[nextY][nextX] #n5

    #n6 = x;y+1
    if x == upperX or y == upperY:
        #!n6
        pass
    else:
        nextX = x
        nextY = y + 1
        neighborCount += generation[nextY][nextX] #n6

    #n7 = x-1;y+1
    if x == 0 or y == upperY:
        #!n7
        pass
    else:
        nextX = x - 1
        nextY = y + 1
        neighborCount += generation[nextY][nextX] #n7

    #n8 = x-1;y
    if x == 0:
        #!n8
        pass
    else:
        nextX = x - 1
        nextY = y
        neighborCount += generation[nextY][nextX] #n8

    return neighborCount

def runLife(xsize, ysize, sprinkle, seed = None):
    #build grid
    gridRow, generationW, generationX, generationY, theseed = ([] for i in range(5))
    for x in range(0,xsize):
        gridRow.append(0)
    for y in range(0,ysize):
        theseed.append(copy.deepcopy(gridRow))

    generationW = copy.deepcopy(theseed)
    generationX = copy.deepcopy(theseed)
    generationY = copy.deepcopy(theseed)

    #seed the grid
    if seed:
        #we got a seed here!
        pass
    else:
        #randomly seed
        for y in range(0,ysize):
            for x in range(0,sprinkle):
                ranCell = random.randint(0,xsize-1)
                generationX[y][ranCell] = theseed[y][ranCell] = 1
        """
        for r in generationX:
            for c in r:
                print c,
            print ""
        """
        tick = 1
        dead = 0
        while not dead:
            imalive = 0
            frozen = 1
            blinking = 1
            for x in range(0,xsize):
                for y in range(0,ysize):
                    if generationX[y][x] == 1:
                        imalive = 1
                    neighbors = getNeighbors(generationX,x,y)
                    #die
                    if generationX[y][x] == 1 and neighbors < 2:
                        generationY[y][x] = 0
                        GCD.cellOff(x,y)
                    if generationX[y][x] == 1 and neighbors > 3:
                        generationY[y][x] = 0
                        GCD.cellOff(x,y)
                    #live
                    if generationX[y][x] == 1 and (neighbors == 2 or neighbors == 3):
                        generationY[y][x] = 1
                        GCD.cellOn(x,y)
                    #birth
                    if generationX[y][x] == 0:
                        if neighbors == 3:
                            generationY[y][x] = 1
                            GCD.cellOn(x,y)

            #clear screen
            #GCD.clear()
            print "tick:",tick
            for r in generationX:
                for c in r:
                    if c == 0:
                        print " ",
                    if c == 1:
                        print "*",
                print ""

            #sleep(0.5)
            tick += 1
            for x in range (0,xsize):
                for y in range(0,ysize):
                    if generationW[y][x] != generationY[y][x]:
                        blinking = 0
                    if generationX[y][x] != generationY[y][x]:
                        frozen = 0
            generationW = copy.deepcopy(generationX)
            generationX = copy.deepcopy(generationY)

            if not imalive or frozen or blinking:
                dead = 1
                if not imalive:
                    cause = "Death"
                elif frozen:
                    cause = "Frozen"
                elif blinking:
                    cause = "Blinking"
                print "Total Generations: ",tick," || Termination Cause: ",cause

GCD = guerillaClockDisplay()
GCD.initiate()
#GCD.oneDot()
runLife(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]))
