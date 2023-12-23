import copy
from collections import defaultdict


bricks = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""


bricks = open("input.txt", "r").read().strip()


def as_coordinates(b: str):
    b, e = b.split("~")
    return tuple(map(int, b.split(","))), tuple(map(int, e.split(",")))


bricks = [
    as_coordinates(brick.strip()) for brick in bricks.splitlines() if brick.strip()
]


def intersection(line1, line2):
    x1, y1, _ = line1[0]
    x2, y2, _ = line1[1]
    x3, y3, _ = line2[0]
    x4, y4, _ = line2[1]
    if max(x1, x2) < min(x3, x4) or min(x1, x2) > max(x3, x4):
        return False
    if max(y1, y2) < min(y3, y4) or min(y1, y2) > max(y3, y4):
        return False
    return True


def disintegrate_v2(bricks):
    sorted_bricks_z = list(sorted(bricks, key=lambda b: min(b[0][2], b[1][2])))
    final_layout = {}
    intersections = defaultdict(list)
    for i, brick in enumerate(sorted_bricks_z):
        z = 1
        for j, other_brick in final_layout.items():
            if intersection(brick, other_brick):
                intersections[i].append(j)
                z = max(z, max(other_brick[0][2], other_brick[1][2]) + 1)
        x1, y1, z1 = brick[0]
        x2, y2, z2 = brick[1]
        h = abs(z2 - z1)
        if z1 < z2:
            z1 = z
            z2 = z1 + h
        else:
            z2 = z
            z1 = z2 + h
        brick_coord = ((x1, y1, z1), (x2, y2, z2))
        final_layout[i] = brick_coord

    filtered_intersections = defaultdict(list)
    for b1, ii in intersections.items():
        brick1 = final_layout[b1]
        for b2 in ii:
            brick2 = final_layout[b2]
            if brick1[1][2] == brick2[0][2] - 1:
                filtered_intersections[b1].append(b2)
            elif brick2[1][2] == brick1[0][2] - 1:
                filtered_intersections[b2].append(b1)

    supported_by_bricks = defaultdict(list)
    for b1, ii in filtered_intersections.items():
        for b2 in ii:
            supported_by_bricks[b2].append(b1)

    accum = 0
    for b in final_layout.keys():
        supported_by_bricks_dis = fall_bricks(supported_by_bricks, b)
        accum += count_unsupported_bricks(supported_by_bricks_dis)
    return accum


def fall_bricks(supported_by_bricks: dict[int, list[int]], brick: int):
    supported_by_bricks = copy.deepcopy(supported_by_bricks)
    queue = [brick]
    while len(queue) > 0:
        brick_id = queue.pop(0)
        for other_brick_id, supported_by in supported_by_bricks.items():
            if other_brick_id == brick_id:
                continue
            if brick_id in supported_by:
                ix = supported_by.index(brick_id)
                del supported_by[ix]
                if len(supported_by) == 0:
                    queue.append(other_brick_id)
    return supported_by_bricks


def count_unsupported_bricks(supported_by_bricks: dict[int, list[int]]):
    accum = 0
    for supported_by in supported_by_bricks.values():
        if not supported_by:
            accum += 1
    return accum


print("result:", disintegrate_v2(bricks))
