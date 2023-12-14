rocks = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""

rocks = open("input.txt", "r").read().strip()

rocks = [list(row.strip()) for row in rocks.splitlines() if row.strip()]

for i in range(len(rocks)):
    for j in range(len(rocks[i])):
        rock = rocks[i][j]
        if rock == 'O':
            k = i
            while k > 0:
                if rocks[k-1][j] == '.':
                    rocks[k-1][j] = 'O'
                    rocks[k][j] = '.'
                else:
                    break
                k -= 1

accum = 0
for i, r in enumerate(rocks):
    accum += r.count('O')*(len(rocks)-i)
    
print("result:", accum)
