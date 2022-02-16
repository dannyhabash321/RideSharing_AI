#visualize through adjacency list
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from prettytable import PrettyTable 


outputFile= "output.txt" #file to output logs to
f = open(outputFile, "w")#opens file to be written to


#class passenger
class Passenger:
    def __init__(self, passID, pickUp, dropOff):
        self.passID = passID #holds passengerID which uniquely identifies passenger
        self.pickUp = pickUp #pickup which is the node where the person is located to be picked up
        self.dropOff = dropOff #what node the person requests to be dropped off
#class passenger

#class vehicle
class Vehicle:
    def __init__(self, vehicleID, path, currentNode, people, pickUps, dropOffs, totalDistance, passCount=0):
        self.vehicleID = vehicleID #unique vehicle identifier
        self.path = path #current path of vehicle, essentially the route of the current destination of vehicle
        self.currentNode = currentNode #the node the vehicle is currently at
        self.people = people #the passengers that are currently in the vhicle or have been assigned to that vehicle
        self.pickUps = pickUps #list of pickup destination amonst the passenegers assigned to the vehicle
        self.dropOffs = dropOffs #list of dropoff destinations for every person in the car
        self.totalDistance = totalDistance #total distance the car traveled during the simulation, used for statistics and reports
        self.passCount = passCount #total passengers vehicle picked up and dropped off
#class vehicle

#this function takes vehicle as an argument and then updates its path to prioritize shortest path pickups and then after all pickups, shortest path dropoffs
def pathPriority(vehicle):
    shortestPath= [None] * nodeCount #initializes path to max
    if len(vehicle.pickUps) != 0: #checks for any pickups first because pickups are prioritized over dropoffs, then picks the shortest path pickup
        for pickUp in vehicle.pickUps:
            path = nx.shortest_path(G, vehicle.currentNode, pickUp)
            if len(shortestPath) > len(path):
                shortestPath= path
        vehicle.path= shortestPath
    elif len(vehicle.dropOffs) != 0: #if all pickups are picked up then shortest path drop off is set to cars path
        for dropOff in vehicle.dropOffs:
            path = nx.shortest_path(G, vehicle.currentNode, dropOff)
            if len(shortestPath) > len(path):
                shortestPath= path
        
        vehicle.path= shortestPath
        vehicle.path.pop(0)
#this function takes vehicle as an argument and then updates its path to prioritize shortest path pickups and then after all pickups, shortest path dropoffs

#function will be used to determine when to stop simuilation
def getTotalPeopleInVehicles(vehicles): #returns total passenegers in all vehicles
    totalPeople=0
    for vehicle in vehicles:
        totalPeople += len(vehicle.people)
    return totalPeople
#function will be used to determine when to stop simuilation

#assigns 
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
            vehicle.pickUps.append(passenger.pickUp)
            vehicle.dropOffs.append(passenger.dropOff)
            pathPriority(vehicle)
            vehicle.passCount+=1
            eta = 6*(len(shortestPath)-1)/60
            print("Vehicle", assignedVehicle, "assigned to", passenger.passID,". ETA:", eta, "minutes.", "Path:", vehicles[assignedVehicle].path, "People:", vehicle.people, file=f)
            advanceVehicles(vehicles, passengers)


#checks destinations of passengers after each node advancement to see if there is a pickup or dropoff 
def checkDestinations(vehicle, passengers):
    if(vehicle.currentNode not in vehicle.pickUps and vehicle.currentNode not in vehicle.dropOffs):
        print("\n", file=f, end="")
    for passenger in vehicle.people:
        if vehicle.currentNode==passengers[passenger].pickUp: #if there is a pickup for any person on the current node, they are picked up and status changes to -1 for picked up
            passengers[passenger].pickUp=-1
            vehicle.pickUps.remove(vehicle.currentNode)
            print(" and picked up passenger", passenger, "at", vehicle.currentNode, file=f)
        if vehicle.currentNode==passengers[passenger].dropOff and passengers[passenger].pickUp==-1: # #if there is a drop for any person on the current node and they have a -1 for picked up which indicates they have been pickedf up, they are dropped off
            vehicle.people.remove(passenger)
            vehicle.dropOffs.remove(vehicle.currentNode)
            print(" and dropped off passenger", passenger, "at", vehicle.currentNode, file=f)
        
#checks destinations of passengers after each node advancement to see if there is a pickup or dropoff 


