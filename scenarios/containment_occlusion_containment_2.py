from math import atan, degrees

import math
import random

DENSITY = 1

# Randomness: size of ball, standard: .02
BALL_RADIUS = .025   # [m]
BALL_MASS = BALL_RADIUS**3 * math.pi * (4/3) * DENSITY  # [kg]
BALL_RESTITUTION = 0.8

TOP_TRACK_LWHT = (0.3, 0.025, 0.006, 0.003)  # [m]

# Randomness: size of occluder
HIGH_PLANK_LWH = (.1, 0.001, 0.15)  # [m]
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
                'force': (-.03,0,0),
                'b_mass': BALL_MASS,
                'b_restitution': BALL_RESTITUTION
            },
            'xform': {
                'value': [.55, .1, BALL_RADIUS+.002,
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
                'value': [.55, .1, FLAT_SUPPORT_LWH[0]/2,
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
        {
            'name': "occluder",
            'type': "Box",
            'args': {
                'extents': HIGH_PLANK_LWH,
                'force': (0,0,0)
            },
            # Randomness: position of occluder
            'xform': {
                'value': [.24, .55, HIGH_PLANK_LWH[0]/2-.005, 0, 0, 90],
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
            # Randomness: position of goblet
            'xform': {
                'value': [.65, .1, GOBLET_R1-.002, 0, 10, -90],
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
                'value': [-.2, .1, GOBLET_R1, 0, 10, 90],
            }
        }, 
         {
            'name': "goblet4",
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
                'value': [-.2, .5, GOBLET_R1, 0, 10, 90],
            }
        }, 
    {
        'name': "ball2",
        'type': "Ball",
        'args': {
            'radius': BALL_RADIUS,
            'force': (0,0,0),
            'b_mass': 0,
            'b_restitution': BALL_RESTITUTION
        },
        # Randomness: ball location
        'xform': {
            'value': [.23, 0.6, BALL_RADIUS+.002,
                      0, 0, 0]
        }
    },  
    {
            'name': "plank",
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
                .5,
                .5,
                .034,
                0, 0, 0
                ],
            }
        }, 
        {
            'name': "plank4",
            'type': "Box",
            'args': {
                'extents': (.03, .03, .03),
                # Randomness: force on plank, standard: .005
                'force': (0,0,0),
                'b_mass': 0,
                'b_restitution': HIGH_PLANK_RESTITUTION
            },
             # Randomness: plank location
             'xform': {
             'value': [
                .3,
                .7,
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
                .15,
                .63,
                .034,
                0, 0, 0
                ],
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
            'value': [.4, 0.4, BALL_RADIUS+.002,
                      0, 0, 0]
        }
    },  
    ],
}