#@author 2d Lt Christopher Rafnson

import math
import random
import datastructs as ds
import timeit

# """
# Merge() is given three indices on the main array to construct two sub arrays which will be merged together
# """
def merge(arr, left_bound, mid_point, right_bound):
    # Create copies of the subarrays
    left_array = arr[left_bound:mid_point + 1] 
    right_array = arr[mid_point + 1:right_bound + 1]
    
    left_index = right_index = 0 #These are our pointers to the left and right arrays, we will not be actually removing elements from them since it is too slow and wastes time
    merge_index = left_bound #This is where we will begin to insert elements from the left and right arrays

    # Merge the two arrays, in this case both left and right have elements in them.
    while left_index < len(left_array) and right_index < len(right_array):
        if left_array[left_index] <= right_array[right_index]:
            arr[merge_index] = left_array[left_index]
            left_index += 1 #iterate our left array index pointer, since we have "removed" an element from that array
        else:
            arr[merge_index] = right_array[right_index]
            right_index += 1 #iterate our right array index pointer, since we have "removed" an element from that array
        merge_index += 1 #Move down the merge array

    # If there are remaining elements in left_array, add them
    while left_index < len(left_array):
        arr[merge_index] = left_array[left_index]
        left_index += 1 #iterate our left array index pointer, since we have "removed" an element from that array
        merge_index += 1 #Move down the merge array

    # If there are remaining elements in right_array, add them
    while right_index < len(right_array):
        arr[merge_index] = right_array[right_index]
        right_index += 1 #iterate our right array index pointer, since we have "removed" an element from that array
        merge_index += 1 #Move down the merge array

# """
# We don't want merge sort to use copious amounts of memory so during the course of its run, it will use the orignal 
# array that was passed into it. merge() and merge_sort() will then require bounds so it knows which parts of the array that 
# it is working on
# """
def merge_sort(arr, left_bound, right_bound):
    if left_bound < right_bound: #If left is bigger than right, we cannot sort the list properly
        mid_point = (left_bound + right_bound) // 2 #We choose the floor to create a clean int input
        merge_sort(arr, left_bound, mid_point) #Sort the left side
        merge_sort(arr, mid_point + 1, right_bound) #Sort the right side
        merge(arr, left_bound, mid_point, right_bound) #Merge the two sides together

    #Note that there is no return on this function, it sorts the given array in-place.


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

def heap_sort(arr):

    #Create a heap object
    my_heap = ds.binary_heap()

    #Insert all array values into the heap, this will iteratively heapify the heap
    for element in arr:
        my_heap.insert_key(element)

    #Now that the heap has been created and is a valid heap we create an array to store
    #the values as we remove them from the heap

    sorted_arr = []

    #Now we iterate through the heap and remove the minimum values, placing them in the sorted
    #array until the heap is empty

    while not my_heap.is_empty():
        sorted_arr.append(my_heap.delete_min())


    return(sorted_arr)

def quick_sort(arr, low, high):
    if low < high:
        # Pivot selection using first, middle, and last elements
        middle = (low + high) // 2
        pivots = [arr[low], arr[middle], arr[high]]
        pivots.sort()
        pivot = pivots[1]  # Select the median as the pivot

        # Array is sorted into higher and lower while still being in place
        left, right = low, high
        while left <= right:
            while arr[left] < pivot:
                left += 1
            while arr[right] > pivot:
                right -= 1

            if left <= right:
                arr[left], arr[right] = arr[right], arr[left]
                left += 1
                right -= 1

        # Recursive calls for left and right partitions
        quick_sort(arr, low, right)
        quick_sort(arr, left, high)

def bucket_sort(arr):
    buckets = []

    # Create buckets
    for i in range(10):
        buckets.append(ds.Doubly_Linked_List())

    # Put elements into the correct buckets
    for element in arr:
        index = element // 10  # Determine bucket index
        buckets[index].insert_end(element)

    # Sort each bucket using insertion sort
    for bucket in buckets:
        for i in range(1, bucket.size):
            key = bucket.find_position(i).my_value
            j = i - 1

            # Shift elements in the bucket that are greater than the key
            while j >= 0 and bucket.find_position(j).my_value > key:
                bucket.replace_value(position=j + 1, value=bucket.find_position(j).my_value)
                j -= 1

            # Insert the key at its correct position
            bucket.replace_value(position=j + 1, value=key)

    # Concatenate buckets into the sorted array
    sorted_array = []
    for bucket in buckets:
        while not bucket.is_empty():
            sorted_array.append(bucket.delete_first())

    return sorted_array



if __name__ == '__main__':
    
    array = [random.randint(0,99) for i in range(20)]
    print(selection_sort(array))



    # array1 = [random.randint(-99,99) for i in range(10000)]
    # code_to_run_1 = "selection_sort(array1)"

    # array2 = [random.randint(0,99) for i in range(10000)]
    # code_to_run_2 = "bucket_sort(array2)"

    # array3 = [random.randint(-99,99) for i in range(10000)]
    # code_to_run_3 = "merge_sort(array3, 0, len(array3)-1)"

    # array4 = [random.randint(-99,99) for i in range(10000)]
    # code_to_run_4 = "quick_sort(array4, 0, len(array4)-1)"

    # time1 = timeit.timeit(code_to_run_1, globals=globals(), number=1)
    # time2 = timeit.timeit(code_to_run_2, globals=globals(), number=1)
    # time3 = timeit.timeit(code_to_run_3, globals=globals(), number=1)
    # time4 = timeit.timeit(code_to_run_4, globals=globals(), number=1)

    # print(time1)
    # print(time2)
    # print(time3)
    # print(time4)



