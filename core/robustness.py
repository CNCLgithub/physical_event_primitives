import numpy as np
import sobol_seq
from joblib import delayed, Parallel
from sklearn.feature_selection import mutual_info_classif
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler
from sklearn.svm import SVC
from tqdm import tqdm

from . import config as cfg


class MultivariateUniform:
    def __init__(self, ndims, a=0., b=1.):
        self.ndims = ndims
        self.a = a
        self.b = b

    def sample(self, n):
        return (self.b - self.a) * np.random.sample((n, self.ndims)) + self.a


class MultivariateMixtureOfGaussians:
    def __init__(self, mixture_params, weights=None, a=0., b=1.):
        self.mixture_params = mixture_params
        self.weights = weights
        self.a = a
        self.b = b

    def sample(self, n):
        mps = self.mixture_params
        choice = np.random.choice(len(mps), size=n, replace=True,
                                  p=self.weights)
        normal = np.random.multivariate_normal
        X = np.array([normal(mps[i][0], mps[i][1]) for i in choice])
        return np.clip(X, self.a, self.b)


class SobolSequence:
    def __init__(self, ndims, a=0., b=1.):
        self.ndims = ndims
        self.a = a
        self.b = b

    def sample(self, n):
        X = sobol_seq.i4_sobol_generate(self.ndims, n)
        return (self.b - self.a) * X + self.a


def find_physically_valid_samples(scenario, distribution, n_valid, max_trials):
    """Find physically valid samples for this scenario.

    Parameters
    ----------
    scenario : scenario.Scenario
      Abstract scenario.
    distribution : {MultivariateUniform, MultivariateMixtureOfGaussians}
      Instance of the distribution to use for sampling.
    n_valid : int
      Number of expected valid samples.
    max_trials : int
      Maximum number of samples to try.

    Returns
    -------
    samples : sequence
      Physically valid samples. Size = (n,ndims), with n <= n_valid.

    """
    cand_samples = distribution.sample(max_trials)
    samples = []
    for sample in cand_samples:
        if scenario.check_physically_valid_sample(sample):
            samples.append(sample)
            if len(samples) == n_valid:
                break
    else:
        print("Attempt to find valid samples ran out of trials")
    return samples


def compute_label(scenario, sample, ret_events_labels=False, **simu_kw):
    instance = scenario.instantiate_from_sample(sample, geom=None, phys=True,
                                                verbose_causal_graph=False)
    global_label = instance.simulate(**simu_kw)
    if ret_events_labels:
        events_labels = {
            e.name: (True if e.success else False if e.failure else None)
            for e in instance.embedded_causal_graph.get_events()
        }
        return global_label, events_labels
    else:
        return global_label


def find_successful_samples_uniform(scenario, n_succ, n_0, n_k, k_max,
                                    totals=None, **simu_kw):
    ndims = len(scenario.design_space)
    # Initialization
    samples = find_physically_valid_samples(
        scenario, MultivariateUniform(ndims), n_0, 100*n_0
    )
    labels = [compute_label(scenario, s, **simu_kw) for s in samples]
    # Main loop
    k = 0
    while k < k_max:
        total = sum(labels)
        print("Number of successful samples at step {}: {}".format(k, total))
        if totals is not None:
            totals.append(total)
        if total >= n_succ:
            break
        k += 1
        samples_k = find_physically_valid_samples(
            scenario, MultivariateUniform(ndims), n_k, 100*n_k
        )
        samples.extend(samples_k)
        labels.extend(compute_label(scenario, s, **simu_kw) for s in samples_k)
    return samples, labels


