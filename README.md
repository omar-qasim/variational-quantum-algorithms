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
