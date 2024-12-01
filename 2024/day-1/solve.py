from collections import defaultdict


locations = """3   4
4   3
2   5
1   3
3   9
3   3"""

locations = open("input.txt", "r").read().strip()

locations = [l.split() for l in locations.splitlines() if l.strip()]

left_numbers = [int(l[0]) for l in locations]
left_numbers.sort()
right_numbers = [int(l[1]) for l in locations]
right_numbers.sort()

diff = [abs(a-b) for a, b in zip(left_numbers, right_numbers)]
print(sum(diff))
