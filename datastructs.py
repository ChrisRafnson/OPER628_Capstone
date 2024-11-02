import math
import random

class binary_heap:
    # data = [2, 6, 8, 13, 11, 13, 20, 14, 19, 27, 22, 16] 
    
    data = [] #Where the heap will be stored


    def __init__(self) -> None:
        pass

    def insert_key(self, key) -> None:
        # print(f'\nInserting Key with value {key}...')
        self.data.append(key)
        key_position = len(self.data) - 1


        if self.sift_up(key_position) == -1:
            # print("Error with sift-up procedure, restoring heap to former state...")
            return False
        else:
            # print("Key succesfully inserted!")
            pass

    def delete_min(self) -> None:

        if len(self.data) == 0:
            # print("\nCannot execute operation. The heap is empty.")
            pass
        else:
            # print(f'\nDeleting minimum valued key...')
            deleted_key = self.data[0]
            self.data[0] = self.data[-1] #We replace the first value with the value at the very end of the array (index: -1)
            self.data.pop(-1) #Remove the very last index from the list, which is what we put at the root node


            if len(self.data) == 0:
                # print(f"Final node in heap removed. The heap is now empty! The value of the last key was {deleted_key}")
                return deleted_key
            elif self.sift_down(0) == -1:
                # print("Error with sift-down procedure, restoring heap to former state...")
                return False
            else:
                # print(f"Minimum key successfully removed! Value of the key was {deleted_key}")
                return deleted_key


    def increase_key(self, position, new_value) -> None:

        if len(self.data) == 0 or position not in range(len(self.data)):
            # print("\nCannot execute operation. Position is outside the range of the heap.")
            pass
        else:
            # print(f'\nChanging value of key at position {position} to {new_value}...')
            self.data[position] = new_value

            """
            We use the sift down procedure when increasing a key, this is because we know that
            if it was a valid heap before the increase, there is no chance of our new key somehow
            being smaller than the nodes above it
            """
            if self.sift_down(position) == -1:
                # print("Error with sift-down procedure, restoring heap to former state...")
                return False
            else:
                # print("Key successfully increased in value!")
                pass


    def decrease_key(self, position, new_value) -> None:

        if len(self.data) == 0 or position not in range(len(self.data)):
            # print("\nCannot execute operation. Position is outside the range of the heap.")
            pass
        else:
            # print(f'\nChanging value of key at position {position} to {new_value}...')
            self.data[position] = new_value

            """
            We use the sift up procedure when decreasing a key, this is because we know that
            if it was a valid heap before the decrease, there is no chance of our new key somehow
            being bigger than the nodes below it
            """
            if self.sift_up(position) == -1:
                # print("Error with sift-up procedure, restoring heap to former state...")
                return False
            else:
                # print("Key successfully decreased in value")
                pass

    #Reminder that for this function we are passing the position of the lower node.
    def sift_up(self, position):
        child_index = position #This is the node we are up-sifting

        if len(self.data) == 0:
            # print("\nCannot execute operation. The heap is empty.")
            pass
        else:
            while(1):
                parent_index = self.get_parent(child_index)

                if child_index == 0: #This is the case where the node we are trying to sift up is the root node.
                    # print("No sift-up required, node is at the top of the heap.")
                    return 0
                elif (child_index in range(len(self.data))): #This verifies that the child is within the indices of the heap
                    if (parent_index in range(len(self.data))): #This also verifies that the parent is within range of the heap
                        if self.data[child_index] < self.data[parent_index]:
                            placeholder = self.data[parent_index]
                            self.data[parent_index] = self.data[child_index]
                            self.data[child_index] = placeholder

                            # print("Succesfully switched child and parent.")
                            child_index = parent_index #This is the new position of our node
                            #Since we don't return anything, the loop will continue to try to sift up the node
                        else:
                            # print("No sift-up required, node is not less than parent.")
                            return 0 #Return 0 if no sift-up was required 
                    else:
                        # print("Parent index not in the heap or does not exist.")
                        return -1 #Return -1 as error
                else:
                    # print("Position does not exist within this heap.")
                    return -1 #Return -1 as error

    def sift_down(self, position):
        parent_index = position #This is the node that we are DOWN-sifting

        if len(self.data) == 0:
            # print("\nCannot execute operation. The heap is empty.")
            pass
        else:
            while(1): #We use a loop to continue to down sift until we are done
                left_child_index = self.get_left_child(parent_index)
                right_child_index = self.get_right_child(parent_index)
                swap_index = None #This is the index of the child node that we will swap

                if (parent_index in range(len(self.data))): #Check that the parent is in the heap
                    
                    #This first case is if the node has no children, which means its a leaf node
                    if (left_child_index not in range(len(self.data))) and (right_child_index not in range(len(self.data))):
                        # print("No sift-down required, node does not have any children.")
                        return 0
                    elif (right_child_index not in range(len(self.data))): #This means that just the left child exists
                        swap_index = left_child_index #The node we will swap is the left child

                    else:
                        if self.data[left_child_index] <= self.data[right_child_index]: #If the left child is smaller or equal to the right child we will swap the left
                            swap_index = left_child_index
                        else: #In this case the right child is smaller than the left, so we will swap the right node
                            swap_index = right_child_index

                    if self.data[parent_index] > self.data[swap_index]: #In this case the parent node is greater than its smallest child so we swap it
                        #Next we create a placeholder variable and perform the switch
                        child_placeholder = self.data[swap_index]
                        self.data[swap_index] = self.data[parent_index]
                        self.data[parent_index] = child_placeholder

                        # print("Succesfully switched left child and its parent.")
                        parent_index = swap_index #This is the new position of our node
                        #Since we don't return anything, the loop will continue to try to sift down the node
                    else:
                        # print("No down sift required, parent is smaller than or equal to both of its children")
                        return 0

    def print_heap(self) -> None:

        if len(self.data) == 0:
            # print("[]\nThe heap is empty.")
            pass
        else:
            num_levels = math.ceil(math.log2(len(self.data)))

            # print("\nPrinting Heap...\n")

            if num_levels == 0: #In this case there is only one node in the heap.
                print(self.data[0: 1])



            for i in range(num_levels):
                starting_index = 2**i - 1
                ending_index = starting_index * 2

                if ending_index > len(self.data):
                    ending_index = len(self.data) - 1

                print(self.data[starting_index: ending_index + 1])


    #Given an index, return the index of the node's parent
    def get_parent(self, position) -> int:

        if position == 0: #In this case the node is the root, so it doesn't have a parent
            return 0
        elif position >= len(self.data): #In this case the position is outside the size of the array so it doesn't exist
            return -1
        else:
            return (position - 1) // 2 #This tells us where in the array our node's parent is located

    def get_left_child(self, position) -> int:
        left_child = (2*position) + 1

        '''
        Note that if the index of the left child is greater than or equal to the size of the list, 
        then it cannot appear in the heap meaning that it does not exist. In this case we return -1.
        This also catches the case where the position given to the function is not in the heap either.
        This is because position < (2*position) + 1 < size, so if the left child exists then so does the parent.
        Note that this does not check if the parent node exists, since that is outside the scope of this function
        '''

        if left_child >= len(self.data):
            return -1
        else:
            return left_child

    def get_right_child(self, position) -> int:
        right_child = (2*position) + 2

        '''
        Note that if the index of the left child is greater than or equal to the size of the list, 
        then it cannot appear in the heap meaning that it does not exist. In this case we return -1.
        This also catches the case where the position given to the function is not in the heap either.
        This is because position < (2*position) + 1 < size, so if the left child exists then so does the parent.
        Note that this does not check if the parent node exists, since that is outside the scope of this function
        
        '''
        if right_child >= len(self.data):
            return -1
        else:
            return right_child
        
    def isEmpty(self):

        if len(self.data)==0:
            return True
        else:
            return False

