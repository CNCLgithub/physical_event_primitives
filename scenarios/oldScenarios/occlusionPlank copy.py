from math import atan, degrees
import random

# BALL_RADIUS = 0.0105  # [m]
BALL_RADIUS = 0.008  # [m]
# BALL_MASS = 0.013  # [kg]
BALL_MASS = 0.0056  # [kg]
BALL_RESTITUTION = 0.8
TOP_TRACK_LWHT = (0.3, 0.05, 0.006, 0.003)  # [m]
BOTTOM_TRACK_LWHT = TOP_TRACK_LWHT  # [m]
HIGH_PLANK_LWH = (0.1, 0.001, 0.4)  # [m]
HIGH_PLANK_RESTITUTION = 0.8
HIGH_PLANK_MASS = 0.021  # [kg]
LOW_PLANK_LWH = (0.3, 0.10, 0.006)  # [m]
LOW_PLANK_MASS = 0.02  # [kg]
BASE_PLANK_LWH = (0.1, 0.001, 0.4)  # [m]
BASE_PLANK_MASS = 0.021  # [kg]
FLAT_SUPPORT_LWH = (.04, .05, .005)  # [m]
# GOBLET_HEIGHT = 0.119  # [m]
# GOBLET_R1 = 0.0455  # [m]
# GOBLET_R2 = 0.031  # [m]
GOBLET_HEIGHT = 0.11  # [m]
GOBLET_R1 = 0.036  # [m]
GOBLET_R2 = 0.025  # [m]
GOBLET_EPS = .002  # [m]

PIVOTING_ANGULAR_VELOCITY = 1
ANGVEL = 10
HIGH_PLANK_TOPPLING_ANGLE = degrees(atan(HIGH_PLANK_LWH[2]/HIGH_PLANK_LWH[0]))
STOPPING_LINEAR_VELOCITY = 1e-2
STOPPING_ANGULAR_VELOCITY = 1

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
                'force': (0,0,0),
                'b_mass': HIGH_PLANK_MASS,
                'b_restitution': HIGH_PLANK_RESTITUTION
            },
            'parent': "track",
            'xform': {
                'value': [
                    -TOP_TRACK_LWHT[0]/2+.01,
                    0,
                    .023,
                    0, 0, 90
                ],
            }
        },
                {
            'name': "occluder",
            'type': "Box",
            'args': {
                'extents': BASE_PLANK_LWH,
                'force': (0,0,0)
            },
            'xform': {
                'value': [.25, random.uniform(0,.3), .05, 0, 0, 90],
            }
        },
        {
            'name': "track",
            'type': "Track",
            'args': {
                'extents': TOP_TRACK_LWHT,
            },
            'xform': {
                'value': [-.1, TOP_TRACK_LWHT[1]/2+.01, .06, 0, 0, 20],
            }
        },
        
        
    ],
}
