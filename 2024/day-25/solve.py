from collections import defaultdict
from typing import Optional


keys_and_locks = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
"""

keys_and_locks = open("input.txt", "r").read().strip()

keys_and_locks = [
    [list(row.strip()) for row in l.strip().splitlines() if row.strip()]
    for l in keys_and_locks.split("\n\n")
    if l.strip()
]

Schematic = list[list[str]]


def is_lock(schematic: Schematic) -> bool:
    for el in schematic[0]:
        if el != "#":
            return False
    return True


def split_keys_and_locks(
    schematics: list[Schematic],
) -> tuple[list[Schematic], list[Schematic]]:
    keys = []
    locks = []
    for schematic in schematics:
        if is_lock(schematic):
            locks.append(schematic)
        else:
            keys.append(schematic)
    return keys, locks


def schematic_as_sizes(schematic: Schematic) -> list[int]:
    sizes = [-1 for _ in schematic[0]]
    for row in schematic:
        for i, el in enumerate(row):
            sizes[i] += 1 if el == "#" else 0
    return sizes


keys, locks = split_keys_and_locks(keys_and_locks)

keys_sizes = [schematic_as_sizes(key) for key in keys]
locks_sizes = [schematic_as_sizes(lock) for lock in locks]

result = 0
for lock_size in locks_sizes:
    for key_size in keys_sizes:
        fits = True
        for k, l in zip(key_size, lock_size):
            if k + l >= 6:
                fits = False
                break
        if fits:
            result += 1

print("result:", result)
