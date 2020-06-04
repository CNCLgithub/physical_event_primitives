from math import atan, degrees
import math
import random
import json

# Which scene trace are you loading in? (Currently doesn't work because need to edit the import_scenario function located in core/scenario.py and how this function is called in demos/import_scenario.py ...)
# which_trace=sys.argv[1]

# Load in the file that contains the generated items (should be based on a seed input but just default now)
with open('gen_jsons/scene_trace_containment_Gen0.json') as f:
    trace = json.load(f)


DENSITY = 1

if trace["is_ball"]:
    # Randomness: size of ball
    BALL_RADIUS = trace['ball_radius']  # [m]
    BALL_MASS = BALL_RADIUS * math.pi * (4/3) * DENSITY  # [kg]
    BALL_RESTITUTION = 0.8
else:
    # Randomness: size of plank
    FLAT_SUPPORT_LWH = (trace['plank_lwh']['length'],trace['plank_lwh']['width'],trace['plank_lwh']['height']) # [m]
    HIGH_PLANK_MASS = FLAT_SUPPORT_LWH[0] * FLAT_SUPPORT_LWH[1] * FLAT_SUPPORT_LWH[2] * DENSITY # [kg]



TOP_TRACK_LWHT = (0.5, 0.05, 0.006, 0.003)  # [m]
BOTTOM_TRACK_LWHT = TOP_TRACK_LWHT  # [m]

HIGH_PLANK_LWH = (0.235, 0.023, 0.008)  # [m]
HIGH_PLANK_RESTITUTION = 0.8


# Randomness: Size of Goblet
GOBLET_HEIGHT = trace['goblet']['height']  # [m]
GOBLET_R1 = trace['goblet']['R1']   # [m]
GOBLET_R2 = trace['goblet']['R2']  # [m]
GOBLET_EPS = trace['goblet']['EPS']   # [m]

# Randomness: Ball or plank
if trace["is_ball"]:
    movingObject = {
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
    }
else:
    movingObject = {
            'name': "plank",
            'type': "Box",
            'args': {
                'extents': FLAT_SUPPORT_LWH,
                # Randomness: force on plank
                'force': (trace['force'],0,0),
                'b_mass': HIGH_PLANK_MASS,
                'b_restitution': HIGH_PLANK_RESTITUTION
            },
            'parent': "track",
            'xform': {
                'value': [
                    BOTTOM_TRACK_LWHT[0]/2-.02, 0,  0.028, # Previously used ball radius which isn't defined
                          0, 0, 60
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
                'extents': BOTTOM_TRACK_LWHT,
            },
            # Randomness: height and angle of ramp
            'xform': {
                'value': [0,
                          BOTTOM_TRACK_LWHT[1]/2+.01,
                          .2+BOTTOM_TRACK_LWHT[2]/2+.05+trace['ramp']['height'],
                          0, 0, -5+trace['ramp']['angle']],
            }
        },
        movingObject,
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
            'parent': "track",
            # Randomness: position of goblet
            'xform': {
                'value': [-.35, GOBLET_R1-.02, -.08, 0, 0, 40],
            }
        },
    ],
}
