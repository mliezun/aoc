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
    found_smudge = False
    for i in range(len(pattern)):
        if pattern[i][c1] != pattern[i][c2]:
            if not found_smudge:
                found_smudge = True
            else:
                return False, found_smudge
    return True, found_smudge


def row_match(pattern, r1, r2):
    found_smudge = False
    for j in range(len(pattern[0])):
        if pattern[r1][j] != pattern[r2][j]:
            if not found_smudge:
                found_smudge = True
            else:
                return False, found_smudge
    return True, found_smudge


def pattern_match_value(pattern):
    # Store tuples of index and size
    rows_ranges = []
    for i in range(len(pattern) - 1):
        smudges = 0
        did_match, found_smudge = row_match(pattern, i, i + 1)
        if found_smudge:
            smudges += 1
            found_smudge = False
        if did_match:
            dx = 1
            while 0 <= i - dx and i + 1 + dx < len(pattern):
                did_match, found_smudge = row_match(pattern, i - dx, i + 1 + dx)
                if found_smudge:
                    smudges += 1
                    found_smudge = False
                if did_match and smudges <= 1:
                    dx += 1
                else:
                    break
            if not (0 <= i - dx and i + 1 + dx < len(pattern)) and smudges == 1:
                rows_ranges.append((i, dx))

    column_ranges = []
    for j in range(len(pattern[0]) - 1):
        smudges = 0
        did_match, found_smudge = column_match(pattern, j, j + 1)
        if found_smudge:
            smudges += 1
            found_smudge = False
        if did_match:
            dy = 1
            while 0 <= j - dy and j + 1 + dy < len(pattern[0]):
                did_match, found_smudge = column_match(pattern, j - dy, j + 1 + dy)
                if found_smudge:
                    smudges += 1
                    found_smudge = False
                if did_match and smudges <= 1:
                    dy += 1
                else:
                    break
            if not (0 <= j - dy and j + 1 + dy < len(pattern[0])) and smudges == 1:
                column_ranges.append((j, dy))

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
