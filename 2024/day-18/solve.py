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
first_bytes = 12

fallen_bytes = open("input.txt", "r").read().strip()
map_size = 71
first_bytes = 1024

fallen_bytes = [
    tuple(map(int, l.strip().split(",")))
    for l in fallen_bytes.splitlines()
    if l.strip()
]


memory_map = [["." for _ in range(map_size)] for _ in range(map_size)]


for i, j in fallen_bytes[:first_bytes]:
    memory_map[j][i] = "#"


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

    return nx.single_source_dijkstra(
        graph, (0, 0), (len(memory_map) - 1, len(memory_map[0]) - 1)
    )


print("result:", find_shortest_path(memory_map)[0])
