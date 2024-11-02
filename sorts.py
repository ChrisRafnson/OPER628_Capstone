#@author 2d Lt Christopher Rafnson

import math
import random
import datastructs as ds
import timeit

"""
Merge() is given three indices on the main array to construct two sub arrays which will be merged together
"""
def merge(arr, left_bound, mid_point, right_bound):
    left_array = []
    right_array = []

    # This just puts our left and right arrays into separate arrays so we can merge them
    for i in range(left_bound, mid_point+1):
        left_array.append(arr[i])

    for j in range(mid_point+1, right_bound+1):
        right_array.append(arr[j])

    # This is where the actual merging is done
    for i in range(left_bound, right_bound+1):

        if len(left_array) == 0  and len(right_array) == 0:
            return
        elif len(left_array) == 0:
            arr[i] = right_array.pop(0)
        elif len(right_array) == 0:
            arr[i] = left_array.pop(0)
        elif (left_array[0] <= right_array[0]):
            arr[i] = left_array.pop(0)
        else:
            arr[i] = right_array.pop(0)


"""
We don't want merge sort to use copious amounts of memory so during the course of its run, it will use the orignal 
array that was passed into it. merge() and merge_sort() will then require bounds so it knows which parts of the array that 
it is working on
"""
def merge_sort(arr, left_bound, right_bound):
    
    if right_bound < left_bound: #Our right should never be less than our left bound
        return False
    
    elif left_bound < right_bound: #This condition implies that our list is greater than size 1, so we need to operate on it
        mid_point = (left_bound + right_bound) // 2 #This is the mid point of our array
        merge_sort(arr, left_bound, mid_point) #Recursively sort the left side
        merge_sort(arr, mid_point + 1, right_bound) #Recursively sort the right side
        merge(arr, left_bound, mid_point, right_bound) #Merge them together, by giving merge() the left, mid, and right bounds it can reconstruct the two sub arrays from the main array
        return True

    else: #This means we have an array where the size is 1, i.e length 1. No sorting required.
        return True



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


        if smallest_index is not root_index:
            placeholder = arr[root_index]
            arr[root_index] = arr[smallest_index]
            arr[smallest_index] = placeholder

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

    while not my_heap.isEmpty():
        sorted_arr.append(my_heap.delete_min())


    return(sorted_arr)

def quick_sort(arr):

    if len(arr) <= 1:
        return arr

    length = len(arr)
    last_index = length -1
    middle = length//2
    
    my_dict = {
        0 : arr[0],
        last_index : arr[last_index],
        middle : arr[middle]
    }

    sorted_items = sorted(my_dict.items(), key=lambda item: item[1])
    pivot = sorted_items[1][0]  # This extracts only the key with the median value

    left_array = []
    right_array = []

    i = 0
    while i < pivot:
        if arr[i] < arr[pivot]:
            left_array.append(arr[i])
        else:
            right_array.append(arr[i])

        i+=1

    i = pivot+1
    while i < length:
        if arr[i] < arr[pivot]:
            left_array.append(arr[i])
        else:
            right_array.append(arr[i])

        i+=1
    
    left = quick_sort(left_array)
    middle = [arr[pivot]]
    right = quick_sort(right_array)

    return left+middle+right

def bucket_sort(arr):
    pass


if __name__ == '__main__':
    

    array = [random.randint(0,99) for i in range(15)]
    code_to_run = 'merge_sort(array, 0, len(array) - 1)'

    time = timeit.timeit(code_to_run, globals= globals(), number=1000)
    print(time)
