"""
Various UI functionalities.

"""
import datetime
import math

import numpy as np
from direct.interval.IntervalGlobal import Func, LerpFunc, Parallel, Sequence
from panda3d.core import (CardMaker, CollisionHandlerQueue, CollisionNode,
                          CollisionRay, CollisionTraverser, GeomNode, LineSegs,
                          Plane, Point2, Point3, Quat, Vec3, Vec4)

from gui.geom2d import make_circle
from gui.uiwidgets import PlayerControls


class Focusable:
    """Mixin to add smooth focus functionality to a Modeler.

    """
    def __init__(self):
        self._focus_anim = None
        self._focused = False

    def focus_view(self, nodepath):
        if (self._focused
            or (self._focus_anim is not None
                and self._focus_anim.is_playing())):
            return
        # Get new desired state
        bounds = nodepath.get_bounds()
        center = bounds.get_center()
        radius = bounds.get_radius()
        lens = self.camLens
        fov = min(lens.get_fov()) * math.pi / 180  # min between X and Z axes
        distance = radius / math.tan(fov * .5)
        #  idealFarPlane = distance + radius * 1.5
        #  lens.setFar(max(lens.getDefaultFar(), idealFarPlane))
        #  idealNearPlane = distance - radius
        #  lens.setNear(min(lens.getDefaultNear(), idealNearPlane))

        # Save original state
        self._unfocus_state = {
                'pos': self.pivot.get_pos(),
                'hpr': self.pivot.get_hpr(),
                'zoom': self.cam_distance
                }
        # Launch animation
        time = 1.
        # Note: using the Quat version ensures that the rotation takes the
        # shortest path. We can still give it an HPR argument, which is
        # (I think) easier to visualize than
        # "Quat(0, 0, 1/sqrt(2), 1/sqrt(2))".
        change_rigid = self.pivot.posQuatInterval(
                duration=time,
                pos=center + Vec3(0, 0, distance),
                hpr=Vec3(180, 90, 0),
                blendType='easeOut')
        change_zoom = LerpFunc(
                lambda x: setattr(self, "cam_distance", x),
                duration=time,
                fromData=self.cam_distance,
                toData=distance,
                blendType='easeOut')
        self._focus_anim = Sequence(
                Func(lambda: setattr(self, "move_highlight", False)),
                Parallel(change_rigid, change_zoom),
                Func(lambda: setattr(self, "_focused", True)))
        self._focus_anim.start()

    def unfocus_view(self):
        if (not self._focused
            or (self._focus_anim is not None
                and self._focus_anim.is_playing())):
            return
        # Launch animation
        time = 1.
        change_rigid = self.pivot.posQuatInterval(
                duration=time,
                pos=self._unfocus_state['pos'],
                hpr=self._unfocus_state['hpr'],
                blendType='easeOut')
        change_zoom = LerpFunc(
                lambda x: setattr(self, "cam_distance", x),
                duration=time,
                fromData=self.cam_distance,
                toData=self._unfocus_state['zoom'],
                blendType='easeOut')
        self._focus_anim = Sequence(
                Parallel(change_rigid, change_zoom),
                Func(lambda: setattr(self, "move_highlight", True)),
                Func(lambda: setattr(self, "_focused", False)))
        self._focus_anim.start()


class Tileable:
    """Mixin adding a visual tile selector to a Modeler.

    """
    def __init__(self, tile_size=1):
        self.plane = Plane(Vec3(0, 0, 1), Point3(0, 0, 0))
        self.tile_size = tile_size
        self.tlims = 9

        cm = CardMaker("tile")
        cm.set_frame(Vec4(-1, 1, -1, 1) * tile_size)
        cm.set_color(Vec4(1, 1, 1, .5))
        self.tile = self.visual.attach_new_node(cm.generate())
        self.tile.look_at(Point3(0, 0, -1))
        self.tile.set_two_sided(True)
        self.tile.set_transparency(True)
        #  filters = CommonFilters(self.win, self.cam)
        #  filters.setBloom()
        #  self.tile.setShaderAuto()
        self.tile.hide()

        self.move_highlight = False

    def set_show_tile(self, show):
        if show:
            self.tile.show()
            self.task_mgr.add(self.highlight_tile, "highlight_tile")
        else:
            self.tile.hide()
            self.task_mgr.remove("highlight_tile")
        self.move_highlight = show

    def mouse_to_ground(self, mouse_pos):
        """Get the 3D point where a mouse ray hits the ground plane. If it does
        hit the ground, a Point3; None otherwise.

        Parameters
        ----------
        mouse_pos : (2,) float sequence
          Cartesian coordinates of the mouse in screen space.

        """
        near_point = Point3()
        far_point = Point3()
        self.camLens.extrude(Point2(*mouse_pos), near_point, far_point)
        target_point = Point3()
        do_intersect = self.plane.intersects_line(
                target_point,
                self.render.get_relative_point(self.camera, near_point),
                self.render.get_relative_point(self.camera, far_point)
                )
        if do_intersect:
            return target_point
        else:
            return None

    def highlight_tile(self, task):
        if self.move_highlight and self.mouseWatcherNode.has_mouse():
            mpos = self.mouseWatcherNode.get_mouse()
            pos3d = self.mouse_to_ground(mpos)
            if pos3d is not None:
                pos3d = (np.asarray(pos3d) / self.tile_size).clip(
                        -self.tlims, self.tlims).round() * self.tile_size
                self.tile.set_pos(self.render, *pos3d)
        return task.cont


