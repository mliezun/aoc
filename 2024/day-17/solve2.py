from collections import defaultdict
from typing import Optional
import tqdm


program = """Register A: 117440
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""

program = open("input.txt", "r").read().strip()

registers, program = [
    (
        {
            register: int(value.strip())
            for registers in line.splitlines()
            for register, value in [registers.replace("Register ", "").split(":")]
        }
        if i == 0
        else list(map(int, line.split(":")[1].strip().split(",")))
    )
    for i, line in enumerate(program.split("\n\n"))
    if line.strip()
]


def execute(registers: dict[str, int], program: list[int]):
    ip = 0
    output = []

    def program_end():
        return ip < 0 or ip >= len(program)

    def literal_operand():
        nonlocal ip
        value = program[ip]
        ip += 1
        return value

    def combo_operand():
        nonlocal ip
        value = program[ip]
        ip += 1
        if 0 <= value <= 3:
            return value
        if 4 <= value <= 6:
            return registers[chr(ord("A") + (value - 4))]
        raise RuntimeError("unreachable")

    def fetch_instruction():
        nonlocal ip
        inst = program[ip]
        ip += 1
        return inst

    try:
        while not program_end():
            inst = fetch_instruction()
            if inst == 0:
                # ADV
                registers["A"] >>= combo_operand()
            elif inst == 1:
                # BXL
                registers["B"] ^= literal_operand()
            elif inst == 2:
                # BST
                registers["B"] = combo_operand() % 8
            elif inst == 3:
                # JNZ
                if registers["A"]:
                    ip = literal_operand()
            elif inst == 4:
                # BXC
                registers["B"] ^= registers["C"]
                _ = literal_operand()
            elif inst == 5:
                # OUT
                output.append(combo_operand() % 8)
            elif inst == 6:
                # BDV
                registers["B"] = registers["A"] >> combo_operand()
            elif inst == 7:
                # CDV
                registers["C"] = registers["A"] >> combo_operand()
    except IndexError:
        pass

    return output


# Register A: 64584136
# Register B: 0
# Register C: 0

# Program: 2,4,1,2,7,5,1,3,4,3,5,5,0,3,3,0

# 1. BST regB = regA % 8
# 2. BXL regB = regB xor 2
# 3. CDV regC = regA >> regB
# 4. BXL regB = regB xor 3
# 5. BXC regB = regB xor regC
# 6. OUT regB%8
# 7. ADV regA = regA >> 3
# 8. JNZ if regA exit else ip=0


# OUT regB = (((((regA % 8) xor 2) xor 3) xor (regA >> ((regA % 8) xor 2)))) % 8


op = lambda a: ((((a % 8) ^ 2) ^ 3) ^ (a >> ((a % 8) ^ 2))) % 8


def find_element(regA: int, out: int):
    options = []
    for i in range(8):
        try:
            if op(regA + i) == out:
                options.append(regA + i)
        except ZeroDivisionError:
            pass
    return options


def calculate_result(expected_output: list[int], result: int = 0):
    if len(expected_output) == 0:
        return result
    my_output = expected_output.copy()
    out = my_output.pop()
    found = find_element(result << 3, out)
    for regA in found:
        if (solution := calculate_result(my_output.copy(), regA)) is not None:
            return solution
    return None


print("Result:", calculate_result(program.copy(), 0))
