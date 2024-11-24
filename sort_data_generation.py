import random
import tracemalloc
import csv
import timeit
import sorts

# Dictionary mapping sorting names to functions from sorts.py
SORTING_ALGORITHMS = {
    # 'heap_sort': sorts.heap_sort,
    # 'bucket_sort': lambda arr: sorts.bucket_sort(arr, len(arr), 0),
    'selection_sort': sorts.selection_sort,
    # 'merge_sort': sorts.merge_sort  # Merge sort requires bounds
    # 'quick_sort': lambda arr: sorts.quick_sort(arr),
    
    }

# Data generation utilities
def generate_list(size, generator, **kwargs):
    """Generates a list using the specified generator function."""
    return generator(size, **kwargs)

def generate_uniform_list(size):
    return [1 for i in range (0, size)]

def generate_random_list(size):
    """Generates a list of random integers of given size."""
    return [random.randint(0, size) for _ in range(size)]

def generate_almost_sorted_list(size, disorder_percentage=0.2):
    """Generates an almost sorted list of random integers with a given size and disorder percentage."""
    # Create a sorted list of random integers
    sorted_list = [i for i in range(0, size)]
    
    # Determine the number of elements to swap to introduce disorder
    num_disordered_elements = int(size * disorder_percentage)
    
    for i in range(num_disordered_elements):
        # Randomly select two indices to swap
        sorted_list[i] = random.randint(0, size)
    
    return sorted_list

def generate_almost_reverse_sorted_list(size, disorder_percentage=0.2):
    """Generates an almost reverse sorted list of random integers with a given size and disorder percentage."""
    # Create a reverse sorted list of random integers
    reverse_sorted_list = [i for i in range(size, 0, -1)]
    
    # Determine the number of elements to swap to introduce disorder
    num_disordered_elements = int(size * disorder_percentage)
    
    for i in range(num_disordered_elements):
        # Randomly select two indices to swap
        reverse_sorted_list[i] = random.randint(0, size)
    
    return reverse_sorted_list

# Performance measurement utilities
def measure_time_and_memory(sort_function, data):
    tracemalloc.start()
    time_taken = timeit.timeit(lambda: sort_function(data), number=1)
    current, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return time_taken, peak_memory

# Save results
def save_results_to_csv(filename, data):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["List Size", "Time Taken (s)", "Peak Memory Usage (bytes)"])
        writer.writerows(data)

# Main execution flow
def run_analysis(generator, list_sizes, iterations, output_dir="data", **kwargs):
    results = []
    for algorithm_name, sort_function in SORTING_ALGORITHMS.items():
        random.seed(2024) #DO NOT TOUCH THIS, It is critically important that we set the seed everytime that we change algorithms, this lets every algorithm run on the same set of test instances!
        results.clear()  # Clear results for each algorithm
        output_file = f"{output_dir}/{algorithm_name}_{generator.__name__}.csv"  # Output file name
        print(f"Running analysis for {algorithm_name} using {generator.__name__}...")
        for size in list_sizes:
            for _ in range(iterations):
                data = generate_list(size, generator, **kwargs)
                time_taken, peak_memory = measure_time_and_memory(sort_function, data.copy())  # Pass a copy to preserve data
                results.append([size, time_taken, peak_memory])
            print(f"Size {size}: Completed {iterations} iterations.")
        save_results_to_csv(output_file, results)
        print(f"Results for {algorithm_name} saved to {output_file}")

# Main function, run this to test all sorting algorithms
if __name__ == "__main__":
    # list_sizes = [10, 50, 100, 500, 1000, 5000, 10000, 50000, 100000, 500000, 1000000]  # List sizes
    list_sizes = [10, 50, 100, 500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
    iterations = 25  # Number of repetitions for each size

    # Directory to save results
    output_dir = "sort_data"

    # Run analyses for all sorts and data types

    run_analysis(
        generator=generate_uniform_list,
        list_sizes=list_sizes,
        iterations=iterations,
        output_dir=output_dir
    )

    run_analysis(
        generator=generate_random_list,
        list_sizes=list_sizes,
        iterations=iterations,
        output_dir=output_dir
    )
    run_analysis(
        generator=generate_almost_sorted_list,
        list_sizes=list_sizes,
        iterations=iterations,
        output_dir=output_dir,
        disorder_percentage=0.2
    )
    run_analysis(
        generator=generate_almost_reverse_sorted_list,
        list_sizes=list_sizes,
        iterations=iterations,
        output_dir=output_dir,
        disorder_percentage=0.2
    )
 