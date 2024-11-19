from collections import deque
import networkx as nx
import matplotlib.pyplot as plt
import random
import timeit
import heapq


def Naive_Dijkstras(network, nodes, source, destination):
    num_nodes = len(nodes)
    S = set() #Permanent Nodes
    S_c = set(nodes) #Temporary Nodes
    distance = dict() #Distances to each node
    predecessors = dict() #The predecessor for each node in our path

    #Initializing our distance and predecessor labels
    for n in nodes: 
        distance[n] = 999_999_999
        predecessors[n] = -1

    distance[source] = 0 #Source is where we are starting, i.e cost = 0. Also guarantees that we look at this node first
    predecessors[source] = 0

    #lets calculate some distances, this is the main loop of Dijkstras
    while len(S) < num_nodes:
        current_node = min(S_c, key=distance.get) #This grabs the node with the smallest distance
        S.add(current_node)
        S_c.discard(current_node)

        for adjacent_node in network[current_node]:
            if distance[adjacent_node] > distance[current_node] + network[current_node][adjacent_node]:
                distance[adjacent_node] = distance[current_node] + network[current_node][adjacent_node]
                predecessors[adjacent_node] = current_node

    #This just reconstructs the path into a neater form

    path = deque()
    current_node = destination
    path.append(current_node)
    while current_node != source:
        current_node = predecessors.pop(current_node)
        path.appendleft(current_node)

    return path, distance[destination]

def Heap_Dijkstras(network, nodes, source, destination):
    num_nodes = len(nodes)
    S = set() #Permanent Nodes
    S_c = set(nodes) #Temporary Nodes
    distance = BinaryHeap() #Distances to each node
    predecessors = dict() #The predecessor for each node in our path

    #Initializing our distance and predecessor labels
    for n in nodes: 
        distance.Insert_Key(999_999_999, n)
        predecessors[n] = -1

    distance.Decrease_Key(source, 0) #Source is where we are starting, i.e cost = 0. Also guarantees that we look at this node first
    predecessors[source] = 0

    #lets calculate some distances, this is the main loop of Dijkstras
    while len(S) < num_nodes:
        current_node, distance_current_node = distance.Find_Min_Node() #This grabs the node with the smallest distance
        S.add(current_node)
        S_c.discard(current_node)

        for adjacent_node in network[current_node]:

            #We don't touch the distance labels of nodes in the permanent set
            if adjacent_node not in S:
                distance_adjacent_node = distance.heap[distance.node_locations[adjacent_node]]

                if distance_adjacent_node > distance_current_node + network[current_node][adjacent_node]:
                    distance.Decrease_Key(adjacent_node, distance_current_node + network[current_node][adjacent_node])
                    predecessors[adjacent_node] = current_node
            else:
                pass

    #This just recpnstructs the path into a neater form
    path = deque()
    cost = 0
    current_node = destination
    path.append(current_node)
    while current_node != source:
        current_node = predecessors.pop(current_node)
        cost = cost + network[current_node][path[0]]
        path.appendleft(current_node)

    return path, cost

def Naive_Kruskals(nodes, edges, dist):

    #Initialize vars
    mst = set()
    total_cost = 0
    edges = list(edges)

    #Sort our edges by weight
    edges.sort(key = lambda edge: dist[edge])

    #generate our linked lists
    components = {node: Doubly_Linked_List() for node in nodes}
    for node in nodes:
        components[node].insert_end(node)
        components[node].size = 1

    for i, j in edges:
        weight = dist[(i,j)]

        if type(components[i].find_value(j)) == bool:
            mst.add((i, j)) #Add edge to MST
            total_cost = total_cost + weight #Update total cost

            components[i].merge(components[j]) #Merge the lists together

            #Update list references for every item in the list containing now i and j

            current = components[i].head
            while current:
                components[current.key] = components[i]
                current = current.right_pointer

    return mst, total_cost

