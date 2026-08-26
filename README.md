# variational-quantum-algorithms
A research-oriented implementation and experimental study of VQE and QAOA under NISQ constraints.
--------------------------------------------------
# overview 
 This repository provides a modular, extensible framework to investigate how hybrid quantum-classical optimization loops behave across ideal simulators, noisy environments, and different classical optimizers.

The primary case study implemented here solves the **Max-Cut combinatorial optimization problem** using QAOA, backed by modular architecture designed for easy expansion to VQE and other NISQ benchmarks.
--------------------------------------------------

*How do variational quantum algorithms perform under NISQ constraints, and how do circuit depth, shot noise, and the choice of classical optimizer affect convergence and solution quality?*
--------------------------------------------------

# Project Architecture

variational-quantum-algorithms/
├── src/
│   ├── problems/        # Classical problems & graph encodings (e.g., Max-Cut)
│   ├── algorithms/      # QAOA and VQE circuit ansätze
│   ├── optimizers/      # Classical optimization wrappers (COBYLA, SPSA, Nelder-Mead)
│   ├── noise/           # NISQ noise models & error simulation
│   └── evaluation/      # Approximation ratio & convergence metrics
├── experiments/         # Scripts running benchmark experiments & generating plots
├── results/             # Generated figures, logs, and experimental data
├── notebooks/           # Jupyter notebooks for interactive walkthroughs & visualizations
├── requirements.txt
├── LICENSE
└── README.md
-------------------------------------------------------------------------
Open your terminal (or command prompt) and clone the repository you just created on GitHub to your computer:
Bash

git clone https://github.com/YOUR_USERNAME/variational-quantum-algorithms.git
cd variational-quantum-algorithms

(Make sure to replace YOUR_USERNAME with your actual GitHub username.)
Step 2: Create a Python Virtual Environment

A virtual environment keeps your project packages isolated from your global Python installation. Run the following command inside your project folder:

For Windows:
    Bash

    python -m venv venv

Step 3: Activate the Virtual Environment

Before installing anything, you must activate the environment. You'll know it worked because your terminal prompt will change to show (venv).

For Windows (Command Prompt):
DOS

venv\Scripts\activate.bat

Step 4: Upgrade Pip and Install Dependencies

Now that your virtual environment is active, ensure your package installer (pip) is up to date, then install the core libraries (qiskit, numpy, scipy, matplotlib, and jupyter):
Bash

python -m pip install --upgrade pip
pip install qiskit numpy scipy matplotlib jupyter

Step 5: Save Your requirements.txt

To make your repository reproducible for anyone (or an admissions committee) checking out your code, freeze your current package versions into a requirements.txt file:
Bash

pip freeze > requirements.txt

You can then add, commit, and push this file to GitHub:
Bash

git add requirements.txt
git commit -m "Add requirements.txt with core quantum and scientific dependencies"
git push origin main

-------------------------------------------------------------
Before writing any code, getting the mathematics right is what separates a surface-level tutorial from a rigorous Master's-level portfolio project.
Let's break down Max-Cut and how we translate a graph-theory problem into a quantum mechanical operator (the Cost Hamiltonian).
Step 1: What is Max-Cut?
Imagine you have an undirected graph G = (V, E), where $V$ is the set of vertices (nodes) and $E$ is the set of edges connecting them.

The Max-Cut problem asks:
Can we partition the vertices V into two disjoint sets, say S and V \setminus S$, such that the number of edges bridging (crossing) between the two sets is maximized?

For a small 4-node graph ($A, B, C, D$):
If node $A$ and $C$ are in Group 1, and $B$ and $D$ are in Group 2, any edge connecting a node from Group 1 to Group 2 counts as a "cut."
Step 2: The Classical Cost Function
To write this mathematically, let's assign a binary variable $z_i$ to each vertex $i \in V$:$z_i = +1$ if vertex $i$ belongs to 
Group 1.$z_i = -1$ if vertex $i$ belongs to 

Group 2.Now, consider an edge $(i, j) \in E$ connecting vertex $i$ and vertex
 $j$:If $i$ and $j$ are in the same group, 
 $z_i z_j = (+1)(+1) = +1$ or $(-1)(-1) = +1$
 .If $i$ and $j$ are in different groups, 
 $z_i z_j = (+1)(-1) = -1$.
 This gives us a clever trick to check if an edge is 
 
cut: the quantity $\frac{1 - z_i z_j}{2}$ evaluates to 1 if the edge is cut, and 0 if it is not.


Connecting the Graph to the EquationIn the graph above, every node is assigned a color (representing Group 1 or Group 2):Red Nodes correspond to spins or variables where $z_i = +1$.Blue Nodes correspond to variables where $z_j = -1$.When you look at an edge connecting a red node to a blue node (for example, node 4 connected to node 1 or 0), that edge bridges the two partitions.Mathematically, for that edge:$$z_i z_j = (+1)(-1) = -1$$Plugging this into our cost term:$$\frac{1 - z_i z_j}{2} = \frac{1 - (-1)}{2} = \frac{2}{2} = 1$$This confirms the edge is successfully cut, contributing $+1$ to our total objective value.Conversely, if an edge connects two red nodes or two blue nodes:$$z_i z_j = (+1)(+1) = +1 \quad \text{or} \quad (-1)(-1) = +1$$$$\frac{1 - 1}{2} = 0$$This means the edge is not cut, contributing $0$ to the total.What QAOA Does with This GraphWhen we build the QAOA circuit for this problem:The Cost Hamiltonian ($H_C$) assigns a phase penalty or reward based on how many edges satisfy this condition across all qubits.The Mixer Hamiltonian ($H_B$) uses transverse Pauli-X operators ($\sum \hat{X}_i$) to explore different color configurations (flipping red nodes to blue and vice-versa).The classical optimizer tunes $\gamma$ and $\beta$ to maximize the probability that when we measure the qubits at the end, we land on the partition with the highest possible number of bridging edges.