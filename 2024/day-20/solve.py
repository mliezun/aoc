# Thanks to: https://github.com/robhabraken/advent-of-code-2024/tree/main/solutions/20

from collections import defaultdict
from typing import Optional


race_map = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""

race_map = open("input.txt", "r").read().strip()

race_map = [list(l.strip()) for l in race_map.splitlines() if l.strip()]

delta_map = [(-1, 0), (0, 1), (1, 0), (0, -1)]

racetrack = [[0] * len(race_map[0]) for _ in range(len(race_map))]
start = None
end = None

for y in range(len(race_map)):
    for x in range(len(race_map[0])):
        if race_map[y][x] == "#":
            racetrack[y][x] = -1
        elif race_map[y][x] == "S":
            start = (x, y)
        elif race_map[y][x] == "E":
            end = (x, y)

pos = list(start)
previous_x, previous_y = -1, -1

while not (pos[0] == end[0] and pos[1] == end[1]):
    for i in range(4):
        d_y = pos[1] + delta_map[i][0]
        d_x = pos[0] + delta_map[i][1]

        if racetrack[d_y][d_x] != -1 and not (d_x == previous_x and d_y == previous_y):
            racetrack[d_y][d_x] = racetrack[pos[1]][pos[0]] + 1

            previous_x = pos[0]
            previous_y = pos[1]

            pos[0] = d_x
            pos[1] = d_y
            break


def cheat(a, b):
    global result
    if saved(a, b, 2) >= 100:
        result += 1


def saved(a, b, steps):
    return abs(a - b) - steps


result = 0
for y in range(1, len(race_map) - 1):
    for x in range(1, len(race_map[0]) - 1):
        if racetrack[y][x] == -1:
            if racetrack[y - 1][x] != -1 and racetrack[y + 1][x] != -1:
                cheat(racetrack[y - 1][x], racetrack[y + 1][x])
            elif racetrack[y][x - 1] != -1 and racetrack[y][x + 1] != -1:
                cheat(racetrack[y][x - 1], racetrack[y][x + 1])

print("Result:", result)
