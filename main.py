import mouse
import time
from PIL import ImageGrab
from enum import Enum


width = 16
height = 30


# Number Color
emtpy = (156, 81, 8)
flag = (250, 250, 250)
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


top_l_corner = (2578, 174)
bottom_r_corner = (3153, 1278)
outside_gray = (54, 54, 54)
suv_size = 4
ImageScreenshot = ImageGrab.grab(bbox=(top_l_corner[0], top_l_corner[1], bottom_r_corner[0], bottom_r_corner[1]))


actual_grid = [[9] * height for _ in range(width)]
exposed_grid = [[False] * height for _ in range(width)]

alpha = 0.2
leftCorner = (20, 20)  # (2591, 188)
rightCorner = (550, 1080)  # (3153, 1238)
pixelJump = 5
grayDiff = 500
ColorsDiff = 3500


def get_pixel_rgb(pos):
    return ImageScreenshot.load()[pos]


def move_mouse(pos):
    # move
    mouse.move(pos[0] + top_l_corner[0], pos[1] + top_l_corner[1], absolute=True, duration=0.0)


def move_mouse_cell(x, y):
    # print("moved to pos:")
    # print(x, y)
    move_mouse((real_x + x * real_d, real_y + y * real_d))


def shift_mouse(x, y):
    mouse.move(x, y, absolute=False, duration=1.0)


def fast_click():
    # time.sleep(0.15)
    mouse.drag(0, 0, 0, 0, absolute=False, duration=0.15)
    time.sleep(0.05)


def long_click():
    # todo:
    #  find a good time fot that
    # time.sleep(0.15)
    mouse.drag(0, 0, 0, 0, absolute=False, duration=0.4)
    time.sleep(0.05)


def get_pos():
    return mouse.get_position()


