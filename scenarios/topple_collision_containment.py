
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

size = random.uniform(.9, 1.1)
FLAT_LWH = (.1*size, .015*size, .04*size)  # [m]
FLAT_MASS = FLAT_LWH[0] * FLAT_LWH[1] * FLAT_LWH[2] * DENSITY # [kg]

# Randomness: Size of Goblet, standard: GOBLET_R1 = .036
GOBLET_HEIGHT = 0.2  # [m]
GOBLET_R1 = .1  # [m]
GOBLET_R2 = 0.1  # [m]
GOBLET_EPS = .002  # [m]


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
                .24,
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
                'value': [-GOBLET_HEIGHT, .2, GOBLET_R1-.003, 0, 10, 90],
            }
        },       
        movingObject          
    ],
}
