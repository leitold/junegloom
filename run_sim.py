#!/usr/bin/env python3

import numpy as np

import matplotlib.pyplot as plt

from pottsmodel.simulation import mc_step, randomize_grid
from pottsmodel.visualization import plot_grid, save_figure

# Variable names roughly follow https://en.wikipedia.org/wiki/Potts_model
# Set q (number of spin directions), temperature, and grid size.
Q_SIM = 6
TEMPERATURE = 1.25
BETA = 1.0 / TEMPERATURE

# Grid size. For a square picture, set N = 2M + 2.
M_GRID = 10
N_GRID = 22
# Number of Monte Carlo passes. One pass is NxM atomic moves.
N_PASS = 1000


if __name__ == '__main__':
    grid = np.zeros([M_GRID, N_GRID], dtype=np.int8)
    randomize_grid(grid, Q_SIM, M_GRID, N_GRID)
    plot_grid(grid, Q_SIM, M_GRID, N_GRID)
    save_figure('01_random', grid)

    for i in range(N_PASS):
        for j in range(M_GRID * N_GRID):
            accept = mc_step(grid, Q_SIM, BETA, False, M_GRID, N_GRID)

    plt.figure()
    plot_grid(grid, Q_SIM, M_GRID, N_GRID)
    save_figure('02_regular_interaction', grid)

    for i in range(N_PASS):
        for j in range(M_GRID * N_GRID):
            accept = mc_step(grid, Q_SIM, BETA, True, M_GRID, N_GRID)

    plt.figure()
    plot_grid(grid, Q_SIM, M_GRID, N_GRID)
    save_figure('03_inverted_interaction', grid)
