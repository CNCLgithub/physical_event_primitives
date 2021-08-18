from math import atan, degrees

import math
import random

DENSITY = 1

# Randomness: size of ball, standard: .02
BALL_RADIUS = .025  # [m]
BALL_MASS = BALL_RADIUS**3 * math.pi * (4/3) * DENSITY  # [kg]
BALL_RESTITUTION = 0.8

TOP_TRACK_LWHT = (0.2, 0.025, 0.006, 0.003)  # [m]

# Randomness: size of occluder
HIGH_PLANK_LWH = (.15, 0.001, 0.25)  # [m]
HIGH_PLANK_RESTITUTION = 0.3

# Randomness: size of plank
length = random.uniform(0.04, 0.06)
FLAT_SUPPORT_LWH = (length, length, length)  # [m]
HIGH_PLANK_MASS = FLAT_SUPPORT_LWH[0] * FLAT_SUPPORT_LWH[1] * FLAT_SUPPORT_LWH[2] * DENSITY # [kg]

# Randomness: Size of Goblet, standard: GOBLET_R1 = .036
GOBLET_HEIGHT = 0.2  # [m]
GOBLET_R1 = 0.05  # [m]
GOBLET_R2 = 0.05  # [m]
GOBLET_EPS = .002  # [m]

# Randomness: Ball or Plank
# if False:
if random.random() < 1:
    movingObject = {
            'name': "ball",
            'type': "Ball",
            'args': {
                'radius': BALL_RADIUS,
                # Randomness: force on object
                'force': (-.01,0,0),
                'b_mass': BALL_MASS,
                'b_restitution': BALL_RESTITUTION
            },
            'xform': {
                'value': [.5, .1, BALL_RADIUS+.002,
                          0, 0, 0]
            }
    }
else:
    movingObject = { 
            'name': "plank",
            'type': "Box",
            'args': {
                'extents': FLAT_SUPPORT_LWH,
                # Randomness: force on object, standard: .01
                'force': (random.uniform(.08, .08),0,0),
                'b_mass': HIGH_PLANK_MASS,
                'b_restitution': HIGH_PLANK_RESTITUTION
            },
            'xform': {
                'value': [.5, .1, FLAT_SUPPORT_LWH[0]/2,
                    0, 0, 0],
            }
    }

if random.random() < 1:
    movingObject2 = {
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
                'value': [-.3, .1, BALL_RADIUS+.002,
                          0, 0, 0]
            }
    }
else:
    movingObject2 = { 
            'name': "plank2",
            'type': "Box",
            'args': {
                'extents': FLAT_SUPPORT_LWH,
                # Randomness: force on object, standard: .01
                'force': (0,0,0),
                'b_mass': HIGH_PLANK_MASS,
                'b_restitution': HIGH_PLANK_RESTITUTION
            },
            'xform': {
                'value': [-.2, .1, FLAT_SUPPORT_LWH[0]/2,
                    0, 0, 0],
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
        movingObject,
        movingObject2,
        {
            'name': "occluder",
            'type': "Box",
            'args': {
                'extents': HIGH_PLANK_LWH,
                'force': (0,0,0)
            },
            # Randomness: position of occluder
            'xform': {
                'value': [.02, .35, HIGH_PLANK_LWH[0]/2-.005, 0, 0, 90],
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
                'value': [.6, .1, GOBLET_R1-.002, 0, 10, -90],
            }
        }, 
        {
            'name': "track",
            'type': "Track",
            'args': {
                'extents': TOP_TRACK_LWHT,
            },
            'xform': {
                'value': [.1, TOP_TRACK_LWHT[1]/2+.01, .2, 0, 0, 0]
            }
        }, 
        {
        'name': "ball4",
        'type': "Ball",
        'args': {
            'radius': BALL_RADIUS,
            'force': (0,0,0),
            'b_mass': 0,
            'b_restitution': BALL_RESTITUTION
        },
        'parent': "track",
             # Randomness: plank location
             'xform': {
             'value': [
                -TOP_TRACK_LWHT[0]/2+.10,
                0,
                FLAT_SUPPORT_LWH[0]/2 + .003,
                0, 0, 0
                ],
            }
        }, 
        {
            'name': "plank",
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
                .4,
                .63,
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
                -.05,
                .63,
                .034,
                0, 0, 0
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
            'value': [-.14, 0.55, BALL_RADIUS+.002,
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
            'value': [.08, 0.8, 0.08,
                      0, 0, 0]
        }
    },
    ],
}