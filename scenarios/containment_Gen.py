from math import atan, degrees

import math
import random
import sys
import os
import json

def get_scene_data(gen_json_path):
    
    # Load or make the random decisions
    
    if os.path.exists(gen_json_path):
        
        # Load in the file that contains the generated items
        with open(gen_json_path) as f:
            trace = json.load(f)

    else:
        
        # Make the random decisions in python
        if random.random() < .5:

            # Make the trace for a ball
            trace = {"is_ball": True,
                    "ball_radius": random.uniform(0.005,.3),
                    "force": random.uniform(8,13),
                    "goblet": {"height": random.uniform(0.05,0.15), 
                                           "R1": random.uniform(0.01,0.06), 
                                           "R2": random.uniform(0.01,0.06),
                                           "EPS": random.uniform(0.001,0.003)},
                    "ramp": {"height":random.uniform(-0.05,0.05),
                             "angle": random.uniform(-10,5)}}

        else:
            trace = {"is_ball": False,
                    "plank_lwh": {"length": random.uniform(0.01,0.03), 
                                           "width": random.uniform(0.01,0.03), 
                                           "height": random.uniform(0.01,0.03)},
                    "force": random.uniform(-0.002,-0.01),
                    "goblet": {"height": random.uniform(0.05,0.15), 
                                           "R1": random.uniform(0.01,0.06), 
                                           "R2": random.uniform(0.01,0.06),
                                           "EPS": random.uniform(0.001,0.003)},
                    "ramp": {"height":random.uniform(-0.05,0.05),
                             "angle": random.uniform(-10,5)}}
        # Save
        with open(gen_json_path, 'w') as fp:
            json.dump(trace, fp)                 
            
    # Tell us about it! 
    print(trace)         
        

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
    
    return DATA
