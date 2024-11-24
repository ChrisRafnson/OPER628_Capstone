import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


sorts = ["heap_sort", "merge_sort", "bucket_sort", "selection_sort", "quick_sort"]



def read_runtime_data(sort):

    df_random = pd.read_csv(f"sort_data\{sort}_generate_random_list.csv")
    df_almost = pd.read_csv(f"sort_data\{sort}_generate_almost_sorted_list.csv")
    df_reverse = pd.read_csv(f"sort_data\{sort}_generate_almost_reverse_sorted_list.csv")
    df_uniform = pd.read_csv(f"sort_data\{sort}_generate_uniform_list.csv")

    return df_random, df_almost, df_reverse, df_uniform

def calculate_runtime_mean(df):
    return df.groupby('List Size')['Time Taken (s)'].mean()

def calculate_memory_mean(df):
    df['Peak Memory Usage (MB)'] = df['Peak Memory Usage (bytes)'] / (1024 **2)
    return df.groupby('List Size')['Peak Memory Usage (MB)'].mean()

def generate_single_plot_runtime(sort, df_random, df_almost, df_reverse, df_uniform):

    plt.figure()
    plt.plot(calculate_runtime_mean(df_random), label="Random Inputs", linestyle = '-', color = 'k')
    plt.plot(calculate_runtime_mean(df_almost), label="Almost Sorted", linestyle = '--', color = 'b')
    plt.plot(calculate_runtime_mean(df_reverse), label="Almost Reverse Sorted", linestyle = ':', color = 'r')
    plt.plot(calculate_runtime_mean(df_uniform), label="Uniform Array", linestyle = '-.', color = 'y')

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
    plt.ylabel('Time to Finish Sort (s)')
    plt.legend()
    plt.grid(True)
    # plt.show()
    # plt.savefig(f"plots\sort_algorithms\{sort}\{sort}_single_plot_runtime")

def generate_times_vs_theoretical(sort, df):
    df = calculate_runtime_mean(df)
    df = df.reset_index()
    theoretical_df = pd.DataFrame()

    theoretical_df['List Size'] = [i for i in range(0, df["List Size"].iloc[-1] + 5, 5)]

    # Compute theoretical times and add as a new column
    linearithmic_normalizer = df["Time Taken (s)"].iloc[1] / (df["List Size"].iloc[1] * np.log2(df["List Size"].iloc[1]))
    theoretical_df["Linearithmic Time (s)"] = linearithmic_normalizer * theoretical_df['List Size'] * np.log2(theoretical_df['List Size'])

    # Compute theoretical times and add as a new column
    linear_normalizer = df["Time Taken (s)"].iloc[1] / (df["List Size"].iloc[1])
    theoretical_df["Linear Time (s)"] = linear_normalizer * theoretical_df['List Size']

    # Compute theoretical times and add as a new column
    poloynomial_normalizer = df["Time Taken (s)"].iloc[1] / (df["List Size"].iloc[1] ** 2)
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
    plt.xscale('log')
    
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
    # plt.savefig(f"plots\sort_algorithms\{sort}\{sort}_sinlge_plot_memory")




if __name__ == '__main__':

    # sort= "heap_sort"
    for sort in sorts:
        a, b, c, d = read_runtime_data(sort)
        generate_single_plot_runtime(sort, a, b, c, d)
        generate_single_plot_memory(sort, a, b, c, d)
        generate_times_vs_theoretical(sort, a)


    print("Done")