#!/bin/bash

nDEVICES=(50 100 150 200 300 400 500 600 700 800 900 1000 1100 1200 1300 1400 1500 1600 1700 1800 1900 2000)
#nDEVICES=(10 50 100 200 500 700)
nANTENNAS=(10 100)
nEDGESERVERS=(20 70)
nCLOUDSERVERS=(2)
nRepetitions=10

mkdir -p results/secondPaperIteration

echo "Starting the loop in the bash script. Params: ${PARAMETERS[@]}"

> commands.txt
for ((i = 1; i <= nRepetitions; i++)); do
    for nDEV in "${nDEVICES[@]}"; do
        for nEDGE in "${nEDGESERVERS[@]}"; do
            for nANT in "${nANTENNAS[@]}"; do
                for nCLOUD in "${nCLOUDSERVERS[@]}"; do
                    #echo "Starting Simulation with $nDEV mobile devices and $nEDGE edge servers."
                    echo "python simulate.py "$nDEV" "$nANT" "$nEDGE" "$nCLOUD" "results/secondPaperIteration/${nDEV}agents_${nEDGE}edgeservers_${nANT}antennas_${nCLOUD}cloudservers_${i}.json""
                done
            done
        done
    done
done >> commands.txt

xargs -P 4 -I CMD bash -c CMD < commands.txt

echo "Done."