import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


algorithms = [
    "naive_dijkstras",
    "heap_dijkstras",
    "naive_kruskals",
    "improved_kruskals",
    "naive_prims",
    "heap_prims"
]
densities = [0.25, 0.5, 0.75, 1.0]



def read_graph_data(algorithm):

    df_runtime = pd.read_csv(f"graph_data\{algorithm}_runtime.csv")
    df_memory = pd.read_csv(f"graph_data\{algorithm}_memory.csv")

    return df_runtime, df_memory

def calculate_runtime_mean(df, density):
    return df.groupby('Input Size')[f'{density}'].mean()

def calculate_memory_mean(df, density):
    df[f'{density}'] = df[f'{density}'] / (1024 **2)
    return df.groupby('Input Size')[f'{density}'].mean()

def generate_single_plot_runtime_all_densities(algorithm, df_runtime):

    # plt.figure()
    plt.plot(calculate_runtime_mean(df_runtime, 0.25), label="Density 0.25", linestyle = '-', color = 'k')
    plt.plot(calculate_runtime_mean(df_runtime, 0.5), label="Density 0.50", linestyle = '--', color = 'b')
    plt.plot(calculate_runtime_mean(df_runtime, 0.75), label="Density 0.75", linestyle = ':', color = 'r')
    plt.plot(calculate_runtime_mean(df_runtime, 1.0), label="Density 1.0", linestyle = '-.', color = 'y')

    plt.title(f"Search Performance ({algorithm})")
    plt.xlabel('Graph Size (Nodes)')
    plt.ylabel('Time to Finish (s)')
    plt.legend()
    plt.grid(True)
    plt.show()
    plt.savefig(f"plots\graph_algorithms\{algorithm}\{algorithm}_single_plot_runtime")

