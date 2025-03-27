# Software used in the Game-Offload Article
The code used to generate the figures in the game theory-offloading article ("Scalable Orchestration of Dynamic 6G Control Computations"). The program is mainly written in python and the purpose of this repository is to let the interested reader both replicate the paper results and play around in the simulation with different conditions.

## Abstract (from the associated article)
In this work, by focusing on scalability rather than optimality, a decentralized resource allocation policy for control computations is proposed. It is showed that this policy is guaranteed to converge to a satisfactory solution when the devices only have information about available computational resources on a few close servers. It is also shown that the worst- case number of strategy updates scales linearly with the number of agents, even if the devices are distributed over different network cells and the system includes numerous servers. Finally, the linear convergence behavior is also shown in simulation, where the simulation code is provided to the reader.


## Requirements
* Python (3.11.5 was used to generate the figures in the article)
* xargs - Standard tool on most Unix-like systems. Used to speed up the simulations.
### Python Libraries Used
* sys (standard library)2.0.9
* json (2.0.9 was used to generate the figures in the article)
* numpy (1.24.3 was used to generate the figures in the article)
* random (standard library)
* matplotlib (3.7.2 was used to generate the figures in the article)
* abc (standard library)
* math (standard library)
* glob (standard library)
* os (standard library)

# Quick Start
1. Install Python (preferably ) and required libraries
2. Clone this repository and navigate to its root dorectory
3. Make the script "run_all.sh" runnable: "chmod +x run_all.sh"
4. Run the script "./run_sll.sh"
5. Generate matplotlib-figures: "python analysis/convergenceTimes.py"
6. Generate txt-files from the simulation results: "python analysis/toTxtFile.py"

## Test-file
The file test.py sets up one instance of the game based on a specific setup and runs it. It also plots the potential function over time and the number of strategy updates for the different devices. To run the test file, type "python test.py" in the terminal.