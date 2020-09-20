from math import atan, degrees
import math

import random

DENSITY = 1

# Randomness: Size of ball, standard = .02
BALL_RADIUS = random.uniform(0.018, 0.032)   # [m]
BALL_MASS = BALL_RADIUS**3 * math.pi * (4/3) * DENSITY  # [kg]
BALL_RESTITUTION = 0.3

TOP_TRACK_LWHT = (0.25, 0.10, 0.002, 0.005)  # [m]
BOTTOM_TRACK_LWHT = TOP_TRACK_LWHT  # [m]
HIGH_PLANK_LWH = (0.05, 0.10, 0.02)  # [m]
BASE_PLANK_LWH = (1, 0.10, 0.005)  # [m]

OCCLUDER_LWH = (random.uniform(.08, .2), 0.001, 0.6)  # [m]

# Randomness: Size of plank, standard = .05
length = random.uniform(0.04, 0.06)
BLOCK_LWH = (length, length, length)  # [m]
BLOCK_MASS = BLOCK_LWH[0] * BLOCK_LWH[1] * BLOCK_LWH[2] * DENSITY # [kg]
HIGH_PLANK_RESTITUTION = 0.3

size = random.uniform(.9, 1.1)
FLAT_SUPPORT_LWH = (.1*size, .015*size, .04*size)  # [m]
HIGH_PLANK_MASS = FLAT_SUPPORT_LWH[0] * FLAT_SUPPORT_LWH[1] * FLAT_SUPPORT_LWH[2] * DENSITY # [kg]


# print(str(BALL_MASS) + str(HIGH_PLANK_MASS))

# Randomness: plank or ball
if random.random() < 1:
# if False:
    movingObject = {
            'name': "ball",
            'type': "Ball",
            'args': {
                'radius': BALL_RADIUS,
                # Randomness: force on object, standard = 25
                'force': (.04,0,0),
                'b_mass': BALL_MASS,
                'b_restitution': BALL_RESTITUTION
            },
            # Randomness: position of object
            'xform': {
                'value': [-TOP_TRACK_LWHT[0]/2-.7, .2, BALL_RADIUS+.002,
                          0, 0, 0]
            }
        }
else:
    movingObject = {
            'name': "plank",
            'type': "Box",
            'args': {
                'extents': BLOCK_LWH,
                # Randomness: force on object
                'force': (random.uniform(.1, .12),0,0),
                'b_mass': BLOCK_MASS,
                'b_restitution': HIGH_PLANK_RESTITUTION
            },
            # Randomness: position of object
            'xform': {
                'value': [
                    -TOP_TRACK_LWHT[0]*3,
                    .2,
                    BLOCK_LWH[0]/2,
                    0, 0, 0
                ],
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
            },
        },
        movingObject,
        {
            'name': "plank2",
            'type': "Box",
            'args': {
                'extents': FLAT_SUPPORT_LWH,
                # Randomness: force on plank, standard: .005
                'force': (0,0,0),
                'b_mass': HIGH_PLANK_MASS,
                'b_restitution': HIGH_PLANK_RESTITUTION
            },
            # Randomness: position of plank
            'xform': {
                'value': [
                    .18,
                    .2,
                    FLAT_SUPPORT_LWH[0]/2,
                    45, 0, 90
                ],
            }
        },
                {
            'name': "occluder",
            'type': "Box",
            'args': {
                'extents': OCCLUDER_LWH,
                'force': (0,0,0)
            },
            # Randomness: position of occluder
            'xform': {
                'value': [.55, .3, .05, 0, 0, 90],
            }
        },        
    ],
}
