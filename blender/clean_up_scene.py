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

    if bpy.data.objects.get("ball_geom") is not None:
        ball = bpy.data.objects['ball_geom']
        new_color = bpy.data.materials.new(name="ball_color")
        new_color.use_nodes = False
        new_color.diffuse_color = (0.8, 0, 0, 1)
        ball.active_material = new_color

    if bpy.data.objects.get("ball2_geom") is not None:
        ball2 = bpy.data.objects['ball2_geom']
        new_color2 = bpy.data.materials.new(name="ball_color2")
        new_color2.use_nodes = False
        new_color2.diffuse_color = (0.084, 0.246, 0.8, 1)
        ball2.active_material = new_color2

    if bpy.data.objects.get("ball3_geom") is not None:
        ball3 = bpy.data.objects['ball3_geom']
        new_color9 = bpy.data.materials.new(name="ball_color3")
        new_color9.use_nodes = False
        new_color9.diffuse_color = (0.084, 0.246, 0.8, 1)
        ball3.active_material = new_color9

    if bpy.data.objects.get("ball4_geom") is not None:
        ball4 = bpy.data.objects['ball4_geom']
        new_color12 = bpy.data.materials.new(name="ball_color4")
        new_color12.use_nodes = False
        new_color12.diffuse_color = (1, 0.245, 0.003, 1)
        ball4.active_material = new_color12

    if bpy.data.objects.get("ball5_geom") is not None:
        ball5 = bpy.data.objects['ball5_geom']
        new_color17 = bpy.data.materials.new(name="ball_color5")
        new_color17.use_nodes = False
        new_color17.diffuse_color = (1, 0.245, 0.003, 1)
        ball5.active_material = new_color17

    if bpy.data.objects.get("plank_geom") is not None:
        plank = bpy.data.objects['plank_geom']
        new_color3 = bpy.data.materials.new(name="plank_color")
        new_color3.use_nodes = False
        new_color3.diffuse_color = (0.084, 0.246, 0.8, 1)
        plank.active_material = new_color3

    if bpy.data.objects.get("plank2_geom") is not None:
        plank2 = bpy.data.objects['plank2_geom']
        new_color4 = bpy.data.materials.new(name="plank_color2")
        new_color4.use_nodes = False
        new_color4.diffuse_color = (0.084, 0.246, 0.8, 1)
        plank2.active_material = new_color4

    if bpy.data.objects.get("plank3_geom") is not None:
        plank3 = bpy.data.objects['plank3_geom']
        new_color10 = bpy.data.materials.new(name="plank_color3")
        new_color10.use_nodes = False
        new_color10.diffuse_color = (0.084, 0.246, 0.8, 1)
        plank3.active_material = new_color10

    if bpy.data.objects.get("plank4_geom") is not None:
        plank4 = bpy.data.objects['plank4_geom']
        new_color13 = bpy.data.materials.new(name="plank_color4")
        new_color13.use_nodes = False
        new_color13.diffuse_color = (0.084, 0.246, 0.8, 1)
        plank4.active_material = new_color13

    if bpy.data.objects.get("plank5_geom") is not None:
        plank5 = bpy.data.objects['plank5_geom']
        new_color18 = bpy.data.materials.new(name="plank5_color5")
        new_color18.use_nodes = False
        new_color18.diffuse_color = (0, .5, 0, 1)
        plank5.active_material = new_color18
    
    if bpy.data.objects.get("plank6_geom") is not None:
        plank6 = bpy.data.objects['plank6_geom']
        new_color18 = bpy.data.materials.new(name="plank6_color6")
        new_color18.use_nodes = False
        new_color18.diffuse_color = (0, .5, 0, 1)
        plank5.active_material = new_color18
    
    if bpy.data.objects.get("goblet_geom") is not None:
        goblet = bpy.data.objects['goblet_geom']
        new_color5 = bpy.data.materials.new(name="goblet_color")
        new_color5.use_nodes = False
        new_color5.diffuse_color = (.338, 0.169, 0.169, 1)
        goblet.active_material = new_color5

    if bpy.data.objects.get("goblet2_geom") is not None:
        goblet2 = bpy.data.objects['goblet2_geom']
        new_color15 = bpy.data.materials.new(name="goblet_color2")
        new_color15.use_nodes = False
        new_color15.diffuse_color = (.338, 0.169, 0.169, 1)
        goblet2.active_material = new_color15

    if bpy.data.objects.get("goblet3_geom") is not None:
        goblet3 = bpy.data.objects['goblet3_geom']
        new_color20 = bpy.data.materials.new(name="goblet_color3")
        new_color20.use_nodes = False
        new_color20.diffuse_color = (.921, .334, 1, 1)
        goblet3.active_material = new_color20

    if bpy.data.objects.get("goblet4_geom") is not None:
        goblet4 = bpy.data.objects['goblet4_geom']
        new_color21 = bpy.data.materials.new(name="goblet_color4")
        new_color21.use_nodes = False
        new_color21.diffuse_color = (.338, 0.169, 0.169, 1)
        goblet4.active_material = new_color21

    if bpy.data.objects.get("occluder_geom") is not None:
        occluder = bpy.data.objects['occluder_geom']
        new_color6 = bpy.data.materials.new(name="occluder_color")
        new_color6.use_nodes = False
        new_color6.diffuse_color = (0, .5, 0, 1)
        occluder.active_material = new_color6

    if bpy.data.objects.get("occluder2_geom") is not None:
        occluder2 = bpy.data.objects['occluder2_geom']
        new_color8 = bpy.data.materials.new(name="occluder_color2")
        new_color8.use_nodes = False
        new_color8.diffuse_color = (0, .5, 0, 1)
        occluder2.active_material = new_color8

    if bpy.data.objects.get("occluder3_geom") is not None:
        occluder3 = bpy.data.objects['occluder3_geom']
        new_color17 = bpy.data.materials.new(name="occluder_color3")
        new_color17.use_nodes = False
        new_color17.diffuse_color = (0, .5, 0, 1)
        occluder3.active_material = new_color17

    if bpy.data.objects.get("track_geom") is not None:
        track = bpy.data.objects['track_geom']
        new_color7 = bpy.data.materials.new(name="track_color")
        new_color7.use_nodes = False
        new_color7.diffuse_color = (0, .8, 0, 1)
        track.active_material = new_color7

    if bpy.data.objects.get("track2_geom") is not None:
        track2 = bpy.data.objects['track2_geom']
        new_color14 = bpy.data.materials.new(name="track_color2")
        new_color14.use_nodes = False
        new_color14.diffuse_color = (0, .8, 0, 1)
        track2.active_material = new_color14

    if bpy.data.objects.get("track3_geom") is not None:
        track3 = bpy.data.objects['track3_geom']
        new_color16 = bpy.data.materials.new(name="track_color3")
        new_color16.use_nodes = False
        new_color16.diffuse_color = (0, .8, 0, 1)
        track3.active_material = new_color16

    if bpy.data.objects.get("track4_geom") is not None:
        track4 = bpy.data.objects['track4_geom']
        new_color22 = bpy.data.materials.new(name="track_color4")
        new_color22.use_nodes = False
        new_color22.diffuse_color = (0, .8, 0, 1)
        track4.active_material = new_color22

    if bpy.data.objects.get("cylinder_geom") is not None:
        cylinder = bpy.data.objects['cylinder_geom']
        new_color19 = bpy.data.materials.new(name="cylinder_color")
        new_color19.use_nodes = False
        new_color19.diffuse_color = (1, 0.785, 0.023, 1)
        cylinder.active_material = new_color19

    if bpy.data.objects.get("cylinder2_geom") is not None:
        cylinder2 = bpy.data.objects['cylinder2_geom']
        new_color22 = bpy.data.materials.new(name="cylinder_color2")
        new_color22.use_nodes = False
        new_color22.diffuse_color = (1, 0.245, 0.003, 1)
        cylinder2.active_material = new_color22


main()



