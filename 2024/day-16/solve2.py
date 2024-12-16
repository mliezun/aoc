import networkx as nx

maze = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""

maze = open("input.txt", "r").read().strip()

maze = [list(row.strip()) for row in maze.splitlines() if row.strip()]

def parse_maze(maze):
    start = end = None
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell == 'S':
                start = (i, j)
            elif cell == 'E':
                end = (i, j)
    return start, end

def build_graph_with_turn_costs(maze):
    G = nx.DiGraph()
    directions = [
        (-1, 0),
        (1, 0), 
        (0, -1),
        (0, 1)
    ]
    rows, cols = len(maze), len(maze[0])

    for x in range(rows):
        for y in range(cols):
            if maze[x][y] == '#':
                continue

            for i, (dx, dy) in enumerate(directions):
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < rows and 0 <= new_y < cols and maze[new_x][new_y] != '#':
                    G.add_edge((x, y, i), (new_x, new_y, i), weight=1)

                    for j, _ in enumerate(directions):
                        if j != i:
                            G.add_edge((x, y, i), (new_x, new_y, j), weight=1001)

    return G

def find_shortest_path(maze):
    start, end = parse_maze(maze)
    assert start and end

    graph = build_graph_with_turn_costs(maze)

    virtual_start = "start"
    virtual_end = "end"

    for i in range(4):
        graph.add_edge(virtual_start, (*start, i), weight=0)
        graph.add_edge((*end, i), virtual_end, weight=0)

    try:
        return nx.all_shortest_paths(graph, virtual_start, virtual_end, weight="weight")
    except nx.NetworkXNoPath:
        return None, None


TILES = set()
paths = find_shortest_path(maze)
for path in paths:
    for pos in path:
        if isinstance(pos, tuple):
            x, y, _ = pos
            TILES.add((x, y))
print("TILES:", len(TILES))
