"""
Script to set up Cycles rendering. Sets the correct GPU without changing the
blend file.

Usage
-----
blender -b path/to/file.blend -P path/to/render.py -- $NV_GPU

"""
import bpy
import sys


cycles_prefs = bpy.context.preferences.addons['cycles'].preferences
#cycles_prefs.compute_device_type = 'CUDA'
print("Devices: {}".format(list(cycles_prefs.devices)))
guid = int(sys.argv[-1])
print("Using GPU {}".format(guid))
#for i in range(4):
#    cycles_prefs.devices[i].use = (i == guid)
scene = bpy.data.scenes['Scene']
#scene.cycles.device = 'GPU'
scene.cycles.engine = 'CYCLES'
scene.render.resolution_percentage = 100
print("Rendering to {}".format(scene.render.filepath))

bpy.ops.render.render(animation=True)
