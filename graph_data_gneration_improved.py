import tracemalloc
import csv
import random
import timeit
import numpy as np
import graphs_adj_mat as graphs

SHORTEST_PATH_ALGORITHMS = {
    'naive_dijkstras' : graphs.Naive_Dijkstras,
    'heap_dijkstras' : graphs.Heap_Dijkstras
}

MCST_ALGORITHMS = {
    'naive_prims' : graphs.Naive_Prims,
    'heap_prims' : graphs.Heap_Prims,
    'naive_kruskals' : graphs.Naive_Kruskals,
    'improved_kruskals' : graphs.Improved_Kruskals

}

GRAPH_SIZES = [10, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
GRAPH_SIZES = [600]
DENSITIES = [.25, .5, .75, 1.0]


def measure_time_and_memory(func, *args):
    """Measures time and memory usage of a graph algorithm."""
    tracemalloc.start()
    start_time = timeit.default_timer()
    func(*args)
    elapsed_time = timeit.default_timer() - start_time
    current, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return elapsed_time, peak_memory

def read_test_cases(directed, size, density):
    return np.load(f"test_cases\\graph_test_cases\\{directed}\\size_{size}_density_{density}.npy")

#Just allows us to convert to a collection of nodes and edges without the matrix
#This is pretty much just for kruskals
def convert_matrix(matrix):
    nodes = []
    edges = []
    dist = {}

    for i in range(len(matrix)):
        nodes.append(i)
        for j in range(i + 1, len(matrix)):
            if matrix[i][j] != 0:
                edges.append((i, j))
                dist[(i, j)] = matrix[i][j]

    return nodes, edges, dist

# Save results
def save_results_to_csv(filename, data):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Num Nodes", "Density 0.25", "Density 0.50", "Density 0.75", "Density 1.0"])
        writer.writerows(data)

# Main execution flow
def run_analysis_mcst():

    runtime_data = []
    memory_data = []

    for algorithm_name, graph_function in MCST_ALGORITHMS.items():
        random.seed(2024) #DO NOT TOUCH THIS, It is critically important that we set the seed everytime that we change algorithms, this lets every algorithm run on the same set of test instances!
        runtime_data.clear()  # Clear results for each algorithm
        memory_data.clear()
        output_file_runtime = f"graph_data\\{algorithm_name}_runtime.csv"  # Output file name for runtime
        output_file_memory = f"graph_data\\{algorithm_name}_memory.csv"  # Output file name for memory

        print(f"Running analysis for {algorithm_name}...")

        for size in GRAPH_SIZES:
            data_25 = read_test_cases("undirected", size, 0.25) #Read in test cases for this size/density
            data_50 = read_test_cases("undirected", size, 0.5) #Read in test cases for this size/density
            data_75 = read_test_cases("undirected", size, 0.75) #Read in test cases for this size/density
            data_10 = read_test_cases("undirected", size, 1.0) #Read in test cases for this size/density

            data_groups = [data_25, data_50, data_75, data_10]

            for i in range(2):
                print(f"Running {algorithm_name} on Size {size} Iteration {i}")
                runtime_row = [size]
                memory_row = [size]
                for data in data_groups:
                    
                    if algorithm_name == "naive_kruskals" or algorithm_name == "improved_kruskals": #Kruskals is passed an adjacency list, not a matrix
                        nodes, edges, dist = convert_matrix(data[i])
                        time_taken, peak_memory = measure_time_and_memory(graph_function, nodes, edges, dist)  # Pass a copy to preserve data
                        
                    else:
                        nodes = []
                        for j in range(len(data[i])):
                            nodes.append(j)
                        time_taken, peak_memory = measure_time_and_memory(graph_function, data[i], nodes, random.randint(0, size - 1))

                    runtime_row.append(time_taken)
                    memory_row.append(peak_memory)
                runtime_data.append(runtime_row)
                memory_data.append(memory_row)

        save_results_to_csv(output_file_runtime, runtime_data)
        save_results_to_csv(output_file_memory, runtime_data)

        print(f"Results for {algorithm_name} saved to:\n\t{output_file_runtime}\n\t{output_file_memory}")



if __name__ == '__main__':

    run_analysis_mcst()