patterns = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""

patterns = open("input.txt", "r").read().strip()


patterns = [[list(r) for r in p.splitlines()] for p in patterns.split("\n\n") if p]


def column_match(pattern, c1, c2):
    for i in range(len(pattern)):
        if pattern[i][c1] != pattern[i][c2]:
            return False
    return True


def row_match(pattern, r1, r2):
    for j in range(len(pattern[0])):
        if pattern[r1][j] != pattern[r2][j]:
            return False
    return True


def pattern_match_value(pattern):
    # Store tuples of index and size
    rows_ranges = []
    for i in range(len(pattern) - 1):
        if row_match(pattern, i, i + 1):
            dx = 1
            while 0 <= i - dx and i + 1 + dx < len(pattern):
                if row_match(pattern, i - dx, i + 1 + dx):
                    dx += 1
                else:
                    break
            # if 0 <= i-dx and i+1+dx < len(pattern):
            #     rows_ranges.append((i, dx))
            # else:
            #     rows_ranges.append((i, max(len(pattern)-dx, dx-len(pattern))))
            # # attempt 2
            # if i+1+dx >= len(pattern):
            #     rows_ranges.append((i, i+1))
            # else:
            #     rows_ranges.append((i, dx))
            if not (0 <= i - dx and i + 1 + dx < len(pattern)):
                rows_ranges.append((i, dx))

    column_ranges = []
    # print("row range:", rows_ranges)
    for j in range(len(pattern[0]) - 1):
        if column_match(pattern, j, j + 1):
            dy = 1
            while 0 <= j - dy and j + 1 + dy < len(pattern[0]):
                if column_match(pattern, j - dy, j + 1 + dy):
                    dy += 1
                else:
                    break
            # if 0 <= j-dy and j+1+dy < len(pattern[0]):
            #     column_ranges.append((j, dy))
            # else:
            #     column_ranges.append((j, max(len(pattern[0])-dy, dy-len(pattern[0]))))
            # # attempt 2
            # if j+1+dy >= len(pattern[0]):
            #     column_ranges.append((j, j+1))
            # else:
            #     column_ranges.append((j, dy))
            if not (0 <= j - dy and j + 1 + dy < len(pattern[0])):
                column_ranges.append((j, dy))
    # print("column range:", column_ranges)

    if column_ranges:
        max_column = max(column_ranges, key=lambda x: x[1])
    else:
        max_column = (-1, -1)

    if rows_ranges:
        max_row = max(rows_ranges, key=lambda x: x[1])
    else:
        max_row = (-1, -1)

    if max_row[1] > max_column[1]:
        return 100 * (max_row[0] + 1)
    return max_column[0] + 1


accum = 0
for pattern in patterns:
    value = pattern_match_value(pattern)
    accum += value

print("result:", accum)
