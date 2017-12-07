from components.abstract.ibus import iBusRead, iBusWrite
from components.clock import Clock
from components.reset import Reset
from components.bus import Bus
from components.logic_input import LogicInput
from components.abstract.sequential import Sequential, Latch_Type, Logic_States

class Register(Sequential):

    #TODO enforce bus size rules
    def __init__(self, name, size, clock, reset, in_bus, out_bus = None, default_state = 0, edge_type = Latch_Type.RISING_EDGE, reset_type = Logic_States.ACTIVE_LOW, enable = None, enable_type = Logic_States.ACTIVE_HIGH):
        if not isinstance(name,str) or size <= 0 or default_state < 0 or default_state >= 2**size:
            raise ValueError('Initialization parameters invalid')
        self._name = name
        self._size = size
        self._default_state = default_state
        self._d = default_state
        self._q = default_state

        if not isinstance(clock,iBusRead) or not isinstance(reset,iBusRead) or not isinstance(in_bus,iBusRead):
            raise ValueError('Input buses must be readable')
        self._clock = clock
        self._prev_clock_state = clock.read()
        self._reset = reset
        self._in_bus = in_bus

        if not isinstance(enable,iBusRead) and not enable is None:
            raise ValueError('If enable bus defined then must be readable')
        self._enable = enable

        if not isinstance(out_bus,iBusWrite) and not out_bus is None:
            raise ValueError('If output bus defined then must be writable')
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

    #TODO do check on size to prevent larger than allowed values
    def on_rising_edge(self):
        if self._edge_type == Latch_Type.RISING_EDGE or self._edge_type == Latch_Type.BOTH_EDGE:
            self._q = self._d

    #TODO do check on size to prevent larger than allowed values
    def on_falling_edge(self):
        if self._edge_type == Latch_Type.FALLING_EDGE or self._edge_type == Latch_Type.BOTH_EDGE:
            self._q = self._d

    def on_reset(self):
        self._q = self._default_state

    def inspect(self):
        return {'name' : self._name, 'type' : 'register', 'size' : self._size, 'state' : self._q}

    #TODO write this function so that user can modify internal contents of register
    def modify(self,data):
        pass

    def run(self):
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
