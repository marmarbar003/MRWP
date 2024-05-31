import networkx as nx
import matplotlib.pyplot as plt  # Fix import of pyplot
import community as community_louvain

#file_path = 'socfb-A-anon.mtx'
file_path='socfb-Haverford76.mtx'
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
def visualize(G):
    plt.figure(figsize=(8, 6))
    nx.draw(G, with_labels=True, node_color='skyblue', edge_color='gray', node_size=500, font_size=5)
    plt.show()

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

    # Degree centrality
    degree_centrality = nx.degree_centrality(G)
    print(f"Degree centrality (sample): {dict(list(degree_centrality.items())[:5])}")
    
    # Closeness centrality
    closeness_centrality = nx.closeness_centrality(G)
    print(f"Closeness centrality (sample): {dict(list(closeness_centrality.items())[:5])}")
    
    # Betweenness centrality
    betweenness_centrality = nx.betweenness_centrality(G)
    print(f"Betweenness centrality (sample): {dict(list(betweenness_centrality.items())[:5])}")
    
    # Eigenvector centrality
    eigenvector_centrality = nx.eigenvector_centrality(G, max_iter=1000)
    print(f"Eigenvector centrality (sample): {dict(list(eigenvector_centrality.items())[:5])}")

    print("\nAdditional Network Analysis:")
    
    # Connected components
    num_connected_components = nx.number_connected_components(G)
    largest_cc = max(nx.connected_components(G), key=len)
    print(f"Number of connected components: {num_connected_components}")
    print(f"Size of largest connected component: {len(largest_cc)}")

    # Community detection (Louvain method)
    partition = community_louvain.best_partition(G)  # Use the correct function from python-louvain
    num_communities = len(set(partition.values()))
    modularity = community_louvain.modularity(partition, G)
    print(f"Number of communities (Louvain): {num_communities}")
    print(f"Modularity (Louvain): {modularity}")

# Analyze graph properties
analyze_graph_properties(G)

num_nodes = G.number_of_nodes()
avg_degree = sum(dict(G.degree()).values()) / num_nodes
m = int(avg_degree / 2)

# Create the BA graph
BA_graph = nx.barabasi_albert_graph(num_nodes, m)



# Analyze BA graph properties
print("\nProperties of the Barabási–Albert (BA) graph:")
analyze_graph_properties(BA_graph)