class Node:
    my_value = None
    next_node = None
    previous_node = None

    def __init__(self, value) -> None:
        self.my_value = value

class Doubly_Linked_List:
    size = 0
    head = None
    tail = None

    def __init__(self) -> None:
        return None

    def print_list(self):
        current_node = self.head
        if not self.is_empty():
            for i in range(self.size):
                print(current_node.my_value)
                current_node = current_node.next_node

    def is_empty(self):
        if (self.size == 0):
            return True
        else:
            return False
        
    def insert_front(self, value):
        new_node = Node(value=value)

        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next_node = self.head
            self.head.previous_node = new_node
            self.head = new_node

        self.size += 1


    def insert_end(self, value):
        new_node = Node(value=value)

        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next_node = new_node
            new_node.previous_node = self.tail
            self.tail = new_node

        self.size +=1

    def insert_after(self, position, value):
        new_node = Node(value)
        left_node = self.head

        if self.is_empty():
            self.insert_front(value)
        elif position < 0 or position > self.size:
            return False
        else:
            for i in range(position):
                left_node = left_node.next_node

            right_node = left_node.next_node
            new_node.previous_node = left_node
            new_node.next_node = right_node
            left_node.next_node = new_node
            right_node.previous_node = new_node

        self.size += 1

    #Returns -1 if object not found
    def find_value(self, value):
        current_node = self.head
        position = 0

        while current_node.next_node is not None:
            if current_node.my_value == value:
                return position
            else:
                current_node = current_node.next_node
                position += 1
        
        return -1
    
    def find_position(self, position):
        current_node = self.head
        
        if position < 0 or position > self.size:
            return False
        else:
            for i in range(position):
                current_node = current_node.next_node #iterate through the list

        return current_node

    def replace_value(self, position, value):
        current_node = self.head
        
        if position < 0 or position > self.size:
            return False
        else:
            for i in range(position):
                current_node = current_node.next_node #iterate through the list

        current_node.my_value = value

    def delete_first(self):
        value = self.head.my_value

        if self.size == 1:
            self.head = None
            self.tail = None
        else:   
            next_node = self.head.next_node
            next_node.previous_node = None
            self.head = next_node

        self.size -= 1
        return value
        

    def delete_last(self):
        previous_node = self.tail.previous_node
        previous_node.next_node = None
        self.tail = previous_node

        self.size -=1

    def delete_node(self, position):
        middle_node = self.head

        if position < 0 or position > self.size:
            return -1
        elif position == 0:
            self.delete_first()
        else:

            for i in range(position):
                middle_node = middle_node.next_node

            left_node = middle_node.previous_node
            right_node = middle_node.next_node

            left_node.next_node = right_node
            right_node.previous_node = left_node

        self.size -= 1