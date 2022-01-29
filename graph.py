# class Passenger:
#     def __init__(self, pickUp, dropOff):
#         self.pickUp = pickUp
#         self.dropOff = dropOff


# class vehicle:
#     def __init__(self, path, currentNode, people):
#         self.path = path
#         self.currentNode= currentNode
#         self.people= [None]*5

# class Node:
#     def __init__(self, people, vehicles, edges):
#         self.people=people
#         self.vehicles=vehicles
#         self.edges=edges
    



# graph=[]

# for i in range(10):
#     n= Node([1,2,3,4,5], [3,4], [i,i+1])
#     graph.append(n)


     
# for n in graph:
#     print(n.people)


# n1=Node(["p1","p2"], ["v1","v2"], [1,2])

# print(n1.edges[1])






#g=Graph([1,3])

#print(g.N)

#n1=Node(["p1","p2"], ["v1","v2"], [1,2])

#print(n1.edges)


#p1=Passenger("N1", "N2")

#print(p1.pickUp)
#print(p1.dropOff)




# import networkx as nx
# import matplotlib.pyplot as plt
# import os
# #import PyPDF2
  
# # Defining a Class
# class GraphVisualization:
   
#     def __init__(self):
          
#         # visual is a list which stores all 
#         # the set of edges that constitutes a
#         # graph
#         self.visual = []
          
#     # addEdge function inputs the vertices of an
#     # edge and appends it to the visual list
#     def addEdge(self, a, b):
#         temp = [a, b]
#         self.visual.append(temp)
          
#     # In visualize function G is an object of
#     # class Graph given by networkx G.add_edges_from(visual)
#     # creates a graph with a given list
#     # nx.draw_networkx(G) - plots the graph
#     # plt.show() - displays the graph
#     def visualize(self):
#         G = nx.Graph()
#         G.add_edges_from(self.visual)
#         nx.draw_networkx(G)
#         plt.savefig('myf.jpeg')
#         os.startfile('myf.jpeg')
        


   
#         #plt.show()

  
# # Driver code
# G = GraphVisualization()
# G.addEdge(0, 2)
# G.addEdge(1, 2)
# G.addEdge(1, 3)
# G.addEdge(5, 3)
# G.addEdge(3, 4)
# G.addEdge(1, 0)
# G.visualize()

#visualize through matrix
# import networkx as nx
# import matplotlib.pyplot as plt

# with open("graphInput2.txt", "r") as file:
#     result = [[int(x) for x in line.split(',')] for line in file]



# G = nx.Graph() 


# for i in range(len(result)): 
#     for j in range( len(result[i])): 
#         if result[i][j] == 1: 
#             G.add_edge(i,j) 


# for i in G.nodes:
#     print (i)
#     print(G.edges(i))

# nx.draw_networkx( G ) 
# plt.show() 


# print(G)




#visualize through adjacency list
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


G = nx.DiGraph() #uses networkx library to create directed graph

nodeCnt=50 # the number of nodes to randomly generate

#open file and write random nodes to file given the nodeCount specified above
file1= open("graph.txt", "w", encoding="utf-16" )
for i in range(nodeCnt):
    v1=np.random.randint(nodeCnt)
    while v1==i:
        v1=np.random.randint(nodeCnt)
    v2=np.random.randint(nodeCnt)
    while v2==i:
        v2=np.random.randint(nodeCnt)
    file1.writelines([str(i), " ", str(v1), " ", str(v2), "\n"])
file1.close()
#open file and write random nodes to file given the nodeCount specified above


#opens file graph that contains adjacency list of nodes to create graph
with open("graph.txt", "r", encoding="utf-16") as file:
    for line in file:
        dig = line.strip().split(" ")
        G.add_node(int(dig[0]))
        for i in range(1,len(dig)):
            if dig[i].isdigit():
                G.add_edge(int(dig[0]),int(dig[i]))
#opens file graph that contains adjacency list of nodes to create graph

#draws out the network and visualizes it
nx.draw_networkx( G ) 
plt.show() 
#draws out the network and visualizes it