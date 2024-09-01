from abc import ABC, abstractmethod

from ..ca_system.active_ca import ActiveCA


class AlgorithmCAInteractive(ABC):
    """
    Abstract base class for ICA (Interactive Constraint Acquisition) active_algorithms.
    """

    def __init__(self, ca_system: ActiveCA):
        """
        Initialize the AlgorithmCAInteractive with a constraint acquisition system.

        :param ca_system: An instance of CASystem.
        """
        self.ca = ca_system

    @abstractmethod
    def _learn(self):
        """
        Abstract method to learn constraints. Must be implemented by subclasses.
        """
        raise NotImplementedError

    @property
    def ca(self):
        """
        Get the constraint acquisition system.

        :return: The constraint acquisition system.
        """
        return self._ca

    @ca.setter
    def ca(self, ca_system: ActiveCA):
        """
        Set the constraint acquisition system and assign this algorithm to it.

        :param ca_system: The constraint acquisition system.
        """
        self._ca = ca_system
