from math import atan, degrees
import math
import random

DENSITY = 1
# Randomness: ball size, standard: .008
BALL_RADIUS = random.uniform(0.018, 0.032)   # [m]
BALL_MASS = BALL_RADIUS**3 * math.pi * (4/3) * DENSITY  # [kg]
BALL_RESTITUTION = 0.8

TOP_TRACK_LWHT = (0.3, 0.05, 0.01, 0.006)  # [m]

HIGH_PLANK_LWH = (0.235, 0.023, 0.008)  # [m]
HIGH_PLANK_RESTITUTION = 0.8
BASE_PLANK_LWH = (0.235, 0.001, 0.1)  # [m]

# Randomness: plank size, standard: 1
length = random.uniform(0.04, 0.06)
FLAT_SUPPORT_LWH = (length, length, length)  # [m]
HIGH_PLANK_MASS = FLAT_SUPPORT_LWH[0] * FLAT_SUPPORT_LWH[1] * FLAT_SUPPORT_LWH[2] * DENSITY # [kg]

# Randomness: Size of Goblet, standard: GOBLET_R1 = .036
GOBLET_HEIGHT = 0.2  # [m]
GOBLET_R1 = .05  # [m]
GOBLET_R2 = 0.05  # [m]
GOBLET_EPS = .002  # [m]

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
        'parent': "floor",
        # Randomness: position of object
        'xform': {
            'value': [
                .1,
                .05,
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
            # Randomness: position of object
            'xform': {
                'value': [
                    .1,
                    .05,
                    FLAT_SUPPORT_LWH[0]/2,
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
        {
            'name': "track",
            'type': "Track",
            'args': {
                'extents': TOP_TRACK_LWHT,
            },
            'xform': {
                # Randomness: track height and angle 
                # 10+(random.uniform(-10,10))
                'value': [-.1, TOP_TRACK_LWHT[1]/2+.01, .3+(random.uniform(-.1,.1)), 0, 0, 18]
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
                'value': [GOBLET_HEIGHT*3-.02, .2, GOBLET_R1-.002, 0, 10, -90],
            }
        },   
         {
            'name': "goblet2",
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
                'value': [GOBLET_HEIGHT*3-.02, .4, GOBLET_R1-.002, 0, 10, -90],
            }
        }, 
        {
        'name': "ball3",
        'type': "Ball",
        'args': {
            'radius': BALL_RADIUS,
            'force': (0,0,0),
            'b_mass': 0,
            'b_restitution': BALL_RESTITUTION
        },
        # Randomness: ball location
        'xform': {
            'value': [.1,
                .6,
                BALL_RADIUS+.002,
                0, 0, 90]
        }
    },   

        movingObject,
        movingObject2
    ]
}
