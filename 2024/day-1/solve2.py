from collections import defaultdict


locations = """3   4
4   3
2   5
1   3
3   9
3   3"""

locations = open("input.txt", "r").read().strip()

locations = [l.split() for l in locations.splitlines() if l.strip()]

numbers_count = defaultdict(int)
for l in locations:
    numbers_count[l[1]] += 1

similarity_score = 0
for l in locations:
    similarity_score += int(l[0]) * numbers_count.get(l[0], 0)

print(similarity_score)
