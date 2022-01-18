from math import atan, degrees
import math

import random

DENSITY = 1

# Randomness: Size of ball, standard = .02
BALL_RADIUS = .025   # [m]
BALL_MASS = BALL_RADIUS**3 * math.pi * (4/3) * DENSITY  # [kg]
BALL_RESTITUTION = 0.3

TOP_TRACK_LWHT = (2, 0.25, 0.01, 0.01)  # [m]
BOTTOM_TRACK_LWHT = TOP_TRACK_LWHT  # [m]
HIGH_PLANK_LWH = (0.05, 0.10, 0.02)  # [m]
BASE_PLANK_LWH = (1, 0.10, 0.005)  # [m]

OCCLUDER_LWH = (random.uniform(.08, .1), 0.001, 0.15)  # [m]

# Randomness: Size of plank, standard = .05
length = random.uniform(0.04, 0.06)
FLAT_SUPPORT_LWH = (length, length, length)  # [m]
HIGH_PLANK_MASS = FLAT_SUPPORT_LWH[0] * FLAT_SUPPORT_LWH[1] * FLAT_SUPPORT_LWH[2] * DENSITY # [kg]
PLANK_RESTITUTION = 0.3

# print(str(BALL_MASS) + str(HIGH_PLANK_MASS))

# Randomness: plank or ball
if random.random() < 1:
# if False:
    movingObject = {
            'name': "ball",
            'type': "Ball",
            'args': {
                'radius': BALL_RADIUS,
                # Randomness: force on object, standard = 25
                'force': (.009,0,0),
                'b_mass': BALL_MASS,
                'b_restitution': BALL_RESTITUTION
            },
            'parent': "track",
            # Randomness: position of object
            'xform': {
                'value': [0, 0, BALL_RADIUS+.002,
                          0, 0, 0]
            }
        }
    # if True:
    if random.random() < 1:
        movingObject2 = {
            'name': "ball2",
            'type': "Ball",
            'args': {
                'radius': BALL_RADIUS,
                'force': (0,0,0),
                'b_mass': BALL_MASS,
                'b_restitution': BALL_RESTITUTION
            },
            'parent': "track",
            # Randomness: position of object
            'xform': {
                'value': [
                    .7,
                    0,
                    BALL_RADIUS+.002,
                    0, 0, 90
                ],
            }
        }
    else:
        movingObject2 = {
                'name': "plank2",
                'type': "Box",
                'args': {
                    'extents': FLAT_SUPPORT_LWH,
                    'force': (0,0,0),
                    'b_mass': HIGH_PLANK_MASS,
                    'b_restitution': HIGH_PLANK_RESTITUTION
                },
                'parent': "track",
                # Randomness: position of object
                'xform': {
                    'value': [
                        .7,
                    0,
                    FLAT_SUPPORT_LWH[0]/2,
                    0, 0, 90
                    ],
                }
            }
else:
    movingObject = {
            'name': "plank",
            'type': "Box",
            'args': {
                'extents': FLAT_SUPPORT_LWH,
                # Randomness: force on object
                'force': (random.uniform(.09, .105),0,0),
                'b_mass': HIGH_PLANK_MASS,
                'b_restitution': HIGH_PLANK_RESTITUTION
            },
            'parent': "track", 
            # Randomness: position of object
            'xform': {
                'value': [
                    0, 0, FLAT_SUPPORT_LWH/2,
                          0, 0, 0
                ],
            }
        }
    if random.random() < 1:
        movingObject2 = {
            'name': "ball2",
            'type': "Ball",
            'args': {
                'radius': BALL_RADIUS,
                'force': (0,0,0),
                'b_mass': BALL_MASS,
                'b_restitution': BALL_RESTITUTION
            },
            'parent': "track",
            # Randomness: position of object
            'xform': {
                'value': [
                    .7,
                    0,
                    BALL_RADIUS+.002,
                    0, 0, 90
                ],
            }
        }
    else:
        movingObject2 = {
                'name': "plank2",
                'type': "Box",
                'args': {
                    'extents': FLAT_SUPPORT_LWH,
                    'force': (0,0,0),
                    'b_mass': HIGH_PLANK_MASS,
                    'b_restitution': HIGH_PLANK_RESTITUTION
                },
                'parent': "track",
                # Randomness: position of object
                'xform': {
                    'value': [
                        .7,
                    0,
                    FLAT_SUPPORT_LWH[0]/2,
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
            },
        },
        {
            'name': "track",
            'type': "Track",
            'args': {
                'extents': TOP_TRACK_LWHT,
            },
            'xform': {
                'value': [-.9, TOP_TRACK_LWHT[1]/2+.01, .37, 0, 0, 0]
            }
        },
        {
            'name': "track2",
            'type': "Track",
            'args': {
                'extents': (0.3, 0.10, 0.01, 0.01),
            },
            'xform': {
    
                'value': [.1, TOP_TRACK_LWHT[1]/2+.01, .45, 0, 0, 0]
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
                'value': [.54, .4, .05, 0, 0, 90],
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
            'name': "plank5",
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
                .41,
                .6,
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
            'value': [.23,
                .4,
                BALL_RADIUS+.002,
                0, 0, 90]
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
            'value': [-.1,
                .6,
                BALL_RADIUS+.002,
                0, 0, 90]
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
        movingObject,
        movingObject2
    ],
}