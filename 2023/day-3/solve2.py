from collections import defaultdict

schematic = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""

schematic = open("input.txt", "r").read()


numbers = []
schematic_matrix = [l.strip() for l in schematic.split("\n") if l.strip()]
print(schematic_matrix)
gears = defaultdict(list)
for i, r in enumerate(schematic_matrix):
    number = 0
    adjacent_gears = set()
    for j, d in enumerate(r):
        print(i, j, d)
        if d.isdigit():
            number = (number * 10) + int(d)
            directions = [
                (0, 1),
                (0, -1),
                (1, 0),
                (-1, 0),
                (1, -1),
                (1, 1),
                (-1, 1),
                (-1, -1),
            ]
            for k, l in directions:
                try:
                    x = i + k
                    y = j + l
                    if schematic_matrix[x][y] == "*" and x >= 0 and y >= 0:
                        adjacent_gears.add((x, y))
                        print("here", i, j, (k, l), d, schematic[i + k][j + l])
                        break
                except IndexError:
                    pass

        print(
            d, adjacent_gears, adjacent_gears and (not d.isdigit() or j + 1 == len(r))
        )
        if adjacent_gears and (not d.isdigit() or j + 1 == len(r)):
            for g in adjacent_gears:
                gears[g].append(number)
            number = 0
            adjacent_gears = set()

        if not d.isdigit():
            number = 0

print(gears)
print(sum([nums[0] * nums[1] for g, nums in gears.items() if len(nums) == 2]))
