from collections import defaultdict
from typing import Optional


towels = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""

towels = open("input.txt", "r").read().strip()

towel_patterns, desired_designs = [
    l.split(", ") if i == 0 else l.splitlines()
    for i, l in enumerate(towels.split("\n\n"))
    if l.strip()
]


def can_be_composed(target: str, substrings: list[str]) -> bool:
    if not target:
        return True
    dp = [False] * (len(target) + 1)
    dp[0] = True
    for i in range(1, len(target) + 1):
        for substring in substrings:
            if i >= len(substring) and target[i - len(substring) : i] == substring:
                dp[i] = dp[i] or dp[i - len(substring)]
                if dp[i]:
                    break
    return dp[-1]


result = 0
for design in desired_designs:
    if can_be_composed(design, towel_patterns):
        result += 1

print("result:", result)
