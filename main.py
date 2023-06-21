import mouse
import time
from PIL import ImageGrab
from enum import Enum


width = 16#18
height = 30#20


# Number Color
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


class Tiles(Enum):
    EMPTY = 9
    FLAG = -1
    GRAY0 = 0
    SKY1 = 1
    GREEN2 = 2
    RED3 = 3
    PURPLE4 = 4
    ORANGE5 = 5
    BLUE6 = 6
    COLOR7 = 7
    COLOR8 = 8


ImageScreenshot = ImageGrab.grab(bbox=(2578, 174, 3153, 1278))


actual_grid = [[0] * height for _ in range(width)]
exposed_grid = [[False] * height for _ in range(width)]

alpha = 0.4
leftCorner = (20, 20)#(2591, 188)
rightCorner = (550, 1080)#(3153, 1238)
pixelJump = 5
grayDiff = 500
ColorsDiff = 1500

# rgb(54, 54, 54)
def GetPixelRGB(pos):
    return ImageScreenshot.load()[pos]


def moveMouse(pos):

    mouse.move(pos[0]+2578, pos[1]+174, absolute=True, duration=0.0)


def moveMouseCell(x, y):
    moveMouse((real_x + x * real_d, real_y + y * real_d))


def shiftMouse(x, y):
    mouse.move(x, y, absolute=False, duration=1.0)


def fastClick():
    time.sleep(0.03)
    # time.sleep(1)
    mouse.drag(0, 0, 0, 0, absolute=False, duration=0.035)
    # time.sleep(1)
    time.sleep(0.03)

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


def SearchForcolor(x, y, color, radius, color_dist):
    for i in range(int(x - radius * alpha), int(x + radius * alpha)):
        for j in range(int(y - radius * alpha), int(y + radius * alpha)):
            if ColorDist(GetPixelRGB((i, j)), color) < color_dist:
                return True
    return False


'''
def SearchForNumbers(x, y, radius, colorDist):
    for i in range(int(x - radius * alpha), int(x + radius * alpha)):
        for j in range(int(y - radius * alpha), int(y + radius * alpha)):
            for numColor in numberColors:
                if ColorDist(GetPixelRGB((i, j)), numColor) < colorDist:
                    return i, j
    return None, None
'''


def FindTopLeftCorner():
    # todo:
    #  ugly!!!
    allx = []
    ally = []
    for i in range(leftCorner[1], rightCorner[1]):
        for j in range(leftCorner[0], rightCorner[0]):
            if ColorDist(GetPixelRGB((j, i)), GetPixelRGB((j + pixelJump, i))) > grayDiff:
                allx.append(j+pixelJump)
                ally.append(i)
                # return j + pixelJump, i
    return min(allx), min(ally)


def FindButtomRightCorner():
    # todo:
    #  fix it, it might not work
    for i in range(rightCorner[1], leftCorner[1], -1):
        for j in range(rightCorner[0], leftCorner[0], -1):
            if ColorDist(GetPixelRGB((j, i)), GetPixelRGB((j - pixelJump, i))) > grayDiff:
                return j - pixelJump, i
    return None


def printGrid():
    for j in range(height):
        print(' '.join([str(actual_grid[i][j]) for i in range(width)]))


