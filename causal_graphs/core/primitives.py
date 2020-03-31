"""
Basic primitives for the RGMs.

"""
import math
from functools import partial

import numpy as np
import panda3d.bullet as bt
import scipy.interpolate as ip
import scipy.optimize as opt
import solid as sl
import solid.utils as slu
from panda3d.core import (GeomNode, LineSegs, Quat, NodePath, Point3,
                          PythonCallbackObject, TransformState, Vec3)

from .dominoes import tilt_domino_forward
from .meshio import solid2panda, trimesh2panda
# from .spline2d import show_polyline3d


class CallbackSequence(list):
    """Allows to define a sequence of callbacks to give to BulletWorld"""
    def __call__(self, callback_data):
        for cb in self:
            cb(callback_data)
        callback_data.upcall()  # just to be safe


class World(bt.BulletWorld):
    """The world in which the primitives live."""

    def __init__(self):
        super().__init__()
        # Trick to have several physics callbacks. Note that the callback
        # object must not be a method of World, otherwise you get a circular
        # reference leading to a memory leak when you instantiate many worlds
        # at once.
        self._callbacks = CallbackSequence()
        self.set_tick_callback(
            PythonCallbackObject(self._callbacks), is_pretick=True
        )

    def set_gravity(self, gravity):
        gravity = Vec3(*gravity)
        super().set_gravity(gravity)


class BulletRootNodePath(NodePath):
    """Special NodePath, parent to bt nodes, that propagates transforms."""

    def __init__(self, *args):
        super().__init__(*args)

        xforms = ['set_pos', 'set_hpr', 'set_pos_hpr',
                  'set_x', 'set_y', 'set_z', 'set_h', 'set_p', 'set_r']

        for xform in xforms:
            setattr(self, xform,
                    partial(self.propagate_xform, xform=xform))

    def propagate_xform(self, *args, xform=''):
        getattr(super(), xform)(*args)
        for child in self.get_children():
            if isinstance(child.node(), bt.BulletBodyNode):
                child.node().set_transform_dirty()


class PrimitiveBase:
    """Base class for all primitives.

    Parameters
    ----------
    name : string
      Name of the primitive.
    geom : {None, 'LD', 'HD'}, optional
      Quality of the visible geometry. None by default (i.e. not visible).
    phys : bool, optional
      Whether this primitive participates in the simulation or not. If false,
      bt_props arguments are ignored. True by default.
    bt_props : dict, optional
      Dictionary of Bullet properties (mass, restitution, etc.). Basically
      the method set_key is called for the Bullet body, where "key" is each
      key of the dictionary. Empty by default (i.e. Bullet default values).

    """

    def __init__(self, name, **bt_props):
        self.name = name
        self.bt_props = bt_props

    @staticmethod
    def _attach(path=None, parent=None, bodies=None, constraints=None,
                physics_callback=None, world=None):
        """Attach the object to the scene and world.

        Parameters
        ----------
        path : NodePath, optional
          Path of the root of the instantiated object(s).
        parent : NodePath, optional
          Path of the node in the scene tree where where objects are added.
        bodies : sequence of bt.BulletRigidBodyNode, optional
          Rigid bodies.
        constraints: sequence of bt.BulletConstraint, optional
          Constraints between rigid bodies.
        physics_callback: callable, optional
          Function to call after each simulation step.
        world : World, optional
          Physical world where the rigid bodies and constraints are added.

        """
        if path is not None and parent is not None:
            path.reparent_to(parent)
        if world is not None:
            if bodies:
                for body in bodies:
                    world.attach(body)
            if constraints:
                for cs in constraints:
                    world.attach_constraint(cs, linked_collision=True)
                    cs.set_debug_draw_size(.05)
            if physics_callback is not None:
                world._callbacks.append(physics_callback)

    # def reset(self):
    #     path = None
    #     if phys:
    #         self.bodies = []
    #         self.constraints = []
    #         physics_callback = None

    def create(self, geom, phys, parent=None, world=None):
        raise NotImplementedError

    def _set_properties(self, bullet_object):
        for key, value in self.bt_props.items():
            getattr(bullet_object, "set_" + key)(value)


class Empty(PrimitiveBase):
    """Create an empty primitive (useful for constraints & reparametrization).

     Parameters
     ----------
     name : string
       Name of the primitive.

    """
    def __init__(self, name, **bt_props):
        super().__init__(name, **bt_props)

    def create(self, geom, phys, parent=None, world=None):
        name = self.name + "_solid"
        if phys:
            body = bt.BulletRigidBodyNode(name)
            self._set_properties(body)
            bodies = [body]
            path = NodePath(body)
        else:
            bodies = []
            path = NodePath(name)
        self._attach(path, parent, bodies=bodies, world=world)
        return path

    @staticmethod
    def make_geom(name):
        pass


class Plane(PrimitiveBase):
    """Create a plane.

    Parameters
    ----------
    name : string
      Name of the plane.
    normal : (3,) sequence
      Normal to the plane.
    distance : float
      Distance of the plane along the normal.

    """

    def __init__(self, name, normal=(0, 0, 1), distance=0, **bt_props):
        super().__init__(name=name, **bt_props)
        self.normal = Vec3(*normal)
        self.distance = distance

    def create(self, geom, phys, parent=None, world=None):
        name = self.name + "_solid"
        # Physics
        if phys:
            body = bt.BulletRigidBodyNode(name)
            self._set_properties(body)
            shape = bt.BulletPlaneShape(self.normal, self.distance)
            # NB: Using a box instead of a plane might help stability:
            # shape = bt.BulletBoxShape((1, 1, .1))
            # body.add_shape(shape, TransformState.make_pos(Point3(0, 0, -.1)))
            body.add_shape(shape)
            bodies = [body]
            path = NodePath(body)
        else:
            bodies = []
            path = NodePath(name)
        # Geometry
        if geom is not None:
            path.attach_new_node(self.make_geom(
                self.name + "_geom",
                self.normal,
                self.distance
            ))
        self._attach(path, parent, bodies=bodies, world=world)
        return path

    @staticmethod
    def make_geom(name, normal, distance, scale=100):
        # Compute basis
        normal = np.array(normal, dtype=np.float64)
        normal /= np.linalg.norm(normal)
        tangent = np.ones(3)
        tangent -= tangent.dot(normal) * normal
        tangent /= np.linalg.norm(tangent)
        bitangent = np.cross(normal, tangent)
        # Compute vertices
        vertices = np.array([
            tangent,
            bitangent,
            -tangent,
            -bitangent
        ]) * scale + distance * normal
        faces = np.array(
            [0, 1, 3, 1, 2, 3],
            dtype=np.int64
        ).reshape(-1, 3)
        vertex_normals = np.tile(normal, (len(vertices), 1))
        geom = trimesh2panda(vertices, faces, vertex_normals)
        geom_node = GeomNode(name)
        geom_node.add_geom(geom)
        return geom_node


