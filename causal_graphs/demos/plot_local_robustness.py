"""
Compute the local robustness curves.

Parameters
----------
path : string
  Path to the scenario file.
n_samples : int
  Number of samples in the dataset.
T : int
  Duration of the simulation in seconds.

"""
import os
import sys

import numpy as np
from bayes_opt import BayesianOptimization, UtilityFunction
from joblib import delayed, Memory, Parallel
from prettytable import PrettyTable
# from scipy import stats
from scipy.stats import sem
from timeit import default_timer as timer
from tqdm import tqdm

sys.path.insert(0, os.path.abspath(".."))
import core.optimize as opt  # noqa: E402
import core.robustness as rob  # noqa: E402
from core.scenario import import_scenario_data, load_scenario  # noqa: E402
from core.config import NCORES  # noqa: E402

memory = Memory(cachedir=".cache", verbose=False)
# Local robustness curves parameters
N_STEPS = 30
N_LOCAL = 100
# Number of runs for each random method
N_RUNS = 10
# Simulation parameters
SIMU_KW = dict(timestep=1/500, duration=0)
SCENARIO = None
# Whether to print or plot results
PLOT_RESULTS = False


# Parallelizable
def compute_label(scenario, x):
    if scenario.check_physically_valid_sample(x):
        label = 2*int(rob.compute_label(scenario, x, **SIMU_KW)) - 1
    else:
        label = 0
    return label


@memory.cache
def generate_dataset(scenario, n_samples):
    t = timer()
    ndims = len(scenario.design_space)
    X = rob.MultivariateUniform(ndims).sample(n_samples)
    # labels = [compute_label(scenario, x) for x in X]
    y = Parallel(n_jobs=NCORES)(delayed(compute_label)(scenario, x) for x in X)
    t = timer() - t
    X = np.asarray(X)
    y = np.asarray(y)
    return X, y, t


@memory.cache
def generate_dataset2(scenario, n_samples):
    t = timer()
    n_dims = len(scenario.design_space)
    X = rob.SobolSequence(n_dims).sample(n_samples)
    # labels = [compute_label(scenario, x) for x in X]
    y = Parallel(n_jobs=NCORES)(delayed(compute_label)(scenario, x)
                                for x in tqdm(X))
    t = timer() - t
    X = np.asarray(X)
    y = np.asarray(y)
    return X, y, t


def compute_local_rob_curve(center, n_steps, n_local, dense_dataset):
    # Evaluate local neighborhood.
    eta = 1 / (10 * n_steps)
    X_loc = np.tile(center, (n_local+1, 1))
    X_loc[1:] += np.random.uniform(-eta, eta, (n_local, len(center)))
    y_loc = Parallel(n_jobs=NCORES)(
        delayed(compute_label)(SCENARIO, x) for x in tqdm(X_loc)
    )
    # Update dataset.
    X = np.vstack((dense_dataset[0], X_loc))
    y = np.concatenate((dense_dataset[1], y_loc))
    # Evaluate local robustness.
    radii = np.linspace(0, 1, n_steps)
    valid = np.flatnonzero(y)
    y = y[valid]
    d = np.linalg.norm(X[valid] - center, axis=1)
    loc_rob = np.zeros(n_steps)
    for i, r in enumerate(radii):
        y_in_ball = y[d <= (r + eta)]
        if y_in_ball.size:
            loc_rob[i] = (y_in_ball == 1).mean()
    return loc_rob


class LocalRobustnessEstimator:
    def __init__(self, radius, n_local):
        self.radius = radius
        self.n_local = n_local
        self.n_eval = 0

    def __call__(self, x):
        x = np.asarray(x)
        if not SCENARIO.check_physically_valid_sample(x):
            return 0.
        self.n_eval += 1
        radius = self.radius
        n_local = self.n_local
        dist = rob.MultivariateUniform(x.size, x-radius, x+radius)
        X = rob.find_physically_valid_samples(
            SCENARIO, dist, n_local, 100*n_local
        )
        X.append(x)
        y = Parallel(n_jobs=NCORES)(
            delayed(rob.compute_label)(SCENARIO, xi, **SIMU_KW) for xi in X
        )
        return sum(y) / len(y)

    def from_dict(self, **x_dict):
        return self(self.dict2array(x_dict))

    @staticmethod
    def dict2array(x_dict):
        x = np.empty(len(x_dict))
        for k, v in x_dict.items():
            x[int(k)] = v
        return x


@memory.cache
def find_success_uniform(simu_budget, seed=None):
    if seed is not None:
        np.random.seed(seed)
    n_dims = len(SCENARIO.design_space)
    dist = rob.MultivariateUniform(n_dims)
    X = rob.find_physically_valid_samples(
        SCENARIO, dist, simu_budget, 100*simu_budget
    )
    y = Parallel(n_jobs=NCORES)(
        delayed(rob.compute_label)(SCENARIO, xi, **SIMU_KW) for xi in X
    )
    try:
        ind = next(i for i, yi in enumerate(y) if yi == 1)
    except StopIteration:
        ind = np.random.choice(simu_budget)
    return X[ind]


