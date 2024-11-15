import math
import random

class binary_heap:
    def __init__(self):
        self.data = []  # Where the heap is stored

    def insert_key(self, key):
        self.data.append(key)
        self.sift_up(len(self.data) - 1)

    def delete_min(self):
        if self.is_empty():
            return None  # Return None if the heap is empty
        if len(self.data) == 1:
            return(self.data.pop())

        min_value = self.data[0]
        # Move the last element to the root and sift it down
        self.data[0] = self.data.pop()
        if not self.is_empty():
            self.sift_down(0)
        return min_value

    def increase_key(self, position, new_value):
        if 0 <= position < len(self.data):
            self.data[position] = new_value
            self.sift_down(position)

    def decrease_key(self, position, new_value):
        if 0 <= position < len(self.data):
            self.data[position] = new_value
            self.sift_up(position)

    def sift_up(self, position):
        while position > 0:
            parent_index = self.get_parent(position)
            if self.data[position] < self.data[parent_index]:
                # Swap with the parent
                self.data[position], self.data[parent_index] = self.data[parent_index], self.data[position]
                position = parent_index
            else:
                break

    def sift_down(self, position):
        size = len(self.data)
        while True:
            left = self.get_left_child(position)
            right = self.get_right_child(position)
            smallest = position

            if left is not None and self.data[left] < self.data[smallest]:
                smallest = left
            if right is not None and self.data[right] < self.data[smallest]:
                smallest = right

            if smallest != position:
                # Swap with the smallest child
                self.data[position], self.data[smallest] = self.data[smallest], self.data[position]
                position = smallest
            else:
                break

    def get_parent(self, position):
        if position == 0:
            return None
        return (position - 1) // 2

    def get_left_child(self, position):
        left = 2 * position + 1
        return left if left < len(self.data) else None

    def get_right_child(self, position):
        right = 2 * position + 2
        return right if right < len(self.data) else None

    def print_heap(self):
        if self.is_empty():
            print("Heap is empty")
        else:
            num_levels = math.ceil(math.log2(len(self.data) + 1))
            for level in range(num_levels):
                start_index = (1 << level) - 1
                end_index = min((1 << (level + 1)) - 1, len(self.data))
                print(self.data[start_index:end_index])

    def is_empty(self):
        return len(self.data) == 0


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

