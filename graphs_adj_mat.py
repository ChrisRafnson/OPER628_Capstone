from collections import deque
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import timeit
from heapq import heappush, heappop, heapify
from doubly_linked_list import Doubly_Linked_List

random.seed(2024)

def Naive_Dijkstras(adj_list, nodes, source, destination):
    num_nodes = len(nodes)
    S = set()  # Permanent Nodes
    S_c = set(nodes)  # Temporary Nodes
    distance = dict()  # Distances to each node
    predecessors = dict()  # The predecessor for each node in our path

    # Initialize distance and predecessor labels
    for n in nodes: 
        distance[n] = float('inf')  # Use infinity for initialization
        predecessors[n] = None

    distance[source] = 0  # Start from the source node

    # Main loop of Dijkstra's
    while len(S) < num_nodes:
        current_node = min(S_c, key=distance.get)  # Node with the smallest distance
        S.add(current_node)
        S_c.discard(current_node)

        # Update distances for all adjacent nodes
        for adjacent_node, weight in adj_list[current_node]:  # Unpack the adjacency list
            if distance[adjacent_node] > distance[current_node] + weight:
                distance[adjacent_node] = distance[current_node] + weight
                predecessors[adjacent_node] = current_node

    # Reconstruct the path
    path = deque()
    current_node = destination
    path.append(current_node)
    while current_node != source:
        current_node = predecessors[current_node]
        path.appendleft(current_node)

    return path, distance[destination]

def Heap_Dijkstras(network, nodes, source, destination):
    S = set()  # Permanent Nodes
    S_c = set(nodes)  # Temporary Nodes
    min_heap = []  # Priority queue for distances
    predecessors = dict()  # The predecessor for each node in our path
    distances = {n: float('inf') for n in nodes}  # Best-known distances

    # Initialize distance for source node
    distances[source] = 0
    heappush(min_heap, (0, source))
    predecessors[source] = None

    # Main loop of Dijkstra's algorithm
    while min_heap:
        distance_current_node, current_node = heappop(min_heap)

        # Skip processing if the node is already in the permanent set
        if current_node in S:
            continue

        S.add(current_node)
        S_c.discard(current_node)

        for adjacent_node, weight in network[current_node].items():
            # Skip nodes in the permanent set
            if adjacent_node in S:
                continue

            new_distance = distance_current_node + weight

            # Update the distance and predecessor if a shorter path is found
            if new_distance < distances[adjacent_node]:
                distances[adjacent_node] = new_distance
                heappush(min_heap, (new_distance, adjacent_node))
                predecessors[adjacent_node] = current_node

    # Reconstruct the path
    path = deque()
    cost = distances[destination]
    current_node = destination
    if cost < float('inf'):  # Check if the destination is reachable
        while current_node is not None:
            path.appendleft(current_node)
            current_node = predecessors[current_node]
    else:
        return None, float('inf')  # Destination is not reachable

    return list(path), cost

def Naive_Kruskals(nodes, edges, dist):
    # Initialize vars
    mst = set()
    total_cost = 0
    edges = list(edges)

    # Sort edges by weight
    edges.sort(key=lambda edge: dist[edge])

    # Generate initial sets for each node
    components = {node: {node} for node in nodes}

    for i, j in edges:
        weight = dist[(i, j)]

        # Check if i and j are in the same component
        if components[i] != components[j]:
            # Add edge to MST
            mst.add((i, j))
            total_cost += weight

            # Merge the two components
            new_component = components[i].union(components[j])
            
            # Update references for all nodes in the new component
            for node in new_component:
                components[node] = new_component

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

def Naive_Prims(matrix, nodes, source):
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
                current_cost = matrix[node][adjacent_node]
                
                # Check if the edge exists and is the minimum so far
                if current_cost > 0 and current_cost < min_cost:
                    min_cost = current_cost
                    next_node = adjacent_node
                    connecting_node = node

        # Update sets and MST path
        in_mst.add(next_node)
        not_in_mst.remove(next_node)
        mst_path.add((connecting_node, next_node))
        total_cost += min_cost

    return mst_path, total_cost

def Heap_Prims(matrix, nodes, source):
    # Initialize the MST path and total cost
    mst_path = set()
    total_cost = 0

    # Set to track nodes already in the MST
    in_mst = set()
    in_mst.add(source)

    # Min-Heap to keep track of edges (weight, from_node, to_node)
    heap = []

    for i in range(len(matrix[source])):
        if matrix[source][i] != 0:
            heappush(heap, (matrix[source][i], source, i))

    # Main loop to construct the MST
    while len(in_mst) < len(nodes):
        # Extract the edge with the minimum weight
        min_weight, from_node, to_node = heappop(heap)

        # If the to_node is already in the MST, skip it
        if to_node in in_mst:
            continue

        # Otherwise, add this edge to the MST
        in_mst.add(to_node)
        total_cost += min_weight
        mst_path.add((from_node, to_node))

        # Add all new edges from the newly added node to the heap
        for i in range(len(matrix[to_node])):
            if (matrix[to_node][i] != 0) and (i not in in_mst):
                heappush(heap, (matrix[to_node][i], to_node, i))

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

def convert_matrix(matrix, create_adj_list=False):
    nodes = []
    edges = []
    dist = {}
    adj_list = {} if create_adj_list else None

    for i in range(len(matrix)):
        nodes.append(i)
        if create_adj_list:
            adj_list[i] = []
        for j in range(len(matrix)):  # Check all rows and columns (not just upper triangle)
            if matrix[i][j] != 0:  # Non-zero weight indicates an edge
                edges.append((i, j))
                dist[(i, j)] = matrix[i][j]
                if create_adj_list:
                    adj_list[i].append((j, matrix[i][j]))  # Directed edge from i to j

    if create_adj_list:
        return nodes, edges, dist, adj_list
    return nodes, edges, dist


#**************************************************************************
##                           Test Cases                                  ##
#**************************************************************************

# Example adjacency matrix
adj_matrix = np.array([
    [0, 2, 3, 0],
    [2, 0, 1, 4],
    [3, 1, 0, 5],
    [0, 4, 5, 0]
])

if __name__ == "__main__":

    # data = np.load("test_cases\\graph_test_cases\\undirected\\size_100_density_0.25.npy")

    # for adj_matrix in data:

    #     nodes, edges, dist = convert_matrix(adj_matrix)

    #     print(Naive_Kruskals(nodes, edges, dist))
    #     print(Improved_Kruskals(nodes, edges, dist))
    #     print(Naive_Prims(adj_matrix, nodes, 2))
    #     print(Heap_Prims(adj_matrix, nodes, 2))

    nodes, edges, dist, list = convert_matrix(adj_matrix, True)
    print(Naive_Dijkstras(list, nodes, 0, random.randint(0, len(adj_matrix))))

