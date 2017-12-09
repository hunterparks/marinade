"""
    Clock input is to be viewed as a user adjustable read only bus where the
    frequency of calling a clock generate relative to the timestep (run rate)
    determines the resolution of the application.

    Note that clock can be used as a logic read bus of size one
"""

from components.abstract.hooks import InputHook
from components.abstract.ibus import iBusRead
from components.abstract.entity import Entity
import limits



class Clock(InputHook,iBusRead,Entity):
    """
        Input hook into architecture reflecting a clock signal, however it can
        be used as a logical bus. Note that the state expected to be stored is
        only the current value, for logic that requires previous state
        information that logic is responsible for keeping track of state change
    """

    def __init__(self, name, freq, default_state = 0):
        "Constructor will cause exception on invalid parameters"
        if not isinstance(name, str):
            raise TypeError('Name must be a string')
        elif not isinstance(default_state,int) or default_state < 0 or default_state > 1:
            raise TypeError('Default state must be a bit value')
        elif freq < limits.MIN_FREQUENCY or freq > limits.MAX_FREQUENCY:
            raise ValueError('Frequency must be valid')

        self._name = name
        self._state = default_state
        self._freq = freq #Hz
        self._default_state = default_state


    def inspect(self):
        "Returns a dictionary message to application defining current state"
        return {'name' : self._name, 'type' : 'clock', 'size' : 1, 'state' : self._state}


    def generate(self, message=None):
        "Sets a new state or frequency for clock bus from user space"
        if message is None:
            # Assume that generate means a logic toggle (for compatibility)
            self._state = (self._state + 1) % 2
        elif 'frequency' in message:
            freq  = message['frequency']
            if freq < limits.MIN_FREQUENCY or freq > limits.MAX_FREQUENCY:
                raise ValueError('Frequency must be valid')
            self._freq = freq
        elif 'state' in message:
            state = message['state']
            if not isinstance(state, int) or state < 0 or state > 1:
                raise ValueError('Clock bit can only be zero or one')
            self._state = state
        else:
            raise TypeError('Message type not supported')


    def read(self):
        "Returns last valid state set in user space"
        return self._state


    def size(self):
        "Returns size of bus"
        return 1


    def run(self,time):
        "Generates a clock which is dependent on it's frequency and current time"
        if not self._freq == 0:
            T = (1 / self._freq)
            t = time % T
            self._state = self._default_state if t < T / 2 else (self._default_state + 1) % 2
        else:
            self._state = self._default_state
