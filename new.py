import sys
import random
import pygame
from pygame.locals import *
import pyglet
import pymunk
from pymunk.vec2d import Vec2d
import pymunk.pygame_util

space = pymunk.Space()
space.gravity = 0, -1000



def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 700))
    pymunk_layer = pygame.Surface((1000, 700))

    camera = pygame.Vector2((0, 0))
    clock = pygame.time.Clock()

    options = pymunk.pygame_util.DrawOptions(pymunk_layer)

    create_static(2)
    create_joint(2)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or \
                    event.type == KEYDOWN and (event.key in [K_ESCAPE, K_q]):
                return
            elif event.type == KEYDOWN and event.key == K_p:
                pygame.image.save(screen, "pygame_util_demo.png")

        # camera movement
        pressed = pygame.key.get_pressed()
        camera_move = pygame.Vector2()
        if pressed[pygame.K_UP]: camera_move += (0, 1)
        if pressed[pygame.K_LEFT]: camera_move += (1, 0)
        if pressed[pygame.K_DOWN]: camera_move += (0, -1)
        if pressed[pygame.K_RIGHT]: camera_move += (-1, 0)
        if camera_move.length() > 0: camera_move.normalize_ip()
        camera += camera_move * 5

        space.debug_draw(options)
        screen.blit(pymunk_layer, camera)

        pygame.display.flip()

        clock.tick(30)


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


def on_mouse_press(x, y, button, modifiers):
    circle_moment = pymunk.moment_for_circle(1, 0, 14)
    circle_body = pymunk.Body(1, circle_moment)
    circle_body.position = x, y
    circle = pymunk.Circle(circle_body, 14)
    circle.friction = 1.0
    circle.elasticity = 0.8
    space.add(circle_body, circle)


if __name__ == '__main__':
    sys.exit(main())
