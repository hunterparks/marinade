from components.clock import Clock
from components.reset import Reset
from components.bus import Bus
from components.logic_input import LogicInput
from components.abstract.sequential import Sequential
from enum import Enum

class Register_Edge_Type(Enum):
    LATCH_RISING_EDGE = 0
    LATCH_FALLING_EDGE = 1
    LATCH_BOTH_EDGE = 2

class Register_Reset_Type(Enum):
    RESET_ACTIVE_LOW = 0
    RESET_ACTIVE_HIGH = 1

class Register(Sequential):

    def __init__(self, name, clock, reset, in_bus, out_bus, size, default_state = 0, edge_type = Register_Edge_Type.LATCH_RISING_EDGE, reset_type = Register_Reset_Type.RESET_ACTIVE_LOW):

        self._name = name
        self._clock = clock
        self._prev_clock_state = clock.read()
        self._reset = reset
        self._in_bus = in_bus
        self._out_bus = out_bus
        self._size = size
        self._default_state = default_state
        self._d = default_state
        self._q = default_state
        self._edge_type = edge_type
        self._reset_type = reset_type

    def on_rising_edge(self):
        if self._edge_type == Register_Edge_Type.LATCH_RISING_EDGE or self._edge_type == Register_Edge_Type.LATCH_BOTH_EDGE:
            self._q = self._d

    def on_falling_edge(self):
        if self._edge_type == Register_Edge_Type.LATCH_FALLING_EDGE or self._edge_type == Register_Edge_Type.LATCH_BOTH_EDGE:
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

        #check for clock change
        if self._clock.read() == 1 and self._prev_clock_state == 0:
            self.on_rising_edge()
        elif self._clock.read() == 0 and self._prev_clock_state == 1:
            self.on_falling_edge()
        self._prev_clock_state = self._clock.read()

        #check for reset event
        if self._reset_type == Register_Reset_Type.RESET_ACTIVE_LOW and self._reset.read() == 0:
            self.on_reset()
        elif self._reset_type == Register_Reset_Type.RESET_ACTIVE_HIGH and self._reset.read() == 1:
            self.on_reset()

        # assert output for timestep
        self._out_bus.write(self._q)