@memory.cache
def find_best_uniform(rob_est, n_eval, seed=None):
    if seed is not None:
        np.random.seed(seed)
    n_dims = len(SCENARIO.design_space)
    dist = rob.MultivariateUniform(n_dims)
    X = rob.find_physically_valid_samples(
        SCENARIO, dist, n_eval, 100*n_eval
    )
    r = [rob_est(x) for x in X]
    x_best = X[np.argmax(r)]
    return x_best


@memory.cache
def find_best_gpo(rob_est, n_eval, xi=0., acq='ei', seed=None):
    if seed is not None:
        np.random.seed(seed)
    rob_est.n_eval = 0
    n_dims = len(SCENARIO.design_space)
    pbounds = {str(i): (0, 1) for i in range(n_dims)}
    optimizer = BayesianOptimization(rob_est.from_dict, pbounds, seed)
    # We compute our own initial valid points.
    n_init = n_eval // 2
    dist = rob.MultivariateUniform(n_dims)
    X_init = rob.find_physically_valid_samples(
        SCENARIO, dist, n_init, 100*n_init
    )
    for x in X_init:
        optimizer.probe({str(i): x[i] for i in range(n_dims)})
    # Run main maximization routine.
    n_iter = n_eval - n_init
    optimizer.maximize(init_points=0, n_iter=n_iter, acq=acq, xi=xi)
    # Add iterations until n_eval has effectively been spent.
    util = UtilityFunction(kind=acq, kappa=2.576, xi=xi)  # as in maximize()
    while rob_est.n_eval < n_eval:
        optimizer.probe(optimizer.suggest(util), lazy=False)
    return rob_est.dict2array(optimizer.max['params'])


@memory.cache
def find_successful_samples_adaptive(n_succ, n_0, n_k, k_max, sigma,
                                     ret_event_labels, seed=None):
    # 'seed' is just here to cache several results
    return rob.find_successful_samples_adaptive(
        SCENARIO, n_succ, n_0, n_k, k_max, sigma, ret_event_labels, **SIMU_KW
    )


@memory.cache
def learn_spd_active(X, y, accuracy, n_k, k_max, dims=None, event=None,
                     ret_simu_cost=False, seed=None):
    # 'seed' is just here to cache several results
    step_data = [] if ret_simu_cost else None
    rob_est = rob.train_and_consolidate_boundary2(
        SCENARIO, X, y, accuracy, n_k, k_max, dims, event, step_data,
        **SIMU_KW
    )
    if ret_simu_cost:
        simu_cost = len(step_data[-1][0]) - len(step_data[0][0])
        return rob_est, simu_cost
    else:
        return rob_est


@memory.cache
def find_best_ours(explo_n_0, explo_n_succ, explo_n_k,
                   learn_n_k=None, learn_k_max=None,
                   factorized=True, active=True, optimizer='local',
                   ret_simu_cost=False, seed=None):
    if seed is not None:
        np.random.seed(seed)
    if not active:
        learn_k_max = 0  # if 0, SVC will only be trained once
    if factorized:
        # Initialize
        X, y, y_e = find_successful_samples_adaptive(
            n_succ=explo_n_succ, n_0=explo_n_0, n_k=explo_n_k, k_max=500,
            sigma=.01, ret_event_labels=True, seed=seed
        )
        if ret_simu_cost:
            simu_cost = len(y)
        assignments = rob.map_events_to_dimensions(
            X, y_e, invar_success_rate=.95, select_coeff=.2
        )
        # Build the robustness estimators
        learn_output = [learn_spd_active(
            X, y_e[event], accuracy=.99, n_k=learn_n_k, k_max=learn_k_max,
            dims=dims, event=event, ret_simu_cost=ret_simu_cost
        ) for event, dims in assignments.items() if len(dims)]
        if ret_simu_cost:
            rob_estimators, learn_simu_costs = zip(*learn_output)
            simu_cost += sum(learn_simu_costs)
        else:
            rob_estimators = learn_output
    else:
        # Initialize
        X, y = find_successful_samples_adaptive(
            n_succ=explo_n_succ, n_0=explo_n_0, n_k=explo_n_k, k_max=500,
            sigma=.01, ret_event_labels=False, seed=seed
        )
        if ret_simu_cost:
            simu_cost = len(y)
        # Build the robustness estimator
        learn_output = learn_spd_active(
            X, y, accuracy=.99, n_k=learn_n_k, k_max=learn_k_max,
            ret_simu_cost=ret_simu_cost
        )
        if ret_simu_cost:
            rob_est, learn_simu_cost = learn_output
            simu_cost += learn_simu_cost
        else:
            rob_est = learn_output
        rob_estimators = [rob_est]
    # Find optimal solution
    init_probas = np.prod([e.predict_proba(X)[:, 1]
                           for e in rob_estimators], axis=0)
    if optimizer is None:
        x = X[np.argmax(init_probas)]
    elif optimizer == 'local':
        x0 = X[np.argmax(init_probas)]
        res = opt.maximize_robustness_local(SCENARIO, rob_estimators, x0)
        x = res.x
    if ret_simu_cost:
        return x, simu_cost
    else:
        return x


