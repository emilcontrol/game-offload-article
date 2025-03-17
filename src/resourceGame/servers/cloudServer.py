from src.resourceGame.servers.serverInterface import ServerInterface
from config import global_variables
import math
"""
    Cloud Server class.
    Information about a data center,
    like location, range, strength.
    Possible to extend with functionality
    for randomness and decreasing strength
    if further away.

    Every connected UAV gets assigned to one container
    of equal size, meaning that there are no competition
    of resources in these servers. Every UAV gets a certain amount
    of cpu resources.
"""
class CloudServer(ServerInterface):
    def __init__(self,cpuCapacityPerUnit,ID):
        self.type = "cloud"
        self.ID=ID
        
        self.connectedUAVs=[]
        self.nbrUAVs=0
        self.cpuCapacityPerUnit=cpuCapacityPerUnit
        
    def getCpuPerUAV(self,extraUAVs):
        return self.cpuCapacityPerUnit
    
    def getCpuForHypotheticalNbrUAV(self,UAVs):
        return self.cpuCapacityPerUnit
        
    def connectUAV(self,UAV): #Called from drone instance
        if UAV in self.connectedUAVs:
            raise NameError("Failed to add drone to server. Already one identical there.")
        
        self.connectedUAVs.append(UAV)
        self.nbrUAVs += 1
        
    def disconnectUAV(self,UAV): #Called from drone instance
        if not UAV in self.connectedUAVs:
            raise NameError("Failed to remove drone from server. This drone is not here.")
        
        self.connectedUAVs.remove(UAV)
        self.nbrUAVs -= 1
        
    def printInfo(self):
        if not len(self.connectedUAVs) > 0:
            print("This is Cloud Server ", self.ID, 
                  "No UAVs are connected to me.")
        else:
            print("This is Cloud Server ", self.ID, ". Total cpu capacity: ", self.cpuCapacityPerUnit,  
                  ". ", self.nbrUAVs, "UAVs are connected to me. Bandwidth per drone is ",
                 self.getCpuPerUAV(0))
        
        