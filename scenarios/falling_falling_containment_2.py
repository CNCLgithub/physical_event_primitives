from math import atan, degrees
import math
import random

DENSITY = 1
# Randomness: ball size, standard: .008 (changed to not random for consistent ball velocity)
BALL_RADIUS = .025   # [m]
BALL_MASS = BALL_RADIUS**3 * math.pi * (4/3) * DENSITY  # [kg]
BALL_RESTITUTION = 0.8

TOP_TRACK_LWHT = (0.43, 0.12, 0.01, 0.01)  # [m]

HIGH_PLANK_LWH = (0.235, 0.023, 0.008)  # [m]
HIGH_PLANK_RESTITUTION = 0.8
BASE_PLANK_LWH = (0.235, 0.001, 0.1)  # [m]

OCCLUDER_LWH = (random.uniform(.08, .2), 0.001, 0.6)  # [m]

# Randomness: plank size, standard: 1
length = random.uniform(0.04, 0.06)
FLAT_SUPPORT_LWH = (length, length, length)  # [m]
HIGH_PLANK_MASS = FLAT_SUPPORT_LWH[0] * FLAT_SUPPORT_LWH[1] * FLAT_SUPPORT_LWH[2] * DENSITY # [kg]

# Randomness: Size of Goblet, standard: GOBLET_R1 = .036
GOBLET_HEIGHT = 0.11  # [m]
GOBLET_R1 = .05  # [m]
GOBLET_R2 = 0.025  # [m]
GOBLET_EPS = .002  # [m]

# Randomness: plank or ball
if random.random() < 0:
    movingObject = {
        'name': "plank",
        'type': "Box",
        'args': {
            'extents': FLAT_SUPPORT_LWH,
            'force': .001,
            'b_mass': HIGH_PLANK_MASS,
            'b_restitution': HIGH_PLANK_RESTITUTION
        },
        'parent': "track",
        # Randomness: plank location
        'xform': {
            'value': [
                -TOP_TRACK_LWHT[0]/2-.03,
                0,
                FLAT_SUPPORT_LWH[0]/2 + .005,
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
            'force': (0.001,0,0),
            'b_mass': BALL_MASS,
            'b_restitution': BALL_RESTITUTION
        },
        'parent': "track",
        # Randomness: ball location
        'xform': {
            'value': [-TOP_TRACK_LWHT[0]/2-.03, 0, BALL_RADIUS+.002,
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
                'extents': (0.63, 0.1, 0.01, 0.006),
            },
            'xform': {
                # Randomness: track height 
                # 10+(random.uniform(-10,10))
                'value': [-.066, TOP_TRACK_LWHT[1]/2+.01, .45, 0, 0, 0.5]
            }
        },
        {
            'name': "track2",
            'type': "Track",
            'args': {
                'extents': TOP_TRACK_LWHT,
            },
            'xform': {
                # Randomness: track height and angle 
                # 10+(random.uniform(-10,10))
                'value': [.36, TOP_TRACK_LWHT[1]/2+.01, .20, 0, 0, 0]
            }
        },
        {
            'name': "track3",
            'type': "Track",
            'args': {
                'extents': TOP_TRACK_LWHT,
            },
            'xform': {
                # Randomness: track height and angle 
                # 10+(random.uniform(-10,10))
                'value': [-.05, TOP_TRACK_LWHT[1]/2+.01, .30, 0, 0, 0]
            }
        },
        {
        'name': "cylinder2",
        'type': "Cylinder",
        'args': {
            'extents': [0.02, 0.05]
        },
        'parent': "track3",
        # Randomness: ball location
        'xform': {
            'value': [-TOP_TRACK_LWHT[0]/2+.02, 0, .026,
                      0, 0, 0]
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
                    GOBLET_EPS
                ]
            },
            # Randomness: position of goblet
            'xform': {
                'value': [.69, GOBLET_R1, 0.01, 0, 0, -15],
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
                    GOBLET_EPS
                ]
            },
            # Randomness: position of goblet
            'xform': {
                'value': [.69, GOBLET_R1, 0.37, 0, 0, 230],
            }
        },
        {
        'name': "ball5",
        'type': "Ball",
        'args': {
            'radius': BALL_RADIUS,
            'force': (0,0,0),
            'b_mass': 0,
            'b_restitution': BALL_RESTITUTION
        },
        # Randomness: ball location
        'xform': {
            'value': [.3, 0.4, BALL_RADIUS+.002,
                      0, 0, 0]
        }
    },
    {
            'name': "plank4",
            'type': "Box",
            'args': {
                'extents': (.05, .05, .05),
                # Randomness: force on plank, standard: .005
                'force': (0,0,0),
                'b_mass': 0,
                'b_restitution': HIGH_PLANK_RESTITUTION
            },
             # Randomness: plank location
             'xform': {
             'value': [
                .5,
                .6,
                .034,
                0, 0, 0
                ],
            }
        }, 
    {
            'name': "plank5",
            'type': "Box",
            'args': {
                'extents': (.03, .03, .03),
                # Randomness: force on plank, standard: .005
                'force': (0,0,0),
                'b_mass': 0,
                'b_restitution': HIGH_PLANK_RESTITUTION
            },
             # Randomness: plank location
             'xform': {
             'value': [
                .1,
                .7,
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
            'value': [-.1, 0.8, 0.1,
                      0, 0, 0]
        }
    },
        movingObject
    ]
}