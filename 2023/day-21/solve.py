garden = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""


garden = open("input.txt", "r").read().strip()


garden = [list(row.strip()) for row in garden.splitlines() if row.strip()]


def str_garden(garden):
    out = ""
    for row in garden:
        out += "".join(row) + "\n"
    return out[:-1]


def neighbors(garden, x, y):
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        if (
            0 <= x + dx < len(garden)
            and 0 <= y + dy < len(garden[0])
            and garden[x + dx][y + dy] in (".", "S")
        ):
            yield (x + dx, y + dy)


def walk_garden(garden, steps):
    current_pos = next(
        (x, y) for x, row in enumerate(garden) for y, c in enumerate(row) if c == "S"
    )
    walked = {0: {current_pos}}
    for i in range(steps):
        walked[i + 1] = set()
        for x, y in walked[i]:
            for nx, ny in neighbors(garden, x, y):
                walked[i + 1].add((nx, ny))
    # for x, y in walked[steps]:
    #     garden[x][y] = "O"
    # print(str_garden(garden))
    return walked[steps]


print("result:", len(walk_garden(garden, 64)))
