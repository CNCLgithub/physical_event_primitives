import math
import os
import sys
import time

from panda3d.core import load_prc_file_data, Point2, Point3, Quat, Vec3, Vec4
from direct.gui.DirectGui import DirectButton

sys.path.insert(0, os.path.abspath(".."))
from core import primitives  # noqa: E402
from core.dominoes import create_line, create_smooth_path  # noqa: E402
from core.scenario import Scene, StateObserver, simulate_scene  # noqa: E402
from gui.uimixins import (Animable, Drawable, Pickerable,  # noqa: E402
                          WithViewHelpers)
from gui.uiwidgets import DropdownMenu, ParameterEditor  # noqa: E402
from gui.viewers import Modeler  # noqa: E402


# Default primitive arguments !as seen from the UI!
# keys preceded by _ are not shown in the parameter editor
DEFAULT_PRIMITIVE_ARGS = {
    'Plane': {
        '_name': "plane",
        'nx': 0,
        'ny': 0,
        'nz': 1,
        'distance': 0,
    },
    'Ball': {
        '_name': "ball",
        'radius': .05,
        'mass': .1
    },
    'Box': {
        '_name': "box",
        'length': .1,
        'width': .1,
        'height': .1,
        'mass': .1
    },
    'Track': {
        '_name': "track",
        'length': .2,
        'width': .1,
        'height': .03,
        'thickness': .01,
    },
    'DominoRun': {
        '_name': "run",
        'number': 3,
        'spacing': .03,
        'length': .02,
        'width': .05,
        'height': .1,
        'mass': .1
    },
}


# This function makes the link between UI parameters and actual Primitive
# parameters.
def get_primitive_instance(primitive, **args):
    PrimitiveType = getattr(primitives, primitive)
    # Use 2 for loops: don't iterate over the dict keys and delete keys at the
    # same time.
    hidden = [arg for arg in args.keys() if arg.startswith("_")]
    for arg in hidden:
        args[arg[1:]] = args[arg]
        del args[arg]
    if PrimitiveType is primitives.Plane:
        args['normal'] = (args['nx'], args['ny'], args['nz'])
        del args['nx'], args['ny'], args['nz']
    if PrimitiveType is primitives.Box:
        args['extents'] = [args['length'], args['width'], args['height']]
        del args['length'], args['width'], args['height']
    if PrimitiveType is primitives.Track:
        args['extents'] = [args['length'], args['width'], args['height'],
                           args['thickness']]
        del args['length'], args['width'], args['height'], args['thickness']
    if PrimitiveType is primitives.DominoRun:
        args['extents'] = [args['length'], args['width'], args['height']]
        if 'coords' in args:
            args['coords'] = create_smooth_path(args['coords'], smoothing=.1,
                                                n_doms=int(args['number']))
        else:
            args['coords'] = create_line(
                [0, 0], 0, args['number']*args['spacing'], int(args['number'])
            )
            del args['spacing']
        del args['number'], args['length'], args['width'], args['height']
    return PrimitiveType(**args)


