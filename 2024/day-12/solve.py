from collections import defaultdict
from typing import Optional


garden = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
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


result = 0
for reg in find_regions(garden):
    result += calculate_outer_perimeter(reg) * len(reg)
print(result)
