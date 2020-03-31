from math import atan, degrees

import random

# BALL_RADIUS = 0.0105  # [m]
BALL_RADIUS = 0.008  # [m]
# BALL_MASS = 0.013  # [kg]
BALL_MASS = 0.0056  # [kg]
BALL_RESTITUTION = 0.8
TOP_TRACK_LWHT = (0.3, 0.025, 0.006, 0.003)  # [m]
BOTTOM_TRACK_LWHT = TOP_TRACK_LWHT  # [m]
HIGH_PLANK_LWH = (0.235, 0.023, 0.008)  # [m]
HIGH_PLANK_RESTITUTION = 0.8
HIGH_PLANK_MASS = 0.021  # [kg]
LOW_PLANK_LWH = (0.1175, 0.023, 0.016)  # [m]
LOW_PLANK_MASS = 0.02  # [kg]
BASE_PLANK_LWH = (0.35, 0.025, 0.005)  # [m]
BASE_PLANK_MASS = 0.021  # [kg]
FLAT_SUPPORT_LWH = (.02, .025, .005)  # [m]
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
            'name': "board",
            'type': "Plane",
            'args': {
                'normal': [0, 1, 0],
                'distance': 0
            }
        },
        {
            'name': "board2",
            'type': "Plane",
            'args': {
                'normal': [0, 0, 1],
                'distance': 0
            }
        },
        {
            'name': "ball",
            'type': "Ball",
            'args': {
                'radius': BALL_RADIUS,
                'b_mass': BALL_MASS,
                'b_restitution': BALL_RESTITUTION
            },
            'parent': "top_track",
            'xform': {
                'value': [-TOP_TRACK_LWHT[0]/2+.01, 0, BALL_RADIUS+.002,
                          0, 0, 0]
            }
        },
        {
            'name': "top_track",
            'type': "Track",
            'args': {
                'extents': TOP_TRACK_LWHT,
            },
            'xform': {
                'value': [-.1, TOP_TRACK_LWHT[1]/2+.1+(random.uniform(-.05,.05)), .3, 0, 0, 20+(random.uniform(-20,10))],
                'range': [
                    [-BASE_PLANK_LWH[0]/3, 0],
                    None,
                    [HIGH_PLANK_LWH[0]/2, HIGH_PLANK_LWH[0]],
                    None,
                    None,
                    [5, 35]
                ]
            }
        },
        
        
    ],
}
