from collections import defaultdict
from typing import Optional
from itertools import chain


words = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""

words = open("input.txt", "r").read().strip()

words = [list(l.strip()) for l in words.splitlines() if l.strip()]

ROTATIONS = [
    (
        ("M", ".", "S"),
        (".", "A", "."),
        ("M", ".", "S"),
    ),
    (
        ("M", ".", "M"),
        (".", "A", "."),
        ("S", ".", "S"),
    ),
    (
        ("S", ".", "M"),
        (".", "A", "."),
        ("S", ".", "M"),
    ),
    (
        ("S", ".", "S"),
        (".", "A", "."),
        ("M", ".", "M"),
    ),
]

def match_pattern(words, pattern, pos):
    assert len(pattern) == 3, len(pattern[0]) == 3
    
    try:
        x, y = pos
        row1 = list(zip(words[x][y:], pattern[0]))
        row2 = list(zip(words[x+1][y:], pattern[1]))
        row3 = list(zip(words[x+2][y:], pattern[2]))
        assert (len(row1), len(row2), len(row3)) == (3,)*3
        for a, b in chain(row1, row2, row3):
            if a != b and b != '.':
                return 0
        return 1
    except (IndexError, AssertionError):
        pass
    return 0

match_count = 0
for i in range(len(words)):
    for j in range(len(words[i])):
        for pattern in ROTATIONS:
            match_count += match_pattern(words, pattern, (i, j))
            
print(match_count)