#this function advances all busy vehicles, one node at a time to their next node in their cuurrent path
def advanceVehicles(vehicles, passengers):
    for vehicle in vehicles:
        #initial condition to not move vehicles if they dont have a path and any destinations
        if len(vehicle.pickUps) ==0 and len(vehicle.dropOffs) == 0 and len(vehicle.path)==0:
            continue
        
        vehicle.totalDistance+=1 #this increases the total distance by one becuase each busy car will be moving one node up
        if len(vehicle.path)==1:#checks if there is one node leftr in path so that the next destination can be chosen from either pickups or dropoffs of the car
            vehicle.currentNode = vehicle.path[0] #sets current node to the next node in path
            vehicle.path.pop(0)#removes that node to make it empty
            print("Vehicle:", vehicle.vehicleID, "Advanced to", vehicle.currentNode, file=f, end="")
            checkDestinations(vehicle, passengers) #checks if there are any people to be dropped or picked
            if len(vehicle.pickUps)>0 or len(vehicle.dropOffs)>0: #if the car still has any dropoffs pickups then path will be updated in the following function, if not then path is emnpty and car waits at current node until next pickup
                pathPriority(vehicle)
        elif len(vehicle.path)>1: # if there is more than one node in path then vehicle just goes to the next node and then pops off that node
            vehicle.path.pop(0)
            vehicle.currentNode = vehicle.path[0]
            print("Vehicle:", vehicle.vehicleID, "Advanced to", vehicle.currentNode, file=f, end="") 
            checkDestinations(vehicle, passengers)#checks if there are any people to be dropped or picked
            
        

G = nx.Graph() #uses networkx library to create directed graph

nodeCount = 200 # the number of nodes to randomly generate
passCount = 1200 #number of total passenegers that will submit a request
vehicleCount = 30 #number of vehicles that spawn at node 0(The hub)
passengers = [] #list to hold passenger objects
vehicles = [] #list for vehicles 
connectivity=4 #connectivity average per node




print("\n****BEGINNING OF SIMULATION****\n", file=f)


#generates a random graph with a specified connectivity average
for i in range(nodeCount):
    G.add_node(i)
    for j in range(0,connectivity):
        v=np.random.randint(nodeCount)
        while v==i: #makes sure a node doesnt connect to itself
            v=np.random.randint(nodeCount)
        G.add_edge(i,v)
#generates a random graph with a specified connectivity average


#generates vehicles up to n at located at node 0, with all empty pickup and dropoffs
for n in range(0, vehicleCount):
    vehicle = Vehicle(n, [], 0,[],[],[],0)
    vehicles.append(vehicle)
#generates vehicles up to n at located at node 0, with all empty pickup and dropoffs

#generate pickup and dropoff location for each passenger, and outputs where they spawned
for n in range(0, passCount):
    if n%150==0:
        print("\nHour:", (n//150)+1, file=f)
    
    pickUp = np.random.randint(nodeCount)
    dropOff = np.random.randint(nodeCount)
    passID=n
    while pickUp==dropOff:
        dropOff = np.random.randint(nodeCount)
    print("SERVICE REQUEST:","Passenger ", n , " spawned at ", pickUp, " to be dropped off at ", dropOff, file=f)
    passenger=Passenger(passID, pickUp, dropOff)
    passengers.append(passenger)
    assign(passenger, vehicles)
#generate pickup and dropoff location for each passenger, and outputs where they spawned



#this code insures that all people are dropped off, runs until theres no passenegers left on any vehicle
while getTotalPeopleInVehicles(vehicles) != 0:
    advanceVehicles(vehicles, passengers)
#this code insures that all people are dropped off, runs until theres no passenegers left on any vehicle

print("\n****END OF SIMULATION****\n", file=f)



print("Simulation has been output to", outputFile, "successfully.")


totalNodes=0
totalTime=0
table = PrettyTable(["Vehicle ID", "Total Passengers Serviced", "Total Nodes Traversed", "Total Driving Time (in minutes)"])
for vehicle in vehicles:
    table.add_row([vehicle.vehicleID, vehicle.passCount, vehicle.totalDistance, (vehicle.totalDistance)/10])
    totalNodes+=vehicle.totalDistance
    totalTime+= (vehicle.totalDistance)/10



table.add_row(["Total", passCount, totalNodes, totalTime//1]) 
print("REPORTS".center(70," "), file=f)
print(table, file=f)
print("Average Nodes Traveled:", totalNodes//vehicleCount, file=f)

f.close()




#draws out the network and visualizes it
nx.draw_networkx(G) 
plt.show() 
#draws out the network and visualizes it