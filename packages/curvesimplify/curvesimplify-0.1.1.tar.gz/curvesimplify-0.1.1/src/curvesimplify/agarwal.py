"""Simplification algorithm by Agarwal et al. [1]_.

This is a greedy algorithm, fast but relatively inaccurate.

References
----------
.. [1] Agarwal, Pankaj K., et al. "Near-linear time approximation algorithms for curve
   simplification." Algorithmica 42 (2005): 203-219.
"""

import numpy as np
from curvesimilarities.frechet import decision_problem, fd
from numba import njit

__all__ = [
    "min_num",
    "min_err",
]


EPSILON = np.finfo(np.float64).eps


@njit(cache=True)
def min_num(curve, err, err_type="frechet"):
    r"""Agarwal min-:math:`\#` simplification.

    Parameters
    ----------
    curve : ndarray
        A :math:`p` by :math:`n` array of :math:`p` points in an :math:`n`-dimensional
        space.
    err : double
        Error threshold.
    err_type : {'frechet'}
        Error type. Refer to the package docstring.

    Returns
    -------
    simp : ndarray
        An :math:`\ell \le p` by :math:`n` array of :math:`\ell` points in an
        :math:`n`-dimensional space.
    """
    ij = 0
    ret = np.empty(len(curve), dtype=np.int_)
    count = 0

    ret[count] = ij
    count += 1

    n = len(curve)
    if err_type == "frechet":
        while ij < n - 1:
            L = 0
            high = min(2 ** (L + 1), n - ij - 1)
            all_ok = False
            while decision_problem(
                np.concatenate((curve[ij : ij + 1], curve[ij + high - 1 : ij + high])),
                curve[ij : ij + high + 1],
                err,
            ):
                if high == n - ij - 1:
                    # stop because all remaining vertices can be skipped
                    all_ok = True
                    break
                L += 1
                high = min(2 ** (L + 1), n - ij - 1)

            if all_ok:
                ret[count] = n - 1
                count += 1
                break

            low = max(1, high // 2)
            while low < high - 1:
                mid = (low + high) // 2
                if decision_problem(
                    np.concatenate(
                        (curve[ij : ij + 1], curve[ij + mid - 1 : ij + mid])
                    ),
                    curve[ij : ij + mid + 1],
                    err,
                ):
                    low = mid
                else:
                    high = mid
            ij += min(low, n - ij - 1)
            ret[count] = ij
            count += 1
    return curve[ret[:count]]


@njit(cache=True)
def min_err(curve, ell, err_type="frechet"):
    r"""Agarwal min-:math:`\epsilon` simplification.

    Parametric search is evoked on :func:`min_num` to find the minimum error satisfying
    :math:`\ell`.

    Parameters
    ----------
    curve : ndarray
        A :math:`p` by :math:`n` array of :math:`p` points in an :math:`n`-dimensional
        space.
    ell : double
        Desired number of vertices of simplification result.
    err_type : {'frechet'}
        Error type. Refer to the package docstring.

    Returns
    -------
    simp : ndarray
        An :math:`p' \le \ell` by :math:`n` array of :math:`p'` points in an
        :math:`n`-dimensional space.
    err : double
        Simplification error.
    """
    thres_low = 0
    shortcut = np.concatenate((curve[:1], curve[:-1]))
    thres_high = fd(curve, shortcut)  # TODO: use cheaper initializer
    simp_vert = min_num(curve, thres_high, err_type)  # may be > 2

    while len(simp_vert) > ell:  # tolerance too small
        thres_low = thres_high
        thres_high *= 2
        simp_vert = min_num(curve, thres_high, err_type)

    # Find adequate threshold by binary search
    while thres_high - thres_low > EPSILON:
        thres = (thres_low + thres_high) / 2
        if (thres - thres_low < EPSILON) | (thres_high - thres < EPSILON):
            break
        simp_vert = min_num(curve, thres, err_type)
        if len(simp_vert) > ell:
            thres_low = thres
        else:
            thres_high = thres

    return simp_vert, thres
