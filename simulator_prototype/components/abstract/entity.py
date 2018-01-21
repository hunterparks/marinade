"""
All objects in architecture that are defined with functionality, excluding
buses, must have this in its inheritance tree. The run function is the
mechanism to cause the functional behavior of each module to interact in
the architecture during runtime.

Run function is to be called on whatever timestep the architecture is using,
whether that be per fastest clock or faster. (Recall Nyquist 2f_comp = f_arch)
"""

from abc import ABC, abstractmethod


class Entity(ABC):
    """
    Entity is interface to define the architecture simulation functionality
    """

    @abstractmethod
    def run(self, time):
        "Implement this in each concrete child to run in the architecture"
        return NotImplemented
