races = """Time:      7  15   30
Distance:  9  40  200"""

races = open("input.txt", "r").read()

race_times, race_distances = races.split("\n")
race_times = [int(x.strip()) for x in race_times.split()[1:] if x.strip()]
race_distances = [int(x.strip()) for x in race_distances.split()[1:] if x.strip()]


def calculate_distance(x):
    t, d = x
    for v in range(t):
        if v * (t - v) > d:
            yield v


def generator_length(x):
    l = 0
    for _ in x:
        l += 1
    return l


records = map(
    generator_length, map(calculate_distance, zip(race_times, race_distances))
)

result = 1
for r in records:
    result *= r

print(result)
