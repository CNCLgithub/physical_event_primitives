from math import atan, degrees

import random

DENSITY = 1

HIGH_PLANK_LWH = (0.235, 0.023, 0.008)  # [m]
HIGH_PLANK_RESTITUTION = 0.03

OCCLUDER_LWH = (random.uniform(.08, .2), 0.001, 0.2)  # [m]

# Randomness: size of plank, standard: 1
size = random.uniform(.9, 1.1)
FLAT_SUPPORT_LWH = (.1*size, .015*size, .04*size)  # [m]
HIGH_PLANK_MASS = FLAT_SUPPORT_LWH[0] * FLAT_SUPPORT_LWH[1] * FLAT_SUPPORT_LWH[2] * DENSITY # [kg]

# Randomness: Size of Goblet, standard: GOBLET_R1 = .036
GOBLET_HEIGHT = 0.2  # [m]
GOBLET_R1 = .1  # [m]
GOBLET_R2 = 0.1  # [m]
GOBLET_EPS = .002  # [m]


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
                'extents': FLAT_SUPPORT_LWH,
                # Randomness: force on plank, standard: .005
                'force': (0,random.uniform(-.004,-.01),0),
                'b_mass': HIGH_PLANK_MASS,
                'b_restitution': HIGH_PLANK_RESTITUTION
            },
            # Randomness: position of plank
            'xform': {
                'value': [
                    .18,
                    .2,
                    FLAT_SUPPORT_LWH[0]/2+.002,
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
                'value': [0, .2, GOBLET_R1, 0, 10, 90],
            }
        },       
    ],
}
