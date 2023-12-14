springs = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

springs = open("input.txt", "r").read().strip()


springs = [s.strip().split(" ") for s in springs.splitlines() if s.strip()]


def possible_arrangements(spring_line: str):
    if not spring_line:
        yield ""
        return
    if spring_line[0] == "?":
        for a in possible_arrangements(spring_line[1:]):
            yield "." + a
            yield "#" + a
    else:
        for a in possible_arrangements(spring_line[1:]):
            yield spring_line[0] + a


def arrangement_matches(arrangement: str, groups: str):
    arrangement = [a for a in arrangement.split(".") if a.strip()]
    groups = [int(g) for g in groups.split(",") if g.strip()]
    if len(arrangement) != len(groups):
        return False
    for a, g in zip(arrangement, groups):
        if a.count("#") != g:
            return False
    return True


arrangement_count = 0
for arrangement, group in springs:
    for a in possible_arrangements(arrangement):
        if arrangement_matches(a, group):
            arrangement_count += 1

print("result:", arrangement_count)
