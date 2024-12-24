# Thanks to https://github.com/encse/adventofcode/blob/master/2024/Day24/

from dataclasses import dataclass
from typing import Optional, Callable
import re
from collections import defaultdict


circuit = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""

circuit = open("input.txt", "r").read().strip()

circuit = [
    [s.split(": ") for s in l.splitlines()]
    if i == 0
    else [s.split(" ") for s in l.splitlines()]
    for i, l in enumerate(circuit.split("\n\n"))
    if l.strip()
]

ins, outs = circuit


@dataclass
class Rule:
    in1: str
    in2: str
    kind: str
    output: str


class Circuit:
    def __init__(self, rules: list[list[str]]):
        self.initial_rules = []
        for parts in rules:
            self.initial_rules.append(
                Rule(in1=parts[0], in2=parts[2], kind=parts[1], output=parts[4])
            )

    def fix(self) -> str:
        swaps = self.find_swaps(self.initial_rules)
        return ",".join(sorted(swaps))

    def find_swaps(self, rules: list[Rule]) -> list[str]:
        cin = self.output(rules, "x00", "AND", "y00")

        for i in range(1, 45):
            x = f"x{i:02d}"
            y = f"y{i:02d}"
            z = f"z{i:02d}"

            xor1 = self.output(rules, x, "XOR", y)
            and1 = self.output(rules, x, "AND", y)

            and2 = self.output(rules, cin, "AND", xor1)
            xor2 = self.output(rules, cin, "XOR", xor1)

            if xor2 is None and and2 is None:
                return self.swap(rules, xor1, and1)

            carry = self.output(rules, and1, "OR", and2)
            if xor2 != z:
                return self.swap(rules, z, xor2)
            else:
                cin = carry

        return []

    def output(self, rules: list[Rule], x: str, gate: str, y: str) -> Optional[str]:
        for rule in rules:
            if (rule.in1 == x and rule.kind == gate and rule.in2 == y) or (
                rule.in1 == y and rule.kind == gate and rule.in2 == x
            ):
                return rule.output
        return None

    def swap(self, rules: list[Rule], out1: str, out2: str) -> list[str]:
        new_rules = []
        for rule in rules:
            if rule.output == out1:
                new_rules.append(Rule(rule.in1, rule.in2, rule.kind, out2))
            elif rule.output == out2:
                new_rules.append(Rule(rule.in1, rule.in2, rule.kind, out1))
            else:
                new_rules.append(rule)

        return list(self.find_swaps(new_rules)) + [out1, out2]


c = Circuit(outs)
print("result:", c.fix())
