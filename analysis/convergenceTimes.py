import glob
import json
from matplotlib import pyplot as plt
import numpy as np

# Load all JSON files in the results folder
folderName = "secondPaperIteration"

all_data = []
for filename in glob.glob("results/"+folderName+"/*.json"):
    with open(filename, "r") as f:
        data = json.load(f)
        all_data.append(data)

def getlistFromLabel(label, all_d):
    l = []
    for d in all_d:
        l.append(d[label])
    return l

devices = getlistFromLabel('nDevices',all_data)
strategyUpdates = getlistFromLabel('nbrStrategyUpdates',all_data)
strategyUpdatesPerDevice = getlistFromLabel('nbrStrategyUpdatesPerDevice',all_data)
avgTaskTimeInit = getlistFromLabel('avgTaskTimeInit',all_data)
avgTaskTime = getlistFromLabel('avgTaskTime',all_data)
edgeServers = getlistFromLabel('nEdgeServers',all_data)
cloudServers = getlistFromLabel('nCloudServers',all_data)
antennas = getlistFromLabel('nAntennas',all_data)

dataToPlot_tot = dict()
dataToPlot_perDevice = dict()
dataToPlot_avgTaskTimeInit = dict()
dataToPlot_avgTaskTime = dict()


for e in set(edgeServers):
    for c in set(cloudServers):
        for a in set(antennas):
            dataToPlot_tot[(e,c,a)] = []
            dataToPlot_perDevice[(e,c,a)] = []
            dataToPlot_avgTaskTimeInit[(e,c,a)] = []
            dataToPlot_avgTaskTime[(e,c,a)] = []

#for case in set(cases): # Create a set where keys are simulation cases
#    dataToPlot_tot[case] = []
#    dataToPlot_perDevice[case] = []
for i in range(1,len(devices)):
    dataToPlot_tot[(edgeServers[i], cloudServers[i], antennas[i])].append([devices[i],strategyUpdates[i]])
    dataToPlot_perDevice[(edgeServers[i], cloudServers[i], antennas[i])].append([devices[i],strategyUpdatesPerDevice[i]])
    dataToPlot_avgTaskTimeInit[(edgeServers[i], cloudServers[i], antennas[i])].append([devices[i],avgTaskTimeInit[i]])
    dataToPlot_avgTaskTime[(edgeServers[i], cloudServers[i], antennas[i])].append([devices[i],avgTaskTime[i]])


# To calculate mean and std deviation, all data points from same setup must be taken out.
# For that we need the set of ndevices.

# Get a dict of a configuration (edges, cells) where keys are number of devices
# and values are lists of data points
setDevices = set(devices)
def getDictWithDevicesAsKey(data,newKey): #Data shall be list of [n,x] and dividerVar set
    dividerDict = dict()
    #Create a dict with number of devices as key. Fill with data points later.
    for d in newKey:
        dividerDict[d] = []
    #Fill this dict with the data.
    for pair in data:
        dividerDict[pair[0]].append(pair[1])
    return dividerDict
    
# Returns a dict of means and standard deviations for data in the returned format from 
# the function getDictWithDevicesAsKey().
def getMeanAndStdDevFromDict(DictWithDevicesAsKey):
    meanAndStdLists = []
    for key,val in DictWithDevicesAsKey.items():
        meanAndStdList = [key,np.mean(val),np.std(val)]
        meanAndStdLists.append(meanAndStdList)
    return meanAndStdLists

"""
deviceKeyDict = getDictWithDevicesAsKey(dataToPlot_tot,setDevices)
print(deviceKeyDict)
print('...')
meanAndStdDict = getMeanAndStdDevFromDict(deviceKeyDict)
print(meanAndStdDict)
"""


fig1, ax1 = plt.subplots()

for key,val in dataToPlot_tot.items():
    deviceKeyDict = getDictWithDevicesAsKey(val,setDevices)
    meanAndStdlist = getMeanAndStdDevFromDict(deviceKeyDict)
    #x_values = [inner[0] for inner in val]
    #y_values = [inner[1] for inner in val]
    #ax1.plot(x_values, y_values, '*', label=str(key), markersize=10)
    x_values_std = [x[0] for x in meanAndStdlist]
    y_values_std = [x[1] for x in meanAndStdlist]
    std = [x[2] for x in meanAndStdlist]
    ax1.errorbar(x_values_std, y_values_std, std,fmt='o',capsize=6,label=str(key))
ax1.legend()
ax1.set_title("Total Nbr of Strategy Updates", fontsize= 20)
ax1.set_xlabel("Nbr of devices", fontsize = 15)
ax1.set_ylabel("Nbr of strategy updates", fontsize = 15)
ax1.set_xbound(0)
ax1.set_ybound(0)
ax1.grid()

