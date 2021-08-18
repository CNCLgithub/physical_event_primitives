from math import atan, degrees

DENSITY = 1

# Randomness: Size of Ball, standard = .02
BALL_RADIUS = random.uniform(0.005, 0.03)  # [m]
BALL_MASS = BALL_RADIUS * math.pi * (4/3) * DENSITY  # [kg]
BALL_RESTITUTION = 0.8

HIGH_PLANK_LWH = (0.235, 0.023, 0.008)  # [m]

#Randomness: Size of plank, standard: scale = 1
scale = random.uniform(.5, 1.5)
BASE_PLANK_LWH = (0.55*scale, 0.1*scale, 0.005*scale)  # [m]
BASE_PLANK_MASS = BASE_PLANK_LWH[0] * BASE_PLANK_LWH[1] * BASE_PLANK_LWH[2] * DENSITY  # [kg]

#Randomness: Size of Goblet, standard: GOBLET_R1 = .036
GOBLET_HEIGHT = 0.11  # [m]
GOBLET_R1 = random.uniform(.02, .05)  # [m]
GOBLET_R2 = 0.025  # [m]
GOBLET_EPS = .002  # [m]

# Randomness: Ball or plank
if random.random() < .5:
    movingObject = {
            'name': "ball",
            'type': "Ball",
            'args': {
                'radius': BALL_RADIUS,
                'b_mass': BALL_MASS,
                'b_restitution': BALL_RESTITUTION
            },
            'xform': {
                'value': [0, BASE_PLANK_LWH[1]/2 + .01, .5,
                          0, 0, 0]
            }
        }
else:
    movingObject = {
            'name': "plank",
            'type': "Box",
            'args': {
                'extents': HIGH_PLANK_LWH,
                'force': (0,0,0),
                'b_mass': BALL_MASS,
                'b_restitution': BALL_RESTITUTION
            },
            'xform': {
                'value': [0, BASE_PLANK_LWH[1]/2 + .01, .5,
                          0, 0, 0]
            }
        }

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
        movingObject,
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
                'value': [random.uniform(-.005, .005), GOBLET_R1, 0, .004, 0, 0]
            }
        },
    ],
}
