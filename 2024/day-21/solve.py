from collections import defaultdict
from typing import Optional
import networkx as nx


codes = """029A
980A
179A
456A
379A"""

codes = open("input.txt", "r").read().strip()

codes = [l.strip() for l in codes.splitlines() if l.strip()]


DIRS_MAP = {
    (0, 1): '>',
    (0, -1): '<',
    (-1, 0): '^',
    (1, 0): 'v',
}

MAP_DIRS = {}
for v, k in DIRS_MAP.items():
    MAP_DIRS[k] = v

def as_commands(dirs: list[tuple[int, int]]):
    cmds = ''
    for dir in dirs:
        cmds += DIRS_MAP[dir]
    return cmds + 'A'


class BasicKeypad:
    def __init__(self, layout: list[list[str]]):
        self.layout = layout
        self.key_pos = {}
        self.pos_key = {}
        self.graph = nx.DiGraph()
        for i in range(len(self.layout)):
            for j in range(len(self.layout[i])):
                self.key_pos[self.layout[i][j]] = (i, j)
                self.pos_key[(i, j)] = self.layout[i][j]
                if self.layout[i][j] == 'A':
                    self.pos = (i, j)
                    
                # Build graph
                for dx, dy in DIRS_MAP.keys():
                    new_x, new_y = i+dx, j+dy
                    if 0 <= new_x < len(self.layout) and 0 <= new_y < len(self.layout[0]) and self.layout[new_x][new_y] != ' ':
                        self.graph.add_edge((i, j), (new_x, new_y))
        
    def move_to(self, key: str):
        x, y = self.pos
        to_x, to_y = self.key_pos[key]
        if x == to_x and y == to_y:
            return [[]]
        
        delta_paths = []
        for path in nx.all_shortest_paths(self.graph, (x, y), (to_x, to_y)):
            deltas = []
            new_x, new_y = path[0]
            for next_x, next_y in path[1:]:
                deltas.append((next_x-new_x, next_y-new_y))
                new_x, new_y = next_x, next_y
            delta_paths.append(deltas)
        return delta_paths
    
    def set_pos_to_key(self, key: str) -> tuple[int, int]:
        self.pos = self.key_pos[key]
        return self.pos
    
    def copy(self) -> "BasicKeypad":
        other = self.__class__()
        other.pos = self.pos
        return other

class NumericKeypad(BasicKeypad):
    def __init__(self):
        super().__init__([
            ['7', '8', '9'],
            ['4', '5', '6'],
            ['1', '2', '3'],
            [' ', '0', 'A'],
        ])
        

class DirectionalKeypad(BasicKeypad):
    def __init__(self):
        super().__init__([
            [' ', '^', 'A'],
            ['<', 'v', '>'],
        ])

def compute_all_possible_moves_for_keys(keys: str, keypad: BasicKeypad):
    key_queue = list(keys)
    moves_so_far = ['']
    while key_queue:
        k = key_queue.pop(0)
        moves_so_far_update = []
        for next_moves in compute_possible_moves_for_single_key(k, keypad):
            for previous_moves in moves_so_far:
                moves_so_far_update.append(previous_moves+next_moves)
        moves_so_far = moves_so_far_update
        keypad.set_pos_to_key(k)
    return moves_so_far
    
def compute_possible_moves_for_single_key(key: str, keypad: BasicKeypad) -> list[str]:
    delta_paths = keypad.move_to(key)
    return list(map(as_commands, delta_paths))


def reverse_from(cmds: str, keypad: BasicKeypad) -> str:
    pos = keypad.pos
    result = ''

    for c in cmds:
        if c == 'A':
            result += keypad.pos_key[pos]
        else:
            dx, dy = MAP_DIRS[c]
            pos = (pos[0] + dx, pos[1] + dy)

    return result



def compute_results(codes: list[str]):
    numeric_keypad = NumericKeypad()
    directional_1 = DirectionalKeypad()
    directional_2 = DirectionalKeypad()

    result = 0
    for code in codes:
        directional_2_results = []
        numeric_options = compute_all_possible_moves_for_keys(code, numeric_keypad)
        for numeric_keys in numeric_options:
            directional_1_options = compute_all_possible_moves_for_keys(numeric_keys, directional_1)
            for directional_1_keys in directional_1_options:
                directional_2_options = compute_all_possible_moves_for_keys(directional_1_keys, directional_2)
                for directional_2_keys in directional_2_options:
                    directional_2_results.append((numeric_keys, directional_1_keys, directional_2_keys))
        min_pushes = min(directional_2_results, key=lambda r: len(r[-1]))
        result += len(min_pushes[-1]) * int(code.replace('A', ''))
        numeric_keypad.set_pos_to_key(code[-1])
        directional_1.set_pos_to_key(min_pushes[0][-1])
        directional_2.set_pos_to_key(min_pushes[1][-1])

    return result

print(compute_results(codes))

# result = reverse_from('<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A', DirectionalKeypad())
# print(result)
# result = reverse_from(result, DirectionalKeypad())
# print(result)
# result = reverse_from(result, NumericKeypad())
# print(result)

