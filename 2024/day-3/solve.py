from collections import defaultdict
import re


memory = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""

memory = open("input.txt", "r").read().strip()


def mul(a, b):
    return a*b

result = 0
for val in re.findall(r"mul\(\d\d?\d?,\d\d?\d?\)", memory):
    result += eval(val)

print(result)