def Improved_Kruskals(nodes, edges, dist):
    
    #Initialize vars
    mst = set()
    total_cost = 0
    edges = list(edges)

    #Sort our edges by weight
    edges.sort(key = lambda edge: dist[edge])

    #generate our linked lists
    components = {node: Doubly_Linked_List() for node in nodes}
    for node in nodes:
        components[node].insert_end(node)
        components[node].size = 1

    for i, j in edges:
        weight = dist[(i,j)]

        if components[i].tail != components[j].tail:
            mst.add((i, j)) #Add edge to MST
            total_cost = total_cost + weight #Update total cost

            components[i].merge(components[j]) #Merge the lists together

            #Update list references for every item in the list containing now i and j

            current = components[i].head
            while current:
                components[current.key] = components[i]
                current = current.right_pointer

    return mst, total_cost

def Heap_Prims(network, nodes, source):
    # Initialize the MST path and total cost
    mst_path = set()
    total_cost = 0

    # Set to track nodes already in the MST
    in_mst = set()
    in_mst.add(source)

    # Min-Heap to keep track of edges (weight, from_node, to_node)
    heap = BinaryHeap()

    # Add all edges from the start node to the heap
    for adjacent, weight in network[source].items():
        heap.Insert_Key(weight, (source, adjacent))

    # Main loop to construct the MST
    while len(in_mst) < len(nodes):

        # Extract the edge with the minimum weight
        (from_node, to_node), min_weight  = heap.Find_Min_Node()

        # If the to_node is already in the MST, skip it
        if to_node in in_mst:
            continue
        
        else:
            # Otherwise, add this edge to the MST
            in_mst.add(to_node)
            total_cost = total_cost + min_weight
            mst_path.add((from_node, to_node))

            # Add all new edges from the newly added node to the heap
            for adjacent, weight in network[to_node].items():
                if adjacent not in in_mst:
                    heap.Insert_Key(weight, (to_node, adjacent))

        

    return mst_path, total_cost

def Heap_Prims_Improved(network, nodes, source):
    # Initialize the MST path and total cost
    mst_path = set()
    total_cost = 0

    # Set to track nodes already in the MST
    in_mst = set()
    in_mst.add(source)

    # Min-Heap to keep track of edges (weight, from_node, to_node)
    heap = []
    heapq.heapify(heap)

    # Add all edges from the start node to the heap
    for adjacent, weight in network[source].items():
        heapq.heappush(heap, (weight, source, adjacent))

    # Main loop to construct the MST
    while len(in_mst) < len(nodes):
        # Extract the edge with the minimum weight
        min_weight, from_node, to_node = heapq.heappop(heap)

        # If the to_node is already in the MST, skip it
        if to_node in in_mst:
            continue

        # Otherwise, add this edge to the MST
        in_mst.add(to_node)
        total_cost += min_weight
        mst_path.add((from_node, to_node))

        # Add all new edges from the newly added node to the heap
        for adjacent, weight in network[to_node].items():
            if adjacent not in in_mst:
                heapq.heappush(heap, (weight, to_node, adjacent))

    return mst_path, total_cost

def Naive_Prims(network, nodes, source):
    # Initialize the MST path and total cost
    mst_path = set()
    total_cost = 0

    # Sets to track nodes in and out of the MST
    in_mst = {source}
    not_in_mst = set(nodes) - in_mst

    # Main loop to construct the MST
    while not_in_mst:
        min_cost = 999_999_999
        next_node = None
        connecting_node = None

        # Iterate over all nodes in the MST
        for node in in_mst:
            for adjacent_node in not_in_mst:
                current_cost = network[node].get(adjacent_node)
                
                # Check if the edge exists and is the minimum so far
                if current_cost is not None and current_cost < min_cost:
                    min_cost = current_cost
                    next_node = adjacent_node
                    connecting_node = node

        # Update sets and MST path
        in_mst.add(next_node)
        not_in_mst.remove(next_node)
        mst_path.add((connecting_node, next_node))
        total_cost += min_cost

    return mst_path, total_cost

