from math import atan, degrees
import math
import random

DENSITY = 1

# Randomness: Size of ball, standard = .02
BALL_RADIUS = random.uniform(0.018, 0.032)    # [m]
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

# Randomness: Size of Goblet, standard: GOBLET_R1 = .036
GOBLET_HEIGHT = 0.08  # [m]
GOBLET_R1 = .04  # [m]
GOBLET_R2 = 0.03  # [m]
GOBLET_EPS = .002  # [m]

# Randomness: plank or ball
if random.random() < 0:
    movingObject = {
        'name': "plank",
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
else:
    movingObject = {
        'name': "ball",
        'type': "Ball",
        'args': {
            'radius': BALL_RADIUS,
            'force': (random.uniform(.015,.025),0,0),
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
                'value': [-.2, TOP_TRACK_LWHT[1]/2+.01, .45, 0, 0, 0]
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
                'value': [.3, .15, .05, 0, 0, 90],
            }
        },
        movingObject,
        {
            'name': "track2",
            'type': "Track",
            'args': {
                'extents': TOP_TRACK_LWHT,
            },
            'xform': {
                # Randomness: track height
                # 10+(random.uniform(-10,10))
                'value': [0.6, TOP_TRACK_LWHT[1]/2+.01, .30, 0, 0, 0]
            }
        },
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
                    .6,
                    .08,
                    FLAT_SUPPORT_LWH[0]/2,
                    45, 0, 90
                ],
            }
        }, 
        {
            'name': "plank3",
            'type': "Box",
            'args': {
                'extents': FLAT_SUPPORT_LWH,
                # Randomness: force on plank, standard: .005
                'force': (0,0,0),
                'b_mass': HIGH_PLANK_MASS,
                'b_restitution': HIGH_PLANK_RESTITUTION
            },
            'parent': "track2",
            # Randomness: position of plank
            'xform': {
                'value': [
                    -TOP_TRACK_LWHT[0]/2+.13,
                0,
                FLAT_SUPPORT_LWH[0]/2 + .005,
                45, 0, 90
                ],
            }
        }, 
        {
            'name': "plank4",
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
                    .56,
                    .4,
                    FLAT_SUPPORT_LWH[0]/2,
                    45, 0, 90
                ],
            }
        }, 
         {
            'name': "plank5",
            'type': "Box",
            'args': {
                'extents': (.07, .07, .07),
                # Randomness: force on plank, standard: .005
                'force': (0,0,0),
                'b_mass': 0,
                'b_restitution': HIGH_PLANK_RESTITUTION
            },
             # Randomness: plank location
             'xform': {
             'value': [
                .18,
                .63,
                .034,
                0, 0, 0
                ],
            }
        }, 
         {
        'name': "cylinder",
        'type': "Cylinder",
        'args': {
            'extents': [0.02, 0.05]
        },
        # Randomness: cylinder location
        'xform': {
            'value': [.04, 0.9, 0.12,
                      0, 0, 0]
        }
    },
    {
        'name': "ball4",
        'type': "Ball",
        'args': {
            'radius': BALL_RADIUS,
            'force': (0,0,0),
            'b_mass': 0,
            'b_restitution': BALL_RESTITUTION
        },
        # Randomness: ball location
        'xform': {
            'value': [.3, 0.6, BALL_RADIUS+.002,
                      0, 0, 0]
        }
    },
    {
        'name': "ball5",
        'type': "Ball",
        'args': {
            'radius': random.uniform(0.032, 0.043),
            'force': (0,0,0),
            'b_mass': 0,
            'b_restitution': BALL_RESTITUTION
        },
        # Randomness: ball location
        'xform': {
            'value': [-.1, 0.6, BALL_RADIUS+.015,
                      0, 0, 0]
        }
    },
    {
            'name': "goblet3",
            'type': "Goblet",
            'args': {
                'extents': [
                    GOBLET_HEIGHT,
                    GOBLET_R1,
                    GOBLET_R2,
                    GOBLET_EPS
                ]
            },
            # Randomness: position of goblet
            'xform': {
                'value': [-.2, 0.4, 0.043, 0, 0, 86],
            }
        },

    ],
}