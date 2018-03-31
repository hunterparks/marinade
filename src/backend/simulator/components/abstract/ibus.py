"""
Define Read and Write behavior for bus types in the system architecture
"""

from abc import abstractmethod
from simulator.components.abstract.configuration_parser import ConfigurationParser

class iBus(ConfigurationParser):
    """
    Interface to enforce size constraint on bus type objects
    """

    @abstractmethod
    def size(self):
        "Interface function for bus to note its size to the caller, expect return"
        return NotImplemented


class iBusRead(iBus):
    """
    Interface to enforce read behavior on a bus type object
    """

    @abstractmethod
    def read(self):
        "Interface function for bus to send data to caller, expect a return value"
        return NotImplemented


class iBusWrite(iBus):
    """
    Interface to enforce write behavior on a bus type object
    """

    @abstractmethod
    def write(self, data):
        "Interface function for bus to receive data from caller, no return"
        return NotImplemented
