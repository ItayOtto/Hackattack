import mouse
import time
from PIL import ImageGrab
from enum import Enum


class Tiles(Enum):
    EMPTY = 0
    FLAG = 1
    GRAY0 = 2
    SKY1 = 3
    GREEN2 = 4
    RED3 = 5
    PURPLE4 = 6
    ORANGE5 = 7
    BLUE6 = 8


ImageScreenshot = ImageGrab.grab()

width = 18
height = 20

actual_grid = [[0] * height for i in range(width)]

alpha = 0.4
leftCorner = (2591, 188)
rightCorner = (3153, 1238)
pixelJump = 5
grayDiff = 1000
ColorsDiff = 1500


def GetPixelRGB(pos):
    return ImageScreenshot.load()[pos]


def moveMouse(x,y):
    mouse.move(x, y, absolute=True, duration=0.0)


def moveMouseCell(x,y):
    moveMouse(real_x + x * real_d, real_y + y * real_d)


def shiftMouse(x,y):
    mouse.move(x, y, absolute=False, duration=1.0)


def fastClick():
    time.sleep(0.02)
    mouse.drag(0, 0, 0, 0, absolute=False, duration=0.035)
    time.sleep(0.02)

def longClick ():
    # todo:
    #  find a good time fot that
    time.sleep(0.02)
    mouse.drag(0, 0, 0, 0, absolute=False, duration=0.5)
    time.sleep(0.02)


def getPos():
    return mouse.get_position()


def ColorDist (c1, c2):
    return (c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2 + (c1[2] - c2[2]) ** 2


def SearchForcolor(x, y, color, radius, colorDist):
    for i in range(int(x - radius * alpha), int(x + radius * alpha)):
        for j in range(int(y - radius * alpha), int(y + radius * alpha)):
            if ColorDist(GetPixelRGB((i, j)), color) < colorDist:
                return True
    return False


def SearchForNumbers(x, y, radius, colorDist):
    for i in range(int(x - radius * alpha), int(x + radius * alpha)):
        for j in range(int(y - radius * alpha), int(y + radius * alpha)):
            for numColor in numberColors:
                if ColorDist(GetPixelRGB((i, j)), numColor) < colorDist:
                    return i, j
    return None, None


def FindTopLeftCorner():
    for i in range(leftCorner[1], rightCorner[1]):
        for j in range(leftCorner[0], rightCorner[0]):
            if ColorDist(GetPixelRGB((j, i)), GetPixelRGB((j + pixelJump, i))) > grayDiff:
                return j + pixelJump, i
    return None


def FindButtomRightCorner():
    for i in range(rightCorner[1], leftCorner[1], -1):
        for j in range(rightCorner[0], leftCorner[0], -1):
            if ColorDist(GetPixelRGB((j, i)), GetPixelRGB((j - pixelJump, i))) > grayDiff:
                return j - pixelJump, i
    return None


def printGrid():
    for j in range(height):
        print(' '.join([str(actual_grid[i][j]) for i in range(width)]))


def inputCell(x, y):
    # todo:
    #  use the x_cell and y_cell!!
    x_cell = real_x + x * real_d
    y_cell = real_y + y * real_d
    if SearchForcolor(x_cell, y_cell, SKY1, alpha, ColorsDiff):
        return Tiles.SKY1.valuse
    elif SearchForcolor(x_cell, y_cell, GREEN2, alpha, ColorsDiff):
        return Tiles.GREEN2.valuse
    elif SearchForcolor(x_cell, y_cell, RED3, alpha, ColorsDiff):
        return Tiles.RED3.valuse
    elif SearchForcolor(x_cell, y_cell, PURPLE4, alpha, ColorsDiff):
        return Tiles.PURPLE4.valuse
    elif SearchForcolor(x_cell, y_cell, ORANGE5, alpha, ColorsDiff):
        return Tiles.ORANGE5.valuse
    elif SearchForcolor(x_cell, y_cell, BLUE6, alpha, ColorsDiff):
        return Tiles.BLUE6.valuse
    elif SearchForcolor(x_cell, y_cell, color7, alpha, ColorsDiff):
        return Tiles.color7.valuse
    elif SearchForcolor(x_cell, y_cell, FLAG, alpha, ColorsDiff):
        return Tiles.FLAG.valuse
    elif SearchForcolor(x_cell, y_cell, EMPTY, alpha, ColorsDiff):
        return Tiles.EMPTY.valuse


def updateGrid():
    global ImageScreenshot
    ImageScreenshot = ImageGrab.grab()
    for x in range(width):
        for y in range(height):
            actual_grid[x][y] = inputCell(x, y)


def getNeighbors(x, y):
    neighbors = []
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if (not 0 <= i < width) or (not 0 <= j <= height) or ((x, y) == (i, j)):
                continue
            neighbors.append(actual_grid[i][j])
    return neighbors


def solveGrid():
    for i in range(height):
        for j in range(width):
            pass




# 2579, 489
# 2579, 1032
# 3123, 1032

# while 1:
#     if mouse.is_pressed("left"):
#         print (GetPixelRGB(getPos()))
#         time.sleep(0.2)

# while 1:
#     if mouse.is_pressed("left"):
#         print (getPos())
#         print (GetPixelRGB(getPos()))
#         time.sleep(0.2)


# Number Color
# TODO:
#   make enum list for the colors!!!
emtpy = (156, 81, 8)
flag = (250, 253, 255)
gray0 = (76, 76, 76)
sky1 = (8, 195, 255)
green2 = (110, 218, 9)
red3 = (209, 64, 64)
purple4 = (176, 90, 224)
orange5 = (236, 145, 11)
blue6 = (101, 140, 235)
# TODO:
color7 = (101, 140, 235)
color8 = (101, 140, 235)


numberColors = [sky1, green2, red3]


# find corners
x_l, y_t = FindTopLeftCorner()
x_r, y_b = FindButtomRightCorner()

# realGame
real_d = (y_b - y_t) / height
# should be the same
# ral_d = (x_r - x_l) / width
real_x = x_l + real_d / 2
real_y = y_t + real_d / 2

# moveMouseCell(1,1)
# print(GetPixelRGB(getPos()))

printGrid()

exit(0)




# answer
answer_x = 1492
answer_y = 523
answer_d = 26.4


'''
time.sleep(1)
for i in range(width):
    for j in range(height):
        newX = answer_x + i * answer_d
        newY = answer_y + j * answer_d
        if SearchForcolor(newX, newY, (255, 255, 255), answer_d, 1500):
            press_x = real_x + i * real_d
            press_y = real_y + j * real_d

            moveMouse(press_x, press_y)
            time.sleep(0.02)
            longClick(0.035)
            time.sleep(0.02)

'''

#ToDo: to correct the white search algorithm

'''
oldPos = []
c = 10
while c:
    c-=1
    for i in range(width):
        for j in range(height):
            newX = real_x + i * real_d
            newY = real_y + j * real_d
            x, y = SearchForNumbers(newX, newY, real_d, 1500)

            if x is None:
                continue

            if oldPos and min([(pos[0] - x) ** 2 + (pos[1] - y) ** 2 for pos in oldPos]) < (real_d ** 2) / 2:
                continue

            if x:
                moveMouse(x, y)
                oldPos.append((x, y))

                time.sleep(0.02)
                longClick(0.035)
                time.sleep(0.02)

    ImageScreenshot = ImageGrab.grab()

'''