# ===================================DATA STRUCTS AND SUPPORT FUNCS=============================================================

#**************************************************************************
def Quick_Sort(array, dist):
  if len(array) < 2:
    return array
  else:
    # Randomly choose a pivot to avoid worst-case O(n²) complexity
    pivot_index = random.randint(0, len(array) - 1)
    pivot = array[pivot_index]
    
    # Create three lists.  One with numbers smaller then the pivot, 
    # One with numbers equal to the pivot value (which includes the pivot) 
    # The last with numbers larger then pivot value
    smaller = [i for i in array if dist[i] < dist[pivot]]
    equal = [i for i in array if dist[i] == dist[pivot]]
    larger = [i for i in array if dist[i] > dist[pivot]]
    return Quick_Sort(smaller, dist) + equal + Quick_Sort(larger, dist)

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

#**************************************************************************
class BinaryHeap:
    
    def __init__(self):
        self.heap = deque()
        self.node_heap_id = deque()
        self.node_locations = {}
        
    def Insert_Key(self, key, node_id):
        self.heap.append(key)
        self.node_heap_id.append(node_id)
        self.node_locations[node_id] = len(self.heap)-1

        node_loc = self.node_locations[node_id]
        self.Sift_Up(node_loc)
        
    def Increase_Key(self, node, new_value):
        
        node_loc = self.node_locations[node]
        self.heap[node_loc] = new_value
        self.Sift_Down(node_loc)
        
    def Decrease_Key(self, node, new_value):
        
        node_loc = self.node_locations[node]
        self.heap[node_loc] = new_value
        self.Sift_Up(node_loc)
        
    def Delete_Min(self):
        min_value = []
        if len(self.heap) > 0:
            min_value = self.heap[0]
            min_node_id = self.node_heap_id.popleft()
            del self.node_locations[min_node_id]
            last_value = self.heap.pop()
            
        if len(self.heap) > 0:
            self.Increase_Key(self.node_heap_id[0], last_value)
            
        return min_value, min_node_id
    
    def Find_Min_Node(self):
        
        min_value = []
        min_node_id = []
        if len(self.heap) > 0:
            min_value = self.heap[0]
            min_node_id = self.node_heap_id[0]
            
            last_value = self.heap.pop()
            last_id = self.node_heap_id.pop()
            
            del self.node_locations[min_node_id]
            
        if len(self.heap) > 0:
            self.node_heap_id[0] = last_id
            self.node_locations[last_id] = 0
            self.Increase_Key(last_id, last_value)
            
        return (min_node_id, min_value)
        

    def Sift_Up(self, node):
        
        sift = True
        child_position = node
        while (sift):
            
            if child_position == 0:
                break
            
            parent_position = (child_position - 1) // 2
            
            if (self.heap[child_position] < self.heap[parent_position]):
                # swap
                parent = self.heap[parent_position]
                child = self.heap[child_position]
                
                self.heap[parent_position] = child
                self.heap[child_position] = parent
                
                # swap node ID order in heap
                parent_id = self.node_heap_id[parent_position]
                child_id = self.node_heap_id[child_position]
                
                self.node_heap_id[parent_position] = child_id
                self.node_heap_id[child_position] = parent_id
                
                self.node_locations[parent_id] = child_position
                self.node_locations[child_id] = parent_position
                
                child_position = parent_position
                    
            else:
                sift = False
    
        
    def Sift_Down(self, node):
        
        sift = True
        parent_position = node
        
        while (sift):
            # determine locations of children
            left_child = 2*parent_position + 1
            right_child = 2*parent_position + 2
            
            if left_child >= len(self.heap):
                # there are no children to this node
                break
            else:
                min_child = left_child
                min_value = self.heap[left_child] 
                
            if right_child <= (len(self.heap)-1):
                if self.heap[right_child] < min_value:
                    min_value = self.heap[right_child]
                    min_child = right_child          
                    
            if (sift):
                if self.heap[parent_position] > min_value:
                    self.heap[min_child] = self.heap[parent_position]
                    self.heap[parent_position] = min_value
                    
                    # swap node ID order in heap
                    parent_node_id = self.node_heap_id[parent_position]
                    child_node_id = self.node_heap_id[min_child]
                    
                    self.node_heap_id[min_child]= parent_node_id
                    self.node_heap_id[parent_position] = child_node_id
                    
                    self.node_locations[parent_node_id] = min_child
                    self.node_locations[child_node_id] = parent_position
                    
                    parent_position = min_child
                    
                else:
                    sift = False

    def Print_Values(self):
        print("heap : ", self.heap)
        print(" node_heap : ", self.node_heap_id)
        print(" node locations: ", self. node_locations)

