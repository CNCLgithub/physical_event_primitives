import math

import random

DENSITY = 1

# Randomness: Size of ball, standard = .02
BALL_RADIUS = random.uniform(0.018, 0.032)   # [m]
BALL_MASS = BALL_RADIUS**3 * math.pi * (4/3) * DENSITY  # [kg]
BALL_RESTITUTION = 0.3

PLANK_RESTITUTION = 0.3
TOP_TRACK_LWHT = (0.25, 0.10, 0.002, 0.005)  # [m]
# Randomness: size of plank, standard: 1
length = random.uniform(0.04, 0.06)
BLOCK_LWH = (length, length, length)  # [m]
BLOCK_MASS = BLOCK_LWH[0] * BLOCK_LWH[1] * BLOCK_LWH[2] * DENSITY


HIGH_PLANK_LWH = (0.235, 0.023, 0.008)  # [m]
HIGH_PLANK_RESTITUTION = 0.03

OCCLUDER_LWH = (random.uniform(.08, .2), 0.001, 0.2)  # [m]

# Randomness: size of plank, standard: 1
size = random.uniform(.9, 1.1)
FLAT_SUPPORT_LWH = (.1*size, .015*size, .04*size)  # [m]
HIGH_PLANK_MASS = FLAT_SUPPORT_LWH[0] * FLAT_SUPPORT_LWH[1] * FLAT_SUPPORT_LWH[2] * DENSITY # [kg]

if random.random() < 0:
    movingObject = {
            'name': "ball",
            'type': "Ball",
            'args': {
                'radius': BALL_RADIUS,
                # Randomness: force on object
                'force': (0,0,0),
                'b_mass': BALL_MASS,
                'b_restitution': BALL_RESTITUTION
            },
            'xform': {
                'value': [
                    .11,
                    .2,
                    BALL_RADIUS+.002,
                    0, 0, 0
                ]
            }
    }
else:
    movingObject = { 
            'name': "plank2",
            'type': "Box",
            'args': {
                'extents': BLOCK_LWH,
                # Randomness: force on object, standard: .01
                'force': (0,0,0),
                'b_mass': BLOCK_MASS,
                'b_restitution': PLANK_RESTITUTION
            },
            'xform': {
                'value': [
                    .09,
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
            }
        },
        {
            'name': "plank",
            'type': "Box",
            'args': {
                'extents': FLAT_SUPPORT_LWH,
                # Randomness: force on plank, standard: .005
                'force': (random.uniform(-.009,-.009),0,0),
                'b_mass': HIGH_PLANK_MASS,
                'b_restitution': HIGH_PLANK_RESTITUTION
            },
            # Randomness: position of plank
            'xform': {
                'value': [
                    .175,
                    .2,
                    FLAT_SUPPORT_LWH[0]/2,
                    90, 0, 90
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
                'value': [.26, .3, .05, 0, 0, 90],
            }
        }, 
        movingObject      
    ],
}
