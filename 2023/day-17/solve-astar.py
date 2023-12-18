# Credits to: https://github.com/jonathanpaulson/AdventOfCode/blob/master/2023/17.py

import heapq

heat = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""

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
            is_valid = new_sdc <= 3
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
