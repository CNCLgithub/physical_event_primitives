from math import atan, degrees
import math
import random

DENSITY = 1
# Randomness: Size of Ball
BALL_RADIUS = random.uniform(0.018, 0.023)   # [m]
BALL_MASS = BALL_RADIUS**3 * math.pi * (4/3) * DENSITY  # [kg]
BALL_RESTITUTION = 0.8

TOP_TRACK_LWHT = (0.5, 0.05*2, 0.01, 0.006)  # [m]
BOTTOM_TRACK_LWHT = TOP_TRACK_LWHT  # [m]

PLANK_LWH = (0.235, 0.023, 0.008)  # [m]
PLANK_RESTITUTION = 0.8

# Randomness: Size of plank
length = random.uniform(0.03, 0.04)
FLAT_SUPPORT_LWH = (length, length, length)  # [m]
PLANK_MASS = FLAT_SUPPORT_LWH[0] * FLAT_SUPPORT_LWH[1] * FLAT_SUPPORT_LWH[2] * DENSITY # [kg]


# Randomness: Size of Goblet, standard: GOBLET_R1 = .036
GOBLET_HEIGHT = 0.15  # [m]
GOBLET_R1 = 0.05  # [m]
GOBLET_R2 = 0.03  # [m]
GOBLET_EPS = .002  # [m]

# Randomness: Ball or plank
if random.random() < 1:
# if False:
    movingObject = {
            'name': "ball",
            'type': "Ball",
            'args': {
                'radius': BALL_RADIUS,
                'force': (random.uniform(-.02,-.04),0,0),
                'b_mass': BALL_MASS,
                'b_restitution': BALL_RESTITUTION
            },
            'parent': "track",
            'xform': {
                'value': [BOTTOM_TRACK_LWHT[0]/2, 0, BALL_RADIUS+.002,
                          0, 0, 0]
            }
    }
else:
    movingObject = {
            'name': "plank",
            'type': "Box",
            'args': {
                'extents': FLAT_SUPPORT_LWH,
                # Randomness: force on plank
                'force': (random.uniform(.08, .08),0,0),
                'b_mass': PLANK_MASS,
                'b_restitution': PLANK_RESTITUTION
            },
            'parent': "track",
            'xform': {
                'value': [
                    BOTTOM_TRACK_LWHT[0]/2-.02, 0, length/2,
                          0, 0, 0
                ],
            }
    }

if random.random() < .7:
    movingObject2 = {
        'name': "ball4",
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
                .45,
                .05,
                BALL_RADIUS+.002,
                0, 0, 0
            ],
        }
    }
else:
    movingObject2 = {
            'name': "plank4",
            'type': "Box",
            'args': {
                'extents': FLAT_SUPPORT_LWH,
                'force': (0,0,0),
                'b_mass': PLANK_MASS,
                'b_restitution': PLANK_RESTITUTION
            },
            # Randomness: position of object
            'xform': {
                'value': [
                    .45,
                    .05,
                    FLAT_SUPPORT_LWH[0]/2,
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
            },
        },
        {
            'name': "track",
            'type': "Track",
            'args': {
                'extents': BOTTOM_TRACK_LWHT,
            },
            # Randomness: height 
            'xform': {
                'value': [0,
                          BOTTOM_TRACK_LWHT[1]/2+.01,
                          .2+BOTTOM_TRACK_LWHT[2]/2+.05+(random.uniform(-.05,.05)),
                          0, 0, 0],
            }
        },
        {
            'name': "track2",
            'type': "Track",
            'args': {
                'extents': (0.3, 0.10, 0.01, 0.01),
            },
            'xform': {
    
                'value': [.2, TOP_TRACK_LWHT[1]/2+.01, .4, 0, 0, 0]
            }
        },
        movingObject,
        movingObject2,
        {
            'name': "goblet",
            'type': "Goblet",
            'args': {
                'extents': [
                    GOBLET_HEIGHT,
                    GOBLET_R1,
                    GOBLET_R2,
                    GOBLET_EPS
                ]
            },
            'parent': "track",
            # Randomness: position of goblet
            'xform': {
                'value': [-.38, 0, GOBLET_R1+.002, 0, 0, 88],
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
                    GOBLET_EPS
                ]
            },
            # Randomness: position of goblet
            'xform': {
                'value': [-.2, 0, 0, 0, 0, 0],
            }
        },
         {
            'name': "plank5",
            'type': "Box",
            'args': {
                'extents': (.05, .05, .05),
                # Randomness: force on plank, standard: .005
                'force': (0,0,0),
                'b_mass': 0,
                'b_restitution': PLANK_RESTITUTION
            },
             # Randomness: plank location
             'xform': {
             'value': [
                -.05,
                .2,
                .03,
                0, 0, 0
                ],
            }
        },  
        {
            'name': "plank2",
            'type': "Box",
            'args': {
                'extents': (.06, .06, .06),
                # Randomness: force on plank, standard: .005
                'force': (0,0,0),
                'b_mass': 0,
                'b_restitution': PLANK_RESTITUTION
            },
             # Randomness: plank location
             'xform': {
             'value': [
                .25,
                .5,
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
            'value': [.45, 0.4, BALL_RADIUS+.002,
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
            'value': [.1, 0.8, 0.08,
                      0, 0, 0]
        }
    },     
    ],
}