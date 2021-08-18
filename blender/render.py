"""
Script to set up Cycles rendering. Sets the correct GPU without changing the
blend file.

Usage
-----
blender -b path/to/file.blend -P path/to/render.py -- $NV_GPU

"""
import bpy
import sys
import os

filename = bpy.path.basename(bpy.data.filepath)
filename = os.path.splitext(filename)[0]

# bpy.context.scene.eevee.gi_diffuse_bounces = 1
# bpy.context.scene.eevee.taa_render_samples = 5

# cycles_prefs = bpy.context.preferences.addons['cycles'].preferences
# #cycles_prefs.compute_device_type = 'CUDA'
# print("Devices: {}".format(list(cycles_prefs.devices)))
# guid = int(sys.argv[-1])
# print("Using GPU {}".format(guid))
#for i in range(4):
#    cycles_prefs.devices[i].use = (i == guid)
scene = bpy.data.scenes['Scene']
#scene.cycles.device = 'GPU'
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_percentage = 100
scene.render.filepath = filename
print("Rendering to {}".format(scene.render.filepath))

bpy.ops.render.render(animation=True)
