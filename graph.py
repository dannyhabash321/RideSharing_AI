#visualize through adjacency list
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


#class passenger
class Passenger:
    def __init__(self, passID, pickUp, dropOff):
        self.passID = passID #holds passengerID which uniquely identifies passenger
        self.pickUp = pickUp #pickup which is the node where the person is located to be picked up
        self.dropOff = dropOff #what node the person requests to be dropped off
#class passenger


#class vehicle
class Vehicle:
    def __init__(self, vehicleID, path, currentNode, people, pickUps, dropOffs, totalDistance):
        self.vehicleID = vehicleID #unique vehicle identifier
        self.path = path #current path of vehicle, essentially the route of the current destination of vehicle
        self.currentNode = currentNode #the node the vehicle is currently at
        self.people = people #the passengers that are currently in the vhicle or have been assigned to that vehicle
        self.pickUps = pickUps #list of pickup destination amonst the passenegers assigned to the vehicle
        self.dropOffs = dropOffs #
        self.totalDistance = totalDistance
#class vehicle



def pathPriority(vehicle):
    shortestPath= [None] * nodeCount
    if len(vehicle.pickUps) != 0:
        for pickUp in vehicle.pickUps:
            path = nx.shortest_path(G, vehicle.currentNode, pickUp)
            if len(shortestPath) > len(path):
                shortestPath= path
        vehicle.path= shortestPath
    elif len(vehicle.dropOffs) != 0:
        for dropOff in vehicle.dropOffs:
            path = nx.shortest_path(G, vehicle.currentNode, dropOff)
            if len(shortestPath) > len(path):
                shortestPath= path
        vehicle.path= shortestPath
    else:
        vehicle.path=[]




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
            vehicle.pickUps.append(passenger.pickUp)
            vehicle.dropOffs.append(passenger.dropOff)
            pathPriority(vehicle)
            eta = 6*(len(shortestPath)-1)/60
            print("Vehicle", assignedVehicle, "assigned to", passenger.passID,". ETA:", eta, "minutes.", "Path:", vehicles[assignedVehicle].path, "People:", vehicle.people)
            advanceVehicles(vehicles, passengers)



def checkDestinations(vehicle, passengers):
    for passenger in vehicle.people:
        if vehicle.currentNode==passengers[passenger].pickUp:
            passengers[passenger].vehicle= vehicle.vehicleID
            passengers[passenger].pickUp=-1
            vehicle.pickUps.remove(vehicle.currentNode)
            print("Vehicle:", vehicle.vehicleID, "picked up passenger", passenger, "at", vehicle.currentNode)
        if vehicle.currentNode==passengers[passenger].dropOff and passengers[passenger].pickUp==-1:
            vehicle.people.remove(passenger)
            vehicle.dropOffs.remove(vehicle.currentNode)
            print("Vehicle:", vehicle.vehicleID, "dropped off passenger", passenger, "at", vehicle.currentNode)



def advanceVehicles(vehicles, passengers):

    for vehicle in vehicles:
        #initial condition to not move vehicles if they dont have a path and any destinations
        if len(vehicle.pickUps) ==0 and len(vehicle.dropOffs) == 0 and len(vehicle.path)==0:
            continue
        
        vehicle.totalDistance+=1
        if len(vehicle.path)==1:
            vehicle.currentNode = vehicle.path[0]
            vehicle.path.pop(0)
            print("Vehicle:", vehicle.vehicleID, "Advanced to", vehicle.currentNode)
            checkDestinations(vehicle, passengers)
            if len(vehicle.pickUps)>0 or len(vehicle.dropOffs)>0:
                pathPriority(vehicle)
        elif len(vehicle.path)>1:
            vehicle.currentNode = vehicle.path[0]
            vehicle.path.pop(0)
            print("Vehicle:", vehicle.vehicleID, "Advanced to", vehicle.currentNode) 
            checkDestinations(vehicle, passengers)
            
        

G = nx.Graph() #uses networkx library to create directed graph

nodeCount = 200 # the number of nodes to randomly generate
passengers = []
passCount = 1200
vehicleCount = 30
vehicles = []
connectivity=2
outputFile= "output.txt"

f = open(outputFile, "w")

print("\n****BEGINNING OF SIMULATION****\n", file=f)


#generates a graph with a specified connectivity average
for i in range(nodeCount):
    G.add_node(i)
    for j in range(0,connectivity):
        v=np.random.randint(nodeCount)
        while v==i:
            v=np.random.randint(nodeCount)
        G.add_edge(i,v)
#generates a graph with a specified connectivity average


#generates vehicles up to n at located at node 0
for n in range(0, vehicleCount):
    vehicle = Vehicle(n, [], 0,[],[],[],0)
    vehicles.append(vehicle)
#generates vehicles up to n at located at node 0

#generate pickup and dropoff location for each passenger, and outputs where they spawned
for n in range(0, passCount):
    pickUp = np.random.randint(nodeCount)
    dropOff = np.random.randint(nodeCount)
    passID=n
    while pickUp==dropOff:
        dropOff = np.random.randint(nodeCount)
    print("Passenger ", n , " spawned at ", pickUp, " to be dropped off at ", dropOff, file=f)
    passenger=Passenger(passID, pickUp, dropOff)
    passengers.append(passenger)
    assign(passenger, vehicles)
#generate pickup and dropoff location for each passenger, and outputs where they spawned



#this code insures that all people are dropped off, runs until theres no passenegers left on any vehicle
while getTotalPeopleInVehicles(vehicles) != 0:
    advanceVehicles(vehicles, passengers)
    print(getTotalPeopleInVehicles(vehicles), file=f)
#this code insures that all people are dropped off, runs until theres no passenegers left on any vehicle

print("\n****END OF SIMULATION****\n", file=f)





total=0
for vehicle in vehicles:
    print("Vhicle",vehicle.vehicleID,":" ,vehicle.totalDistance, file=f)
    total+=vehicle.totalDistance
print("total:", total)



#draws out the network and visualizes it
# nx.draw_networkx(G) 
# plt.show() 
#draws out the network and visualizes it

