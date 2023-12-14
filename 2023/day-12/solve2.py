from functools import cache


springs = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

springs = open("input.txt", "r").read().strip()


springs = [s.strip().split(" ") for s in springs.splitlines() if s.strip()]


@cache
def possible_count(
    spring_line: str,
    groups: tuple[int],
    prev_size: int = 0,
    must_operational: bool = False,
):
    if spring_line == "":
        if groups:
            if len(groups) == 1 and groups[0] == prev_size:
                return 1
            return 0
        else:
            if prev_size == 0:
                return 1
            return 0

    if len(groups) == 0:
        if "#" in spring_line or prev_size > 0:
            return 0
        return 1

    curr = spring_line[0]
    rest = spring_line[1:]

    if curr == "?":
        return possible_count(
            "#" + rest, groups, prev_size, must_operational
        ) + possible_count("." + rest, groups, prev_size, must_operational)

    if curr == "#":
        if must_operational:
            return 0

        curr_size = prev_size + 1
        if curr_size > groups[0]:
            return 0
        elif curr_size == groups[0]:
            return possible_count(rest, groups[1:], 0, True)
        else:
            return possible_count(rest, groups, curr_size, False)

    if curr == ".":
        if must_operational:
            return possible_count(rest, groups, 0, False)

        if prev_size == 0:
            return possible_count(rest, groups, 0, False)
        else:
            if prev_size != groups[0]:
                return 0
            else:
                return possible_count(rest, groups[1:], 0, False)


arrangement_count = 0
for spring_line, groups in springs:
    spring_line = "?".join([spring_line] * 5)
    groups = tuple(map(int, groups.split(","))) * 5
    arrangement_count += possible_count(spring_line, groups)

print("result:", arrangement_count)
