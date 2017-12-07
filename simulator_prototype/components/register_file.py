from components.clock import Clock
from components.reset import Reset
from components.bus import Bus
from components.logic_input import LogicInput
from components.abstract.sequential import Sequential, Edge_Type, Reset_Type
from enum import Enum

#Note to larry I might have broken your code if you continued working on it after
#meeting. I changed the parameter order of register and made some parameters optional that
#were not before (check git changes if it affects you, or slack me)

class Register_File(Sequential):

    def __init__(self, name, clock, reset, write_enable, write_data, a1, a2, a3, rd1, rd2, size, default_state = 0, edge_type = Edge_Type.LATCH_FALLING_EDGE, reset_type = Reset_Type.RESET_ACTIVE_LOW):

        self._name = name
        self._clock = clock
        self._prev_clock_state = clock.read()
        self._reset = reset
        self._write_enable = write_enable
        self._write_data = write_data
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
        if self._edge_type == Edge_Type.LATCH_RISING_EDGE or self._edge_type == Edge_Type.LATCH_BOTH_EDGE:
            

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
