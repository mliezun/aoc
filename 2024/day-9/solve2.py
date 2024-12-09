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


def region_size(reg: list[int]) -> int:
    return abs(reg[1] - reg[0])


def compact_disk(expanded_disk: list[str]) -> list[str]:
    attempted_to_move = set()
    ix_b = []
    my_b = None
    search_space_mode = False
    for i, b in enumerate(reversed(expanded_disk)):
        if b != "." and my_b is None:
            my_b = b
            ix_b.append(len(expanded_disk) - i)
        elif b != my_b and my_b is not None:
            ix_b.insert(0, len(expanded_disk) - i)
            search_space_mode = True
        if search_space_mode:
            if my_b not in attempted_to_move:
                attempted_to_move.add(my_b)
                reg_b = region_size(ix_b)
                reg_a = 0
                start_a = 0
                while reg_a < reg_b:
                    ix_a = []
                    my_a = None
                    for j in range(start_a, ix_b[1]):
                        a = expanded_disk[j]
                        if a == "." and my_a is None:
                            my_a = "."
                            ix_a.append(j)
                        elif a != "." and my_a is not None:
                            ix_a.append(j)
                            break
                    # print(ix_a)
                    if len(ix_a) == 2:
                        reg_a = region_size(ix_a)
                        start_a = ix_a[1]
                    else:
                        # print("Not found big enough space")
                        break
                # print(f"'{my_b}'", "*", reg_b, "| '.' *", reg_a, [ix_a, ix_b])
                if len(ix_a) == 2 and len(ix_b) == 2:
                    reg_b = region_size(ix_b)
                    reg_a = region_size(ix_a)
                    if reg_b <= reg_a:
                        for x, y in zip(range(*ix_a), range(*ix_b)):
                            expanded_disk[x], expanded_disk[y] = (
                                expanded_disk[y],
                                expanded_disk[x],
                            )
            # Clear search params for next outer loop iteration
            ix_b = []
            my_b = None
            search_space_mode = False
            if b != ".":
                my_b = b
                ix_b.append(len(expanded_disk) - i)
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
# print(compacted_disk)
print(checksum)
