#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 23:03:36 2024

@author: RalfsArvids123
"""

import networkx as nx
import matplotlib.pyplot as plt
import random


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

# ... (Your file reading and graph creation code remain the same)

# SIR model parameters
infection_probability = 0.2  # Probability of transmission per contact
recovery_probability = 0.1  # Probability of recovery per time step
num_time_steps = 100

# Find the node with the highest degree
node_degrees = G.degree()  # Get the degrees of all nodes
highest_degree_node = max(node_degrees, key=lambda x: x[1])[0]  # Find the node with max degree
# Find nodes with degree 10
degree_10_nodes = [node for node, degree in G.degree() if degree == 10]

if not degree_10_nodes:
    raise ValueError("No nodes with degree 10 found in the graph.")

# Choose one node with degree 10 as the initial infected node
initial_infected_nodes = [random.choice(degree_10_nodes)]
# Initial conditions
#initial_infected_nodes = [highest_degree_node]  # Start with the highest degree node

# Initial conditions
#initial_infected_nodes = [random.choice(list(G.nodes()))]  # Start with one random infected node
susceptible_nodes = set(G.nodes()) - set(initial_infected_nodes)
infected_nodes = set(initial_infected_nodes)
recovered_nodes = set()

# Store the time series for S, I, and R
S, I, R = [], [], []

# SIR simulation
for time_step in range(num_time_steps):
    # Record the current state
    S.append(len(susceptible_nodes))
    I.append(len(infected_nodes))
    R.append(len(recovered_nodes))

    new_infected_nodes = set()  # Nodes that become infected in this time step

    # Infection step
    for infected_node in infected_nodes:
        for neighbor in G.neighbors(infected_node):
            if neighbor in susceptible_nodes and random.random() < infection_probability:
                new_infected_nodes.add(neighbor)
                
    # Recovery step
    for infected_node in infected_nodes:
        if random.random() < recovery_probability:
            recovered_nodes.add(infected_node)

    # Update node states
    susceptible_nodes -= new_infected_nodes
    infected_nodes |= new_infected_nodes
    infected_nodes -= recovered_nodes

# Plot SIR curves
plt.figure(figsize=(10, 6))
plt.plot(S, label='Susceptible', color='blue')
plt.plot(I, label='Infected', color='red')
plt.plot(R, label='Recovered', color='green')
plt.xlabel('Time Step')
plt.ylabel('Number of Nodes')
plt.title('SIR Model Simulation (first infected node with highest degree)')
plt.legend()
plt.show()
