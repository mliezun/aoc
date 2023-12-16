layout = """.|...\\....
|.-.\\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|...."""


layout = open("input.txt", "r").read().strip()


layout = [list(line.strip()) for line in layout.splitlines() if line.strip()]


def follow_beams(layout, starting_pos, starting_direction):
    beams_pos = [starting_pos]
    visited_direction = set()
    beams_direction = [starting_direction]
    energized = set()
    all_exited = False
    while not all_exited and not all(
        [vd in visited_direction for vd in zip(beams_pos, beams_direction)]
    ):
        all_exited = True
        for current_beam in range(len(beams_pos)):
            try:
                x, y = beams_pos[current_beam]
                dx, dy = beams_direction[current_beam]
                vd = ((x, y), (dx, dy))
                if vd in visited_direction or x + dx < 0 or y + dy < 0:
                    continue
                visited_direction.add(vd)
                mirror = layout[x + dx][y + dy]
                beams_pos[current_beam] = (x + dx, y + dy)
                energized.add((x + dx, y + dy))
                match mirror:
                    case ".":
                        pass
                    case "|":
                        if (dx, dy) in [(0, 1), (0, -1)]:
                            beams_direction[current_beam] = (1, 0)
                            beams_direction.append((-1, 0))
                            beams_pos.append((x + dx, y + dy))
                    case "-":
                        if (dx, dy) in [(1, 0), (-1, 0)]:
                            beams_direction[current_beam] = (0, 1)
                            beams_direction.append((0, -1))
                            beams_pos.append((x + dx, y + dy))
                    case "\\":
                        if (dx, dy) == (1, 0):
                            beams_direction[current_beam] = (0, 1)
                        elif (dx, dy) == (-1, 0):
                            beams_direction[current_beam] = (0, -1)
                        elif (dx, dy) == (0, 1):
                            beams_direction[current_beam] = (1, 0)
                        elif (dx, dy) == (0, -1):
                            beams_direction[current_beam] = (-1, 0)
                    case "/":
                        if (dx, dy) == (1, 0):
                            beams_direction[current_beam] = (0, -1)
                        elif (dx, dy) == (-1, 0):
                            beams_direction[current_beam] = (0, 1)
                        elif (dx, dy) == (0, 1):
                            beams_direction[current_beam] = (-1, 0)
                        elif (dx, dy) == (0, -1):
                            beams_direction[current_beam] = (1, 0)
                all_exited = False
            except IndexError:
                pass
    return len(energized)

def copy_layout(layout):
    copy_layout = []
    for r in layout:
        copy_layout.append([c for c in r])
    return copy_layout


max_energized = 0
for i in range(len(layout)):
    max_energized = max(max_energized, follow_beams(layout, (i, -1), (0, 1)))
    max_energized = max(max_energized, follow_beams(layout, (i, len(layout[0])), (0, -1)))
for j in range(len(layout[0])):
    max_energized = max(max_energized, follow_beams(layout, (-1, j), (1, 0)))
    max_energized = max(max_energized, follow_beams(layout, (len(layout), j), (-1, 0)))
print("result:", max_energized)
