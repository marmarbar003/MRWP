#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 31 10:49:42 2024

@author: RalfsArvids123
"""

"""
global influencer: connections to others with high connections
"""
import networkx as nx

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


# Find nodes with many connections to high-degree nodes
def nodes_connected_to_high_degree_nodes(G, degree_threshold):
    # Calculate degree of each node
    node_degrees = dict(G.degree())

    # Identify high-degree nodes
    high_degree_nodes = {node for node, degree in node_degrees.items() if degree > degree_threshold}

    # Find nodes with many connections to high-degree nodes
    nodes_with_many_high_degree_connections = {}
    for node in G.nodes():
        high_degree_connections = [neighbor for neighbor in G.neighbors(node) if neighbor in high_degree_nodes]
        if high_degree_connections:
            nodes_with_many_high_degree_connections[node] = high_degree_connections

    return nodes_with_many_high_degree_connections

# Set degree threshold for high-degree nodes
degree_threshold = 10

# Get nodes connected to high-degree nodes
nodes_with_many_high_degree_connections = nodes_connected_to_high_degree_nodes(G, degree_threshold)

# Print nodes with their connections to high-degree nodes
print("Nodes with many connections to high-degree nodes:")
for node, connections in nodes_with_many_high_degree_connections.items():
    print(f"Node {node} is connected to high-degree nodes: {connections}")


