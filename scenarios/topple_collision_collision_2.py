
import math
import random

DENSITY = 1

# Randomness: Size of ball, standard = .02
BALL_RADIUS = .025   # [m]
BALL_MASS = BALL_RADIUS**3 * math.pi * (4/3) * DENSITY  # [kg]
BALL_RESTITUTION = 0.3

PLANK_RESTITUTION = 0.3
TOP_TRACK_LWHT = (0.25, 0.10, 0.002, 0.005)  # [m]
# Randomness: size of plank, standard: 1
length = random.uniform(0.04, 0.06)
BLOCK_LWH = (length, length, length)  # [m]
BLOCK_MASS = BLOCK_LWH[0] * BLOCK_LWH[1] * BLOCK_LWH[2] * DENSITY

size = random.uniform(.9, 1.1)
FLAT_LWH = (.1*size, .015*size, .04*size)  # [m]
FLAT_MASS = FLAT_LWH[0] * FLAT_LWH[1] * FLAT_LWH[2] * DENSITY # [kg]

# Randomness: Size of Goblet, standard: GOBLET_R1 = .036
GOBLET_HEIGHT = 0.11  # [m]
GOBLET_R1 = .05  # [m]
GOBLET_R2 = 0.025  # [m]
GOBLET_EPS = .002  # [m]

movingObject = {
        'name': "ball2",
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
                .24,
                FLAT_LWH[0]/2 + BALL_RADIUS+.18,
                BALL_RADIUS+.002,
                0, 0, 0
            ]
        }
}

# if True:
if random.random() < 1:
    movingObject2 = {
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
                0,
                FLAT_LWH[0]/2 + BALL_RADIUS+.12,
                BALL_RADIUS,
                45, 0, 90
            ],
        }
    }
else:
    movingObject2 = {
            'name': "plank2",
            'type': "Box",
            'args': {
                'extents': BLOCK_LWH,
                'force': (0,0,0),
                'b_mass': BLOCK_MASS,
                'b_restitution': HIGH_PLANK_RESTITUTION
            },
            # Randomness: position of object
            'xform': {
                'value': [
                    0,
                    .4,
                    BLOCK_LWH[0]/2,
                    45, 0, 90
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
                'extents': FLAT_LWH,
                # Randomness: force on plank, standard: .005
                'force': (0,random.uniform(.012,.012),0),
                'b_mass': FLAT_MASS,
                'b_restitution': PLANK_RESTITUTION
            },
            # Randomness: position of plank
            'xform': {
                'value': [
                    .3,
                    .2,
                    FLAT_LWH[0]/2,
                    45, 0, 90
                ],
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
            'value': [ .24,
                FLAT_LWH[0]/2 + BALL_RADIUS+.48,
                BALL_RADIUS+.002,
                0, 0, 0]
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
            'value': [ 0,
                FLAT_LWH[0]/2 + BALL_RADIUS+.5,
                BALL_RADIUS,
                45, 0, 90]
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
                'b_restitution': PLANK_RESTITUTION
            },
             # Randomness: plank location
             'xform': {
             'value': [
                .5,
                .45,
                .03,
                0, 0, 0
                ],
            }
        },   
         {
            'name': "plank3",
            'type': "Box",
            'args': {
                'extents': (.04, .04, .04),
                # Randomness: force on plank, standard: .005
                'force': (0,0,0),
                'b_mass': 0,
                'b_restitution': PLANK_RESTITUTION
            },
             # Randomness: plank location
             'xform': {
             'value': [
                .15,
                .4,
                .03,
                0, 0, 0
                ],
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
                'b_restitution': PLANK_RESTITUTION
            },
             # Randomness: plank location
             'xform': {
             'value': [
                -.15,
                .6,
                .03,
                0, 0, 0
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
                    GOBLET_EPS
                ]
            },
            # Randomness: position of goblet
            'xform': {
                'value': [.55, GOBLET_R1, 0, 0, 0, 0],
            }
        },
        {
            'name': "track",
            'type': "Track",
            'args': {
                'extents': TOP_TRACK_LWHT,
            },
            'xform': {
                # Randomness: track height 
                # 10+(random.uniform(-10,10))
                'value': [-.1, TOP_TRACK_LWHT[1]/2+.01, .40, 0, 0, 0]
            }
        },
        {
        'name': "cylinder",
        'type': "Cylinder",
        'args': {
            'extents': [0.02, 0.05]
        },
        'parent': "track",
        # Randomness: ball location
        'xform': {
            'value': [-TOP_TRACK_LWHT[0]/2+.02, 0, .026,
                      0, 0, 0]
        }
    },
        movingObject,   
        movingObject2 
    ],
}
