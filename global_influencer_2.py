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
import numpy as np

file_path = 'socfb-A-anon.mtx'
# file_path='socfb-Haverford76.mtx'
# Initialize an empty graph
G = nx.Graph()

# Open and read the .mtx file manually
with open(file_path, 'r') as file:
    # Read header lines
    header = file.readline().strip()
    while header.startswith('%'):
        header = file.readline().strip()
    
    # Read the dimensions and number of non-zero entries
    rows, cols, num_entries = map(int, header.split())
    
    # Read the edges
    for line in file:
        parts = line.strip().split()
        if len(parts) == 2:
            node1, node2 = map(int, parts)
            G.add_edge(node1 - 1, node2 - 1)
        elif len(parts) == 3:
            node1, node2, _ = map(int, parts)
            G.add_edge(node1 - 1, node2 - 1) 

def find_highest_degree_nodes(G):
    # Calculate degree of each node
    node_degrees = dict(G.degree())

    # Find the maximum degree
    max_degree = max(node_degrees.values())

    # Identify nodes with the maximum degree
    highest_degree_nodes = [node for node, degree in node_degrees.items() if degree == max_degree]

    return highest_degree_nodes, max_degree

# Function to find the average degree
def calculate_average_degree(G):
    degrees = [degree for _, degree in G.degree()]
    average_degree = sum(degrees) / len(degrees)
    return average_degree

# Function to find the degree threshold for the 0.75 percentile
def find_75_percentile_degree(G):
    degrees = [degree for _, degree in G.degree()]
    degrees.sort()
    index = int(len(degrees) * 0.75) - 1  # 0.75 percentile index
    return degrees[index]

# Get nodes with the highest degree
highest_degree_nodes, max_degree = find_highest_degree_nodes(G)

# Calculate average degree
average_degree = calculate_average_degree(G)

# Find the degree threshold for the 0.75 percentile
percentile_75_degree = find_75_percentile_degree(G)

# Function to count the number of nodes with degrees greater than a given threshold
def count_nodes_above_degree(G, threshold):
    return sum(1 for _, degree in G.degree() if degree > threshold)

# Count nodes with degrees greater than 115
nodes_above_115 = count_nodes_above_degree(G, 115)

# Print results
print(f"Node(s) with the highest degree ({max_degree}): {highest_degree_nodes}")
print(f"Average degree: {average_degree}")
print(f"0.75 percentile degree: {percentile_75_degree}")
print(f"Number of nodes with degree greater than 115: {nodes_above_115}")

# Find nodes with more than 115 degrees