class Ball(PrimitiveBase):
    """Create a ball.

    Parameters
    ----------
    name : string
      Name of the ball.
    radius : float
      Radius of the ball.

    """

    def __init__(self, name, radius, **bt_props):
        super().__init__(name=name, **bt_props)
        self.radius = radius

    def create(self, geom, phys, parent=None, world=None):
        name = self.name + "_solid"
        # Physics
        if phys:
            body = bt.BulletRigidBodyNode(name)
            self._set_properties(body)
            shape = bt.BulletSphereShape(self.radius)
            body.add_shape(shape)
            bodies = [body]
            path = NodePath(body)
        else:
            bodies = []
            path = NodePath(name)
        # Geometry
        if geom is not None:
            n_seg = 2**5 if geom == 'HD' else 2**4
            path.attach_new_node(
                self.make_geom(
                    self.name + "_geom", self.radius, n_seg
                )
            )
        self._attach(path, parent, bodies=bodies, world=world)
        return path

    @staticmethod
    def make_geom(name, radius, n_seg=2**4):
        script = sl.sphere(radius, segments=n_seg)
        geom = solid2panda(script)
        geom_node = GeomNode(name)
        geom_node.add_geom(geom)
        return geom_node


class Box(PrimitiveBase):
    """Create a box.

    Parameters
    ----------
    name : string
      Name of the box.
    extents : float sequence
      Extents of the box.

    """

    def __init__(self, name, extents, **bt_props):
        super().__init__(name=name, **bt_props)
        self.extents = extents

    def create(self, geom, phys, parent=None, world=None):
        name = self.name + "_solid"
        # Physics
        if phys:
            body = bt.BulletRigidBodyNode(name)
            self._set_properties(body)
            shape = bt.BulletBoxShape(Vec3(*self.extents) / 2)
            #  shape.set_margin(.0001)
            body.add_shape(shape)
            bodies = [body]
            path = NodePath(body)
        else:
            bodies = []
            path = NodePath(name)
        # Geometry
        if geom is not None:
            path.attach_new_node(
                self.make_geom(self.name + "_geom", self.extents))
        self._attach(path, parent, bodies=bodies, world=world)
        return path

    @staticmethod
    def make_geom(name, extents):
        box = sl.cube(tuple(extents), center=True)
        geom = solid2panda(box)
        geom_node = GeomNode(name)
        geom_node.add_geom(geom)
        return geom_node


class Cylinder(PrimitiveBase):
    """Create a cylinder.

    Parameters
    ----------
    name : string
      Name of the cylinder.
    extents : float sequence
      Extents of the cylinder: radius, height.
    center : bool
      Whether the cylinder should be centered. Defaults to True.

    """

    def __init__(self, name, extents, center=True,
                 **bt_props):
        super().__init__(name=name, **bt_props)
        self.extents = extents
        self.center = center

    def create(self, geom, phys, parent=None, world=None):
        name = self.name + "_solid"
        # Physics
        if phys:
            body = bt.BulletRigidBodyNode(name)
            self._set_properties(body)
            r, h = self.extents
            shape = bt.BulletCylinderShape(r, h)
            if self.center:
                body.add_shape(shape)
            else:
                body.add_shape(shape,
                               TransformState.make_pos(Point3(0, 0, h/2)))
            bodies = [body]
            path = NodePath(body)
        else:
            bodies = []
            path = NodePath(name)
        # Geometry
        if geom is not None:
            n_seg = 2**5 if geom == 'HD' else 2**4
            path.attach_new_node(
                self.make_geom(
                    self.name + "_geom", self.extents, self.center, n_seg
                )
            )
        self._attach(path, parent, bodies=bodies, world=world)
        return path

    @staticmethod
    def make_geom(name, extents, center=True, n_seg=2**4):
        r, h = extents
        script = sl.cylinder(r=r, h=h, center=center, segments=n_seg)
        geom = solid2panda(script)
        geom_node = GeomNode(name)
        geom_node.add_geom(geom)
        return geom_node


class Capsule(PrimitiveBase):
    """Create a capsule.

    Parameters
    ----------
    name : string
      Name of the capsule.
    extents : float sequence
      Extents of the capsule: radius, height.

    """

    def __init__(self, name, extents, **bt_props):
        super().__init__(name=name, **bt_props)
        self.extents = extents

    def create(self, geom, phys, parent=None, world=None):
        name = self.name + "_solid"
        # Physics
        if phys:
            body = bt.BulletRigidBodyNode(name)
            self._set_properties(body)
            r, h = self.extents
            shape = bt.BulletCapsuleShape(r, h)
            body.add_shape(shape)
            bodies = [body]
            path = NodePath(body)
        else:
            bodies = []
            path = NodePath(name)
        # Geometry
        if geom is not None:
            n_seg = 2**5 if geom == 'HD' else 2**4
            path.attach_new_node(
                self.make_geom(self.name + "_geom", self.extents, n_seg)
            )
        self._attach(path, parent, bodies=bodies, world=world)
        return path

    @staticmethod
    def make_geom(name, extents, n_seg=2**4):
        r, h = extents
        ball = sl.sphere(r=r, segments=n_seg)
        script = (sl.cylinder(r=r, h=h, center=True, segments=n_seg)
                  + slu.up(h / 2)(ball)
                  + slu.down(h / 2)(ball)
                  )
        geom = solid2panda(script)
        geom_node = GeomNode(name)
        geom_node.add_geom(geom)
        return geom_node


class Fastener(PrimitiveBase):
    """Glue two primitives together.

    Parameters
    ----------
    name : string
      Name of the primitive (useless here).
    comp1_xform : (6,) float sequence
      Relative transform of the constraint wrt the first primitive.
    comp2_xform : (6,) float sequence
      Relative transform of the constraint wrt the second primitive.

    """

    def __init__(self, name, comp1_xform, comp2_xform):
        super().__init__(name)
        self.comp1_xform = TransformState.make_pos_hpr(
            Point3(*comp1_xform[:3]), Vec3(*comp1_xform[3:])
        )
        self.comp2_xform = TransformState.make_pos_hpr(
            Point3(*comp2_xform[:3]), Vec3(*comp2_xform[3:])
        )

    def create(self, geom, phys, parent=None, world=None, components=None):
        if not phys or not components:
            return
        comp1, comp2 = components
        cs = bt.BulletGenericConstraint(
            comp1.node(), comp2.node(), self.comp1_xform, self.comp2_xform, 1
        )
        for i in range(3):
            cs.set_angular_limit(i, 0, 0)
            cs.set_linear_limit(i, 0, 0)
        self._attach(constraints=[cs], world=world)


