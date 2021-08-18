
import math
import random

DENSITY = 1

# Randomness: Size of ball, standard = .02
BALL_RADIUS = random.uniform(0.018, 0.032)   # [m]
BALL_MASS = BALL_RADIUS**3 * math.pi * (4/3) * DENSITY  # [kg]
BALL_RESTITUTION = 0.3

PLANK_RESTITUTION = 0.3

# Randomness: size of plank, standard: 1
size = random.uniform(1.1, 1.1)
FLAT_LWH = (.1*size, .015*size, .04*size)  # [m]
FLAT_MASS = FLAT_LWH[0] * FLAT_LWH[1] * FLAT_LWH[2] * DENSITY # [kg]


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
                'force': (0,random.uniform(.013,.013),0),
                'b_mass': FLAT_MASS,
                'b_restitution': PLANK_RESTITUTION
            },
            # Randomness: position of plank
            'xform': {
                'value': [
                    .2,
                    .2,
                    FLAT_LWH[0]/2,
                    45, 0, 90
                ],
            }
        }, 
        {
            'name': "plank2",
            'type': "Box",
            'args': {
                'extents': FLAT_LWH,
                # Randomness: force on plank, standard: .005
                'force': (0,0,0),
                'b_mass': FLAT_MASS,
                'b_restitution': PLANK_RESTITUTION
            },
            # Randomness: position of plank
            'xform': {
                'value': [
                    .12,
                    .25,
                    FLAT_LWH[0]/2,
                    45, 0, 90
                ],
            }
        },  
    ],
}
