from math import atan, degrees
import math

import random

DENSITY = 1

# Randomness: Size of ball, standard = .02
BALL_RADIUS = .025   # [m]
BALL_MASS = BALL_RADIUS**3 * math.pi * (4/3) * DENSITY  # [kg]
BALL_RESTITUTION = 0.3

TOP_TRACK_LWHT = (0.25, 0.10, 0.002, 0.005)  # [m]
BOTTOM_TRACK_LWHT = TOP_TRACK_LWHT  # [m]
HIGH_PLANK_LWH = (0.05, 0.10, 0.02)  # [m]
BASE_PLANK_LWH = (1, 0.10, 0.005)  # [m]

OCCLUDER_LWH = (random.uniform(.08, .2), 0.001, 0.2)  # [m]


# Randomness: Size of plank, standard = .05
length = random.uniform(0.04, 0.06)
FLAT_SUPPORT_LWH = (length, length, length)  # [m]
HIGH_PLANK_MASS = FLAT_SUPPORT_LWH[0] * FLAT_SUPPORT_LWH[1] * FLAT_SUPPORT_LWH[2] * DENSITY # [kg]
HIGH_PLANK_RESTITUTION = 0.3

# Randomness: Size of Goblet, standard: GOBLET_R1 = .036
GOBLET_HEIGHT = 0.08  # [m]
GOBLET_R1 = .04  # [m]
GOBLET_R2 = 0.03  # [m]
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
                'force': (.03,0,0),
                'b_mass': BALL_MASS,
                'b_restitution': BALL_RESTITUTION
            },
            # Randomness: position of object
            'xform': {
                'value': [-.3, BALL_RADIUS*2, BALL_RADIUS+.002,
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
            # Randomness: position of object
            'xform': {
                'value': [
                    -TOP_TRACK_LWHT[0]/2-.7, BALL_RADIUS*2, FLAT_SUPPORT_LWH[0]/2,
                          0, 0, 0
                ],
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
                -.1,
                .04+(random.uniform(.01,.02)),
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
                -.1,
                .04+(random.uniform(.01,.02)),
                FLAT_SUPPORT_LWH[0]/2,
                0, 0, 90
                ],
            }
        }

if random.random() < 1:
    movingObject3 = {
        'name': "ball4",
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
                .55,
                .04+(random.uniform(.01,.02)),
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
            # Randomness: position of object
            'xform': {
                'value': [
                .55,
                .04+(random.uniform(.01,.02)),
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
        movingObject,
        movingObject2,
        movingObject3,
        {
            'name': "occluder",
            'type': "Box",
            'args': {
                'extents': OCCLUDER_LWH,
                'force': (0,0,0)
            },
            # Randomness: position of occluder
            'xform': {
                'value': [.28, random.uniform(.025,.3), .05, 0, 0, 90],
            }
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
                'value': [.54, TOP_TRACK_LWHT[1]/2+.01, .20, 0, 0, 0]
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
        'parent': "track",
        # Randomness: ball location
        'xform': {
            'value': [-TOP_TRACK_LWHT[0]/2+.13,
                0,
                FLAT_SUPPORT_LWH[0]/2,
                0.09, 0, 0],
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
            'value': [.53, 0.4, BALL_RADIUS+.002,
                      0, 0, 0]
        }
    },
    {
            'name': "plank4",
            'type': "Box",
            'args': {
                'extents': (.04, .04, .04),
                # Randomness: force on plank, standard: .005
                'force': (0,0,0),
                'b_mass': 0,
                'b_restitution': HIGH_PLANK_RESTITUTION
            },
             # Randomness: plank location
             'xform': {
             'value': [
                -.1,
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
                'extents': (.06, .06, .06),
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
            'name': "track2",
            'type': "Track",
            'args': {
                'extents': TOP_TRACK_LWHT,
            },
            'xform': {
                # Randomness: track height and angle 
                # 10+(random.uniform(-10,10))
                'value': [-.1, TOP_TRACK_LWHT[1]/2+.01, .30, 0, 0, 0]
            }
        },
        {
            'name': "goblet",
            'type': "Goblet",
            'args': {
                'extents': [
                    0.07,
                    0.03,
                    GOBLET_R2,
                    GOBLET_EPS]
            },
            # Randomness: position of occluder
            'xform': {
                'value': [0.05, .65, GOBLET_R1-.002, 0, 10, -90],
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
            'parent': "track2",
            # Randomness: position of goblet
            'xform': {
                'value': [-TOP_TRACK_LWHT[0]/2+.12,
                0,
                FLAT_SUPPORT_LWH[0]/2 + .018,
                0, 90, 0],
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
                'value': [.2, TOP_TRACK_LWHT[1]/2+.01, .40, 0, 0, 0]
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
            'parent': "track3",
            # Randomness: position of goblet
            'xform': {
                'value': [-TOP_TRACK_LWHT[0]/2+.12,
                0,
                FLAT_SUPPORT_LWH[0]/2-.02,
                0, 0, 0],
            }
        },

    ],
}