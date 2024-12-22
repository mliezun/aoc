from itertools import product
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

initial_secrets = """1
2
3
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


def calculate_price_changes(secret, steps):
    prices = []
    for _ in range(steps):
        secret = evolve_secret(secret)
        prices.append(secret % 10)

    changes = [prices[i] - prices[i - 1] for i in range(1, len(prices))]
    return changes, prices


def evaluate_sequence(args):
    sequence, initial_secrets, sequence_length, steps = args
    total_bananas = 0

    for secret in initial_secrets:
        changes, prices = calculate_price_changes(secret, steps)

        for i in range(len(changes) - sequence_length + 1):
            if tuple(changes[i : i + sequence_length]) == sequence:
                total_bananas += prices[i + sequence_length]
                break

    return sequence, total_bananas


def find_best_sequence(initial_secrets, sequence_length=4, steps=2000):
    max_bananas = 0
    best_sequence = None

    possible_sequences = list(product(range(-9, 10), repeat=sequence_length))

    with Pool(cpu_count()) as pool:
        with tqdm(total=len(possible_sequences), desc="Processing Sequences") as pbar:
            results = []
            for result in pool.imap_unordered(
                evaluate_sequence,
                [
                    (sequence, initial_secrets, sequence_length, steps)
                    for sequence in possible_sequences
                ],
            ):
                results.append(result)
                pbar.update(1)

    for sequence, bananas in results:
        if bananas > max_bananas:
            max_bananas = bananas
            best_sequence = sequence

    return best_sequence, max_bananas


def main():
    _, max_bananas = find_best_sequence(initial_secrets)
    print("Result:", max_bananas)


if __name__ == "__main__":
    main()
