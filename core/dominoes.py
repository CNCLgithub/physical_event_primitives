"""
Utility functions for domino runs.

"""
import numpy as np
from panda3d.core import NodePath, Point3, TransformState, Vec3
from shapely.geometry import LineString

from . import spline2d as spl


def rotate_around(pos: Point3, hpr: Vec3, initial: NodePath):
    """Rotate in place the NodePath around a 3D point.

    Parameters
    ----------
    pos : Point3
      Center of rotation, relative to the NodePath.
    hpr : Vec3
      HPR components of the rotation, relative to the NodePath.
    initial : NodePath
      The NodePath to rotate.

    """
    xform = initial.get_transform()
    xform = xform.compose(
        TransformState.make_pos(pos)
        .compose(TransformState.make_hpr(hpr))
        .compose(TransformState.make_pos(-pos))
    )
    initial.set_transform(xform)


def tilt_domino_forward(domino: NodePath, extents, angle):
    """Rotate a domino around its locally Y-aligned bottom front edge.

    Parameters
    ----------
    domino : NodePath
      NodePath to the domino.
    extents : float triplet
      Extents of the domino.
    angle : float
      Rotation angle around the Y-aligned front edge.

    """
    ctr = Point3(extents[0], 0, -extents[2])
    rotate_around(ctr, Vec3(0, 0, angle), domino)


def _linear_transform_2D(coords, position, angle):
    if angle:
        cos = np.cos(angle)
        sin = np.sin(angle)
        rot_t = np.array([[cos, sin], [-sin, cos]])
        coords[:, :2] = coords[:, :2].dot(rot_t)
    coords[:, :2] += position


def create_branch(origin, angle, length, width, n_doms):
    """Create a Y branching in the domino path.

    Parameters
    ----------
    origin : (2,) sequence
      Position of the base of the Y.
    angle : float
      Global orientation of the Y (in degrees).
    length : float
      Length of the branch (or 'height' of the Y).
    width : float
      Width of the branch.
    n_doms : int
      Number of dominoes per half-length.

    """
    coords = np.zeros((3*n_doms, 3))
    # X
    coords[:2*n_doms, 0] = np.linspace(0, length, 2*n_doms)
    coords[2*n_doms:, 0] = coords[n_doms:2*n_doms, 0]
    # Y
    coords[n_doms:2*n_doms-1, 1] = np.linspace(0, width/2, n_doms)[1:]
    coords[2*n_doms-1, 1] = width/2
    coords[2*n_doms:, 1] = -coords[n_doms:2*n_doms, 1]
    # A
    coords[:, 2] = angle
    _linear_transform_2D(coords, origin, np.radians(angle))
    return coords


def create_line(origin, angle, length, n_doms):
    """Create a row of dominoes.

    Parameters
    ----------
    origin : (2,) sequence
      Position of the first domino.
    angle : float
      Global orientation of the row (in degrees).
    length : float
      Length of the row.
    n_doms : int
      Number of dominoes.

    """
    coords = np.zeros((n_doms, 3))
    coords[:, 0] = np.linspace(0, length, n_doms)
    coords[:, 2] = angle
    _linear_transform_2D(coords, origin, np.radians(angle))
    return coords


def create_circular_arc(center, radius, angle_start, angle_stop, n_doms):
    """Create a circular arc of dominoes.

    Parameters
    ----------
    center : (2,) sequence
      Center of the circle.
    radius : float
      Radius of the circle.
    angle_start : float
      Start angle (in degrees).
    angle_stop : float
      Stop angle (in degrees).
    n_doms : int
      Number of dominoes.

    """
    coords = np.zeros((n_doms, 3))
    angles = np.linspace(angle_start, angle_stop, n_doms)
    angles_rad = np.radians(angles)
    coords[:, 2] = angles + 90
    coords[:, 0] = radius * np.cos(angles_rad)
    coords[:, 1] = radius * np.sin(angles_rad)
    _linear_transform_2D(coords, center, 0)
    return coords


def create_wave(origin, angle, length, width, n_doms):
    """Create a wave y = exp(-x**2/2)sin(x)

    Parameters
    ----------
    origin : (2,) sequence
      Position of the first domino.
    angle : float
      Global orientation of the wave (in degrees).
    length : float
      Length of the row.
    width : float
      Width of the row.
    n_doms : int
      Number of dominoes.

    """
    coords = np.zeros((n_doms, 3))
    # Compute dense (x,y) samples.
    x = np.linspace(0, length, 2*n_doms)
    x_ = np.pi * (2*x/length - 1)  # transform x range to [-pi,pi]
    k = (width/2) / .523573  # the denominator is ~ max{exp(-x**2/2)sin(x)}
    gauss = np.exp(-x_**2 / 2)
    sin = np.sin(x_)
    y = k * gauss * sin
    # Compute equidistant (x,y) samples.
    polyline = LineString(np.column_stack((x, y)))
    uniform = np.array(
        [polyline.interpolate(i/(n_doms-1), normalized=True).coords[0]
         for i in range(n_doms)]
    )
    coords[:, :2] = uniform
    # Compute local arc tangent.
    x_ = np.pi * (2*uniform[:, 0]/length - 1)
    gauss = np.exp(-x_**2 / 2)
    sin = np.sin(x_)
    cos = np.cos(x_)
    coords[:, 2] = np.degrees(
        np.arctan2(k * gauss * (2*np.pi/length) * (cos - x_*sin), 1)
    )
    _linear_transform_2D(coords, origin, angle)
    return coords


def create_x_switch(origin, angle, width, n_doms):
    n_turn = 3
    coords = np.zeros((2*n_doms, 3))
    coords[:n_turn] = create_circular_arc(
        [0, -width/2], width/2, 90, 45, n_turn
    )
    coords[n_turn:n_doms-n_turn] = create_line(
        coords[n_turn-1, :2], -45, width, n_doms-2*n_turn+2
        )[1:-1]
    coords[n_doms-n_turn:n_doms] = create_circular_arc(
        [np.sqrt(2)*width, -width/2], width/2, -135, -90, n_turn
    )
    coords[n_doms:n_doms+n_turn] = create_circular_arc(
        [0, -width/2], width/2, -90, -45, n_turn
    )
    coords[n_doms+n_turn:-n_turn] = create_line(
        coords[n_doms+n_turn-1, :2], 45, width, n_doms-2*n_turn+2
        )[1:-1]
    coords[-n_turn:] = create_circular_arc(
        [np.sqrt(2)*width, -width/2], width/2, 135, 90, n_turn
    )
    coords[(n_doms-1)//2, 2] = 0
    coords = np.delete(coords, n_doms+(n_doms-1)/2, 0)
    _linear_transform_2D(coords, origin, 0)
    return coords


def create_smooth_path(coords, smoothing, n_doms):
    # Smooth the path
    k = min(3, len(coords)-1)
    spline = spl.splprep(list(zip(*coords)), k=k, s=smoothing)[0]
    # Sample positions
    u = spl.linspace(spline, n_doms)
    coords = np.column_stack(spl.splev(u, spline) + [spl.splang(u, spline)])
    return coords
