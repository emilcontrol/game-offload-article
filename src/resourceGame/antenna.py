import random as rnd
from config import global_variables
"""
    Antenna class. 
    Acts as internet. Connects UAVS and data centers.
"""
class Antenna:
    def __init__(self,ID):
        self.serverInfo=[] # [server,RTT]
        self.ID=ID

    # Connect to one server
    def connectToAllServers(self,aServers):
        for server in aServers:
            self.connectToOneServer(server);    
    
    # Connect to N random edge servers
    def connectToNRandomEdgeServers(self, aServers, n):
        try: 
            Nservers = rnd.sample([a for a in aServers if a.type == "edge"], k=n)
        except ValueError:
            print("N (the numbers of edge servers the antenna connects to) is higher than amount of edge servers")

        for server in Nservers:
            self.connectToOneServer(server)

    # Connect to M random cloud servers
    def connectToMRandomCloudServers(self, aServers, m):
        try: 
            Mservers = rnd.sample([a for a in aServers if a.type == "cloud"], k=m)
        except ValueError:
            print("M (the numbers of cloud servers the antenna connects to) is higher than amount of cloud servers.")
        for server in Mservers:
            self.connectToOneServer(server)

    # Does the actual connection to the server and sets the RTT
    def connectToOneServer(self, server):
        if server.type == "edge":
            RTT = rnd.uniform(global_variables.avgRTT_edge + global_variables.RTTPlusMinus_edge, 
                            global_variables.avgRTT_edge - global_variables.RTTPlusMinus_edge)
            self.serverInfo.append([server,RTT])
        elif server.type == "cloud":
            RTT = rnd.uniform(global_variables.avgRTT_cloud + global_variables.RTTPlusMinus_cloud, 
                            global_variables.avgRTT_cloud - global_variables.RTTPlusMinus_cloud)
            self.serverInfo.append([server,RTT])
        else:
            raise NameError("Unknown type of server.")

    def getServerInfo(self):
        return self.serverInfo
    
    def getListOfServerIDs(self):
        IDlist=[]
        for Serverinf in self.serverInfo:
            IDlist.append([Serverinf[0].ID, Serverinf[1]])
        return IDlist
    
    def printInfo(self):
        print("This is Antenna", self.ID, ". Found these servers: ", self.getListOfServerIDs())
