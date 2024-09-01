import time

from cpmpy.transformations.get_variables import get_variables

from .algorithm_core import AlgorithmCAInteractive
from ..ca_system.active_ca import ActiveCA
from ..utils import get_relation, get_scope, get_kappa


class PQuAcq(AlgorithmCAInteractive):

    """
    PQuAcq is a variation of QuAcq, using Predict&Ask function and recommendation queries. Presented in
    "Constraint Acquisition with Recommendation Queries", IJCAI 2016.
    """

    def __init__(self, ca_system: ActiveCA = None):
        """
        Initialize the PQuAcq algorithm with an optional constraint acquisition system.

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
                self.predictAsk(get_relation(c, self.ca.instance.language))


    def predictAsk(self, r):
        """
        Predict&Ask function presented in "Constraint Acquisition with Recommendation Queries", IJCAI 2016.

        :param r: The index of a relation in gamma.
        :return: List of learned constraints.
        """
        try:
            import networkx as nx
        except ImportError:
            raise ImportError("To use the predictAsk function of PQuAcq, networkx needs to be installed")

        assert isinstance(r, int) and r in range(len(self.ca.instance.language)), \
            "predictAsk input must be the index of a relation in the language"

        alpha = 4  # \alpha from the paper, set to 4
        L = []
        C = [c for c in self.ca.instance.cl if get_relation(c, self.ca.instance.language) == r]

        # Project Y to those in C that have relation r
        Y = [v.name for v in get_variables(C)]
        E = [tuple([v.name for v in get_scope(c)]) for c in C]  # all scopes

        # Create the graph
        G = nx.Graph()
        G.add_nodes_from(Y)
        G.add_edges_from(E)

        B = [c for c in self.ca.instance.bias if get_relation(c, self.ca.instance.language) == r and
             frozenset(get_scope(c)).issubset(frozenset(Y))]
        D = [tuple([v.name for v in get_scope(c)]) for c in B]  # missing edges that can be completed (exist in B)
        neg = 0  # counter of negative answers

        while len(D) > 0 and neg < alpha:  # alpha is the cutoff

            scores = list(nx.adamic_adar_index(G, D))

            # Find the index of the tuple with the maximum score
            score_values = [score for _, _, score in scores]
            max_index = score_values.index(max(score_values))
            c = B[max_index]
            B.pop(max_index)
            D.pop(max_index)

            if self.ca.ask_recommendation_query(c):
                self.ca.add_to_cl(c)
                E.append(tuple([v.name for v in get_scope(c)]))
                G.add_edges_from(E)
                neg = 0
            else:
                neg += 1
                self.ca.remove_from_bias(c)
