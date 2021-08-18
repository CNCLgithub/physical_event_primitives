import os
import sys

sys.path.insert(0, os.path.abspath(".."))
from core.robustness import (find_physically_valid_samples,  # noqa: E402
                             MultivariateUniform)
from core.scenario import import_scenario_data, load_scenario  # noqa: E402
from gui.viewers import PhysicsViewer  # noqa: E402


def main():
    if len(sys.argv) < 2:
        return
    path = sys.argv[1]
    scenario_data = import_scenario_data(path)
    if scenario_data is None:
        return
    scenario = load_scenario(scenario_data)
    ndims = len(scenario.design_space)
    print("Number of dimensions:", ndims)
    sample = find_physically_valid_samples(
        scenario, MultivariateUniform(ndims), 1, 1000
    )[0]
    instance = scenario.instantiate_from_sample(sample, geom='LD', phys=True)
    print(instance.scene.get_physical_validity_constraint())
    app = PhysicsViewer(world=instance.scene.world)
    instance.scene.graph.reparent_to(app.models)
    app.run()


if __name__ == "__main__":
    main()
