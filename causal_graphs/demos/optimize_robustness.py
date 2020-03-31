import os
import sys
import tempfile

import numpy as np
from joblib import Memory
from panda3d.core import load_prc_file_data

sys.path.insert(0, os.path.abspath(".."))
import core.robustness as rob  # noqa: E402
from core.optimize import maximize_robustness_local  # noqa: E402
from core.scenario import (StateObserver, import_scenario_data,  # noqa: E402
                           load_scenario, simulate_scene)
from gui.viewers import Replayer, ScenarioViewer  # noqa: E402

memory = Memory(cachedir=".cache", verbose=0)


@memory.cache
def initialize(scenario_data, n_succ=100, n_0=50, n_k=10,
               ret_events_labels=False, **simu_kw):
    scenario = load_scenario(scenario_data)
    return rob.find_successful_samples_adaptive(
        scenario, n_succ=n_succ, n_0=n_0, n_k=n_k, k_max=500, sigma=.01,
        ret_events_labels=ret_events_labels, **simu_kw
    )


@memory.cache
def compute_rob(scenario_data, init_samples, init_labels, n_k, k_max,
                dims=None, event=None, **simu_kw):
    scenario = load_scenario(scenario_data)
    print("Number of dimensions:", len(scenario.design_space))
    return rob.train_and_consolidate_boundary2(
        scenario, init_samples, init_labels, accuracy=.9, n_k=n_k, k_max=k_max,
        dims=dims, event=event, **simu_kw
    )


@memory.cache
def compute_factorized_rob(scenario_data, init_samples, init_events_labels,
                           invar_success_rate, select_coeff, n_k, k_max,
                           **simu_kw):
    assignments = rob.map_events_to_dimensions(
        init_samples, init_events_labels, invar_success_rate, select_coeff
    )
    return [compute_rob(scenario_data, init_samples, init_events_labels[event],
                        n_k, k_max, dims, event, **simu_kw)
            for event, dims in assignments.items() if len(dims)]


def optimize_rob(scenario_data, estimators, x0, smin_coeff):
    scenario = load_scenario(scenario_data)
    res = maximize_robustness_local(scenario, estimators, x0, smin_coeff)
    return res.x


def main():
    if len(sys.argv) < 2:
        return
    path = sys.argv[1]
    scenario_data = import_scenario_data(path)
    if scenario_data is None:
        return
    np.random.seed(111)
    duration = 8
    timestep = 1 / 500

    if 0:
        # Initial exploration
        n_succ = 100
        n_0 = 1000
        n_k = 10
        init_samples, init_labels = initialize(
            scenario_data, n_succ, n_0, n_k,
            duration=duration, timestep=timestep
        )

        # Training and boundary consolidation
        n_k = 10
        k_max = 5
        estimator = compute_rob(
            scenario_data, init_samples, init_labels, n_k, k_max,
            duration=duration, timestep=timestep
        )
        estimators = [estimator]
    else:
        # Initial exploration
        n_succ = 100
        n_0 = 1000
        n_k = 10
        init_samples, init_labels, init_events_labels = initialize(
            scenario_data, n_succ, n_0, n_k, ret_events_labels=True,
            duration=duration, timestep=timestep
        )

        # Factorized training and boundary consolidation
        n_k = 10
        k_max = 5
        estimators = compute_factorized_rob(
            scenario_data, init_samples, init_events_labels,
            invar_success_rate=.95, select_coeff=.2, n_k=n_k, k_max=k_max,
            duration=duration, timestep=timestep
        )

    # Optimization
    init_probas = np.prod([e.predict_proba(init_samples)[:, 1]
                           for e in estimators], axis=0)
    x_init = init_samples[np.argmax(init_probas)]
    smin_coeff = 1
    x_best = optimize_rob(scenario_data, estimators, x_init, smin_coeff)
    # x_best = x_init

    scenario = load_scenario(scenario_data)
    if 1:
        # Print the solution.
        instance = scenario.instantiate_from_sample(
            x_best, geom='HD', phys=True
        )
        instance.scene.export_layout_to_pdf(
            "opt_xz", (21, 29.7), plane='xz',
            # exclude="board_geom",
        )
    if 0:
        # Show the solution.
        load_prc_file_data("", "win-origin 500 200")
        instance = scenario.instantiate_from_sample(
            x_best, geom='LD', phys=True
        )
        app = ScenarioViewer(instance)
        app.run()
    if 1:
        dir_ = tempfile.mkdtemp()
        # Run the instance.
        instance = scenario.instantiate_from_sample(
            x_best, geom='HD', phys=False
        )
        scene_path = os.path.join(dir_, "scene")
        instance.scene.export_scene_to_egg(scene_path)
        instance = scenario.instantiate_from_sample(
            x_best, geom='HD', phys=True
        )
        obs = StateObserver(instance.scene)
        simu_path = os.path.join(dir_, "simu.pkl")
        simulate_scene(instance.scene, duration=duration, timestep=timestep,
                       callbacks=[obs])
        obs.export(simu_path, fps=int(1/timestep))
        # Show the simulation.
        load_prc_file_data("", "win-origin 500 200")
        app = Replayer(scene_path+".bam", simu_path)
        app.run()
    if 0:
        instance = scenario.instantiate_from_sample(
            x_best, geom='HD', phys=True
        )
        instance.scene.export_scene_to_egg("scene.egg")
        obs = StateObserver(instance.scene)
        simulate_scene(instance.scene, duration=duration, timestep=timestep,
                       callbacks=[obs])
        obs.export("simu.pkl", fps=int(1/timestep))


if __name__ == "__main__":
    main()
