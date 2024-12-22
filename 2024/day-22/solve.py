from collections import defaultdict
from typing import Optional


initial_secrets = """1
10
100
2024"""

initial_secrets = open("input.txt", "r").read().strip()

initial_secrets = [int(l.strip()) for l in initial_secrets.splitlines() if l.strip()]


def evolve_secret(secret):
    MODULO = 16777216

    secret ^= secret * 64
    secret %= MODULO

    secret ^= secret // 32
    secret %= MODULO

    secret ^= secret * 2048
    secret %= MODULO

    return secret


def calculate_2000th_secret(initial_secrets):
    results = []

    for initial_secret in initial_secrets:
        secret = initial_secret
        for _ in range(2000):
            secret = evolve_secret(secret)
        results.append(secret)

    return sum(results)


result = calculate_2000th_secret(initial_secrets)
print("Result:", result)
