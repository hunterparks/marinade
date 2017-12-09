"""
    Reset input is to be viewed as a user adjustable read only bus where the
    logical bit means that the component should handle reset behavior

    Note that reset can be used as a logic read bus of size one
"""

from components.abstract.hooks import InputHook
from components.abstract.ibus import iBusRead



class Reset(InputHook,iBusRead):
    """
        Input hook into architecture reflecting a reset signal, however it can
        be used as a logical bus. Note that the state expected to be stored is
        only the current value, for logic that requires previous state
        information that logic is responsible for keeping track of state change
    """

    def __init__(self, name, default_state = 0):
        "Constructor will cause exception on invalid parameters"
        if not isinstance(name, str):
            raise ValueError('Initialization parameters invalid')
        elif not isinstance(default_state,int) or default_state < 0 or default_state > 1:
            raise ValueError('Default state must be a bit value')

        self._name = name
        self._state = default_state


    def inspect(self):
        "Returns a dictionary message to application defining current state"
        return {'name' : self._name, 'type' : 'reset', 'size' : 1, 'state' : self._state}


    def generate(self, message=None):
        "Sets a new state for read only reset bus from user space"
        if message is None:
            # Assume that generate means a logic toggle (for compatibility)
            self._state = (self._state + 1) % 2
        elif 'state' in message:
            state = message['state']
            if not isinstance(state, int) or state < 0 or state > 1:
                raise ValueError('Clock bit can only be zero or one')
            self._state = state
        else:
            raise ValueError('Message type not supported')


    def read(self):
        "Returns last valid state set in user space"
        return self._state


    def size(self):
        "Returns size of bus"
        return 1
