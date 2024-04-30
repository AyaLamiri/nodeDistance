import osmnx as ox
import matplotlib.pyplot as plt
import networkx as nx

map_file = "map (1).osm"
G = ox.graph_from_xml(map_file)

renaming_mapping = {}
n = 0
for node, data in G.nodes(data=True):
    renaming_mapping[node] = n
    n += 1
G = nx.relabel_nodes(G, renaming_mapping)

fig, ax = ox.plot_graph(G, node_color='white', show=False, close=False, node_size=100)

for node, data in G.nodes(data=True):
    ax.text(data['x'], data['y'], node, fontsize=6, ha='center', va='center', color='black')

node = int(input(f'Select a node from 0 to {len(G.nodes()) - 1} to start from: '))
while node not in G.nodes():
    node = int(input('Invalid. Please select again: '))

goal = int(input(f'Select a node from 0 to {len(G.nodes()) - 1} to go to: '))
while goal not in G.nodes():
    goal = int(input('Invalid. Please select again: '))

path = nx.astar_path(G, node, goal, weight='length')
print("Shortest Path:", path)

pos={}

edges=[]

for node, data in G.nodes(data=True):
    pos[node]=(data['x'],data['y'])

nx.draw_networkx_edges(G,pos=pos, edgelist=G.edges(),edge_color='r',width=3)

plt.show()
