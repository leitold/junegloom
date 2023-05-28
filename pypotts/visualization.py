import matplotlib.pyplot as plt
import numpy as np

from palettable.colorbrewer.qualitative import Set3_6


vis_colors = {
    6: Set3_6.mpl_colors,
}


tile_x = np.array([
    0.0,
    2.0,
    2.0,
    0.0,
])


tile_y = np.array([
    0.0,
    2.0,
    3.0,
    1.0,
])


def plot_grid(s, q, m_grid, n_grid):
    colors = vis_colors[q]
    for i in range(m_grid):
        for j in range(n_grid):
            x = tile_x + 2 * i
            y = tile_y + j
            plt.fill(x, y, color=colors[s[i, j]])

    plt.axis('off')
    plt.gca().set_aspect('equal')
    plt.xlim([0.0, 2.0 * m_grid])
    plt.ylim([2.0, 1.0 * n_grid])
