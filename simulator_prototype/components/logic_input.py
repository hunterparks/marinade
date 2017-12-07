"""
    Logic input is to be viewed as either a constant or user changable signal
    into the architecture. Thus the device acts as a read only bus.
"""

from components.abstract.hooks import InputHook
from components.abstract.ibus import iBusRead

class LogicInput(InputHook,iBusRead):
    """
        Input hook into architecture that functions as a logical bus
    """

    def __init__(self, name, size, default_state = 0):
        "Constructor will cause exception on invalid parameters"
        if not isinstance(name, str) or size <= 0 or default_state < 0 or default_state > 2**size:
            raise ValueError('Initialization parameters invalid')

        self._name = name
        self._size = size
        self._state = default_state

    def inspect(self):
        "Returns a dictionary message to application defining current state"
        return {'name' : self._name, 'type' : 'logic', 'size' : 1, 'state' : self._state}

    def generate(self, message):
        "Sets a new state for read only bus from user space"
        if message is None:
            raise ValueError('Expecting message to be provided')
        elif 'state' not in message:
            raise ValueError('Invalid format for message')

        state = message['state']
        if isinstance(state,int) and state >= 0 and state < 2**self._size:
            self._state = state
        else:
            raise ValueError('Data in message does not match expected range')

    def read(self):
        "Returns last valid state set in user space"
        return self._state

    def size(self):
        "Returns size of bus"
        return self._size
