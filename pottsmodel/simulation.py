import numpy as np


def delta(s1, s2, inverse=False):
    if inverse:
        return 1 - int(s1 == s2)
    else:
        return int(s1 == s2)

def randomize_grid(s, q, m_grid, n_grid):
    for i in range(m_grid):
        for j in range(n_grid):
            s[i, j] = np.random.randint(q, dtype=np.int8)


def mc_step(s, q, beta, inverse, m_grid, n_grid, traditional=False):
    """Main function: perform a single Monte Carlo move (in-place).

    Parameters
    ----------
    s : numpy.array[int, int]
        The spin lattice. This is modified in-place after a successful move.
    q : int
        Number of spin directions.
    inverse : bool
        If set to True, the interaction term is inverted, i.e. like spins are
        energetically worse than unlike ones.
    beta : float
        Thermodynamic beta = 1 / kT.
    m_grid, n_grid: int
        Grid dimensions in x and y direction.
    traditional : bool (default False)
        If set to True, use a regular Potts model with four neighbors, one on
        each side. If False, use modified model with "tilted" interaction, i.e.
        corresponding to where the tiles touch. The interaction is also stronger
        by an asymmetry factor along this second direction.

    Returns
    -------
    accept : bool
        True if trial move was accepted, False otherwise.
    """
    accept = False

    i = np.random.randint(m_grid)
    j = np.random.randint(n_grid)

    ip1 = (i + 1) % m_grid
    im1 = (i - 1) % m_grid
    jp1 = (j + 1) % n_grid
    jm1 = (j - 1) % n_grid
    jp2 = (j + 2) % n_grid
    jm2 = (j - 2) % n_grid

    while True:
        s_new = np.random.randint(q, dtype=np.int8)
        if s_new != s[i, j]:
            break


    asymmetry = 2.0

    if traditional:

        e_old = -1 * (delta(s[i, j], s[ip1, j], inverse)
            + delta(s[i, j], s[im1, j], inverse)
            + delta(s[i, j], s[i, jp1], inverse)
            + delta(s[i, j], s[i, jm1], inverse)
        )

        e_new = -1 * (delta(s_new, s[ip1, j])
            + delta(s_new, s[im1, j], inverse)
            + delta(s_new, s[i, jp1], inverse)
            + delta(s_new, s[i, jm1], inverse)
        )
    
    else:

        e_old = -1 * (asymmetry * delta(s[i, j], s[ip1, jp2], inverse)
            + asymmetry * delta(s[i, j], s[im1, jm2], inverse)
            + delta(s[i, j], s[i, jp1], inverse)
            + delta(s[i, j], s[i, jm1], inverse)
        )

        e_new = -1 * (asymmetry * delta(s_new, s[ip1, jp2], inverse)
            + asymmetry * delta(s_new, s[im1, jm2], inverse)
            + delta(s_new, s[i, jp1], inverse)
            + delta(s_new, s[i, jm1], inverse)
        )

    delta_e = e_new - e_old

    if delta_e < 0:
        accept = True
    else:
        if np.random.random() < np.exp(-beta * delta_e):
            accept = True

    if accept:
        s[i, j] = s_new

    return accept
