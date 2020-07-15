from math import atan, degrees
import math

import random

DENSITY = 1

# Randomness: Size of ball
BALL_RADIUS = random.uniform(0.018, 0.032)   # [m]
BALL_MASS = BALL_RADIUS * math.pi * (4/3) * DENSITY  # [kg]
BALL_RESTITUTION = 0.8

TOP_TRACK_LWHT = (0.25, 0.10, 0.002, 0.005)  # [m]


DATA = {
    'scene': [
        {
            'name': "wall",
            'type': "Plane",
            'args': {
                'normal': [0, 1, 0],
                'distance': 0
            }
        },
        {
            'name': "floor",
            'type': "Plane",
            'args': {
                'normal': [0, 0, 1],
                'distance': 0
            },
        },
        {
            'name': "ball",
            'type': "Ball",
            'args': {
                'radius': BALL_RADIUS,
                # Randomness: force on object
                'force': (random.uniform(20,40),0,0),
                'b_mass': BALL_MASS,
                'b_restitution': BALL_RESTITUTION
            },
            # Randomness: position of object
            'xform': {
                'value': [-TOP_TRACK_LWHT[0]/2-.7, BALL_RADIUS*2, BALL_RADIUS+.02,
                          0, 0, 0]
            }
        },
    ],
}
