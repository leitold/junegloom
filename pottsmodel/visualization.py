import pickle

import matplotlib.pyplot as plt
import numpy as np

from palettable.colorbrewer.qualitative import Set3_4, Set3_6
from palettable.wesanderson.wesanderson import get_map


vis_colors = {
    4: Set3_4.mpl_colors,
    5: get_map('Aquatic2').mpl_colors,
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


# Modified from https://stackoverflow.com/questions/11837979/removing-white-space-around-a-saved-image
def save_figure(filepath, grid, fig=None):
    '''Save the current image with no whitespace'''
    import matplotlib.pyplot as plt
    if not fig:
        fig = plt.gcf()

    plt.subplots_adjust(0,0,1,1,0,0)
    for ax in fig.axes:
        ax.axis('off')
        ax.margins(0,0)
        ax.xaxis.set_major_locator(plt.NullLocator())
        ax.yaxis.set_major_locator(plt.NullLocator())

    for ext in ['png', 'pdf']:
        fig.savefig(f'{filepath}.{ext}', pad_inches=0, dpi=600, bbox_inches='tight')

    with open(f'{filepath}.pkl', 'wb') as f:
        pickle.dump(grid, f)
