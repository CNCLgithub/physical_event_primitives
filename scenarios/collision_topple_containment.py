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

# Randomness: Size of plank, standard = .05
length = random.uniform(0.04, 0.06)
BLOCK_LWH = (length, length, length)  # [m]
BLOCK_MASS = BLOCK_LWH[0] * BLOCK_LWH[1] * BLOCK_LWH[2] * DENSITY # [kg]
HIGH_PLANK_RESTITUTION = 0.3

size = random.uniform(.9, 1.1)
FLAT_SUPPORT_LWH = (.1*size, .015*size, .04*size)  # [m]
HIGH_PLANK_MASS = FLAT_SUPPORT_LWH[0] * FLAT_SUPPORT_LWH[1] * FLAT_SUPPORT_LWH[2] * DENSITY # [kg]

# Randomness: Size of Goblet, standard: GOBLET_R1 = .036
GOBLET_HEIGHT = 0.2  # [m]
GOBLET_R1 = .1  # [m]
GOBLET_R2 = 0.1  # [m]
GOBLET_EPS = .002  # [m]


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
                'force': (.035,0,0),
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
            'name': "goblet",
            'type': "Goblet",
            'args': {
                'extents': [
                    GOBLET_HEIGHT,
                    GOBLET_R1,
                    GOBLET_R2,
                    GOBLET_EPS]
            },
            # Randomness: position of occluder
            'xform': {
                'value': [GOBLET_HEIGHT*3-.17, .2, GOBLET_R1-.002, 0, 10, -90],
            }
        },         
    ],
}
