import time
import numpy as np
from cpmpy.expressions.utils import all_pairs

from .algorithm_core import AlgorithmCAInteractive
from ..utils import get_kappa, get_scope, get_relation
from ..ca_system.active_ca import ActiveCA


class MQuAcq2(AlgorithmCAInteractive):
    """
    MQuAcq2 is an implementation of the ICA_Algorithm that uses a modified QuAcq algorithm to learn constraints.
    """

    def __init__(self, ca_system: ActiveCA = None, *, perform_analyzeAndLearn: bool = True, cliques_cutoff=1):
        """
        Initialize the MQuAcq2 algorithm with an optional constraint acquisition system,
        a flag to perform analyze and learn, and a cliques cutoff value.

        :param ca_system: An instance of CASystem, default is None.
        :param perform_analyzeAndLearn: A boolean flag to perform analyze and learn, default is True.
        :param cliques_cutoff: A cutoff value for cliques, default is 1.
        """
        super().__init__(ca_system)
        self._perform_analyzeAndLearn = perform_analyzeAndLearn
        self._cliques_cutoff = cliques_cutoff

        self.cl_neighbours = None
        self.hashX = None

    def _learn(self):
        """
        Learn constraints using the modified QuAcq algorithm by generating queries and analyzing the results.
        """
        # Hash the variables
        self.hashX = [hash(x) for x in self.ca.instance.X]
        self.cl_neighbours = np.zeros((len(self.ca.instance.X), len(self.ca.instance.X)), dtype=bool)

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
            gen_start = time.time()
            Y = self.ca.run_query_generation()
            gen_end = time.time()

            if len(Y) == 0:
                # if no query can be generated it means we have (prematurely) converged to the target network -----
                self.ca.metrics.finalize_results()
                return self.ca.instance.cl

            self.ca.metrics.increase_generation_time(gen_end - gen_start)
            self.ca.metrics.increase_generated_queries()

            kappaB = get_kappa(self.ca.instance.bias, Y)

            while len(kappaB) > 0:

                if self.ca.verbose > 0:
                    print("Size of CL: ", len(self.ca.instance.cl))
                    print("Size of B: ", len(self.ca.instance.bias))
                    print("Number of queries: ", self.ca.metrics.total_queries)
                    print("MQuAcq-2 Queries: ", self.ca.metrics.top_lvl_queries)
                    print("FindScope Queries: ", self.ca.metrics.findscope_queries)
                    print("FindC Queries: ", self.ca.metrics.findc_queries)

                self.ca.metrics.increase_top_queries()

                if self.ca.ask_membership_query(Y):
                    # it is a solution, so all candidates violated must go
                    # B <- B \setminus K_B(e)
                    self.ca.remove_from_bias(kappaB)
                    kappaB = set()
                else:  # user says UNSAT

                    scope = self.ca.run_find_scope(Y)
                    c = self.ca.run_findc(scope)
                    self.ca.add_to_cl(c)

                    NScopes = set()
                    NScopes.add(tuple(scope))

                    if self.perform_analyzeAndLearn:
                        NScopes = NScopes.union(self.analyze_and_learn(Y))

                    Y = [y2 for y2 in Y if not any(y2 in set(nscope) for nscope in NScopes)]

                    kappaB = get_kappa(self.ca.instance.bias, Y)

    def analyze_and_learn(self, Y):

        NScopes = set()
        QCliques = set()

        # Find all neighbours
        self.find_neighbours()

        # Gamma precentage in FindQCliques is set to 0.8
        self.find_QCliques(list(self.ca.instance.X.copy()), set(), set(), QCliques, 0.8, 0)

        # [self.isQClique(clique, 0.8) for clique in QCliques]

        cliques_relations = self.QCliques_relations(QCliques)

        # Find the scopes that have a constraint in B violated, which can fill the incomplete cliques
        if len(QCliques) == 0:
            return set()

        Cq = [c for c in get_kappa(self.ca.instance.bias, Y) if any(
            set(get_scope(c)).issubset(clique) and get_relation(c, self.ca.instance.language) in cliques_relations[i]
            for i, clique in
            enumerate(QCliques))]

        PScopes = {tuple(get_scope(c)) for c in Cq}

        for pscope in PScopes:

            if self.ca.ask_membership_query(pscope):
                # It is a solution, so all candidates violated must go
                # B <- B \setminus K_B(e)
                kappaB = get_kappa(self.ca.instance.bias, pscope)
                self.ca.remove_from_bias(kappaB)

            else:  # User says UNSAT

                # c <- findC(e, findScope(e, {}, grid, false))
                c = self.ca.run_findc(pscope)
                self.ca.add_to_cl(c)

                NScopes.add(tuple(pscope))

        if len(NScopes) > 0:
            NScopes = NScopes.union(self.analyze_and_learn(Y))

        return NScopes

    def find_neighbours(self):

        C = self.ca.instance.cl

        for c in C:

            scope = get_scope(c)

            i = self.hashX.index(hash(scope[0]))
            j = self.hashX.index(hash(scope[1]))

            self.cl_neighbours[i][j] = True
            self.cl_neighbours[j][i] = True

    def QCliques_relations(self, QCliques):

        cl_relations = [get_relation(c, self.ca.instance.language) for c in self.ca.instance.cl]
        cliques_relations = [[rel for i, rel in enumerate(cl_relations)
                              if set(get_scope(self.ca.instance.cl[i])).issubset(clique)] for clique in QCliques]

        return cliques_relations

    # For debugging
    def is_QClique(self, clique, gammaPerc):

        edges = 0

        q = len(clique)
        q = gammaPerc * (q * (q - 1) / 2)  # number of edges needed to be considered a quasi-clique

        for var1, var2 in all_pairs(clique):
            k = self.hashX.index(hash(var1))
            l = self.hashX.index(hash(var2))

            if self.cl_neighbours[k, l]:
                edges = edges + 1

        if edges < q:
            raise Exception(
                f'findQCliques returned a clique that is not a quasi clique!!!! -> {clique} \nedges = {edges}\nq = {q}')

    def find_QCliques(self, A, B, K, QCliques, gammaPerc, t):
        """
        Find quasi-cliques in the given set of variables.

        :param A: Set of variables to be considered.
        :param B: Set of variables to be excluded.
        :param K: Set of variables forming the current clique.
        :param QCliques: Set of found quasi-cliques.
        :param gammaPerc: Percentage of edges needed to be considered a quasi-clique.
        :param t: Time taken for the process.
        """

        start = time.time()

        if len(A) == 0 and len(K) > 2:
            if not any(K.issubset(set(clique)) for clique in QCliques):
                QCliques.add(tuple(K))

        while len(A) > 0:

            end = time.time()
            t = t + end - start
            start = time.time()

            if t > self.cliques_cutoff:
                return

            x = A.pop()

            K2 = K.copy()
            K2.add(x)

            A2 = set(self.ca.instance.X) - K2 - B
            A3 = set()

            # calculate the number of existing edges on K2
            edges = 0
            for var1, var2 in all_pairs(K2):
                k = self.hashX.index(hash(var1))
                l = self.hashX.index(hash(var2))

                if self.cl_neighbours[k, l]:
                    edges = edges + 1

            q = len(K2) + 1
            q = gammaPerc * (q * (q - 1) / 2)  # number of edges needed to be considered a quasi-clique

            # for every y in A2, check if K2 U y is a gamma-clique (if so, store in A3)
            for y in list(A2):  # take (yet another) copy

                edges_with_y = edges

                # calculate the number of from y to K2
                for var in K2:

                    k = self.hashX.index(hash(var))
                    l = self.hashX.index(hash(y))

                    if self.cl_neighbours[k, l]:
                        edges_with_y = edges_with_y + 1

                if edges_with_y >= q:
                    A3.add(y)

            self.find_QCliques(A3, B.copy(), K2.copy(), QCliques, gammaPerc, t)

            B.add(x)

    @property
    def perform_analyzeAndLearn(self):
        """
        Get the flag indicating whether to perform analyze and learn.

        :return: Boolean flag indicating whether to perform analyze and learn.
        """
        return self._perform_analyzeAndLearn

    @perform_analyzeAndLearn.setter
    def perform_analyzeAndLearn(self, perform_analyzeAndLearn: bool):
        """
        Set the flag indicating whether to perform analyze and learn.

        :param perform_analyzeAndLearn: Boolean flag indicating whether to perform analyze and learn.
        """
        self._perform_analyzeAndLearn = perform_analyzeAndLearn

    @property
    def cliques_cutoff(self):
        """
        Get the cutoff value for cliques.

        :return: Cutoff value for cliques.
        """
        return self._cliques_cutoff

    @cliques_cutoff.setter
    def cliques_cutoff(self, cliques_cut: float):
        """
        Set the cutoff value for cliques.

        :param cliques_cut: Cutoff value for cliques.
        """
        self._cliques_cutoff = cliques_cut
        