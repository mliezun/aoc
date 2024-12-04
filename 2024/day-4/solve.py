from collections import defaultdict
from typing import Optional


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

DIRECTIONS = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0),
    (1, 1),
    (1, -1),
    (-1, 1),
    (-1, -1),
]

SEARCH_WORD = "XMAS"

def search_direction(
    words: list[list[str]],
    direction: tuple[int, int],
    pos: tuple[int, int],
    path: Optional[list] = None,
) -> int:
    if not path:
        path = []
    if len(path) > len(SEARCH_WORD):
        return 0
    x, y = pos
    try:
        if words[x][y] == SEARCH_WORD[len(path)]:
            new_path = path + [(x, y)]
            if len(new_path) == len(SEARCH_WORD):
                return 1
            dx, dy = direction
            new_x, new_y = x+dx, y+dy
            assert new_x >= 0 and new_y >= 0
            return search_direction(words, direction, (new_x, new_y), new_path)
    except (IndexError, AssertionError):
        pass
    return 0


xs = []
for i in range(len(words)):
    for j in range(len(words[i])):
        if words[i][j] == "X":
            xs.append((i, j))
            
xmas_count = 0
for pos in xs:
    for dir in DIRECTIONS:
        xmas_count += search_direction(words, dir, pos)
        

print(xmas_count)
