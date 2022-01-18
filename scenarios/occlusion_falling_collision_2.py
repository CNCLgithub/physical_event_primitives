from math import atan, degrees
import math
import random

DENSITY = 1
# Randomness: ball size, standard: .008
BALL_RADIUS = .03   # [m]
BALL_MASS = BALL_RADIUS**3 * math.pi * (4/3) * DENSITY  # [kg]
BALL_RESTITUTION = 0.8

TOP_TRACK_LWHT = (0.5, 0.1, 0.01, 0.006)  # [m]

HIGH_PLANK_LWH = (0.235, 0.023, 0.008)  # [m]
HIGH_PLANK_RESTITUTION = 0.8
BASE_PLANK_LWH = (0.235, 0.001, 0.1)  # [m]

OCCLUDER_LWH = (random.uniform(.08, .15), 0.001, 0.2)  # [m]

# Randomness: plank size, standard: 1
length = random.uniform(0.04, 0.06)
FLAT_SUPPORT_LWH = (length, length, length)  # [m]
HIGH_PLANK_MASS = FLAT_SUPPORT_LWH[0] * FLAT_SUPPORT_LWH[1] * FLAT_SUPPORT_LWH[2] * DENSITY # [kg]

# Randomness: plank or ball
if random.random() < 0:
    movingObject = {
        'name': "plank",
        'type': "Box",
        'args': {
            'extents': FLAT_SUPPORT_LWH,
            'force': (.01,0,0),
            'b_mass': HIGH_PLANK_MASS,
            'b_restitution': HIGH_PLANK_RESTITUTION
        },
        'parent': "track",
        # Randomness: plank location
        'xform': {
            'value': [
                -TOP_TRACK_LWHT[0]/2+.01,
                0,
                FLAT_SUPPORT_LWH[0]/2 + .005,
                0, 0, 90
            ],
        }
    }
else:
    movingObject = {
        'name': "ball",
        'type': "Ball",
        'args': {
            'radius': BALL_RADIUS,
            'force': (random.uniform(.02, .03),0,0),
            'b_mass': BALL_MASS,
            'b_restitution': BALL_RESTITUTION
        },
        'parent': "track",
        # Randomness: ball location
        'xform': {
            'value': [-TOP_TRACK_LWHT[0]/2+.01, 0, BALL_RADIUS+.002,
                      0, 0, 0]
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
        'parent': "floor",
        # Randomness: position of object
        'xform': {
            'value': [
                .4,
                .05,
                BALL_RADIUS+.002,
                0, 0, 0
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
            # Randomness: position of object
            'xform': {
                'value': [
                    .3,
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
                'extents': TOP_TRACK_LWHT,
            },
            'xform': {
                'value': [-.12, TOP_TRACK_LWHT[1]/2+.01, .33, 0, 0, 0]
            }
        },
         {
            'name': "track2",
            'type': "Track",
            'args': {
                'extents': (0.3, 0.10, 0.01, 0.01),
            },
            'xform': {
    
                'value': [.2, TOP_TRACK_LWHT[1]/2+.01, .45, 0, 0, 0]
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
                'value': [-.05, .05, OCCLUDER_LWH[0]/2-.002, 0, 0, 90],
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
            'value': [.4,
                .5,
                BALL_RADIUS+.002,
                0, 0, 0]
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
                'b_restitution': HIGH_PLANK_RESTITUTION
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
                'b_restitution': HIGH_PLANK_RESTITUTION
            },
             # Randomness: plank location
             'xform': {
             'value': [
                .2,
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
            'radius': 0.03,
            'force': (0,0,0),
            'b_mass': 0,
            'b_restitution': BALL_RESTITUTION
        },
        # Randomness: ball location
        'xform': {
            'value': [.5, 0.6, BALL_RADIUS+.003,
                          0, 0, 0]
        }
    },
     {
        'name': "cylinder",
        'type': "Cylinder",
        'args': {
            'extents': [0.02, 0.06]
        },
        # Randomness: cylinder location
        'xform': {
            'value': [.1, 0.8, 0.08,
                      0, 0, 0]
        }
    },             movingObject,
        movingObject2
    ]
}