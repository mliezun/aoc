sequence = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""

sequence = open("input.txt", "r").read().strip()


def hash(value: str) -> int:
    result = 0
    for c in value:
        result += ord(c)
        result *= 17
        result %= 256
    return result


print("result:", sum(hash(x) for x in sequence.split(",")))
