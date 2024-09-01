from abc import ABC, abstractmethod

from .. import Metrics
from ..problem_instance import ProblemInstance


class CASystem(ABC):
    """
    Abstract class interface for CA systems.
    """

    def __init__(self, instance: ProblemInstance, *, metrics: Metrics = None, verbose=0):
        """
        Initialize the CA system.

        :param instance: An instance of ProblemInstance.
        :param metrics: An instance of Metrics, default is a new Metrics object.
        :param verbose: Verbosity level, default is 0.
        """
        self._given_instance = instance  # ProblemInstance given by the user. Won't change during learning
        self.instance = instance  # ProblemInstance, changing during the acquisition process
        self.metrics = metrics
        self.verbose = verbose
        self.converged = False

    @abstractmethod
    def learn(self):
        """
        learn() method to initiate the learning process
        Must implement in subclasses
        """
        raise NotImplementedError

    def clear(self):
        """Clear the state of CA system: need to run after learning for a given instance"""
        self.instance = self._given_instance
        self._metrics = Metrics()
        self._converged = False

    @property
    def instance(self):
        """ Getter method for _instance """
        return self._instance

    @instance.setter
    def instance(self, instance):
        """ Setter method for _instance """
        self._instance = instance.copy() if instance is not None else None
        self._given_instance = instance

    @property
    def metrics(self):
        """ Getter method for _metrics """
        return self._metrics

    @metrics.setter
    def metrics(self, metrics):
        """ Setter method for _metrics """
        self._metrics = metrics if metrics is not None else Metrics()

    @property
    def verbose(self):
        """ Get the verbosity of the system """
        return self._verbose

    @verbose.setter
    def verbose(self, verbose):
        """ Set the verbosity of the system """
        self._verbose = verbose

    @property
    def converged(self):
        """ Get the convergence value """
        return self._converged

    @converged.setter
    def converged(self, converged):
        """ Set the convergence value """
        self._converged = converged
