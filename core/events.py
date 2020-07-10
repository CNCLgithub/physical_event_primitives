from panda3d.core import Vec3


class Contact:
    _num_objects = 2

    def __init__(self, first, second, world):
        self.first = first
        self.second = second
        self.world = world

    def __call__(self):
        contact = self.world.contact_test_pair(
            self.first.node(), self.second.node()
        ).get_num_contacts()
        return bool(contact)


class Dummy:
    _num_objects = 0

    def __call__(self):
        return True


class Falling:
    _num_objects = 1

    def __init__(self, body, min_linvel=0):
        self.body = body
        self.min_linvel = abs(min_linvel)

    def __call__(self):
        linvel = self.body.node().get_linear_velocity()[2]
        return linvel < -self.min_linvel


class Inclusion:
    _num_objects = 2

    def __init__(self, inside, outside, world):
        self.inside = inside
        self.outside = outside
        self.world = world

    def __call__(self):
        ci = self.inside.get_net_transform().get_pos()
        co = self.outside.get_net_transform().get_pos()
        # Check if there's any body between the two bodies.
        closest = self.world.ray_test_closest(co, ci).get_node()
        if closest != self.inside.node():
            return False
        # Check for visibility of inside body.
        # Shape bounds are always SphereBounds for BulletBodyNodes.
        out_radius = self.outside.node().get_shape_bounds().get_radius()
        # Check in all XY directions.
        directions = [Vec3(-out_radius, 0, 0),
                      Vec3(out_radius, 0, 0),
                      Vec3(0, -out_radius, 0),
                      Vec3(0, out_radius, 0)]
        hits = [self.world.ray_test_closest(ci, ci+d).get_node()
                for d in directions]
        return all(hit == self.outside.node() for hit in hits)


class NoContact:
    _num_objects = 2

    def __init__(self, first, second, world):
        self.first = first
        self.second = second
        self.world = world

    def __call__(self):
        contact = self.world.contact_test_pair(
            self.first.node(), self.second.node()
        ).get_num_contacts()
        return not contact


class NotMoving:
    _num_objects = 1

    def __init__(self, body, pos_tol=1e-3, hpr_tol=1):
        self.body = body
        init_xform = body.get_net_transform()
        self.init_pos = init_xform.get_pos()
        self.init_hpr = init_xform.get_hpr()
        self.pos_tol = pos_tol
        self.hpr_tol = hpr_tol

    def __call__(self):
        xform = self.body.get_net_transform()
        pos = xform.get_pos()
        hpr = xform.get_hpr()
        # compare_to returns 0 if vectors are equal within tolerance.
        return (not pos.compare_to(self.init_pos, self.pos_tol)
                and not hpr.compare_to(self.init_hpr, self.hpr_tol))


class Pivoting:
    _num_objects = 1

    def __init__(self, body, min_angvel=0):
        self.body = body
        self.min_angvel_sq = min_angvel ** 2

    def __call__(self):
        angvel_sq = self.body.node().get_angular_velocity().length_squared()
        return angvel_sq > self.min_angvel_sq


class Rising:
    _num_objects = 1

    def __init__(self, body, min_linvel=0):
        self.body = body
        self.min_linvel = abs(min_linvel)

    def __call__(self):
        linvel = self.body.node().get_linear_velocity()[2]
        return linvel > self.min_linvel


class RollingOn:
    _num_objects = 2

    def __init__(self, rolling, support, world, min_angvel=0):
        self.rolling = rolling
        self.support = support
        self.world = world
        self.min_angvel_sq = min_angvel ** 2

    def __call__(self):
        contact = self.world.contact_test_pair(
            self.rolling.node(), self.support.node()
        ).get_num_contacts()
        if contact:
            angvel_sq = self.rolling.node().get_angular_velocity(
            ).length_squared()
            return angvel_sq > self.min_angvel_sq
        else:
            return False


class Stopping:
    _num_objects = 1

    def __init__(self, body, max_linvel=1e-3, max_angvel=1):
        self.body = body
        self.max_linvel_sq = max_linvel ** 2
        self.max_angvel_sq = max_angvel ** 2

    def __call__(self):
        linvel_sq = self.body.node().get_linear_velocity().length_squared()
        angvel_sq = self.body.node().get_angular_velocity().length_squared()
        return (linvel_sq < self.max_linvel_sq
                and angvel_sq < self.max_angvel_sq)


class Toppling:
    _num_objects = 1

    def __init__(self, body, angle):
        self.body = body
        self.angle = angle
        self.start_angle = body.get_r()

    def __call__(self):
        return abs(self.body.get_r() - self.start_angle) >= self.angle + 1


def needs_world(event_type):
    return event_type in (Contact, Inclusion, NoContact, RollingOn)