#**************************************************************************
def create_undirected_unweighted_network(E):
    """
Creates an adjacency list representation of an **undirected unweighted ** graph using a list of edges.

Parameters:
E (list of tuples): A list where each tuple represents a directed edge in the graph.

Returns:
dict: A dictionary representing the adjacency list of the graph.
      Keys are nodes with outgoing edges, and values are deques containing
      nodes that can be reached directly from each key node.

"""
    #Initialize empty dictionary
    network = {}

    # First pass: Adds a node (as key) and an empty deque (as value) for all nodes
    for edge in E:
        if edge[0] not in network:
            network[edge[0]] = deque()
        if edge[1] not in network:
            network[edge[1]] = deque()

    # Second pass: for every edge [i,j] add node j to node i's deque
    for edge in E:
        network[edge[0]].append(edge[1])
        network[edge[1]].append(edge[0])
         
    return network

#**************************************************************************
def create_directed_unweighted_network(E):
    """
Creates an adjacency list representation of an **directed unweighted ** graph using a list of edges.

Parameters:
E (list of tuples): A list where each tuple represents a directed edge in the graph.

Returns:
dict: A dictionary representing the adjacency list of the graph.
      Keys are nodes with outgoing edges, and values are deques containing
      nodes that can be reached directly from each key node.

"""
    #Initialize empty dictionary
    network = {}

    # First pass: Adds a node (as key) and an empty deque (as value) for all nodes
    for edge in E:
        if edge[0] not in network:
            network[edge[0]] = deque()
        if edge[1] not in network:
            network[edge[1]] = deque()

    # Second pass: for every edge [i,j] add node j to node i's deque
    for edge in E:
        network[edge[0]].append(edge[1])
         
    return network

#**************************************************************************
def create_undirected_weighted_network(E, dist):
    """
    Creates an **undirected, weighted** network from a list of edges and corresponding distances.

    Parameters:
    - E (list of tuples): List of edges, where each edge is represented as a tuple (node1, node2).
                          Each edge indicates an *undirected* connection between node1 and node2.
    - dist (dict): Dictionary where keys are edges (tuples), and values are the distances associated with each edge.
                          The distances represent the cost of traveling between the nodes

    Returns:
    - dict: A dictionary representing the undirected, weighted network, where:
            - Each key is a node, and each value is a dictionary.
            - The nested dictionary contains neighboring nodes as keys and their edge weights as values.
            

    """
    
    # Initialize an empty dictionary to store the network structure
    network = {}

    # First pass: Initialize each node with an empty dictionary to store its neighbors
    for edge in E: # Look at each edge (i, j)
        if edge[0] not in network:
            network[edge[0]] = {}  # Add node i with an empty dictionary if node i is not in network
        if edge[1] not in network:
            network[edge[1]] = {}  # Add node j with an empty dictionary if node j is not in network

    # Second pass: Populate each node's dictionary with neighbors and corresponding edge weights
    for edge in E:
        # Given an edge (i, j) set both i -> j and j -> i with the same distance
        network[edge[0]][edge[1]] = dist[edge]  # Add edge from node i to j with given distance
        network[edge[1]][edge[0]] = dist[edge]  # Add edge from node j to i with the same distance

    return network  # Return the undirected, weighted network dictionary