class Designer(Animable, Drawable, Pickerable, WithViewHelpers, Modeler):
    def __init__(self):
        Modeler.__init__(self)

        Animable.__init__(self)

        Drawable.__init__(self, color=Vec4(1, 1, 0, 1))

        Pickerable.__init__(self)
        self.hit_object = None  # NodePath
        self.last_click_time = time.perf_counter()
        self.on_double_click = self.ui_edit_clicked_object
        self.parameter_editor = None  # ParameterEditor

        self.edit_button = DirectButton(
            command=self.ui_set_mode,
            extraArgs=['edit'],
            state='disabled',
            # Button aspect
            relief='flat',
            frameSize=(-.15, .15, -.03, .07),
            frameColor=(Vec4(.3, .3, .3, 1),
                        Vec4(.2, .2, .2, 1),
                        Vec4(.2, .2, .2, 1),
                        Vec4(.2, .2, .2, 1)),
            text="Edit",
            text_scale=.05,
            text_fg=Vec4(1),
            # Position
            parent=self.a2dTopCenter,
            pos=Point3(-.15, 0, -.15),
        )

        self.simulate_button = DirectButton(
            command=self.ui_set_mode,
            extraArgs=['simu'],
            # Button aspect
            relief='flat',
            frameSize=(-.15, .15, -.03, .07),
            frameColor=(Vec4(.3, .3, .3, 1),
                        Vec4(.2, .2, .2, 1),
                        Vec4(.2, .2, .2, 1),
                        Vec4(.2, .2, .2, 1)),
            text="Simulate",
            text_scale=.05,
            text_fg=Vec4(1),
            # Position
            parent=self.a2dTopCenter,
            pos=Point3(.15, 0, -.15),
        )

        self.prim_names = [p.__name__ for p in primitives.get_primitives()]
        self.prim_counter = {p: 0 for p in self.prim_names}
        self.add_menu = DropdownMenu(
            command=self.ui_choose_primitive_from_menu,
            items=self.prim_names,
            # Button aspect
            frameColor=(Vec4(.2, .2, .2, 1),
                        Vec4(.3, .3, .3, 1)),
            frameSize=(-.18, .18, -.04, .07),
            relief='flat',
            # Text
            text="Add primitive",
            text_scale=.05,
            text_fg=Vec4(1, 1, 1, 1),
            # Shadow
            shadowSize=.2,
            # Items
            dropUp=True,
            item_frameColor=Vec4(.25, .25, .25, 1),
            highlightColor=Vec4(.3, .3, .3, 1),
            # Position
            parent=self.a2dBottomRight,
            pos=Point3(-.3, 0, .25*9/16),
        )
        self.add_menu.set_bin('gui-popup', 0)

        self.ui_set_mode('edit')

    def edit_primitive_parameter(self, edited_object, parameter, value):
        parameters = edited_object.get_python_tag('parameters')
        primitive = edited_object.get_tag('primitive')
        parameters.update({parameter: value})
        path = self.instantiate_primitive(primitive, _parent=self.models,
                                          **parameters)
        path.set_transform(edited_object.get_transform())
        self.remove_object(edited_object)
        return path

    def instantiate_primitive(self, primitive, add_defaults=False, _geom='LD',
                              _phys=False, _parent=None, _world=None, **kw):
        if add_defaults:
            args = DEFAULT_PRIMITIVE_ARGS[primitive].copy()
            if '_name' not in kw:
                self.prim_counter[primitive] += 1
                args['_name'] += "_{}".format(self.prim_counter[primitive])
        else:
            args = {}
        args.update(**kw)
        prim = get_primitive_instance(primitive, **args)
        o = prim.create(_geom, _phys, _parent, _world)
        o.set_tag('primitive', primitive)
        o.set_python_tag('parameters', args)
        o.set_python_tag('pickable', True)
        return o

    def remove_object(self, obj):
        if obj is self.hit_object:
            self.hit_object = None
        obj.clear_python_tag(obj.get_python_tag_keys())
        obj.remove_node()

    def ui_choose_primitive_from_menu(self, primitive):
        self.instantiate_primitive(primitive, add_defaults=True,
                                   _parent=self.models)

    def ui_click_left(self):
        click_time = time.perf_counter()
        dt = click_time - self.last_click_time
        self.last_click_time = click_time
        if dt < .5:
            self.on_double_click()

    def ui_create_parameter_editor(self, obj):
        parameters = obj.get_python_tag('parameters')
        name = parameters['_name']
        parameters = [(p, v) for p, v in parameters.items()
                      if not p.startswith("_")]
        parameters.sort()
        editor = ParameterEditor(
            # Shape
            frameSize=(-.2, .2, -.1*len(parameters)/2, .15*len(parameters)/2),
            frameColor=Vec4(.25, .25, .25, 1),
            # Title
            title_text=name,
            title_text_scale=.05,
            title_text_fg=Vec4(1),
            title_frameColor=Vec4(.2, .2, .2, 1),
            # Close button
            close_scale=.05,
            close_text_fg=Vec4(1),
            close_frameColor=(Vec4(.2, .2, .2, 1),
                              Vec4(.3, .3, .3, 1)),
            close_relief='flat',
            # Parameters
            param_text_scale=.05,
            param_text_fg=Vec4(1),
            entry_scale=.05,
            entry_frameColor=Vec4(1),
            entry_width=3,
            # Position
            parent=self.a2dTopRight,
            pos=Point3(-.3, 0, -1*9/16),
            # Specific
            paramData=parameters,
            command=self.ui_enter_value_in_parameter_editor,
            shadowSize=.2,
        )
        if obj.get_tag('primitive') == "DominoRun":
            editor.createcomponent(
                "editPathButton", (), None, DirectButton, (editor,),
                command=self.ui_set_mode,
                extraArgs=['edit_domrun'],
                # Button aspect
                frameSize=(-.15, .15, -.03, .05),
                frameColor=(Vec4(.2, .2, .2, 1),
                            Vec4(.3, .3, .3, 1)),
                relief='flat',
                # Text
                text="Draw path",
                text_fg=Vec4(1),
                text_scale=.04,
                # Position
                pos=Point3(0, 0, editor['frameSize'][2]+.04),
            )
        return editor

    def ui_delete_hit_object(self):
        obj = self.get_hit_object()
        if obj is not None:
            self.remove_object(obj)

    def ui_edit_clicked_object(self):
        obj = self.get_hit_object()
        if obj is None:
            # If user double-clicks in empty space, hide the editor.
            if self.parameter_editor is not None:
                self.parameter_editor.hide()
        else:
            if self.parameter_editor is not None:
                if self.parameter_editor['title_text'] == obj.name:
                    self.parameter_editor.show()
                    return
                else:
                    self.parameter_editor.destroy()
                    self.parameter_editor.remove_node()
            self.parameter_editor = self.ui_create_parameter_editor(obj)

    def ui_enter_value_in_parameter_editor(self, value, parameter):
        o = self.models.find(self.parameter_editor['title_text'] + "*")
        value = int(value) if parameter == "number" else float(value)
        self.edit_primitive_parameter(o, parameter, value)

    def ui_rotate_hit_object(self, clockwise):
        obj = self.get_hit_object()
        if obj is None:
            return
        axis = Vec3()
        self.camLens.extrude_vec(0, axis)
        axis = self.models.get_relative_vector(self.camera, axis)
        axis.normalize()
        angle = math.radians(2) * (-1, 1)[clockwise]
        quat = Quat(math.cos(angle/2), axis * math.sin(angle/2))
        obj.set_quat(obj, quat)

    def ui_run_highlighting_task(self, task):
        if self.hit_object is not None:
            self.hit_object.clear_render_mode()
            self.hit_object = None
        hit = self.get_hit_object()
        if hit is not None:
            hit.set_render_mode_filled_wireframe(.9)
            self.hit_object = hit
        return task.cont

    def ui_run_translate_object_task(self, obj, plane, offset, task):
        new_pos = self.project_mouse_onto_plane(plane)
        if new_pos is not None:
            obj.set_pos(new_pos + offset)
        return task.cont

    def ui_set_mode(self, mode):
        if mode == 'simu':
            self.simulate_button.show()
            self.simulate_button['state'] = 'disabled'
            self.edit_button.show()
            self.edit_button['state'] = 'normal'
            self.add_menu.hide()
            if self.parameter_editor is not None:
                self.parameter_editor.hide()
            if self.models.get_num_children():
                self.ui_simulate_scene()
                self.make_player_controls()
                self.task_mgr.add(self.update_frame, "update_frame")
            # Background tasks
            self.task_mgr.remove("highlighting")
            # Interactions
            self.ignore('mouse1')
            self.ignore('mouse1-up')
            self.ignore('shift-wheel_up')
            self.ignore('shift-wheel_down')
            self.ignore('shift-mouse1')
            self.ignore('delete')
        if mode == 'edit':
            self.edit_button.show()
            self.edit_button['state'] = 'disabled'
            self.simulate_button.show()
            self.simulate_button['state'] = 'normal'
            self.add_menu.show()
            if self._play_controls is not None:
                self._play_controls.hide()
            if self.current_frame > 0:
                self.reset_frame()
            # Background tasks
            self.task_mgr.remove("update_frame")
            self.task_mgr.add(self.ui_run_highlighting_task, "highlighting")
            # Interactions
            self.accept('mouse1', self.ui_click_left)
            self.accept('mouse1-up', self.ui_stop_left_mouse_task)
            self.accept('shift-wheel_up', self.ui_rotate_hit_object, [True])
            self.accept('shift-wheel_down', self.ui_rotate_hit_object, [False])
            self.accept('shift-mouse1', self.ui_translate_hit_object)
            self.accept('delete', self.ui_delete_hit_object)
        if mode == 'edit_domrun':
            self.edit_button.hide()
            self.simulate_button.hide()
            self.add_menu.hide()
            domrun = self.models.find(self.parameter_editor['title_text'])
            self.parameter_editor.destroy()
            self.parameter_editor.remove_node()
            self.view_top()
            self.set_show_tip(True)
            # Background tasks
            self.task_mgr.remove("highlighting")
            # Interactions
            self.accept('mouse1', self.ui_start_drawing_dompath, [domrun])
            self.ignore('mouse1-up')
            self.ignore('shift-wheel_up')
            self.ignore('shift-wheel_down')
            self.ignore('shift-mouse1')
            self.ignore('delete')

    def ui_simulate_scene(self, duration=2., fps=500):
        scene = Scene(geom=None, phys=True)
        for o in self.models.get_children():
            prim_name = o.get_tag('primitive')
            args = o.get_python_tag('parameters').copy()
            args.update(_geom=None, _phys=True, _parent=scene.graph,
                        _world=scene.world)
            path = self.instantiate_primitive(prim_name, **args)
            path.set_transform(o.get_transform())
        obs = StateObserver(scene)
        simulate_scene(scene, duration, 1/fps, [obs])
        self.load_frames(obs.states, fps)

    def ui_start_drawing_dompath(self, domrun):
        self.set_draw(True)
        self.accept('mouse1-up', self.ui_stop_drawing_dompath, [domrun])

    def ui_stop_drawing_dompath(self, domrun):
        self.set_show_tip(False)
        self.set_draw(False)
        stroke = self.strokes.pop()
        self.clear_drawing()
        if len(stroke) > 2:
            # Project the drawing
            plane = self.compute_view_orthogonal_plane(domrun)
            for point in stroke:
                point[0], point[1], _ = self._project_mouse_pos_onto_plane(
                    Point2(*point), plane
                )
            # Update the primitive
            parameters = domrun.get_python_tag('parameters')
            if 'spacing' in parameters:
                del parameters['spacing']
            domrun = self.edit_primitive_parameter(domrun, "_coords", stroke)
        self.parameter_editor = self.ui_create_parameter_editor(domrun)
        self.ui_set_mode('edit')

    def ui_stop_left_mouse_task(self):
        self.task_mgr.remove("translate_object")

    def ui_translate_hit_object(self):
        obj = self.hit_object
        if obj is None:
            return
        # Compute the translation plane now, as it needs to stay fixed
        plane = self.compute_view_orthogonal_plane(obj)
        # Compute the initial offset between mouse and object
        offset = obj.get_pos() - self.project_mouse_onto_plane(plane)
        self.task_mgr.add(
            self.ui_run_translate_object_task, "translate_object",
            extraArgs=[obj, plane, offset], appendTask=True
        )


def main():
    load_prc_file_data("", "win-origin 100 100")
    load_prc_file_data("", "win-size 1600 900")
    load_prc_file_data("", "window-title Chain Reaction Designer")
    # load_prc_file_data("", "framebuffer-multisample 1")
    # load_prc_file_data("", "multisamples 2")

    app = Designer()
    app.run()


if __name__ == "__main__":
    main()
