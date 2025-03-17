import numpy as np
from config import global_variables
import random as rnd

#Here, the drone class is defined
class GameUAV:
    def __init__(self, cpuCapacity, ID):
        self.ID=ID
        self.cpuCapacity = cpuCapacity

        # Factor of how much more computations is required for the cyclic task of this device
        self.weight = rnd.uniform(global_variables.NMPCcycles_expected_weightFactor_min,
                                  global_variables.NMPCcycles_expected_weightFactor_max)
        
        self.LocalExpectedCpuCycles = self.weight*global_variables.NMPCcycles_expected
        self.RTTleft=0
        self.calculationsLeft=round(rnd.uniform(self.LocalExpectedCpuCycles + global_variables.NMPCcyclesPlusMinus, 
                                                self.LocalExpectedCpuCycles - global_variables.NMPCcyclesPlusMinus))

        #Internet
        self.antenna=-1 
        
        #Server
        self.serverInfo=-1

        #Startegy. Location of computation.
        self.strategy=0 #0=local, higher=offload to Server with ID
        self.oldU=self.U_local()
        self.deltaU=0
        self.percentageImprovement = 0

        self.nbrStrategyUpdates = 0
        self.nbrNMPCexecutions = 0

        
    # Connect to the internet (antenna)
    def connectToInternet(self,antenna):
        self.antenna=antenna
        #BS.connectDrone(self)
        
    # Disconnect from the internet (antenna)
    def disconnectFromInternet(self):
        self.antenna=-1

    # Connect to server
    def connectToServer(self,serverInfo):
        self.serverInfo=serverInfo
        serverInfo[0].connectUAV(self)
        
    # Disconnect from server
    def disconnectFromServer(self):
        if not self.serverInfo == -1:
            self.serverInfo[0].disconnectUAV(self)
            self.serverInfo=-1

    """
    Calculates the utility function value
    """
    def U(self):
        if self.strategy == 0:
            return self.U_local()
        else:
            return self.U_offload(serverInfo = self.serverInfo)

    """
    Calculates utility function if offloading
    """
    def U_offload(self,serverInfo):
        server = serverInfo[0]
        RTT = serverInfo[1]
        if server.ID == self.strategy:
            # weight included in LocalExpectedCpuCycles. Important!
            return -1*(RTT + self.LocalExpectedCpuCycles/server.getCpuPerUAV(0)) #current state
        else:
            # weight included in LocalExpectedCpuCycles. Important!
            return -1*(RTT + self.LocalExpectedCpuCycles/server.getCpuPerUAV(1)) # One extra drone at server
        
    """
    Utility function if computing locally
    """
    def U_local(self):
        return -1*self.LocalExpectedCpuCycles/self.cpuCapacity
    
    """
    Calculates the best strategy
    (where to put computations)
    """
    def calculateBestStrategy(self):
        # Update only if it is a significant improvement.
        scoreToBeat = self.oldU*(1-global_variables.tImprovementReq)
        bestScore = self.oldU
        bestStrategy = self.strategy

        #print("____start____")
        #print("UAV", self.ID, "score to beat: ", scoreToBeat)
        #print("UAV", self.ID, "current best score: ", bestScore)
        #print("UAV", self.ID, "current best strategy: ", self.strategy)
        
        if self.U_local() > scoreToBeat:
            scoreToBeat = self.U_local()
            bestScore=self.U_local()
            bestStrategy=0

        #print("UAV", self.ID, "U_Local ", self.U_local())
        
        if self.antenna == -1:
            bestScore=self.U_local()
            bestStrategy=0
            return bestStrategy, bestScore
        
        aServers = self.antenna.getServerInfo()
        if len(aServers) > 0:
            for server in aServers:
                score = self.U_offload(server)
        #        print("UAV", self.ID, "U_DC ", server[0].ID ,"score", score)
                if score > scoreToBeat:
                    bestStrategy=server[0].ID
                    scoreToBeat = score
                    bestScore=score
        #print("Best strategy was: ", bestStrategy)
        #print("____end____")
        return bestStrategy, bestScore
    
    # Find Data center from its ID
    def findServerfromID(self,serverInfo,ID):
        if serverInfo != -1:
            for server in serverInfo:
                if server[0].ID == ID:
                    return server
        raise NameError("Server with ID", ID, "not found.")
    

    """
    updateToASpecificStrategy(strategy):
    Updates to a specific strategy. Used for debugging and manually set strategy.
    In all "normal" cases, it runs self.updateStrategy(),
    since that gives the best strategy
    """
    def updateToASpecificStrategy(self, strategy):
        # Calculate old U
        strategyUpdated = 0
        if self.strategy == 0:
            self.oldU = self.U_local()
        else:
            self.oldU = self.U_offload(serverInfo = self.serverInfo)

        # Calculate new U
        if strategy == 0:
            newScore = self.U_local()
        else:
            #print([self.findDCfromID(serverInfo = self.antenna.serverInfo, ID = strategy)])
            newScore = self.U_offload(self.findServerfromID(serverInfo = self.antenna.getServerInfo(), ID = strategy))
        
        # Update strategy
        if strategy != self.strategy and strategy != 0:
            if self.strategy != 0:
                self.disconnectFromDC()
            self.strategy = strategy
            self.connectToServer(self.findServerfromID(self.antenna.getServerInfo(), self.strategy))
            strategyUpdated=1
        elif strategy != self.strategy:
            self.strategy = strategy
            self.disconnectFromDC()
            strategyUpdated=1

        # Calculate dU
        self.deltaU = newScore - self.oldU
        self.percentageImprovement =  abs(1 - newScore/self.oldU)*100
        return strategyUpdated
    
    
    """
    updateStrategy(self):
    Updates to the best strategy (a specific server or local computing) and calculates utility score and time improvements.
    """
    def updateStrategy(self):
        strategyUpdated = 0
        if self.strategy == 0:
            self.oldU = self.U_local()
        else:
            self.oldU = self.U_offload(serverInfo = self.serverInfo)
        
        [bestStrategy, bestScore] = self.calculateBestStrategy()
        
        if bestStrategy != self.strategy and bestStrategy != 0:
            if self.strategy != 0:
                self.disconnectFromServer()
            self.strategy = bestStrategy
            self.connectToServer(self.findServerfromID(self.antenna.getServerInfo(), self.strategy))
            strategyUpdated=1
            
        elif bestStrategy != self.strategy:
            self.strategy = bestStrategy
            self.disconnectFromServer()
            strategyUpdated=1
       
        self.deltaU = bestScore - self.oldU  # Calculate deltaU to compare with delta potential function
        self.percentageImprovement =  abs(1 - bestScore/self.oldU)*100
        if strategyUpdated:
            self.nbrStrategyUpdates += 1
        return strategyUpdated

    """
    calculateTimeLeft():
        Calculates expected time left for the current cycle.
    """ 
    def calculateTimeLeft(self):
        if self.strategy == 0:
            return self.calculationsLeft/self.cpuCapacity
        else:
            return self.RTTleft + self.calculationsLeft/self.serverInfo[0].getCpuPerUAV(0)
       
    """
    elapseTimeDataAndCpu():
        This is a bit tricky and ugly. But the method 
        takes a couple of seconds as input and lets the drone/BS/data transfer
        to occurr. It updates the attribute self.calcLeftOneImage according
        to how much calculations that has been done during this time.
        
        If local computing, it simply calculates locally.
        
        If offloading, the data is first transfered and then the computations are done.
        This makes it messy.
    """
    def elapseTimeDataAndCpu(self,time):
        # If the data transfer is done.
        if self.RTTleft <= 0:
            if self.strategy == 0: #Local
                self.calculationsLeft -= self.cpuCapacity*time
            else: #DC
                self.calculationsLeft -= self.serverInfo[0].getCpuPerUAV(0)*time

        elif self.RTTleft <= time:
            # Always offloading here. t1 is time to send all data that are left to send. 
            self.calculationsLeft -= self.serverInfo[0].getCpuPerUAV(0)*(time-self.RTTleft)
            self.RTTleft = 0
        else:
            self.RTTleft -= time
        
    """
    elapseTime():
        If the current calculation gets done, update strategy and return 1.
        If still in the process of the current image, just let the time
        elapse and return 0.
    """
    def elapseTime(self,time):
        self.elapseTimeDataAndCpu(time)
        strategyUpdated = 0
        calculationDone = 0
        if self.calculationsLeft <= 0:
            calculationDone = 1
            strategyUpdated = self.updateStrategy()
            self.setNewCalc()
        
        return strategyUpdated, calculationDone
        
    # When computation is done, this 
    # method sets the next calculations + RTT
    def setNewCalc(self):
        self.nbrNMPCexecutions += 1
        if self.strategy == 0:
            self.RTTleft = 0
            self.calculationsLeft = round(rnd.uniform(self.LocalExpectedCpuCycles + global_variables.NMPCcyclesPlusMinus, 
                                                      self.LocalExpectedCpuCycles - global_variables.NMPCcyclesPlusMinus))
        else:
            self.RTTleft = self.serverInfo[1]
            self.calculationsLeft = round(rnd.uniform(self.LocalExpectedCpuCycles + global_variables.NMPCcyclesPlusMinus, 
                                                      self.LocalExpectedCpuCycles - global_variables.NMPCcyclesPlusMinus))
            
    """
    printInfo():
        Prints all important drone info.
    """
    def printInfo(self):
        if self.antenna != -1:
            print("This is Drone ", self.ID, ", with strategy", self.strategy, 
                " connected to antenna", self.antenna.ID, ", current U: ", round(self.calculateBestStrategy()[1],5), "local U: ", round(self.U_local(),5))
        else:
            print("This is Drone ", self.ID, ", with strategy", self.strategy, 
                " Not connected to Internet, current U: ", round(self.calculateBestStrategy()[1],5), "local U: ", round(self.U_local(),5))