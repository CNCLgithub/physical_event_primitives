from math import atan, degrees
import random

# BALL_RADIUS = 0.0105  # [m]
BALL_RADIUS = 0.02  # [m]
# BALL_MASS = 0.013  # [kg]
BALL_MASS = 0.0056  # [kg]
BALL_RESTITUTION = 0.8
TOP_TRACK_LWHT = (0.5, 0.05, 0.006, 0.003)  # [m]
BOTTOM_TRACK_LWHT = TOP_TRACK_LWHT  # [m]
HIGH_PLANK_LWH = (0.235, 0.023, 0.008)  # [m]
HIGH_PLANK_RESTITUTION = 0.8
HIGH_PLANK_MASS = 0.021  # [kg]
LOW_PLANK_LWH = (0.1175, 0.023, 0.016)  # [m]
LOW_PLANK_MASS = 0.02  # [kg]
BASE_PLANK_LWH = (0.55, 0.025, 0.005)  # [m]
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
            'name': "ball",
            'type': "Ball",
            'args': {
                'radius': BALL_RADIUS,
                'force': (0,0,0),
                'b_mass': BALL_MASS,
                'b_restitution': BALL_RESTITUTION
            },
            'parent': "track",
            'xform': {
                'value': [BOTTOM_TRACK_LWHT[0]/2, 0, BALL_RADIUS+.002,
                          0, 0, 0]
            }
        },
        {
            'name': "track",
            'type': "Track",
            'args': {
                'extents': BOTTOM_TRACK_LWHT,
            },
            'xform': {
                'value': [0,
                          BOTTOM_TRACK_LWHT[1]/2+.01,
                          .2+BOTTOM_TRACK_LWHT[2]/2+.05+(random.uniform(-.05,.05)),
                          0, 0, -5+(random.uniform(-10,5))],
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
                    GOBLET_EPS
                ]
            },
            'parent':"track",
            'xform': {
                'value': [-.35, GOBLET_R1-.02, -.08, 0, 0, 40],
            }
        },
    ],
}
