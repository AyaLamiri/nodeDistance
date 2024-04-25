import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

filename = 'map (1).osm'
G = ox.graph_from_xml(filename)

mapping = {node: f"{i}" for i, node in enumerate(G.nodes())}
G = nx.relabel_nodes(G, mapping)

selected_node = input("Enter the name of the node you want to start from: ")

if selected_node not in G.nodes():
    print("Error")
    exit()

bfs_tree = nx.bfs_tree(G, source=selected_node)
distances = {node: nx.shortest_path_length(bfs_tree, source=selected_node, target=node) for node in G.nodes()}

print("Distances from", selected_node, "to each node:")
for node, distance in distances.items():
    print("Node:", node, "Distance:", distance)

fig, ax = ox.plot_graph(G, show=False, close=False, node_color='blue', node_size=30, edge_linewidth=0.5)

for node, data in G.nodes(data=True):
    ax.text(data['x'], data['y'], node, fontsize=9, ha='center', va='center', color='red')

plt.show()
