"""
Utility functions for 2D splines.

"""
from itertools import repeat

import numpy as np
from panda3d.core import LineSegs, Vec4
from scipy.integrate import romberg
from scipy.interpolate import splev
from scipy.interpolate import splprep
from scipy.optimize import fsolve


def arclength(tck, t1=1, t0=0):
    """Return the length of the (T, C, K) spline over [t0, t1], t <= 1.

    Defaults to the total arc length.
    """
    t1 = np.atleast_1d(t1)
    if t1.size > 1 and t0 == 0:
        t0 = np.zeros_like(t1)
    else:
        t0 = np.atleast_1d(t0)
    return np.array([
        romberg(lambda u: arclength_der(tck, u), t0i, t1i, tol=1e-6,
                vec_func=True)
        for t0i, t1i in zip(t0, t1)])


def arclength_der(tck, t):
    """Return the arclength derivative (= speed) of the (T, C, K) spline."""
    dx, dy = splev(t, tck, 1)
    return np.sqrt(dx*dx + dy*dy)


def arclength_inv(tck, s):
    """Return the arclength inverse t(s) for the (T, C, K) spline."""
    init_guess = s / arclength(tck)  # Initialize with the unit speed case.
    return fsolve(
            lambda t: arclength(tck, t) - s,
            init_guess,
            fprime=lambda t: np.diag(arclength_der(tck, t)))


def linspace(tck, n, t1=1, t0=0, sampling_factor=2):
    """Return the parameter values of n equally spaced points along the
    (T, C, K) spline, optionally in the [t0, t1] interval.

    This methods computes (u, s(u)) values and uses interpolation to compute
    u(s_eq), with s_eq the equally spaced points along the spline.
    Precision of the results can be increased with the interpolation sampling
    factor: number of points used for interpolation = n * sampling_factor.

    For a sampling factor of 2, experiments suggest a 5x speedup compared to
    using arclength_inv(), with an error on parameters of 1e-3.
    """
    u_ref = np.linspace(t0, t1, sampling_factor*n)
    s_ref = arclength(tck, u_ref)
    s_lin = np.linspace(s_ref[0], s_ref[-1], n)
    s_interp = np.interp(s_lin, s_ref, u_ref)
    return s_interp


def curvature(tck, t):
    """Return the (unsigned) curvature at t for the (T, C, K) spline."""
    dx, dy = splev(t, tck, 1)
    ddx, ddy = splev(t, tck, 2)
    return np.abs(dx*ddy - dy*ddx) / np.power(dx*dx + dy*dy, 1.5)


def get_smooth_path(path, s=.1, prep=None):
    """Smooth the input polyline.

    Parameters
    ----------
    path : (n,2) array
        List of 2D points.
    s : float, positive, optional
        Smoothing factor. Higher s => more smoothing.
    prep : callable, optional
        Preprocessing method applied to each vertex. Must accept and return
        a Point3.

    Returns
    -------
    tck : tuple
        Spline parameters; see scipy.interpolate.splprep for more details.
    """
    # Prepare the points for smoothing.
    clean_path = [path[0]]
    last_added = path[0]
    for point in path[1:]:
        # Ensure that no two consecutive points are duplicates.
        # Alternatively we could do before the loop:
        # vertices = [p[0] for p in itertools.groupby(path)]
        if not np.allclose(point, last_added):
            last_added = point
            if prep is not None:
                point = prep(point)
            clean_path.append(point)
    # Smooth the trajectory.
    # scipy's splprep is more convenient here than panda3d's Rope class,
    # since it gives better control over curve smoothing.
    # TODO. Make changes in the code to handle a BSpline instead of tck.
#    t, c, k = splprep(np.array(points).T, s=s)[0]
#    c = np.column_stack(c)
#    return BSpline(t, c, k)
    return splprep(np.array(clean_path).T, s=s)[0]


def splang(u, tck, degrees=True):
    """Get the tangential angle, defined as tan(phi) = dy / dx.
    For convenience wrt Panda3D's conventions, phi is returned in degrees by
    default.

    """
    dx, dy = splev(u, tck, 1)
    if degrees:
        return np.degrees(np.arctan2(dy, dx))
    else:
        return np.arctan2(dy, dx)


def splev3d(u, tck, zoffset):
    """Convenience function to convert a sequence of parameter values to
    a sequence of 3D positions along the (T, C, K) spline.

    """
    return np.column_stack(splev(u, tck) + [np.full(u.size, zoffset)])


def show_polyline3d(parent, vertices, label="polyline", color=(1, 1, 0, 1)):
    if np.isscalar(color[0]):
        color = repeat(color)
    elif np.isscalar(color[0][0]):
        color = iter(color)
    vertices = iter(vertices)
    ls = LineSegs(label)
    ls.set_thickness(5)
    ls.set_color(Vec4(*next(color)))
    ls.move_to(*next(vertices))
    for v, c in zip(vertices, color):
        ls.set_color(Vec4(*c))
        ls.draw_to(*v)
    parent.attach_new_node(ls.create())
    return ls


def show_spline2d(parent, tck, u, label="spline", color=(1, 1, 0, 1)):
    """Create a LineSegs instance representing the (t, c, k) spline, from a
    list of parameter values.

    """
    vertices = splev3d(u, tck, -.001)
    return show_polyline3d(parent, vertices, label, color)


def translate(tck, xy):
    return (tck[0].copy(), [tck[1][0]+xy[0], tck[1][1]+xy[1]], tck[2])


def copy(tck):
    return (tck[0].copy(), [tck[1][0].copy(), tck[1][1].copy()], tck[2])
