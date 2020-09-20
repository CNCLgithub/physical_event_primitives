from math import atan, degrees
import math
import random

DENSITY = 1
# Randomness: ball size, standard: .008
BALL_RADIUS = random.uniform(0.018, 0.032)   # [m]
BALL_MASS = BALL_RADIUS**3 * math.pi * (4/3) * DENSITY  # [kg]
BALL_RESTITUTION = 0.8

TOP_TRACK_LWHT = (0.3, 0.05, 0.01, 0.006)  # [m]
BOTTOM_TRACK_LWHT = TOP_TRACK_LWHT  # [m]

HIGH_PLANK_LWH = (0.235, 0.023, 0.008)  # [m]
HIGH_PLANK_RESTITUTION = 0.8
BASE_PLANK_LWH = (0.235, 0.001, 0.1)  # [m]

# Randomness: plank size, standard: 1
length = random.uniform(0.04, 0.06)
FLAT_SUPPORT_LWH = (length, length, length)  # [m]
HIGH_PLANK_MASS = FLAT_SUPPORT_LWH[0] * FLAT_SUPPORT_LWH[1] * FLAT_SUPPORT_LWH[2] * DENSITY # [kg]

size = random.uniform(.9, 1.1)
FLAT_LWH = (.1*size, .015*size, .04*size)  # [m]
FLAT_MASS = FLAT_LWH[0] * FLAT_LWH[1] * FLAT_LWH[2] * DENSITY # [kg]

# Randomness: plank or ball
if random.random() < 0:
    movingObject = {
        'name': "plank",
        'type': "Box",
        'args': {
            'extents': FLAT_SUPPORT_LWH,
            'force': (random.uniform(.03, .04),0,0),
            'b_mass': HIGH_PLANK_MASS,
            'b_restitution': HIGH_PLANK_RESTITUTION
        },
        'parent': "track",
        # Randomness: plank location
        'xform': {
            'value': [
                -TOP_TRACK_LWHT[0]/2+.01,
                0,
                FLAT_SUPPORT_LWH[0]/2 + .005,
                0, 0, 90
            ],
        }
    }
else:
    movingObject = {
        'name': "ball",
        'type': "Ball",
        'args': {
            'radius': BALL_RADIUS,
            'force': (0,0,0),
            'b_mass': BALL_MASS,
            'b_restitution': BALL_RESTITUTION
        },
        'parent': "track",
        # Randomness: ball location
        'xform': {
            'value': [-TOP_TRACK_LWHT[0]/2+.01, 0, BALL_RADIUS+.002,
                      0, 0, 0]
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
        {
            'name': "track",
            'type': "Track",
            'args': {
                'extents': TOP_TRACK_LWHT,
            },
            'xform': {
                # Randomness: track height and angle 
                # 10+(random.uniform(-10,10))
                'value': [-.1, TOP_TRACK_LWHT[1]/2+.01, .3+(random.uniform(-.1,.1)), 0, 0, 10+(random.uniform(-10,10))]
            }
        },
        movingObject,
        {        
            'name': "plank2",
            'type': "Box",
            'args': {
                'extents': FLAT_LWH,
                # Randomness: force on plank, standard: .005
                'force': (0,0,0),
                'b_mass': FLAT_MASS,
                'b_restitution': HIGH_PLANK_RESTITUTION
            },
            # Randomness: position of plank
            'xform': {
                'value': [
                    .5,
                    .04+(random.uniform(.01,.02)),
                    FLAT_LWH[0]/2+.002,
                    45, 0, 90
                ],
            }
        }
    ]
}
