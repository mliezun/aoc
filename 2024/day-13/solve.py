from collections import defaultdict
from typing import Optional

import numpy as np
from scipy.optimize import linprog


claws = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""

claws = open("input.txt", "r").read().strip()

claws = [
    [
        tuple(
            map(
                int,
                v.split(":")[1]
                .replace("X", "")
                .replace("Y", "")
                .replace("+", "")
                .replace("=", "")
                .split(","),
            )
        )
        for v in l.strip().splitlines()
    ]
    for l in claws.split("\n\n")
    if l.strip()
]


def minimize_cost(A, B, P):
    a, b = A
    c, d = B
    x, y = P

    cost = [3, 1]

    A_eq = [[a, c], [b, d]]
    b_eq = [x, y]

    bounds = [(0, None), (0, None)]

    result = linprog(cost, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")

    if result.success:
        u, v = result.x
        return u, v, result.fun

    return None, None, None

def as_int(presses: Optional[float], precision: float = 0.00001) -> Optional[int]:
    if presses is None:
        return None
    presses_int = round(presses)
    if abs(presses - presses_int) > precision:
        return None
    return presses_int
    

total_cost = 0
for A, B, P in claws:
    pressed_a, pressed_b, cost = minimize_cost(A, B, P)
    print(pressed_a, pressed_b, cost)
    pressed_a = as_int(pressed_a)
    pressed_b = as_int(pressed_b)
    cost = as_int(cost)
    if pressed_a is None or pressed_b is None or cost is None:
        print("Not found solution for", A, B, P)
    else:
        total_cost += cost
        
print("result:", total_cost)
