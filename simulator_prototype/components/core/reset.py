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

    def __init__(self, default_state = 0):
        "Constructor will cause exception on invalid parameters"
        if not isinstance(default_state,int) or default_state < 0 or default_state > 1:
            raise TypeError('Default state must be a bit value')

        self._state = default_state


    def inspect(self):
        "Returns a dictionary message to application defining current state"
        return {'type' : 'reset', 'size' : 1, 'state' : self._state}


    def generate(self, message=None):
        "Sets a new state for read only reset bus from user space"

        if message is None:
            return {'error' : 'expecting message to be provided'}
        elif 'state' not in message:
            return {'error' : 'invalid format for message'}

        state = message['state']
        if isinstance(state,int) and state >= 0 and state < 2:
            self._state = state
            return {'success' : True}
        else:
            return {'error' : 'data in message does not match expected range'}


    def read(self):
        "Returns last valid state set in user space"
        return self._state


    def size(self):
        "Returns size of bus"
        return 1
