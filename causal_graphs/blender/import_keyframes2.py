import pickle

import bpy
from bpy_extras.io_utils import ImportHelper


class StatesImporter(bpy.types.Operator, ImportHelper):
    bl_idname = "custom.states_importer"
    bl_label = "Import"
    filename_ext = ".pkl"

    def execute(self, context):
#        path = self.properties.filepath
        path = "/Users/scyasuda/Desktop/causal_graphs/demos/fallingBall_success.pkl"
#        self.report({'INFO'}, "Importing {}".format(path))
        import_states(path)
        return {'FINISHED'}

classes = (
    StatesImporter,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


def import_states(path):
    with open(path, 'rb') as f:
        data = pickle.load(f)
    fps = data['metadata']['fps']
    states = data['states']
    # Set keyframes
    scene = bpy.context.scene
    max_frame = 0

    for o in scene.objects:
        # print(o)
        try:
            o_states = states[o.name]
        except KeyError:
            continue
        try:
            #o.game.properties['save_scale']
            has_scale = False
        except KeyError:
            has_scale = False
        print("Keyframing {}".format(o))
        o.rotation_mode = 'QUATERNION'
        for state in o_states:
            t, x, y, z, w, i, j, k, *_ = state
            frame = int(t*fps) + 1
            if has_scale:
                sx, sy, sz = state[-3:]
            else:
                sx = 1
                sy = 1 
                sz = 1
                
            o.scale = (sx, sy, sz)
            o.keyframe_insert(data_path='scale', frame=frame)
            o.location = (x, y, z)
            o.rotation_quaternion = (w, i, j, k)
            o.keyframe_insert(data_path='location', frame=frame)
            o.keyframe_insert(data_path='rotation_quaternion', frame=frame)
        # Keep track of max frame.
        # Do it after the for loop because highest frame is always last!
        if frame > max_frame:
            max_frame = frame
    # Set time remapping
    render = scene.render
    new_fps = render.fps
    print("Remapping {}FPS to {}FPS".format(fps, new_fps))
    render.frame_map_old = fps
    render.frame_map_new = new_fps
    scene.frame_end = max_frame * new_fps // fps


if __name__ == "__main__":
    register()
    bpy.ops.custom.states_importer('INVOKE_DEFAULT')

