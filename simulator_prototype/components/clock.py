"""
    Clock input is to be viewed as a user adjustable read only bus where the
    frequency of calling a clock generate relative to the timestep (run rate)
    determines the resolution of the application.

    Note that clock can be used as a logic read bus of size one
"""

from components.abstract.hooks import InputHook
from components.abstract.ibus import iBusRead

class Clock(InputHook,iBusRead):
    """
        Input hook into architecture reflecting a clock signal, however it can
        be used as a logical bus. Note that the state expected to be stored is
        only the current value, for logic that requires previous state
        information that logic is responsible for keeping track of state change
    """

    def __init__(self, name, default_state = 0):
        "Constructor will cause exception on invalid parameters"
        if not isinstance(name, str) or default_state < 0 or default_state > 1:
            raise ValueError('Initialization parameters invalid')

        self._name = name
        self._state = default_state

    def inspect(self):
        "Returns a dictionary message to application defining current state"
        return {'name' : self._name, 'type' : 'clock', 'size' : 1, 'state' : self._state}

    def generate(self, message=None):
        "Sets a new state for read only clock bus from user space"
        self._state = (self._state + 1) % 2

    def read(self):
        "Returns last valid state set in user space"
        return self._state

    def size(self):
        "Returns size of bus"
        return self._size
