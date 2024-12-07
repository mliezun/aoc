from collections import defaultdict
from typing import Optional
from functools import lru_cache
from itertools import product


equations = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

equations = open("input.txt", "r").read().strip()

equations = [[int(n) for n in l.replace(":", "").split(" ")] for l in equations.splitlines() if l.strip()]

@lru_cache()
def permutations_operators(size: int) -> list[list[str]]:
    if size == 2:
        return [["+"], ["*"]]
    
    result = []
    for perm in permutations_operators(size-1):
        result.append(["+"] + perm)
        result.append(["*"] + perm)
    return result

def operate(equation: list[int], operators: list[str]) -> int:
    assert len(equation) == len(operators)+1, f"{equation=} {operators=}"
    value = equation[0]
    for v, op in zip(equation[1:], operators):
        if op == '+':
            value += v
        elif op == '*':
            value *= v
    return value


total_result = 0
for calibration in equations:
    calibration_value = calibration[0]
    equation = calibration[1:]
    for operators in permutations_operators(len(equation)):
        if operate(equation, operators) == calibration_value:
            total_result += calibration_value
            break
            
print(total_result)
