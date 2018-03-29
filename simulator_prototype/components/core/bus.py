"""
Bus instances used as conduits of numerical data of fixed size. Expectation
is that a bus will be written to by one component but can be read by many.
"""

from components.abstract.hooks import OutputHook
from components.abstract.ibus import iBusRead, iBusWrite


class Bus(OutputHook, iBusRead, iBusWrite):
    """
    Bus is a read/write object used to connect architecture entities
    """

    def __init__(self, size, default_value=0):
        "Constructor will cause exception on invalid parameters"
        if not isinstance(size, int) or size <= 0:
            raise TypeError('Size must be an integer greater than zero')
        elif not isinstance(default_value, int) or default_value < 0 or default_value >= 2**size:
            raise TypeError('Default state must be an integer that fits in defined range')

        self._size = size
        self._value = default_value

    def inspect(self):
        "Returns a dictionary message to application caller defining state of bus"
        return {'type': 'logic', 'size': self._size, 'state': self._value}

    def read(self):
        "Returns last valid value written to bus object"
        return self._value

    def write(self, value):
        "Writes parameter to bus, if out of bus' bounds then exception occurs"
        if isinstance(value, int):
            if value < 0 or value >= 2**self._size:
                raise ValueError('Value out of range for bus')
            self._value = value
        elif isinstance(value, iBusRead):
            self.write(value.read())
        else:
            raise TypeError('Type invalid, pass either integer or readable')

    def size(self):
        "Returns size of bus"
        return self._size

    @classmethod
    def from_dict(cls, config):
        "Implements conversion from configuration to component"
        return NotImplemented

    @classmethod
    def to_dict(cls):
        "Implements conversion from component to configuration"
        return NotImplemented
