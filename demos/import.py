import bpy


bpy.ops.object.delete(use_global=False)


directory = "/Users/Winnie/Desktop/physical_event_primitives/demos/"

file = input()

bpy.ops.import_scene.egg(filepath=directory+file, directory="/Users/Winnie/Desktop/physical_event_primitives/demos/", files=[{"name":file, "name":file}])