class Pivot(PrimitiveBase):
    """Attach a pivot constraint to a primitive.

    Parameters
    ----------
    name : string
      Name of the primitive.
    pivot_pos : (3,) float sequence
      Relative position of the pivot wrt the primitive.
    pivot_hpr : (3,) float sequence
      Relative orientation of the pivot wrt the primitive.
    pivot_extents : None or (2,) float sequence, optional
      Parameters of the visual cylinder (if geom is not None): radius, height.
      None by default.

    """

    def __init__(self, name, pivot_pos, pivot_hpr, pivot_extents=None):
        super().__init__(name)
        pivot_pos = Point3(*pivot_pos)
        pivot_hpr = Vec3(*pivot_hpr)
        self.pivot_xform = TransformState.make_pos_hpr(pivot_pos, pivot_hpr)
        self.pivot_extents = pivot_extents

    def create(self, geom, phys, parent=None, world=None, components=None):
        pivot = Cylinder(name=self.name, extents=self.pivot_extents)
        path = pivot.create(geom, phys, parent, world)
        if not components:
            return path
        path.set_transform(components[0], self.pivot_xform)
        # Physics
        if phys:
            cs = bt.BulletHingeConstraint(
                path.node(), components[0].node(),
                TransformState.make_identity(), self.pivot_xform
            )
            self._attach(constraints=[cs], world=world)
        # return path


class Lever(PrimitiveBase):
    """Create a lever.

    Parameters
    ----------
    name : string
      Name of the lever.
    extents : float sequence
      Extents of the lever (same as Box).
    pivot_pos : (3,) float sequence
      Relative position of the pivot wrt the primitive.
    pivot_hpr : (3,) float sequence
      Relative orientation of the pivot wrt the primitive.
    pivot_extents : (2,) float sequence
      Parameters of the visual cylinder (if geom is True): radius, height.

    """

    def __init__(self, name, extents, pivot_pos, pivot_hpr, pivot_extents=None,
                 **bt_props):
        super().__init__(name)
        self.extents = extents
        self.pivot_pos = Point3(*pivot_pos)
        self.pivot_hpr = Vec3(*pivot_hpr)
        self.pivot_extents = pivot_extents
        self.bt_props = bt_props

    def create(self, geom, phys, parent=None, world=None):
        # Scene graph
        path = BulletRootNodePath(self.name) if phys else NodePath(self.name)
        self._attach(path, parent)
        # Physics
        box = Box(name=self.name, extents=self.extents, **self.bt_props)
        box_path = box.create(geom, phys, path, world)
        pivot = Pivot(
            name=self.name + "_pivot", pivot_pos=self.pivot_pos,
            pivot_hpr=self.pivot_hpr, pivot_extents=self.pivot_extents,
        )
        pivot.create(geom, phys, path, world, [box_path])
        return path


class Pulley(PrimitiveBase):
    """Create a pulley.

    Parameters
    ----------
    name : string
      Name of the lever.
    extents : float sequence
      Extents of the pulley (same as Cylinder): radius, height.
    pivot_pos : (3,) float sequence
      Relative position of the pivot wrt the primitive.
    pivot_hpr : (3,) float sequence
      Relative orientation of the pivot wrt the primitive.
    pivot_extents : (2,) float sequence
      Parameters of the visual cylinder (if geom is True): radius, height.
    geom : bool
      Whether to generate a geometry for visualization.
    bt_props : dict
      Dictionary of Bullet properties (mass, restitution, etc.). Basically
      the method set_key is called for the Bullet body, where "key" is each
      key of the dictionary.

    """

    def __init__(self, name, extents, pivot_pos, pivot_hpr, pivot_extents=None,
                 **bt_props):
        super().__init__(name)
        self.extents = extents
        self.pivot_pos = Point3(*pivot_pos)
        self.pivot_hpr = Vec3(*pivot_hpr)
        self.pivot_extents = pivot_extents
        self.bt_props = bt_props

    def create(self, geom, phys, parent=None, world=None):
        # Scene graph
        path = BulletRootNodePath(self.name) if phys else NodePath(self.name)
        self._attach(path, parent)
        # Physics
        cyl = Cylinder(name=self.name, extents=self.extents, **self.bt_props)
        cyl_path = cyl.create(geom, phys, path, world)
        pivot = Pivot(
            name=self.name+"_pivot", pivot_pos=self.pivot_pos,
            pivot_hpr=self.pivot_hpr, pivot_extents=self.pivot_extents,
        )
        pivot.create(geom, phys, path, world, [cyl_path])
        return path


