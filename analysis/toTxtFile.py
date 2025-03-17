import glob
import json
from matplotlib import pyplot as plt
import os
import numpy as np

# Load all JSON files in the results folder
all_data = []

folderName = "secondPaperIteration"

for filename in glob.glob('results/'+folderName+"/*.json"):
    with open(filename, "r") as f:
        data = json.load(f)
        all_data.append(data)

def getlistFromLabel(label, all_d):
    l = []
    for d in all_d:
        l.append(d[label])
    return l

devices = getlistFromLabel('nDevices',all_data)
avgTaskTimeInit = getlistFromLabel('avgTaskTimeInit',all_data)
avgTaskTime = getlistFromLabel('avgTaskTime',all_data)
strategyUpdates = getlistFromLabel('nbrStrategyUpdates',all_data)
strategyUpdatesPerDevice = getlistFromLabel('nbrStrategyUpdatesPerDevice',all_data)
edgeServers = getlistFromLabel('nEdgeServers',all_data)
cloudServers = getlistFromLabel('nCloudServers',all_data)
antennas = getlistFromLabel('nAntennas',all_data)

# Data structure to fill with simulation data
dataToPlot_tot = dict()
dataToPlot_perDevice = dict()
dataToPlot_avgTaskTimeInit = dict()
dataToPlot_avgTaskTime = dict()

# Finding the different test cases
for e in set(edgeServers):
    for c in set(cloudServers):
        for a in set(antennas):
            dataToPlot_tot[(e,c,a)] = []
            dataToPlot_perDevice[(e,c,a)] = []
            dataToPlot_avgTaskTimeInit[(e,c,a)] = []
            dataToPlot_avgTaskTime[(e,c,a)] = []

# Adding data to the case-indexed dicts
for i in range(1,len(devices)):
    dataToPlot_tot[(edgeServers[i], cloudServers[i], antennas[i])].append([devices[i],strategyUpdates[i]])
    dataToPlot_perDevice[(edgeServers[i], cloudServers[i], antennas[i])].append([devices[i],strategyUpdatesPerDevice[i]])
    dataToPlot_avgTaskTimeInit[(edgeServers[i], cloudServers[i], antennas[i])].append([devices[i],avgTaskTimeInit[i]])
    dataToPlot_avgTaskTime[(edgeServers[i], cloudServers[i], antennas[i])].append([devices[i],avgTaskTime[i]])


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




# Define output directory
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, 'TxtOutputs/'+folderName)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Add and write total strategy updates to txt file
for key,val in dataToPlot_tot.items():
    deviceKeyDict = getDictWithDevicesAsKey(val,setDevices)
    meanAndStdlist = getMeanAndStdDevFromDict(deviceKeyDict)
    fileName = str(key[0]) + 'edge' + str(key[1]) + 'cloud' + str(key[2]) + 'cells_nbrStrategyUpdates.txt'
    with open(os.path.join(output_dir, fileName), "w") as file:
        # Writing the header row for tot updates
        file.write("nDevices,nbrStrategyUpdates,stdDev\n")

        x_values_std = [x[0] for x in meanAndStdlist]
        y_values_std = [x[1] for x in meanAndStdlist]
        std = [x[2] for x in meanAndStdlist]

        # Writing the data rows
        for i in range(0,len(x_values_std)):
            file.write(",".join(map(str, [x_values_std[i],y_values_std[i],std[i]])) + "\n")

# Add and write total strategy updates per device to txt file
for key,val in dataToPlot_perDevice.items():
    deviceKeyDict = getDictWithDevicesAsKey(val,setDevices)
    meanAndStdlist = getMeanAndStdDevFromDict(deviceKeyDict)
    fileName = str(key[0]) + 'edge' + str(key[1]) + 'cloud' + str(key[2]) + 'cells_nbrStrategyUpdatesPerDevice.txt'
    with open(os.path.join(output_dir, fileName), "w") as file:
        # Writing the header row for tot updates
        file.write("nDevices,nbrStrategyUpdatesPerDevice,stdDev\n")
        x_values_std = [x[0] for x in meanAndStdlist]
        y_values_std = [x[1] for x in meanAndStdlist]
        std = [x[2] for x in meanAndStdlist]
        # Writing the data rows
        for i in range(0,len(x_values_std)):
            file.write(",".join(map(str, [x_values_std[i],y_values_std[i],std[i]])) + "\n")


# Add and write initial average task time value to txt file
for key,val in dataToPlot_avgTaskTimeInit.items():
    # x-values
    nbrDevices = [inner[0] for inner in val]
    # The difference here will be the y-values
    avgTimeInit = [inner[1] for inner in val]
    avgTime = [inner[1] for inner in dataToPlot_avgTaskTime[key]]

    # Calculating the difference between before and after
    #y = []
    #x = []
    data = []
    for i in range(0,len(nbrDevices)):
        data.append([nbrDevices[i], avgTimeInit[i] - avgTime[i]])
        #y.append(avgTimeInit[i]-avgTime[i])
        #x.append(nbrDevices[i])
    deviceKeyDict = getDictWithDevicesAsKey(data,setDevices)
    meanAndStdlist = getMeanAndStdDevFromDict(deviceKeyDict)
    x_values_std = [x[0] for x in meanAndStdlist]
    y_values_std = [x[1] for x in meanAndStdlist]
    std = [x[2] for x in meanAndStdlist]

    fileNameTotDevices = str(key[0]) + 'edge' + str(key[1]) + 'cloud' + str(key[2]) + 'cells_avgTaskTimeDiff.txt'
    with open(os.path.join(output_dir, fileNameTotDevices), "w") as file:
        # Writing the header row for tot updates
        file.write("nDevices,avgTaskTimeDiff,stdDev\n")
        # Writing the data rows
        for i in range(0,len(x_values_std)):
            file.write(",".join(map(str, [x_values_std[i],y_values_std[i],std[i]])) + "\n")