#**************************************************************************
def create_directed_weighted_network(E, dist):
    """
    Creates an **directed, weighted** network from a list of edges and corresponding distances.

    Parameters:
    - E (list of tuples): List of edges, where each edge is represented as a tuple (node1, node2).
                          Each edge indicates an *undirected* connection between node1 and node2.
    - dist (dict): Dictionary where keys are edges (tuples), and values are the distances associated with each edge.
                          The distances represent the cost of traveling between the nodes

    Returns:
    - dict: A dictionary representing the directed, weighted network, where:
            - Each key is a node, and each value is a dictionary.
            - The nested dictionary contains neighboring nodes as keys and their edge weights as values.
            

    """
    
    # Initialize an empty dictionary to store the network structure
    network = {}

    # First pass: Initialize each node with an empty dictionary to store its neighbors
    for edge in E: # Look at each edge (i, j)
        if edge[0] not in network:
            network[edge[0]] = {}  # Add node i with an empty dictionary if node i is not in network
        if edge[1] not in network:
            network[edge[1]] = {}  # Add node j with an empty dictionary if node j is not in network

    # Second pass: Populate each node's dictionary with neighbors and corresponding edge weights
    for edge in E:
        # Given an edge (i, j) set distance for only i -> j 
        network[edge[0]][edge[1]] = dist[edge]  # Add edge from node i to j with given distance

    return network  # Return the undirected, weighted network dictionary

#**************************************************************************
def generate_graph(num_nodes, density, max_weight):
    # Ensure the density is between 0 and 1
    if density < 0:
        density = 0
    elif density > 1:
        density = 1

    # Define nodes
    nodes = set(range(1, num_nodes + 1))

    # Generate all possible edges
    all_possible_edges = [(i, j) for i in nodes for j in nodes if i < j]
    num_edges = int(len(all_possible_edges) * density)

    # Randomly select a subset of edges
    edges = set(random.sample(all_possible_edges, num_edges))

    # Assign random distances to each edge
    distance = {edge: random.randint(1, max_weight) for edge in edges}

    return nodes, edges, distance

def generate_connected_graph(num_nodes, density, max_weight):
    # Ensure the density is between 0 and 1
    if density < 0:
        density = 0
    elif density > 1:
        density = 1

    # Define nodes
    nodes = set(range(1, num_nodes + 1))

    # Step 1: Create a spanning tree to ensure all nodes are connected
    edges = set()
    available_nodes = list(nodes)
    random.shuffle(available_nodes)

    # Connect all nodes in a chain to form a spanning tree
    for i in range(num_nodes - 1):
        edges.add((available_nodes[i], available_nodes[i + 1]))

    # Assign random distances to each edge in the spanning tree
    distance = {edge: random.randint(1, max_weight) for edge in edges}

    # Step 2: Generate all possible remaining edges that are not in the spanning tree
    all_possible_edges = [(i, j) for i in nodes for j in nodes if i < j and (i, j) not in edges]
    num_additional_edges = int(len(all_possible_edges) * density)

    # Randomly select additional edges to meet the density requirement
    additional_edges = set(random.sample(all_possible_edges, num_additional_edges))
    edges.update(additional_edges)

    # Assign random distances to each additional edge
    distance.update({edge: random.randint(1, max_weight) for edge in additional_edges})

    return nodes, edges, distance




#**************************************************************************
##                           Test Cases                                  ##
#**************************************************************************

# Define all nodes in the network
nodes = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13}

# Define all edges in the network
edges = {(1, 2), (1, 12),  (2, 3), (2, 11), (3, 4),
         (3, 9), (9, 4), (4, 5), (4, 7), (8, 4), (5, 6),
         (7, 6), (8, 7), (13, 7), (9, 8), (10, 8),
         (10, 9), (11, 10), (12, 11), (12, 13), (13, 8)}