class Drawable:
    """Mixin giving to ShowBase the ability to sketch on the screen.

    """
    def __init__(self, color=(0, 0, 1, 1), thickness=2):
        self.strokes = []
        self.pencil = LineSegs("pencil")
        self.pencil.set_color(color)
        self.pencil.set_thickness(thickness)
        self.sketch_np = self.render2d.attach_new_node("sketches")
        self.tip = self.pixel2d.attach_new_node(
            make_circle("tip", thickness, resol=8)
        )
        self.tip.set_color(color)
        self.tip.hide()

    def set_draw(self, draw):
        if draw:
            if self.mouseWatcherNode.has_mouse():
                pos = self.mouseWatcherNode.get_mouse()
                # /!\ get_mouse returns a shallow copy
                self.strokes.append([list(pos)])
            self.task_mgr.add(self._update_drawing, "update_drawing")
        else:
            self.task_mgr.remove("update_drawing")

    def set_show_tip(self, show):
        if show:
            self.tip.show()
            self.task_mgr.add(self._update_tip_pos, "update_tip_pos")
        else:
            self.tip.hide()
            self.task_mgr.remove("update_tip_pos")

    def _update_drawing(self, task):
        if self.mouseWatcherNode.has_mouse():
            # /!\ get_mouse returns a shallow copy
            pos = list(self.mouseWatcherNode.get_mouse())
            stroke = self.strokes[-1]
            # Filter duplicates
            if not (len(stroke) and np.allclose(pos, stroke[-1])):
                stroke.append(pos)
            # Update the drawing
            node = self._draw_stroke(stroke)
            if self.sketch_np.get_num_children() == len(self.strokes):
                node.replace_node(self.sketch_np.get_children()[-1].node())
            else:
                self.sketch_np.attach_new_node(node)
        return task.cont

    def _update_tip_pos(self, task):
        mwn = self.mouseWatcherNode
        if mwn.has_mouse():
            mouse_pos = self.pixel2d.get_relative_point(
                self.render2d, (mwn.get_mouse_x(), 0, mwn.get_mouse_y())
            )
            self.tip.set_pos(mouse_pos)
        return task.cont

    def _draw_stroke(self, stroke):
        """Generate the GeomNode for this stroke.

        Returns
        -------
        out : GeomNode
          The node generated by LineSegs.create().

        """
        pencil = self.pencil
        pencil.move_to(stroke[0][0], 0, stroke[0][1])
        for x, y in stroke[1:]:
            pencil.draw_to(x, 0, y)
        return pencil.create()

    def clear_drawing(self):
        self.sketch_np.node().remove_all_children()
        #  self.pencil.reset()
        self.strokes = []

    def save_drawing(self, path=""):
        a = np.array(self.strokes)
        filename = path + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        np.save(filename, a)


class Pickerable:
    """Mixin giving Modeler the ability to pick objects.

    You need to set the python tag 'pickable' to True if you want a model
    to be pickable.

    Attributes
    ----------
    pick_level : int
      Which ancestor to return when calling get_hit_object().
      0 is the object itself (default), 1 is the parent, etc.

    """
    def __init__(self):
        self.pick_traverser = CollisionTraverser()
        self.pick_queue = CollisionHandlerQueue()
        self.picker_ray = CollisionRay()
        picker_node = CollisionNode('mouse_ray')
        picker_node.set_from_collide_mask(GeomNode.get_default_collide_mask())
        picker_node.add_solid(self.picker_ray)
        picker_np = self.camera.attach_new_node(picker_node)
        self.pick_traverser.add_collider(picker_np, self.pick_queue)

        self.pick_level = 0

    def get_hit_object(self):
        if self.mouseWatcherNode.has_mouse():
            pos = self.mouseWatcherNode.get_mouse()
            self.picker_ray.set_from_lens(
                self.camNode, pos.get_x(), pos.get_y()
            )
            self.pick_traverser.traverse(self.models)
            pick_queue = self.pick_queue
            if pick_queue.get_num_entries() > 0:
                pick_queue.sort_entries()
                picked_obj = pick_queue.get_entry(0).get_into_node_path()
                picked_obj = picked_obj.find_net_python_tag('pickable')
                # False and None are equivalent here
                if picked_obj.get_python_tag('pickable'):
                    return picked_obj.get_ancestor(self.pick_level)
        return None


