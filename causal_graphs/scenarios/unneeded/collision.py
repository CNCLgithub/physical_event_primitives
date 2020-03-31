import os
import sys

sys.path.insert(0, os.path.abspath(".."))
from core.dominoes import (create_branch, create_line,  # noqa: E402
                           create_wave, create_x_switch)


SUPPORT_LWH = [.175, .33, .093]
DOMINO_LWH = [.007, .02, .044]
DOMINO_MASS = .00305
PLANK_LWH = [.008, .024, .118]
PLANK_MASS = .01
TRACK_LWHT = [.30, .024, .005, .001]
TRACK2_LWHT = [.30, .024, .010, .001]
BALL_RADIUS = .01
BALL_MASS = .008
BRANCH_LENGTH = .20
BRANCH_WIDTH = .12
STRAIGHT_LENGTH = .08
WAVE_LENGTH = .3
WAVE_WIDTH = .11
SWITCH_WIDTH = .12

LEFT_FASTER = 1
FASTER_END = ('left', 'right')[LEFT_FASTER]
SLOWER_END = ('right', 'left')[LEFT_FASTER]
FASTER_DOM_ID = (16, 8)[LEFT_FASTER]
SLOWER_DOM_ID = (8, 16)[LEFT_FASTER]

DATA = {
    'scene': [
        {
            'name': "ground",
            'type': "Plane",
            'args': {
                'normal': [0, 0, 1],
                'distance': 0
            },
        },
        {
            'name': "support",
            'type': "Box",
            'args': {
                'extents': SUPPORT_LWH
            },
            'xform': {
                'value': [0, -SUPPORT_LWH[1]*2, SUPPORT_LWH[2]/2, 0, 0, 0]
            }
        },
        {
            'name': "support2",
            'type': "Box",
            'args': {
                'extents': SUPPORT_LWH
            },
            'xform': {
                'value': [0, SUPPORT_LWH[1]*2, SUPPORT_LWH[2]/2, 0, 0, 0]
            }
        },

        # {
        #     'name': "branch_run",
        #     'type': "DominoRun",
        #     'args': {
        #         'extents': DOMINO_LWH,
        #         'coords': create_branch([0, 0], 0,
        #                                 BRANCH_LENGTH, BRANCH_WIDTH, 5),
        #         'tilt_angle': 10,
        #         'b_mass': DOMINO_MASS
        #     },
        #     'parent': "support",
        #     'xform': {
        #         'value': [0, -.08, SUPPORT_LWH[2]/2, 90, 0, 0]
        #     }
        # },
        # {
        #     'name': "smol_run",
        #     'type': "DominoRun",
        #     'args': {
        #         'extents': DOMINO_LWH,
        #         'coords': create_line([0, 0], 0, .02, 2),
        #         'b_mass': DOMINO_MASS
        #     },
        #     'parent': "support",
        #     'xform': {
        #         'value': [BRANCH_WIDTH/2,
        #                   SUPPORT_LWH[1]/2-.025,
        #                   SUPPORT_LWH[2]/2,
        #                   90, 0, 0]
        #     }
        # },
        {
            'name': "ball",
            'type': "Ball",
            'args': {
                'radius': BALL_RADIUS,
                'b_mass': BALL_MASS
            },
            'parent': "support",
            'xform': {
                'value': [-BRANCH_WIDTH/2,
                          SUPPORT_LWH[1]/2,
                          BALL_RADIUS+SUPPORT_LWH[2]/2,
                          0, 0, 0]
            }
        },

        {
            'name': "ball2",
            'type': "Ball",
            'args': {
                'radius': BALL_RADIUS,
                'b_mass': BALL_MASS
            },
            'parent': "support",
            'xform': {
                'value': [-BRANCH_WIDTH/2,
                          SUPPORT_LWH[1]*3.5,
                          BALL_RADIUS+SUPPORT_LWH[2]/2,
                          0, 0, 0]
            }
        },
        {
            'name': "ball_guide1",
            'type': "Box",
            'args': {
                'extents': [DOMINO_LWH[1], DOMINO_LWH[2], DOMINO_LWH[0]],
            },
            'parent': "support",
            'xform': {
                'value': [-BRANCH_WIDTH/2-DOMINO_LWH[1]-.003,
                          SUPPORT_LWH[1]/2-DOMINO_LWH[2]/2,
                          DOMINO_LWH[0]/2+SUPPORT_LWH[2]/2,
                          0, 0, 0]
            }
        },
        {
            'name': "ball_guide2",
            'type': "Box",
            'args': {
                'extents': [DOMINO_LWH[1], DOMINO_LWH[2], DOMINO_LWH[0]],
            },
            'parent': "support",
            'xform': {
                'value': [-BRANCH_WIDTH/2+DOMINO_LWH[1]+.003,
                          SUPPORT_LWH[1]/2-DOMINO_LWH[2]/2,
                          DOMINO_LWH[0]/2+SUPPORT_LWH[2]/2,
                          0, 0, 0]
            }
        },
        {
            'name': "track_joint",
            'type': "Empty",
            'args': {
            },
            'parent': "support",
            'xform': {
                'value': [-BRANCH_WIDTH/2,
                          SUPPORT_LWH[1]/2,
                          SUPPORT_LWH[2]/2,
                          0, -13, 0],
                'range': [
                    None,
                    None,
                    [0, SUPPORT_LWH[2]/2-TRACK_LWHT[3]],
                    None,
                    [-18, 0],
                    None
                ]
            }
        },
        {
            'name': "track",
            'type': "Track",
            'args': {
                'extents': TRACK_LWHT,
            },
            'parent': "track_joint",
            'xform': {
                'value': [0,
                          TRACK_LWHT[0]/2,
                          TRACK_LWHT[2]/2,
                          90, 0, 0]
            }
        },
        #        {
        #     'name': "ball_guide3",
        #     'type': "Box",
        #     'args': {
        #         'extents': [DOMINO_LWH[1], DOMINO_LWH[2], DOMINO_LWH[0]],
        #     },
        #     'parent': "support",
        #     'xform': {
        #         'value': [-BRANCH_WIDTH/2-DOMINO_LWH[1]-.003,
        #                   SUPPORT_LWH[1]/2-DOMINO_LWH[2]/2,
        #                   DOMINO_LWH[0]/2+SUPPORT_LWH[2]/2,
        #                   0, 0, 0]
        #     }
        # },
        # {
        #     'name': "ball_guide4",
        #     'type': "Box",
        #     'args': {
        #         'extents': [DOMINO_LWH[1], DOMINO_LWH[2], DOMINO_LWH[0]],
        #     },
        #     'parent': "support",
        #     'xform': {
        #         'value': [-BRANCH_WIDTH/2+DOMINO_LWH[1]+.003,
        #                   SUPPORT_LWH[1]/2-DOMINO_LWH[2]/2,
        #                   DOMINO_LWH[0]/2+SUPPORT_LWH[2]/2,
        #                   0, 0, 0]
        #     }
        # },
        {
            'name': "track_joint2",
            'type': "Empty",
            'args': {
            },
            'parent': "support2",
            'xform': {
                'value': [-BRANCH_WIDTH/2,
                          SUPPORT_LWH[1]/2,
                          SUPPORT_LWH[2]/2-TRACK2_LWHT[3],
                          0, 13, 0],
                'range': [
                    None,
                    None,
                    [0, SUPPORT_LWH[2]/2-TRACK2_LWHT[3]],
                    None,
                    [18, 0],
                    None
                ]
            }
        },
        {
            'name': "track2",
            'type': "Track",
            'args': {
                'extents': TRACK_LWHT,
            },
            'parent': "track_joint2",
            'xform': {
                'value': [0,
                          TRACK2_LWHT[0]*2.8,
                          TRACK2_LWHT[2],
                          -90, 0, 0]
            }
        },
        # {
        #     'name': "plank",
        #     'type': "Box",
        #     'args': {
        #         'extents': PLANK_LWH,
        #         'b_mass': PLANK_MASS
        #     },
        #     'xform': {
        #         'value': [BRANCH_WIDTH/2, .03, PLANK_LWH[2]/2, 90, 0, 0],
        #         'range': [None, [.01, .04], None, None, None, None]
        #     }
        # },
        # {
        #     'name': "straight_run",
        #     'type': "DominoRun",
        #     'args': {
        #         'extents': DOMINO_LWH,
        #         'coords': create_line([0, 0], 0, STRAIGHT_LENGTH, 5),
        #         'b_mass': DOMINO_MASS
        #     },
        #     'parent': "switch_run",
        #     'xform': {
        #         'value': [-STRAIGHT_LENGTH-.02, 0, 0, 0, 0, 0]
        #     }
        # },
        # {
        #     'name': "wavey_run",
        #     'type': "DominoRun",
        #     'args': {
        #         'extents': DOMINO_LWH,
        #         'coords': create_wave([0, 0], 0, WAVE_LENGTH, WAVE_WIDTH, 22),
        #         'b_mass': DOMINO_MASS
        #     },
        #     'parent': "switch_run",
        #     'xform': {
        #         'value': [-WAVE_LENGTH-.02, -SWITCH_WIDTH, 0, 0, 0, 0]
        #     }
        # },
        # {
        #     'name': "switch_run",
        #     'type': "DominoRun",
        #     'args': {
        #         'extents': DOMINO_LWH,
        #         'coords': create_x_switch([0, 0], 0, SWITCH_WIDTH, 9),
        #         'b_mass': DOMINO_MASS
        #     },
        #     'xform': {
        #         'value': [-SWITCH_WIDTH/2, .43, 0, 90, 0, 0],
        #         'range': [None, [.40, .46], None, None, None, None]
        #     }
        # },
        # {
        #     'name': "switch_guide1",
        #     'type': "Box",
        #     'args': {
        #         'extents': [DOMINO_LWH[0], DOMINO_LWH[2], DOMINO_LWH[1]],
        #         'b_mass': DOMINO_MASS
        #     },
        #     'parent': "switch_run",
        #     'xform': {
        #         'value': [SWITCH_WIDTH-.038, -SWITCH_WIDTH/2-.02,
        #                   DOMINO_LWH[1]/2,
        #                   45, 0, 0]
        #     }
        # },
        # {
        #     'name': "switch_guide2",
        #     'type': "Box",
        #     'args': {
        #         'extents': [DOMINO_LWH[0], DOMINO_LWH[2], DOMINO_LWH[1]],
        #         'b_mass': DOMINO_MASS
        #     },
        #     'parent': "switch_run",
        #     'xform': {
        #         'value': [SWITCH_WIDTH-.038, -SWITCH_WIDTH/2+.02,
        #                   DOMINO_LWH[1]/2,
        #                   -45, 0, 0]
        #     }
        # },
    ],
    # 'causal_graph': [
    #     {
    #         'name': "first_dom_topples",
    #         'type': "Toppling",
    #         'args': {
    #             'body': "branch_run_dom_0",
    #             'angle': 15
    #         },
    #         'children': [
    #             "left_dom_of_branch_hits_ball",
    #             "right_dom_of_branch_hits_plank",
    #         ]
    #     },
    #     {
    #         'name': "left_dom_of_branch_hits_ball",
    #         'type': "Contact",
    #         'args': {
    #             'first': "branch_run_dom_9",
    #             'second': "ball"
    #         },
    #         'children': [
    #             "ball_rolls_on_track",
    #         ]
    #     },
    #     {
    #         'name': "ball_rolls_on_track",
    #         'type': "RollingOn",
    #         'args': {
    #             'rolling': "ball",
    #             'support': "track",
    #             'min_angvel': 10,
    #         },
    #         'children': [
    #             "ball_hits_first_dom_of_left_row",
    #         ]
    #     },
    #     {
    #         'name': "ball_hits_first_dom_of_left_row",
    #         'type': "Contact",
    #         'args': {
    #             'first': "ball",
    #             'second': "straight_run_dom_0"
    #         },
    #         'children': [
    #             "first_dom_of_left_row_topples",
    #         ]
    #     },
    #     {
    #         'name': "first_dom_of_left_row_topples",
    #         'type': "Toppling",
    #         'args': {
    #             'body': "straight_run_dom_0",
    #             'angle': 15
    #         },
    #         'children': [
    #             "left_dom_of_switch_topples",
    #         ]
    #     },
    #     {
    #         'name': "left_dom_of_switch_topples",
    #         'type': "Toppling",
    #         'args': {
    #             'body': "switch_run_dom_0",
    #             'angle': 15
    #         },
    #         'children': [
    #             "center_dom_of_switch_topples",
    #         ]
    #     },
    #     {
    #         'name': "right_dom_of_branch_hits_plank",
    #         'type': "Contact",
    #         'args': {
    #             'first': "smol_run_dom_1",
    #             'second': "plank"
    #         },
    #         'children': [
    #             "plank_topples",
    #         ]
    #     },
    #     {
    #         'name': "plank_topples",
    #         'type': "Toppling",
    #         'args': {
    #             'body': "plank",
    #             'angle': 15
    #         },
    #         'children': [
    #             "plank_hits_first_dom_of_wave",
    #         ]
    #     },
    #     {
    #         'name': "plank_hits_first_dom_of_wave",
    #         'type': "Contact",
    #         'args': {
    #             'first': "plank",
    #             'second': "wavey_run_dom_0"
    #         },
    #         'children': [
    #             "first_dom_of_wave_topples",
    #         ]
    #     },
    #     {
    #         'name': "first_dom_of_wave_topples",
    #         'type': "Toppling",
    #         'args': {
    #             'body': "wavey_run_dom_0",
    #             'angle': 15
    #         },
    #         'children': [
    #             "right_dom_of_switch_topples",
    #         ]
    #     },
    #     {
    #         'name': "right_dom_of_switch_topples",
    #         'type': "Toppling",
    #         'args': {
    #             'body': "switch_run_dom_9",
    #             'angle': 15
    #         },
    #         'children': [
    #             "center_dom_of_switch_topples",
    #         ]
    #     },
    #     {
    #         'name': "center_dom_of_switch_topples",
    #         'type': "Toppling",
    #         'args': {
    #             'body': "switch_run_dom_4",
    #             'angle': 15
    #         },
    #         'children': [
    #             "{}_end_dom_of_switch_topples".format(FASTER_END),
    #         ]
    #     },
    #     {
    #         'name': "{}_end_dom_of_switch_topples".format(FASTER_END),
    #         'type': "Toppling",
    #         'args': {
    #             'body': "switch_run_dom_{}".format(FASTER_DOM_ID),
    #             'angle': 15
    #         },
    #         'children': [
    #             "{}_end_dom_of_switch_remains".format(SLOWER_END),
    #         ]
    #     },
    #     {
    #         'name': "{}_end_dom_of_switch_remains".format(SLOWER_END),
    #         'type': "NotMoving",
    #         'args': {
    #             'body': "switch_run_dom_{}".format(SLOWER_DOM_ID),
    #         }
    #     },
    # ]
}
