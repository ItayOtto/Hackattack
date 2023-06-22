from functools import reduce

import mouse
import time
from PIL import ImageGrab
from enum import Enum


#Todo:
# 1. get a 4*4 square
# 2. put all blank tiles in a list (blank tiles which are near a number (GetNeighbors))
# 3. brute force all options for a filling
# 4. (for each option) check if correct
# 5. take the tiles all correct fillings are agreeing on
# 6. click them

width = 16
height = 16


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


top_left_corner = (2578, 174)
bottom_right_corner = (3153, 1278)
outside_gray = (54, 54, 54)

ImageScreenshot = ImageGrab.grab(bbox=(top_left_corner[0], top_left_corner[1], bottom_right_corner[0], bottom_right_corner[1]))


actual_grid = [[0] * height for _ in range(width)]
exposed_grid = [[False] * height for _ in range(width)]

alpha = 0.4
leftCorner = (20, 20) # (2591, 188)
rightCorner = (550, 1080) # (3153, 1238)
pixelJump = 5
grayDiff = 500
ColorsDiff = 1500


def GetPixelRGB(pos):
    return ImageScreenshot.load()[pos]


def moveMouse(pos):
    # move
    mouse.move(pos[0] + top_left_corner[0], pos[1] + top_left_corner[1], absolute = True, duration = 0.0)


def moveMouseCell(x, y):
    moveMouse((real_x + x * real_d, real_y + y * real_d))


def shiftMouse(x, y):
    mouse.move(x, y, absolute=False, duration=1.0)


def fastClick():
    time.sleep(0.035)
    mouse.drag(0, 0, 0, 0, absolute = False, duration = 0.05)
    time.sleep(0.035)


def longClick ():
    # todo:
    #  find a good time fot that
    time.sleep(0.035)
    mouse.drag(0, 0, 0, 0, absolute = False, duration = 0.5)
    time.sleep(0.035)


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


def SearchForEdge(x1, x2, y1, y2, dir):
    scan_count = 15
    if x1 > x2:
        x1, x2 = x2, x1

    if y1 > y2:
        y1, y2 = y2, y1

    if x1 == x2:
        # searching for vertical edge
        x = x1
        while 1:
            step_size = (y2 - y1) // scan_count
            for y in range(y1, y2, step_size):
                if ColorDist(outside_gray, GetPixelRGB((x, y))) > grayDiff:
                    return x
            x += dir
    if y1 == y2:
        # searching for vertical edge
        y = y1
        while 1:
            step_size = (x2 - x1) // scan_count
            for x in range(x1, x2, step_size):
                if ColorDist(outside_gray, GetPixelRGB((x, y))) > grayDiff:
                    return y
            y += dir


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
    time.sleep(0.01)
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
        return False

    if flagCount == actual_grid[x][y]:
        return True


def mustSeeFlags(x, y):
    neighbors = getNeighbors(x, y)
    flagCount = neighbors.count(-1)
    emptyCount = neighbors.count(9)
    value = actual_grid[x][y]
    if value == flagCount + emptyCount:
        return True
    return False


def smart(x, y):
    suv = get_suv(x, y)
    tiles = interesting_blank_tiles(suv)
    tiles_count = len(tiles)
    all_good_tries = []
    for sol in range(1 << tiles_count):
        for i in range(tiles_count):
            pos = tiles[i]
            if (1 << i) & sol:
                actual_grid[pos[0]+x][pos[1]+y] = -1
            else:
                actual_grid[pos[0]+x][pos[1]+y] = 11 # some number we don't know about
        if good_try(x, y):
            all_good_tries.append(sol)
    print(suv)
    print(tiles)
    print(all_good_tries)
    # revert changes
    for i in range(tiles_count):
        pos = tiles[i]
        actual_grid[pos[0] + x][pos[1] + y] = 9

    if not all_good_tries:
        return False

    and_of_all = [all(sol & (1 << tile) for sol in all_good_tries) for tile in range(tiles_count)]
    or_of_all = [all(sol & (1 << tile) == 0 for sol in all_good_tries) for tile in range(tiles_count)]
    need_for_pic = False
    for i in range(tiles_count):
        if and_of_all[i]:
            # make a flag
            pos = tiles[i]
            moveMouseCell(x + pos[0], y+pos[1])
            fastClick()
            actual_grid[x + pos[0]][y+pos[1]] = -1
        if or_of_all[i]:
            # make a number
            pos = tiles[i]
            moveMouseCell(x + pos[0], y + pos[1])
            longClick()
            need_for_pic = True
    return need_for_pic


def solveGrid():
    for i in range(width):
        for j in range(height):

            if seenEnoughFlags(i, j):
                print("seen enough flags", i, j)
                moveMouseCell(i, j)
                fastClick()

            if mustSeeFlags(i, j):
                for x in range(i - 1, j + 2):
                    for y in range(i - 1, j + 2):
                        if (0 <= x < width) and (0 <= y < height):
                            if actual_grid[x][y] == 9:
                                print("must see flags", x, y)
                                moveMouseCell(x, y)
                                fastClick()
                                actual_grid[i][j] = -1

            if smart(i, j):
                return


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
screen_width = bottom_right_corner[0] - top_left_corner[0] - 10
screen_height = bottom_right_corner[1] - top_left_corner[1] - 10

x_l = SearchForEdge(5, 5, 5, screen_height, 1)
x_r = SearchForEdge(screen_width, screen_width, 5, screen_height, -1)
y_t = SearchForEdge(5, screen_width, 5, 5, 1)
y_b = SearchForEdge(5, screen_width, screen_height, screen_height, -1)

# realGame
real_d = (y_b - y_t) / height
# should be the same
# ral_d = (x_r - x_l) / width
real_x = x_l + real_d / 2
real_y = y_t + real_d / 2

# moveMouse((x_l,y_t))
# exit(0)
# print(GetPixelRGB(getPos()))

# updateGrid()
# printGrid()
# print(get_suv(3, 1))


c = 100
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