fig2, ax2 = plt.subplots()

for key,val in dataToPlot_perDevice.items():
    deviceKeyDict = getDictWithDevicesAsKey(val,setDevices)
    meanAndStdlist = getMeanAndStdDevFromDict(deviceKeyDict)
    #x_values = [inner[0] for inner in val]
    #y_values = [inner[1] for inner in val]
    #ax2.plot(x_values, y_values, '*', label=str(key), markersize=10)
    x_values_std = [x[0] for x in meanAndStdlist]
    y_values_std = [x[1] for x in meanAndStdlist]
    std = [x[2] for x in meanAndStdlist]
    ax2.errorbar(x_values_std, y_values_std, std,fmt='o',capsize=6,label=str(key))
ax2.legend()
ax2.set_title("Total Nbr of Strategy Updates per Device", fontsize = 20)
ax2.set_xlabel("Nbr of devices", fontsize = 15)
ax2.set_ylabel("Nbr of strategy updates per device", fontsize = 15)
ax2.set_xbound(0)
ax2.set_ybound(0)
ax2.grid()

fig3, ax3 = plt.subplots()

for key,val in dataToPlot_avgTaskTimeInit.items():
    deviceKeyDict = getDictWithDevicesAsKey(val,setDevices)
    meanAndStdlist = getMeanAndStdDevFromDict(deviceKeyDict)
    #x_values = [inner[0] for inner in val]
    #y_values = [inner[1] for inner in val]
    #ax3.plot(x_values, y_values, '*', label=str(key), markersize=10)
    x_values_std = [x[0] for x in meanAndStdlist]
    y_values_std = [x[1] for x in meanAndStdlist]
    std = [x[2] for x in meanAndStdlist]
    ax3.errorbar(x_values_std, y_values_std, std,fmt='o',capsize=6,label=str(key))
ax3.legend()
ax3.set_title("Average Task Time Before Game", fontsize = 20)
ax3.set_xlabel("Nbr of devices", fontsize = 15)
ax3.set_ylabel("Task Time (s)", fontsize = 15)
ax3.set_xbound(0)
ax3.set_ybound(0)
ax3.grid()

fig4, ax4 = plt.subplots()

for key,val in dataToPlot_avgTaskTime.items():
    deviceKeyDict = getDictWithDevicesAsKey(val,setDevices)
    meanAndStdlist = getMeanAndStdDevFromDict(deviceKeyDict)
    #x_values = [inner[0] for inner in val]
    #y_values = [inner[1] for inner in val]
    #ax4.plot(x_values, y_values, '*', label=str(key), markersize=10)
    x_values_std = [x[0] for x in meanAndStdlist]
    y_values_std = [x[1] for x in meanAndStdlist]
    std = [x[2] for x in meanAndStdlist]
    ax4.errorbar(x_values_std, y_values_std, std,fmt='o',capsize=6,label=str(key))
ax4.legend()
ax4.set_title("Average Task Time After Game", fontsize = 20)
ax4.set_xlabel("Nbr of devices", fontsize = 15)
ax4.set_ylabel("Task Time (s)", fontsize = 15)
ax4.set_xbound(0)
ax4.set_ybound(0)
ax4.grid()


fig5, ax5 = plt.subplots()

for key,val in dataToPlot_avgTaskTime.items():  
    x_values = [inner[0] for inner in val]
    y_values = [inner[1] for inner in val]
    #x_values_Init = [inner[0] for inner in dataToPlot_avgTaskTimeInit[key]]
    y_values_Init = [inner[1] for inner in dataToPlot_avgTaskTimeInit[key]]
    #y = []
    #x = []
    data = []
    for i in range(0,len(y_values)):
        #y.append(y_values_Init[i] - y_values[i])
        #x.append(x_values[i])
        data.append([x_values[i], y_values_Init[i] - y_values[i]])

    deviceKeyDict = getDictWithDevicesAsKey(data,setDevices)
    meanAndStdlist = getMeanAndStdDevFromDict(deviceKeyDict)
    x_values_std = [x[0] for x in meanAndStdlist]
    y_values_std = [x[1] for x in meanAndStdlist]
    std = [x[2] for x in meanAndStdlist]
    ax5.errorbar(x_values_std, y_values_std, std,fmt='o',capsize=6,label=str(key))
    #ax5.plot(x, y, '*', label=str(key), markersize=10)
ax5.legend()
ax5.set_title("Improvement (s)", fontsize = 20)
ax5.set_xlabel("Nbr of devices", fontsize = 15)
ax5.set_ylabel("Task Time Improvement (s)", fontsize = 15)
ax5.set_xbound(0)
ax5.set_ybound(0)
ax5.grid()

plt.show()


