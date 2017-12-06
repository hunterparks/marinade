"""
    Define Read and Write behavior for bus types in the system architecture
"""

from abc import ABC, abstractmethod

class iBusRead(ABC):
    """
        Interface to enforce read behavior on a bus type object
    """

    @abstractmethod
    def read(self):
        "Interface function for bus to send data to caller, expect a return value"
        return NotImplemented

class iBusWrite(ABC):
    """
        Interface to enforce write behavior on a bus type object
    """

    @abstractmethod
    def write(self,data):
        "Interface function for bus to receive data from caller, no return"
        return NotImplemented
