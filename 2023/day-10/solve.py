from collections import defaultdict

pipes = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""

pipes = open("input.txt", "r").read().strip()

pipes = pipes.splitlines()
for i, r in enumerate(pipes):
    for j, p in enumerate(r):
        if p == "S":
            starting_pos = (i, j)
            break


def get_delta(pos1, pos2):
    return (pos2[0] - pos1[0], pos2[1] - pos1[1])


def is_opposite(pos1, pos2):
    return (pos1[0] == -pos2[0]) and (pos1[1] == -pos2[1])


def is_closed_loop(start_pos, connections):
    if not connections[start_pos]:
        return False
    max_places = sum([len(r) for r in pipes])
    next_pos = connections[start_pos][0]
    delta = get_delta(start_pos, next_pos)
    already_visited = []
    for _ in range(max_places):
        already_visited.append(next_pos)
        for np in connections[next_pos]:
            if np not in already_visited and not is_opposite(
                get_delta(next_pos, np), delta
            ):
                delta = get_delta(next_pos, np)
                next_pos = np
                break
        if already_visited[-1] == start_pos:
            return True
    return False


compatible_pipes = {
    "L": {
        (0, 1): ["-", "7", "J"],
        (0, -1): [],
        (1, 0): [],
        (-1, 0): ["|", "7", "F"],
    },
    "J": {
        (0, 1): [],
        (0, -1): ["-", "F", "L"],
        (1, 0): [],
        (-1, 0): ["|", "F", "7"],
    },
    "7": {
        (0, 1): [],
        (0, -1): ["-", "F", "L"],
        (1, 0): ["|", "L", "J"],
        (-1, 0): [],
    },
    "F": {
        (0, 1): ["-", "7", "J"],
        (0, -1): [],
        (1, 0): ["|", "L", "J"],
        (-1, 0): [],
    },
    "-": {
        (0, 1): ["-", "7", "J"],
        (0, -1): ["-", "F", "L"],
        (1, 0): [],
        (-1, 0): [],
    },
    "|": {
        (0, 1): [],
        (0, -1): [],
        (1, 0): ["|", "J", "L"],
        (-1, 0): ["|", "7", "F"],
    },
}


def calculate_distances():
    max_distances = []
    for s in compatible_pipes.keys():
        already_visited = set()
        queue = [starting_pos]
        pos_distances = {starting_pos: 0}
        connections = defaultdict(list)
        # closed_loop = False
        while queue:
            i, j = queue.pop(0)
            already_visited.add((i, j))
            p = pipes[i][j]
            if p == "S":
                if queue:
                    break
                p = s
            for dx, dy in compatible_pipes[p].keys():
                try:
                    if pipes[i + dx][j + dy] == "S":
                        pn = s
                    else:
                        pn = pipes[i + dx][j + dy]
                    cond1 = i + dx >= 0 and j + dy >= 0
                    cond2 = pn in compatible_pipes[p][(dx, dy)]
                    if all([cond1, cond2]):
                        connections[(i, j)].append((i + dx, j + dy))
                        if (i + dx, j + dy) not in already_visited:
                            # print((i,j), p, "->", (i+dx, j+dy), pipes[i+dx][j+dy], "#", compatible_pipes[p][(dx, dy)])
                            queue.append((i + dx, j + dy))
                            pos_distances[(i + dx, j + dy)] = min(
                                pos_distances[(i, j)] + 1,
                                pos_distances.get((i + dx, j + dy), float("inf")),
                            )
                except IndexError:
                    pass
        if not is_closed_loop(starting_pos, connections):
            print("Not a closed loop", "S ->", s)
            continue
        print("Closed loop", "S ->", s)
        max_distance = 0
        for _, d in pos_distances.items():
            max_distance = max(max_distance, d)
        if max_distance:
            max_distances.append(max_distance)
    return max_distances


print("result:", calculate_distances())
