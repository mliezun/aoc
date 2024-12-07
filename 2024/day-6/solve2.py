from collections import defaultdict
from typing import Optional


guard_map = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

guard_map = open("input.txt", "r").read().strip()

guard_map = [list(l.strip()) for l in guard_map.splitlines() if l.strip()]

guard_pos = (0, 0)
for i in range(len(guard_map)):
    for j in range(len(guard_map[i])):
        if guard_map[i][j] == "^":
            guard_pos = (i, j)

DIRECTIONS = [
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1),
]
guard_map[guard_pos[0]][guard_pos[1]] = "."


def move_guard(guard_map, guard_pos):
    guard_orientation = 0
    visited_positions = set((guard_pos, guard_orientation))
    try:
        # while True
        for _ in range(10_000_000):
            dx, dy = DIRECTIONS[guard_orientation]
            x, y = guard_pos
            new_x, new_y = x + dx, y + dy
            assert new_x >= 0 and new_y >= 0
            if guard_map[new_x][new_y] == ".":
                guard_pos = (new_x, new_y)
                # Detected cycle
                if (guard_pos, guard_orientation) in visited_positions:
                    return True
                visited_positions.add((guard_pos, guard_orientation))
            else:
                guard_orientation = (guard_orientation + 1) % 4
    except (KeyError, AssertionError, IndexError) as e:
        return False


result = 0
for i in range(len(guard_map)):
    for j in range(len(guard_map[i])):
        og = guard_map[i][j]
        guard_map[i][j] = "#"
        if move_guard(guard_map, guard_pos):
            result += 1
        guard_map[i][j] = og

print(result)
