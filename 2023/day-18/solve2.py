import shapely


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


def dig_lagoon_edges(dig_plan):
    current = (0, 0)
    digged_cubes = [current]
    dir_map_numbers = {"0": "R", "1": "D", "2": "L", "3": "U"}
    dir_map = {"R": (0, 1), "L": (0, -1), "U": (-1, 0), "D": (1, 0)}
    edge_area = 0
    for _, _, hex_color in dig_plan:
        hex_color = hex_color[2:-1]
        distance = int(hex_color[:5], base=16)
        direction = dir_map_numbers[hex_color[5]]
        print(hex_color, distance, direction)
        x, y = current
        edge_area += distance
        dx, dy = dir_map[direction]
        next_pos = (x+dx*distance, y+dy*distance)
        digged_cubes.append(next_pos)
        current = next_pos
    return digged_cubes, edge_area


lagoon_edges, edge_area = dig_lagoon_edges(dig_plan)
print(lagoon_edges)
p = shapely.Polygon(lagoon_edges)
# i: interior points, b: edge points (edge_area)
# A = i + b/2 - 1 (p.area)
# i = A - b/2 + 1
# lagoon_size = i + b = A + b/2 + 1
print("result:", p.area+edge_area/2+1)
