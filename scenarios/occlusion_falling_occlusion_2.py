from math import atan, degrees
import math
import random

DENSITY = 50
# Randomness: ball size, standard: .008
BALL_RADIUS = .025   # [m]
BALL_MASS = BALL_RADIUS**3 * math.pi * (4/3) * DENSITY  # [kg]
BALL_RESTITUTION = 0.8

TOP_TRACK_LWHT = (0.5, 0.1, 0.01, 0.01)  # [m]

HIGH_PLANK_LWH = (0.235, 0.023, 0.008)  # [m]
HIGH_PLANK_RESTITUTION = 0.8
BASE_PLANK_LWH = (0.235, 0.001, 0.1)  # [m]

OCCLUDER_LWH = (.14, 0.001, 0.2)  # [m]
OCCLUDER2_LWH = (.14, 0.001, 0.15)  # [m]


# Randomness: plank size, standard: 1
length = .05
FLAT_SUPPORT_LWH = (length, length, length)  # [m]
HIGH_PLANK_MASS = FLAT_SUPPORT_LWH[0] * FLAT_SUPPORT_LWH[1] * FLAT_SUPPORT_LWH[2] * DENSITY # [kg]


# Randomness: Size of Goblet, standard: GOBLET_R1 = .036
GOBLET_HEIGHT = 0.15  # [m]
GOBLET_R1 = 0.05  # [m]
GOBLET_R2 = 0.03  # [m]
GOBLET_EPS = .002  # [m]

# Randomness: plank or ball
movingObject = {
        'name': "ball",
        'type': "Ball",
        'args': {
            'radius': BALL_RADIUS,
            'force': (0,0,0),
            'b_mass': BALL_MASS,
            'b_restitution': BALL_RESTITUTION
        },
        'parent': "track",
        # Randomness: ball location
        'xform': {
            'value': [-TOP_TRACK_LWHT[0]/2+.01, 0, BALL_RADIUS+0.002,
                      0, 0, 0]
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
            },
        },
        {
            'name': "track",
            'type': "Track",
            'args': {
                'extents': TOP_TRACK_LWHT,
            },
            'xform': {
                'value': [-.11, TOP_TRACK_LWHT[1]/2+.01, .34, 0, 0, 4]
            }
        },
         {
            'name': "track2",
            'type': "Track",
            'args': {
                'extents': (0.3, 0.10, 0.01, 0.01),
            },
            'xform': {
    
                'value': [-0.05, TOP_TRACK_LWHT[1]/2+.01, .25, 0, 0, 0]
            }
        },
        {
            'name': "occluder",
            'type': "Box",
            'args': {
                'extents': OCCLUDER_LWH,
                'force': (0,0,0)
            },
            'parent': "track",
            # Randomness: position of occluder
            'xform': {
                'value': [.03, .05, OCCLUDER_LWH[0]/2-.002, 0, 0, 90],
            }
        },
        {
            'name': "occluder2",
            'type': "Box",
            'args': {
                'extents': OCCLUDER2_LWH,
                'force': (0,0,0)
            },
            # Randomness: position of occluder
            'xform': {
                'value': [.51, .2, .05, 0, 0, 90],
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
                'b_restitution': HIGH_PLANK_RESTITUTION
            },
             # Randomness: plank location
             'xform': {
             'value': [
                -.025,
                .6,
                .03,
                0, 0, 0
                ],
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
                .43,
                .45,
                .03,
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
            'value': [.3, 0.4, BALL_RADIUS,
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
            'value': [.13, 0.8, 0.08,
                      0, 0, 0]
        }
    },  
             {
            'name': "goblet3",
            'type': "Goblet",
            'args': {
                'extents': [
                    GOBLET_HEIGHT,
                    GOBLET_R1,
                    GOBLET_R2,
                    GOBLET_EPS
                ]
            },
            # Randomness: position of goblet
            'xform': {
                'value': [-0.2, 0.2, 0, 0, 0, 0],
            }
        }, 

        movingObject,
    ]
}