def inputCell(x, y):
    x_cell = real_x + x * real_d
    y_cell = real_y + y * real_d
    isBackgroundGray = SearchForcolor(x_cell, y_cell, gray0, real_d, ColorsDiff)

    if SearchForcolor(x_cell, y_cell, flag, real_d, ColorsDiff):
        return Tiles.FLAG.value
    elif SearchForcolor(x_cell, y_cell, sky1, real_d, ColorsDiff) and isBackgroundGray:
        return Tiles.SKY1.value
    elif SearchForcolor(x_cell, y_cell, green2, real_d, ColorsDiff) and isBackgroundGray:
        return Tiles.GREEN2.value
    elif SearchForcolor(x_cell, y_cell, red3, real_d, ColorsDiff) and isBackgroundGray:
        return Tiles.RED3.value
    elif SearchForcolor(x_cell, y_cell, purple4, real_d, ColorsDiff) and isBackgroundGray:
        return Tiles.PURPLE4.value
    elif SearchForcolor(x_cell, y_cell, orange5, real_d, ColorsDiff) and isBackgroundGray:
        return Tiles.ORANGE5.value
    elif SearchForcolor(x_cell, y_cell, blue6, real_d, ColorsDiff) and isBackgroundGray:
        return Tiles.BLUE6.value
    # elif SearchForcolor(x_cell, y_cell, color7, real_d, ColorsDiff) and isBackgroundGray:
    #     return Tiles.COLOR7.value
    # elif SearchForcolor(x_cell, y_cell, color8, real_d, ColorsDiff) and isBackgroundGray:
    #     return Tiles.COLOR8.value
    elif SearchForcolor(x_cell, y_cell, emtpy, real_d, ColorsDiff):
        return Tiles.EMPTY.value
    elif isBackgroundGray:
        return Tiles.GRAY0.value


def updateGrid():
    moveMouse(leftCorner)
    time.sleep(0.1)
    global ImageScreenshot
    ImageScreenshot = ImageGrab.grab(bbox=(2578, 174, 3153, 1278))
    for x in range(width):
        for y in range(height):
            value = inputCell(x, y)
            actual_grid[x][y] = value
            if not value == 9:
                exposed_grid[x][y] = True


def getNeighbors(x, y):
    neighbors = []
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if (not 0 <= i < width) or (not 0 <= j < height) or ((x, y) == (i, j)):
                continue
            neighbors.append(actual_grid[i][j])
    return neighbors


def seenEnoughFlags(x, y):
    neighbors = getNeighbors(x, y)
    flagCount = neighbors.count(-1)
    emptyCount = neighbors.count(9)

    if emptyCount == 0:
        return

    if flagCount == actual_grid[x][y]:
        print("seen enough flags", x, y)
        moveMouseCell(x, y)
        fastClick()


def mustSeeFlags(x, y):
    neighbors = getNeighbors(x, y)
    flagCount = neighbors.count(-1)
    emptyCount = neighbors.count(9)
    value = actual_grid[x][y]
    if value == flagCount + emptyCount:
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if (0 <= i < width) and (0 <= j < height):
                    if actual_grid[i][j] == 9:
                        print("must see flags", x, y)
                        moveMouseCell(i, j)
                        fastClick()
                        actual_grid[i][j] = -1


def smart(x, y):
    # get a 4x4 grid
    environment = [[9] * 4] * 4
    for i in range(x, x + 4):
        for j in range(y, y + 4):
            if (i < width) and (j <= height):
                environment[i-x][j-y] = actual_grid[i][j]


def solveGrid():
    for i in range(width):
        for j in range(height):
            seenEnoughFlags(i, j)
            mustSeeFlags(i, j)
            # smart(i, j)


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
#         # print (GetPixelRGB(getPos()))
#         time.sleep(0.2)
#




# find corners
x_l, y_t = FindTopLeftCorner()
x_r, y_b = FindButtomRightCorner()
# realGame
real_d = (y_b - y_t) / height
# should be the same
# ral_d = (x_r - x_l) / width
real_x = x_l + real_d / 2
real_y = y_t + real_d / 2

# moveMouse((x_l,y_t))
# exit(0)
# moveMouseCell(1,1)
# print(GetPixelRGB(getPos()))

# updateGrid()
# printGrid()
# print(inputCell(11, 14))
# moveMouseCell(11, 14)
# mustSeeFlags(11,14)
# exit(0)
c = 200
# moveMouseCell(8,8)

while c:
    c -= 1
    updateGrid()
    printGrid()
    solveGrid()


'''

# answer
answer_x = 1492
answer_y = 523
answer_d = 26.4



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
