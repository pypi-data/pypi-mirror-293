import math

import numpy as np
from numba import float64, int64, njit, prange, typed, vectorize

from .utils import correct_num_errors, euclidean_dist, rand, randint


@njit
def find_neighbors(matrix_length, neighbors_radius):
    """Find all the neighbors inside the radius of each patch.

    Parameters
    ----------
    matrix_length : int
        The length of the matrix.
    neighbors_radius : float
        The radius of neighbors to consider.

    Returns
    -------
    numba typed-list
        The list of all possible neighbors.

    Notes
    -----
    This function assumes reflective borders, which means that patches on
    the matrix's edges are not considered neighbors of patches of the other
    side.

    Considering a radius of 1, the neighbors list will contain the 4 adjacent
    neighbors (up, down, left, right) for each patch if exists. See the 4x4
    matrix below where the '!' represents the patch and 'x' represents its
    neighbors:

       0  1  2  3
    0 [!, x, o, o]  !Patch 0(0, 0) -> Neighbors: 1(0, 1); 4(1, 0)
    1 [x, o, o, x]
    2 [o, o, x, !]  !Patch 11(2, 3) -> Neighbors: 7(1, 3); 10(2, 2); 15(3, 3)
    3 [o, o, o, x]
    """

    major = np.arange(1, matrix_length + 1, dtype=np.int64)
    major[-1] = matrix_length - 2

    minor = np.arange(-1, matrix_length - 1, dtype=np.int64)
    minor[0] = 1

    neighbors = typed.List()

    for x in range(matrix_length):
        for y in range(matrix_length):
            was_visited = np.full((matrix_length, matrix_length), False)
            was_visited[x, y] = True

            patch_index = x * matrix_length + y
            tmp_neighbors = [patch_index]

            total_num_added = 1

            run = True
            while run:
                temp_num_added = 0

                for i in range(total_num_added):
                    patch_index2 = tmp_neighbors[i]

                    x2 = int(patch_index2 / matrix_length)
                    y2 = patch_index2 - (x2 * matrix_length)

                    for dx, dy in [
                        (major[x2], y2),
                        (minor[x2], y2),
                        (x2, major[y2]),
                        (x2, minor[y2]),
                    ]:
                        if not was_visited[dx, dy]:
                            if euclidean_dist(x, y, dx, dy) <= neighbors_radius:
                                tmp_neighbors.append(dx * matrix_length + dy)

                                was_visited[dx, dy] = True
                                temp_num_added += 1

                if temp_num_added == 0:
                    run = False

                total_num_added += temp_num_added

            # excludes the patch itself
            neighbors.append(np.array(tmp_neighbors[1:]))

    return neighbors


@vectorize([int64(float64, float64)])
def _calc_emigrants(pop, migration_rate):
    """Calculates the number of emigrants according to the migration rate.

    Parameters
    ----------
    pop : np.ndarray[float64]
        The population array.
    migration_rate : float
        The percentage of individuals that will migrate.

    Returns
    -------
    np.ndarray[int64]
        The array of emigrants.

    Notes
    -----
    The result only considers whole numbers because the number of emigrants
    must be an integer. If the result is less than 1, then the number of
    emigrants is set to 0 and the remaining will stay in the patch.
    """

    return pop * migration_rate


@njit
def migration(pop, migration_rate, neighbors_info):
    """Performs migration between neighboring patches.

    It randomly selects neighboring patches as destinations for the
    emigrants, and updates the population array accordingly.

    Parameters
    ----------
    pop : np.ndarray[float64]
        The population array.
    migration_rate : float
        The percentage of individuals that will migrate.
    neighbors_info : numba typed-list
        The list of all possible neighbors.

    Returns
    -------
    np.ndarray[float64]
        The updated population array.
    """

    immigrants = np.zeros(pop.size, dtype=np.int64)
    emigrants = _calc_emigrants(pop, migration_rate)

    for i in range(pop.size):
        local_emigrants = emigrants[i]
        local_neighbors = neighbors_info[i]

        while local_emigrants >= 1:
            neighbor_index = local_neighbors[randint(0, local_neighbors.size)]

            immigrants[neighbor_index] += 1
            local_emigrants -= 1

    pop += immigrants
    pop -= emigrants
    pop = correct_num_errors(pop)

    return pop


@vectorize([int64(int64)])
def kn_update(landscape):
    """Updates the carrying capacity of the native species.

    Parameters
    ----------
    landscape : np.ndarray[int64]
        The landscape array.

    Returns
    -------
    np.ndarray[int64]
        The carrying capacity array.

    Raises
    ------
    ValueError
        If the landscape quality is invalid. The acceptable values
        are 0, 1 or 2.
    """

    if landscape == 2 or landscape == 1:
        return 1000

    elif landscape == 0:
        return 500

    else:
        raise ValueError("Invalid landscape quality")


@vectorize([int64(int64)])
def ki_update(landscape):
    """Updates the carrying capacity of the invasive species.

    Parameters
    ----------
    landscape : np.ndarray[int64]
        The landscape array.

    Returns
    -------
    np.ndarray[int64]
        The carrying capacity array.

    Raises
    ------
    ValueError
        If the landscape quality is invalid. The acceptable values
        are 0, 1 or 2.
    """

    if landscape == 2:
        return 500

    elif landscape == 1 or landscape == 0:
        return 1000

    else:
        raise ValueError("Invalid landscape quality")


