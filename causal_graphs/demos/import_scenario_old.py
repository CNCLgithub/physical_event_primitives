"""
Import, simulate and visualize a scenario instance defined as a data file.

Parameters
----------
path : string
  Path to the data file.
interactive : {0,1}, optional
  Wether to run the simulation in real-time, or offline (and replay it).

"""
import os
import sys
import tempfile

from panda3d.core import load_prc_file_data

#sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath("."))
from core.scenario import (StateObserver, import_scenario_data,  # noqa: E402
                           load_scenario_instance, load_scene)
from gui.viewers import PhysicsViewer, ScenarioViewer, Replayer  # noqa: E402

FPS = 500
DURATION = 4


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    path = sys.argv[1]
    if len(sys.argv) > 2:
        interactive = bool(int(sys.argv[2]))
    else:
        interactive = False

    print(interactive)
    scenario_data = import_scenario_data(path)
    scene_data = scenario_data['scene']
    load_prc_file_data("", "win-origin 500 200")
    if interactive:
        if scenario_data['causal_graph']:
            instance = load_scenario_instance(scenario_data,
                                              geom='LD', phys=True)
            print("Physically valid:", instance.scene.check_physically_valid())
            app = ScenarioViewer(instance)
        else:
            scene = load_scene(scene_data, geom='LD', phys=True)
            app = PhysicsViewer(world=scene.world)
            scene.graph.reparent_to(app.models)
    else:
        dir_ = tempfile.mkdtemp()
        # Create the scene geometry.
        scene = load_scene(scene_data, geom='HD', phys=False)
        # scene_path = os.path.join(dir_, "scene")
        scene_path = input()
        scene.export_scene_to_egg(scene_path)
        # Run the instance.
        instance = load_scenario_instance(scenario_data, geom='HD', phys=True)
        obs = StateObserver(instance.scene)
        print("Physically valid:", instance.scene.check_physically_valid())
        instance.simulate(duration=DURATION, timestep=1/FPS, callbacks=[obs])
        # simu_path = os.path.join(dir_, "simu.pkl")
        simu_path = scene_path + ".pkl"
        obs.export(simu_path, fps=FPS)
        # Show the simulation.
    #     app = Replayer(scene_path+".bam", simu_path)
    # app.cam_distance = 1
    # app.min_cam_distance = .01
    # app.camLens.set_near(.01)
    # app.zoom_speed = .01
    # app.run()


if __name__ == "__main__":
    main()