@memory.cache
def compute_ours(dense_dataset, n_runs, factorized=True, active=True,
                 optimizer='local', seed=None, **method_params):
    curves = []
    simu_costs = []
    for i in range(n_runs):
        x_out, simu_cost = find_best_ours(
            factorized=factorized, active=active, optimizer=optimizer,
            ret_simu_cost=True, seed=(seed if seed is None else seed+i),
            **method_params
        )
        curve = compute_local_rob_curve(x_out, N_STEPS, N_LOCAL, dense_dataset)
        curves.append(curve)
        simu_costs.append(simu_cost)
    simu_cost = sum(simu_costs) // len(simu_costs)
    return curves, simu_cost


@memory.cache
def compute_B1(dense_dataset, simu_budget, n_runs, seed=None):
    curves = []
    for i in range(n_runs):
        x_out = find_success_uniform(simu_budget,
                                     seed=(seed if seed is None else seed+i))
        curve = compute_local_rob_curve(x_out, N_STEPS, N_LOCAL, dense_dataset)
        curves.append(curve)
    return curves


@memory.cache
def compute_B2(dense_dataset, n_runs, n_eval, radius, n_local, seed=None):
    curves = []
    X, y = dense_dataset
    for i in range(n_runs):
        rob_est = LocalRobustnessEstimator(radius, n_local)
        x_out = find_best_uniform(rob_est, n_eval,
                                  seed=(seed if seed is None else seed+i))
        curve = compute_local_rob_curve(x_out, N_STEPS, N_LOCAL, dense_dataset)
        curves.append(curve)
    return curves


@memory.cache
def compute_B3(dense_dataset, n_runs, n_eval, radius, n_local, seed=None):
    curves = []
    X, y = dense_dataset
    for i in range(n_runs):
        rob_est = LocalRobustnessEstimator(radius, n_local)
        x_out = find_best_gpo(rob_est, n_eval,
                              seed=(seed if seed is None else seed+i))
        curve = compute_local_rob_curve(x_out, N_STEPS, N_LOCAL, dense_dataset)
        curves.append(curve)
    return curves


def get_metadata(fun, *args, **kwargs):
    return fun.store_backend.get_metadata(
        fun._get_output_identifiers(*args, **kwargs)
    )


def get_times_ours(dense_dataset, n_runs, factorized=True, active=True,
                   optimizer='local', seed=None, **method_params):
    times = np.zeros(n_runs)
    for i in range(n_runs):
        fun = find_best_ours
        metadata = get_metadata(
            fun,
            factorized=factorized, active=active, optimizer=optimizer,
            ret_simu_cost=True, seed=(seed if seed is None else seed+i),
            **method_params
        )
        times[i] = metadata['duration']
    return times


def get_times_B1(dense_dataset, simu_budget, n_runs, seed=None):
    times = np.zeros(n_runs)
    for i in range(n_runs):
        fun = find_success_uniform
        metadata = get_metadata(
            fun, simu_budget, seed=(seed if seed is None else seed+i)
        )
        times[i] = metadata['duration']
    return times


def get_times_B2(dense_dataset, n_runs, n_eval, radius, n_local, seed=None):
    times = np.zeros(n_runs)
    for i in range(n_runs):
        rob_est = LocalRobustnessEstimator(radius, n_local)
        rob_est.n_eval = n_eval
        fun = find_best_uniform
        metadata = get_metadata(
            fun, rob_est, n_eval, seed=(seed if seed is None else seed+i)
        )
        times[i] = metadata['duration']
    return times


def get_times_B3(dense_dataset, n_runs, n_eval, radius, n_local, seed=None):
    times = np.zeros(n_runs)
    for i in range(n_runs):
        rob_est = LocalRobustnessEstimator(radius, n_local)
        rob_est.n_eval = n_eval
        fun = find_best_gpo
        metadata = get_metadata(
            fun, rob_est, n_eval, seed=(seed if seed is None else seed+i)
        )
        times[i] = metadata['duration']
    return times


