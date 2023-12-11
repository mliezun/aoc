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

universe = open("input.txt", "r").read().strip()


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
            expanded_universe.append(["."] * len(universe[i]))
        expanded_universe.append(universe[i].copy())
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
                expanded_universe[i].insert(j + d_j, ".")
            d_j += 1
    return expanded_universe


def find_shortest_length(g_src, g_dst) -> int:
    delta = (g_dst[0] - g_src[0], g_dst[1] - g_src[1])
    return abs(delta[0]) + abs(delta[1])


def get_galaxies(universe):
    galaxies = []
    for i in range(len(universe)):
        for j in range(len(universe[i])):
            if universe[i][j] == "#":
                galaxies.append((i, j))
    return galaxies


def galaxies_distances(universe):
    galaxies = get_galaxies(universe)
    distances = []
    for g1, g2 in list(combinations(galaxies, 2)):
        # print(g1, g2)
        distances.append(find_shortest_length(g1, g2))
    return distances


universe = expand_universe(universe)
# print('\n'.join([''.join(g) for g in universe]))

distances = galaxies_distances(universe)
# print(distances)
print("result:", sum(distances))
