from dataclasses import dataclass

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
# (15950, 574735, 4715347)
# (0.26s, 10.78s, 238.63s)

MAX_STRAIGHT = 3


@dataclass
class Node:
    # Position
    p: tuple[int, int]
    # Heat
    h: int
    # Direction
    d: tuple[int, int]
    # Direction count
    dc: int

    def __post_init__(self):
        self.record = []

    def is_reverse(self, other_dir: tuple[int, int]) -> bool:
        return self.d[0] == -other_dir[0] and self.d[1] == -other_dir[1]

    def can_go(self, other_dir: tuple[int, int]) -> bool:
        if self.is_reverse(other_dir):
            return False
        if self.d == other_dir and self.dc >= MAX_STRAIGHT:
            return False
        return True

    def go_to(self, other_dir: tuple[int, int], h: int):
        next_node = Node(self.p, self.h + h, self.d, self.dc)
        # assert next_node.can_go(other_dir)
        if next_node.d == other_dir:
            next_node.dc += 1
        else:
            next_node.d = other_dir
            next_node.dc = 1
        x, y = next_node.p
        dx, dy = other_dir
        next_node.p = (x + dx, y + dy)
        # next_node.record = self.record + [self]
        return next_node

    def as_tuple(self):
        return (self.p, self.d, self.dc)

    def distance(self, pos):
        return abs(self.p[0] - pos[0]) + abs(self.p[1] - pos[1])


## Heat limits (880, 590)
## Calculated from AOC hints
CAP_HEAT = 880


def find_path(heat):
    visited = {}
    min_route = None
    final_pos = (len(heat) - 1, len(heat[-1]) - 1)
    alternate = [(0, 1), (1, 0)]
    current_pos = (0, 0)
    i = 0
    h = 0
    while current_pos != final_pos:
        d = alternate[i]
        i = (i + 1) % 2
        x = current_pos[0] + d[0]
        y = current_pos[1] + d[1]
        current_pos = (x, y)
        h += heat[x][y]
        node = Node(p=(x, y), h=h, d=d, dc=1)
        visited[node.as_tuple()] = node.h
        min_route = node
    print("Starting route", min_route)
    to_visit = [
        Node((0, 1), heat[0][1], (0, 1), 1),
        Node((1, 0), heat[1][0], (1, 0), 1),
    ]
    iterations = 0
    while to_visit:
        iterations += 1
        print("\rIterations:", iterations, end="")
        node = to_visit.pop(0)
        if node.p == final_pos:
            if node.h < min_route.h:
                # print("\r\nroute:", node)
                min_route = node
        else:
            if node.h > CAP_HEAT:
                continue
            x, y = node.p
            neighbors = []
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                if (
                    x + dx >= 0
                    and y + dy >= 0
                    and x + dx < len(heat)
                    and y + dy < len(heat[0])
                ):
                    if not node.can_go((dx, dy)):
                        continue
                    h = heat[x + dx][y + dy]
                    if node.h + h > CAP_HEAT:
                        continue
                    if min_route and node.h + h > min_route.h:
                        continue
                    ns = node.go_to((dx, dy), h)
                    if ns.as_tuple() in visited:
                        if ns.h < visited[ns.as_tuple()]:
                            visited[ns.as_tuple()] = ns.h
                        else:
                            continue
                    else:
                        visited[ns.as_tuple()] = ns.h
                    neighbors.append(ns)
            if neighbors:
                sort_key = lambda n: (n.h, n.distance(final_pos))
                min_n = min(neighbors, key=sort_key)
                for n in sorted(neighbors, key=sort_key, reverse=True):
                    if n != min_n:
                        to_visit.append(n)
                    else:
                        to_visit.insert(0, n)
    return min_route


route = find_path(heat)
print("\nresult:", route)
# Starting route Node(p=(140, 140), h=1455, d=(1, 0), dc=1)
# Iterations: 23496624
# result: Node(p=(140, 140), h=861, d=(1, 0), dc=1)
