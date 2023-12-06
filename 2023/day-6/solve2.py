import tqdm

races = """Time:      7  15   30
Distance:  9  40  200"""

races = open("input.txt", "r").read()

def clean_number(x):
    while " " in x:
        x = x.replace(" ", "")
    return x

race_times, race_distances = races.split("\n")
race_times = int(clean_number(race_times.split(':')[1]))
race_distances = int(clean_number(race_distances.split(':')[1]))

print(race_times, race_distances)

def calculate_distance(x):
    t, d = x
    for v in range(t):
        if v * (t-v) > d:
            yield v
            
def generator_length(x):
    l = 0
    for _ in x:
        l += 1
    return l

records = map(generator_length, map(calculate_distance, zip([race_times], [race_distances])))
    
result = 1
for r in tqdm.tqdm(records):
    result *= r

print(result)