def find_successful_samples_adaptive(scenario, n_succ, n_0, n_k, k_max, sigma,
                                     ret_events_labels=False, totals=None,
                                     verbose=True, **simu_kw):
    """Sample the design space until enough successful samples are found.

    Returns
    -------
    (n,n_dims) sequence
      All physically valid samples accumulated during the process.
    (n,) sequence
      Success label for each sample (True = success, False = failure).
    dict [only if ret_events_labels]
      Dictionary of event:labels pairs where labels is a (n,)-list of elements
      in {True, False, None}, corresponding to the success of the event for
      each sample.

    """
    ndims = len(scenario.design_space)
    cov = sigma * np.eye(ndims)
    # Initialization
    samples = find_physically_valid_samples(
        scenario, SobolSequence(ndims), n_0, 100*n_0
    )
    # res = [compute_label(scenario, s, True, **simu_kw) for s in samples]
    res = Parallel(n_jobs=cfg.NCORES)(
        delayed(compute_label)(scenario, s, True, **simu_kw)
        for s in tqdm(samples)
    )
    nse = [sum(filter(None, el.values())) for _, el in res]
    labels = [label for label, _ in res]
    if ret_events_labels:
        events_labels = [el for _, el in res]
    # Main loop
    k = 0
    while k < k_max:
        total = sum(labels)
        if verbose:
            print("Number of successes at step {}: {}".format(k, total))
        if totals is not None:
            totals.append(total)
        if total >= n_succ:
            break
        k += 1
        # Select the top n_succ samples (or n_samples, whichever is smaller).
        n_top = min(n_succ, len(samples))
        top_ind = np.argpartition(-np.array(nse), n_top-1)[:n_top]
        top_samples = [samples[i] for i in top_ind]
        top_nse = [nse[i] for i in top_ind]
        # Compute their PMF.
        weights = np.array(top_nse, dtype=np.float64)
        weights /= weights.sum()
        # Generate the new samples.
        mixture_params = [(ts, cov) for ts in top_samples]
        dist = MultivariateMixtureOfGaussians(mixture_params, weights)
        samples_k = find_physically_valid_samples(scenario, dist, n_k, 100*n_k)
        samples.extend(samples_k)
        # res_k = [compute_label(scenario, s, True, **simu_kw)
        #          for s in samples_k]
        res_k = Parallel(n_jobs=cfg.NCORES)(
            delayed(compute_label)(scenario, s, True, **simu_kw)
            for s in tqdm(samples_k)
        )
        nse.extend(sum(filter(None, el.values())) for _, el in res_k)
        labels.extend(label for label, _ in res_k)
        if ret_events_labels:
            events_labels.extend(el for _, el in res_k)
    if ret_events_labels:
        events_labels_dict = {name: [el[name] for el in events_labels]
                              for name in events_labels[0].keys()}
        return samples, labels, events_labels_dict
    else:
        return samples, labels


def train_svc(samples, labels, probability=False, dims=None,
              ret_xval_score=False, random_state=None, verbose=True):
    if verbose:
        print("Number of samples:", len(samples))
        print("Number of features:",
              len(dims) if dims is not None else len(samples[0]))
    # Create pipeline.
    steps = [
        StandardScaler(),
        SVC(kernel='rbf', probability=probability, random_state=random_state,
            cache_size=512),
    ]
    if dims is not None:
        selector = FunctionTransformer(np.take, validate=True,
                                       kw_args=dict(indices=dims, axis=1))
        steps.insert(0, selector)
    pipeline = make_pipeline(*steps)
    # Initialize cross-validation.
    C_range = np.logspace(*cfg.SVC_C_RANGE)
    gamma_range = np.logspace(*cfg.SVC_GAMMA_RANGE)
    class_weight_options = [None, 'balanced']
    param_grid = {
        'svc__gamma': gamma_range,
        'svc__C': C_range,
        'svc__class_weight': class_weight_options
    }
    grid = GridSearchCV(pipeline, param_grid=param_grid, cv=3,
                        n_jobs=cfg.NCORES, iid=False)
    # Run cross-validation.
    grid.fit(samples, labels)
    if verbose:
        print("The best parameters are {}".format(grid.best_params_))
        print("Score on the training set: {}".format(grid.best_score_))
    if ret_xval_score:
        return grid.best_estimator_, grid.best_score_
    else:
        return grid.best_estimator_


