import osmnx as ox
import matplotlib.pyplot as plt
import networkx as nx
import imageio
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def create_frame(G, path, j, source, goal):
    fig, ax = ox.plot_graph(G, node_color='white', show=False, close=False, node_size=100)

    pos={}

    for node, data in G.nodes(data=True):
        pos[node]=(data['x'],data['y'])

    for node, data in G.nodes(data=True):
        ax.text(data['x'], data['y'], node, fontsize=6, ha='center', va='center', color='black')
        if (node == source) :
            ax.text(data['x'], data['y'], " ━━━━━ Source", fontsize=12, ha='left', va='center', color='r')
        if (node == goal):
            ax.text(data['x'], data['y'], " ━━━━━ Target", fontsize=12, ha='left', va='center', color='r')

    nx.draw_networkx_edges(G, pos=pos, edgelist=[(path[i], path[i+1]) for i in range(len(path)-1)], edge_color=(255/255, 255/255, 0/255), width=3, arrows=False)
    
    plt.savefig(f'./img/img_{j}.png', 
                transparent = False,  
                facecolor = 'white'
               )

def generate_gif(G, source, goal):
    path = nx.astar_path(G, source, goal, weight='length')
    print("Shortest Path:", path)

    frames = []

    for i, _ in enumerate(path):
        create_frame(G, path[:i+1], i, source, goal)
        image = imageio.v2.imread(f'./img/img_{i}.png')
        frames.append(image)

    imageio.mimsave('./ShortesthPath.gif',
                    frames,          
                    fps = 3)       

    for i, _ in enumerate(path):
        os.remove(f'./img/img_{i}.png')
        
    os.system('start "" "./ShortesthPath.gif"')  # with the default program

def select_map():
    global map_file
    map_file = filedialog.askopenfilename(filetypes=[("OSM Files", "*.osm")])
    
    if map_file:
        show_map()

def show_map():
    global G, pos
    G = ox.graph_from_xml(map_file)
    renaming_mapping = {}
    n = 0

    pos={}

    for node, data in G.nodes(data=True):
        pos[node]=(data['x'],data['y'])

    for node, data in G.nodes(data=True):
        renaming_mapping[node] = n
        n += 1
    G = nx.relabel_nodes(G, renaming_mapping)

    fig, ax = ox.plot_graph(G, node_color='white', show=False, close=False, node_size=100)

    for node, data in G.nodes(data=True):
        ax.text(data['x'], data['y'], node, fontsize=6, ha='center', va='center', color='black')

    source_goal_window(G)

    plt.show()

def source_goal_window(G):
    source_goal_window_popup = tk.Toplevel(root)  # Renamed the variable to avoid conflict
    source_goal_window_popup.title("Source and Goal Selection")
    center_window(source_goal_window_popup)  # Center the source and goal selection window

    source_label = tk.Label(source_goal_window_popup, text="Select Source Node:")
    source_label.grid(row=0, column=0, padx=5, pady=5)
    source_var = tk.StringVar()
    source_var.set("Select Source")
    source_menu = tk.OptionMenu(source_goal_window_popup, source_var, *G.nodes())
    source_menu.grid(row=0, column=1, padx=5, pady=5)

    goal_label = tk.Label(source_goal_window_popup, text="Select Goal Node:")
    goal_label.grid(row=1, column=0, padx=5, pady=5)
    goal_var = tk.StringVar()
    goal_var.set("Select Goal")
    goal_menu = tk.OptionMenu(source_goal_window_popup, goal_var, *G.nodes())
    goal_menu.grid(row=1, column=1, padx=5, pady=5)

    search_button = tk.Button(source_goal_window_popup, text="Search Shortest Path", command=lambda: on_search_click(G, source_var.get(), goal_var.get(), source_goal_window_popup))
    search_button.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

def on_search_click(G, source, goal, window):
    if source == "Select Source" or goal == "Select Goal":
        messagebox.showerror("Error", "Please select both source and goal nodes.")
    else:
        generate_gif(G, int(source), int(goal))
        window.destroy()

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x_offset = (window.winfo_screenwidth() - width) // 2
    y_offset = (window.winfo_screenheight() - height) // 2
    window.geometry(f"+{x_offset}+{y_offset}")

# Main Tkinter setup
root = tk.Tk()
root.title("Shortest Path Finder")
root.geometry("300x150")
root.resizable(False, False)
center_window(root) 

map_file = ""
map_window = tk.Frame(root)

map_button = tk.Button(map_window, text="Select Map File", command=select_map)
map_button.pack(pady=20)

map_window.pack()

root.mainloop()
