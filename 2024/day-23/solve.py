from collections import defaultdict
from typing import Optional
import networkx as nx
import matplotlib.pyplot as plt


lan_party = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
"""

lan_party = open("input.txt", "r").read().strip()

lan_party = [l.strip().split("-") for l in lan_party.splitlines() if l.strip()]

G = nx.Graph()
for u, v in lan_party:
    G.add_edge(u, v)


result = 0
CLIQUE_SIZE = 3
for clique in nx.enumerate_all_cliques(G):
    if len(clique) == CLIQUE_SIZE:
        for n in clique:
            if n.startswith("t"):
                result += 1
                break
    elif len(clique) > CLIQUE_SIZE:
        break

print(result)
