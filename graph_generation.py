import numpy as np
import networkx as nx
import random

def generate_undirected_graph(size, density):
    #NOTE THAT THIS WILL RETURN AN ADJACENCY MATRIX

    #Set our end condition, we set this to true once we get a graph that has every node connected
    done = False

    while not done:
        G = nx.fast_gnp_random_graph(size, density)

        if nx.is_connected(G) == True:
            done = True # We know our graph is connected so we don't need to generate a new one
        else:
            pass

    for u, v in G.edges():
        G[u][v]['weight'] = random.randint(0, 1_000_000)

    adj_matrix = nx.to_numpy_array(G, weight='weight')

    return adj_matrix

def generate_test_cases_undirected(size, density, num_matrices):

    all_matrices = np.zeros((num_matrices, size, size)) #Prepare a matrix of zeros to store our adjacency matrices

    for i in range(num_matrices):
        adj_matrix = generate_undirected_graph(size, density)
        all_matrices[i] = adj_matrix

    path = f"test_cases\\graph_test_cases\\undirected\\size_{size}_density_{density}.npy"
    np.save(path, all_matrices)

if __name__ == '__main__':

    graph_sizes = [10, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
    densities = [.25, .5, .75, 1.0]
    iterations = 25

    for size in graph_sizes:
        for density in densities:
            print(f"Generating Test Cases of Size :{size}, Density: {density} ")
            generate_test_cases_undirected(size, density, iterations)