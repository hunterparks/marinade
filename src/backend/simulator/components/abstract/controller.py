"""
Controller class is a flexible distinct entity that can take behavior from
combinational logic. However in some cases a sequential component is
necessary. Thus this class provides a means of defining a special component
labled as the constructor
"""

from simulator.components.abstract.combinational import Combinational
from simulator.components.abstract.sequential import Sequential

# TODO write the methods for this component


class Controller(Combinational, Sequential):
    """
    Controller is expected to be used as a singular component in the
    architecture with a specific purpose.
    """
    pass
