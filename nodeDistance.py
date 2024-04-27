import osmnx as ox
import matplotlib.pyplot as plt
import networkx as nx

map = "map (1).osm"
G = ox.graph_from_xml(map)

renaming_mapping = {}
n = 0
for node, data in G.nodes(data=True):
    renaming_mapping[node] = n
    n += 1
G = nx.relabel_nodes(G, renaming_mapping)

fig, ax = ox.plot_graph(G, node_color='white', show=False, close=False, node_size=100)

for node, data in G.nodes(data=True):
    ax.text(data['x'], data['y'], node, fontsize=6, ha='center', va='center', color='black')

node = int(input(f'Select a node from 0 to {len(G.nodes())}: '))

while node not in G.nodes() :
    node = int(input('Invalid. Please Select again: '))

tree = nx.bfs_tree(G,source=node)
distances = {}

for i in G.nodes():
    distances[i] = nx.shortest_path_length(tree,source=node,target=i, method="dijkstra")

for i, distance in distances.items():
    print('Node', i, 'distance is :', distance)

plt.show()