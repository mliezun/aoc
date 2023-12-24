import sys
from collections import defaultdict


hike_map = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""


hike_map = open("input.txt", "r").read().strip()


hike_map = [list(r.strip()) for r in hike_map.splitlines() if r.strip()]


START = (0, 1)
END = (len(hike_map) - 1, len(hike_map[-1]) - 2)

SLOPES = {
    ">": (0, 1),
    "<": (0, -1),
    "^": (-1, 0),
    "v": (1, 0),
}


def neighbors(hike_map, x, y):
    for dx, dy in SLOPES.values():
        if (
            0 <= x + dx < len(hike_map)
            and 0 <= y + dy < len(hike_map[x])
            and hike_map[x + dx][y + dy] != "#"
        ):
            yield (x + dx, y + dy)


def find_paths(hike_map):
    queue = [(1, 0)]
    visited = set()
    paths = defaultdict(list)
    while queue:
        current = queue.pop()
        if current in visited:
            continue
        for next_step in neighbors(hike_map, current[0], current[1]):
            length = 1
            previous = current
            next_pos = next_step
            dead_end = False
            while True:
                ngs = list(neighbors(hike_map, next_pos[0], next_pos[1]))
                if ngs == [previous] and hike_map[next_pos[1]][next_pos[0]] in "<>^v":
                    dead_end = True
                    break
                if len(ngs) != 2:
                    break
                for n in ngs:
                    if n != previous:
                        length += 1
                        previous = next_pos
                        next_pos = n
                        break
            if dead_end:
                continue
            paths[current].append((next_pos, length))
            queue.append(next_pos)
        visited.add(current)
    return paths


def get_path_lengths(hike_map_paths):
    stack = [(START, 0, {START})]
    while stack:
        current, length, visited = stack.pop()
        if current == END:
            yield length
            continue
        for next_pos, path_length in hike_map_paths[current]:
            if next_pos not in visited:
                stack.append((next_pos, length + path_length, visited | {next_pos}))


hike_map_paths = find_paths(hike_map)
print("result:", max(get_path_lengths(hike_map_paths)))
