import os
import sys

sys.path.insert(0, os.path.abspath(".."))
from core.dominoes import create_line  # noqa: E402


SUPPORT_LWH = [.1, .2, .1]
SUPPORT2_LWH = [.1, .05, .05]
DOMINO_LWH = [.003, .01, .02]
DOMINO_MASS = .005
PLANK_LWH = [SUPPORT_LWH[0]*.8, .003, .02]
PLANK_MASS = .01
TRACK_LWHT = [SUPPORT_LWH[1]/2-.01, .02, .004, .002]
BALL_RADIUS = .006
BALL_MASS = .01
LEVER_LWH = [SUPPORT_LWH[0]*.8, .02, .003]
LEVER_MASS = .008
GOBLET_HEIGHT = .025
GOBLET_R1 = .015
GOBLET_R2 = .011

DATA = {
    'scene': [
        {
            'name': "support",
            'type': "Box",
            'args': {
                'extents': SUPPORT_LWH
            },
            'xform': {
                'value': [0, 0, -SUPPORT_LWH[2]/2, 0, 0, 0]
            }
        },
        {
            'name': "support2",
            'type': "Box",
            'args': {
                'extents': SUPPORT2_LWH
            },
            'xform': {
                'value': [0,
                          SUPPORT_LWH[1]/2+SUPPORT2_LWH[1]/2,
                          -SUPPORT_LWH[2]*3/4,
                          0, 0, 0]
            }
        },
        {
            'name': "run1",
            'type': "DominoRun",
            'args': {
                'extents': DOMINO_LWH,
                'coords': create_line([0, -SUPPORT_LWH[1]*.4], 90,
                                      SUPPORT_LWH[1]*.35, 8),
                'tilt_angle': 9,
                'b_mass': DOMINO_MASS
            },
            'xform': {
                'value': [0, 0, 0, 0, 0, 0]
            }
        },
        {
            'name': "plank",
            'type': "Box",
            'args': {
                'extents': PLANK_LWH,
                'b_mass': PLANK_MASS
            },
            'xform': {
                'value': [0, 0, PLANK_LWH[2]/2, 0, 0, 0]
            }
        },
        {
            'name': "run2",
            'type': "DominoRun",
            'args': {
                'extents': DOMINO_LWH,
                'coords': create_line([-SUPPORT_LWH[0]*.25, .01], 90,
                                      SUPPORT_LWH[1]*.25, 7),
                'b_mass': DOMINO_MASS
            },
            'xform': {
                'value': [0, 0, 0, 0, 0, 0]
            }
        },
        {
            'name': "track",
            'type': "Track",
            'args': {
                'extents': TRACK_LWHT,
            },
            'xform': {
                'value': [SUPPORT_LWH[0]/4,
                          SUPPORT_LWH[1]/2-TRACK_LWHT[0]/2,
                          TRACK_LWHT[2]/2,
                          90, 0, 0]
            }
        },
        {
            'name': "ball",
            'type': "Ball",
            'args': {
                'radius': BALL_RADIUS,
                'b_mass': BALL_MASS
            },
            'parent': "track",
            'xform': {
                'value': [-TRACK_LWHT[0]/2+BALL_RADIUS/2,
                          0,
                          BALL_RADIUS-(TRACK_LWHT[2]/2-TRACK_LWHT[3]),
                          0, 0, 0]
            }
        },
        {
            'name': "lever",
            'type': "Lever",
            'args': {
                'extents': LEVER_LWH,
                'pivot_pos': [0, 0, 0],
                'pivot_hpr': [0, 90, 0],
                'pivot_extents': [LEVER_LWH[2]*.4, LEVER_LWH[1]*1.25],
                'b_mass':LEVER_MASS
            },
            'xform': {
                'value': [0,
                          SUPPORT_LWH[1]*.4,
                          .011,
                          0, 0, 0]
            }
        },
        {
            'name': "goblet",
            'type': "Goblet",
            'args': {
                'extents': [
                    GOBLET_HEIGHT,
                    GOBLET_R1,
                    GOBLET_R2
                ]
            },
            'parent': "support2",
            'xform': {
                'value': [SUPPORT2_LWH[0]/4,
                          0,
                          SUPPORT2_LWH[2]/2+.001,
                          0, 0, 0]
            }
        },
    ],
    'causal_graph': []
}
