from collections import defaultdict
import re


memory = """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""

memory = open("input.txt", "r").read().strip()

compute_enabled = True


def mul(a, b):
    if compute_enabled:
        return a * b
    return 0


def do():
    global compute_enabled
    compute_enabled = True


def dont():
    global compute_enabled
    compute_enabled = False


result = 0
for val in re.findall(r"(mul\(\d\d?\d?,\d\d?\d?\))|(do\(\))|(don\'t\(\))", memory):
    multiply, do_fn, dont_fn = val
    if do_fn:
        do()
    elif dont_fn:
        dont()
    elif multiply:
        result += eval(multiply)

print(result)