def learn_active(scenario, init_samples, init_labels, sampler, accuracy=.9,
                 n_k=10, k_max=10, dims=None, event=None, step_data=None,
                 **simu_kw):
    """
    Run the active learning routine.

    Returns
    -------
    estimator : sklearn.pipeline.Pipeline
      Trained estimator.

    """
    msg = "Running the active learning routine"
    if event is not None:
        msg += " for event {}".format(event)
    if dims is not None:
        msg += " with features {}".format(dims)
    print(msg)
    # Initialization: collect valid samples.
    valid = [i for i, l in enumerate(init_labels) if l is not None]
    X = [init_samples[i] for i in valid]
    y = [init_labels[i] for i in valid]
    # Train the SVC.
    print("Training the estimator")
    estimator, score = train_svc(X, y, dims=dims, ret_xval_score=True)
    if step_data is not None:
        step_data.append((np.copy(X), np.copy(y), estimator, score))
    k = 0
    # Main loop
    while k < k_max and score < accuracy:
        # Query synthesis: determine new samples.
        print("Generating new samples")
        D = sampler(X, y, estimator, dims)
        if D is None:
            break
        cand = find_physically_valid_samples(scenario, D, 10*n_k, 1000*n_k)
        cand = np.asarray(cand)
        margin = np.abs(estimator.decision_function(cand))
        X_k = cand[np.argpartition(margin, n_k)[:n_k]]  # n_k smallest margins
        # Query the new samples and add them to the training set.
        if event is None:
            X.extend(X_k)
            y.extend(compute_label(scenario, x, **simu_kw) for x in X_k)
        else:
            y_k = [compute_label(scenario, x, True, **simu_kw)[1][event]
                   for x in X_k]
            valid = [i for i, l in enumerate(y_k) if l is not None]
            X.extend(X_k[i] for i in valid)
            y.extend(y_k[i] for i in valid)
        # Train the SVC.
        print("Training the estimator")
        estimator, score = train_svc(X, y, dims=dims, ret_xval_score=True)
        if step_data is not None:
            step_data.append((np.copy(X), np.copy(y), estimator, score))
        k += 1
    # Calibrate
    print("Calibrating the classifier")
    estimator = train_svc(X, y, probability=True, dims=dims, verbose=False)
    return estimator


def _get_uniform_distrib(X, y, estimator, dims=None):
    if dims is not None:
        random_success = X[np.random.choice(np.flatnonzero(y))]
        a = random_success.copy()
        b = a.copy()
        a[dims] = 0
        b[dims] = 1
        return MultivariateUniform(X.shape[1], a, b)
    else:
        return MultivariateUniform(X.shape[1])


def train_and_add_uniform_samples(scenario, init_samples, init_labels,
                                  accuracy=.9, n_k=10, k_max=10, dims=None,
                                  event=None, step_data=None, **simu_kw):
    """
    Train the SVC and add more uniform samples until accuracy is reached.

    Returns
    -------
    estimator : sklearn.pipeline.Pipeline
      Trained estimator.

    """
    return learn_active(
        scenario, init_samples, init_labels, _get_uniform_distrib,
        accuracy, n_k, k_max, dims, event,
        step_data, **simu_kw
    )


def _get_misclassified_distrib(X, y, estimator, dims=None):
    is_wrong = estimator.predict(X) != y
    if not is_wrong.any():
        return None
    wrong_X = X[is_wrong]
    wrong_af = np.abs(estimator.decision_function(wrong_X))
    # Compute weights.
    weights = wrong_af / wrong_af.sum()
    # Generate samples.
    diag = 1 / estimator.named_steps['standardscaler'].scale_
    if dims is not None:
        # Restore the full-sized diagonal (where non-free dims are 0)
        fulldiag = np.zeros(X.shape[1])
        fulldiag[dims] = diag
        diag = fulldiag
    scale = np.diagflat(diag)
    mixture_params = [(xi, afi*scale)
                      for xi, afi in zip(wrong_X, wrong_af)]
    return MultivariateMixtureOfGaussians(mixture_params, weights)


