"""
Register component is a standalone core component for general architecture
development.

Configuration file template should follow form
{
    /* Required */

    "name" : "register",
    "type" : "Register",
    "size" : 8,
    "clock" : "",
    "reset" : "",
    "input" : "",

    /* Optional */

    "package" : ""core,
    "output" : "",
    "enable" : "",
    "value" : 0,
    "edge_type" : "",
    "reset_type" : "",
    "enable_type" : ""
}

name is the entity name, used by entity map (Used externally)
type is the component class (Used externally)
package is associated package to override general (Used externally)
size is number of bits stored in register
clock is control bus clock line reference
reset is control bus reset line reference
input is the data bus reference to store into register
output is the data bus reference to read from register
enable is write control bus reference
value is default value of a byte in memory
edge_type is edge to clock data
reset_type is logic level to clear memory
enable_type is logic level to write to memory
"""

from simulator.components.abstract.ibus import iBusRead, iBusWrite
from simulator.components.abstract.sequential import Sequential, Latch_Type, Logic_States


class Register(Sequential):
    """
    Register component implements a sequential fixed bit width memory space.
    Component expects a clock, reset as per sequential requirement.
    Component expects input and output bus to be of same size as internal

    Default state is state of device at startup and on reset
    """

    DEFAULT_STATE = 0
    DEFAULT_LATCH_TYPE = Latch_Type.RISING_EDGE
    DEFAULT_RESET_TYPE = Logic_States.ACTIVE_HIGH
    DEFAULT_ENABLE_TYPE = Logic_States.ACTIVE_HIGH

    def __init__(self, size, clock, reset, in_bus, out_bus=None, default_state=DEFAULT_STATE,
                 edge_type=Latch_Type.RISING_EDGE, reset_type=DEFAULT_RESET_TYPE,
                 enable=None, enable_type=DEFAULT_ENABLE_TYPE):
        "Constructor will check for valid parameters, exception thrown on invalid"

        if not isinstance(size, int) or size <= 0:
            raise TypeError('Size must be an integer greater than zero')
        elif not isinstance(default_state, int) or default_state < 0 or default_state >= 2**size:
            raise TypeError('Default state must be an integer that fits in defined range')

        self._size = size
        self._default_state = default_state
        self._q = default_state

        if not isinstance(clock, iBusRead) or not isinstance(reset, iBusRead) or not isinstance(in_bus, iBusRead):
            raise TypeError('Input buses must be readable')

        if not clock.size() == 1:
            raise ValueError('Clock bus must be size {}'.format(1))
        self._clock = clock
        self._prev_clock_state = clock.read()

        if not reset.size() == 1:
            raise ValueError('Reset bus must be size {}'.format(1))
        self._reset = reset

        if not in_bus.size() == size:
            raise ValueError('Input bus size must match internal size {}'.format(size))
        self._in_bus = in_bus

        if not isinstance(enable, iBusRead) and not enable is None:
            raise TypeError('If enable bus defined then must be readable')
        elif not enable is None and not enable.size() == 1:
            raise ValueError('Enable bus must be size {}'.format(1))
        self._enable = enable

        if not isinstance(out_bus, iBusWrite) and not out_bus is None:
            raise TypeError('If output bus defined then must be writable')
        elif not out_bus is None and not out_bus.size() == size:
            raise ValueError('Output bus size must match internal size {}'.format(size))
        self._out_bus = out_bus

        if not Latch_Type.valid(edge_type):
            raise ValueError('Invalid latch edge type')
        self._edge_type = edge_type

        if not Logic_States.valid(reset_type):
            raise ValueError('Invalid active reset type')
        self._reset_type = reset_type

        if not Logic_States.valid(enable_type):
            raise ValueError('Invalid active enable type')
        self._enable_type = enable_type

    def on_rising_edge(self):
        "Implements clock rising behavior: captures data if latching type matches"
        if self._edge_type == Latch_Type.RISING_EDGE or self._edge_type == Latch_Type.BOTH_EDGE:
            self._q = self._in_bus.read()

    def on_falling_edge(self):
        "Implements clock falling behavior: captures data if latching type matches"
        if self._edge_type == Latch_Type.FALLING_EDGE or self._edge_type == Latch_Type.BOTH_EDGE:
            self._q = self._in_bus.read()

    def on_reset(self):
        "Resets the output to default state defined for register"
        self._q = self._default_state

    def inspect(self):
        "Returns dictionary message to user"
        return {'type': 'register', 'size': self._size, 'state': self._q}

    def modify(self, message):
        "Handles message from user to modify memory contents"

        if message is None:
            return {'error': 'expecting message to be provided'}
        elif 'state' not in message:
            return {'error': 'invalid format for message'}

        state = message['state']
        if isinstance(state, int) and state >= 0 and state < 2**self._size:
            self._q = state
            return {'success': True}
        else:
            return {'error': 'data in message does not match internal size'}

    def clear(self):
        "Hook method to clear memory, thereby returning it to default value"
        self.on_reset()
        return {'success': True}

    def run(self, time=None):
        "Timestep handler function clocks data into register and asserts output"

        # process enable line
        e = True
        if not self._enable is None:
            if self._enable_type == Logic_States.ACTIVE_LOW:
                e = self._enable.read() == 0
            else:
                e = self._enable.read() == 1

        # check for clock change
        if e:
            if self._clock.read() == 1 and self._prev_clock_state == 0:
                self.on_rising_edge()
            elif self._clock.read() == 0 and self._prev_clock_state == 1:
                self.on_falling_edge()
        self._prev_clock_state = self._clock.read()

        # check for reset event
        if self._reset_type == Logic_States.ACTIVE_LOW and self._reset.read() == 0:
            self.on_reset()
        elif self._reset_type == Logic_States.ACTIVE_HIGH and self._reset.read() == 1:
            self.on_reset()

        # assert output for timestep
        if not self._out_bus is None:
            self._out_bus.write(self._q)

    @classmethod
    def from_dict(cls, config, hooks):
        "Implements conversion from configuration to component"
        if "output" in config:
            output = hooks[config["output"]]
        else:
            output = None

        if "value" in config:
            default_state = config["value"]
        else:
            default_state = Register.DEFAULT_STATE

        if "edge_type" in config:
            edge_type = Latch_Type.fromString(config["edge_type"])
        else:
            edge_type = Register.DEFAULT_LATCH_TYPE

        if "reset_type" in config:
            reset_type = Logic_States.fromString(config["reset_type"])
        else:
            reset_type = Register.DEFAULT_RESET_TYPE

        if "enable" in config:
            enable = hooks[config["enable"]]
        else:
            enable = None

        if "enable_type" in config:
            enable_type = Logic_States.fromString(config["enable_type"])
        else:
            enable_type = Register.DEFAULT_ENABLE_TYPE

        return Register(config["size"], hooks[config["clock"]], hooks[config["reset"]],
                        hooks[config["input"]], output, default_state, edge_type,
                        reset_type, enable, enable_type)
