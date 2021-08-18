from math import atan, degrees
import math

import random

DENSITY = 1

# Randomness: Size of ball, standard = .02
BALL_RADIUS = random.uniform(0.018, 0.032)   # [m]
BALL_MASS = BALL_RADIUS**3 * math.pi * (4/3) * DENSITY  # [kg]
BALL_RESTITUTION = 0.3

TOP_TRACK_LWHT = (1, 0.2, .01)  # [m]
BOTTOM_TRACK_LWHT = TOP_TRACK_LWHT  # [m]
HIGH_PLANK_LWH = (0.05, 0.10, 0.02)  # [m]
BASE_PLANK_LWH = (1, 0.10, 0.005)  # [m]

# Randomness: Size of plank, standard = .05
length = random.uniform(0.04, 0.06)
FLAT_SUPPORT_LWH = (length, length, length)  # [m]
HIGH_PLANK_MASS = FLAT_SUPPORT_LWH[0] * FLAT_SUPPORT_LWH[1] * FLAT_SUPPORT_LWH[2] * DENSITY # [kg]
HIGH_PLANK_RESTITUTION = 0.3

# print(str(BALL_MASS) + str(HIGH_PLANK_MASS))

# Randomness: plank or ball
if random.random() < 1:
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
        'parent': "track",
        # Randomness: position of object
        'xform': {
            'value': [-.4, 0, BALL_RADIUS+.002,
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
            'force': (random.uniform(.09, .105),0,0),
            'b_mass': HIGH_PLANK_MASS,
            'b_restitution': HIGH_PLANK_RESTITUTION
        },
        'parent': "track",
        # Randomness: position of object
        'xform': {
            'value': [
                -.4,
                0,
                FLAT_SUPPORT_LWH[0]/2,
                0, 0, 0
            ],
        }
    }

# if True:
if random.random() < 1:
    movingObject2 = {
        'name': "ball2",
        'type': "Ball",
        'args': {
            'radius': BALL_RADIUS,
            'force': (0,0,0),
            'b_mass': BALL_MASS,
            'b_restitution': BALL_RESTITUTION
        },
        'parent': "track",
        # Randomness: position of object
        'xform': {
            'value': [
                0,
                0,
                BALL_RADIUS+.002,
                0, 0, 90
            ],
        }
    }
else:
    movingObject2 = {
            'name': "plank2",
            'type': "Box",
            'args': {
                'extents': FLAT_SUPPORT_LWH,
                'force': (0,0,0),
                'b_mass': HIGH_PLANK_MASS,
                'b_restitution': HIGH_PLANK_RESTITUTION
            },
            'parent': "track",
            # Randomness: position of object
            'xform': {
                'value': [
                    0,
                    0,
                    .025,
                    0, 0, 90
                ],
            }
        }

if random.random() < 1:
    movingObject3 = {
        'name': "ball3",
        'type': "Ball",
        'args': {
            'radius': BALL_RADIUS,
            'force': (0,0,0),
            'b_mass': BALL_MASS,
            'b_restitution': BALL_RESTITUTION
        },
        'parent': "track",
        # Randomness: position of object
        'xform': {
            'value': [
                .4,
                0,
                BALL_RADIUS+.002,
                0, 0, 90
            ],
        }
    }
else:
    movingObject3 = {
            'name': "plank3",
            'type': "Box",
            'args': {
                'extents': FLAT_SUPPORT_LWH,
                'force': (0,0,0),
                'b_mass': HIGH_PLANK_MASS,
                'b_restitution': HIGH_PLANK_RESTITUTION
            },
            'parent': "track",
            # Randomness: position of object
            'xform': {
                'value': [
                    .4,
                    0,
                    .025,
                    0, 0, 90
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
        movingObject2,
        movingObject3,  
        {
            'name': "track",
            'type': "Box",
            'args': {
                'extents': TOP_TRACK_LWHT,
                'force': (0,0,0)
            },
            'xform': {
                # Randomness: track height and angle 
                # 10+(random.uniform(-10,10))
                'value': [0, TOP_TRACK_LWHT[1]/2+.01, .3+(random.uniform(-.1,.1)), 0, -.01, 0]
            }
        },    
    ],
}
