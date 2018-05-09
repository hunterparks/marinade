"""
Logic input is to be viewed as user changable signal
into the architecture. Thus the device acts as a read only bus.

Configuration file template should follow form
{
    /* Required */
    "name" : "logic_input",
    "type" : "LogicInput",
    "size" : 1,

    /* Optional */

    "package" : "core",
    "value" : 1
}

name is the entity name, used by entity map (Used externally)
type is the component class (Used externally)
package is associated package to override general (Used externally)
size is the bit-width for the component
value is the default value for the component
"""

from simulator.components.abstract.hooks import InputHook
from simulator.components.abstract.ibus import iBusRead


class LogicInput(InputHook, iBusRead):
    """
    Input hook into architecture that functions as a logical bus
    """

    DEFAULT_STATE = 0

    def __init__(self, size, default_state=DEFAULT_STATE):
        "Constructor will cause exception on invalid parameters"
        if not isinstance(size, int) or size <= 0:
            raise TypeError('Size must be an integer greater than zero')
        elif not isinstance(default_state, int) or default_state < 0 or default_state >= 2**size:
            raise TypeError('Default state must be an integer that fits in defined range')

        self._size = size
        self._state = default_state

    def inspect(self):
        "Returns a dictionary message to application defining current state"
        return {'type': 'logic', 'size': self._size, 'state': self._state}

    def generate(self, message):
        "Sets a new state for read only bus from user space, returns confirmation"

        if message is None:
            return {'error': 'expecting message to be provided'}
        elif 'state' not in message:
            return {'error': 'invalid format for message'}

        state = message['state']
        if isinstance(state, int) and state >= 0 and state < 2**self._size:
            self._state = state
            return {'success': True}
        else:
            return {'error': 'data in message does not match expected range'}

    def read(self):
        "Returns last valid state set in user space"
        return self._state

    def size(self):
        "Returns size of bus"
        return self._size

    @classmethod
    def from_dict(cls, config, hooks):
        "Implements conversion from configuration to component"
        if "value" in config:
            default_state = config["value"]
        else:
            default_state = LogicInput.DEFAULT_STATE

        return LogicInput(config["size"],default_state)
