from collections import defaultdict

pipes = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""

pipes = open("input.txt", "r").read().strip()

pipes = pipes.splitlines()
for i, r in enumerate(pipes):
    for j, p in enumerate(r):
        if p == 'S':
            starting_pos = (i, j)
            break
        
def get_delta(pos1, pos2):
    return (pos2[0]-pos1[0], pos2[1]-pos1[1])

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
            if np not in already_visited and not is_opposite(get_delta(next_pos, np), delta):
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

def get_loop_connections():
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
            if p == 'S':
                if queue:
                    break
                p = s
            for dx, dy in compatible_pipes[p].keys():
                try:
                    if pipes[i+dx][j+dy] == "S":
                        pn = s
                    else:
                        pn = pipes[i+dx][j+dy]
                    cond1 = i+dx >= 0 and j+dy >= 0
                    cond2 = pn in compatible_pipes[p][(dx, dy)]
                    if all([cond1, cond2]):
                        connections[(i, j)].append((i+dx, j+dy))
                        if (i+dx, j+dy) not in already_visited:
                            queue.append((i+dx, j+dy))
                            pos_distances[(i+dx, j+dy)] = min(pos_distances[(i, j)]+1, pos_distances.get((i+dx, j+dy), float('inf')))
                except IndexError:
                    pass
        if not is_closed_loop(starting_pos, connections):
            print("Not a closed loop", "S ->" , s)
            continue
        print("Closed loop", "S ->", s)
        return connections

# print("result:", get_loop_connections())

def increase_space(pipes):
    result = []
    for r in pipes:
        rr = ""
        for p in r:
            rr += " " + p
        result.append(" "*len(rr))
        result.append(rr)
    return result

def fill_gaps(pipes, connections):
    new_pipes = [list(r) for r in pipes]
    for conn, next_positions in connections.items():
        i, j = conn
        new_i = i+i+1
        new_j = j+j+1
        for next_p in next_positions:
            dx, dy = get_delta((i, j), next_p)
            new_pipes[new_i+dx][new_j+dy] = "x"
    # print('\n'.join([str(p) for p in new_pipes]))
    return new_pipes


def is_contained(pos, pipes):
    directions = next(iter(compatible_pipes.values())).keys()
    already_visited = set()
    queue = [pos]
    while queue:
        i, j = queue.pop(0)
        if i in [0, len(pipes)-1] or j in [0, len(pipes[0])-1]:
            return False
        for dx, dy in directions:
            if 0 <= i+dx < len(pipes) and 0 <= j+dy < len(pipes[0]):
                if pipes[i+dx][j+dy] in [' ', '.'] and (i+dx, j+dy) not in already_visited:
                    already_visited.add((i+dx, j+dy))
                    queue.append((i+dx, j+dy))
    return True

def count_contained(pipes, connections):
    transform_connections = []
    for i, j in connections.keys():
        transform_connections.append((i+i+1, j+j+1))
    counts = 0
    for i, r in enumerate(pipes):
        for j, p in enumerate(r):
            if p not in [' ', 'x'] and (i, j) not in transform_connections and is_contained((i, j), pipes):
                counts += 1
    return counts

connections = get_loop_connections()
new_pipes = increase_space(pipes)
new_pipes = fill_gaps(new_pipes, connections)

print(count_contained(new_pipes, connections))

