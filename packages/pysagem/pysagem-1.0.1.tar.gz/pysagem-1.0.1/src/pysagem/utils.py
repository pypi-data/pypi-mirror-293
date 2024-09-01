import logging

import numpy as np
from numba import float64, njit, vectorize


@njit
def set_seed(seed):
    """Seed the numba random generator"""

    np.random.seed(seed)


@njit
def rand():
    """Return a random float from 0 (inclusive) to 1 (exclusive)"""

    return np.random.rand()


@njit
def randint(low, high):
    """Return a random integer from low (inclusive) to high (exclusive)"""

    return np.random.randint(low, high)


@njit
def euclidean_dist(x1, y1, x2, y2):
    """Return the euclidean distance between two points"""

    point1 = np.array([x1, y1], dtype=np.float64)
    point2 = np.array([x2, y2], dtype=np.float64)

    return np.linalg.norm(point2 - point1)


@vectorize([float64(float64)])
def correct_num_errors(x):
    """Correct numerical errors, that should be 0.0"""

    if x < 1e-5:
        return 0.0
    else:
        return x


def get_pattern(p, q):
    """Return the pattern of the disturbance"""

    if q == p:
        pattern = "random pattern"
    elif q < p:
        pattern = "scattered pattern"
    elif q > p:
        pattern = "aggregate pattern"

    return pattern


def setup_logger(filename):
    """Setup the logger"""

    logging.basicConfig(
        format="%(message)s",
        handlers=[logging.FileHandler(f"{filename}.log", mode="w", encoding="utf-8")],
    )

    logger = logging.getLogger("pysagem")
    logger.setLevel(logging.INFO)

    return logger


def log_initial_args(logger, args):
    """Log the initial arguments"""

    lst_initial_description = [
        f"# run name: {args.name}\n",
        "general parameters:",
        f"\u2022 seed: {args.seed}",
        f"\u2022 matrix size: {args.length}x{args.length}",
        f"\u2022 number of generations: {args.gen}",
        f"\u2022 neighbors radius: {args.radius}",
        f"\u2022 number of invasors: {args.invasors}",
        f"\u2022 native species migration rate: {args.mignative}",
        f"\u2022 invasive species migration rate: {args.miginvasive}",
        f"\u2022 alpha: {args.alpha}",
        f"\u2022 beta: {args.beta}",
        f"\u2022 rn: {args.rn}",
        f"\u2022 ri: {args.ri}\n",
        "events: ",
        "\u2022 initial disturbance:",
        f"  - intensity: {args.p_initialdist}",
        f"  - degree of clustering: {args.q_initialdist}",
        f"  - {get_pattern(args.p_initialdist, args.q_initialdist)}\n",
    ]

    for item in lst_initial_description:
        logger.info(item)
