from math import inf

lines = open("input.txt", "r").read().strip().splitlines()


def get_adjacent_positions(keypad_map, position):
    directions = {"<": (0, -1), ">": (0, 1), "^": (-1, 0), "v": (1, 0)}
    adjacent = []
    for move, (dx, dy) in directions.items():
        neighbor = (position[0] + dx, position[1] + dy)
        if neighbor in keypad_map:
            adjacent.append((neighbor, move))
    return adjacent


def enumerate_paths(start, target, keypad):
    position_map = {v: k for k, v in keypad.items()}
    start_pos = keypad[start]
    paths = []

    def traverse(current, route, visited):
        if position_map[current] == target:
            paths.append(route + ["A"])
            return
        for next_pos, direction in get_adjacent_positions(position_map, current):
            if next_pos not in visited:
                traverse(next_pos, route + [direction], visited | {next_pos})

    traverse(start_pos, [], {start_pos})
    return paths


memo = {}


def calculate_path_length(sequence, keypad_levels, current_level=0, max_depth=25):
    sequence_key = "".join(sequence)
    if (sequence_key, current_level) in memo:
        return memo[(sequence_key, current_level)]

    keypad = keypad_levels[current_level]
    sequence = ["A"] + sequence
    total_steps = 0

    for idx in range(len(sequence) - 1):
        from_key, to_key = sequence[idx], sequence[idx + 1]
        candidate_paths = enumerate_paths(from_key, to_key, keypad)
        shortest = inf

        for path in candidate_paths:
            if current_level < max_depth:
                path_cost = calculate_path_length(
                    path, keypad_levels, current_level + 1, max_depth
                )
            else:
                path_cost = len(path)
            shortest = min(shortest, path_cost)

        total_steps += shortest

    memo[(sequence_key, current_level)] = total_steps
    return total_steps


numeric_keys = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "0": (3, 1),
    "A": (3, 2),
}

arrow_keys = {
    "^": (0, 1),
    "A": (0, 2),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
}

keypad_map = {level: arrow_keys for level in range(1, 26)}
keypad_map[0] = numeric_keys

result = 0
for code in lines:
    result += int(code[:-1]) * calculate_path_length(
        list(code), keypad_map, max_depth=25
    )
print(result)
