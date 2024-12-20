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


def cheat(a_x, a_y, b_x, b_y):
    global result
    picoseconds = distance(a_x, b_x) + distance(a_y, b_y)
    if (
        picoseconds <= 20
        and saved(racetrack[a_y][a_x], racetrack[b_y][b_x], picoseconds) >= 100
    ):
        result += 1


def saved(a, b, steps):
    return abs(a - b) - steps


def distance(a, b):
    return abs(a - b)


result = 0
for y in range(1, len(race_map) - 1):
    for x in range(1, len(race_map[0]) - 1):
        if racetrack[y][x] != -1:
            for d_y in range(1, len(race_map) - 1):
                for d_x in range(1, len(race_map[0]) - 1):
                    if racetrack[d_y][d_x] != -1 and not (y == d_y and x == d_x):
                        cheat(x, y, d_x, d_y)

print(result // 2)