class Goblet(PrimitiveBase):
    """Create a goblet.

    Parameters
    ----------
    name : string
      Name.
    extents : (4,) float sequence
      Extents of the goblet / truncated cone (h, r1, r2, eps), as defined in
      solidpython (r1 = radius at the bottom of the cone).

    """

    def __init__(self, name, extents, **bt_props):
        super().__init__(name=name, **bt_props)
        self.extents = extents

    def create(self, geom, phys, parent=None, world=None):
        name = self.name + "_solid"
        # Physics
        if phys:
            h, r1, r2, eps = self.extents
            alpha = math.atan2(r1 - r2, h)
            length = math.sqrt((r1 - r2) ** 2 + h ** 2)
            n_seg = 2**5
            body = bt.BulletRigidBodyNode(name)
            self._set_properties(body)
            # Add bottom
            bottom = bt.BulletCylinderShape(r2, eps)
            bottom.set_margin(eps)
            body.add_shape(bottom,
                           TransformState.make_pos(Point3(0, 0, eps / 2)))
            # Add sides
            side = bt.BulletBoxShape(
                Vec3(eps, 2 * math.pi * r1 / n_seg, length) / 2)
            side.set_margin(eps)
            cz = eps + h/2 - math.cos(alpha) * eps / 2
            cr = (r1 + r2) / 2 + math.sin(alpha) * eps / 2
            for i in range(n_seg):
                ai = (i + .5) * 2 * math.pi / n_seg  # .5 to match the geometry
                pos = Point3(cr * math.cos(ai), cr * math.sin(ai), cz)
                hpr = Vec3(math.degrees(ai), 0, math.degrees(alpha))
                body.add_shape(side, TransformState.make_pos_hpr(pos, hpr))
            bodies = [body]
            path = NodePath(body)
        else:
            bodies = []
            path = NodePath(name)
        # Geometry
        if geom is not None:
            n_seg = 2**5 if geom == 'HD' else 2**4
            path.attach_new_node(
                self.make_geom(self.name+"_geom", self.extents, n_seg)
            )
        self._attach(path, parent, bodies=bodies, world=world)
        return path

    @staticmethod
    def make_geom(name, extents, n_seg=2**4):
        h, r1, r2, eps = extents
        cos_alpha_inv = math.sqrt(1 + ((r1 - r2) / h)**2)
        h_ext = h + eps
        r1_ext = r1 + eps * cos_alpha_inv
        r2_ext = r1_ext - (r1 - r2) * h_ext / h
        script = (sl.cylinder(r1=r1_ext, r2=r2_ext, h=h_ext, segments=n_seg)
                  - sl.cylinder(r1=r1, r2=r2, h=h, segments=n_seg))
        script = sl.translate([0, 0, h + eps])(sl.rotate([180, 0, 0])(script))
        geom = solid2panda(script)
        geom_node = GeomNode(name)
        geom_node.add_geom(geom)
        return geom_node


class DominoRun(PrimitiveBase):
    """Create a domino run.

    Parameters
    ----------
    name : string
      Name of the box.
    extents : float sequence
      Extents of each domino.
    coords : (n,3) ndarray
      (x,y,heading) of each domino.
    tilt_angle : float, optional
      Angle by which the first domino should be tilted. Defaults to 0.

    """

    def __init__(self, name, extents, coords, tilt_angle=0, **bt_props):
        super().__init__(name=name, **bt_props)
        self.extents = extents
        self.coords = np.asarray(coords)
        self.tilt_angle = tilt_angle

    def create(self, geom, phys, parent=None, world=None):
        # Physics
        bodies = []
        if phys:
            shape = bt.BulletBoxShape(Vec3(*self.extents) / 2)
            path = BulletRootNodePath(self.name)
        else:
            path = NodePath(self.name)
        # Geometry
        if geom is not None:
            geom_path = NodePath(
                    Box.make_geom(self.name+"_geom", self.extents))
        #     # Path
        #     path_coords = np.c_[self.coords[:, :2],
        #                         np.zeros(len(self.coords))]
        #     if geom == 'LD':
        #         show_polyline3d(path, path_coords, self.name + "_path")
        #     elif geom == 'HD':
        #         path.attach_new_node(
        #             self.make_path_geom(self.name + "_path", path_coords,
        #                                 n_seg=2**3)
        #         )
        for i, (x, y, head) in enumerate(self.coords):
            name = self.name + "_dom_{}_solid".format(i)
            # Physics
            if phys:
                body = bt.BulletRigidBodyNode(name)
                bodies.append(body)
                body.add_shape(shape)
                self._set_properties(body)
            # Scene graph + local coords
            dom_path = NodePath(body) if phys else NodePath(name)
            dom_path.reparent_to(path)
            dom_path.set_pos(Point3(x, y, self.extents[2] / 2))
            dom_path.set_h(head)
            if i == 0 and self.tilt_angle:
                tilt_domino_forward(dom_path, self.extents, self.tilt_angle)
            # Geometry
            if geom is not None:
                geom_path.instance_to(dom_path)
        self._attach(path, parent, bodies=bodies, world=world)
        return path

    @staticmethod
    def make_path_geom(name, vertices, thickness=.001, n_seg=2**2):
        geom_node = GeomNode(name)
        vertices = [Vec3(*v) for v in vertices]
        for i, (a, b) in enumerate(zip(vertices[:-1], vertices[1:])):
            name = name + "_seg_" + str(i)
            length = (b - a).length()
            geom = Cylinder.make_geom(name, (thickness, length), False, n_seg)
            path = NodePath(geom)
            path.set_pos(a)
            path.look_at(b)
            path.set_hpr(path, Vec3(90, 0, 90))
            path.flatten_light()
            geom_node.add_geoms_from(path.node())
        return geom_node


class _VisualRopeCallback:
    def __init__(self, name, parent, hooks, rope_length, geom):
        self.name = name
        self.parent = parent
        self.hook1, self.hook2 = hooks
        self.rope_length = rope_length
        # Visual
        self.n_vertices = 15
        self.thickness = .001
        if geom == 'LD':
            self.rope = self._create_rope_ld()
            self._update_rope = self._update_rope_ld
        elif geom == 'HD':
            self.rope = self._create_rope_hd()
            self._update_rope = self._update_rope_hd
        # Useful variables.
        self._dt = 0.
        self._old_xforms = (self.hook1.get_net_transform(),
                            self.hook2.get_net_transform())

    def __call__(self, callback_data: bt.BulletTickCallbackData):
        if self._check_stale(callback_data):
            self._update_rope(self.rope)

    def check_physically_valid(self):
        return True

    @property
    def loose_rope(self):
        return 0

    def _check_stale(self, callback_data: bt.BulletTickCallbackData):
        # Check that objects' transforms have been updated.
        xforms = (self.hook1.get_net_transform(),
                  self.hook2.get_net_transform())
        stale = (self._old_xforms[0] != xforms[0] or
                 self._old_xforms[1] != xforms[1])
        self._old_xforms = xforms
        return stale

    def _create_rope_hd(self):
        thickness = self.thickness
        base_name = self.name
        rope = NodePath(base_name)
        for i in range(1, self.n_vertices):
            name = base_name + "_seg" + str(i)
            geom = Cylinder.make_geom(name, (thickness, 1), 4, False)
            geom.set_tag('anim_id', '')
            geom.set_tag('save_scale', '')
            rope.attach_new_node(geom)
        self._update_rope_hd(rope)
        rope.reparent_to(self.parent)
        return rope

    def _create_rope_ld(self):
        vertices = self._get_rope_vertices()
        ls = LineSegs(self.name)
        ls.set_color(0)
        vertiter = iter(vertices)
        ls.move_to(next(vertiter))
        for v in vertiter:
            ls.draw_to(v)
        rope = NodePath(ls.create(dynamic=True))
        self._rope_maker = ls
        rope.reparent_to(self.parent)
        return rope

    def _get_rope_vertices(self):
        P1 = self.hook1.get_pos(self.parent)
        P2 = self.hook2.get_pos(self.parent)
        t = np.linspace(0, 1, self.n_vertices)
        loose_rope = max(0, self.rope_length - (P1-P2).length())
        vertices = []
        for ti in t:
            p = P1 * (1-ti) + P2 * ti
            p[2] -= loose_rope * .5 * math.sin(math.pi * ti)
            vertices.append(p)
        return vertices

    def _update_rope_hd(self, rope):
        vertices = self._get_rope_vertices()
        # Update rope
        for i in range(len(vertices)-1):
            seg = rope.get_child(i)
            a = vertices[i]
            b = vertices[i+1]
            seg.set_pos(a)
            seg.set_scale(Vec3(1, 1, (b - a).length()))
            seg.look_at(b)
            seg.set_hpr(seg, Vec3(90, 0, 90))

    def _update_rope_ld(self, rope):
        vertices = self._get_rope_vertices()
        # Update rope
        ls = self._rope_maker
        for i, v in enumerate(vertices):
            ls.set_vertex(i, v)


