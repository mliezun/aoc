
dig_plan = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""


dig_plan = open("input.txt", "r").read().strip()

dig_plan = [line.split(" ") for line in dig_plan.splitlines() if line.strip()]


# Result: 44307 (too high)

def dig_lagoon_edges(dig_plan):
    current = (0, 0, "")
    digged_cubes = {current}
    dir_map = {"R": (0, 1), "L": (0, -1), "U": (-1, 0), "D": (1, 0)}
    for direction, distance, _ in dig_plan:
        x, y, _ = current
        dx, dy = dir_map[direction]
        for i in range(1, int(distance)+1):
            next_pos = (x+dx*i, y+dy*i, direction)
            digged_cubes.add(next_pos)
        current = next_pos
    return digged_cubes

def normalize_lagoon_edges(lagoon_edges):
    min_x = min(lagoon_edges, key=lambda x: x[0])[0]
    min_y = min(lagoon_edges, key=lambda x: x[1])[1]
    new_lagoon_edges = set()
    for x, y, direction in lagoon_edges:
        new_lagoon_edges.add((x+abs(min_x), y+abs(min_y), direction))
    return new_lagoon_edges

def lagoon_as_graphic(lagoon_edges):
    max_x = max(lagoon_edges, key=lambda x: x[0])[0]*2
    max_y = max(lagoon_edges, key=lambda x: x[1])[1]*2
    graphic = [["." for _ in range(max_y+1)] for _ in range(max_x+1)]
    map_direction_rev = {"L": (0, 1), "R": (0, -1), "D": (-1, 0), "U": (1, 0), "": (0, 0)}
    for x, y, direction in lagoon_edges:
        dx, dy = map_direction_rev[direction]
        graphic[x*2][y*2] = "#"
        if 0 <= x*2+dx <= max_x and 0 <= y*2+dy <= max_y:
            graphic[x*2+dx][y*2+dy] = "x"
    return graphic

def print_lagoon(lagoon_graphic):
    return "\n".join(["".join(r) for r in lagoon_graphic])

def element_neighbors(lagoon_graphic, element):
    visited = set()
    queue = [element]
    is_internal = True
    while queue:
        current = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)
        x, y = current
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if 0 <= x+dx < len(lagoon_graphic) and 0 <= y+dy < len(lagoon_graphic[0]):
                if lagoon_graphic[x+dx][y+dy] == ".":
                    queue.append((x+dx, y+dy))
                    if x+dx in [0, len(lagoon_graphic)-1] or y+dy in [0, len(lagoon_graphic[0])-1]:
                        is_internal = False
    return visited, is_internal

def dig_lagoon_interior(lagoon_graphic):
    non_interior = set()
    print(len(lagoon_graphic), len(lagoon_graphic[0]))
    for i, r in enumerate(lagoon_graphic):
        for j, c in enumerate(r):
            if c == '.' and (i, j) not in non_interior:
                neighbors, is_interior = element_neighbors(lagoon_graphic, (i, j))
                # print((i, j), is_interior)
                if is_interior:
                    return neighbors
                else:
                    non_interior = non_interior.union(neighbors)
    return non_interior
    
        
lagoon_edges = dig_lagoon_edges(dig_plan)
lagoon_edges = normalize_lagoon_edges(lagoon_edges)
lagoon_graphic = lagoon_as_graphic(lagoon_edges)
# print(print_lagoon(lagoon_graphic))
interior = dig_lagoon_interior(lagoon_graphic)
# only pairs
pairs = set([(x//2, y//2) for x, y in interior if x%2==0 and y%2==0])
edges = set([(x, y) for x, y, _ in lagoon_edges])
print("result:", len(edges.union(pairs)))
# print(pairs.union(edges))
# print("\r\nresult:", len(digged))
