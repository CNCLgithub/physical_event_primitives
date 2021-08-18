
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
GOBLET_HEIGHT = 0.12  # [m]
GOBLET_R1 = .05  # [m]
GOBLET_R2 = 0.05  # [m]
GOBLET_EPS = .001  # [m]


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
                .12,
                FLAT_LWH[0]/2 + BALL_RADIUS+.18,
                BALL_RADIUS+.002,
                0, 0, 0
            ]
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
                'force': (0,.012,0),
                'b_mass': FLAT_MASS,
                'b_restitution': PLANK_RESTITUTION
            },
            # Randomness: position of plank
            'xform': {
                'value': [
                    .18,
                    .2,
                    FLAT_LWH[0]/2,
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
                'value': [-.08, .25, GOBLET_R1, 0, 10, 90],
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
                'value': [-.07, .6, GOBLET_R1+.002, 0, 10, 90],
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
            'value': [.24,
                FLAT_LWH[0]/2 + BALL_RADIUS+.5,
                BALL_RADIUS+.002,
                0, 0, 0]
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
            'value': [.28, 0.8, 0.08,
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
            'value': [-.2,
                .5,
                BALL_RADIUS+.002,
                0, 0, 90]
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
                .2,
                .03,
                0, 0, 0
                ],
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
                'b_restitution': PLANK_RESTITUTION
            },
             # Randomness: plank location
             'xform': {
             'value': [
                .5,
                .5,
                .03,
                0, 0, 0
                ],
            }
        },               
        movingObject          
    ],
}
