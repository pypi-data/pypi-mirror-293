import copy

from .mquacq2 import MQuAcq2
from .algorithm_core import AlgorithmCAInteractive
from ..ca_system.active_ca import ActiveCA


class GrowAcq(AlgorithmCAInteractive):
    """
    GrowAcq ICA algorithm from:
    Dimos Tsouros, Senne Berden, and Tias Guns. "Guided Bottom-Up Interactive Constraint Acquisition." CP, 2023
    """

    def __init__(self, ca_system: ActiveCA = None, inner_algorithm: AlgorithmCAInteractive = None):
        """
        Initialize the GrowAcq algorithm with an optional constraint acquisition system and inner algorithm.

        :param ca_system: An instance of CASystem, default is None.
        :param inner_algorithm: An instance of ICA_Algorithm to be used as the inner algorithm, default is MQuAcq2.
        """
        super().__init__(ca_system)
        self.inner_algorithm = inner_algorithm if inner_algorithm is not None else MQuAcq2(ca_system)

    def _learn(self):
        """
        Learn constraints by incrementally adding variables and using the inner algorithm to learn constraints
        for each added variable.
        """
        sub_ca = copy.copy(self.ca)
        sub_ca.algorithm = self.inner_algorithm

        self.ca.instance.X = []

        for x in self.ca.instance.variables.flatten():

            if self.ca.verbose > 0:
                print(f"\nAdding variable {x} in GrowAcq")
                print("size of B in growacq: ", len(self.ca.instance.bias))

            self.ca.instance.X.append(x)
            self.ca.instance.construct_bias_for_var(x)

            sub_ca.learn()

            if self.ca.verbose > 0:
                print("C_L: ", len(self.ca.instance.cl))
                print("B: ", len(self.ca.instance.bias))
                print("Number of queries: ", self.ca.metrics.membership_queries_count)
                print("Top level Queries: ", self.ca.metrics.top_lvl_queries)
                print("FindScope Queries: ", self.ca.metrics.findscope_queries)
                print("FindC Queries: ", self.ca.metrics.findc_queries)

        if self.ca.verbose > 0:
            print("Converged ------------------------------------")
            print("Number of queries: ", self.ca.metrics.membership_queries_count)
            print("Number of recommendation queries: ", self.ca.metrics.recommendation_queries_count)
            print("Number of generalization queries: ", self.ca.metrics.generalization_queries_count)
            print("Top level Queries: ", self.ca.metrics.top_lvl_queries)
            print("FindScope Queries: ", self.ca.metrics.findscope_queries)
            print("FindC Queries: ", self.ca.metrics.findc_queries)
        self.ca.metrics.finalize_results()
        