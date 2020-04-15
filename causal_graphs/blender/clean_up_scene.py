import bpy
import sys



context = bpy.context
view_layer = context.view_layer


def clean_up(objects):
    for o in objects:
        if o.type == 'MESH':
            view_layer.objects.active = o
            bpy.ops.mesh.customdata_custom_splitnormals_clear()
        if o.type == 'EMPTY':
            o.hide_set(True)


def main():
    bpy.ops.object.select_all(action='SELECT')
    init = context.active_object
    clean_up(context.selected_objects)
    view_layer.objects.active = init
    
    obj_camera = bpy.context.scene.camera
    
    obj_camera.location[0] = 0.17
    obj_camera.location[1] = 1.65
    obj_camera.location[2] = 0.20
    
    obj_camera.rotation_euler[0] = 1.5708
    obj_camera.rotation_euler[1] = 0
    obj_camera.rotation_euler[2] = 3.14159

    moving = sys.argv[sys.argv.index("--") + 1]

    if "Ball" in moving:
        ball = bpy.data.objects['ball_geom']
        new_color = bpy.data.materials.new(name="ball_color")
        new_color.use_nodes = False
        new_color.diffuse_color = (0.8, 0, 0, 1)
        ball.active_material = new_color

    if "2Ball" in moving:
        ball2 = bpy.data.objects['ball2_geom']
        new_color2 = bpy.data.materials.new(name="ball_color2")
        new_color2.use_nodes = False
        new_color2.diffuse_color = (0.084, 0.246, 0.8, 1)
        ball2.active_material = new_color2

    if "Plank" in moving:
        plank = bpy.data.objects['plank_geom']
        new_color3 = bpy.data.materials.new(name="plank_color")
        new_color3.use_nodes = False
        if "BallPlank" in moving:
            new_color3.diffuse_color = (0.084, 0.246, 0.8, 1)
        else:
            new_color3.diffuse_color = (0.8, 0, 0, 1)
        plank.active_material = new_color3

    if "2Plank" in moving:
        plank2 = bpy.data.objects['plank2_geom']
        new_color4 = bpy.data.materials.new(name="plank_color2")
        new_color4.use_nodes = False
        new_color4.diffuse_color = (0.084, 0.246, 0.8, 1)
        plank2.active_material = new_color4

    if "containment" in moving:
        goblet = bpy.data.objects['goblet_geom']
        new_color5 = bpy.data.materials.new(name="goblet_color")
        new_color5.use_nodes = False
        new_color5.diffuse_color = (1, 1, 1, .2)
        goblet.active_material = new_color5



main()



