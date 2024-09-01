import math

from .. import ActiveCA
from ..ca_system import ActiveCAPredict
from ..utils import get_variables_from_constraints


def obj_max_viol(B, **kwargs):
    """
    Objective function to maximize the number of violated constraints.

    :param B: A list of constraints.
    :return: The sum of violated constraints.
    """
    return sum([~c for c in B])


def obj_min_viol(B, **kwargs):
    """
    Objective function to minimize the number of violated constraints.

    :param B: A list of constraints.
    :return: The sum of satisfied constraints.
    """
    return sum([c for c in B])


def obj_proba(B, ca_system: ActiveCA, **kwargs):
    """
    Probability-based objective function.

    :param B: A list of constraints.
    :param ca_system: An instance of CASystem.
    :return: The probability-based objective function.
    :raises Exception: If ca_system is not an instance of CASystemPredict.
    """
    if not isinstance(ca_system, ActiveCAPredict):
        raise Exception('Probability based objective can only be used with CASystemPredict')

    proba = {c: ca_system.bias_proba[c] for c in B}
    Y = get_variables_from_constraints(B)

    O_c = [((1 / proba[c]) <= math.log2(len(Y))) for c in B]
    objective = sum(
        [~c * (1 - len(ca_system.instance.language) * o_c) for
         c, o_c in zip(B, O_c)])

    return objective
