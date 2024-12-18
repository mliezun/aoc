from collections import defaultdict
from typing import Optional


program = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""

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


output = execute(registers, program)
print(",".join(map(str, output)))
