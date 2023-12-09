from collections import defaultdict

games = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

games = open("input.txt", "r").read()


def sum_set(s):
    sums = defaultdict(int)
    for v in s.split(","):
        num, color = v.strip().split(" ")
        sums[color.strip()] += int(num.strip())
    print(sums)
    return sums


game_limits = {"red": 12, "green": 13, "blue": 14}


def is_valid(sums):
    for k, v in game_limits.items():
        if sums.get(k, 0) > v:
            return False
    return True


result = 0
for g in games.split("\n"):
    if not g.strip():
        continue
    gid, gset = g.split(":")
    gn = int(gid.split(" ")[1].strip())
    print(g)
    all_valid = True
    for s in gset.split(";"):
        if not is_valid(sum_set(s)):
            all_valid = False
            print("not valid")
            break
    if all_valid:
        print("all valid", gn)
        result += gn
print(result)
