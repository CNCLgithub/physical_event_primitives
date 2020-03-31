"""
Generate 2D geometry to be displayed in Panda3D, mainly for GUI purposes.

"""
import math

from panda3d.core import Point3D
from panda3d.egg import load_egg_data
from panda3d.egg import EggData
from panda3d.egg import EggVertexPool
from panda3d.egg import EggVertex
from panda3d.egg import EggPolygon
from shapely.geometry import box


def make_circle(name, radius=1, angle_start=0, angle_end=360, resol=16):
    data = EggData()

    vp = EggVertexPool(name)
    data.add_child(vp)

    poly = EggPolygon()
    data.add_child(poly)

    angle_start = angle_start * math.pi / 180
    angle_end = angle_end * math.pi / 180

    for i in range(resol + 1):
        a = angle_start + (angle_end - angle_start) * i / resol
        y = radius * math.sin(a)
        x = radius * math.cos(a)

        v = EggVertex()
        v.set_pos(Point3D(x, 0, y))
        poly.add_vertex(vp.add_vertex(v))

    return load_egg_data(data)  # PandaNode


def make_rectangle(name, width, height, radius=0, resol=8):
    data = EggData()

    vp = EggVertexPool(name)
    data.add_child(vp)

    poly = EggPolygon()
    data.add_child(poly)

    # Generate the shape.
    b = box(-width/2 + radius, -height/2 + radius,
            width/2 - radius,  height/2 - radius)
    if radius:
        b = b.buffer(radius, resolution=resol, join_style=1)

    for x, y in b.exterior.coords:
        v = EggVertex()
        v.set_pos(Point3D(x, 0, y))
        poly.add_vertex(vp.add_vertex(v))

    return load_egg_data(data)  # PandaNode
