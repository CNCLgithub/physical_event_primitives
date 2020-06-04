from math import atan, degrees

import random

DENSITY = 1

TOP_TRACK_LWHT = (0.25, 0.10, 0.002, 0.005)  # [m]
HIGH_PLANK_RESTITUTION = 0.3

# Randomness: Size of plank
FLAT_SUPPORT_LWH = (.05, .05, .05)  # [m]
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
            },
        },
        {
            'name': "plank",
            'type': "Box",
            'args': {
                'extents': FLAT_SUPPORT_LWH,
                # Randomness: force on object
                'force': (.2,0,0),
                'b_mass': HIGH_PLANK_MASS,
                'b_restitution': HIGH_PLANK_RESTITUTION
            },
            # Randomness: position of object
            'xform': {
                'value': [
                    -TOP_TRACK_LWHT[0]*3,
                    .02,
                    FLAT_SUPPORT_LWH[0]/2,
                    0, 0, 90
                ],
            }
        }
    ],
}