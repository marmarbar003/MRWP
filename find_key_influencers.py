#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 31 10:46:50 2024

@author: RalfsArvids123
"""

import networkx as nx
import matplotlib.pyplot as plt
import community as community_louvain

# file_path = 'socfb-A-anon.mtx'
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
        
        
def find_louvain_communities(G):
    partition = community_louvain.best_partition(G)
    return partition

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

# Analyze graph properties and find communities
def analyze_and_find_communities(G):
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
    
    closeness_centrality = nx.closeness_centrality(G)
    print(f"Closeness centrality (sample): {dict(list(closeness_centrality.items())[:5])}")
    
    betweenness_centrality = nx.betweenness_centrality(G)
    print(f"Betweenness centrality (sample): {dict(list(betweenness_centrality.items())[:5])}")
    
    eigenvector_centrality = nx.eigenvector_centrality(G, max_iter=1000)
    print(f"Eigenvector centrality (sample): {dict(list(eigenvector_centrality.items())[:5])}")

    print("\nAdditional Network Analysis:")
    
    # Connected components
    num_connected_components = nx.number_connected_components(G)
    largest_cc = max(nx.connected_components(G), key=len)
    print(f"Number of connected components: {num_connected_components}")
    print(f"Size of largest connected component: {len(largest_cc)}")

    # Community detection (Louvain method)
    partition = find_louvain_communities(G)
    num_communities = len(set(partition.values()))
    modularity = community_louvain.modularity(partition, G)
    print(f"Number of communities (Louvain): {num_communities}")
    print(f"Modularity (Louvain): {modularity}")

    highest_degree_nodes = highest_degree_in_communities(G, partition)
    print("\nNodes with highest degree in each community:")
    for community, node in highest_degree_nodes.items():
        print(f"Community {community}: Node {node} with degree {G.degree[node]}")

# Analyze graph properties and find communities
analyze_and_find_communities(G)