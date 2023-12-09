with open("input.txt", "r") as f:
    content = f.readlines()

# content = ["two1nine", "eightwothree", "abcone2threexyz", "xtwone3four", "4nineeightseven2", "zoneight234", "7pqrstsixteen"]

numbers_english = [
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]


def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            return
        yield start
        start += len(sub)  # use start += 1 to find overlapping matches


def replace_numbers(l):
    index_found = []
    for i, n in enumerate(numbers_english):
        for ix in find_all(l, n):
            index_found.append((n, i + 1, ix))
    for ix, d in enumerate(l):
        try:
            index_found.append((None, int(d), ix))
        except ValueError:
            pass
    print(l, list(sorted(index_found, key=lambda x: x[2])))
    l = "".join([str(x[1]) for x in sorted(index_found, key=lambda x: x[2])])
    return l


def process_line(l):
    l = replace_numbers(l)
    first_digit = None
    last_digit = None
    for d in l:
        try:
            first_digit = int(d)
            break
        except ValueError:
            pass
    for d in reversed(l):
        try:
            last_digit = int(d)
            break
        except ValueError:
            pass
    return first_digit * 10 + last_digit


print(list(map(process_line, content)))
print(sum(map(process_line, content)))
