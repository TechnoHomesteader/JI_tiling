"""
Shared utility functions for JI_tiling notebooks.
"""

import numpy as np
from itertools import chain, combinations
from scipy.spatial import Delaunay


def basis2D(eigenVectors, k, l):
    """Construct a 2D projection basis from two eigenvectors of the 5D rotation matrix.

    Returns a (2, 5) matrix `p` such that `p @ x` projects a 5D point onto the plane.
    Also prints the rotation angle between the projected standard basis vectors.
    """
    pi_unicode = "\u03C0"

    u, v = (eigenVectors[:, k] + eigenVectors[:, l]).real, \
           (1j * (eigenVectors[:, k] - eigenVectors[:, l])).real
    u /= np.linalg.norm(u)
    v /= np.linalg.norm(v)
    p = np.vstack((u, v))

    e1 = p @ np.array([0, 1, 0, 0, 0])
    e2 = p @ np.array([0, 0, 1, 0, 0])
    e1 = e1 / np.linalg.norm(e1)
    e2 = e2 / np.linalg.norm(e2)

    p_rotation = np.arccos(np.dot(e1, e2)) * (5 / np.pi)
    print(f'-->5D basis vectors are rotated in 2D plane by ({p_rotation}{pi_unicode})/5')

    return p


def subSet(iterable, n):
    """Return all subsets of length n from iterable.

    Example: subSet([1,2,3], 2) --> (1,2) (1,3) (2,3)
    """
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(n, n + 1))


def in_hull(p, hull):
    """Test if points in `p` are in `hull`.

    `p` should be an NxK array of N points in K dimensions.
    `hull` is either a scipy.spatial.Delaunay object or an MxK array of points
    for which Delaunay triangulation will be computed.

    Reference: https://stackoverflow.com/questions/16750618/
    """
    if not isinstance(hull, Delaunay):
        hull = Delaunay(hull)
    return hull.find_simplex(p) >= 0


def unitVector(l, d):
    """Return a unit vector of length `l` with a 1 at index `d`."""
    u = np.zeros(l)
    u[d] = 1.0
    return u


def polygonDataFunction(point, dir_):
    """Return the four 5D corners of a rhombus tile.

    `point` is the base corner; `dir_` is a 2-tuple of axis indices.
    """
    return np.array([
        point,
        point + unitVector(5, dir_[0]),
        point + unitVector(5, dir_[0]) + unitVector(5, dir_[1]),
        point + unitVector(5, dir_[1]),
    ])


def nMemberQ(set_, point_):
    """Return True if `point_` is contained in `set_` (within tolerance 1e-6)."""
    return np.any(np.sum(np.abs(set_ - point_), 1) < 1e-6)
