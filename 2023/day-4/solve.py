cards = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""

cards = open("input.txt", "r").read()

cards = [card for card in cards.split("\n") if card.strip()]

value = 0
for card in cards:
    cn, numbers = card.split(":")
    winning_numbers, my_numbers = numbers.split("|")
    winning_numbers = [int(x.strip()) for x in winning_numbers.split(" ") if x.strip()]
    my_numbers = [int(x.strip()) for x in my_numbers.split(" ") if x.strip()]
    match_numbers = list(filter(lambda x: x in winning_numbers, my_numbers))
    print(match_numbers, 2 ** (len(match_numbers) - 1))
    if match_numbers:
        value += 2 ** (len(match_numbers) - 1)

print(value)