@vectorize([float64(float64, float64, float64, float64, int64)])
def lotka(pop1, pop2, r, alpha_or_beta, k):
    """This function calculates the updated size of population 1 based on
    the Lotka-Volterra equation.

    Parameters
    ----------
    pop1 : np.ndarray[float64]
        Size of population 1.
    pop2 : np.ndarray[float64]
        Size of population 2.
    r : float
        Growth rate.
    alpha_or_beta : float
        Competition coefficient.
    k : np.ndarray[int64]
        The carrying capacity array.

    Returns
    -------
    np.ndarray[float64]
        Updated size of population 1.
    """

    result_pop1 = pop1 * (1 + r * (1 - ((pop1 + alpha_or_beta * pop2) / k)))
    result_pop1 = correct_num_errors(result_pop1)

    return result_pop1


@njit
def invasion(landscape, invpop, invasive_to_introduce):
    """Distributes the invaders through the disturbed patches.

    This function randomly selects disturbed patches (quality 0) and
    increases the invasive population in those patches.

    Parameters
    ----------
    landscape : np.ndarray[int64]
        The landscape array.
    invpop : np.ndarray[float64]
        The invasive population array.
    invasive_to_introduce : int
        The number of invaders to introduce.

    Returns
    -------
    np.ndarray[float64]
        An updated array representing the invasive population.
    """

    (disturbed_patches,) = np.nonzero(landscape == 0)

    if disturbed_patches.size >= 1:
        for _ in range(invasive_to_introduce):
            chosen_index = disturbed_patches[randint(0, disturbed_patches.size)]
            invpop[chosen_index] += 1

    return invpop


@vectorize([int64(int64, float64)])
def _rand_disturbance(landscape, p):
    if landscape > 0:
        if rand() <= p:
            landscape = 0

    return landscape


@njit(parallel=True)
def _count_blocks(landscape, close_neighbors):
    result_00 = 0
    result_02 = 0
    result_22 = 0

    for i in prange(landscape.size):
        neighbors = close_neighbors[np.int64(i)]

        for index_neighbor in neighbors:
            if landscape[i] == 0:
                if landscape[index_neighbor] == 0:
                    result_00 += 1

                elif landscape[index_neighbor] == 2:
                    result_02 += 1

            elif landscape[i] == 2:
                if landscape[index_neighbor] == 0:
                    result_02 += 1

                elif landscape[index_neighbor] == 2:
                    result_22 += 1

    return result_00, result_02, result_22


@njit
def _calc_dvalue(desired_blocks, counted_blocks):
    desired_00, desired_02, desired_22 = desired_blocks
    counted_00, counted_02, counted_22 = counted_blocks

    d_value = (
        abs(desired_00 - counted_00)
        + 2 * abs(desired_02 - counted_02)
        + abs(desired_22 - counted_22)
    )

    return d_value


@njit
def disturbance(landscape, p, q, close_neighbors):
    """Causes a disturbance over the landscape.

    Parameters
    ----------
    landscape : np.ndarray[int64]
        The landscape array.
    p : float
        The probability of disturbance (0 <= p <= 1).
    q : float
        The degree of clustering (0 <= q <= 1).
    close_neighbors : numba typed-list
        A list containing the index of the 4 adjacent neighbors (up, down,
        left, right) for each patch if exists.

    Returns
    -------
    np.ndarray[int64]
        Disturbed landscape array.

    Notes
    -----
    if q == p:
        The pattern of the disturbance is random.
    if q < p:
        The pattern of the disturbance is scattered.
    if q > p:
        The pattern of the disturbance is aggregate/clustered.

    This function is based on the Hiebeler's algorithm originally
    written in C [1]_.

    References
    ----------
    .. [1] Hiebeler, D. (2000) Populations on Fragmented Landscapes
        with Spatially Structured Heterogeneities: Landscape
        Generation and Local Dispersal. Ecology, 81(6), 1629-1641.
    """

    matrix_length = int(math.sqrt(landscape.size))

    p00 = p * q
    p02 = p - p00
    p22 = 1.0 - (p00 + 2.0 * (p02))

    percentages = correct_num_errors(np.array([p00, p02 * 2, p22], dtype=np.float64))
    total_blocks = ((matrix_length - 1) / matrix_length) * (4 * (matrix_length**2))
    desired = percentages * total_blocks

    landscape = _rand_disturbance(landscape, p)
    for _ in range(1e4):
        temp_landscape = np.copy(landscape)
        counted = _count_blocks(landscape, close_neighbors)
        d_value = _calc_dvalue(desired, counted)

        random_idx = randint(0, landscape.size)
        if temp_landscape[random_idx] == 0:
            temp_landscape[random_idx] = 2
        else:
            temp_landscape[random_idx] = 0

        temp_count = _count_blocks(temp_landscape, close_neighbors)
        temp_d = _calc_dvalue(desired, temp_count)

        if temp_d < d_value:
            landscape[random_idx] = temp_landscape[random_idx]

    return landscape


@vectorize([int64(int64, float64)])
def restoration(landscape, pr):
    """Restores the quality of disturbed patches by 1 according to the given
    probability.

    This function ignores patches with landscape quality 2 (maximum quality).

    Parameters
    ----------
    landscape : np.ndarray[int64]
        The landscape array.
    pr : float
        The probability of restoration.

    Returns
    -------
    np.ndarray[int64]
        The updated landscape array.
    """
    if landscape < 2:
        if rand() <= pr:
            landscape += 1

    return landscape
