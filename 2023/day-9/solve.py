history = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

history = open("input.txt", "r").read()

history = [list(map(int, values.split())) for values in history.splitlines()]

def diff(values):
    diffs = []
    for i in range(len(values)-1):
        diffs.append(values[i+1]-values[i])
    return diffs


results = []
for values in history:
    changes = [values]
    while any(changes[-1]):
        changes.append(diff(changes[-1]))
    last_number = 0
    for change in changes:
        last_number += change[-1]
    results.append(last_number)
    
print("results:", results, sum(results))