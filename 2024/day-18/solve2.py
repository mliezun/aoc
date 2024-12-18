from collections import defaultdict
from typing import Optional
import networkx as nx


fallen_bytes = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
"""
map_size = 7

fallen_bytes = open("input.txt", "r").read().strip()
map_size = 71

fallen_bytes = [
    tuple(map(int, l.strip().split(",")))
    for l in fallen_bytes.splitlines()
    if l.strip()
]


memory_map = [["." for _ in range(map_size)] for _ in range(map_size)]


def build_graph(memory_map):
    G = nx.DiGraph()
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    rows, cols = len(memory_map), len(memory_map[0])

    for x in range(rows):
        for y in range(cols):
            if memory_map[x][y] == "#":
                continue

            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                if (
                    0 <= new_x < rows
                    and 0 <= new_y < cols
                    and memory_map[new_x][new_y] != "#"
                ):
                    G.add_edge((x, y), (new_x, new_y), weight=1)

    return G


def find_shortest_path(memory_map):
    graph = build_graph(memory_map)
    try:
        nx.single_source_dijkstra(
            graph, (0, 0), (len(memory_map) - 1, len(memory_map[0]) - 1)
        )
        return True
    except nx.NetworkXNoPath:
        return False


def binary_search_min(lst, cond_fn):
    left, right = 0, len(lst) - 1
    result = -1
    while left <= right:
        mid = (left + right) // 2
        if cond_fn(mid):
            result = mid
            right = mid - 1
        else:
            left = mid + 1
    return result


def consider_n_bytes(n: int):
    memory_map_copy = [memory_row.copy() for memory_row in memory_map]
    for x, y in fallen_bytes[:n]:
        memory_map_copy[y][x] = "#"
    return not find_shortest_path(memory_map_copy)


ix = binary_search_min(fallen_bytes, consider_n_bytes)
print("result", ",".join(map(str, fallen_bytes[ix - 1])))
