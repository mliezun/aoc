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
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""

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


@dataclass
class Entity:
    start_pos: tuple[int, int]
    end_pos: tuple[int, int]

    def move(self, lanternfish_map: list[list["Entity"]], dir: str) -> bool:
        dx, dy = DIR_AS_DELTA[dir]
        x1, y1 = self.start_pos
        new_x1, new_y1 = x1 + dx, y1 + dy
        if new_x1 >= len(lanternfish_map) or new_x1 < 0:
            return False
        if new_y1 >= len(lanternfish_map[0]) or new_y1 < 0:
            return False
        if isinstance(lanternfish_map[new_x1][new_y1], Wall):
            return False
        x2, y2 = self.end_pos
        new_x2, new_y2 = x2 + dx, y2 + dy
        if new_x2 >= len(lanternfish_map) or new_x2 < 0:
            return False
        if new_y2 >= len(lanternfish_map[0]) or new_y2 < 0:
            return False
        if isinstance(lanternfish_map[new_x2][new_y2], Wall):
            return False

        entity1 = lanternfish_map[new_x1][new_y1]
        entity2 = lanternfish_map[new_x2][new_y2]

        the_entity = None
        if entity1 == entity2:
            the_entity = entity1
        elif entity1 == self:
            the_entity = entity2
        elif entity2 == self:
            the_entity = entity1

        if the_entity:
            if the_entity.move(lanternfish_map, dir):
                lanternfish_map[x1][y1] = Empty(start_pos=(x1, y1), end_pos=(x1, y1))
                lanternfish_map[x2][y2] = Empty(start_pos=(x2, y2), end_pos=(x2, y2))
                self.start_pos = (new_x1, new_y1)
                self.end_pos = (new_x2, new_y2)
                lanternfish_map[new_x1][new_y1] = self
                lanternfish_map[new_x2][new_y2] = self
                return True
            return False

        lanternfish_map_aux = [
            [entity.copy() for entity in row] for row in lanternfish_map
        ]
        can_move1 = lanternfish_map_aux[new_x1][new_y1].move(lanternfish_map_aux, dir)
        can_move2 = lanternfish_map_aux[new_x2][new_y2].move(lanternfish_map_aux, dir)
        if not (can_move1 and can_move2):
            return False

        lanternfish_map[new_x1][new_y1].move(lanternfish_map, dir)
        lanternfish_map[new_x2][new_y2].move(lanternfish_map, dir)
        lanternfish_map[x1][y1] = Empty(start_pos=(x1, y1), end_pos=(x1, y1))
        lanternfish_map[x2][y2] = Empty(start_pos=(x2, y2), end_pos=(x2, y2))
        self.start_pos = (new_x1, new_y1)
        self.end_pos = (new_x2, new_y2)
        lanternfish_map[new_x1][new_y1] = self
        lanternfish_map[new_x2][new_y2] = self
        return True

    def copy(self) -> "Entity":
        return self.__class__(self.start_pos, self.end_pos)


class Wall(Entity):
    def move(self, lanternfish_map: list[list["Entity"]], dir: str) -> bool:
        return False


class Empty(Entity):
    def move(self, lanternfish_map: list[list["Entity"]], dir: str) -> bool:
        return True


class Box(Entity):
    pass


class Robot(Entity):
    pass


CHAR_AS_CLASS: dict[str, Entity] = {
    "#": Wall,
    ".": Empty,
    "@": Robot,
    "O": Box,
}
lanternfish_map: list[list[Entity]] = [
    [CHAR_AS_CLASS[c](start_pos=(i, j), end_pos=(i, j)) for j, c in enumerate(row)]
    for i, row in enumerate(lanternfish_map)
]

# Duplicate entities
lanternfish_map_new = []
for i in range(len(lanternfish_map)):
    current_row = []
    for j in range(len(lanternfish_map[i])):
        ent = lanternfish_map[i][j].copy()
        x, y = i, j * 2
        if isinstance(ent, Box):
            ent.start_pos = (x, y)
            ent.end_pos = (x, y + 1)
            current_row.append(ent)
            current_row.append(ent)
        if isinstance(ent, Empty) or isinstance(ent, Wall):
            ent.start_pos = (x, y)
            ent.end_pos = (x, y)
            current_row.append(ent)
            new_ent = ent.copy()
            new_ent.start_pos = (x, y + 1)
            new_ent.end_pos = new_ent.start_pos
            current_row.append(new_ent)
        if isinstance(ent, Robot):
            ent.start_pos = (x, y)
            ent.end_pos = (x, y)
            current_row.append(ent)
            new_ent = Empty(start_pos=(x, y + 1), end_pos=(x, y + 1))
            current_row.append(new_ent)
    lanternfish_map_new.append(current_row)


def print_map(lanternfish_map_new):
    for row in lanternfish_map_new:
        for e in row:
            print(e.__class__.__name__[0], end="")
        print("")


ROBOT_ENTITY = None
for row in lanternfish_map_new:
    for entity in row:
        if isinstance(entity, Robot):
            ROBOT_ENTITY = entity
            break
assert ROBOT_ENTITY


# print_map(lanternfish_map_new)
for i, dir in enumerate(lanternfish_moves):
    ROBOT_ENTITY.move(lanternfish_map_new, dir)
    # print("== STEP ==", i+1, dir)
    # print_map(lanternfish_map_new)
    # print("")

BOXES = []
for row in lanternfish_map_new:
    for ent in row:
        if isinstance(ent, Box) and ent not in BOXES:
            BOXES.append(ent)

result = 0
for box in BOXES:
    result += box.start_pos[0] * 100 + box.start_pos[1]
print("Result:", result)
