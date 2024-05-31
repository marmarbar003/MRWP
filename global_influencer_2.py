#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 31 10:51:53 2024

@author: RalfsArvids123
"""
"""
global influencer: many connections overall
"""

import networkx as nx


file_path = 'socfb-A-anon.mtx'
#file_path='socfb-Haverford76.mtx'
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



# Find node(s) with the highest degree
def find_highest_degree_nodes(G):
    # Calculate degree of each node
    node_degrees = dict(G.degree())

    # Find the maximum degree
    max_degree = max(node_degrees.values())

    # Identify nodes with the maximum degree
    highest_degree_nodes = [node for node, degree in node_degrees.items() if degree == max_degree]

    return highest_degree_nodes, max_degree

# Get nodes with the highest degree
highest_degree_nodes, max_degree = find_highest_degree_nodes(G)

# Print nodes with the highest degree
print(f"Node(s) with the highest degree ({max_degree}): {highest_degree_nodes}")

