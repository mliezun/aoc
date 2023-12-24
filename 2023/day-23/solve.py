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
    if hike_map[x][y] in SLOPES.keys():
        dx, dy = SLOPES[hike_map[x][y]]
        yield (x + dx, y + dy)
    else:
        for dx, dy in SLOPES.values():
            if (
                0 <= x + dx < len(hike_map)
                and 0 <= y + dy < len(hike_map[x])
                and hike_map[x + dx][y + dy] != "#"
            ):
                yield (x + dx, y + dy)


def find_paths(hike_map):
    queue = [START]
    visited = set()
    came_from = defaultdict(set)
    while queue:
        x, y = queue.pop(0)
        if (x, y) in visited:
            continue
        visited.add((x, y))
        for ng in neighbors(hike_map, x, y):
            came_from[ng].add((x, y))
            queue.append(ng)
    return came_from


def get_longest_path(hike_map_paths, current_pos, step_count, trail_path):
    if current_pos == START:
        return step_count

    if len(trail_path) != len(set(trail_path)):
        return 0

    max_step_count = 0
    for previous in hike_map_paths[current_pos]:
        max_step_count = max(
            get_longest_path(
                hike_map_paths, previous, step_count + 1, trail_path + [previous]
            ),
            max_step_count,
        )

    return max_step_count


print("result:", get_longest_path(find_paths(hike_map), END, 0, []))
