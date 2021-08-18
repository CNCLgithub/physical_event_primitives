BALL_FRICTION = .1
# BALL_MASS = 0.013  # [kg]
BALL_MASS = 0.006  # [kg]
# BALL_RADIUS = 0.0105  # [m]
BALL_RADIUS = 0.008  # [m]
BALL_RESTITUTION = 0.8
BLOCKER_LWH = (.01, .025, .005)  # [m]
FLAT_SUPPORT_LWH = (.02, .025, .005)  # [m]
GOBLET_ANGULAR_DAMPING = 1
GOBLET_LINEAR_DAMPING = .1
GOBLET_FRICTION = 1
GOBLET_HEIGHT = 0.11  # [m]
GOBLET_MASS = .005  # [g]
GOBLET_R1 = 0.036  # [m]
GOBLET_R2 = 0.025  # [m]
GOBLET_EPS = .002  # [m]
LEFT_PULLEY_ROPE_LENGTH = .95  # [m]
LONG_TRACK_LWHT = (0.3, 0.025, 0.008, .002)  # [m]
LONG_TRACK_MASS = .01  # [kg] TODO
NAIL_LEVER_LWH = (0.11, 0.005, 0.002)  # [m]
NAIL_LEVER_MASS = 0.01  # [kg]
PIVOT_LENGTH = .06  # [m]
PIVOT_RADIUS = .004  # [m]
PLANK_LWH = (0.1175, 0.023, 0.008)  # [m]
PLANK_MASS = 0.01  # [kg]
PLANK_RESTITUTION = 0.8
PULLEY_HPR = (0, 90, 0)
QUAD_PLANK_LWH = (0.031, 0.023, 0.1175)  # [m]
RIGHT_PULLEY_PIVOT_HEIGHT = .003  # [m]
RIGHT_PULLEY_PIVOT_RADIUS = .006  # [m]
RIGHT_PULLEY_ROPE_LENGTH = 1.  # [m]
RIGHT_WEIGHT_HEIGHT = 0.0315  # [m]
RIGHT_WEIGHT_MASS = 0.2  # [kg]
RIGHT_WEIGHT_RADIUS = 0.0315 / 2  # [m]
SHORT_TRACK_LWHT = (0.15, 0.025, 0.008, .002)  # [m]
SMOL_TRACK_LWHT = (0.1, 0.025, 0.008, .002)  # [m]
SMOL_WEIGHT_HEIGHT = 0.014  # [m]
SMOL_WEIGHT_RADIUS = 0.0075  # [m]
SMOL_WEIGHT_MASS = 0.02  # [kg]
STARTING_TRACK_FRICTION = 1
STARTING_TRACK_LWHT = (0.3, 0.025, 0.005, .002)  # [m]
TEAPOT_FRICTION = .1
TEAPOT_LID_ANGULAR_DAMPING = 1
TEAPOT_LID_HEIGHT = .005  # [m]
TEAPOT_LID_MASS = 0.002  # [kg]
TEAPOT_LID_RADIUS = GOBLET_R1
TINY_TRACK_LWH = (0.1, 0.025, 0.005)  # [m]
TINY_TRACK_MASS = .01  # [kg]
GATE_PULLEY_ROPE_LENGTH = .50  # [m]
GATE_PULLEY_ROPE_EXTENTS = (.002, .5, .01)   # [m]
PULLEY_EXTENTS = (.005, .02)  # [m]
GATE_PUSHER_GUIDE_LWHT = (0.099, 0.016, 0.012, 0.003)  # [m]

PIVOTING_ANGULAR_VELOCITY = 1
ROLLING_ANGVEL = 10
MOVING_LINEAR_VELOCITY = 1e-2

