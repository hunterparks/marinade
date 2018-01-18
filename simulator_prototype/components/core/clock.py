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

    def __init__(self, freq, default_state = 0):
        "Constructor will cause exception on invalid parameters"
        if not isinstance(default_state,int) or default_state < 0 or default_state > 1:
            raise TypeError('Default state must be a bit value')
        elif not isinstance(freq,(float,int)):
            raise TypeError('Frequency must be a real number type')
        elif freq < limits.MIN_FREQUENCY or freq > limits.MAX_FREQUENCY:
            raise ValueError('Frequency must be within limits')

        self._state = default_state
        self._freq = freq #Hz
        self._default_state = default_state


    def inspect(self):
        "Returns a dictionary message to application defining current state"
        return {'type' : 'clock', 'size' : 1, 'state' : self._state, 'frequency' : self._freq}


    def generate(self, message=None):
        "Sets a new state or frequency for clock bus from user space"
        no_valid_in_message = True

        # do not handle empty message
        if message is None:
            return {'error' : 'expecting message to be provided'}

        # get frequency message if available
        f = self._freq
        if 'frequency' in message:
            no_valid_in_message = False
            freq  = message['frequency']
            if not isinstance(freq,(float,int)):
                return {'error' : 'frequency must be a real number type'}
            elif freq < limits.MIN_FREQUENCY or freq > limits.MAX_FREQUENCY:
                return {'error' : 'data in message does not match expected range'}
            f = freq

        # get state message if available
        s = self._state
        if 'state' in message:
            no_valid_in_message = False
            state = message['state']
            if not isinstance(state, int) or state < 0 or state > 1:
                return {'error' : 'data in message does not match expected range'}
            s = state

        # if a message was valid then set and return success else failure
        if no_valid_in_message:
            return {'error' : 'invalid format for message'}
        else:
            self._freq = f
            self._state = s
            return {'success' : True}


    def read(self):
        "Returns last valid state set in user space"
        return self._state


    def size(self):
        "Returns size of bus"
        return 1


    def frequency(self):
        "Returns clock frequency"
        return self._freq


    def run(self,time):
        "Generates a clock which is dependent on it's frequency and current time"
        if not self._freq == 0:
            T = (1 / self._freq)
            t = time % T
            self._state = self._default_state if t < T / 2 else (self._default_state + 1) % 2
        else:
            self._state = self._default_state