def train_and_consolidate_boundary(scenario, init_samples, init_labels,
                                   accuracy=.9, n_k=10, k_max=10, dims=None,
                                   event=None, step_data=None, **simu_kw):
    """
    Train the SVC and consolidate the boundary around its misclassified samples
    until accuracy is reached.

    Returns
    -------
    estimator : sklearn.pipeline.Pipeline
      Trained estimator.

    """
    return learn_active(
        scenario, init_samples, init_labels, _get_misclassified_distrib,
        accuracy, n_k, k_max, dims, event,
        step_data, **simu_kw
    )


def _get_support_distrib(X, y, estimator, dims=None):
    X = np.asarray(X)
    # Retrieve the support vectors.
    support = estimator.named_steps['svc'].support_
    # Compute weights.
    af = np.abs(estimator.decision_function(X[support]))
    weights = af / af.sum()
    # Generate samples.
    diag = 1 / estimator.named_steps['standardscaler'].scale_
    if dims is not None:
        # Restore the full-sized diagonal (where non-free dims are 0)
        fulldiag = np.zeros(X.shape[1])
        fulldiag[dims] = diag
        diag = fulldiag
    scale = np.diagflat(diag)
    mixture_params = [(X[si], afi*scale)
                      for si, afi in zip(support, af)]
    return MultivariateMixtureOfGaussians(mixture_params, weights)


def train_and_consolidate_boundary2(scenario, init_samples, init_labels,
                                    accuracy=.9, n_k=10, k_max=10, dims=None,
                                    event=None, step_data=None, **simu_kw):
    """
    Train the SVC and consolidate the boundary around its support vectors until
    accuracy is reached.

    Returns
    -------
    estimator : sklearn.pipeline.Pipeline
      Trained estimator.

    """
    return learn_active(
        scenario, init_samples, init_labels, _get_support_distrib,
        accuracy, n_k, k_max, dims, event,
        step_data, **simu_kw
    )


def map_events_to_dimensions(samples, events_labels, invar_success_rate=.95,
                             select_coeff=.1):
    """
    For each event, identify the best dimensions (i.e., columns of 'samples')
    as predictors of the event's success.

    Parameters
    ----------
    samples : (m,n) array
      Array of m samples with n dimensions.
    events_labels : dict
      Dictionary of event:labels pairs where labels is a (m,)-list of elements
      in {True, False, None}, corresponding to the success of the event for
      each sample.
    invar_success_rate : float in [0,1]
      Any event with a conditional success rate above this value is considered
      invariant (i.e., mapped to 0 dimensions).
    select_coeff : float in [0,1)
      For each event, the dimension is kept if
        score > select_coeff * max(scores).
      Low coefficients are more conservative (i.e.m more dimensions are kept).

    Returns
    -------
    dict
      Dictionary of event:dims pairs where dims is a (possibly empty) list of
      indices.

    """
    # Create initial datasets for each event.
    datasets = {}
    for event, labels in events_labels.items():
        valid = [i for i, l in enumerate(labels) if l is not None]
        event_samples = np.array([samples[i] for i in valid])
        event_labels = np.fromiter((labels[i] for i in valid), bool)
        datasets[event] = (event_samples, event_labels)
    # Filter out low variance events.
    key_events = [event for event, (_, labels) in datasets.items()
                  if labels.mean() < invar_success_rate]
    print("Key events:", key_events)
    # Determine best dimensions.
    assignments = {}
    for event in events_labels.keys():
        if event in key_events:
            # scores = f_classif(*datasets[event])[0]
            scores = mutual_info_classif(*datasets[event])
            correlated = scores > (scores.max() * select_coeff)
            assignments[event] = np.flatnonzero(correlated)
        else:
            assignments[event] = []
    return assignments
