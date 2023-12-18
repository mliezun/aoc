import heapq

heat = """111111111111
999999999991
999999999991
999999999991
999999999991"""

heat = open("input.txt", "r").read().strip()


heat = [list(map(int, h.strip())) for h in heat.splitlines() if h.strip()]


def astar(heat):
    # Distance, row, column, direction, same direction count
    queue = [(0, 0, 0, -1, -1)]
    distances = {}
    while queue:
        dist, x, y, d, sdc = heapq.heappop(queue)
        if (x, y, d, sdc) in distances:
            continue
        distances[(x, y, d, sdc)] = dist
        for new_d, (dx, dy) in enumerate([(0, 1), (1, 0), (0, -1), (-1, 0)]):
            new_x = x + dx
            new_y = y + dy
            new_sdc = sdc + 1 if new_d == d else 1
            is_reverse = (new_d + 2) % 4 == d
            has_4_moves = (
                (dy == 1 and len(heat[0])-new_y >= 4) or
                (dy == -1 and new_y >= 3) or
                (dx == 1 and len(heat)-new_x >= 4) or
                (dx == -1 and new_x >= 3)
            )
            is_valid = (new_sdc <= 10 and (new_d == d or ((sdc >= 4 or sdc == -1) and has_4_moves)))
            if (
                0 <= new_x < len(heat)
                and 0 <= new_y < len(heat[0])
                and not is_reverse
                and is_valid
            ):
                added_heat = heat[new_x][new_y]
                heapq.heappush(queue, (dist + added_heat, new_x, new_y, new_d, new_sdc))

    result = float("inf")
    for (x, y, _, _), v in distances.items():
        if x == len(heat) - 1 and y == len(heat[0]) - 1:
            result = min(result, v)

    return result


print("result:", astar(heat))
