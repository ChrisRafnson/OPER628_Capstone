import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def read_graph_data(algorithm):

    df_runtime = pd.read_csv(f"graph_data\{algorithm}_runtime.csv")
    df_memory = pd.read_csv(f"graph_data\{algorithm}_memory.csv")

    return df_runtime, df_memory

def calculate_runtime_mean(df, density):
    return df.groupby('Input Size')[f'{density}'].mean()

def calculate_memory_mean(df, density):
    df[f'{density}'] = df[f'{density}'] / (1024 ** 2)
    return df.groupby('Input Size')[f'{density}'].mean()

def generate_single_plot_runtime_all_densities(algorithm, df_runtime):
    plt.figure()


    plt.plot(calculate_runtime_mean(df_runtime, 0.25), label="Density 0.25", linestyle = '-', color = 'k')
    plt.plot(calculate_runtime_mean(df_runtime, 0.5), label="Density 0.50", linestyle = '--', color = 'b')
    plt.plot(calculate_runtime_mean(df_runtime, 0.75), label="Density 0.75", linestyle = ':', color = 'r')
    plt.plot(calculate_runtime_mean(df_runtime, 1.0), label="Density 1.0", linestyle = '-.', color = 'y')

    plt.title(f"Search Performance ({algorithm})")
    plt.xlabel('Graph Size (Nodes)')
    plt.ylabel('Time to Finish (s)')
    plt.legend()
    plt.grid(True)
    # plt.show()
    plt.savefig(f"plots\graph_algorithms\{algorithm}\{algorithm}_single_plot_runtime")

def generate_single_plot_memory_all_densities(algorithm, df_memory):
    plt.figure()


    plt.plot(calculate_memory_mean(df_memory, 0.25), label="Density 0.25", linestyle = '-', color = 'k')
    plt.plot(calculate_memory_mean(df_memory, 0.5), label="Density 0.50", linestyle = '--', color = 'b')
    plt.plot(calculate_memory_mean(df_memory, 0.75), label="Density 0.75", linestyle = ':', color = 'r')
    plt.plot(calculate_memory_mean(df_memory, 1.0), label="Density 1.0", linestyle = '-.', color = 'y')

    plt.title(f"Search Performance ({algorithm})")
    plt.xlabel('Graph Size (Nodes)')
    plt.ylabel('Peak Memory Used (Megabytes)')
    plt.legend()
    plt.grid(True)
    # plt.show()
    plt.savefig(f"plots\graph_algorithms\{algorithm}\{algorithm}_single_plot_memory_usage")

