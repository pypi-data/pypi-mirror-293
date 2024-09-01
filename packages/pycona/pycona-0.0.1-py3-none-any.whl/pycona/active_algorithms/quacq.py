import time

from .algorithm_core import AlgorithmCAInteractive
from ..ca_system.active_ca import ActiveCA
from ..utils import get_kappa


class QuAcq(AlgorithmCAInteractive):
    """
    QuAcq is an implementation of the ICA_Algorithm that uses the QuAcq algorithm to learn constraints.
    """

    def __init__(self, ca_system: ActiveCA = None):
        """
        Initialize the QuAcq algorithm with an optional constraint acquisition system.

        :param ca_system: An instance of CASystem, default is None.
        """
        super().__init__(ca_system)

    def _learn(self):
        """
        Learn constraints using the QuAcq algorithm by generating queries and analyzing the results.
        """
        if len(self.ca.instance.bias) == 0:
            self.ca.instance.construct_bias()

        while True:
            if self.ca.verbose > 0:
                print("Size of CL: ", len(self.ca.instance.cl))
                print("Size of B: ", len(self.ca.instance.bias))
                print("Number of Queries: ", self.ca.metrics.membership_queries_count)

            gen_start = time.time()
            Y = self.ca.run_query_generation()
            gen_end = time.time()

            if len(Y) == 0:
                # if no query can be generated it means we have (prematurely) converged to the target network -----
                self.ca.metrics.finalize_results()
                return self.ca.instance.cl

            self.ca.metrics.increase_generation_time(gen_end - gen_start)
            self.ca.metrics.increase_generated_queries()
            self.ca.metrics.increase_top_queries()
            kappaB = get_kappa(self.ca.instance.bias, Y)

            answer = self.ca.ask_membership_query(Y)
            if answer:
                # it is a solution, so all candidates violated must go
                # B <- B \setminus K_B(e)
                self.ca.remove_from_bias(kappaB)

            else:  # user says UNSAT

                scope = self.ca.run_find_scope(Y)
                c = self.ca.run_findc(scope)
                self.ca.add_to_cl(c)


