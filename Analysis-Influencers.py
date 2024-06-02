# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 12:02:21 2024

@author: marma
"""

import networkx as nx
import matplotlib.pyplot as plt  # Fix import of pyplot
import community


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
    
    partition = community.best_partition(G)
    modularity = community.modularity(partition, G)
    num_communities = len(set(partition.values()))

    print(f"Number of communities (Louvain): {num_communities}")
    print(f"Modularity (Louvain): {modularity}")


# Analyze graph properties
analyze_graph_properties(G)

num_nodes = G.number_of_nodes()
avg_degree = sum(dict(G.degree()).values()) / num_nodes
m = int(avg_degree / 2)

# Create the BA graph
BA_graph = nx.barabasi_albert_graph(1446, 41, seed = 3 )
print(len(BA_graph.nodes))
analyze_graph_properties(BA_graph)

### Assuming its based on degree cenrtality #####

# Analyze BA graph properties

def Global_Inf_centrality(gr) :

    degree_centrality = nx.degree_centrality(gr)

    top_5_nodes = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]

    for node, centrality in top_5_nodes:
        centrality_r = round(centrality, 5)
        print(f"Node: {node}, Degree Centrality: {centrality_r}")
        
print("\nGlobal Influencers FB graph:") 
Global_Inf_centrality(G)
print("\nGlobal Influencers BA graph:")
Global_Inf_centrality(BA_graph)

# Highest degree nodes
def find_highest_degree_nodes(G, num_nodes=5):
    node_degrees = dict(G.degree())

    sorted_nodes = sorted(node_degrees.items(), key=lambda x: x[1], reverse=True)

    highest_degree_nodes = sorted_nodes[:num_nodes]

    return highest_degree_nodes

print("FB network highest degree nodes")
highest_degree_nodes = find_highest_degree_nodes(G, 5)

for node, degree in highest_degree_nodes:
    print(f"Node : {node}, with degree {degree}")
    
highest_degree_nodes = find_highest_degree_nodes(BA_graph, 10)
print("BA-model highest degree nodes")
for node, degree in highest_degree_nodes:
    print(f"Node : {node}, with degree {degree}")


# Find nodes with the highest degree in each community
def highest_degree_in_communities(G, partition):
    communities = {}
    for node, community in partition.items():
        if community not in communities:
            communities[community] = []
        communities[community].append(node)
    
    highest_degree_nodes = {}
    for community, nodes in communities.items():
        highest_degree_node = max(nodes, key=lambda node: G.degree[node])
        highest_degree_nodes[community] = highest_degree_node
    
    return highest_degree_nodes


# Perform louvain partition CHECK IF CORRECT
def partition(G, t):
    communities = {}
    partition = community.best_partition(G)
    modularity = community.modularity(partition, G)
    num_communities = len(set(partition.values()))
    
    for node, community_id in partition.items():
        if community_id not in communities:
            communities[community_id] = [node]
        else:
            communities[community_id].append(node)


    community_list = [nodes for community_id, nodes in communities.items()]
    
    print(f"Number of communities (Louvain) {t}: {num_communities}")
    print(f"Modularity (Louvain): {modularity}")
    
    highest_degree_nodes = highest_degree_in_communities(G, partition)
    print(f"\nKey Influencer (highest degree) in each community for {t}:")
    for com, node in highest_degree_nodes.items():
        print(f"Community {com}: Node {node} with degree {G.degree[node]}")

    return community_list

community_G = partition(G, "FB Network")

community_BA = partition(BA_graph, "BA Network")

