"""
    Register component is a standalone core component for general architecture
    development.
"""

from components.abstract.ibus import iBusRead, iBusWrite
from components.core.clock import Clock
from components.core.reset import Reset
from components.abstract.sequential import Sequential, Latch_Type, Logic_States



class Register(Sequential):
    """
        Register component implements a sequential fixed bit width memory space.
        Component expects a clock, reset as per sequential requirement.
        Component expects input and output bus to be of same size as internal

        Default state is state of device at startup and on reset
    """

    def __init__(self, name, size, clock, reset, in_bus, out_bus = None, default_state = 0,
                edge_type = Latch_Type.RISING_EDGE, reset_type = Logic_States.ACTIVE_LOW,
                enable = None, enable_type = Logic_States.ACTIVE_HIGH):
        "Constructor will check for valid parameters, exception thrown on invalid"

        if not isinstance(name,str):
            raise ValueError('Name must be a string')
        elif not isinstance(size,int) or size <= 0:
            raise ValueError('Size must be an integer greater than zero')
        elif not isinstance(default_state,int) or default_state < 0 or default_state >= 2**size:
            raise ValueError('Default state must be an integer that fits in defined range')

        self._name = name
        self._size = size
        self._default_state = default_state
        self._d = default_state
        self._q = default_state

        if not isinstance(clock,iBusRead) or not isinstance(reset,iBusRead) or not isinstance(in_bus,iBusRead):
            raise ValueError('Input buses must be readable')

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

        if not isinstance(enable,iBusRead) and not enable is None:
            raise ValueError('If enable bus defined then must be readable')
        elif not enable is None and not enable.size() == 1:
            raise ValueError('Enable bus must be size {}'.format(1))
        self._enable = enable

        if not isinstance(out_bus,iBusWrite) and not out_bus is None:
            raise ValueError('If output bus defined then must be writable')
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
            raise ValueError('Invalid active reset type')
        self._enable_type = enable_type


    def on_rising_edge(self):
        "Implements clock rising behavior: captures data if latching type matches"
        if self._edge_type == Latch_Type.RISING_EDGE or self._edge_type == Latch_Type.BOTH_EDGE:
            self._q = self._d


    def on_falling_edge(self):
        "Implements clock falling behavior: captures data if latching type matches"
        if self._edge_type == Latch_Type.FALLING_EDGE or self._edge_type == Latch_Type.BOTH_EDGE:
            self._q = self._d


    def on_reset(self):
        "Resets the output to default state defined for register"
        self._q = self._default_state


    def inspect(self):
        "Returns dictionary message to user"
        return {'name' : self._name, 'type' : 'register', 'size' : self._size, 'state' : self._q}


    def modify(self,data):
        "Handles message from user to modify memory contents"
        if data is None:
            raise ValueError('Expecting message to be provided')
        elif 'state' not in data:
            raise ValueError('Invalid format for message')

        state = data['state']
        if isinstance(state,int) and state >= 0 and state < 2**self._size:
            self._q = state
        else:
            raise ValueError('Data in message does fit in internal size')


    def run(self,time=None):
        "Timestep handler function clocks data into register and asserts output"
        # receive input from in bud
        self._d = self._in_bus.read()

        #process enable line
        e = True
        if not self._enable is None:
            if self._enable_type == Logic_States.ACTIVE_LOW:
                e = self._enable.read() == 0
            else:
                e = self._enable.read() == 1

        #check for clock change
        if e:
            if self._clock.read() == 1 and self._prev_clock_state == 0:
                self.on_rising_edge()
            elif self._clock.read() == 0 and self._prev_clock_state == 1:
                self.on_falling_edge()
        self._prev_clock_state = self._clock.read()

        #check for reset event
        if self._reset_type == Logic_States.ACTIVE_LOW and self._reset.read() == 0:
            self.on_reset()
        elif self._reset_type == Logic_States.ACTIVE_HIGH and self._reset.read() == 1:
            self.on_reset()

        # assert output for timestep
        if not self._out_bus is None:
            self._out_bus.write(self._q)
