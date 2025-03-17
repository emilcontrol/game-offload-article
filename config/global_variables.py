# Global variables

# This one dividing NMPCcycles_expected to get vmax in the article.
cpuEdge = 50000000000 #ÄNDRAD! Ta bort en nolla! #10GHz to share on the edge. 10^10

cpuCloudPerUAV = 20000000000 #20GHz in cloud for each UAV. 2*10^10. Note that to get v_c from the paper, NMPCcycles_expected is
# divided by this number.

cpuLocal=2000000000 #2GHz (cpu cycles per second for drone. (jetson nano CPU has 1.4GHz))2*10^9
cpuLocalPlusMinus=1000000000 #1000000000 #Variance between units

v_l_min = 0.05 #local minimal time for nominal task.
v_l_max = 0.15 #local maximum time for nominal task.

NMPCcycles_expected = 200000000 #Expected Cpu cycles to perform a NMPC calculation. 2*10^8
NMPCcycles_expected_weightFactor_min = 1 # uniform distribution min to max in weight of cycles
NMPCcycles_expected_weightFactor_max = 2 # uniform distribution min to max in weight of cycles
NMPCcyclesPlusMinus=50000000 #optimizion steps required will vary a bit, even if not expected.

avgRTT_edge=0.02 #Average RTT from antenna to Edge server
RTTPlusMinus_edge=0.01 #Uniform distribution with this value representing the min/max deviation from avgRTT_edge

avgRTT_cloud=0.1 #Average RTT from antenna to Cloud server
RTTPlusMinus_cloud=0.02 #Uniform distribution with this value representing the min/max deviation from avgRTT_cloud

tImprovementReq = 0.05 #Required improvement (percent/100) in time for device to update strategy

edgeServersPerAntenna = 5 # The amount of servers each device shall reach
cloudServersPerAntenna = 1