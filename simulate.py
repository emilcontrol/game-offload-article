import sys
import json

from src.resourceGame.GreatGame import GreatGame

if len(sys.argv) != 6:
    raise ImportError("Usage: Wrong number of arguments")

v_nUAVs = int(sys.argv[1])
v_nAntennas = int(sys.argv[2])
v_nEdgeServers = int(sys.argv[3])
v_nCloudServers = int(sys.argv[4])
output_filename = str(sys.argv[5])

Spelet = GreatGame(nUAVs=v_nUAVs, nAntennas=v_nAntennas, nEdgeServers=v_nEdgeServers, nCloudServers = v_nCloudServers)
simulationResults = Spelet.runSequence(plotOption=0,printOption=0)

simulationResults['nDevices'] = v_nUAVs
simulationResults["nAntennas"] = v_nAntennas
simulationResults["nEdgeServers"] = v_nEdgeServers
simulationResults["nCloudServers"] = v_nCloudServers

output_data = {
    "nDevices": v_nUAVs,
    "nAntennas": v_nAntennas,
    "nEdgeServers": v_nEdgeServers,
    "nCloudServers": v_nCloudServers,
    "results": simulationResults
}

with open(output_filename, "w") as f:
    json.dump(simulationResults, f)

print("Converged:", simulationResults['hasConverged'] , ", Results written to", output_filename)