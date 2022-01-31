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
HIGH_PLANK_LWH = (.14, 0.001, 0.2)  # [m]
HIGH_PLANK_RESTITUTION = 0.3

# Randomness: size of plank
length = .05
FLAT_SUPPORT_LWH = (length, length, length)  # [m]
HIGH_PLANK_MASS = FLAT_SUPPORT_LWH[0] * FLAT_SUPPORT_LWH[1] * FLAT_SUPPORT_LWH[2] * DENSITY # [kg]

# Randomness: Ball or Plank
# if False:
movingObject = {
            'name': "ball",
            'type': "Ball",
            'args': {
                'radius': BALL_RADIUS,
                # Randomness: force on object
                'force': (0.01,0,0),
                'b_mass': BALL_MASS,
                'b_restitution': BALL_RESTITUTION
            },
            'xform': {
                'value': [-.5, BALL_RADIUS*4, BALL_RADIUS,
                          0, 0, 0]
            }
    }
movingObject2 = {
        'name': "ball2",
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
                .58,
                BALL_RADIUS*4,
                BALL_RADIUS,
                0, 0, 90
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
                'value': [.3, .35, .05, 0, 0, 90],
            }
        },
        {
            'name': "occluder2",
            'type': "Box",
            'args': {
                'extents': HIGH_PLANK_LWH,
                'force': (0,0,0)
            },
            # Randomness: position of occluder
            'xform': {
                'value': [-.1, .35, .05, 0, 0, 90],
            }
        },
         {
            'name': "plank5",
            'type': "Box",
            'args': {
                'extents': (.06, .03, .03),
                # Randomness: force on plank, standard: .005
                'force': (0,0,0),
                'b_mass': 0,
                'b_restitution': HIGH_PLANK_RESTITUTION
            },
             # Randomness: plank location
             'xform': {
             'value': [
                .24,
                .5,
                .03,
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
            'value': [ .52,
               .5,
                BALL_RADIUS,
                0, 0, 90]
        }
    }, 
    {
            'name': "plank2",
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
                -.1,
                .6,
                .026,
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
            'value': [.34, 0.6, BALL_RADIUS,
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
            'value': [.1, 0.94, 0.08,
                      0, 0, 0]
        }
    },   
    ],
}