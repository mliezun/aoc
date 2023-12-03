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

schematic = open('input.txt', 'r').read()


numbers = []
schematic_matrix = [l.strip() for l in schematic.split('\n') if l.strip()]
print(schematic_matrix)
for i, r in enumerate(schematic_matrix):
	number = 0
	adjacent = False
	for j, d in enumerate(r):
		print(i, j, d)
		if d.isdigit():
			number = (number*10) + int(d)
			directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, -1), (1, 1), (-1, 1), (-1, -1)]
			for k, l in directions:
				try:
					x = i+k
					y = j+l
					if schematic_matrix[x][y] != '.' and not schematic_matrix[x][y].isdigit() and x >= 0 and y >= 0:
						adjacent = True
						print('here', i, j, (k, l), d, schematic[i+k][j+l])
						break
				except IndexError:
					pass
		print(d, adjacent and (not d.isdigit() or j+1 == len(r)))
		if adjacent and (not d.isdigit() or j+1 == len(r)):
			adjacent = False
			numbers.append(number)
			number = 0

		if not d.isdigit():
			number = 0

print(numbers)
print(sum(numbers))
