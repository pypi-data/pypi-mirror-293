from abc import ABC, abstractmethod
from ..ca_system.active_ca import ActiveCA


class QGenBase(ABC):
    """
    Abstract class interface for QGen implementations.
    """

    def __init__(self, ca_system: ActiveCA = None, time_limit=2):
        """
        Initialize the QGenBase with the given CA system and time limit.

        :param ca_system: The CA system used.
        :param time_limit: Overall time limit.
        """
        self._ca = ca_system
        self._time_limit = time_limit

    @abstractmethod
    def generate(self):
        """
        Method that all QGen implementations must implement to generate a query.
        """
        raise NotImplementedError

    @property
    def ca(self):
        """
        Get the CA system.

        :return: The CA system.
        """
        return self._ca

    @ca.setter
    def ca(self, ca_system: ActiveCA = None):
        """
        Set the CA system.

        :param ca_system: The CA system to set.
        """
        self._ca = ca_system

    @property
    def time_limit(self):
        """
        Get the time limit.

        :return: The time limit.
        """
        return self._time_limit

    @time_limit.setter
    def time_limit(self, time_limit):
        """
        Set the time limit.

        :param time_limit: The time limit to set.
        """
        self._time_limit = time_limit