def get_xform_between_vectors(u, v):
    cross = u.cross(v)
    dot = u.dot(v)
    theta = math.atan2(cross.length(), dot)
    q = Quat(math.cos(theta/2), cross.normalized() * math.sin(theta/2))
    return TransformState.make_quat(q)


class TensionRope(PrimitiveBase):
    """Create a rope in tension between two primitives.

    Parameters
    ----------
    name : string
      Name of the primitive.
    comp1_pos : (3,) float sequence
      Relative position of the hook on the first component.
    comp2_pos : (3,) float sequence
      Relative position of the hook on the second component.
    pivot_hpr: (3,) float sequence
      Orientation of the pivot constraints.
    hook_radius : float, optional
      Radius of the visual hook.
    loose_rope : float, optional
      Additional loose rope.

    """

    def __init__(self, name, comp1_pos, comp2_pos, pivot_hpr, hook_radius=.01,
                 loose_rope=0):
        super().__init__(name)
        self.comp1_pos = Point3(*comp1_pos)
        self.comp2_pos = Point3(*comp2_pos)
        self.pivot_hpr = Vec3(*pivot_hpr)
        self.loose_rope = loose_rope
        # Hardcoded physical properties.
        self.hook_mass = 5e-3
        self.max_slider_force = 1e6
        # Visual properties.
        self.hook_radius = hook_radius

    def create(self, geom, phys, parent=None, world=None, components=None):
        # Scene graph
        path = NodePath(self.name)
        self._attach(path, parent)
        # Components
        comp1, comp2 = components
        name1 = comp1.get_name()
        name2 = comp2.get_name()
        # The rope connection is a combination of three constraints: one pivot
        # at each component and a slider between them.
        # Hooks
        hook1 = Ball(  # using Ball instead of Empty stabilizes it
            name1 + "_hook", self.hook_radius, mass=self.hook_mass
        ).create(geom, phys, comp1, world)
        hook1.set_pos(self.comp1_pos)
        hook2 = Ball(  # using Ball instead of Empty stabilizes it
            name2 + "_hook", self.hook_radius, mass=self.hook_mass
        ).create(geom, phys, comp2, world)
        hook2.set_pos(self.comp2_pos)
        length = (
            hook1.get_net_transform().pos - hook2.get_net_transform().pos
        ).length() + self.loose_rope
        # Physics
        if phys:
            # comp1.node().set_deactivation_enabled(False)
            # comp2.node().set_deactivation_enabled(False)
            # hook1.node().set_deactivation_enabled(False)
            # hook2.node().set_deactivation_enabled(False)
            pivot_hpr = self.pivot_hpr.normalized()
            # Constraints
            cs1 = bt.BulletHingeConstraint(
                hook1.node(), comp1.node(),
                Point3(0), self.comp1_pos, pivot_hpr, pivot_hpr, True
            )
            cs2 = bt.BulletHingeConstraint(
                hook2.node(), comp2.node(),
                Point3(0), self.comp2_pos, pivot_hpr, pivot_hpr, True
            )
            x = Vec3.unit_x()  # slider axis is along the X-axis by default
            axis = hook2.get_pos(hook1)
            xform = get_xform_between_vectors(x, axis)
            cs3 = bt.BulletSliderConstraint(
                hook1.node(), hook2.node(), xform, xform, True
            )
            cs3.set_lower_linear_limit(0)
            cs3.set_upper_linear_limit(length)
            self._attach(constraints=(cs1, cs2, cs3), world=world)
        if geom is not None:
            # Rope
            cb = _VisualRopeCallback(self.name, path, (hook1, hook2),
                                     length, geom)
            self._attach(physics_callback=cb, world=world)
        return path


class _RopePulleyCallback:
    def __init__(self, components, hooks, constraints, rope_length, pulleys):
        self.comp1, self.comp2 = components
        self.hook1, self.hook2 = hooks
        self.slider1_cs = constraints[1]
        self.slider2_cs = constraints[4]
        self.hook1_cs = constraints[2]
        self.hook2_cs = constraints[5]
        self.rope_length = rope_length
        self.pulleys = pulleys
        # Useful values.
        self.dist_pulleys = sum(
            (c2 - c1).length() for c2, c1 in zip(pulleys[1:], pulleys[:-1])
        )
        self.max_dist = self.rope_length - self.dist_pulleys
        # Useful variables.
        self._dt = 0.  # time since previous update
        self._in_tension = False
        self._old_xforms = (self.hook1.get_net_transform(),
                            self.hook2.get_net_transform())

    def __call__(self, callback_data: bt.BulletTickCallbackData):
        # This callback may be called more often than the objects being
        # actually updated. Check if an update is necessary.
        stale = self._check_stale(callback_data)
        if stale:
            dt = self._dt + callback_data.get_timestep()
            self._dt = 0
        else:
            self._dt += callback_data.get_timestep()
            return
        slider1 = self.slider1_cs
        slider2 = self.slider2_cs
        loose_rope = self.loose_rope
        max_dist = self.max_dist
        # If in tension now
        if loose_rope <= 0:
            # If in tension before
            if self._in_tension:
                weight = self._get_weight_force()
                delta = dt * weight
                new_dist1 = slider1.get_upper_linear_limit() + delta
                new_dist2 = slider2.get_upper_linear_limit() - delta
                # Clamp values between hard limits.
                if new_dist1 < 0 or new_dist2 > max_dist:
                    new_dist1 = 0
                    new_dist2 = max_dist
                if new_dist2 < 0 or new_dist1 > max_dist:
                    new_dist2 = 0
                    new_dist1 = max_dist
            else:
                self._in_tension = True
                new_dist1 = self.vec1.length() + loose_rope/2
                new_dist2 = self.vec2.length() + loose_rope/2
            slider1.set_upper_linear_limit(new_dist1)
            slider2.set_upper_linear_limit(new_dist2)
        # If in tension before but not anymore
        elif self._in_tension:
            self._in_tension = False
            slider1.set_upper_linear_limit(self.max_dist)
            slider2.set_upper_linear_limit(self.max_dist)
        # If not in tension now or before, don't do anything.

    def check_physically_valid(self):
        return self.loose_rope >= 0

    def _check_stale(self, callback_data: bt.BulletTickCallbackData):
        # Check that objects' transforms have been updated.
        xforms = (self.hook1.get_net_transform(),
                  self.hook2.get_net_transform())
        stale = (self._old_xforms[0] != xforms[0] or
                 self._old_xforms[1] != xforms[1])
        self._old_xforms = xforms
        return stale

    @property
    def loose_rope(self):
        return self.max_dist - self.vec1.length() - self.vec2.length()

    @property
    def vec1(self):
        return self.hook1.get_pos() - self.pulleys[0]

    @property
    def vec2(self):
        return self.hook2.get_pos() - self.pulleys[-1]

    def _get_weight_force(self):
        gravity = 9.81
        mass1 = self.comp1.node().get_mass()
        mass2 = self.comp2.node().get_mass()
        return gravity * (mass1 - mass2) / (mass1 + mass2)