def plot_results(results):
    import matplotlib.pyplot as plt
    import seaborn
    seaborn.set()
    fig, ax = plt.subplots(figsize=(6, 2))
    x = np.linspace(0, 1, N_STEPS)
    linestyles = ('-', '--', '-.', ':')
    for (method, curves, _), ls in zip(results, linestyles):
        avg_curve = np.mean(curves, axis=0)
        ax.plot(x, avg_curve, label=method, linestyle=ls)
        sem_curve = sem(curves, axis=0)
        # Use student distribution as sample size is small.
        # low, high = stats.t.interval(.95, N_RUNS-1, avg_curve, sem_curve)
        low, high = avg_curve - sem_curve, avg_curve + sem_curve
        ax.fill_between(x, low, high, alpha=.5)
    ax.legend()
    fig.tight_layout()
    plt.show()


def print_results(results):
    results_table = PrettyTable()
    results_table.field_names = ["method", "local_rob(0)", "global_rob",
                                 "time"]
    x = np.linspace(0, 1, N_STEPS)
    for method, curves, times in results:
        local_rob = np.mean(curves, axis=0)
        global_rob = np.trapz(local_rob, x)
        time = times.mean()
        results_table.add_row([method, local_rob[0], global_rob, time])
    print(results_table)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    path = sys.argv[1]
    n_samples = int(sys.argv[2])
    SIMU_KW['duration'] = int(sys.argv[3])
    scenario_data = import_scenario_data(path)
    global SCENARIO
    SCENARIO = load_scenario(scenario_data)
    seed = int(bin(hash(SCENARIO))[:34], 2)  # seed must be 32bit int

    # Generate dataset.
    # X, y, t = generate_dataset(scenario, n_samples)
    X, y, t = generate_dataset2(SCENARIO, n_samples)
    # Print dataset statistics.
    dataset_table = PrettyTable()
    dataset_table.field_names = ["Invalid", "Successes", "Failures", "Time"]
    dataset_table.add_row([(y == 0).sum(), (y == 1).sum(), (y == -1).sum(), t])
    print(dataset_table)

    results = []  # (method, local_rob_mean, local_rob_sem)

    # ------------------------------ OUR METHOD ------------------------------
    # Compute the decay of the most robust solution of our method.
    method_params = {
        'explo_n_0': 500,
        'explo_n_succ': 100,
        'explo_n_k': 10,
        'learn_n_k': 10,
        'learn_k_max': 5,
    }
    # Full active optimized
    curves, simu_cost = compute_ours(
        (X, y), N_RUNS, factorized=False, active=True, optimizer='local',
        seed=seed, **method_params
    )
    times = get_times_ours(
        (X, y), N_RUNS, factorized=False, active=True, optimizer='local',
        seed=seed, **method_params
    )
    # results.append(("Full SPD", curves, times))
    # Factorized active not optimized
    curves, _ = compute_ours(
        (X, y), N_RUNS, factorized=True, active=True, optimizer=None,
        seed=seed, **method_params
    )
    # results.append(("Factorized SPD, no-opt", curves, times))
    # Factorized active optimized
    curves, simu_cost = compute_ours(
        (X, y), N_RUNS, factorized=True, active=True, optimizer='local',
        seed=seed, **method_params
    )
    times = get_times_ours(
        (X, y), N_RUNS, factorized=True, active=True, optimizer='local',
        seed=seed, **method_params
    )
    # results.append(("Factorized SPD", curves, times))
    results.append(("Ours", curves, times))

    # ----------------------------- BASELINES --------------------------------
    # simu_budget = 1000  # number of simus allowed for each method
    simu_budget = simu_cost
    print("Number of simulations allowed:", simu_budget)
    # Initialize options for baselines based on local robustness evaluation.
    n_dims = X.shape[1]
    radius = .1  # radius of the ball to compute local robustness
    n_local = n_dims**2  # number of simulations to compute local rob
    n_eval = simu_budget // (n_local + 1)  # number of rob eval allowed
    # B1: random uniform successes.
    curves = compute_B1((X, y), simu_budget, N_RUNS, seed=seed)
    times = get_times_B1((X, y), simu_budget, N_RUNS, seed=seed)
    results.append(("B1", curves, times))
    # B2: robustness-based uniform search.
    curves = compute_B2((X, y), N_RUNS, n_eval, radius, n_local, seed=seed)
    times = get_times_B2((X, y), N_RUNS, n_eval, radius, n_local, seed=seed)
    results.append(("B2", curves, times))
    # B3: Bayesian optimization.
    curves = compute_B3((X, y), N_RUNS, n_eval, radius, n_local, seed=seed)
    times = get_times_B3((X, y), N_RUNS, n_eval, radius, n_local, seed=seed)
    results.append(("B3", curves, times))

    if PLOT_RESULTS:
        plot_results(results)
    else:
        print_results(results)


if __name__ == "__main__":
    main()
