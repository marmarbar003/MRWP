#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 12:41:52 2024

@author: RalfsArvids123
"""

import networkx as nx
import matplotlib.pyplot as plt  # Fix import of pyplot
from scipy.stats import norm, powerlaw
import numpy as np
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
        
# Function to plot degree distribution and fit distributions

def plot_degree_distribution(G):
    degree_sequence = [d for n, d in G.degree()]
    plt.hist(degree_sequence, bins=100, density=True, alpha=0.75, color='blue', label='Degree Distribution')
    """
    # Fit a normal distribution
    mu, std = norm.fit(degree_sequence)
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 5)
    p = norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2, label='Normal fit')

    # Fit a power-law distribution
    a, loc, scale = powerlaw.fit(degree_sequence)
    p = powerlaw.pdf(x, a, loc, scale)
    plt.plot(x, p, 'r--', linewidth=2, label='Power-law fit')
    """
    plt.legend()
    plt.xlabel('Degree')
    plt.ylabel('Density')
    plt.title('Degree Distribution')
    plt.show()

# Plot degree distribution for the graph
#plot_degree_distribution(G)



def plot_degree_distribution_counts_new(G, max_degree=1000):
    degree_sequence = [d for n, d in G.degree()]
    max_degree_to_display = max_degree

    # Filter degrees exceeding the limit
    filtered_degrees = [d for d in degree_sequence if d <= max_degree_to_display]

    # Create bins and count occurrences in each bin
    bins = range(1, max_degree_to_display + 2)  
    counts, _ = np.histogram(filtered_degrees, bins=bins) 

    # Plot the degree distribution with counts (no density=True)
    plt.bar(bins[:-1], counts, width=1, alpha=0.75, color='blue', label='Degree Counts')
    

    # Fit a normal distribution
    mu, std = norm.fit(degree_sequence)
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 5)
    p = norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2, label='Normal fit')

    # Fit a power-law distribution
    a, loc, scale = powerlaw.fit(degree_sequence)
    p = powerlaw.pdf(x, a, loc, scale)
    plt.plot(x, p, 'r--', linewidth=2, label='Power-law fit')

    # Set x-axis limits explicitly
    plt.xlim(0, max_degree_to_display + 1)

    plt.xlabel('Degree')
    plt.ylabel('Count') # Changed from Density to Count
    plt.title(f'Degree Distribution Counts (up to {max_degree_to_display})')
    plt.show()

# Plot the degree distribution with the first 1000 degrees
plot_degree_distribution_counts_new(G, max_degree=80) 
