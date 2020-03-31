from math import atan, degrees

# BALL_RADIUS = 0.0105  # [m]
BALL_RADIUS = 0.008  # [m]
# BALL_MASS = 0.013  # [kg]
BALL_MASS = 0.0056  # [kg]
BALL_RESTITUTION = 0.8
TOP_TRACK_LWHT = (0.25, 0.025, 0.006, 0.003)  # [m]
BOTTOM_TRACK_LWHT = TOP_TRACK_LWHT  # [m]
HIGH_PLANK_LWH = (0.235, 0.023, 0.008)  # [m]
HIGH_PLANK_RESTITUTION = 0.8
HIGH_PLANK_MASS = 0.021  # [kg]
LOW_PLANK_LWH = (0.05, 0.001, 0.2)  # [m]
LOW_PLANK_MASS = 0.02  # [kg]
BASE_PLANK_LWH = (0.55, 0.05, 0.005)  # [m]
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
            'name': "plank",
            'type': "Box",
            'args': {
                'extents': FLAT_SUPPORT_LWH,
                'b_mass': HIGH_PLANK_MASS,
                'b_restitution': HIGH_PLANK_RESTITUTION
            },
            'parent': "bottom_track",
            'xform': {
                'value': [
                    BOTTOM_TRACK_LWHT[0]/2, 0, BALL_RADIUS+.01,
                          0, 0, 60
                ],
            }
        },
        {
            'name': "bottom_track_joint",
            'type': "Empty",
            'args': {},
            'xform': {
                'value': [BOTTOM_TRACK_LWHT[0]/2-.001, 0, .18, 0, 0, -20],
                'range': [
                    None,
                    None,
                    [.03, HIGH_PLANK_LWH[0]-BALL_RADIUS],
                    None,
                    None,
                    [-45, -5]
                ]
            }
        },
        {
            'name': "bottom_track",
            'type': "Track",
            'args': {
                'extents': BOTTOM_TRACK_LWHT,
            },
            'parent': "bottom_track_joint",
            'xform': {
                'value': [-BOTTOM_TRACK_LWHT[0]/2,
                          BOTTOM_TRACK_LWHT[1]/2+.01,
                          BOTTOM_TRACK_LWHT[2]/2,
                          0, 0, 0],
            }
        },
        {
            'name': "high_plank",
            'type': "Box",
            'args': {
                'extents': HIGH_PLANK_LWH,
            },
            'parent': "base_plank",
            'xform': {
                'value': [
                    BOTTOM_TRACK_LWHT[0]/2 + HIGH_PLANK_LWH[2]/2,
                    0,
                    HIGH_PLANK_LWH[0]/2 + BASE_PLANK_LWH[2]/2,
                    0, 0, 90
                ],
            }
        },
        {
            'name': "base_plank",
            'type': "Lever",
            'args': {
                'extents': BASE_PLANK_LWH,
                'pivot_pos': [0, 0, 0],
                'pivot_hpr': [0, 90, 0],
                'pivot_extents': [BASE_PLANK_LWH[2]*.4,
                                  BASE_PLANK_LWH[1]*1.5],
                'b_mass': BASE_PLANK_MASS
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
            'name': "flat_support",
            'type': "Box",
            'args': {
                'extents': FLAT_SUPPORT_LWH,
            },
            'xform': {
                'value': [
                    BASE_PLANK_LWH[0]/2 - FLAT_SUPPORT_LWH[0]/2,
                    FLAT_SUPPORT_LWH[0]/2 + .01,
                    -FLAT_SUPPORT_LWH[2],
                    0, 0, 0
                ],
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
            'xform': {
                'value': [-.2, GOBLET_R1, .02, 0, 0, 45],
                'range': [
                    [-BASE_PLANK_LWH[0],
                     -BASE_PLANK_LWH[0]/2-GOBLET_R1/2],
                    None,
                    [-LOW_PLANK_LWH[0]/2-GOBLET_HEIGHT/2, -GOBLET_HEIGHT/2],
                    None,
                    None,
                    [0, 60]
                ]
            }
        },
    ],
}
