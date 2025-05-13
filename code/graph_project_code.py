# Final Combined Evacuation Analysis Code

import networkx as nx
import matplotlib.pyplot as plt

# ----- Function to Create Evacuation Graphs for Each Floor -----
def create_evacuate_graph(floor_name, nodes, edges, exits):
    G_floor = nx.DiGraph()
    G_floor.add_nodes_from(nodes)
    G_floor.add_weighted_edges_from(edges)

    # Connect exits to a pseudo-exit node
    pseudo_exit = f"Pseudo-Exit-{floor_name}"
    G_floor.add_node(pseudo_exit)
    exit_edges = [(exit_node, pseudo_exit, 25) for exit_node in exits]  # Assuming exits have equal capacity
    G_floor.add_weighted_edges_from(exit_edges)

    return G_floor, pseudo_exit

# ----- Define Nodes and Edges for Each Floor -----
# Ground Floor
ground_nodes = ["Entrance", "Reception", "Hallway 1", "Hallway 2", "Cafeteria", "Admission Office", "Exit 1", "Exit 2"]
ground_edges = [
    ("Entrance", "Reception", 50), ("Reception", "Hallway 1", 40), ("Reception", "Hallway 2", 30),
    ("Hallway 1", "Admission Office", 25), ("Hallway 2", "Cafeteria", 30),
    ("Hallway 1", "Exit 1", 20), ("Hallway 2", "Exit 2", 20)
]
ground_exits = ["Exit 1", "Exit 2"]
ground_graph, ground_pseudo_exit = create_evacuate_graph("Ground Floor", ground_nodes, ground_edges, ground_exits)

# Mezzanine
mezzanine_nodes = ["Dining Hall", "Test Center", "Doctor's Office", "Staircase", "Exit 3"]
mezzanine_edges = [
    ("Dining Hall", "Test Center", 20), ("Dining Hall", "Doctor's Office", 15),
    ("Test Center", "Exit 3", 25), ("Doctor's Office", "Exit 3", 20),
    ("Staircase", "Exit 3", 30)
]
mezzanine_exits = ["Exit 3"]
mezzanine_graph, mezzanine_pseudo_exit = create_evacuate_graph("Mezzanine", mezzanine_nodes, mezzanine_edges, mezzanine_exits)

# First Floor
first_floor_nodes = ["Hallway A", "Classroom A-102", "Classroom A-103", "Registrar Office", "Staircase", "Exit 4"]
first_floor_edges = [
    ("Hallway A", "Classroom A-102", 20), ("Hallway A", "Classroom A-103", 20),
    ("Hallway A", "Registrar Office", 15), ("Hallway A", "Staircase", 25),
    ("Staircase", "Exit 4", 30)
]
first_floor_exits = ["Exit 4"]
first_floor_graph, first_floor_pseudo_exit = create_evacuate_graph("First Floor", first_floor_nodes, first_floor_edges, first_floor_exits)

# Second Floor
second_floor_nodes = ["Career Center", "Meeting Room", "A-200", "A-201", "Staircase", "Exit 5"]
second_floor_edges = [
    ("Career Center", "Meeting Room", 20), ("Meeting Room", "A-200", 30),
    ("Meeting Room", "A-201", 25), ("A-200", "Exit 5", 30), ("A-201", "Exit 5", 30),
    ("Staircase", "Exit 5", 40)
]
second_floor_exits = ["Exit 5"]
second_floor_graph, second_floor_pseudo_exit = create_evacuate_graph("Second Floor", second_floor_nodes, second_floor_edges, second_floor_exits)

# ----- Calculate Max-Flow for Each Floor -----
flow_results = {}

for floor_name, graph, pseudo_exit in [
    ("Ground Floor", ground_graph, ground_pseudo_exit),
    ("Mezzanine", mezzanine_graph, mezzanine_pseudo_exit),
    ("First Floor", first_floor_graph, first_floor_pseudo_exit),
    ("Second Floor", second_floor_graph, second_floor_pseudo_exit),
]:
    flow_value, _ = nx.maximum_flow(graph, list(graph.nodes)[0], pseudo_exit, capacity="weight")
    flow_results[floor_name] = flow_value

# Prepare data for plots
floors = list(flow_results.keys())
max_flows = list(flow_results.values())
bottlenecks = [
    'Hallway 1 & 2 - Exit flow constrained',
    "Doctor's Office & Test Center",
    'Staircase to Exit 4',
    'Meeting Room to A-200'
]

# ----- Plot 1: Max Flow per Floor -----
plt.figure(figsize=(10,6))
plt.bar(floors, max_flows, color='skyblue', edgecolor='black')
plt.title('Max Flow per Floor (People Evacuated per Minute)', fontsize=16)
plt.xlabel('Floor', fontsize=14)
plt.ylabel('Max Flow (People per Minute)', fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('max_flow_per_floor.png')
plt.show()

# ----- Plot 2: Bottlenecks Highlight -----
plt.figure(figsize=(10,6))
colors = ['red' if flow <= 25 else 'green' for flow in max_flows]
plt.barh(floors, max_flows, color=colors, edgecolor='black')

for idx, bottleneck in enumerate(bottlenecks):
    plt.text(max_flows[idx]+1, idx, bottleneck, va='center', fontsize=10)

plt.title('Evacuation Bottlenecks per Floor', fontsize=16)
plt.xlabel('Max Flow (People per Minute)', fontsize=14)
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('bottlenecks_per_floor.png')
plt.show()

# ----- Plot 3: Evacuation Graphs per Floor -----
def plot_evacuation_graph(graph, floor_name):
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph, seed=42, k=2)  # <== increased spacing here
    node_colors = []
    for node in graph.nodes():
        if 'Exit' in node and 'Pseudo' not in node:
            node_colors.append('green')
        elif 'Pseudo' in node:
            node_colors.append('yellow')
        else:
            node_colors.append('skyblue')

    nx.draw(graph, pos, with_labels=True, node_color=node_colors, node_size=2500, font_size=10, edge_color='gray')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels={(u, v): f"{w}" for u, v, w in graph.edges(data="weight")})
    plt.title(f"Evacuation Graph - {floor_name}")
    plt.tight_layout()
    plt.savefig(f"{floor_name.lower().replace(' ', '_')}_evacuation_graph.png")
    plt.show()


# Plot each floor's graph
plot_evacuation_graph(ground_graph, "Ground Floor")
plot_evacuation_graph(mezzanine_graph, "Mezzanine")
plot_evacuation_graph(first_floor_graph, "First Floor")
plot_evacuation_graph(second_floor_graph, "Second Floor")

# ----- Print Max-Flow Results -----
print("Max-Flow Results for Each Floor:")
for floor, flow in flow_results.items():
    print(f"{floor}: Max Flow = {flow}")
