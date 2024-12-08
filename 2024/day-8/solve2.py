from collections import defaultdict
from typing import Optional


antenna_map = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""

antenna_map = open("input.txt", "r").read().strip()

antenna_map = [list(l.strip()) for l in antenna_map.splitlines() if l.strip()]

antenna_group = defaultdict(list)
for i in range(len(antenna_map)):
    for j in range(len(antenna_map[i])):
        if antenna_map[i][j] != '.':
            antenna_group[antenna_map[i][j]].append((i, j))
            
def within_range(x: int, y: int, max_x: int, max_y: int):
    return (0 <= x < max_x) and (0 <= y < max_y)

def find_antinodes(positions: list[tuple[int, int]], max_x: int, max_y: int):
    antinodes = []
    for i, p1 in enumerate(positions[:-1]):
        for p2 in positions[i+1:]:
            x1, y1 = p1
            x2, y2 = p2
            assert x1 <= x2
            dx, dy = abs(x1-x2), abs(y1-y2)
            antinodes.append(p1)
            antinodes.append(p2)
            dx_unit, dy_unit = dx, dy
            while True:
                exceeded_map_x = False
                exceeded_map_y = False
                if y1 < y2:
                    a1_x, a1_y = x1-dx, y1-dy
                    a2_x, a2_y = x2+dx, y2+dy
                else:
                    a1_x, a1_y = x1-dx, y1+dy
                    a2_x, a2_y = x2+dx, y2-dy
                if within_range(a1_x, a1_y, max_x, max_y):
                    antinodes.append((a1_x, a1_y))
                else:
                    exceeded_map_x = True
                if within_range(a2_x, a2_y, max_x, max_y):
                    antinodes.append((a2_x, a2_y))
                else:
                    exceeded_map_y = True
                if exceeded_map_y and exceeded_map_x:
                    break
                dx += dx_unit
                dy += dy_unit
    return antinodes


result = set()
for g, pos in antenna_group.items():
    antis = find_antinodes(pos, len(antenna_map), len(antenna_map[1]))
    result.update(antis)

for a, b in result:
    if antenna_map[a][b] == '.':
        antenna_map[a][b] = '#'
print(len(result))

# for row in antenna_map:
#     print(''.join(row))
