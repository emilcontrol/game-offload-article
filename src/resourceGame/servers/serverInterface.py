from abc import ABC, abstractmethod

"""
    Abstract class for different types
    of data centers.

"""
class ServerInterface(ABC):

    # If extraUAVs are added, this method returns the amount of cpu power per UAV with all UAVs.
    @abstractmethod
    def getCpuPerUAV(self,extraUAVs):
        pass

    # Calculates cpu per uav if a total of "UAVs" are connected. Used for calculating the potential function.
    @abstractmethod
    def getCpuForHypotheticalNbrUAV(self,UAVs):
        pass

    # Called from UAV instance. Adds UAV to internal list of connected UAVs.
    @abstractmethod
    def connectUAV(self,UAV):
        pass

    # Called from UAV instance. Removes UAV from internal list of connected UAVs.
    @abstractmethod
    def disconnectUAV(self,UAV): 
        pass

    # Prints some status info of the data center.
    @abstractmethod
    def printInfo(self):
        pass