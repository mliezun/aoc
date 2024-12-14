from collections import defaultdict
from typing import Optional
import random


garden = """
AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
"""

garden = open("input.txt", "r").read().strip()

garden = [list(l.strip()) for l in garden.splitlines() if l.strip()]


DIRECTIONS = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0),
]


def find_next(garden: list[list[str]], explored_plots: set):
    for i in range(len(garden)):
        for j in range(len(garden[i])):
            if (i, j) not in explored_plots:
                return (i, j)
    return None


def find_regions(garden: list[list[str]]):
    current_region = set()
    all_regions = []
    explored_plots = set()
    queue = [(0, 0)]

    while queue:
        x, y = queue.pop(0)
        if not current_region:
            current_region.add((x, y))

        if (x, y) in explored_plots:
            if not queue:
                all_regions.append(current_region)
                current_region = set()
                next_to_explore = find_next(garden, explored_plots)
                if next_to_explore:
                    queue.append(next_to_explore)
            continue
        explored_plots.add((x, y))

        continue_exploring = False
        for dx, dy in DIRECTIONS:
            try:
                assert x + dx >= 0 and y + dy >= 0
                if garden[x + dx][y + dy] == garden[x][y]:
                    continue_exploring = True
                    current_region.add((x + dx, y + dy))
                    queue.append((x + dx, y + dy))
            except Exception:
                pass

        if not continue_exploring:
            all_regions.append(current_region)
            current_region = set()
            if not queue:
                next_to_explore = find_next(garden, explored_plots)
                if next_to_explore:
                    queue.append(next_to_explore)

    return all_regions


def calculate_outer_perimeter(points: set):
    perimeter = 0
    for x, y in points:
        for dx, dy in DIRECTIONS:
            if (x + dx, y + dy) not in points:
                perimeter += 1
    return perimeter


def find_segments(sides: set):
    current_side = sides.pop()
    x, y, d = current_side
    current_segment = [(x, y, d)]
    i = 1
    while d == "u" and ((x, y + i, "u") in sides or (x, y - i, "u") in sides):
        if (x, y + i, "u") in sides:
            sides.remove((x, y + i, "u"))
            current_segment.append((x, y + i, "u"))
        if (x, y - i, "u") in sides:
            sides.remove((x, y - i, "u"))
            current_segment.append((x, y - i, "u"))
        i += 1
    k = 1
    while d == "d" and ((x, y + k, "d") in sides or (x, y - k, "d") in sides):
        if (x, y + k, "d") in sides:
            sides.remove((x, y + k, "d"))
            current_segment.append((x, y + k, "d"))
        if (x, y - k, "d") in sides:
            sides.remove((x, y - k, "d"))
            current_segment.append((x, y - k, "d"))
        k += 1
    j = 1
    while d == "r" and ((x - j, y, "r") in sides or (x + j, y, "r") in sides):
        if (x - j, y, "r") in sides:
            sides.remove((x - j, y, "r"))
            current_segment.append((x - j, y, "r"))
        if (x + j, y, "r") in sides:
            sides.remove((x + j, y, "r"))
            current_segment.append((x + j, y, "r"))
        j += 1
    m = 1
    while d == "l" and ((x - m, y, "l") in sides or (x + m, y, "l") in sides):
        if (x - m, y, "l") in sides:
            sides.remove((x - m, y, "l"))
            current_segment.append((x - m, y, "l"))
        if (x + m, y, "l") in sides:
            sides.remove((x + m, y, "l"))
            current_segment.append((x + m, y, "l"))
        m += 1
    if sides:
        return [current_segment] + find_segments(sides)
    return [current_segment]


def calculate_number_of_sides(points: set):
    sides = set()
    for x, y in points:
        for dx, dy in DIRECTIONS:
            if (x + dx, y + dy) not in points:
                if dx != 0:
                    sides.add((x + dx, y + dy, "d" if dx > 0 else "u"))
                if dy != 0:
                    sides.add((x + dx, y + dy, "r" if dy > 0 else "l"))
    sides = list(sides)
    sides.sort()
    segments = find_segments(sides)
    assert len(segments) >= 4
    assert len(sides) == 0
    # print(garden[x][y], len(segments), len(points))
    return len(segments)


result = 0
count_points = 0
for reg in find_regions(garden):
    count_points += len(reg)
    num_sides = calculate_number_of_sides(reg)
    result += num_sides * len(reg)
assert count_points == sum(len(row) for row in garden)
print(result)
