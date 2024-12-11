from collections import defaultdict
from typing import Optional, Union


stones = """125 17"""

stones = open("input.txt", "r").read().strip()

stones = [int(l) for l in stones.split(" ") if l.strip()]


def flatten(arr: list) -> list:
    result = []
    for el in arr:
        if isinstance(el, list):
            result.extend(el)
        else:
            result.append(el)
    return result


def apply_rule(stone: int) -> Union[list[int], int]:
    if stone == 0:
        return 1
    if len(str(stone)) % 2 == 0:
        left_stone = str(stone)[: len(str(stone)) // 2]
        right_stone = str(stone)[len(str(stone)) // 2 :]
        return [int(left_stone), int(right_stone)]
    return stone * 2024


def blink(stones: list[int]) -> list[int]:
    return flatten(map(apply_rule, stones))


for _ in range(25):
    stones = blink(stones)


print(len(stones))
