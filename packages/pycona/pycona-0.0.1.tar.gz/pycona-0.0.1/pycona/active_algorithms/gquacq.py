import time

import networkx as nx
from cpmpy.transformations.get_variables import get_variables

from .algorithm_core import AlgorithmCAInteractive
from .utils import is_clique, can_be_clique
from ..ca_system.active_ca import ActiveCA
from ..utils import get_relation, get_scope, get_kappa


class GQuAcq(AlgorithmCAInteractive):

    """
    QuAcq variation algorithm, using mine&Ask to detect types of variables and ask genralization queries. From:
    "Detecting Types of Variables for Generalization in Constraint Acquisition", ICTAI 2015.
    """

    def __init__(self, ca_system: ActiveCA = None, qg_max=10):
        """
        Initialize the PQuAcq algorithm with an optional constraint acquisition system.

        :param ca_system: An instance of CASystem, default is None.
        : param GQmax: maximum number of generalization queries
        """
        super().__init__(ca_system)
        self._negativeQ = []
        self._qg_max = qg_max

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
                self.mineAsk(get_relation(c, self.ca.instance.language))


    def mineAsk(self, r):
        """
        Mine&Ask function presented in
        "Detecting Types of Variables for Generalization in Constraint Acquisition", ICTAI 2015.

        :param r: The index of a relation in gamma.
        :return: List of learned constraints.
        """
        gq_counter = 0

        C = [c for c in self.ca.instance.cl if get_relation(c, self.ca.instance.language) == r]

        # Project Y to those in C that have relation r
        Y = [v.name for v in get_variables(C)]
        E = [tuple([v.name for v in get_scope(c)]) for c in C]  # all scopes

        # Create the graph
        G = nx.Graph()
        G.add_nodes_from(Y)
        G.add_edges_from(E)

        T = [comp for comp in nx.components.connected_components(G) if not is_clique(G.subgraph(comp))]

        while len(T) > 0 and gq_counter < self._qg_max:
            Y = T.pop()
            gen_flag = False
            B = [c for c in self.ca.instance.bias if
                 get_relation(c, self.ca.instance.language) == r and frozenset(get_scope(c)).issubset(Y)]
            D = [tuple([v.name for v in get_scope(c)]) for c in B]  # missing edges that can be completed (exist in B)

            # if already a subset of it was negative, or cannot be completed to a clique, continue to next
            if not any(Y2.issubset(Y) for Y2 in self._negativeQ) and can_be_clique(G.subgraph(Y), D):
                # if potentially generalizing leads to unsat, continue to next
                new_CL = self.ca.instance.cl.copy()
                new_CL += B
                if new_CL.solve() and self.ca.ask_generalization_query(r, B):
                    gen_flag = True
                    self.ca.add_to_cl(B)
                else:
                    gq_counter += 1
                    self._negativeQ.append(Y)

            if not gen_flag:
                communities = nx.community.greedy_modularity_communities(G.subgraph(Y))
                [T.append(com) for com in communities if 2 < len(com) < len(Y)]
