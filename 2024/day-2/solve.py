from collections import defaultdict


reports = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""

reports = open("input.txt", "r").read().strip()

reports = [list(map(int, l.split())) for l in reports.splitlines() if l.strip()]

def is_safe(rep):
    global_delta = None
    try:
        for l1, l2 in zip(rep[:-1], rep[1:]):
            delta = int((l1-l2)/abs(l1-l2))
            if global_delta is None:
                global_delta = delta
            diff = 1 <= abs(l1-l2) <= 3
            if not diff:
                return False
            if delta != global_delta:
                return False
    except ZeroDivisionError:
        return False
    return True

count_reports = 0
for rep in reports:
    if is_safe(rep):
        count_reports += 1
        
print(count_reports)