def generate_times_vs_theoretical(sort, df):
    df = calculate_runtime_mean(df)
    df = df.reset_index()
    theoretical_df = pd.DataFrame()

    theoretical_df['List Size'] = [i for i in range(0, df["List Size"].iloc[-1] + 5, 5)]

    
    # Compute theoretical times and add as a new column
    linearithmic_normalizer = df["Time Taken (s)"].iloc[(len(df)//2)] / (df["List Size"].iloc[(len(df)//2)] * np.log2(df["List Size"].iloc[(len(df)//2)]))
    theoretical_df["Linearithmic Time (s)"] = linearithmic_normalizer * theoretical_df['List Size'] * np.log2(theoretical_df['List Size'])

    # Compute theoretical times and add as a new column
    linear_normalizer = df["Time Taken (s)"].iloc[(len(df)//2)] / (df["List Size"].iloc[(len(df)//2)])
    theoretical_df["Linear Time (s)"] = linear_normalizer * theoretical_df['List Size']

    average_case_normalizer = df["Time Taken (s)"].iloc[(len(df) // 2)] / (2 * df["List Size"].iloc[(len(df) // 2)])
    theoretical_df["Average Case Time (s)"] = average_case_normalizer * (2 * theoretical_df["List Size"])

    # Compute theoretical times and add as a new column
    poloynomial_normalizer = df["Time Taken (s)"].iloc[(len(df)//2)] / (df["List Size"].iloc[(len(df)//2)] ** 2)
    theoretical_df["Polynomial Time (s)"] = poloynomial_normalizer * (theoretical_df["List Size"] ** 2)

    # Plot using pandas

    plt.figure()
    plt.plot(df["List Size"], df["Time Taken (s)"], 'o--', label="Measured Times", color = 'k')
    plt.plot(theoretical_df["List Size"], theoretical_df["Linearithmic Time (s)"], '-', label=r"Theoretical $O(n \log n)$", color = 'b')
    plt.plot(theoretical_df["List Size"], theoretical_df["Linear Time (s)"], '-', label=r"Theoretical $O(n)$", color = 'y')
    plt.plot(theoretical_df["List Size"], theoretical_df["Polynomial Time (s)"], '-', label=r"Theoretical $O(n^2)$", color = 'r')

        
    if sort == 'heap_sort':
        plt.title("Heap Sort Performance: Measured vs Theoretical")
    elif sort == 'bucket_sort':
        plt.title("Bucket Sort Performance: Measured vs Theoretical")
    elif sort == 'quick_sort':
        plt.title("Quick Sort Performance: Measured vs Theoretical")
    elif sort == 'merge_sort':
        plt.title("Merge Sort Performance: Measured vs Theoretical")
    else:
        plt.title("Selection Sort Performance: Measured vs Theoretical")


    plt.xlabel("List Size")
    plt.ylabel("Time (seconds)")
    plt.ylim(0, df["Time Taken (s)"].iloc[-1] * 1.25)
    plt.legend()
    plt.grid(True)
    plt.show()
    # plt.savefig(f"plots\sort_algorithms\{sort}\{sort}_theoretical_runtime")

def generate_single_plot_memory(sort, df_random, df_almost, df_reverse, df_uniform):

    plt.figure()
    plt.plot(calculate_memory_mean(df_random), label="Random Inputs", linestyle = '-', color = 'k')
    plt.plot(calculate_memory_mean(df_almost), label="Almost Sorted", linestyle = '--', color = 'r')
    plt.plot(calculate_memory_mean(df_reverse), label="Almost Reverse Sorted", linestyle = ':', color = 'b')
    plt.plot(calculate_memory_mean(df_uniform), label="Uniform Array", linestyle = '-.', color = 'y')

    if sort == 'heap_sort':
        plt.title(f'Heap Sort Performance')
    elif sort == 'bucket_sort':
        plt.title(f'Bucket Sort Performance')
    elif sort == 'quick_sort':
        plt.title(f'Quick Sort Performance')
    elif sort == 'merge_sort':
        plt.title(f'Merge Sort Performance')
    else:
        plt.title(f'Selection Sort Performance')

    plt.xlabel('Input Size (n)')
    plt.ylabel('Peak Memory Usage (Megabytes)')
    plt.legend()
    plt.grid(True)
    # plt.show()
    plt.savefig(f"plots\sort_algorithms\{sort}\{sort}_single_plot_memory")

def generate_sort_comparison(sorts, data_type):
    
    line_styles = [('o', '-', 'k'), ('o', '-', 'b'), ('o', '-', 'r'), ('o', '-', 'y'), ('o', '-', 'c')]

    plt.figure()
    max_y_val = 0
    for sort, line_style in zip(sorts, line_styles):

        if sort == 'heap_sort':
            legend = "Heap Sort"
        elif sort == 'bucket_sort':
            legend = "Bucket Sort"
        elif sort == 'quick_sort':
            legend = "Quick Sort"
        elif sort == 'merge_sort':
            legend = "Merge Sort"
        else:
            legend = "Selection Sort"

        df = pd.read_csv(f"sort_data\{sort}_generate_{data_type}_list.csv")
        grouped = df.groupby('List Size')['Time Taken (s)'].mean()

        # if grouped.iloc[-1] > max_y_val:
        #     max_y_val = grouped.iloc[-1]

        if sort == 'merge_sort':
            max_y_val = grouped.iloc[-1]

        plt.plot(grouped, label=legend, marker = line_style[0], linestyle = line_style[1], color = line_style[2])

    plt.xlabel('Input Size (n)')
    plt.ylabel('Time to Finish Sort (s)')
    plt.title(f"Comparison of Sorting Algorithms ({data_type})")
    plt.ylim(0, max_y_val)
    plt.legend()
    plt.grid(True)
    # plt.show()

    plt.savefig(f"plots\sort_algorithms\comparison_{data_type}")




if __name__ == '__main__':

    for algorithm in algorithms:
        df_runtime, df_memory = read_graph_data(algorithm)

        generate_single_plot_runtime_all_densities(algorithm, df_runtime)

    print("Done")