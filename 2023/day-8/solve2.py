import math

instructions = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

instructions = open("input.txt", "r").read()

rl, nodes = instructions.split("\n\n")
nodes = [node.strip().split("=") for node in nodes.splitlines() if node.strip()]
nodes = {
    node_name.strip(): [
        node.strip() for node in next_nodes.replace("(", "").replace(")", "").split(",")
    ]
    for node_name, next_nodes in nodes
}


def at_end(nodes: list[str]):
    return all((node.endswith("Z") for node in nodes))


start_nodes = [node for node in nodes.keys() if node.endswith("A")]
for node in start_nodes:
    start_node = node
    for i in range(100_000):
        k = i % len(rl)
        ix = 0 if rl[k] == "L" else 1
        next_node = nodes[start_node][ix]
        start_node = next_node
        if next_node.endswith("Z"):
            print("next_node", next_node, i+1, k)
    print("="*20)

# Copied from previous print
# Length of the cycles to get to the last node:
numbers = [18157, 14363, 16531, 12737, 19783, 19241]
print("result:", math.lcm(*numbers))
