import networkx as nx
import matplotlib.pyplot as plt  # Fix import of pyplot
from scipy.stats import norm, powerlaw
import numpy as np

file_path = '/Users/giamihuynh/Downloads/socfb-Haverford76/socfb-Haverford76.mtx'

# Initialize an empty graph
G = nx.Graph()

# Open and read the .mtx file manually
with open(file_path, 'r') as file:
    # Skip the header lines starting with '%'
    for line in file:
        if line.startswith('%'):
            continue
        # Split the line into nodes (assuming space-separated values)
        parts = line.strip().split()
        if len(parts) == 3:
            node1, node2, _ = map(int, parts)  # Read nodes and ignore the third part
        else:
            node1, node2 = map(int, parts)
        
        # Add edges to the graph (Matrix Market is 1-indexed, so adjust to 0-indexed)
        G.add_edge(node1 - 1, node2 - 1)

# Visualize the graph
# plt.figure(figsize=(8, 6))
# nx.draw(G, with_labels=True, node_color='skyblue', edge_color='gray', node_size=500, font_size=5)
# plt.show()

# Function to plot degree distribution and fit distributions
def plot_degree_distribution(G):
    degree_sequence = [d for n, d in G.degree()]
    plt.hist(degree_sequence, bins=50, density=True, alpha=0.75, color='blue', label='Degree Distribution')

    # Fit a normal distribution
    mu, std = norm.fit(degree_sequence)
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2, label='Normal fit')

    # Fit a power-law distribution
    a, loc, scale = powerlaw.fit(degree_sequence)
    p = powerlaw.pdf(x, a, loc, scale)
    plt.plot(x, p, 'r--', linewidth=2, label='Power-law fit')

    plt.legend()
    plt.xlabel('Degree')
    plt.ylabel('Density')
    plt.title('Degree Distribution')
    plt.show()

# Plot degree distribution for the graph
plot_degree_distribution(G)

def analyze_graph_properties(G):
    print(f"Number of nodes: {G.number_of_nodes()}")
    print(f"Number of edges: {G.number_of_edges()}")
    print(f"Average degree: {sum(dict(G.degree()).values()) / G.number_of_nodes()}")
    print(f"Average clustering coefficient: {nx.average_clustering(G)}")
    try:
        avg_shortest_path_length = nx.average_shortest_path_length(G)
        print(f"Average shortest path length: {avg_shortest_path_length}")
    except nx.NetworkXError as e:
        print(f"Error calculating average shortest path length: {e}")

    degree_centrality = nx.degree_centrality(G)
    print(f"Degree centrality (sample): {dict(list(degree_centrality.items())[:5])}")

# Analyze graph properties
analyze_graph_properties(G)
