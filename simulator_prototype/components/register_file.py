from components.clock import Clock
from components.reset import Reset
from components.bus import Bus
from components.logic_input import LogicInput
from components.abstract.sequential import Sequential
from enum import Enum

class Register_File(Sequential):

    def __init__(self, name, clock, reset, regwr, wd3, a1, a2, a3, rd1, rd2, size, default_state = 0, edge_type = 'RISING_EDGE', reset_type = 'ACTIVE_LOW'):

        self._name = name
        self._clock = clock
        self._prev_clock_state = clock.read()
        self._reset = reset
        self._regwr = regwr
        self._wd3 = wd3
        self._a1 = a1
        self._a2 = a2
        self._a3 = a3
        self._rd1 = rd1
        self._rd2 = rd2
        self._size = size
        self._default_state = default_state
        self._edge_type = edge_type
        self._reset_type = reset_type

    #TODO
    def on_rising_edge(self):
        pass

    #TODO
    def on_falling_edge(self):
        pass

    #TODO
    def on_reset(self):
        pass

    #TODO
    def inspect(self):
        pass

    #TODO
    def modify(self,data):
        pass

    #TODO 
    def run(self):
        pass