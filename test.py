from src.resourceGame.GreatGame import GreatGame

# Try the system.
Spelet = GreatGame(nUAVs=1500, nAntennas=10, nEdgeServers=20, nCloudServers = 2)
Spelet.runSequence(plotOption=2, printOption=1)