from collections import defaultdict
from typing import Optional


topo_map = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""

topo_map = open("input.txt", "r").read().strip()

topo_map = [
    [int(e) for e in list(l.strip())] for l in topo_map.splitlines() if l.strip()
]


def find_zeroes(topo_map: list[list[int]]) -> list[list[int]]:
    indexes = []
    for i, r in enumerate(topo_map):
        for j, e in enumerate(r):
            if e == 0:
                indexes.append((i, j))
    return indexes


DIRECTIONS = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0),
]


def find_trail(
    topo_map: list[list[int]],
    starting_pos: list[int],
    trail: Optional[list[int]] = None,
):
    i, j = starting_pos
    if not trail:
        trail = [(i, j)]
    if i < 0 or j < 0 or i >= len(topo_map) or j >= len(topo_map[i]):
        return []
    if topo_map[i][j] == 9:
        return trail
    trails_found = []
    for dx, dy in DIRECTIONS:
        try:
            assert i + dx >= 0 and j + dy >= 0
            if topo_map[i + dx][j + dy] == topo_map[i][j] + 1:
                next_pos = (i + dx, j + dy)
                trails_found.append(find_trail(topo_map, next_pos, trail + [next_pos]))
        except (IndexError, AssertionError):
            pass
    return trails_found


def flatten(trails: list):
    if len(trails) > 0:
        if not isinstance(trails[0], tuple):
            return sum([flatten(el) for el in trails], start=[])
        return [trails]
    return []


result = 0
for zero in find_zeroes(topo_map):
    found_trails = set(map(tuple, flatten(find_trail(topo_map, zero))))
    result += len(found_trails)
print(result)
