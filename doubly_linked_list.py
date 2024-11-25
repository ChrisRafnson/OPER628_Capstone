#**************************************************************************
class Node:
    def __init__(self, value):
        self.key = value
        self.right_pointer = None
        self.left_pointer = None


#**************************************************************************
class Doubly_Linked_List:
    # create an empty DLL
    def __init__(self):
        self.head = None
        self.tail = None

    def merge(self, other_list):
        if not self.head:  # If the current list is empty
            self.head = other_list.head
            self.tail = other_list.tail
        else:  # If the current list is not empty
            self.tail.right_pointer = other_list.head  # Connect the tail of the current list to the head of the other list
            if other_list.head:  # If the other list is not empty
                other_list.head.left_pointer = self.tail  # Update the prev pointer of the head of the other list
            self.tail = other_list.tail  # Update the tail of the current list
            self.size = self.size + other_list.size

     
    # Returns True if the DLL is empty
    def is_empty(self):
        return self.head is None
    
    
    # Inserts a new node at the front of the DLL
    def insert_front(self, value):
        new_node = Node(value)
        
        # if the DLL is empty, then update head/tail of DLL to point to new element
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        # otherwise update head of DLL to point to new element, update right pointer
        # of new element to point to previous first element, and update left pointer
        # of previous first element to point to new element
        else:
            new_node.right_pointer = self.head
            self.head.left_pointer = new_node
            self.head = new_node
       
            
    # Inserts a new node at the end of the DLL
    def insert_end(self, value):
        new_node = Node(value)
        
        # If the DLL is empty, then update head/tail of DLL to point to new element
        if self.is_empty():
            self.head = new_node
            self.tail = new_node  
        # otherwise update tail of DLL to point to new element, update right pointer
        # of preiovus tail element to point to new element, update left pointer
        # of new element so to point to previous tail element
        else:
            new_node.left_pointer = self.tail
            self.tail.right_pointer = new_node
            self.tail = new_node
    
    
    # Inserts a new node with value = 'value' at position = 'position'
    def insert_after(self, position, value):
        # Find the node at the given position
        current = self.head
        loc = 0
        
        # Traverse to the node at the desired position
        while current is not None and loc < position:
            current = current.right_pointer
            loc += 1
        
        # If the position is out of bounds, raise an error
        if current is None:
            print("Position out of bounds.")
            return
        
        # Create new node
        new_node = Node(value)
        
        # The desired end state looks like:
        # current node (matches position) -> new node -> next node
        # Set the left pointer of the new node to point to the current node
        new_node.left_pointer = current
        
        # Get the next node (the one that comes after the current node)
        next_node = current.right_pointer
        
        # If the current node is the tail, update the tail to the new node
        if next_node is None:
            self.tail = new_node
        else:
            # Otherwise, update the next node's left pointer to the new node
            next_node.left_pointer = new_node
        
        # Update the current node's right pointer to point to the new node
        current.right_pointer = new_node
        
        # Set the new node's right pointer to the next node
        new_node.right_pointer = next_node
       
        
    # delete the first element in the list, and return its value
    def delete_first(self):
        if self.is_empty():
            return None
        else:
            val = self.head.key
            # if there is only one element in the DLL, then DLL is now empty
            if self.head == self.tail:
                self.head = None
                self.tail = None
            # otherwise, update head to point to right pointer of element that is 
            # removed, and update left pointer of new first element
            else:
                self.head = self.head.right_pointer
                self.head.left_pointer = None
            return val
    
    
    # Delete the last element in the list, and return its value
    def delete_last(self):
        if self.is_empty():
            return None
        else:
            val = self.tail.key
            # if there is only one element in the DLL, then DLL is now epty
            if self.head == self.tail:
                self.head = None
                self.tail = None
            # otherwise, update tail of DLL to point to left pointer of element 
            # that is removed, and update right pointer of new last element
            else:
                self.tail = self.tail.left_pointer
                self.tail.right_pointer = None
            return val
    
        
    # Delete the an element in the list based on it's position.   
    def delete_node(self, position):
        # If the position provided (say from find_value) is False you should stop.
        if position is False:
            print(position, "is an invalid position skipping delete_node")
            return None
        
        # If the list is empty, return None
        if self.is_empty():
            return None
    
        # Find the node at the given position
        current = self.head
        loc = 0
    
        # Traverse to the node at the desired position
        while current is not None and loc < position:
            current = current.right_pointer
            loc += 1
    
        # If position is out of bounds (position greater than the length of the list)
        if current is None:
            print("Position out of bounds.")
            return None
    
        # If the node to be deleted is the head
        if current == self.head:
            #set the new head to be the node to the right of the current head
            self.head = current.right_pointer
            if self.head:  # If the new head exists, update its left pointer
                self.head.left_pointer = None
        
        # If the node to be deleted is the tail
        elif current == self.tail:
            self.tail = current.left_pointer
            if self.tail:  # If the new tail exists, update its right pointer
                self.tail.right_pointer = None
        
        # For any node in the middle
        else:
            current.left_pointer.right_pointer = current.right_pointer
            current.right_pointer.left_pointer = current.left_pointer
    


        
    # Searches the DLL to determine if a given input value is present in the list
    # returns the position in list, or False if not in DLL
    def find_value(self, value):
        current = self.head
        loc = 0
    
        while current:
            if current.key == value:
                return loc
            current = current.right_pointer
            loc += 1
    
        return False  # Return False if the value isn't found

    
    # Replace the value of the node at the given position.   
    def replace_value(self, position, value):
        if position is False:
            print(position, "is an invalid position, skipping replace_value")
            return None

        current = self.head
        loc = 0
        
        # Traverse to the desired position
        while current and loc < position:
            current = current.right_pointer
            loc += 1
    
        # If position is out of bounds
        if current is None:
            print("Position out of bounds.")
            return
    
        # Replace the node's value
        current.key = value

    
    
    def print_list(self):
        current = self.head
        
        while current:
            print(current.key, " ")
            current = current.right_pointer
