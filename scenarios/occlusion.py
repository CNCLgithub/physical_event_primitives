from math import atan, degrees

import math
import random

DENSITY = 1

# Randomness: size of ball
BALL_RADIUS = 0.02  # [m]
BALL_MASS = BALL_RADIUS * math.pi * (4/3) * DENSITY  # [kg]
BALL_RESTITUTION = 0.8

TOP_TRACK_LWHT = (0.3, 0.025, 0.006, 0.003)  # [m]

# Randomness: size of occluder
HIGH_PLANK_LWH = (0.1, 0.001, 0.4)  # [m]
HIGH_PLANK_RESTITUTION = 0.8

# Randomness: size of plank
FLAT_SUPPORT_LWH = (.02, .025, .02)  # [m]
HIGH_PLANK_MASS = FLAT_SUPPORT_LWH[0] * FLAT_SUPPORT_LWH[1] * FLAT_SUPPORT_LWH[2] * DENSITY # [kg]

# Randomness: Ball or Plank
if random.random() < .5:
    movingObject = {
            'name': "ball",
            'type': "Ball",
            'args': {
                'radius': BALL_RADIUS,
                # Randomness: force on object
                'force': (13,0,0),
                'b_mass': BALL_MASS,
                'b_restitution': BALL_RESTITUTION
            },
            'xform': {
                'value': [-TOP_TRACK_LWHT[0], BALL_RADIUS*4, BALL_RADIUS+.002,
                          0, 0, 0]
            }
    }
else:
    movingObject = { 
            'name': "plank",
            'type': "Box",
            'args': {
                'extents': FLAT_SUPPORT_LWH,
                # Randomness: force on object
                'force': (.01,0,0),
                'b_mass': HIGH_PLANK_MASS,
                'b_restitution': HIGH_PLANK_RESTITUTION
            },
            'xform': {
                'value': [-TOP_TRACK_LWHT[0]/2+.01, 0, FLAT_SUPPORT_LWH[0]/2,
                    0, 0, 90],
            }
    }

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
            }
        },
        movingObject,
        {
            'name': "occluder",
            'type': "Box",
            'args': {
                'extents': HIGH_PLANK_LWH,
                'force': (0,0,0)
            },
            # Randomness: position of occluder
            'xform': {
                'value': [.3, random.uniform(0,.3), .05, 0, 0, 90],
            }
        },
        
    ],
}
