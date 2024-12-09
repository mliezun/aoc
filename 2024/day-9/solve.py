from collections import defaultdict
from typing import Optional


disk = """2333133121414131402"""

disk = open("input.txt", "r").read().strip()


def expand_blocks(disk: str) -> list[str]:
    block_id = 0
    free_space = False
    result = []
    for b in disk:
        if free_space:
            result.extend(
                [
                    ".",
                ]
                * int(b)
            )
        else:
            result.extend(
                [
                    f"{block_id}",
                ]
                * int(b)
            )
            block_id += 1
        free_space = not free_space
    return result


def compact_disk(expanded_disk: list[str]) -> list[str]:
    while True:
        ix_a, ix_b = None, None
        for i, b in enumerate(reversed(expanded_disk)):
            if b != ".":
                ix_b = len(expanded_disk) - i - 1
                break
        for i, a in enumerate(expanded_disk):
            if a == ".":
                ix_a = i
                break
        if ix_a is None or ix_b is None or ix_a > ix_b:
            break
        expanded_disk[ix_a], expanded_disk[ix_b] = (
            expanded_disk[ix_b],
            expanded_disk[ix_a],
        )
    return expanded_disk


def checksum_disk(compacted_disk: list[str]) -> int:
    result = 0
    for i, b in enumerate(compacted_disk):
        if b == ".":
            continue
        result += int(b) * i
    return result


expanded_disk = expand_blocks(disk)
compacted_disk = compact_disk(expanded_disk)
checksum = checksum_disk(compacted_disk)
print(checksum)
