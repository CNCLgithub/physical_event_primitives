import pyglet
import pymunk
import random
import pygame
import pymunk.pygame_util
from pymunk.pyglet_util import DrawOptions

camera = pygame.Vector2((0, 0))
clock = pygame.time.Clock()

space = pymunk.Space()
space.gravity = 0, -1000

window = pyglet.window.Window(1280, 720, "tester", resizable=False)
options = DrawOptions()


mass = 1
radius = 30


def create_static(n):
    length = []
    for pos in range(n):
        length.append((random.randrange(0, 500), random.randrange(0, 500)))
    x_position = []
    for pos in range(n):
        x_position.append(random.randrange(0, 1280))
    y_position = []
    for pos in range(n):
        y_position.append(random.randrange(0, 720))

    for pos in range(n):
        segment_shape = pymunk.Segment(space.static_body, (0, 0), length[pos], 2)
        segment_shape.body.position = x_position[pos], y_position[pos]
        segment_shape.elasticity = 0.8
        segment_shape.friction = 1.0
        space.add(segment_shape)


def create_joint(n):
    for seg in range(n):
        x = random.randrange(0, 1280)
        y = random.randrange(0, 720)
        # creates a center for rotation
        rotation_center_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        rotation_center_body.position = (x, y)

        # creates a line segment

        segment_moment = pymunk.moment_for_segment(10, (-255, 0), (255, 0), 2)
        segment_body = pymunk.Body(10, segment_moment)
        segment_body.position = (x, y)
        segment_shape = pymunk.Segment(segment_body, (-255, 0), (255, 0), 2)
        segment_shape.friction = 1.0
        segment_shape.elasticity = 0.8

        rotation_center_joint = pymunk.PinJoint(segment_body, rotation_center_body, (0, 0), (0, 0))

        space.add(segment_shape, segment_body, rotation_center_joint)


def add_block():
    block_shape = pymunk.Poly.create_box(None, size=(50, 50))
    block_moment = pymunk.moment_for_poly(mass, block_shape.get_vertices())
    block_body = pymunk.Body(mass, block_moment)
    block_body.position = random.randint(0, 720), 600
    block_shape.body = block_body
    block_shape.elasticity = 0.8
    block_shape.friction = 1.0
    space.add(block_body, block_shape)


def add_circle():
    circle_moment = pymunk.moment_for_circle(mass, 0, radius)
    circle_body = pymunk.Body(mass, circle_moment)
    circle_body.position = random.randint(0, 720), 600
    circle_shape = pymunk.Circle(circle_body, radius)
    circle_shape.elasticity = 0.8
    circle_shape.friction = 1.0
    space.add(circle_body, circle_shape)


for i in range(1):
    if bool(random.getrandbits(1)):
        if bool(random.getrandbits(1)):
            add_circle()
        else:
            add_block()

circle_moment_default = pymunk.moment_for_circle(mass, 0, radius)
circle_body_default = pymunk.Body(mass, circle_moment_default)
circle_body_default.position = 10, 600
circle_shape_default = pymunk.Circle(circle_body_default, radius)
circle_shape_default.friction = 1.0
circle_shape_default.elasticity = 0.8
space.add(circle_body_default, circle_shape_default)

segment_body = pymunk.Body(body_type=pymunk.Body.STATIC)
segment_shape = pymunk.Segment(segment_body, (0, 0), (10000, 0), 10)
segment_shape.friction = 1.0
segment_shape.elasticity = 0.8
segment_body.position = -10, 0

triangle_shape = pymunk.Poly(None, ((0, 0), (0, 100), (100, 0)))
triangle_body = pymunk.Body(body_type=pymunk.Body.STATIC)
triangle_body.position = 0, 50
triangle_shape.body = triangle_body

table_body = pymunk.Body(body_type=pymunk.Body.STATIC)
table_shape = pymunk.Segment(table_body, (0, 0), (100, 0), 2)
table_body.position = 100, 50

space.add(segment_body, segment_shape, triangle_body, triangle_shape, table_body, table_shape)


create_static(2)
create_joint(2)

for shape in space.shapes:
    if shape.body.position.y < 0:
        space.remove(shape)


@window.event
def on_draw():
    window.clear()
    space.debug_draw(options)


@window.event
def on_mouse_press(x, y, button, modifiers):
    circle_moment = pymunk.moment_for_circle(1, 0, 14)
    circle_body = pymunk.Body(1, circle_moment)
    circle_body.position = x, y
    circle = pymunk.Circle(circle_body, 14)
    circle.friction = 1.0
    circle.elasticity = 0.8
    space.add(circle_body, circle)


def update(dt):
    space.step(dt)


if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1.0 / 60.0)
    pyglet.app.run()
