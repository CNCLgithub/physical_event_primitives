import bpy


bpy.ops.object.delete(use_global=False)


#directory = "/Users/scyasuda/Desktop/physical_event_primitives/causal_graphs/demos/"
directory = "./"

file = input()

bpy.ops.import_scene.egg(filepath=directory+file, directory=directory, files=[{"name":file, "name":file}])
