import bpy
import os

bpy.ops.object.delete(use_global=False)


directory = os.getcwd()

file = input()

bpy.ops.import_scene.egg(filepath=directory+file, directory="/Users/Winnie/Desktop/physical_event_primitives/demos/", files=[{"name":file, "name":file}])
