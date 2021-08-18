
import sys

# Event Types: (Rolling, Sliding,) Falling, Topple, Collision, Containment, Occlusion
# Object Types: Ball, Cube, Plank, Goblet, Track, Occluder, Wall, Floor

class Object:
	def __init__(self, name, type, extents, radius, force, b_mass, b_restitution, value):
    self.name = name
    self.radius = radius
    self.age = age
    self.type = type
    self.extents = extents
    self.force = force
    self.b_mass = b_mass
    self.b_restitution, value

class Wall:
	def __init__(self, name, type, normal, distance):
		self.name = name
		self.type = type
		self.normal = normal
		self.distance = 0

if __name__ == '__main__':

	objectList = []

	numEvents = len(sys.argv)

	if numEvents == 1:

	# if numEvents == 2:

	# if numEvents == 3:

	# List of all Objects
	# Dictionary of variables