class _VisualRopePulleyCallback(_VisualRopeCallback):
    def __init__(self, name, parent, hooks, pulleys, rope_length, geom):
        self.pulleys = pulleys
        # Useful values.
        self.dist_pulleys = sum(
            (c2 - c1).length() for c2, c1 in zip(pulleys[1:], pulleys[:-1])
        )
        self.max_dist = rope_length - self.dist_pulleys
        super().__init__(name, parent, hooks, rope_length, geom)

    @property
    def loose_rope(self):
        return self.max_dist - self.vec1.length() - self.vec2.length()

    @property
    def vec1(self):
        return self.hook1.get_pos() - self.pulleys[0]

    @property
    def vec2(self):
        return self.hook2.get_pos() - self.pulleys[-1]

    def _get_rope_vertices(self):
        P0 = self.hook1.get_pos(self.parent)
        P1 = self.pulleys[0]
        Pn_1 = self.pulleys[-1]
        Pn = self.hook2.get_pos(self.parent)
        t = np.linspace(0, 1, self.n_vertices-2)
        loose_rope = max(0, self.loose_rope)
        vertices = [P0]
        for ti in t:
            p = P1 * (1-ti) + Pn_1 * ti
            p[2] -= loose_rope * .5 * math.sin(math.pi * ti)
            vertices.append(p)
        vertices.append(Pn)
        return vertices


class RopePulley(PrimitiveBase):
    """Create a rope-pulley system connecting two primitives.

    Parameters
    ----------
    name : string
      Name of the primitive.
    comp1_pos : (3,) float sequence
      Relative position of the hook on the first component.
    comp2_pos : (3,) float sequence
      Relative position of the hook on the second component.
    rope_length : float
      Length of the rope.
    pulleys : (n,3) float array
      (x, y, z) of each pulley.
    pulley_extents : float pair
      Radius and height of the cylinder.
    pulley_hpr : (3,) float sequence
      Orientation of all the pulleys.

    """

    def __init__(self, name, comp1_pos, comp2_pos, rope_length, pulleys,
                 pulley_extents, pulley_hpr):
        super().__init__(name)
        self.comp1_pos = Point3(*comp1_pos)
        self.comp2_pos = Point3(*comp2_pos)
        self.rope_length = rope_length
        self.pulleys = [Point3(*c) for c in pulleys]
        self.pulley_hpr = Vec3(*pulley_hpr)
        # Useful values.
        self.dist_pulleys = sum(
            (c2 - c1).length()
            for c2, c1 in zip(self.pulleys[1:], self.pulleys[:-1])
        )
        self.max_dist = self.rope_length - self.dist_pulleys
        # Hardcoded physical properties.
        self.hook_mass = 1e-2
        # self.max_slider_force = 1e6
        # Visual properties.
        self.pulley_extents = pulley_extents

    def _attach_objects(self, geom, phys, parent, world, components):
        hook1, cs1 = self._attach_pulley(components[0], self.comp1_pos,
                                         self.pulleys[0], parent, phys, world)
        hook2, cs2 = self._attach_pulley(components[1], self.comp2_pos,
                                         self.pulleys[-1], parent, phys, world)
        if phys:
            cb = _RopePulleyCallback(components, (hook1, hook2), cs1+cs2,
                                     self.rope_length, self.pulleys)
            self._attach(physics_callback=cb, world=world)
        if geom is not None:
            cb = _VisualRopePulleyCallback(
                self.name+"_rope", parent, (hook1, hook2), self.pulleys,
                self.rope_length, geom
            )
            self._attach(physics_callback=cb, world=world)

    def _attach_pulley(self, component, comp_coords, pulley_coords,
                       parent, phys, world):
        name = component.get_name()
        object_hook_coords = component.get_transform(
        ).get_mat().xform_point(comp_coords)
        # Each pulley connection is a combination of three constraints: One
        # pivot at the pulley, another at the component, and a slider between
        # them.
        # Pulley hook (can rotate on the base)
        pulley_hook = Ball(  # using Ball instead of Empty stabilizes it
            name + "_pulley-hook", self.pulley_extents[0], mass=self.hook_mass
        ).create(None, phys, parent, world)
        pulley_hook.set_pos(pulley_coords)
        # Object hook (can rotate on the object)
        object_hook = Empty(
            name + "_object-hook", mass=self.hook_mass
        ).create(None, phys, parent, world)
        object_hook.set_pos(object_hook_coords)
        # Physics
        if phys:
            # component.node().set_deactivation_enabled(False)
            # pulley_hook.node().set_deactivation_enabled(False)
            # object_hook.node().set_deactivation_enabled(False)
            pulley_hpr = self.pulley_hpr.normalized()
            # Constraints
            cs1 = bt.BulletHingeConstraint(
                pulley_hook.node(), Point3(0), pulley_hpr
            )
            x = Vec3.unit_x()  # slider axis is along the X-axis by default
            axis = object_hook.get_pos() - pulley_hook.get_pos()
            xform = get_xform_between_vectors(x, axis)
            cs2 = bt.BulletSliderConstraint(
                pulley_hook.node(), object_hook.node(), xform, xform, True
            )
            cs2.set_lower_linear_limit(0)
            cs2.set_upper_linear_limit(self.max_dist)
            # cs2.set_max_linear_motor_force(self.max_slider_force)
            cs3 = bt.BulletHingeConstraint(
                object_hook.node(), component.node(),
                Point3(0), comp_coords, pulley_hpr, pulley_hpr, True
            )
            self._attach(constraints=(cs1, cs2, cs3), world=world)
            return object_hook, (cs1, cs2, cs3)
        else:
            return object_hook, ()

    def create(self, geom, phys, parent=None, world=None, components=None):
        # Scene graph
        path = NodePath(self.name)
        self._attach(path, parent)
        # Components
        if components:
            self._attach_objects(geom, phys, path, world, components)
        # Geometry
        if geom is not None:
            pulley_hpr = self.pulley_hpr
            for i, coords in enumerate(self.pulleys):
                n_seg = 2**5 if geom == 'HD' else 2**4
                pulley = path.attach_new_node(
                    Cylinder.make_geom(
                        self.name + "_pulley_" + str(i) + "_geom",
                        self.pulley_extents, center=True, n_seg=n_seg
                    )
                )
                pulley.set_pos(coords)
                pulley.set_hpr(pulley_hpr)
        return path


