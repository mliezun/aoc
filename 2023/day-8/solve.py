instructions = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""

instructions = open("input.txt", "r").read()

rl, nodes = instructions.split("\n\n")
nodes = [node.strip().split("=") for node in nodes.splitlines() if node.strip()]
nodes = {
    node_name.strip(): [
        node.strip() for node in next_nodes.replace("(", "").replace(")", "").split(",")
    ]
    for node_name, next_nodes in nodes
}


current_node = "AAA"
steps = 0
while current_node != "ZZZ":
    ix = 0 if rl[steps % len(rl)] == "L" else 1
    current_node = nodes[current_node][ix]
    steps += 1

print(current_node, steps)
