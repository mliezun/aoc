from itertools import combinations


universe = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""

EXPANSION_RATE = 10

universe = open("input.txt", "r").read().strip()

EXPANSION_RATE = 1000000

universe = [list(g.strip()) for g in universe.splitlines() if g.strip()]


def expand_universe(universe: list[list]):
    expanded_universe = []
    for i in range(len(universe)):
        all_empty = True
        for j in range(len(universe[i])):
            if universe[i][j] != ".":
                all_empty = False
                break
        if all_empty:
            expanded_universe.append([(".", EXPANSION_RATE - 1)] * len(universe[i]))
        expanded_universe.append([(g, 1) for g in universe[i]])
    d_j = 0
    for j in range(len(universe[0])):
        all_empty = True
        for i in range(len(universe)):
            if universe[i][j] != ".":
                all_empty = False
                break
        if all_empty:
            # Add column
            for i in range(len(expanded_universe)):
                expanded_universe[i].insert(j + d_j, (".", EXPANSION_RATE - 1))
            d_j += 1
    return expanded_universe


def find_shortest_length(universe, g_src, g_dst) -> int:
    steps = []
    x, y = g_src
    dx, dy = (g_dst[0] - g_src[0], g_dst[1] - g_src[1])
    if dx:
        step_x = -1 if dx < 0 else 1
        for ddx in range(1, abs(dx) + 1):
            steps.append((x + step_x * ddx, y))
    if dy:
        step_y = -1 if dy < 0 else 1
        for ddy in range(1, abs(dy) + 1):
            steps.append((x, y + step_y * ddy))
    travel_length = 0
    for step in steps:
        i, j = step
        travel_length += universe[i][j][1]
    return travel_length


def get_galaxies(universe):
    galaxies = []
    for i in range(len(universe)):
        for j in range(len(universe[i])):
            if universe[i][j][0] == "#":
                galaxies.append((i, j))
    return galaxies


def galaxies_distances(universe):
    galaxies = get_galaxies(universe)
    distances = []
    for g1, g2 in list(combinations(galaxies, 2)):
        distances.append(find_shortest_length(universe, g1, g2))
    return distances


universe = expand_universe(universe)
# print('\n'.join([str(g) for g in universe]))

distances = galaxies_distances(universe)
# print(distances)
print("result:", sum(distances))
