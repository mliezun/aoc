from collections import defaultdict

games = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

games = open('input.txt', 'r').read()

def sum_set(s):
	sums = defaultdict(int)
	for v in s.split(','):
		num, color = v.strip().split(' ')
		sums[color.strip()] += int(num.strip())
	print(sums)
	return sums

def min_sets(ss):
	min_s = defaultdict(int)
	for s in ss:
		for k, v in s.items():
			if v > min_s.get(k, 0):
				min_s[k] = v
	return min_s

game_limits = {'red': 12, 'green': 13, 'blue': 14}

def is_valid(sums):
	for k, v in game_limits.items():
		if sums.get(k, 0) > v:
			return False
	return True

result = 0
for g in games.split('\n'):
	if not g.strip():
		continue
	gid, gset = g.split(':')
	gn = int(gid.split(' ')[1].strip())
	print(g)
	all_valid = True
	ms = min_sets(map(sum_set, gset.split(';')))
	print('min', ms)
	power = 1
	for k in ms.values():
		power *= k
	print(power)
	result += power

print(result)
