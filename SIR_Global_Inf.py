# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 13:41:13 2024

@author: marma
"""
import matplotlib.pyplot as plt
import random
from Analysis import global_inf_deg_BA,global_inf_deg_FB,G,BA_graph,node_high_perc_BA, node_high_con_BA, node_high_perc_FB,node_high_con_FB





def sim(G, n, t):
    # SIR model parameters
    infection_probability = 0.5
    recovery_probability = 0.2  
    num_time_steps = 40

    initial_infected_nodes = [n]
    # Initial conditions

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
    plt.title(f'SIR Model: Global Influencer {t}')
    plt.legend()
    plt.show()


# Key  BA
sim(BA_graph,global_inf_deg_BA, "BA Network")
sim(BA_graph, node_high_perc_BA, "BA Network")
sim(BA_graph, node_high_con_BA, "BA Network")

# Key Facebook
sim(G,global_inf_deg_FB, "Facebook Network")
sim(G, node_high_perc_FB, "Facebook Network")
sim(G, node_high_con_FB, "Facebook Network")