DATA = {
    'scene': [
        {
            'name': "start_track_origin",
            'type': "Empty",
            'args': {},
            'xform': {
                'value': [-.33, 0, .105, 0, 0, 13],
            }
        },
        {
            'name': "start_track",
            'type': "Track",
            'args': {
                'extents': STARTING_TRACK_LWHT,
            },
            'parent': "start_track_origin",
            'xform': {
                'value': [STARTING_TRACK_LWHT[0]/2, 0, 0, 0, 0, 0],
            }
        },
        {
            'name': "ball1",
            'type': "Ball",
            'args': {
                'radius': BALL_RADIUS,
                'b_mass': BALL_MASS,
                'b_restitution': BALL_RESTITUTION
            },
            'parent': "start_track",
            'xform': {
                'value': [-.095, 0, BALL_RADIUS+.002, 0, 0, 0]
            }
        },
        {
            'name': "ball2",
            'type': "Ball",
            'args': {
                'radius': BALL_RADIUS,
                'b_mass': BALL_MASS,
                'b_friction': BALL_FRICTION,
                'b_restitution': BALL_RESTITUTION
            },
            'parent': "start_track",
            'xform': {
                'value': [-.13, 0, BALL_RADIUS+.002, 0, 0, 0]
            }
        },
        {
            'name': "cage",
            'type': "Goblet",
            'args': {
                'extents': [
                    GOBLET_HEIGHT,
                    GOBLET_R1,
                    GOBLET_R2,
                    GOBLET_EPS
                ],
                'b_mass': GOBLET_MASS,
                'b_friction': GOBLET_FRICTION,
                'b_linear_damping': GOBLET_LINEAR_DAMPING,
                'b_angular_damping': GOBLET_ANGULAR_DAMPING,
            },
            'xform': {
                'value': [-.32, 0, .21, 0, 0, 180],
            }
        },
        {
            'name': "cage_support",
            'type': "Box",
            'args': {
                'extents': PLANK_LWH,
            },
            'xform': {
                'value': [-.32, 0, .093, 90, 0, 0]
            }
        },
        {
            'name': "gate",
            'type': "Box",
            'args': {
                'extents': PLANK_LWH,
                'b_mass': PLANK_MASS,
            },
            'xform': {
                'value': [0, 0, .15, 0, 0, 90],
            }
        },
        {
            'name': "gate_pulley",
            'type': "RopePulley",
            'args': {
                'comp1_pos': [0, 0, 0],
                'comp2_pos': [-PLANK_LWH[0]/2, 0, 0],
                # 'rope_extents': GATE_PULLEY_ROPE_EXTENTS,
                'rope_length': GATE_PULLEY_ROPE_LENGTH,
                'pulleys': [[-.32, 0, .29], [0, 0, .29]],
                'pulley_extents': PULLEY_EXTENTS,
                'pulley_hpr': PULLEY_HPR
            },
            'components': ["cage", "gate"],
        },
        {
            'name': "gate_guide_left",
            'type': "Box",
            'args': {
                'extents': PLANK_LWH,
            },
            'xform': {
                'value': [-.02, 0, .20, 90, 0, 0],
            }
        },
        # {
        #     'name': "gate_guide_back",
        #     'type': "Box",
        #     'args': {
        #         'extents': PLANK_LWH,
        #     },
        #     'xform': {
        #         'value': [0, .02, .15, 90, 0, 90],
        #     }
        # },
        # {
        #     'name': "gate_guide_right",
        #     'type': "Box",
        #     'args': {
        #         'extents': PLANK_LWH,
        #     },
        #     'xform': {
        #         'value': [.01, 0, .18, 0, 0, 90],
        #     }
        # },
        {
            'name': "gate_pusher_guide",
            'type': "Track",
            'args': {
                'extents': GATE_PUSHER_GUIDE_LWHT,
            },
            'xform': {
                'value': [PLANK_LWH[0]/2-.007, 0, .08, 0, 0, 0],
            }
        },
        {
            'name': "gate_pusher",
            'type': "Box",
            'args': {
                'extents': PLANK_LWH,
                'b_mass': PLANK_MASS
            },
            'parent': "gate_pusher_guide",
            'xform': {
                'value': [.011, 0, .009, 0, 90, 0],
            }
        },
        {
            'name': "hit_lever",
            'type': "Lever",
            'args': {
                'extents': PLANK_LWH,
                'pivot_pos': [0, 0, .005],
                'pivot_hpr': [0, 90, 0],
                'pivot_extents': [PIVOT_RADIUS, PIVOT_LENGTH],
                'b_mass': PLANK_MASS
            },
            'parent': "gate_pusher_guide",
            'xform': {
                'value': [.074, 0, -.04, 0, 0, 90],
            }
        },
        {
            'name': "middle_track",
            'type': "Track",
            'args': {
                'extents': SMOL_TRACK_LWHT,
            },
            'xform': {
                'value': [.05, 0, 0, 0, 0, 0],
                'range': [
                    None,
                    None,
                    [-.02, .01],
                    None,
                    None,
                    None,
                ]
            }
        },
        {
            'name': "right_track_top",
            'type': "Track",
            'args': {
                'extents': SHORT_TRACK_LWHT,
            },
            'xform': {
                'value': [.16, 0, -.05, 0, 0, 3],
                'range': [
                    [.14, .18],
                    None,
                    [-.07, -.03],
                    None,
                    None,
                    [1, 6],
                ]
            }
        },
        {
            'name': "right_track_middle_origin",
            'type': "Empty",
            'args': {},
            'parent': "left_balance_track_blocker",
            'xform': {
                'value': [0, .001, PLANK_LWH[2]/2, -90, 0, -6],
                'range': [
                    None,
                    None,
                    None,
                    None,
                    None,
                    [-8, -1],
                ]
            }
        },
        {
            'name': "right_track_middle",
            'type': "Track",
            'args': {
                'extents': SHORT_TRACK_LWHT,
            },
            'parent': "right_track_middle_origin",
            'xform': {
                'value': [SHORT_TRACK_LWHT[0]/2, 0, SHORT_TRACK_LWHT[2]/2,
                          0, 0, 0],
            }
        },
        {
            'name': "balance_track",
            'type': "Track",
            'args': {
                'extents': STARTING_TRACK_LWHT,
                'b_mass': LONG_TRACK_MASS
            },
            'xform': {
                'value': [.16, 0, -.17, 0, 0, 0],
            }
        },
        {
            'name': "balance_track_left_weight",
            'type': "Cylinder",
            'args': {
                'extents': [SMOL_WEIGHT_RADIUS, SMOL_WEIGHT_HEIGHT],
                'b_mass': SMOL_WEIGHT_MASS
            },
            'parent': "balance_track",
            'xform': {
                'value': [-STARTING_TRACK_LWHT[0]/2+.002,
                          0,
                          -STARTING_TRACK_LWHT[2]/2+STARTING_TRACK_LWHT[3]+(
                              SMOL_WEIGHT_HEIGHT/2),
                          0, 0, 0],
            }
        },
        {
            'name': "balance_track_right_weight",
            'type': "Cylinder",
            'args': {
                'extents': [SMOL_WEIGHT_RADIUS, SMOL_WEIGHT_HEIGHT],
                'b_mass': SMOL_WEIGHT_MASS
            },
            'parent': "balance_track",
            'xform': {
                'value': [STARTING_TRACK_LWHT[0]/2-.01,
                          0,
                          -STARTING_TRACK_LWHT[2]/2-SMOL_WEIGHT_HEIGHT/2,
                          0, 0, 0],
            }
        },
        {
            'name': "fastener1",
            'type': "Fastener",
            'args': {
                'comp1_xform': [
                    STARTING_TRACK_LWHT[0]/2-.01, 0, -STARTING_TRACK_LWHT[2]/2,
                    0, 0, 0
                ],
                'comp2_xform': [0, 0, SMOL_WEIGHT_HEIGHT/2, 0, 0, 0]
            },
            'components': ["balance_track", "balance_track_right_weight"]
        },
        {
            'name': "balance_track_pivot",
            'type': "Pivot",
            'args': {
                'pivot_pos': [0,
                              0,
                              -STARTING_TRACK_LWHT[2]/2-.003],
                'pivot_hpr': [0, 90, 0],
                'pivot_extents': [PIVOT_RADIUS, PIVOT_LENGTH],
            },
            'components': ["balance_track"],
        },
        {
            'name': "balance_track_blocker",
            'type': "Box",
            'args': {
                'extents': PLANK_LWH
            },
            'xform': {
                'value': [.20, 0, -.18, 90, 0, 0],
            }
        },
        {
            'name': "bridge_blocker",
            'type': "Box",
            'args': {
                'extents': BLOCKER_LWH,
                'b_mass': .001
            },
            'parent': "balance_track",
            'xform': {
                'value': [-STARTING_TRACK_LWHT[0]/3,
                          0,
                          -STARTING_TRACK_LWHT[2]/2-BLOCKER_LWH[0]/2,
                          0, 0, -90],
            }
        },
        {
            'name': "fastener2",
            'type': "Fastener",
            'args': {
                'comp1_xform': [
                    -STARTING_TRACK_LWHT[0]/3, 0, -STARTING_TRACK_LWHT[2]/2,
                    0, 0, 0
                ],
                'comp2_xform': [BLOCKER_LWH[0]/2, 0, 0, 0, 0, 90]
            },
            'components': ["balance_track", "bridge_blocker"]
        },
        {
            'name': "right_track_bottom",
            'type': "Track",
            'args': {
                'extents': LONG_TRACK_LWHT,
            },
            'xform': {
                'value': [.35, 0, -.26, 0, 0, -10],
                'range': [
                    [.33, .37],
                    None,
                    [-.28, -.24],
                    None,
                    None,
                    [-15, -5],
                ]
            }
        },
        {
            'name': "left_balance_track",
            'type': "Track",
            'args': {
                'extents': LONG_TRACK_LWHT,
                'b_mass': LONG_TRACK_MASS
            },
            'xform': {
                'value': [.03, 0, -.125, 0, 0, 0],
            }
        },
        {
            'name': "left_balance_track_pivot",
            'type': "Pivot",
            'args': {
                'pivot_pos': [0,
                              0,
                              -LONG_TRACK_LWHT[2]/2-.003],
                'pivot_hpr': [0, 90, 0],
                'pivot_extents': [PIVOT_RADIUS, PIVOT_LENGTH],
            },
            'components': ["left_balance_track"],
        },
        {
            'name': "left_balance_track_blocker",
            'type': "Box",
            'args': {
                'extents': PLANK_LWH
            },
            'xform': {
                'value': [.19, 0, -.135, 90, 0, 0],
            }
        },
        {
            'name': "left_track_top",
            'type': "Track",
            'args': {
                'extents': SHORT_TRACK_LWHT,
            },
            'xform': {
                'value': [-.03, 0, -.03, 0, 0, -5],
                'range': [
                    [-.05, -.01],
                    None,
                    [-.05, -.01],
                    None,
                    None,
                    [-9, -1],
                ]
            }
        },
        {
            'name': "left_track_middle",
            'type': "Track",
            'args': {
                'extents': SHORT_TRACK_LWHT,
            },
            'xform': {
                'value': [-.14, 0, -.07, 0, 0, 14],
                'range': [
                    [-.16, -.12],
                    None,
                    [-.09, -.05],
                    None,
                    None,
                    [10, 18],
                ]
            }
        },
        {
            'name': "left_track_bottom_origin",
            'type': "Empty",
            'args': {},
            'parent': "bridge_support",
            'xform': {
                'value': [0, 0, PLANK_LWH[2]/2+.02, -90, 0, 5],
                'range': [
                    None,
                    None,
                    None,
                    None,
                    None,
                    [1, 9],
                ]
            }
        },
        {
            'name': "left_track_bottom",
            'type': "Track",
            'args': {
                'extents': LONG_TRACK_LWHT,
            },
            'parent': "left_track_bottom_origin",
            'xform': {
                'value': [-LONG_TRACK_LWHT[0]/2, 0, LONG_TRACK_LWHT[2]/2,
                          0, 0, 0],
            }
        },
        {
            'name': "bridge",
            'type': "Track",
            'args': {
                'extents': SHORT_TRACK_LWHT,
                'b_mass': PLANK_MASS
            },
            'xform': {
                'value': [.09, 0, -.25, 0, 0, 80],
            }
        },
        {
            'name': "bridge_pivot",
            'type': "Pivot",
            'args': {
                'pivot_pos': [SHORT_TRACK_LWHT[0]/2-.002,
                              0,
                              -SHORT_TRACK_LWHT[2]/2-.004],
                'pivot_hpr': [0, 90, 0],
                'pivot_extents': [PIVOT_RADIUS, PIVOT_LENGTH],
            },
            'components': ["bridge"],
        },
        {
            'name': "bridge_support",
            'type': "Box",
            'args': {
                'extents': PLANK_LWH
            },
            'xform': {
                'value': [-.05, 0, -.29, 90, 0, 0],
            }
        },
        {
            'name': "pit",
            'type': "Goblet",
            'args': {
                'extents': [
                    GOBLET_HEIGHT,
                    GOBLET_R1,
                    GOBLET_R2,
                    GOBLET_EPS
                ],
            },
            'xform': {
                'value': [-.02, 0, -.45, 0, 0, 0]
            }
        },
        {
            'name': "teapot",
            'type': "Goblet",
            'args': {
                'extents': [
                    GOBLET_HEIGHT,
                    GOBLET_R1,
                    GOBLET_R2,
                    GOBLET_EPS
                ],
            },
            'xform': {
                'value': [.15, 0, -.45, 0, 0, 0],
                'range': [
                    None,
                    None,
                    [-.46, -.44],
                    None,
                    None,
                    None,
                ]
            }
        },
    ],
    'causal_graph': [
        # ------------------------- FIRST TIMELINE ---------------------------
        {
            'name': "ball1_rolls_on_start_track",
            'type': "RollingOn",
            'args': {
                'rolling': "ball1",
                'support': "start_track",
                'min_angvel': ROLLING_ANGVEL
            },
            'children': [
                "ball1_rolls_on_middle_track",
            ]
        },
        {
            'name': "ball1_rolls_on_middle_track",
            'type': "RollingOn",
            'args': {
                'rolling': "ball1",
                'support': "middle_track",
                'min_angvel': ROLLING_ANGVEL
            },
            'children': [
                "ball1_hits_lever",
            ]
        },
        {
            'name': "ball1_hits_lever",
            'type': "Contact",
            'args': {
                'first': "ball1",
                'second': "hit_lever"
            },
            'children': [
                "ball1_rolls_on_right_track_top",
                "gate_falls",
            ]
        },
        {
            'name': "ball1_rolls_on_right_track_top",
            'type': "RollingOn",
            'args': {
                'rolling': "ball1",
                'support': "right_track_top",
                'min_angvel': ROLLING_ANGVEL
            },
            'children': [
                "ball1_rolls_on_right_track_middle",
            ]
        },
        {
            'name': "ball1_rolls_on_right_track_middle",
            'type': "RollingOn",
            'args': {
                'rolling': "ball1",
                'support': "right_track_middle",
                'min_angvel': ROLLING_ANGVEL
            },
            'children': [
                "ball1_rolls_on_balance_track",
            ]
        },
        {
            'name': "ball1_rolls_on_balance_track",
            'type': "RollingOn",
            'args': {
                'rolling': "ball1",
                'support': "balance_track",
                'min_angvel': ROLLING_ANGVEL
            },
            'children': [
                "ball1_hits_balance_track_weight",
            ]
        },
        {
            'name': "ball1_hits_balance_track_weight",
            'type': "Contact",
            'args': {
                'first': "ball1",
                'second': "balance_track_left_weight"
            },
            'children': [
                "balance_track_pivots",
            ]
        },
        {
            'name': "balance_track_pivots",
            'type': "Pivoting",
            'args': {
                'body': "balance_track",
                'min_angvel': PIVOTING_ANGULAR_VELOCITY,
            },
            'children': [
                "ball1_rolls_on_balance_track_in_reverse",
                "bridge_pivots",
            ]
        },
        {
            'name': "ball1_rolls_on_balance_track_in_reverse",
            'type': "RollingOn",
            'args': {
                'rolling': "ball1",
                'support': "balance_track",
                'min_angvel': ROLLING_ANGVEL
            },
            'children': [
                "ball1_rolls_on_right_track_bottom",
            ]
        },
        {
            'name': "ball1_rolls_on_right_track_bottom",
            'type': "RollingOn",
            'args': {
                'rolling': "ball1",
                'support': "right_track_bottom",
                'min_angvel': ROLLING_ANGVEL
            },
            'children': [
                "ball1_goes_in_teapot",
            ]
        },
        {
            'name': "ball1_goes_in_teapot",
            'type': "Inclusion",
            'args': {
                'inside': "ball1",
                'outside': "teapot",
            },
            'children': [
                "ball2_meets_ball1_and_they_lived_happily_ever_after",
            ]
        },
        {
            'name': "ball2_meets_ball1_and_they_lived_happily_ever_after",
            'type': "Contact",
            'args': {
                'first': "ball2",
                'second': "ball1"
            },
        },
        # ------------------------ SECOND TIMELINE ---------------------------
        {
            'name': "gate_falls",
            'type': "Falling",
            'args': {
                'body': "gate",
                'min_linvel': MOVING_LINEAR_VELOCITY
            },
            'children': [
                "cage_rises",
            ]
        },
        {
            'name': "cage_rises",
            'type': "Rising",
            'args': {
                'body': "cage",
                'min_linvel': MOVING_LINEAR_VELOCITY
            },
            'children': [
                "ball2_rolls_on_start_track",
            ]
        },
        {
            'name': "ball2_rolls_on_start_track",
            'type': "RollingOn",
            'args': {
                'rolling': "ball2",
                'support': "start_track",
                'min_angvel': ROLLING_ANGVEL
            },
            'children': [
                "ball2_hits_gate",
            ]
        },
        {
            'name': "ball2_hits_gate",
            'type': "Contact",
            'args': {
                'first': "ball2",
                'second': "gate"
            },
            'children': [
                "ball2_rolls_on_left_track_top",
            ]
        },
        {
            'name': "ball2_rolls_on_left_track_top",
            'type': "RollingOn",
            'args': {
                'rolling': "ball2",
                'support': "left_track_top",
                'min_angvel': ROLLING_ANGVEL
            },
            'children': [
                "ball2_rolls_on_left_track_middle",
            ]
        },
        {
            'name': "ball2_rolls_on_left_track_middle",
            'type': "RollingOn",
            'args': {
                'rolling': "ball2",
                'support': "left_track_middle",
                'min_angvel': ROLLING_ANGVEL
            },
            'children': [
                "ball2_rolls_on_left_balance_track",
            ]
        },
        {
            'name': "ball2_rolls_on_left_balance_track",
            'type': "RollingOn",
            'args': {
                'rolling': "ball2",
                'support': "left_balance_track",
                'min_angvel': ROLLING_ANGVEL
            },
            'children': [
                "left_balance_track_pivots",
            ]
        },
        {
            'name': "left_balance_track_pivots",
            'type': "Pivoting",
            'args': {
                'body': "left_balance_track",
                'min_angvel': PIVOTING_ANGULAR_VELOCITY,
            },
            'children': [
                "ball2_rolls_on_left_track_bottom",
                "ball1_rolls_on_balance_track",
            ]
        },
        {
            'name': "ball2_rolls_on_left_track_bottom",
            'type': "RollingOn",
            'args': {
                'rolling': "ball2",
                'support': "left_track_bottom",
                'min_angvel': ROLLING_ANGVEL
            },
            'children': [
                "ball2_rolls_on_bridge",
            ]
        },
        {
            'name': "ball2_rolls_on_bridge",
            'type': "RollingOn",
            'args': {
                'rolling': "ball2",
                'support': "bridge",
                'min_angvel': ROLLING_ANGVEL
            },
            'children': [
                "ball2_goes_in_teapot",
            ]
        },
        {
            'name': "ball2_goes_in_teapot",
            'type': "Inclusion",
            'args': {
                'inside': "ball2",
                'outside': "teapot",
            },
            'children': [
                "ball2_meets_ball1_and_they_lived_happily_ever_after",
            ]
        },
        # ------------------------ BRIDGE TIMELINE ---------------------------
        {
            'name': "bridge_pivots",
            'type': "Pivoting",
            'args': {
                'body': "bridge",
                'min_angvel': PIVOTING_ANGULAR_VELOCITY,
            },
            'children': [
                "ball2_rolls_on_bridge",
            ]
        },
    ]
}
