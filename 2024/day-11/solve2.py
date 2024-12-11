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


MEMOIZE = defaultdict(dict)


def apply_rule(stone: int, deep: int) -> int:
    if deep == 0:
        return 1

    result = MEMOIZE[stone].get(deep)
    if result:
        return result

    if stone == 0:
        result = apply_rule(1, deep - 1)
        MEMOIZE[stone][deep] = result
        return result

    if len(str(stone)) % 2 == 0:
        left_stone = str(stone)[: len(str(stone)) // 2]
        right_stone = str(stone)[len(str(stone)) // 2 :]
        result = apply_rule(int(left_stone), deep - 1) + apply_rule(
            int(right_stone), deep - 1
        )
        MEMOIZE[stone][deep] = result
        return result

    result = apply_rule(stone * 2024, deep - 1)
    MEMOIZE[stone][deep] = result
    return result


BLINKS = 75
result = sum(map(lambda x: apply_rule(x, BLINKS), stones))
print(result)
