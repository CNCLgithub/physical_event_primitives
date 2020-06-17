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
                    "occluder_lwh": {"length": random.uniform(0.1,0.4), 
                                           "width": random.uniform(0.0005,0.0001), 
                                           "height": random.uniform(0.1,0.6)},
                    "occluder_pos": random.uniform(0,.3)}

        else:
            trace = {"is_ball": False,
                    "plank_lwh": {"length": random.uniform(0.01,0.03), 
                                           "width": random.uniform(0.01,0.03), 
                                           "height": random.uniform(0.01,0.03)},
                    "force": random.uniform(0.01,0.04),
                    "occluder_lwh": {"length": random.uniform(0.1,0.4), 
                                           "width": random.uniform(0.0005,0.0001), 
                                           "height": random.uniform(0.1,0.6)},
                    "occluder_pos": random.uniform(0,.3)}     
        # Save
        with open(gen_json_path, 'w') as fp:
            json.dump(trace, fp)

            
    # Tell us about it! 
    print(trace)
    
    ## Now create the scene
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

    TOP_TRACK_LWHT = (0.3, 0.025, 0.006, 0.003)  # [m]

    # Randomness: size of occluder
    HIGH_PLANK_LWH = (trace["occluder_lwh"]['length'], trace["occluder_lwh"]['width'], trace["occluder_lwh"]['height'])  # [m]
    HIGH_PLANK_RESTITUTION = 0.8

    # Randomness: Ball or Plank
    if trace["is_ball"]:
        movingObject = {
                'name': "ball",
                'type': "Ball",
                'args': {
                    'radius': BALL_RADIUS,
                    # Randomness: force on object
                    'force': (trace["force"],0,0),
                    'b_mass': BALL_MASS,
                    'b_restitution': BALL_RESTITUTION
                },
                'xform': {
                    'value': [-TOP_TRACK_LWHT[0], BALL_RADIUS*4, BALL_RADIUS+.002,
                              0, 0, 0]
                }
        }
    else:
        movingObject = { 
                'name': "plank",
                'type': "Box",
                'args': {
                    'extents': FLAT_SUPPORT_LWH,
                    # Randomness: force on object
                    'force': (trace["force"],0,0),
                    'b_mass': HIGH_PLANK_MASS,
                    'b_restitution': HIGH_PLANK_RESTITUTION
                },
                'xform': {
                    'value': [-TOP_TRACK_LWHT[0]/2+.01, 0, FLAT_SUPPORT_LWH[0]/2,
                        0, 0, 90],
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
                }
            },
            movingObject,
            {
                'name': "occluder",
                'type': "Box",
                'args': {
                    'extents': HIGH_PLANK_LWH,
                    'force': (0,0,0)
                },
                # Randomness: position of occluder
                'xform': {
                    'value': [.3, trace["occluder_pos"], .05, 0, 0, 90],
                }
            },
            
        ],
        'causal_graph' : False
    }

    return DATA
