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


def copy_columns(r, times):
    assert times % 2 == 1
    out = []
    for i in range(times):
        if i == times // 2:
            for e in r:
                out.append(e)
        else:
            for e in r:
                out.append(e if e != "S" else ".")
    return out


def copy_rows(rows, times):
    assert times % 2 == 1
    out = []
    for i in range(times):
        if i == times // 2:
            out.extend(rows)
        else:
            out.extend([[e if e != "S" else "." for e in r] for r in rows])
    return out


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
        if i > 2:
            del walked[i - 1]
    return walked[i + 1]


# This was a very tricky one
# See discussion: https://www.reddit.com/r/adventofcode/comments/18nevo3/2023_day_21_solutions/

expansion_rate = 5
expanded_garden = copy_rows(
    [copy_columns(r, expansion_rate) for r in garden], expansion_rate
)
print("After expansion")

STEPS = 26501365
remainder = STEPS % len(garden)
points = []
for i in range(3):
    steps = remainder + len(garden) * i
    print(f"Walking {steps=}")
    points.append(len(walk_garden(expanded_garden, steps)))


print(points)
# Values for quadratic polynomial
a = points[0] / 2 - points[1] + points[2] / 2
b = -3 * points[0] / 2 + 2 * points[1] - points[2] / 2
c = points[0]
N = STEPS // len(garden)

print(a, b, c, N)
print("result:", a * N**2 + b * N + c)
