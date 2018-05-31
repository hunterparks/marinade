"""
Constant is to be viewed as an immutable bus in architectures

Configuration file template should follow form
{
    /* Required */

    "width" : 1,
    "value" : 12,

    /* Optional */

    "append_to_entities" : true
}

append_to_entities is flag used to append an hooks as entity (Used externally)
width is the bit-width for the component
value is the value for the component
"""

from simulator.components.abstract.hooks import Hook
from simulator.components.abstract.ibus import iBusRead


class Constant(Hook, iBusRead):
    """
    Input hook into architecture without the ability to change value
    """

    def __init__(self, size, state):
        "Constructor will cause exception on invalid parameters"
        if not isinstance(size, int) or size <= 0:
            raise TypeError('Size must be an integer greater than zero')
        elif not isinstance(state, int) or state < 0 or state >= 2**size:
            raise TypeError('State must be an integer that fits in defined range')

        self._size = size
        self._state = state

    def inspect(self):
        "Returns a dictionary messag to application defining current state"
        return {'type': 'logic', 'size': self._size, 'state': self._state}

    def read(self):
        "Returns last valid state set in user space"
        return self._state

    def size(self):
        "Returns size of bus"
        return self._size

    @classmethod
    def from_dict(cls, config, hooks):
        "Implements conversion from configuration to component"
        return Constant(config["width"],config["value"])
