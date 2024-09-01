import numpy as np
from cpmpy.expressions.core import Expression

from .ca_system_core import CASystem
from ..answering_queries.oracle import Oracle
from ..answering_queries.user_oracle import UserOracle
from ..problem_instance import ProblemInstance
from ..metrics import Metrics
from ..utils import get_kappa


class ActiveCA(CASystem):
    """
    Class interface for the interactive CA systems. Using all CA components (Algorithm, Query generation, FindScope,
    FindC etc.), storing the necessary elements and providing functionality to update the state of the system as needed.
    """

    def __init__(self, instance: ProblemInstance, *, algorithm: 'ICA_Algorithm' = None, qgen: 'QGenBase' = None,
                 find_scope: 'FindScopeBase' = None, findc: 'FindCBase' = None, oracle: Oracle = None,
                 metrics: Metrics = None, verbose=0):
        """
        Initialize with an optional problem instance, oracle, and metrics.

        :param instance: An instance of ProblemInstance, default is None.
        :param algorithm: An instance of ICA_Algorithm, default is None.
        :param qgen: An instance of QGenBase, default is None.
        :param find_scope: An instance of FindScopeBase, default is None.
        :param findc: An instance of FindCBase, default is None.
        :param oracle: An instance of Oracle, default is None.
        :param metrics: An instance of Metrics, default is a new Metrics object.
        :param verbose: Verbosity level, default is 0.
        """
        super().__init__(instance, metrics=metrics, verbose=verbose)
        self.algorithm = algorithm
        self.qgen = qgen
        self.find_scope = find_scope
        self.findc = findc
        self._oracle = oracle if oracle is not None else UserOracle()
        self._last_answer = True

    def clear(self):
        """Clear the state of CA system: need to run after learning for a given instance"""
        super().clear()
        self._last_answer = True

    def init_state(self):
        """ Initialize the state of the CA system. """
        self.algorithm.ca = self
        self.qgen.ca = self
        self.find_scope.ca = self
        self.findc.ca = self

    def learn(self):
        """ Start the learning process of the CA system. """
        self.init_state()
        self.algorithm._learn()
        return self.instance

    def run_query_generation(self):
        """ Run the query generation process. """
        Y = self.qgen.generate()
        return Y

    def run_find_scope(self, Y, kappa=None):
        """ Run the find scope process. """
        scope = self.find_scope.run(Y, kappa)
        return scope

    def run_findc(self, scope):
        """ Run the find constraint process. """
        c = self.findc.run(scope)
        return c

    @property
    def algorithm(self):
        """ Getter method for _algorithm """
        return self._algorithm

    @algorithm.setter
    def algorithm(self, algorithm: 'ICA_Algorithm'):
        """ Setter method for _algorithm """
        from ..active_algorithms import AlgorithmCAInteractive, GrowAcq
        assert isinstance(algorithm, AlgorithmCAInteractive) or algorithm is None
        self._algorithm = algorithm if algorithm is not None else GrowAcq()
        self._algorithm.ca = self

    @property
    def qgen(self):
        """ Getter method for _qgen """
        return self._qgen

    @qgen.setter
    def qgen(self, qgen: 'QGenBase'):
        """ Setter method for _qgen """
        from ..query_generation import QGenBase, PQGen
        from ..query_generation.qgen_obj import obj_max_viol
        assert isinstance(qgen, QGenBase) or qgen is None
        self._qgen = qgen if qgen is not None else PQGen(objective_function=obj_max_viol)
        self._qgen.ca = self

    @property
    def find_scope(self):
        """ Getter method for _find_scope """
        return self._find_scope

    @find_scope.setter
    def find_scope(self, find_scope: 'FindScopeBase'):
        """ Setter method for _find_scope """
        from ..find_scope import FindScopeBase, FindScope2
        assert isinstance(find_scope, FindScopeBase) or find_scope is None
        self._find_scope = find_scope if find_scope is not None else FindScope2()
        self._find_scope.ca = self

    @property
    def findc(self):
        """ Getter method for _findc """
        return self._findc

    @findc.setter
    def findc(self, findc: 'FindCBase'):
        """ Setter method for _findc """
        from ..find_constraint import FindCBase, FindC
        assert isinstance(findc, FindCBase) or findc is None
        self._findc = findc if findc is not None else FindC()
        self._findc.ca = self

    @property
    def oracle(self):
        """ Getter method for _oracle """
        return self._oracle

    @oracle.setter
    def oracle(self, oracle):
        """ Setter method for _oracle """
        self._oracle = oracle

    @property
    def last_answer(self):
        """ Get the last answer (bool) """
        return self._last_answer

    @last_answer.setter
    def last_answer(self, last_answer):
        """ Set the last answer (bool) """
        self._last_answer = last_answer

    def ask_membership_query(self, Y=None):
        """
        Ask a membership query to the oracle.

        :param Y: Optional. A subset of variables to be used in the query. If None, all variables are used.
        :return: The oracle's answer to the membership query (True/False).
        """
        X = self.instance.X
        if Y is None:
            Y = X
        e = self.instance.variables.value()
        value = np.zeros(e.shape, dtype=int)

        # Create a truth table numpy array
        sel = np.array([item in set(Y) for item in list(self.instance.variables.flatten())]).reshape(self.instance.variables.shape)

        # Variables present in the partial query
        value[sel] = e[sel]

        # Post the query to the user/oracle
        if self.verbose > 0:
            print(f"Query{self.metrics.membership_queries_count}: is this a solution?")
            self.instance.visualize(value)
        if self.verbose > 1:
            print("violated from B: ", get_kappa(self.instance.bias, Y))

        # Oracle answers
        self.last_answer = self.oracle.answer_membership_query(Y)
        if self.verbose > 0:
            print("Answer: ", ("Yes" if self.last_answer else "No"))

        # For the evaluation metrics
        if self.metrics:
            self.metrics.increase_membership_queries_count()
            self.metrics.increase_queries_size(len(Y))
            self.metrics.asked_query()

        return self.last_answer

    def ask_recommendation_query(self, c):
        """
        Ask a recommendation query to the oracle.

        :param c: The constraint to be recommended.
        :return: The oracle's answer to the recommendation query (True/False).
        """
        assert isinstance(c, Expression), "Recommendation queries need constraints as input"
        if self.verbose > 0:
            print(f"Rec query: is this a constraint of the problem? {c}")

        answer = self.oracle.answer_recommendation_query(c)
        if self.verbose > 0:
            print("Answer: ", ("Yes" if answer else "No"))

        # For the evaluation metrics
        if self.metrics:
            self.metrics.increase_recommendation_queries_count()
            self.metrics.asked_query()

        return answer

    def ask_generalization_query(self, c, C):
        """
        Ask a generalization query to the oracle.

        :param c: The constraint to be generalized.
        :param C: A list of constraints to which the generalization is applied.
        :return: The oracle's answer to the generalization query (True/False).
        """
        assert isinstance(c, Expression), "Generalization queries first input needs to be a constraint"
        assert isinstance(C, list), "Generalization queries second input needs to be a list of constraints"
        assert all(isinstance(c1, Expression) for c1 in C), "Generalization queries second input needs to be " \
                                                           "a list of constraints"
        if self.verbose > 0:
            print(f"Generalization query: Can we generalize constraint {c} to all in {C}?")

        answer = self.oracle.answer_generalization_query(C)
        if self.verbose > 0:
            print("Answer: ", ("Yes" if answer else "No"))

        # For the evaluation metrics
        if self.metrics:
            self.metrics.increase_generalization_queries_count()
            self.metrics.asked_query()

        return answer

    def remove_from_bias(self, C):
        """
        Remove given constraints from the bias (candidates)

        :param C: list of constraints to be removed from B
        """
        if isinstance(C, Expression):
            C = [C]
        assert isinstance(C, list), "remove_from_bias accepts as input a list of constraints or a constraint"

        if self.verbose > 1:
            print(f"removing the following constraints from bias: {C}")

        self.instance.bias = list(set(self.instance.bias) - set(C))

    def add_to_cl(self, C):
        """
        Add the given constraints to the list of learned constraints

        :param C: Constraints to add to CL
        """
        if isinstance(C, Expression):
            C = [C]
        assert isinstance(C, list), "add_to_cl accepts as input a list of constraints or a constraint"

        if self.verbose > 1:
            print(f"adding the following constraints to C_L: {C}")

        # Add constraint(s) c to the learned network and remove them from the bias
        self.instance.cl.extend(C)  # TODO check if works properly
        self.instance.bias = list(set(self.instance.bias) - set(C))
        self.metrics.cl += 1


