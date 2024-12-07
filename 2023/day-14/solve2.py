from collections import defaultdict

rocks = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""

rocks = open("input.txt", "r").read().strip()

rocks = [list(row.strip()) for row in rocks.splitlines() if row.strip()]


def go_north(rocks):
    for i in range(len(rocks)):
        for j in range(len(rocks[i])):
            rock = rocks[i][j]
            if rock == "O":
                k = i
                while k > 0:
                    if rocks[k - 1][j] == ".":
                        rocks[k - 1][j] = "O"
                        rocks[k][j] = "."
                    else:
                        break
                    k -= 1
    return rocks


def go_south(rocks):
    for i in range(len(rocks) - 1, -1, -1):
        for j in range(len(rocks[i])):
            rock = rocks[i][j]
            if rock == "O":
                k = i
                while k < len(rocks) - 1:
                    if rocks[k + 1][j] == ".":
                        rocks[k + 1][j] = "O"
                        rocks[k][j] = "."
                    else:
                        break
                    k += 1
    return rocks


def go_east(rocks):
    for i in range(len(rocks)):
        for j in range(len(rocks[i]) - 1, -1, -1):
            rock = rocks[i][j]
            if rock == "O":
                k = j
                while k < len(rocks[i]) - 1:
                    if rocks[i][k + 1] == ".":
                        rocks[i][k + 1] = "O"
                        rocks[i][k] = "."
                    else:
                        break
                    k += 1
    return rocks


def go_west(rocks):
    for i in range(len(rocks)):
        for j in range(len(rocks[i])):
            rock = rocks[i][j]
            if rock == "O":
                k = j
                while k > 0:
                    if rocks[i][k - 1] == ".":
                        rocks[i][k - 1] = "O"
                        rocks[i][k] = "."
                    else:
                        break
                    k -= 1
    return rocks


def do_cycle(rocks):
    rocks = go_north(rocks)
    rocks = go_west(rocks)
    rocks = go_south(rocks)
    rocks = go_east(rocks)
    return rocks


def get_value(rocks):
    accum = 0
    for i, r in enumerate(rocks):
        accum += r.count("O") * (len(rocks) - i)
    return accum


def str_rocks(rocks):
    out = ""
    for row in rocks:
        out += "".join(row) + "\n"
    return out


rock_id = 0
rock_ids = {}
repeated_cycles = defaultdict(int)
cycle_value = {}
CYCLES = 1000000000
for _ in range(CYCLES):
    rock_as_str = str_rocks(rocks)
    if rock_as_str in rock_ids:
        print("Found cycle", rock_ids[rock_as_str])
        break
    if rock_as_str not in rock_ids:
        rock_ids[rock_as_str] = rock_id
        rock_id += 1
    repeated_cycles[rock_ids[rock_as_str]] += 1
    if rock_ids[rock_as_str] not in cycle_value:
        cycle_value[rock_ids[rock_as_str]] = get_value(rocks)
    rocks = do_cycle(rocks)


located = rock_ids[rock_as_str] + (CYCLES - rock_ids[rock_as_str]) % (
    1 + max(repeated_cycles.keys()) - rock_ids[rock_as_str]
)

print("result:", cycle_value[located])
