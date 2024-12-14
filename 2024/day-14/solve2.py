import os
import sys
import time
from collections import defaultdict
from dataclasses import dataclass
from typing import Optional


straight_lines = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""
tile_map = [[[] for _ in range(11)] for _ in range(7)]

straight_lines = open("input.txt", "r").read().strip()
tile_map = [[[] for _ in range(101)] for _ in range(103)]

straight_lines = [[tuple(map(int, v.replace("p=", "").replace("v=", "").split(','))) for v in l.split(" ")] for l in straight_lines.splitlines() if l.strip()]


@dataclass
class Robot:
    pos: tuple[int, int]
    velocity: tuple[int, int]
    seconds: int

def move_robot(tile_map: list[list[list[Robot]]], robot: Robot, seconds: int):
    if robot.seconds == seconds:
        return
    
    x, y = robot.pos
    vx, vy = robot.velocity
    robot.seconds = seconds
    
    cell = tile_map[y][x]
    assert robot in cell
    cell.remove(robot)
    
    new_y = y+vy
    if new_y >= len(tile_map):
        new_y = new_y-len(tile_map)
    elif new_y < 0:
        new_y = len(tile_map)-abs(new_y)
    new_x = x+vx
    if new_x >= len(tile_map[0]):
        new_x = new_x-len(tile_map[0])
    elif new_x < 0:
        new_x = len(tile_map[0])-abs(new_x)
        
    robot.pos = (new_x, new_y)
    tile_map[new_y][new_x].append(robot)
    

for p, v in straight_lines:
    x, y = p
    tile_map[y][x].append(Robot(p, v, 0))


# def print_map(tile_map, sec: int):
#     print("="*20, "MAP", "="*20)
#     for i in range(len(tile_map)):
#         for j in range(len(tile_map[i])):
#             print("X" if len(tile_map[i][j]) else ".", end="")
#         print("")
#     print("\nSeconds:", sec)

# starting_threshold = int(sys.argv[1])
# for sec in range(10_000):
#     for i in range(len(tile_map)):
#         for j in range(len(tile_map[0])):
#             cell = [r for r in tile_map[i][j]]
#             for r in cell:
#                 move_robot(tile_map, r, sec+1)
#     if sec > starting_threshold:
#         os.system("clear")
#         print_map(tile_map, sec)
#         time.sleep(0.1)


# Executed multiple terminals in parallel with values for starting
# threshold as 5000, 7000, 9000.
# Watched the terminals until the tree appeared.
#
# Also gamed the input box of AOC to get a range of where the tree
# was located:
# 1000 sec -> Input is too low
# 10000 sec -> Input is too high
# 5000 sec -> Input is too low
# Then tried to find tried between 5000-10000 seconds.
#
# After watching for a while I saw the following tree and cancelled
# the terminal execution.

tree = """............X..........XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX...............................................
.......................X.............................X...............................................
.......................X.............................X...............................................
.......................X.............................X...............................................
.......................X.............................X...............................................
.......................X..............X..............X...............................X...............
.................X.....X.............XXX.............X...................X...........................
.......................X............XXXXX............X...............................................
.......................X...........XXXXXXX...........X...............................................
.......................X..........XXXXXXXXX..........X..............................X...X............
.......................X............XXXXX............X.......................X.......................
.......................X...........XXXXXXX...........X...............................................
.......................X..........XXXXXXXXX..........X..........................................X....
.......................X.........XXXXXXXXXXX.........X.....................X.........................
.......................X........XXXXXXXXXXXXX........X...............................................
.......................X..........XXXXXXXXX..........X...............................................
.......................X.........XXXXXXXXXXX.........X....................X........X...............X.
..X....................X........XXXXXXXXXXXXX........X...............................................
.......................X.......XXXXXXXXXXXXXXX.......X...............................................
.......................X......XXXXXXXXXXXXXXXXX......X..........X....................................
.......................X........XXXXXXXXXXXXX........X..............X................X...X...........
.......................X.......XXXXXXXXXXXXXXX.......X...X......X....................................
........X........X.....X......XXXXXXXXXXXXXXXXX......X...............................................
.............XX........X.....XXXXXXXXXXXXXXXXXXX.....X...............................................
.......................X....XXXXXXXXXXXXXXXXXXXXX....X........................................X......
.......................X.............XXX.............X....................X..........................
.......................X.............XXX.............X............................X..................
.......................X.............XXX.............X...............................................
..........X............X.............................X...............................................
.......................X.............................X...............................................
.......................X.............................X...................X............X..............
...X...................X.............................X...............................................
.......................XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.........................X............X........"""


def generate_screen(tile_map):
    screen = ""
    for i in range(len(tile_map)):
        for j in range(len(tile_map[i])):
            screen += "X" if len(tile_map[i][j]) else "."
        screen += "\n"
    return screen

for sec in range(10_000):
    for i in range(len(tile_map)):
        for j in range(len(tile_map[0])):
            cell = [r for r in tile_map[i][j]]
            for r in cell:
                move_robot(tile_map, r, sec+1)
    if tree in (screen := generate_screen(tile_map)):
        print(screen)
        print("Seconds:", sec+1)
        break
