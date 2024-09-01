import time

from .algorithm_core import AlgorithmCAInteractive
from ..utils import get_kappa
from ..ca_system.active_ca import ActiveCA


class MQuAcq(AlgorithmCAInteractive):
    """
    MQuAcq is an implementation of the ICA_Algorithm that uses a modified QuAcq algorithm to learn constraints.
    """

    def __init__(self, ca_system: ActiveCA = None):
        """
        Initialize the MQuAcq algorithm with an optional constraint acquisition system.

        :param ca_system: An instance of CASystem, default is None.
        """
        super().__init__(ca_system)

    def _learn(self):
        """
        Learn constraints using the modified QuAcq algorithm by generating queries and analyzing the results.
        """
        if len(self.ca.instance.bias) == 0:
            self.ca.instance.construct_bias()

        while True:
            if self.ca.verbose > 0:
                print("Size of CL: ", len(self.ca.instance.cl))
                print("Size of B: ", len(self.ca.instance.bias))
                print("Number of queries: ", self.ca.metrics.total_queries)
                print("MQuAcq-2 Queries: ", self.ca.metrics.top_lvl_queries)
                print("FindScope Queries: ", self.ca.metrics.findscope_queries)
                print("FindC Queries: ", self.ca.metrics.findc_queries)

            # generate e in D^X accepted by C_l and rejected by B
            gen_start = time.time()
            Y = self.ca.run_query_generation()
            gen_end = time.time()

            if len(Y) == 0:
                # if no query can be generated it means we have (prematurely) converged to the target network -----
                self.ca.metrics.finalize_results()
                return self.ca.instance.cl

            self.ca.metrics.increase_generation_time(gen_end - gen_start)
            self.ca.metrics.increase_generated_queries()
            self.find_all_cons(list(Y), set())

    def find_all_cons(self, Y, Scopes):
        """
        Recursively find all constraints that can be learned from the given query.

        :param Y: The query to be analyzed.
        :param Scopes: The set of scopes to be considered.
        :return: The set of learned scopes.
        """
        kappa = get_kappa(self.ca.instance.bias, Y)
        if len(kappa) == 0:
            return set()

        NScopes = set()

        if len(Scopes) > 0:
            s = Scopes.pop()
            for x in s:
                Y2 = set(Y.copy())
                if x in Y2:
                    Y2.remove(x)

                scopes = self.find_all_cons(list(Y2), NScopes.union(Scopes))
                NScopes = NScopes.union(scopes)

        else:
            self.ca.metrics.increase_top_queries()
            if self.ca.ask_membership_query(Y):
                self.ca.remove_from_bias(kappa)
            else:
                scope = self.ca.run_find_scope(Y)
                c = self.ca.run_findc(scope)
                self.ca.add_to_cl(c)

                NScopes.add(frozenset(scope))

                NScopes = NScopes.union(self.find_all_cons(Y, NScopes.copy()))

        return NScopes