def generate_times_vs_theoretical(algorithm, df, density):
    plt.figure()


    #Initialize essential variables
    df = calculate_runtime_mean(df, density)
    df = df.reset_index()
    theoretical_df = pd.DataFrame()

    theoretical_df['Input Size'] = [i for i in range(0, df["Input Size"].iloc[-1] + 5, 5)]


    #This is where we calculate the values for our theoretical curves
    time = df[f"{density}"].iloc[(len(df)//2)]
    n = df["Input Size"].iloc[(len(df)//2)]
    m = (df["Input Size"].iloc[(len(df)//2)] ** 2) * density

    n_theoretical = theoretical_df["Input Size"]
    m_theoretical = (theoretical_df["Input Size"] ** 2) * density

    # Calculates O((n+m) log n) for heap Dijkstras
    n_plus_m_log_n = time / ((n + m) * np.log2(n))
    theoretical_df["O((n+m) log n)"] = n_plus_m_log_n * ((n_theoretical + m_theoretical) * np.log2(n_theoretical))

    # Calculates O(mn) for naive kruskals and prims
    n_plus_m_log_n = time / (n * m)
    theoretical_df["O(mn)"] = n_plus_m_log_n * (n_theoretical * m_theoretical)

    # Calculates O(m log n) for improved prims
    m_log_n = time / (m * np.log2(n))
    theoretical_df["O(m log n)"] = m_log_n * (m_theoretical * np.log2(n_theoretical))

    # Calculates O(m + n log n) for improved kruskals
    m_log_n = time / (m + (n * np.log2(n)))
    theoretical_df["O(m + n log n)"] = m_log_n * (m_theoretical + (n * np.log2(n_theoretical)))

    #n log n theoretical time
    linearithmic = time / (n * np.log2(n))
    theoretical_df["Linearithmic"] = linearithmic * (n_theoretical * np.log2(n_theoretical))

    # N
    linear = time / n
    theoretical_df["Linear"] = linear * n_theoretical

    # N^2
    squared = time / (n ** 2)
    theoretical_df["Squared"] = squared * (n_theoretical ** 2)

    # N^3
    cubed = time / (n ** 3)
    theoretical_df["Cubed"] = cubed * (n_theoretical ** 3)

    # N^4
    cubed = time / (n ** 4)
    theoretical_df["Quartic"] = cubed * (n_theoretical ** 4)
  
    #Plot different things based on algorithm

    if algorithm == 'naive_dijkstras':
        plt.plot(theoretical_df["Input Size"], theoretical_df["Linearithmic"], '-', label=r"Theoretical $O(n \log n)$", color = 'b')
        plt.plot(theoretical_df["Input Size"], theoretical_df["Squared"], '-', label=r"Theoretical $O(n^2)$", color = 'r')
        plt.plot(theoretical_df["Input Size"], theoretical_df["Cubed"], '-', label=r"Theoretical $O(n^3)$", color = 'y')

    elif algorithm == 'heap_dijkstras':
        plt.plot(theoretical_df["Input Size"], theoretical_df["O(m log n)"], '-', label=r"Theoretical $O(m log n)$", color = 'b')
        plt.plot(theoretical_df["Input Size"], theoretical_df["Squared"], '-', label=r"Theoretical $O(n^2)$", color = 'r')
        plt.plot(theoretical_df["Input Size"], theoretical_df["Cubed"], '-', label=r"Theoretical $O(n^3)$", color = 'y')

    elif algorithm == 'naive_kruskals':
        plt.plot(theoretical_df["Input Size"], theoretical_df["O(mn)"], '-', label=r"Theoretical $O(mn)$", color = 'b')
        plt.plot(theoretical_df["Input Size"], theoretical_df["Squared"], '-', label=r"Theoretical $O(n^2)$", color = 'r')
        plt.plot(theoretical_df["Input Size"], theoretical_df["Cubed"], '-', label=r"Theoretical $O(n^3)$", color = 'y')
    
    elif algorithm == 'improved_kruskals':
        plt.plot(theoretical_df["Input Size"], theoretical_df["O(m + n log n)"], '-', label=r"Theoretical $O(m + n log n)$", color = 'b')
        plt.plot(theoretical_df["Input Size"], theoretical_df["Squared"], '-', label=r"Theoretical $O(n^2)$", color = 'r')
        plt.plot(theoretical_df["Input Size"], theoretical_df["Cubed"], '-', label=r"Theoretical $O(n^3)$", color = 'y')
    
    elif algorithm == 'naive_prims':
        plt.plot(theoretical_df["Input Size"], theoretical_df["O(mn)"], '-', label=r"Theoretical $O(mn)$", color = 'b')
        plt.plot(theoretical_df["Input Size"], theoretical_df["Squared"], '-', label=r"Theoretical $O(n^2)$", color = 'r')
        plt.plot(theoretical_df["Input Size"], theoretical_df["Cubed"], '-', label=r"Theoretical $O(n^3)$", color = 'y')
    
    else:
        plt.plot(theoretical_df["Input Size"], theoretical_df["O(m log n)"], '-', label=r"Theoretical $O(m log n)$", color = 'b')
        plt.plot(theoretical_df["Input Size"], theoretical_df["Squared"], '-', label=r"Theoretical $O(n^2)$", color = 'r')
        plt.plot(theoretical_df["Input Size"], theoretical_df["Cubed"], '-', label=r"Theoretical $O(n^3)$", color = 'y')


    plt.title(f"Search Performance ({algorithm})")
    plt.plot(df["Input Size"], df[f"{density}"], 'o--', label="Measured Times", color = 'k')
    plt.xlabel("Input Size (nodes)")
    plt.ylabel("Time To Complete (seconds)")
    plt.ylim(0, df[f"{density}"].iloc[-1] * 1.25)
    plt.legend()
    plt.grid(True)

    # plt.show()
    plt.savefig(f"plots\graph_algorithms\{algorithm}\{algorithm}_theoretical_runtime")   

def generate_graph_comparison(algorithms, density, alg_type):

    line_styles = [('o', '-', 'k'), ('o', '-', 'b'), ('o', '-', 'r'), ('o', '-', 'y'), ('o', '-', 'c'), ('o', '-', 'm')]

    plt.figure()
    max_y_val = 0

    for algorithm, line_style in zip(algorithms, line_styles):

        # Read the runtime data for the algorithm
        df_runtime, _ = read_graph_data(algorithm)
        grouped = calculate_runtime_mean(df_runtime, density)

        # Update max_y_val to dynamically set the y-axis limit
        max_y_val = max(max_y_val, grouped.max())

        # Algorithm-specific legend
        if algorithm == "naive_dijkstras":
            legend = "Naive Dijkstra's"
        elif algorithm == "heap_dijkstras":
            legend = "Heap Dijkstra's"
        elif algorithm == "naive_kruskals":
            legend = "Naive Kruskal's"
        elif algorithm == "improved_kruskals":
            legend = "Improved Kruskal's"
        elif algorithm == "naive_prims":
            legend = "Naive Prim's"
        else:
            legend = "Heap Prim's"

        # Plot the runtime data for the algorithm
        plt.plot(grouped, label=legend, marker=line_style[0], linestyle=line_style[1], color=line_style[2])

    # Configure plot appearance
    plt.xlabel('Graph Size (Nodes)')
    plt.ylabel('Time to Finish (s)')
    plt.title(f"Comparison of Graph Algorithms (Density {density})")
    plt.ylim(0, max_y_val * 1.1)
    plt.legend()
    plt.grid(True)

    # Save the plot
    plt.savefig(f"plots/graph_algorithms/runtime_comparisons/comparison_{alg_type}_density_{density}_.png")
    plt.show()

algorithms = [
    "naive_dijkstras",
    "heap_dijkstras",
    "naive_kruskals",
    "improved_kruskals",
    "naive_prims",
    "heap_prims"
]

shortest_path_algorithms = [
    "naive_dijkstras",
    "heap_dijkstras"
]

mcst_algorithms = [
    "naive_kruskals",
    "improved_kruskals",
    "naive_prims",
    "heap_prims"
]

prims_algorithms = [
    "naive_prims",
    "heap_prims"
]

kruskals_algorithms = [
    "naive_kruskals",
    "improved_kruskals"
]
densities = [0.25, 0.5, 0.75, 1.0]

if __name__ == '__main__':

    for algorithm in algorithms:
        df_runtime, df_memory = read_graph_data(algorithm)

        generate_single_plot_runtime_all_densities(algorithm, df_runtime)
        # generate_times_vs_theoretical(algorithm, df_runtime, 1.0)
        generate_single_plot_memory_all_densities(algorithm, df_memory)


    



    print("Done")