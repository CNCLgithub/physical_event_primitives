
import math
import random

DENSITY = 1

# Randomness: Size of ball, standard = .02
BALL_RADIUS = random.uniform(0.018, 0.032)   # [m]
BALL_MASS = BALL_RADIUS**3 * math.pi * (4/3) * DENSITY  # [kg]
BALL_RESTITUTION = 0.3

PLANK_RESTITUTION = 0.3
TOP_TRACK_LWHT = (.5, 0.20, 0.01, 0.01)  # [m]
# Randomness: size of plank, standard: 1
length = random.uniform(0.04, 0.06)
BLOCK_LWH = (length, length, length)  # [m]
BLOCK_MASS = BLOCK_LWH[0] * BLOCK_LWH[1] * BLOCK_LWH[2] * DENSITY

size = random.uniform(.9, 1.1)
FLAT_LWH = (.1*size, .015*size, .04*size)  # [m]
FLAT_MASS = FLAT_LWH[0] * FLAT_LWH[1] * FLAT_LWH[2] * DENSITY # [kg]

if random.random() < 1:
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
            'parent': "track",
            'xform': {
                'value': [
                    .127,
                    FLAT_LWH[0]/2 + BALL_RADIUS-.02,
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
            'parent': "track",
            'xform': {
                'value': [
                    .12,
                    FLAT_LWH[0]/2 + BALL_RADIUS+.02,
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
                'extents': FLAT_LWH,
                # Randomness: force on plank, standard: .005
                'force': (0,random.uniform(.009,.009),0),
                'b_mass': FLAT_MASS,
                'b_restitution': PLANK_RESTITUTION
            },
            'parent': "track",
            # Randomness: position of plank
            'xform': {
                'value': [
                    .18,
                    0,
                    FLAT_LWH[0]/2,
                    45, 0, 90
                ],
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
                'value': [.4, TOP_TRACK_LWHT[1]/2+.01, .3+(random.uniform(-.1,.1)), 0, 0, 0]
            }
        },
        movingObject          
    ],
}
