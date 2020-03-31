import cma
import numpy as np
import scipy.optimize as opt

# from .config import NCORES
from .robustness import compute_label


class RobustnessEnergy:
    def __init__(self, estimators, smin_coeff=1):
        self.estimators = estimators
        self.smin_coeff = smin_coeff

    def __call__(self, x):
        x = x.reshape(1, -1)
        r = np.array([e.predict_proba(x)[0, 1] for e in self.estimators])
        exp = np.exp(-self.smin_coeff * r)
        return -r.dot(exp) / exp.sum()


class CombinedEnergy:
    def __init__(self, estimators, scenario, smin_coeff=1, **simu_kw):
        self.robustness = RobustnessEnergy(estimators, smin_coeff)
        self.phys_cs = PhysicalValidityConstraint(scenario)
        self.succ_cs = SuccessConstraint(scenario, **simu_kw)

    def __call__(self, x):
        phys = self.phys_cs(x)
        if phys < 0:
            return 100 * -phys
        elif self.succ_cs(x) < 0:
            return 100
        else:
            return self.robustness(x)


class PhysicalValidityConstraint:
    def __init__(self, scenario):
        self.scenario = scenario

    def __call__(self, x):
        C = self.scenario.instantiate_from_sample(
            x, geom=None, phys=True, verbose_causal_graph=False
        ).scene.get_physical_validity_constraint()
        return min(C, 0.)


class PhysicalValidityConstraintBoolean:
    def __init__(self, scenario):
        self.scenario = scenario

    def __call__(self, x, *args, **kwargs):
        return self.scenario.check_physically_valid_sample(x)


class SuccessConstraint:
    def __init__(self, scenario, **simu_kw):
        self.scenario = scenario
        self.simu_kw = simu_kw

    def __call__(self, x):
        if self.scenario.check_physically_valid_sample(x):
            # _, labels = compute_label(
            #     self.scenario, x, ret_events_labels=True, **self.simu_kw
            # )
            # return sum(filter(None, labels.values())) / len(labels) - 1.
            return compute_label(self.scenario, x, **self.simu_kw) - 1.
        else:
            return 0.


def maximize_robustness_local(scenario, estimators, x0, smin_coeff=1):
    energy = RobustnessEnergy(estimators, smin_coeff)
    phys_cs = dict(type='ineq', fun=PhysicalValidityConstraint(scenario))
    ndims = len(scenario.design_space)
    bounds = [(0, 1)] * ndims
    res = opt.minimize(energy, x0, method='SLSQP',
                       bounds=bounds, constraints=(phys_cs,),
                       options=dict(disp=True))
    return res


# def maximize_robustness_global(scenario, estimators, init, smin_coeff=1,
#                                **simu_kw):
#     energy = CombinedEnergy(estimators, scenario, smin_coeff, **simu_kw)
#     ndims = len(scenario.design_space)
#     bounds = [(0, 1)] * ndims
#     res = opt.differential_evolution(energy, bounds, init=init, maxiter=10,
#                                      disp=True, polish=False, workers=NCORES)
#     return res


def maximize_robustness_global(scenario, estimators, x0, smin_coeff=1,
                               fevals=np.inf, **simu_kw):
    energy = CombinedEnergy(estimators, scenario, smin_coeff, **simu_kw)
    # energy = RobustnessEnergy(estimators, smin_coeff)
    phys_cs = PhysicalValidityConstraintBoolean(scenario)
    options = {'bounds': [0, 1], 'is_feasible': phys_cs, 'maxfevals': fevals}
    sigma0 = .25
    res = cma.fmin(energy, x0, sigma0, options=options)
    return res
