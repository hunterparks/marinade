"""
    Hooks provide a means of communicating between other backend behavior and
    the simulator architecture. Thus the input functions into the architecture
    should be asserted at start of cycle.
"""

from abc import ABC, abstractmethod

class Hook(ABC):
    """
        Abstract Hook interface to define application inspection
    """

    @abstractmethod
    def inspect(self):
        "Hook method to inspect signals from the network"
        return NotImplemented

class InputHook(Hook):
    """
        Abstract Hook for module message generation
    """

    @abstractmethod
    def generate(self,message=None):
        "Hook method to generate signals to the rest of the network"
        return NotImplemented

class OutputHook(Hook):
    """
        Abstract Hook for module message inspection. (Distinct from Hook)
    """
    pass

class InternalHook(Hook):
    """
        Abstraction on Hook to define a subtype intended to be embedded inside
        another module type
    """

    @abstractmethod
    def modify(self,data):
        "Hook method to modify internal data for element"
        return NotImplemented
