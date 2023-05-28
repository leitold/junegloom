#!/usr/bin/env python3

import numpy as np

from pypotts.simulation import mc_step
from pypotts.visualization import plot_grid


Q_SIM = 6
TEMPERATURE = 1.2
BETA = 1.0 / TEMPERATURE

M_GRID = 10
N_GRID = 22
N_PASS = 100


if __name__ == '__main__':
    grid = np.zeros([M_GRID, N_GRID], dtype=np.int8)

    for i in range(N_PASS):
        for j in range(M_GRID * N_GRID):
            accept = mc_step(grid, Q_SIM, BETA, M_GRID, N_GRID)

    plot_grid(grid, Q_SIM, M_GRID, N_GRID)
