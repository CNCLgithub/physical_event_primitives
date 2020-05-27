from math import atan, degrees

# BALL_RADIUS = 0.0105  # [m]
BALL_RADIUS = 0.03  # [m]
# BALL_MASS = 0.013  # [kg]
BALL_MASS = 0.5  # [kg]
BALL_RESTITUTION = 0.8
TOP_TRACK_LWHT = (0.25, 0.12, 0.002, 0.005)  # [m]
BOTTOM_TRACK_LWHT = TOP_TRACK_LWHT  # [m]
HIGH_PLANK_LWH = (0.1, 0.05, 0.05)  # [m]
HIGH_PLANK_RESTITUTION = 0.3
HIGH_PLANK_MASS = 0.41  # [kg]
LOW_PLANK_LWH = (0.235, 0.001, 0.3)  # [m]
LOW_PLANK_MASS = 0.02  # [kg]
BASE_PLANK_LWH = (1, 0.12, 0.005)  # [m]
BASE_PLANK_MASS = 0.100  # [kg]
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
            'name': "ball",
            'type': "Ball",
            'args': {
                'radius': BALL_RADIUS,
                'b_mass': BALL_MASS,
                'b_restitution': BALL_RESTITUTION
            },
            'parent': "top_track",
            'xform': {
                'value': [-TOP_TRACK_LWHT[0]/2, 0, BALL_RADIUS+.005,
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
                'value': [-.5, TOP_TRACK_LWHT[1]/2+.01, .3, 0, 0, 20],
                'range': [
                    [-BASE_PLANK_LWH[0]/2, 0],
                    None,
                    [HIGH_PLANK_LWH[0]/2, HIGH_PLANK_LWH[0]],
                    None,
                    None,
                    [5, 35]
                ]
            }
        },
        {
            'name': "high_plank",
            'type': "Box",
            'args': {
                'extents': HIGH_PLANK_LWH,
                'b_mass': HIGH_PLANK_MASS,
                'b_restitution': HIGH_PLANK_RESTITUTION
            },
            'parent': "base_plank",
            'xform': {
                'value': [
                    BOTTOM_TRACK_LWHT[0] + HIGH_PLANK_LWH[2] - .15,
                    0,
                    HIGH_PLANK_LWH[0]/2 + BASE_PLANK_LWH[2]/2,
                    0, 0, 90
                ],
            }
        },
        {
            'name': "base_plank",
            'type': "Box",
            'args': {
                'extents': BASE_PLANK_LWH
            },
            'xform': {
                'value': [
                    0,
                    BASE_PLANK_LWH[1]/2 + .01,
                    0,
                    0, 0, 0
                ],
            }
        },
                        {
            'name': "wall",
            'type': "Box",
            'args': {
                'extents': LOW_PLANK_LWH,
            },
            'xform': {
                'value': [.35, -.05, .12, 0, 0, 90],
            }
        },
    ],
}
