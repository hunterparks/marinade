"""
    Combinational logic class makes a distinction between itself and other
    entities for the architecture construction process. 
"""

from abc import ABC, abstractmethod
from components.abstract.entity import Entity

class Combinational(Entity):
    """
        Interface to define a combinational logic compoent as distinct from
        other types of entities. This distinction is more for the overall
        architecture as opposed to providing unique behavior.

        The expectation is that combinational logic will be defined as a block
        with an unknown number of inputs and outputs but something that does
        not rely on clock or reset.
    """
    pass
