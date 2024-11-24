#@author 2d Lt Christopher Rafnson

import random
import timeit
from heapq import heapify, heappop

# def merge_sort(arr):
#     temp = [0] * len(arr)
#     _merge_sort(arr, temp, 0, len(arr) - 1)

# def _merge_sort(arr, temp, left, right):
#     if left < right:
#         mid = (left + right) // 2
#         _merge_sort(arr, temp, left, mid)
#         _merge_sort(arr, temp, mid + 1, right)
#         merge(arr, temp, left, mid, right)

# def merge(arr, temp, left, mid, right):
#     for i in range(left, right + 1):
#         temp[i] = arr[i]
    
#     i, j, k = left, mid + 1, left
#     while i <= mid and j <= right:
#         if temp[i] <= temp[j]:
#             arr[k] = temp[i]
#             i += 1
#         else:
#             arr[k] = temp[j]
#             j += 1
#         k += 1
    
#     while i <= mid:
#         arr[k] = temp[i]
#         i += 1
#         k += 1

# """
# Merge() is given three indices on the main array to construct two sub arrays which will be merged together
# """
def merge(arr, temp, left_bound, mid_point, right_bound):
    for i in range(left_bound, right_bound + 1):
        temp[i] = arr[i]
    
    #These are our pointers to the left and right arrays, we will not be actually removing elements from them since it is too slow and wastes time
    left_index = left_bound
    right_index = mid_point + 1
    merge_index = left_bound #This is where we will begin to insert elements from the left and right arrays

    # Merge the two arrays, in this case both left and right have elements in them.
    while (left_index <= mid_point) and (right_index <= right_bound):
        if temp[left_index] <= temp[right_index]:
            arr[merge_index] = temp[left_index]
            left_index += 1 #iterate our left array index pointer, since we have "removed" an element from that array
        else:
            arr[merge_index] = temp[right_index]
            right_index += 1 #iterate our right array index pointer, since we have "removed" an element from that array
        merge_index += 1 #Move down the merge array

    # If there are remaining elements in left_array, add them
    while left_index <= mid_point:
        arr[merge_index] = temp[left_index]
        left_index += 1 #iterate our left array index pointer, since we have "removed" an element from that array
        merge_index += 1 #Move down the merge array


# """
# We don't want merge sort to use copious amounts of memory so during the course of its run, it will use the orignal 
# array that was passed into it. merge() and merge_sort() will then require bounds so it knows which parts of the array that 
# it is working on
# """
def _merge_sort(arr, temp, left_bound, right_bound):

    if left_bound < right_bound: #If left is bigger than right, we cannot sort the list properly
        mid_point = (left_bound + right_bound) // 2 #We choose the floor to create a clean int input
        _merge_sort(arr, temp, left_bound, mid_point) #Sort the left side
        _merge_sort(arr, temp, mid_point + 1, right_bound) #Sort the right side
        merge(arr, temp, left_bound, mid_point, right_bound) #Merge the two sides together

    #Note that there is no return on this function, it sorts the given array in-place.

def merge_sort(arr):
    temp = [0] * len(arr)
    _merge_sort(arr, temp, 0, len(arr)-1)


"""
Selection sort will also be sorted within the given array so as to conserve memory.
This is a pretty simple sort but rather naive.
"""
def selection_sort(arr):
    size = len(arr)

    for i in range(size):
        root_index = i
        j = root_index

        smallest_index = i        

        while j < size:
            if arr[j] < arr[smallest_index]:
                smallest_index = j
            j+=1 


        if smallest_index != root_index:
            arr[root_index], arr[smallest_index] = arr[smallest_index], arr[root_index]

    return(arr)

def selection_sort(arr):
    size = len(arr)
    for i in range(size):
        smallest_index = i  # Assume the current position is the smallest
        for j in range(i + 1, size):  # Search for the smallest in the remaining array
            if arr[j] < arr[smallest_index]:
                smallest_index = j
        # Swap only if needed
        if smallest_index != i:
            arr[i], arr[smallest_index] = arr[smallest_index], arr[i]
    return arr

def heap_sort(arr):

    size = len(arr)
    #Create a heap object, we can do this by just heapifying the arr given
    heapify(arr)

    #Now that the heap has been created and is a valid heap we create an array to store
    #the values as we remove them from the heap

    sorted_arr = []

    #Now we iterate through the heap and remove the minimum values, placing them in the sorted
    #array until the heap is empty

    for i in range(size):
        sorted_arr.append(heappop(arr))

    return sorted_arr

def quick_sort(arr):
    # Base case: arrays of length 0 or 1 are already sorted
    if len(arr) <= 1:
        return arr

    # Random pivot selection
    pivots = (arr[0], arr[len(arr)//2], arr[-1])
    pivot = sorted(pivots)[1]

    # Three-way partitioning
    left = []
    middle = []
    right = []

    for value in arr:
        if value < pivot:
            left.append(value)
        elif value > pivot:
            right.append(value)
        else:
            middle.append(value)

    # Recursively sort left and right partitions, and concatenate
    return quick_sort(left) + middle + quick_sort(right)

def bucket_sort(arr, max, min):

    length_array = len(arr) #This is also equal to the number of buckets we have

    #If the list is empty of only size 1, then it is already sorted
    if length_array == 0 or length_array == 1:
        return arr

    bucket_range = (max - min)/length_array

    #Create buckets
    buckets = [[] for i in range(length_array)]

        # Distribute the elements into buckets
    for num in arr:
        bucket_index = length_array - int((num - min) / bucket_range) - 1
        if bucket_index == length_array:  # Edge case for the max value
            bucket_index -= 1
        buckets[bucket_index].append(num)

    # Sort each bucket and concatenate the results
    sorted_array = []
    for bucket in buckets:
        sorted_array.extend(quick_sort(bucket))

    return sorted_array

if __name__ == '__main__':

    min, max = 0, 1000
    random.seed(2024)
    
    array = [random.randint(min,max) for i in range(1000)]
    # print(selection_sort(array))



    array1 = array.copy()
    # # array2 = array.copy()

    code_to_run_1 = "selection_sort(array1)"
    # # code_to_run_2 = "bucket_sort(array2, min, max)"

    # # array3 = [random.randint(-99,99) for i in range(10000)]
    # # code_to_run_3 = "merge_sort(array3, 0, len(array3)-1)"

    # # array4 = [random.randint(-99,99) for i in range(10000)]
    # # code_to_run_4 = "quick_sort(array4, 0, len(array4)-1)"

    time1 = timeit.timeit(code_to_run_1, globals=globals(), number=1)
    # time2 = timeit.timeit(code_to_run_2, globals=globals(), number=1)
    # time3 = timeit.timeit(code_to_run_3, globals=globals(), number=1)
    # time4 = timeit.timeit(code_to_run_4, globals=globals(), number=1)

    print(time1)
    # print(time2)
    # print(time3)
    # print(time4)



