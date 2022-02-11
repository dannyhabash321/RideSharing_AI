#visualize through adjacency list
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np



class Passenger:
    def __init__(self, passID, pickUp, dropOff, vehicle):
        self.passID = passID
        self.pickUp = pickUp
        self.dropOff = dropOff
        self.vehicle = vehicle



class Vehicle:
    def __init__(self, vehicleID, path, currentNode, people, destinations):
        self.vehicleID = vehicleID
        self.path = path
        self.currentNode = currentNode
        self.people = people
        self.destinations=destinations



#function will be used to determine when to stop simuilation
def getTotalPeopleInVehicles(vehicles):
    totalPeople=0
    for vehicle in vehicles:
        totalPeople += len(vehicle.people)
    return totalPeople
#function will be used to determine when to stop simuilation


def assign(passenger, vehicles):
    shortestPath = [None] * nodeCount
    assignedVehicle = -1
    for vehicle in vehicles:
        path = nx.shortest_path(G, vehicle.currentNode, passenger.pickUp)
        if(len(shortestPath) > len(path) and len(vehicle.people) < 5):
            shortestPath = path
            assignedVehicle = vehicle.vehicleID
            
    for vehicle in vehicles:
        if vehicle.vehicleID == assignedVehicle:
            vehicle.people.append(passenger.passID)
            vehicle.destinations.insert(0,passenger.pickUp)
            vehicle.destinations.append(passenger.dropOff)
            vehicle.path=shortestPath
            eta = 6*(len(shortestPath)-1)/60
            print("Vehicle", assignedVehicle, "assigned to", passenger.passID,". ETA:", eta, "minutes.", "Path:", vehicles[assignedVehicle].path, "Destinations:", vehicles[assignedVehicle].destinations, "People:", vehicle.people)
            # pathUpdate(vehicle)
            advanceVehicles(vehicles, passengers)







# def pathUpdate(vehicle):
#     vehicle.path=nx.shortest_path(G, vehicle.currentNode, vehicle.destinations[0])
#     advanceVehicles(vehicles, passengers)



def checkDestinations(vehicle, passengers):
    for passenger in vehicle.people:
        if vehicle.currentNode==passengers[passenger].pickUp:
            passengers[passenger].vehicle= vehicle.vehicleID
            passengers[passenger].pickUp=-1
            vehicle.destinations.remove(vehicle.currentNode)
            print("Vehicle:", vehicle.vehicleID, "picked up passenger", passenger, "at", vehicle.currentNode)
        if vehicle.currentNode==passengers[passenger].dropOff and passengers[passenger].pickUp==-1:
            vehicle.people.remove(passenger)
            passengers[passenger].vehicle= -1
            lrev=list(reversed(vehicle.destinations))
            lrev.remove(vehicle.currentNode)
            vehicle.destinations= list(reversed(lrev))
            print("Vehicle:", vehicle.vehicleID, "dropped off passenger", passenger, "at", vehicle.currentNode)



def advanceVehicles(vehicles, passengers):

    for vehicle in vehicles:
        #initial condition to not move vehicles if they dont have a path and any destinations
        if len(vehicle.destinations) ==0 and len(vehicle.path)==0:
            continue
        
        if len(vehicle.path)==1:
            vehicle.currentNode = vehicle.path[0]
            vehicle.path.pop(0)
            print("Vehicle:", vehicle.vehicleID, "Advanced to", vehicle.currentNode, "with dest:" ,vehicle.destinations) 
            checkDestinations(vehicle, passengers)
            if len(vehicle.destinations)>0:
                # vehicle.destinations.pop(0)
                vehicle.path=nx.shortest_path(G, vehicle.currentNode, vehicle.destinations[0])
        elif len(vehicle.path)>1:
            vehicle.currentNode = vehicle.path[0]
            vehicle.path.pop(0)
            print("Vehicle:", vehicle.vehicleID, "Advanced to", vehicle.currentNode, "with dest:" ,vehicle.destinations) 
            checkDestinations(vehicle, passengers)
            
        

        

        





    
    # for vehicle in vehicles:
    #     if len(vehicle.destinations) !=0 or len(vehicle.path)!=0:
    #         if len(vehicle.path)==1:
    #             for personID in vehicle.people:
    #                 if passengers[personID].pickUp==vehicle.currentNode:
    #                     print("Vehicle:", vehicle.vehicleID, "picked up passenger", personID)
    #                     vehicle.destinations.remove(vehicle.currentNode)
    #                     passengers[personID].pickUp=-1
    #                 if passengers[personID].dropOff==vehicle.currentNode and passengers[personID].pickUp==-1:
    #                     print("Vehicle:", vehicle.vehicleID, "dropped off passenger", personID)
    #                     vehicle.destinations.remove(vehicle.currentNode)
    #                     vehicle.people.remove(personID)
    #                     vehicle.path.pop(0)
    #         elif len(vehicle.path)>1:
    #             for personID in vehicle.people:
    #                 if passengers[personID].pickUp==vehicle.currentNode:
    #                     print("Vehicle:", vehicle.vehicleID, "picked up passenger", personID)
    #                     vehicle.destinations.remove(vehicle.currentNode)
    #                     passengers[personID].pickUp=-1
    #                 if passengers[personID].dropOff==vehicle.currentNode and passengers[personID].pickUp==-1:
    #                     print("Vehicle:", vehicle.vehicleID, "dropped off passenger", personID)
    #                     vehicle.destinations.remove(vehicle.currentNode)
    #                     vehicle.people.remove(personID)
    #                     vehicle.currentNode= vehicle.path[1]
    #                     vehicle.path.pop(0)
                
            






