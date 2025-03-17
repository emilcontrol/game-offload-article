from src.resourceGame.antenna import Antenna
from src.resourceGame.gameUAV import GameUAV
from src.resourceGame.servers.edgeServer import EdgeServer
from src.resourceGame.servers.cloudServer import CloudServer

from config import global_variables

import random as rnd
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker

class GreatGame:
    def __init__(self, nUAVs, nAntennas, nEdgeServers, nCloudServers):
        self.aServers=[] #List of base stations
        self.aUAVs=[] #List of drones
        self.UAVindexCounter = 1
        self.aAntennas=[]

        self.timeVec = [] #For plotting
        self.potentialValuesPerTime = [] #For plotting
        self.totalTime = 0 #For plotting
        self.convergeTimes = []
        self.startOfaNewGameTimes = []
        self.hasConverged = False

        self.addMultipleUAVs(nUAVs)
        self.addMultipleAntennas(nAntennas)
        self.addMultipleServers(nEdgeServers, nCloudServers)

        self.connectAllUAVsToRandomAntennas()

        if nEdgeServers >= global_variables.edgeServersPerAntenna:
            self.connectAntennasToNEdgeServers(global_variables.edgeServersPerAntenna) #nEdge
        else:
            raise ValueError("The system cannot have fewer edge servers than edge servers per antenna!")
        
        if nCloudServers >= global_variables.cloudServersPerAntenna:
            self.connectAntennasToMCloudServers(global_variables.cloudServersPerAntenna) #mCloud
        else:
            raise ValueError("The system cannot have fewer cloud servers than cloud servers per antenna!")
        #self.connectAntennasToServers()

        self.assigneachUAVaRandomServer(1) #probability to run local

        self.PotentialFunctionInit = self.potentialFunction()
        self.avgTaskTimeInit = self.avgTaskTime()

        #self.printAllInfo()

    
    def addAntenna(self,ID):
        self.aAntennas.append(Antenna(ID))

    def addMultipleAntennas(self,nAntennas):
        for i in range(1,nAntennas+1):
            self.addAntenna(i)

    def addEdgeServer(self,ID):
        self.aServers.append(EdgeServer(cpuCapacity=global_variables.cpuEdge, ID=ID))

    def addCloudServer(self,ID):
        self.aServers.append(CloudServer(cpuCapacityPerUnit=global_variables.cpuCloudPerUAV, ID=ID))
    
    """
    Add multiple servers.
    """
    def addMultipleServers(self,nEdgeServers,nCloudServers):
        for i in range(1,nEdgeServers+1):
            self.addEdgeServer(i)
        for i in range(1+nEdgeServers,nEdgeServers+nCloudServers+1):
            self.addCloudServer(i)

    """
    Add a device to the system.
    """
    def addUAV(self,ID):
        if ID in [UAV.ID for UAV in self.aUAVs]:
            raise NameError("UAV ID already exist in the game. Cannot add!!")
        #cpuCapacity=round(rnd.uniform(global_variables.cpuLocal + global_variables.cpuLocalPlusMinus, 
        #                             global_variables.cpuLocal - global_variables.cpuLocalPlusMinus))
        cpuCapacity=global_variables.NMPCcycles_expected/rnd.uniform(global_variables.v_l_max,
                                                                     global_variables.v_l_min)
        
        self.aUAVs.append(GameUAV(cpuCapacity=cpuCapacity, ID=ID))
        self.UAVindexCounter += 1

    """
    Remove n devices randomly from the system.
    """
    def removeNRandomUAVs(self,nUAVs):
        if nUAVs > len(self.aUAVs):
            raise IndexError("Tried to remove too many UAVs.")
        IDs = rnd.sample([UAV.ID for UAV in self.aUAVs], k=nUAVs)
        for UAV in self.aUAVs:
            if UAV.ID in IDs:
                UAV.disconnectFromServer()
                self.aUAVs.remove(UAV)

    """
    Add multiple UAVs to the system.
    """
    def addMultipleUAVs(self,nUAVs):
        startCount = self.UAVindexCounter
        for i in range(startCount+1,startCount+nUAVs+1):
            self.addUAV(i)

    """
    Connects all antennas to servers.
    Also sets a RTT from antenna to server individually.
    """
    def connectAntennasToServers(self):
        for antenna in self.aAntennas:
            antenna.connectToAllServers(self.aServers)

    """
    Connects all antennas to the nEdge closest edge servers.
    Also sets a RTT from antenna to server individually.
    """
    def connectAntennasToNEdgeServers(self, nEdge):
        for antenna in self.aAntennas:
            antenna.connectToNRandomEdgeServers(self.aServers, nEdge)

    """
    Connects all antennas to the mCloud closest cloud servers.
    Also sets a RTT from antenna to server individually.
    """
    def connectAntennasToMCloudServers(self, mCloud):
        for antenna in self.aAntennas:
            antenna.connectToMRandomCloudServers(self.aServers, mCloud)

    """
    Connets each UAV with a random antenna.
    """
    def connectAllUAVsToRandomAntennas(self):
        for UAV in self.aUAVs:
            if UAV.antenna == -1:
                UAV.connectToInternet(rnd.choice(self.aAntennas))

    """
    Each of the UAVs that are connected to an antenna gets assigned a server.
    """
    def assigneachUAVaRandomServer(self,probLocal):
        for UAV in self.aUAVs:
            if UAV.antenna == -1:
                pass
            nbrAlternatives = len(UAV.antenna.serverInfo)
            ServerOffload = rnd.choices([0,1],[probLocal, 1-probLocal])[0]
            if not ServerOffload:
                UAV.updateToASpecificStrategy(0)
            else:
                choice = rnd.choice(UAV.antenna.serverInfo)[0]
                UAV.updateToASpecificStrategy(choice.ID)


    """
    Updates all game theory strategies
    (where to put computations) for all UAVs
    """
    def updateAllStrategies(self):
        for UAV in self.aUAVs:
            UAV.updateStrategy()

    """
    Returns the time left (list) for current 
    computation for all drones
    """
    def getAllTimesLeft(self):
        timesLeft=[]
        for UAV in self.aUAVs:
            timeLeft = UAV.calculateTimeLeft()
            if timeLeft <= 0:
                timesLeft.append(0.0000001) #Om det strular, kör en mikrosekund. Ändra detta sen.
            else:
                timesLeft.append(timeLeft)
        return timesLeft

    """
    runAndCompete(breakTime):
    Runs the simulation for breaktime iterations. 
    Ends if the drones comes to an agreement (NE).
    Checks what drone is most soon done with its computations,
    and then let that time elapse for all UAVs.
    breakTime is in seconds.
    """
    def runAndCompete(self, breakTime, printOption):

        self.hasConverged = False
        realBreakTime = breakTime + self.totalTime
        potentialValues = [] 
        oldPotential=self.potentialFunction()
        aConvergence = [False]*len(self.aUAVs) #For convergence chack
        convCheck = True
        self.startOfaNewGameTimes.append(self.totalTime) #For plotting
        possibleConvergeTime = self.totalTime
        
        
        while self.totalTime < realBreakTime:
            timesLeft = self.getAllTimesLeft()
            timeToSubtract = min(timesLeft)
            self.totalTime += timeToSubtract

            
            for i in range(0,len(self.aUAVs)):
                UAV = self.aUAVs[i]
                update, calculationDone = UAV.elapseTime(timeToSubtract)
                

                if calculationDone: # Convercence check logic
                    aConvergence[i] = True
                
                if update:
                    potentialValues.append(self.potentialFunction())
                    if printOption:
                        print("UAV ID:", UAV.ID, "Du:", round(UAV.deltaU,6), ", Dphi:", round(potentialValues[-1] - oldPotential,6),
                            ", Div:", round(UAV.deltaU/(potentialValues[-1] - oldPotential),6) , ", Weight:", round(UAV.weight,6),
                            ", New strategy:", UAV.strategy, ", Time:", round(self.totalTime,3), "s")#, ", Relative Improvement (%):", round(UAV.percentageImprovement,4), )
                    
                    if UAV.percentageImprovement/100 < global_variables.tImprovementReq:
                        raise ValueError("To low improvement in u allowed. Fix!")
                    
                    if abs(UAV.deltaU/(potentialValues[-1] - oldPotential) - UAV.weight) > 0.00001:
                        raise ValueError("Weighted potential function not the same as utility difference!")
                    
                    oldPotential = potentialValues[-1]
                    aConvergence = [False]*len(self.aUAVs)
                    possibleConvergeTime = self.totalTime
            
            # Plotting purposes
            self.timeVec.append(self.totalTime)
            self.potentialValuesPerTime.append(self.potentialFunction())

            if all(aConvergence) and convCheck:
                self.hasConverged = True
                convCheck = False
                self.convergeTimes.append(possibleConvergeTime)
                if printOption:
                    print("...")
                    print("Converged!!!", ", Time:", round(self.totalTime,3), "s")
                    print("...")
                break
            
        
    """
    THIS IS THE ACTUAL SEQUENCE.
    plotOption: 0=no plots. 1=plots shown in 3s. 2: plots shown until user wants
    printOption: 1=prints. 2=does not print.
    """
    def runSequence(self, plotOption, printOption):
        self.runAndCompete(10, printOption)
        #self.connectAllUAVsToRandomAntennas()
        #self.runAndCompete(1)
        #self.removeNRandomUAVs(10)
        #self.runAndCompete(1)
        #self.removeNRandomUAVs(10)
        #self.runAndCompete(1)
        #self.removeNRandomUAVs(10)
        #self.runAndCompete(1)
        #self.addMultipleUAVs(70)
        #self.connectAllUAVsToRandomAntennas()
        #self.runAndCompete(1)

        if plotOption:
            self.plotPotentialFunction()
            self.plotNbrOfStrategyUpdates()

            if plotOption == 1:
                plt.show(block=False)
                plt.pause(3)
            elif plotOption == 2:
                plt.show()

        if printOption > 0:
            self.printAllInfo()

        return self.relevantData()
    
    """
    Obtain relevant data to save from simulation
    """
    def relevantData(self):
        localUAVs, edgeUAVs, cloudUAVs = self.calculateNbrLocalEdgeCloud()
        relData = {'PotentialFunctionInit': self.PotentialFunctionInit,
                   'PotentialFunction': self.potentialFunction(),
                   'avgTaskTimeInit': self.avgTaskTimeInit,
                   'avgTaskTime': self.avgTaskTime(),
                   'nbrStrategyUpdates': self.nbrStrategyUpdates(),
                   'nbrStrategyUpdatesPerDevice': self.nbrStrategyUpdates()/len(self.aUAVs),
                   'nbrNmpcExecutions': self.nbrNmpcExecutions(),
                   'nbrNmpcExecutionsPerDevice': self.nbrNmpcExecutions()/len(self.aUAVs),
                   'hasConverged': self.hasConverged,
                   'nbrLocal': localUAVs,
                   'nbrEdge': edgeUAVs,
                   'nbrCloud': cloudUAVs}
        return relData


    """
    Calculates the proposed potential function.
    """
    def potentialFunction(self):
        potential=0
        for server in self.aServers:
            for i in range(1,server.nbrUAVs+1):
                potential -= global_variables.NMPCcycles_expected/server.getCpuForHypotheticalNbrUAV(i)
                #print("Potential after DC", DC.ID, "Iterated", i, "times: " , potential)
        #print("Potential after step 1: ", potential)
        for UAV in self.aUAVs:
            if UAV.strategy == 0:
                potential -= global_variables.NMPCcycles_expected/UAV.cpuCapacity
        #print("Potential after step 2: ", potential)
        for UAV in self.aUAVs:
            if UAV.strategy != 0:
                potential -= UAV.serverInfo[1]/UAV.weight #Important with weight for weighted potential function!!!
        #print("Potential after step 3: ", potential)
        return potential
    
    """
    Plots the value of the potential function over time.
    """
    def plotPotentialFunction(self):
        plt.plot(self.timeVec,self.potentialValuesPerTime, label="Potential Function Value", linewidth=1.5)
        for xVal in self.convergeTimes:
            plt.axvline(xVal, color = 'r',label="Game Converged to Solution" if xVal == self.convergeTimes[0] else "", linewidth = 0.5)

        for xVal in self.startOfaNewGameTimes:
            plt.axvline(xVal, color = 'g',label="Start of a new Game" if xVal == self.startOfaNewGameTimes[0] else "", linewidth = 0.5)

        plt.xlabel("Time (seconds)")
        plt.ylabel("Value of potential function")
        plt.title("Potential Function")
        plt.legend()
        plt.draw()
        

    """
    Get total number of strategy updates
    """
    def nbrStrategyUpdates(self):
        sumUpdates = 0
        for UAV in self.aUAVs:
            sumUpdates += UAV.nbrStrategyUpdates
        return sumUpdates
    
    """
    Get total number of strategy updates
    """
    def nbrNmpcExecutions(self):
        sumExecutions = 0
        for UAV in self.aUAVs:
            sumExecutions += UAV.nbrNMPCexecutions
        return sumExecutions
    
    """
    Get average time to finish a task.
    """
    def avgTaskTime(self):
        totTime = 0
        for UAV in self.aUAVs:
            totTime = totTime + -1*UAV.U()
        return totTime/len(self.aUAVs)

    """
    Plot number of strategy updates
    """
    def plotNbrOfStrategyUpdates(self):
        aNbrNMPCexecutions = []
        aUpdates = []
        aX1 = []
        aX2 = []
        sumUpdates=self.nbrStrategyUpdates()
        width = 0.5
        i=1
        for UAV in self.aUAVs:
            aX1.append(i-width/3)
            aX2.append(i+width/3)
            aUpdates.append(UAV.nbrStrategyUpdates)
            aNbrNMPCexecutions.append(UAV.nbrNMPCexecutions)
            i+=1
    
        fig, ax1 = plt.subplots()
        
        color = 'tab:red'
        titleStr = 'Total nbr of Strategy Updates:' + str(sumUpdates) + ', average:' + str(round(sumUpdates/i,1))
        ax1.set_title(titleStr)
        ax1.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        ax1.bar(aX1,aUpdates,width,color=color)
        ax1.set_xlabel("Drone ID")
        ax1.set_ylabel("Number of strategy updates", color=color)
        ax2 = ax1.twinx()
        color = 'tab:blue'
        ax2.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        ax2.bar(aX2,aNbrNMPCexecutions,width,color=color)
        ax2.set_xlabel("Drone ID")
        ax2.set_ylabel("Number of NMPC executions", color=color)
        fig.tight_layout()
        plt.draw()
        plt.show(block=False)
        plt.pause(3)

    """
    Calculates number of devices that are computing local/edge/cloud.
    """
    def calculateNbrLocalEdgeCloud(self):
        localUAVs=0
        cloudUAVs=0
        edgeUAVs=0
        for UAV in self.aUAVs:
            # UAV.printInfo()
            if UAV.strategy == 0:
                localUAVs += 1
            else:
                if UAV.serverInfo[0].type == "edge":
                    edgeUAVs += 1
                elif UAV.serverInfo[0].type == "cloud":
                    cloudUAVs += 1
                else:
                    raise NameError("Error when counting UAVs in edge/cloud. Type not found.")
        return localUAVs, edgeUAVs, cloudUAVs

    """
    Prints most info from the system.
    """
    def printAllInfo(self):
        print("Information requested:")
        localUAVs, edgeUAVs, cloudUAVs = self.calculateNbrLocalEdgeCloud()
        for antenna in self.aAntennas:
            antenna.printInfo()
        for server in self.aServers:
            server.printInfo()
        print("Number of UAVs that compute locally: ", localUAVs)
        print("Number of UAVs that compute on an edge server: ", edgeUAVs)
        print("Number of UAVs that compute on a cloud server: ", cloudUAVs)
        print("End of information.")