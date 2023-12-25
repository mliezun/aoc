import copy
import networkx as nx

wiring_diagram = """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr"""


wiring_diagram = open("input.txt", "r").read().strip()

wiring_diagram = dict(
    [
        (w.split(":")[0].strip(), w.split(":")[1].strip().split(" "))
        for w in wiring_diagram.splitlines()
    ]
)



G = nx.Graph()
for w, ngs in wiring_diagram.items():
    for n in ngs:
        G.add_edge(w, n)
      
for e in nx.connectivity.minimum_edge_cut(G):
    G.remove_edge(*e)


connected_components = list(nx.connected_components(G))

print("result:", len(connected_components[0])*len(connected_components[1]))
