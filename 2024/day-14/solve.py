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

straight_lines = [
    [
        tuple(map(int, v.replace("p=", "").replace("v=", "").split(",")))
        for v in l.split(" ")
    ]
    for l in straight_lines.splitlines()
    if l.strip()
]


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

    new_y = y + vy
    if new_y >= len(tile_map):
        new_y = new_y - len(tile_map)
    elif new_y < 0:
        new_y = len(tile_map) - abs(new_y)
    new_x = x + vx
    if new_x >= len(tile_map[0]):
        new_x = new_x - len(tile_map[0])
    elif new_x < 0:
        new_x = len(tile_map[0]) - abs(new_x)

    robot.pos = (new_x, new_y)
    tile_map[new_y][new_x].append(robot)


for p, v in straight_lines:
    x, y = p
    tile_map[y][x].append(Robot(p, v, 0))

for sec in range(100):
    for i in range(len(tile_map)):
        for j in range(len(tile_map[0])):
            cell = [r for r in tile_map[i][j]]
            for r in cell:
                move_robot(tile_map, r, sec + 1)


middle_horizontal = len(tile_map) // 2
assert len(tile_map) % 2 != 0

middle_vertical = len(tile_map[0]) // 2
assert len(tile_map[0]) % 2 != 0


def quadrant(i: int, j: int) -> int:
    if i < middle_horizontal:
        if j < middle_vertical:
            return 0
        elif j > middle_vertical:
            return 1
    elif i > middle_horizontal:
        if j < middle_vertical:
            return 2
        elif j > middle_vertical:
            return 3
    return None


robots_per_quadrant = defaultdict(int)
for i in range(len(tile_map)):
    for j in range(len(tile_map[i])):
        robots_per_quadrant[quadrant(i, j)] += len(tile_map[i][j])

result = 1
for q, v in robots_per_quadrant.items():
    if q is not None:
        result *= v

print(result)
