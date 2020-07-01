import bpy
import os
import sys

print(sys.version)
print()
blend_dir = os.path.dirname(bpy.data.filepath)
sys.path.append(os.path.join(os.getcwd(),'blender/python_blender_modules'))
print('sys.path:', sys.path, '\n\n')


# pytorch3d stuff to sample point from the blender meshes
print("importing pytorch3d stuff...")
from pytorch3d.io import load_obj, save_obj
from pytorch3d.structures import Meshes
from pytorch3d.utils import ico_sphere
from pytorch3d.ops import sample_points_from_meshes
print("imported pytorch3d!\n\n")

# import other libraries
import torch
import numpy as np

# visualization
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['savefig.dpi'] = 80
mpl.rcParams['figure.dpi'] = 80

# let's visulize some meshes!!!!!
def plot_pointcloud(mesh, title=""):
    # Sample points uniformly from the surface of the mesh.
    points = sample_points_from_meshes(mesh, 1000)
    x, y, z = points.clone().detach().cpu().squeeze().unbind(1)    
    fig = plt.figure(figsize=(5, 5))
    ax = Axes3D(fig)
    ax.scatter3D(x, z, -y)
    ax.set_xlabel('x')
    ax.set_ylabel('z')
    ax.set_zlabel('y')
    ax.set_title(title)
    ax.view_init(190, 30)
    plt.savefig(title+'.png')


### getting arguments after "--"
import sys
argv = sys.argv
try:
    index = argv.index("--") + 1
except ValueError:
    index = len(argv)
argv = argv[index:]
##############################

scenario_dir = argv[0]
trace = argv[1]


meshes = {}
# getting the meshes of the objects
for ob in bpy.data.objects:
    print(ob.name, "mesh", ob.data)
    
    if ob.type == 'MESH':
        meshes[ob.name] = ob.data


# data.polygons to get faces!! (somehow)
# pytorch3d needs vertices and faces

pt_meshes = {}
for name in meshes:
    # print(name)
    mesh = meshes[name]

    V = torch.empty(len(mesh.vertices), 3)
    F = torch.empty(len(mesh.polygons), 3)

    for i in range(len(mesh.vertices)):
        # .co gets the vector
        V[i,:] = torch.tensor(mesh.vertices[i].co)
    
    for i in range(len(mesh.polygons)):
        F[i,:] = torch.tensor(mesh.polygons[i].vertices)
    
    pt_meshes[name] = Meshes(verts=[V], faces=[F])

for name in pt_meshes:
    plot_pointcloud(pt_meshes[name], name)
