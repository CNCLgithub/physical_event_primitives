import bpy
import os

bpy.ops.object.delete(use_global=False)

# getting arguments after "--"
import sys
argv = sys.argv
try:
    index = argv.index("--") + 1
except ValueError:
    index = len(argv)
argv = argv[index:]
    
scenario_dir = argv[0]
trace = argv[1]

fname = '{trace}.egg'.format(trace=trace)
filepath = os.path.join(scenario_dir, fname)
bpy.ops.import_scene.egg(filepath=filepath, directory=scenario_dir, files=[{"name":fname, "name":fname}])