def updatePath(vehicle, passengers):

    #send graph, vehicle, current node, all pass nodes

    print("where car at? ", vehicle.currentNode)
    peopleList = []

    peepCount = len(vehicle.people)
    id = vehicle.people[0]
    shortestPath = nx.shortest_path(G, vehicle.currentNode, passengers[id].dropOff)

    for person in range(0, peepCount):

        id = vehicle.people[person]
        path = nx.shortest_path(G, vehicle.currentNode, passengers[id].dropOff)

        if(len(shortestPath) >=  len(path)):
            shortestPath = path
            peopleList.append(person)

    updatedPath = []
    # firstID = vehicle.people[peopleList[0]]
    # updatedPath.append(nx.shortest_path(G, vehicle.currentNode, passengers[firstID].dropOff))

    count = 0
    for x in peopleList:
        if count == 0:
            updatedPath.extend(nx.shortest_path(G, passengers[x].pickUp, passengers[x].dropOff))
            count += 1
        else:
            id = vehicle.people[x]
            path = nx.shortest_path(G, passengers[(x-1)].dropOff, passengers[x].dropOff)
            print(x, "persons path: ", path)
            path.remove(0)
            updatedPath.extend(path)

        print(x, "'s path", updatedPath)







        

G = nx.Graph() #uses networkx library to create directed graph

nodeCount = 200 # the number of nodes to randomly generate
passengers = []
passCount = 1200
vehicleCount = 30
vehicles = []


print("\n****BEGINNING OF SIMULATION****\n")


#open file and write random nodes to file given the nodeCount specified above
file1= open("graph.txt", "w", encoding="utf-16" )
for i in range(nodeCount):
    v1=np.random.randint(nodeCount)
    while v1==i:
        v1=np.random.randint(nodeCount)
    v2=np.random.randint(nodeCount)
    while v2==i:
        v2=np.random.randint(nodeCount)
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

for n in range(0, vehicleCount):
    vehicle = Vehicle(n, [], 0 , [], [])
    vehicles.append(vehicle)

for n in range(0, passCount):
    pickUp = np.random.randint(nodeCount)
    dropOff = np.random.randint(nodeCount)
    passID=n
    while pickUp==dropOff:
        dropOff = np.random.randint(nodeCount)
    print("Passenger ", n , " spawned at ", pickUp, " to be dropped off at ", dropOff)
    passenger=Passenger(passID, pickUp, dropOff, None)
    passengers.append(passenger)
    assign(passenger, vehicles)
    


while getTotalPeopleInVehicles(vehicles) != 0:
    advanceVehicles(vehicles, passengers)
    print(getTotalPeopleInVehicles(vehicles))



print("\n****END OF SIMULATION****\n")

#  passengers.remove((passID == 0))

# for n in passengers:
#     print("Passenger ", n.passID, "info: ", n.pickUp, " drop: ", n.dropOff)
#     if n.passID == 3:
#         passengers.remove(n)
# print("After")
# for n in passengers:
#     print("Passenger ", n.passID, "info: ", n.pickUp, " drop: ", n.dropOff)

# list= nx.shortest_path(G, 0, 9)
# list2 = nx.shortest_path(G, 9, 3)
# list2.pop(0)
# list.extend(list2)

# H = G.subgraph(list)

# nx.draw_networkx( G ) 
# plt.show() 

# for n in vehicles:
#     print(n.vehicleID, " ", n.path, " ", n.currentNode, " ", n.people)


#draws out the network and visualizes it
nx.draw_networkx(G) 
plt.show() 
#draws out the network and visualizes it



















#vehicles

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
