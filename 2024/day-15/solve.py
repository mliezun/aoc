from dataclasses import dataclass
from abc import ABC
from collections import defaultdict
from typing import Optional


lanternfish = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""

lanternfish = open("input.txt", "r").read().strip()

lanternfish = [
    [list(c.strip()) for c in l.strip().splitlines() if c.strip()]
    if i == 0
    else "".join([c.strip() for c in l.splitlines() if c.strip()])
    for i, l in enumerate(lanternfish.split("\n\n"))
    if l.strip()
]

lanternfish_map, lanternfish_moves = lanternfish


DIR_AS_DELTA = {
    ">": (0, 1),
    "<": (0, -1),
    "^": (-1, 0),
    "v": (1, 0),
}


class Entity(ABC):
    def move(self, lanternfish_map: list[list["Entity"]], dir: str) -> bool:
        dx, dy = DIR_AS_DELTA[dir]
        x, y = self.pos
        new_x, new_y = x + dx, y + dy
        if new_x >= len(lanternfish_map) or new_x < 0:
            return False
        if new_y >= len(lanternfish_map) or new_y < 0:
            return False
        if isinstance(lanternfish_map[new_x][new_y], Wall):
            return False

        if lanternfish_map[new_x][new_y].move(lanternfish_map, dir):
            # Store in local variable for swap
            next_entity = lanternfish_map[new_x][new_y]
            # Swap current with next
            lanternfish_map[new_x][new_y] = self
            lanternfish_map[x][y] = next_entity
            next_entity.pos = (x, y)
            self.pos = (new_x, new_y)
            return True
        return False


@dataclass
class Wall(Entity):
    pos: tuple[int, int]

    def move(self, lanternfish_map: list[list["Entity"]], dir: str) -> bool:
        return False


@dataclass
class Empty(Entity):
    pos: tuple[int, int]

    def move(self, lanternfish_map: list[list["Entity"]], dir: str) -> bool:
        return True


@dataclass
class Box(Entity):
    pos: tuple[int, int]


@dataclass
class Robot(Entity):
    pos: tuple[int, int]


CHAR_AS_CLASS: dict[str, Entity] = {
    "#": Wall,
    ".": Empty,
    "@": Robot,
    "O": Box,
}
lanternfish_map: list[list[Entity]] = [
    [CHAR_AS_CLASS[c](pos=(i, j)) for j, c in enumerate(row)]
    for i, row in enumerate(lanternfish_map)
]

ROBOT_ENTITY = None
for row in lanternfish_map:
    for entity in row:
        if isinstance(entity, Robot):
            ROBOT_ENTITY = entity
            break
assert ROBOT_ENTITY

for dir in lanternfish_moves:
    ROBOT_ENTITY.move(lanternfish_map, dir)

result = 0
for i in range(len(lanternfish_map)):
    for j in range(len(lanternfish_map[i])):
        if isinstance(lanternfish_map[i][j], Box):
            result += i * 100 + j
print("Result:", result)
