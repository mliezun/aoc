from collections import defaultdict


hailstones = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""


TEST_AREA = (7, 27)

TEST_AREA = (200000000000000, 400000000000000)
hailstones = open("input.txt", "r").read().strip()


hailstones = [h.strip().split(" @ ") for h in hailstones.splitlines() if h.strip()]
hailstones = [
    (tuple(map(int, h[0].split(","))), tuple(map(int, h[1].split(","))))
    for h in hailstones
]


def intersect_lines(line1, line2):
    a, b, c, d = line1
    e, f, g, h = line2
    t2 = (h - d - ((f - b) / a * c)) / ((c * e / a) - g)
    t1 = (e * t2 + f - b) / a
    if t1 > 0 and t2 > 0:
        return (a * t1 + b, c * t1 + d)
    return None


def intersection(hail1, hail2):
    # (a*t+b, c*t+d, e*t+f) == (q*t+w, r*t+h, u*t+v)
    # Disregarding Z-axis for now
    (b, d, f), (a, c, e) = hail1
    (w, h, v), (q, r, u) = hail2
    try:
        return intersect_lines((a, b, c, d), (q, w, r, h))
    except ZeroDivisionError:
        return None


def crossing_paths(hailstones):
    intersects = defaultdict(set)
    intersection_count = 0
    for i in range(len(hailstones) - 1):
        h1 = hailstones[i]
        for j in range(i + 1, len(hailstones)):
            h2 = hailstones[j]
            if result := intersection(h1, h2):
                x, y = result
                if (
                    TEST_AREA[0] <= x <= TEST_AREA[1]
                    and TEST_AREA[0] <= y <= TEST_AREA[1]
                ):
                    # print(h1, h2, result)
                    intersects[i].add(j)
                    intersection_count += 1
    return intersects, intersection_count


print("result:", crossing_paths(hailstones)[1])