class RopePulley2(PrimitiveBase):
    """Create a rope-pulley system connecting two primitives.

    Parameters
    ----------
    name : string
      Name of the primitive.
    comp1_pos : (3,) float sequence
      Relative position of the hook on the first component.
    comp2_pos : (3,) float sequence
      Relative position of the hook on the second component.
    rope_extents : float triplet
      Radius, total length and segment length of the rope.
    pulleys : (n,3) float array
      (x, y, z) of each pulley.
    pulley_extents : float pair
      Radius and height of the cylinder.

    """
    def __init__(self, name, comp1_pos, comp2_pos, rope_extents, pulleys,
                 pulley_extents):
        super().__init__(name)
        self.comp1_pos = Point3(*comp1_pos)
        self.comp2_pos = Point3(*comp2_pos)
        self.rope_radius, self.rope_length, self.seg_len = rope_extents
        self.seg_mass = .00004
        self.seg_angular_damping = .9
        self.pulleys = np.asarray(pulleys)
        self.pulley_radius, self.pulley_height = pulley_extents

    def create(self, geom, phys, parent=None, world=None, components=None):
        # Scene graph
        path = NodePath(self.name)
        # Physics
        bodies = []
        constraints = []
        # Pulleys
        pulley_shape = bt.BulletCylinderShape(self.pulley_radius,
                                              self.pulley_height)
        border_shape = bt.BulletCylinderShape(
            3*self.rope_radius+self.pulley_radius, self.rope_radius
        )
        border_pos = Point3(0, 0, self.pulley_height/2 + self.rope_radius/2)
        border_xform = TransformState.make_pos(border_pos)
        border_xform2 = TransformState.make_pos(-border_pos)
        pulley_hpr = self._get_pulley_hpr()
        for i, coords in enumerate(self.pulleys):
            name = self.name + "_pulley_{}_solid".format(i)
            body = bt.BulletRigidBodyNode(name)
            bodies.append(body)
            body.add_shape(pulley_shape)
            body.add_shape(border_shape, border_xform)
            body.add_shape(border_shape, border_xform2)
            pulley_path = NodePath(body)
            pulley_path.reparent_to(path)
            pulley_path.set_pos(*coords)
            pulley_path.set_hpr(pulley_hpr)
        # Rope
        rope_i = len(bodies)
        rope_points = self._get_rope_points(components)
        seg_shape = bt.BulletCapsuleShape(self.rope_radius, self.seg_len)
        seg_xform = TransformState.make_pos(Point3(0, 0, self.seg_len/2))
        for i, (a, b) in enumerate(zip(rope_points[:-1], rope_points[1:])):
            name = self.name + "_ropeseg_{}_solid".format(i)
            body = bt.BulletRigidBodyNode(name)
            bodies.append(body)
            body.add_shape(seg_shape, seg_xform)
            body.set_mass(self.seg_mass)
            body.set_angular_damping(self.seg_angular_damping)
            seg_path = NodePath(body)
            seg_path.reparent_to(path)
            seg_path.set_pos(*a)
            seg_path.look_at(*b)
            seg_path.set_hpr(seg_path, Vec3(90, 0, 90))
        cs_xform = Point3(0, 0, self.seg_len)
        for b1, b2 in zip(bodies[rope_i:-1], bodies[rope_i+1:]):
            cs = bt.BulletSphericalConstraint(b1, b2, cs_xform, 0)
            constraints.append(cs)
        if components:
            cs1 = bt.BulletSphericalConstraint(
                components[0].node(), bodies[rope_i], self.comp1_pos, 0
            )
            cs2 = bt.BulletSphericalConstraint(
                components[1].node(), bodies[-1], self.comp2_pos, cs_xform
            )
            constraints.extend([cs1, cs2])
        # Attach all
        self._attach(path, parent, bodies=bodies, constraints=constraints,
                     world=world)
        return path

    def _get_pulley_hpr(self):
        pulley_line = self.pulleys[-1] - self.pulleys[0]
        if pulley_line[0]:
            pulley_hpr = Vec3(0, 90, 0)
        else:
            pulley_hpr = Vec3(0, 0, 90)
        return pulley_hpr

    def _get_rope_points(self, components):
        # Compute init points
        pulleys = self.pulleys
        comp1, comp2 = components
        pos1 = comp1.get_net_transform().get_mat().xform_point(self.comp1_pos)
        pos2 = comp2.get_net_transform().get_mat().xform_point(self.comp2_pos)
        init_points = np.empty((2*len(pulleys)+2, 3))
        init_points[0] = pos1
        init_points[-1] = pos2
        shift = self.pulley_radius + 2*self.rope_radius
        pulley_dir = pulleys[1] - pulleys[0]
        shift_x = shift * np.sign(pulley_dir[0])
        shift_y = shift * np.sign(pulley_dir[1])
        init_points[1:2*len(pulleys):2] = pulleys + [-shift_x, -shift_y, shift]
        init_points[2:2*len(pulleys)+1:2] = pulleys + [shift_x, shift_y, shift]
        distances = np.linalg.norm(init_points[1:] - init_points[:-1], axis=1)
        residual = self.rope_length - distances.sum()
        if residual > 0:
            # print("r", residual)
            cat = self._solve_catenary_3d(init_points[2], init_points[3],
                                          distances[2]+residual)
            loose_points = cat(np.linspace(0, 1, 10)[1:-1])
            init_points = np.insert(init_points, 3, loose_points, axis=0)
        # Compute subdivided points
        distances = np.linalg.norm(init_points[1:] - init_points[:-1], axis=1)
        init_t = np.zeros(len(init_points))
        init_t[1:] = np.cumsum(distances)
        n_seg = int(init_t[-1] / self.seg_len)
        t = np.linspace(0, init_t[-1], n_seg)
        rope_points = np.column_stack([
            ip.interp1d(init_t, init_points[:, d])(t) for d in range(3)
        ])
        # print(rope_points)
        return rope_points

    def _solve_catenary_3d(self, p1, p2, s):
        h = math.sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)
        v = p2[2] - p1[2]
        rhs = math.sqrt(s**2 - v**2)
        sinh, arcsinh, cosh = np.sinh, np.arcsinh, np.cosh

        def f(x):
            return (2*x*sinh(h/(2*x)) - rhs) ** 2

        def fprime(x):
            return 2 * (2*sinh(h/(2*x)) - h*cosh(h/(2*x))/x) * (
                2*x*sinh(h/(2*x)) - rhs)
        x0_test = np.linspace(.01, s, 20)
        x0 = x0_test[np.argmin(f(x0_test))]
        a = opt.newton(f, x0=x0, fprime=fprime)
        # Compute the vertex coordinates
        x0 = a*arcsinh(v / (2*a*sinh(h/(2*a)))) - h/2
        z0 = p2[2] - a*cosh((h+x0)/a)

        def catenary(t):
            p = np.outer(t, (p2 - p1)) + p1
            p[:, 2] = a*cosh((t*h + x0) / a) + z0
            return p
        return catenary


