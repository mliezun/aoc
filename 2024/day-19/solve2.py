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


def composed_option_count(target: str, substrings: list[str]) -> int:
    if not target:
        return 1
    dp = [0] * (len(target) + 1)
    dp[0] = 1
    for i in range(1, len(target) + 1):
        for substring in substrings:
            if i >= len(substring) and target[i - len(substring) : i] == substring:
                dp[i] += dp[i - len(substring)]
    return dp[-1]


result = 0
for design in desired_designs:
    result += composed_option_count(design, towel_patterns)

print("result:", result)
