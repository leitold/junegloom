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

PARAMETER_RANGE_STEPS = 4000


def plot_grid_and_return_tiles(s, axes):
    all_tiles = []

    colors = vis_colors[Q_SIM]
    for i in range(M_GRID):
        for j in range(N_GRID):
            x = tile_x + 2 * i
            y = tile_y + j

            current_tile = axes[0].fill(x, y, color=colors[s[i, j]], animated=True)[0]

            all_tiles.append(current_tile)

    axes[0].axis('off')
    axes[0].set_aspect('equal')
    axes[0].set_xlim([0.0, 2.0 * M_GRID])
    axes[0].set_ylim([2.0, 1.0 * N_GRID])

    parameter_plot = axes[1].plot(parameter_x, parameter_y, animated=True)[0]
    parameter_dot = axes[1].plot([0.0], [1.0], 's', animated=True)[0]

    axes[1].set_ylim([0.45 * TEMPERATURE, 1.55 * TEMPERATURE])
    axes[1].grid(visible=True)

    all_tiles.append(parameter_plot)
    all_tiles.append(parameter_dot)

    return all_tiles


def animate_potts_grid(parameter_index):
    if parameter_index <= 0:
        current_temperature = TEMPERATURE * (1.25 + 0.5 * parameter_index / PARAMETER_RANGE_STEPS)
    else:
        current_temperature = TEMPERATURE * (1.25 - 0.5 * parameter_index / PARAMETER_RANGE_STEPS)

    current_beta = 1.0 / current_temperature

    colors = vis_colors[Q_SIM]
    for i in range(M_GRID):
        for j in range(N_GRID):
            tile_index = i * N_GRID + j
            all_tiles[tile_index].set_color(colors[grid[i, j]])

    n_accept = 0
    for i in range(N_UPDATE_STEPS):
        accept = mc_step(grid, Q_SIM, current_beta, False, M_GRID, N_GRID)
        if accept:
            n_accept += 1
    print(f'{parameter_index:4d} {current_temperature:8.4f} acceptance ratio: {n_accept / N_UPDATE_STEPS:.3f}')

    parameter_y[PARAMETER_RANGE_STEPS + parameter_index] = current_temperature
    all_tiles[-2].set_ydata(parameter_y)

    all_tiles[-1].set_xdata([parameter_x[PARAMETER_RANGE_STEPS + parameter_index]])
    all_tiles[-1].set_ydata([current_temperature])

    return all_tiles


if __name__ == '__main__':
    grid = np.zeros([M_GRID, N_GRID], dtype=np.int8)

    parameter_x = np.arange(2 * PARAMETER_RANGE_STEPS)
    parameter_y = np.zeros(2 * PARAMETER_RANGE_STEPS)
    # randomize_grid(grid, Q_SIM, M_GRID, N_GRID)

    fig, axes = plt.subplots(nrows=2, height_ratios=[4, 1])

    all_tiles = plot_grid_and_return_tiles(grid, axes)

    # Interval is the time between animation updates in ms. Set to larger value to slow everything down.
    ani = animation.FuncAnimation(
        fig,
        animate_potts_grid,
        range(-PARAMETER_RANGE_STEPS, PARAMETER_RANGE_STEPS),
        interval=0, blit=True,
        repeat=True,
    )

    plt.show()
