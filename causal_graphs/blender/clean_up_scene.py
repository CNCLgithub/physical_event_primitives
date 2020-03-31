import bpy




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
    
    obj_camera.location[0] = -0.02
    obj_camera.location[1] = 1.79
    obj_camera.location[2] = 0.28
    
    obj_camera.rotation_euler[0] = 1.5708
    obj_camera.rotation_euler[1] = 0
    obj_camera.rotation_euler[2] = 3.14159

    # ball = bpy.data.objects['ball_geom']
    # new_color = bpy.data.materials.new(name="ball_color")
    # new_color.use_nodes = False
    # new_color.diffuse_color = (0.8, 0, 0, 1)
    # ball.material = new_color














main()
