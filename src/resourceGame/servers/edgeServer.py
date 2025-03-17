from src.resourceGame.servers.serverInterface import ServerInterface
from config import global_variables
import math
"""
    Edge Server class.
    Information about a data center,
    like location, range, strength.
    Possible to extend with functionality
    for randomness and decreasing strength
    if further away.

    In these servers, there are competition of
    resources. The UAVs can take it from 
    each other.
"""
class EdgeServer(ServerInterface):
    def __init__(self,cpuCapacity,ID):
        self.type = "edge"
        self.ID=ID
        
        self.connectedUAVs=[]
        self.nbrUAVs=0
        self.cpuCapacity=cpuCapacity
        
    """
    getBandwidth(extraDrones):
        Returns the available bandwidth if "extraDrones" extra 
        drones are connected to the base station. Does not take the distance into consideration.
    """
    def getCpuPerUAV(self,extraUAVs):
        return self.cpuCapacity/(self.nbrUAVs + extraUAVs)
    
    def getCpuForHypotheticalNbrUAV(self,UAVs):
        return self.cpuCapacity/(UAVs)
        
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
            print("This is Edge Server ", self.ID, 
                  "No UAVs are connected to me.")
        else:
            print("This is Edge Server ", self.ID, ". Total cpu capacity: ", self.cpuCapacity,  
                  ". ", self.nbrUAVs, "UAVs are connected to me. Bandwidth per drone is ",
                 self.getCpuPerUAV(0))
        
        