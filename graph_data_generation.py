import tracemalloc
import csv
import random
import timeit
from graphs import (
    Naive_Dijkstras,
    Heap_Dijkstras,
    Naive_Kruskals,
    Improved_Kruskals,
    Naive_Prims,
    Heap_Prims,
    generate_connected_graph,
    create_directed_weighted_network,
    create_undirected_weighted_network,
)

algorithms = [
    # Naive_Dijkstras,
    # Heap_Dijkstras,
    Naive_Kruskals,
    Improved_Kruskals,
    Naive_Prims,
    Heap_Prims
]

def measure_time_and_memory(func, *args):
    """Measures time and memory usage of a graph algorithm."""
    tracemalloc.start()
    start_time = timeit.default_timer()
    func(*args)
    elapsed_time = timeit.default_timer() - start_time
    current, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return elapsed_time, peak_memory

def save_results_to_csv(filename, data):
    """Saves analysis data to a CSV file."""
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)

def generate_data_for_algorithm(algorithm, filename_prefix, input_sizes, densities, seed, max_weight=100):
    """Generates runtime and memory usage data for a given algorithm."""
    random.seed(seed)
    runtime_data = [["Input Size"] + densities]
    memory_data = [["Input Size"] + densities]
    
    for size in input_sizes:
        for i in range(25):
            print(f"Running Size: {size}, Iteration: {i}")
            runtime_row = [size]
            memory_row = [size]
            for density in densities:
                # Generate the same graph for all algorithms by setting a seed
                nodes, edges, weights = generate_connected_graph(size, density, max_weight)
                if algorithm.__name__.startswith("Naive_Dijkstras") or algorithm.__name__.startswith("Heap_Dijkstras"):
                    network = create_directed_weighted_network(edges, weights)
                    runtime, memory = measure_time_and_memory(algorithm, network, nodes, 1, size//2)
                elif algorithm.__name__.startswith("Naive_Kruskals") or algorithm.__name__.startswith("Improved_Kruskals"):
                    runtime, memory = measure_time_and_memory(algorithm, nodes, edges, weights)
                elif algorithm.__name__.startswith("Naive_Prims") or algorithm.__name__.startswith("Heap_Prims"):
                    network = create_undirected_weighted_network(edges, weights)
                    runtime, memory = measure_time_and_memory(algorithm, network, nodes, 1)
                runtime_row.append(runtime)
                memory_row.append(memory)
            runtime_data.append(runtime_row)
            memory_data.append(memory_row)

    save_results_to_csv(f"{filename_prefix}_runtime.csv", runtime_data)
    save_results_to_csv(f"{filename_prefix}_memory.csv", memory_data)

if __name__ == "__main__":
    # User-specified parameters
    input_sizes = [10, 50, 100, 250, 500, 750, 1000]

    densities = [0.25, 0.5, 0.75, 1.0]
    seed = 2024  # Ensure reproducibility
    
    # Replace with the desired algorithm to test
    algorithm = Naive_Prims  # Example: change this to test other algorithms


    for algorithm in algorithms:
        filename_prefix = f"data/{algorithm.__name__.lower()}"
        generate_data_for_algorithm(algorithm, filename_prefix, input_sizes, densities, seed)