def color_dist(c1, c2):
    return (c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2 + (c1[2] - c2[2]) ** 2


def search_for_color(x, y, color, radius, color_dist_allowed):
    for i in range(int(x - radius * alpha), int(x + radius * alpha)):
        for j in range(int(y - radius * alpha), int(y + radius * alpha)):
            if color_dist(get_pixel_rgb((i, j)), color) < color_dist_allowed:
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


def search_for_edge(x1, x2, y1, y2, direction):
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
                if color_dist(outside_gray, get_pixel_rgb((x, y))) > grayDiff:
                    return x
            x += direction
    if y1 == y2:
        # searching for vertical edge
        y = y1
        while 1:
            step_size = (x2 - x1) // scan_count
            for x in range(x1, x2, step_size):
                if color_dist(outside_gray, get_pixel_rgb((x, y))) > grayDiff:
                    return y
            y += direction


def make_str_length_2(num):
    s = str(num)
    if 0 <= num <= 9:
        s = ' ' + s
    return s


def print_grid(grid):
    for j in range(len(grid[0])):
        print(' '.join([make_str_length_2(grid[i][j]) for i in range(len(grid))]))


def input_cell(x, y):
    x_cell = real_x + x * real_d
    y_cell = real_y + y * real_d
    is_background_gray = search_for_color(x_cell, y_cell, gray0, real_d, ColorsDiff)

    if search_for_color(x_cell, y_cell, flag, real_d, ColorsDiff):
        return Tiles.FLAG.value
    elif search_for_color(x_cell, y_cell, sky1, real_d, ColorsDiff) and is_background_gray:
        return Tiles.SKY1.value
    elif search_for_color(x_cell, y_cell, green2, real_d, ColorsDiff) and is_background_gray:
        return Tiles.GREEN2.value
    elif search_for_color(x_cell, y_cell, red3, real_d, ColorsDiff) and is_background_gray:
        return Tiles.RED3.value
    elif search_for_color(x_cell, y_cell, purple4, real_d, ColorsDiff) and is_background_gray:
        return Tiles.PURPLE4.value
    elif search_for_color(x_cell, y_cell, orange5, real_d, ColorsDiff) and is_background_gray:
        return Tiles.ORANGE5.value
    elif search_for_color(x_cell, y_cell, blue6, real_d, ColorsDiff) and is_background_gray:
        return Tiles.BLUE6.value
    # elif search_for_color(x_cell, y_cell, color7, real_d, ColorsDiff) and is_background_gray:
    #     return Tiles.COLOR7.value
    # elif search_for_color(x_cell, y_cell, color8, real_d, ColorsDiff) and is_background_gray:
    #     return Tiles.COLOR8.value
    elif search_for_color(x_cell, y_cell, emtpy, real_d, ColorsDiff):
        return Tiles.EMPTY.value
    elif is_background_gray:
        return Tiles.GRAY0.value
    else:
        print("DID NOT RECOGNIZE CELL!!!")
        print(x, y)
        return None


def update_grid():
    move_mouse(leftCorner)
    time.sleep(0.2)
    global ImageScreenshot
    ImageScreenshot = ImageGrab.grab(bbox=(2578, 174, 3153, 1278))
    wx = None
    wy = None
    bef =0
    for x in range(width):
        for y in range(height):
            prev_value = actual_grid[x][y]
            value = input_cell(x, y)
            if (not prev_value == 9) and (not value == prev_value):
                wx = x
                wy = y
                bef = prev_value
            actual_grid[x][y] = value
            if not value == 9:
                exposed_grid[x][y] = True

    if wx is not None:
        print("DANGER! DIDN'T PRESS")
        print_grid(actual_grid)
        print(wx, wy)
        print("before it was: " + str(bef))
        move_mouse_cell(wx, wy)
        exit(0)


def get_neighbors(x, y):
    neighbors = []
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if (not 0 <= i < width) or (not 0 <= j < height) or ((x, y) == (i, j)):
                continue
            neighbors.append(actual_grid[i][j])
    return neighbors


def neighbors_exists_in_a_box(suv, x, y):
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if 0 <= i < suv_size and 0 <= j < suv_size:
                if 1 <= suv[i][j] <= 8:
                    return True
    return False


def get_suv(x, y):
    # get a 4x4 grid
    suv = [[-999] * suv_size for _ in range(suv_size)]
    for i in range(x, x + suv_size):
        for j in range(y, y + suv_size):
            if (i < width) and (j < height):
                suv[i-x][j-y] = actual_grid[i][j]
    return suv


def seen_enough_flags(x, y):
    neighbors = get_neighbors(x, y)
    flag_count = neighbors.count(-1)
    empty_count = neighbors.count(9)

    if empty_count == 0:
        return False

    if flag_count == actual_grid[x][y]:
        return True


def must_see_flags(x, y):
    neighbors = get_neighbors(x, y)
    flag_count = neighbors.count(-1)
    empty_count = neighbors.count(9)
    value = actual_grid[x][y]
    if value == flag_count + empty_count:
        return True
    return False


def interesting_blank_tiles(suv):
    blank_tiles = []
    for i in range(suv_size):
        for j in range(suv_size):
            if suv[i][j] == 9 and neighbors_exists_in_a_box(suv, i, j):
                blank_tiles.append((i, j))
    return blank_tiles


def good_try(x, y):
    for i in range(x - 2, x + suv_size + 2):
        for j in range(y - 2, y + suv_size + 2):
            if (not 0 <= i < width) or (not 0 <= j < height):
                continue
            value = actual_grid[i][j]
            if 1 <= value <= 8:
                neighbors = get_neighbors(i, j)
                if neighbors.count(-1) > value:
                    return False
                if neighbors.count(9) + neighbors.count(-1) < value:
                    return False
    return True


def surrounded_by_flags():
    for x in range(width):
        for y in range(height):
            if actual_grid[x][y] == 9:
                neighbors = get_neighbors(x, y)
                if all([nei == -1 for nei in neighbors]):
                    print("SPECIAL FUCKING MOVE!!!")
                    print("NUMBER SURROUNDED BY FLAGS!!!")
                    move_mouse_cell(x,y)
                    long_click()


def smart(x, y):
    suv = get_suv(x, y)
    tiles = interesting_blank_tiles(suv)
    tiles_count = len(tiles)
    all_good_tries = []
    if tiles_count == 0:
        return False
    print("original suv:")
    print_grid(suv)
    print()
    for sol in range(1 << tiles_count):
        for i in range(tiles_count):
            pos = tiles[i]
            if (1 << i) & sol:
                actual_grid[pos[0]+x][pos[1]+y] = -1
                suv[pos[0]][pos[1]] = -1
            else:
                actual_grid[pos[0]+x][pos[1]+y] = 11  # some number we don't know about
                suv[pos[0]][pos[1]] = 11
        if good_try(x, y):
            print("viable solution:")
            print_grid(suv)
            print()
            all_good_tries.append(sol)

    # revert changes
    for pos in tiles:
        actual_grid[pos[0] + x][pos[1] + y] = 9

    if not all_good_tries:
        print("DANGER!!!!")
        exit(0)

    flag_for_all = [all(sol & (1 << tile) for sol in all_good_tries) for tile in range(tiles_count)]
    number_for_all = [all(sol & (1 << tile) == 0 for sol in all_good_tries) for tile in range(tiles_count)]
    need_for_pic = False
    for i in range(tiles_count):
        if flag_for_all[i]:
            # make a flag
            pos = tiles[i]
            move_mouse_cell(x + pos[0], y + pos[1])
            fast_click()
            actual_grid[x + pos[0]][y + pos[1]] = -1
            print("made smart flag")
            print(x + pos[0], y + pos[1])
        if number_for_all[i]:
            # make a number
            pos = tiles[i]
            move_mouse_cell(x + pos[0], y + pos[1])
            long_click()
            need_for_pic = True
            print("made smart number")
            print(x + pos[0], y + pos[1])
    return need_for_pic


def suv_intersect(pos1, pos2):
    if pos1[0] <= pos2[0] < pos1[0] + 4 and pos1[1] <= pos2[1] < pos1[1] + 4:
        return True
    if pos2[0] <= pos1[0] < pos2[0] + 4 and pos2[1] <= pos1[1] < pos2[1] + 4:
        return True
    return False


def solve_grid():
    smart_already_done = []
    for i in range(width):
        for j in range(height):

            # if seen_enough_flags(i, j):
            #     print("seen enough flags", i, j)
            #     move_mouse_cell(i, j)
            #     fast_click()

            # if mustSeeFlags(i, j):
            #     for x in range(i - 1, j + 2):
            #         for y in range(i - 1, j + 2):
            #             if (0 <= x < width) and (0 <= y < height):
            #                 if actual_grid[x][y] == 9:
            #                     print("must see flags", x, y)
            #                     moveMouseCell(x, y)
            #                     fastClick()
            #                     actual_grid[i][j] = -1
            if all([not suv_intersect(pos, (i, j)) for pos in smart_already_done]):
                if smart(i, j):
                    smart_already_done.append((i, j))


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
screen_width = bottom_r_corner[0] - top_l_corner[0] - 10
screen_height = bottom_r_corner[1] - top_l_corner[1] - 10

x_l = search_for_edge(5, 5, 5, screen_height, 1)
x_r = search_for_edge(screen_width, screen_width, 5, screen_height, -1)
y_t = search_for_edge(5, screen_width, 5, 5, 1)
y_b = search_for_edge(5, screen_width, screen_height, screen_height, -1)

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

# print(input_cell(3,12))
# move_mouse_cell(3,12)
# exit(0)

# move_mouse((real_x-alpha*real_d, real_y-alpha*real_d))
# time.sleep(2)
# move_mouse((real_x+alpha*real_d, real_y+alpha*real_d))
# exit(0)
c = 300
while c:
    c -= 1
    t1 = time.time()
    update_grid()
    print_grid(actual_grid)
    t2 = time.time()
    solve_grid()
    t3 = time.time()
    surrounded_by_flags()
    t4 = time.time()
    print("updating: " + str(t2 - t1))
    print("solving: "+str(t3-t2))
    print("surrounded: " + str(t4 - t3))


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
        if search_for_color(newX, newY, (255, 255, 255), answer_d, 1500):
            press_x = real_x + i * real_d
            press_y = real_y + j * real_d

            moveMouse(press_x, press_y)
            time.sleep(0.02)
            longClick(0.035)
            time.sleep(0.02)

'''

# ToDo: to correct the white search algorithm

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
