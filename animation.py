#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

from pottsmodel.simulation import mc_step, randomize_grid
from pottsmodel.visualization import vis_colors, tile_x, tile_y

# Variable names roughly follow https://en.wikipedia.org/wiki/Potts_model
# Set q (number of spin directions), temperature, and grid size.
Q_SIM = 6
TEMPERATURE = 1.25
BETA = 1.0 / TEMPERATURE

# Grid size. For a square picture, set N = 2M + 2.
M_GRID = 10
N_GRID = 20
# Number of Monte Carlo steps between animation updates. One step = one attempted atomic move.
N_UPDATE_STEPS = 100


def plot_grid_and_return_tiles(s, ax):
    all_tiles = []

    colors = vis_colors[Q_SIM]
    for i in range(M_GRID):
        for j in range(N_GRID):
            x = tile_x + 2 * i
            y = tile_y + j

            current_tile = ax.fill(x, y, color=colors[s[i, j]], animated=True)[0]

            all_tiles.append(current_tile)

    ax.axis('off')
    ax.set_aspect('equal')
    ax.set_xlim([0.0, 2.0 * M_GRID])
    ax.set_ylim([2.0, 1.0 * N_GRID])

    return all_tiles


def animate_potts_grid(parameter_index):
    colors = vis_colors[Q_SIM]
    for i in range(M_GRID):
        for j in range(N_GRID):
            tile_index = i * N_GRID + j
            all_tiles[tile_index].set_color(colors[grid[i, j]])

    n_accept = 0
    for i in range(N_UPDATE_STEPS):
        accept = mc_step(grid, Q_SIM, BETA, False, M_GRID, N_GRID)
        if accept:
            n_accept += 1
    print(f'{parameter_index:2d} acceptance ratio: {n_accept / N_UPDATE_STEPS:.3f}')

    return all_tiles


if __name__ == '__main__':
    grid = np.zeros([M_GRID, N_GRID], dtype=np.int8)
    # randomize_grid(grid, Q_SIM, M_GRID, N_GRID)

    axis = plt.gca()
    fig = plt.gcf()

    all_tiles = plot_grid_and_return_tiles(grid, axis)

    # Interval is the time between animation updates in ms. Set to larger value to slow everything down.
    ani = animation.FuncAnimation(
        fig, animate_potts_grid, range(1, 20), interval=10, blit=True, repeat=True,
    )

    plt.show()