class Track(PrimitiveBase):
    """Create straight track (e.g. for a ball run).

    The track is square because it makes collision shapes easier.
    The center is the center of the (length, width, height) bounding box.

    Parameters
    ----------
    name : string
      Name of the primitive.
    extents : (4,) float sequence
      Extents of the track: (length, width, height, thickness). The first 3
      are external.

    """

    def __init__(self, name, extents, **bt_props):
        super().__init__(name=name, **bt_props)
        self.extents = extents

    def create(self, geom, phys, parent=None, world=None):
        name = self.name + "_solid"
        # Physics
        if phys:
            body = bt.BulletRigidBodyNode(name)
            self._set_properties(body)
            l, w, h, t = self.extents
            bottom = bt.BulletBoxShape(Vec3(l/2, w/2 - t, t/2))
            body.add_shape(bottom,
                           TransformState.make_pos(Point3(0, 0, (t-h)/2)))
            side = bt.BulletBoxShape(Vec3(l/2, t/2, h/2))
            body.add_shape(side,
                           TransformState.make_pos(Point3(0, (t-w)/2, 0)))
            body.add_shape(side,
                           TransformState.make_pos(Point3(0, (w-t)/2, 0)))
            bodies = [body]
            path = NodePath(body)
        else:
            bodies = []
            path = NodePath(name)
        # Geometry
        if geom is not None:
            path.attach_new_node(
                self.make_geom(self.name + "_geom", self.extents))
        self._attach(path, parent, bodies=bodies, world=world)
        return path

    @staticmethod
    def make_geom(name, extents):
        l, w, h, t = extents
        box = sl.cube((l, w, h), center=True)
        groove = sl.cube((l, w - 2*t, h), center=True)
        script = box - sl.translate([0, 0, t])(groove)
        geom = solid2panda(script)
        geom_node = GeomNode(name)
        geom_node.add_geom(geom)
        return geom_node


class OpenBox(PrimitiveBase):
    """Create a hollow box with the top open.

    Parameters
    ----------
    name : string
      Name of the box.
    extents : float sequence
      Extents of the box.

    """

    def __init__(self, name, extents, **bt_props):
        super().__init__(name=name, **bt_props)
        self.extents = extents

    def create(self, geom, phys, parent=None, world=None):
        name = self.name + "_solid"
        # Physics
        if phys:
            body = bt.BulletRigidBodyNode(name)
            self._set_properties(body)
            l, w, h, t = self.extents
            bottom = bt.BulletBoxShape(Vec3(l, w, t) / 2)
            bottom_xform = TransformState.make_pos(Point3(0, 0, t/2-h/2))
            body.add_shape(bottom, bottom_xform)
            front = bt.BulletBoxShape(Vec3(l, h, t) / 2)
            front_xform = TransformState.make_pos_hpr(Point3(0, t/2-w/2, 0),
                                                      Vec3(0, 90, 0))
            body.add_shape(front, front_xform)
            back_xform = TransformState.make_pos_hpr(Point3(0, -t/2+w/2, 0),
                                                     Vec3(0, -90, 0))
            body.add_shape(front, back_xform)
            side = bt.BulletBoxShape(Vec3(h, w, t) / 2)
            left_xform = TransformState.make_pos_hpr(Point3(-t/2+l/2, 0, 0),
                                                     Vec3(0, 0, -90))
            body.add_shape(side, left_xform)
            right_xform = TransformState.make_pos_hpr(Point3(t/2-l/2, 0, 0),
                                                      Vec3(0, 0, 90))
            body.add_shape(side, right_xform)
            bodies = [body]
            path = NodePath(body)
        else:
            bodies = []
            path = NodePath(name)
        # Geometry
        if geom is not None:
            path.attach_new_node(
                self.make_geom(self.name + "_geom", self.extents))
        self._attach(path, parent, bodies=bodies, world=world)
        return path

    @staticmethod
    def make_geom(name, extents):
        l, w, h, t = extents
        box_out = sl.cube((l, w, h), center=True)
        box_in = sl.cube((l - 2*t, w - 2*t, h), center=True)
        box = box_out - sl.translate([0, 0, t])(box_in)
        geom = solid2panda(box)
        geom_node = GeomNode(name)
        geom_node.add_geom(geom)
        return geom_node


def get_primitives():
    return (Plane, Ball, Box, Cylinder, Lever, Pulley, Goblet, DominoRun,
            TensionRope, RopePulley, RopePulley2, Track, OpenBox)
