from math import atan, degrees

import random

DENSITY = 1

HIGH_PLANK_LWH = (0.235, 0.023, 0.008)  # [m]
HIGH_PLANK_RESTITUTION = 0.03

OCCLUDER_LWH = (random.uniform(.08, .1), 0.001, 0.2)  # [m]

# Randomness: size of plank, standard: 1
size = random.uniform(.9, 1.4)
FLAT_SUPPORT_LWH = (.1*size, .015*size, .04*size)  # [m]
HIGH_PLANK_MASS = FLAT_SUPPORT_LWH[0] * FLAT_SUPPORT_LWH[1] * FLAT_SUPPORT_LWH[2] * DENSITY # [kg]


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
                'force': (0,random.uniform(.02,.02),0),
                'b_mass': HIGH_PLANK_MASS,
                'b_restitution': HIGH_PLANK_RESTITUTION
            },
            # Randomness: position of plank
            'xform': {
                'value': [
                    .18,
                    .15,
                    FLAT_SUPPORT_LWH[0]/2,
                    45, 0, 90
                ],
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
                'value': [.095, .3, 0, 0, 0, 90],
            }
        },       
    ],
}
