from collections import defaultdict
from typing import Optional


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


STATES = {}


def and_gate(in1: str, in2: str, out: str) -> int:
    STATES[out] = STATES[in1] & STATES[in2]
    return STATES[out]


def or_gate(in1: str, in2: str, out: str) -> int:
    STATES[out] = STATES[in1] | STATES[in2]
    return STATES[out]


def xor_gate(in1: str, in2: str, out: str) -> int:
    STATES[out] = STATES[in1] ^ STATES[in2]
    return STATES[out]


def process_signals():
    for i, v in ins:
        STATES[i] = int(v)

    to_process = [(o[0], o[1], o[2], o[4]) for o in outs]
    while to_process:
        in1, op, in2, out = to_process.pop(0)
        if in1 not in STATES or in2 not in STATES:
            to_process.append((in1, op, in2, out))
            continue

        if op == "AND":
            and_gate(in1, in2, out)
        elif op == "OR":
            or_gate(in1, in2, out)
        if op == "XOR":
            xor_gate(in1, in2, out)


def state_as_number():
    zs = []
    for z in sorted(STATES.keys()):
        if z.startswith("z"):
            zs.append(z)

    result = 0
    e = 1
    for z in zs:
        result += e * STATES[z]
        e *= 2
    return result


process_signals()
print(state_as_number())