# Define the distance/length of every arc
distance = {(1, 2):1, (1, 12):2, (2, 3):2, (2, 11):3, (3, 4):6,
         (3, 9):2, (9, 4):3, (4, 5):3, (4, 7):1, (8, 4):5, (5, 6):1,
         (7, 6):1, (8, 7):2, (13, 7):2, (9, 8):2, (10, 8):8,
         (10, 9):2, (11, 10):1, (12, 11):1, (12, 13):8, (13,8):4}

# --------------
nodes_2 = {1,2,3,4,5}

edges_2 = {(1,2), (1,3), (2,3), (2,4), (3, 4), (3,5), (4,5)}
       
distance_2 = {(1,2):35, (1,3):40, (2,3):25, (2,4):10, (3, 4):20, (3,5):15, (4,5):30}

# --------------

nodes_3 = {1,2,3,4,5,6,7,8}

edges_3 = {(1,2), (1,3), (2,3), (2, 4), (2,5), (3, 5), (4, 5), (4, 6), (5, 6), (5, 7), (6, 7), (6, 8), (7, 8)}

distance_3 = {(1,2):4, (1,3):7, (2,3):3, (2, 4):24, (2,5):19, (3, 5):32, (4, 5):8, (4, 6):15, (5, 6):3, (5, 7):11, (6, 7):8, (6, 8):0, (7, 8):12}

# --------------

nodes_4 = {1,2,3,4,5,6}

edges_4 = {(1,2), (1,3), (2,3), (2, 4), (3, 4), (3, 5), (4, 6), (5, 4), (5, 6)}

distance_4 = {(1,2):6, (1,3):4, (2,3):2, (2, 4):2, (3, 4):1, (3, 5):2, (4, 6):7, (5, 4):1, (5, 6):3}
       




if __name__ == "__main__":

    num_nodes = 10000
    nodes, edges, weights = generate_connected_graph(num_nodes, .9, 100)

    undirected_weighted = create_undirected_weighted_network(edges, weights)
    directed_weighted = create_directed_weighted_network(edges, weights)

    code_to_run_1 = "Naive_Dijkstras(directed_weighted, nodes, 1, 1000)"
    code_to_run_2 = "Heap_Dijkstras(directed_weighted, nodes, 1, 1000)"
    code_to_run_3 = "Naive_Kruskals(nodes, edges, weights)"
    code_to_run_4 = "Improved_Kruskals(nodes, edges, weights)"
    code_to_run_5 = "Naive_Prims(undirected_weighted, nodes, 2)"
    code_to_run_6 = "Heap_Prims_Improved(undirected_weighted, nodes, 2)"
    

    time1 = timeit.timeit(code_to_run_1, globals=globals(), number=1)
    time2 = timeit.timeit(code_to_run_2, globals=globals(), number=1)
    time3 = timeit.timeit(code_to_run_3, globals=globals(), number=1)
    time4 = timeit.timeit(code_to_run_4, globals=globals(), number=1)
    time5 = timeit.timeit(code_to_run_5, globals=globals(), number=1)
    time6 = timeit.timeit(code_to_run_6, globals=globals(), number=1)
    
    print(time1)
    print(time2)
    print(time3)
    print(time4)
    print(time5)
    print(time6)

    # Example usage
    
    # # Create a graph
    # G = nx.DiGraph()

    # # Add nodes
    # G.add_nodes_from(nodes)

    # for edge, weight in distance.items():
    #     G.add_edge(edge[0], edge[1], weight=weight)

    # # Draw the graph with labels and edge weights
    # pos = nx.spring_layout(G)  # Layout for the nodes
    # nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10)

    # # Draw edge labels (weights)
    # edge_labels = nx.get_edge_attributes(G, 'weight')
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # plt.show()

    print("Done")