class Animable:
    """Give modeler the ability to play a sequence of frames.

    The input frame rate is automatically remapped to the current video frame
    rate.

    """
    def __init__(self):
        self._frames = None
        self._remapping_factor = 1
        self._frame_start = 0
        self._frame_end = 0

        self.play = False
        self.current_frame = 0
        self._play_controls = None

    def go_to_frame(self, fi):
        # Clip fi
        fs = self._frame_start
        fe = self._frame_end
        fi = fs if fi < fs else fe if fi > fe else fi
        self.current_frame = fi
        # Update transforms
        fi_original = self.remap_frame(fi)
        for nopa, frame in self._frames[fi_original]:
            if nopa.has_tag('save_scale'):
                nopa.set_scale(Vec3(*frame[-3:]))
            nopa.set_pos(Point3(*frame[:3]))
            nopa.set_quat(Quat(*frame[3:7]))

    def go_to_next_frame(self):
        self.go_to_frame(self.current_frame + 1)

    def go_to_previous_frame(self):
        self.go_to_frame(self.current_frame - 1)

    def load_frames(self, objects_frames, fps):
        # Total length is the highest time found in the list of states of
        # each object.
        length = max(o_frames[-1][0] for o_frames in objects_frames.values())
        n_frames = int(length * fps) + 1
        # Instead of having objects mapped to a sequence of states, make a list
        # mapping fi to (object, state) at fi.
        fi2object_state = [[] for _ in range(n_frames)]
        name2path = {}
        for o_name, o_frames in objects_frames.items():
            try:
                nopa = name2path[o_name]
            except KeyError:
                nopa = self.models.find("**/{}".format(o_name))
                name2path[o_name] = nopa
            for frame in o_frames:
                t = frame[0]
                fi = int(t * fps)
                fi2object_state[fi].append((nopa, frame[1:]))
        self._frames = fi2object_state
        self._remapping_factor = fps / self.video_frame_rate
        self._frame_start = 0
        self._frame_end = int((n_frames - 1) / self._remapping_factor)
        self.current_frame = 0

    def make_player_controls(self):
        if self._play_controls is not None:
            self._play_controls.destroy()
            self._play_controls.remove_node()
        self._play_controls = PlayerControls(
            frameSize=(-.45, .45, -.06, .06),
            frameColor=Vec4(.2, .2, .2, 1),
            # Labels
            label_text_fg=Vec4(1, 1),
            # Buttons
            button_frameColor=Vec4(.25, .25, .25, 1),
            button_text_fg=Vec4(1, 1),
            # Position
            parent=self.a2dBottomCenter,
            pos=Point3(0, 0, .25*9/16),
            # Specific
            command=self.update_control,
            currentFrame=self.current_frame+1,
            numFrames=self._frame_end+1,
            shadowSize=.2,
        )

    def remap_frame(self, fi):
        return int(fi * self._remapping_factor)

    def reset_frame(self):
        self.go_to_frame(0)

    def toggle_play(self):
        self.play = not self.play

    def update_frame(self, task):
        if self.play:
            fi = (self.current_frame + 1) % (self._frame_end + 1)
            self.go_to_frame(fi)
            self._play_controls.updateCurrentFrame(self.current_frame + 1)
        return task.cont

    def update_control(self, *args):
        if self._play_controls is None:
            return
        name = args[-1]
        control = self._play_controls.component(name)
        if name == "timelineSlider":
            self.go_to_frame(round(control['value']) - 1)
        if name == "startButton":
            self.reset_frame()
        if name == "prevButton":
            self.go_to_previous_frame()
        if name == "ppButton":
            self.toggle_play()
            self._play_controls.togglePlayPause(self.play)
        if name == "nextButton":
            self.go_to_next_frame()
        if name == "endButton":
            self.go_to_frame(self._frame_end)
        self._play_controls.updateCurrentFrame(self.current_frame + 1)


class WithViewHelpers:
    """Mixin providing useful screen-space-to-3D-space geometric functions.

    """
    def compute_view_orthogonal_plane(self, obj):
        # Get the vector going through the center of the lens...
        axis = Vec3()
        self.camLens.extrude_vec(0, axis)
        # ... in the frame of the 3d objects
        axis = self.models.get_relative_vector(self.camera, axis)
        return Plane(axis, obj.get_pos())

    def project_mouse_onto_plane(self, plane):
        mwn = self.mouseWatcherNode
        if mwn.has_mouse():
            return self._project_mouse_pos_onto_plane(mwn.get_mouse(), plane)

    def _project_mouse_pos_onto_plane(self, mouse_pos, plane):
        near = Point3()
        far = Point3()
        self.camLens.extrude(mouse_pos, near, far)
        ref = self.models
        near = ref.get_relative_point(self.camera, near)
        far = ref.get_relative_point(self.camera, far)
        target = Point3()
        do_intersect = plane.intersects_line(target, near, far)
        return target if do_intersect else None
