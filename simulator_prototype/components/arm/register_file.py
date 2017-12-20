from components.core.clock import Clock
from components.core.reset import Reset
from components.core.bus import Bus
from components.core.logic_input import LogicInput
from components.abstract.sequential import Sequential, Latch_Type, Logic_States
from components.core.register import Register
from enum import Enum
from components.abstract.combinational import Combinational

#Note to larry I might have broken your code if you continued working on it after
#meeting. I changed the parameter order of register and made some parameters optional that
#were not before (check git changes if it affects you, or slack me)

class Register_File(Sequential):

    def __init__(self, clock, reset, write_enable, write_data, a1, a2, a3, rd1, rd2,
                 edge_type = Latch_Type.FALLING_EDGE, reset_type = Logic_States.ACTIVE_LOW,
                 enable_type = Logic_States.ACTIVE_HIGH):
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
        self._edge_type = edge_type
        self._reset_type = reset_type
        self._enable_type = enable_type
        # output busses from internal registers
        self._data0 = Bus(32)
        self._data1 = Bus(32)
        self._data2 = Bus(32)
        self._data3 = Bus(32)
        self._data4 = Bus(32)
        self._data5 = Bus(32)
        self._data6 = Bus(32)
        self._data7 = Bus(32)
        self._data8 = Bus(32)
        self._data9 = Bus(32)
        self._data10 = Bus(32)
        self._data11 = Bus(32)
        self._data12 = Bus(32)
        self._data13 = Bus(32)
        self._data14 = Bus(32)
        self._data15 = Bus(32)
         # output bus array
        self._output = [self._data0, self._data1, self._data2, self._data3, self._data4, self._data5,
                        self._data6, self._data7, self._data8, self._data9, self._data10, self._data11,
                        self._data12, self._data13, self._data14, self._data15]
        # initialize registers
        self._r0 = Register(32, self._clock, self._reset, self._write_data, self._data0, 0,
                      self._edge_type, self._reset_type, self._write_enable, self._enable_type)
        self._r1 = Register(32, self._clock, self._reset, self._write_data, self._data0, 0,
                      self._edge_type, self._reset_type, self._write_enable, self._enable_type)
        self._r2 = Register(32, self._clock, self._reset, self._write_data, self._data0, 0,
                      self._edge_type, self._reset_type, self._write_enable, self._enable_type)
        self._r3 = Register(32, self._clock, self._reset, self._write_data, self._data0, 0,
                      self._edge_type, self._reset_type, self._write_enable, self._enable_type)
        self._r4 = Register(32, self._clock, self._reset, self._write_data, self._data0, 0,
                      self._edge_type, self._reset_type, self._write_enable, self._enable_type)
        self._r5 = Register(32, self._clock, self._reset, self._write_data, self._data0, 0,
                      self._edge_type, self._reset_type, self._write_enable, self._enable_type)
        self._r6 = Register(32, self._clock, self._reset, self._write_data, self._data0, 0,
                      self._edge_type, self._reset_type, self._write_enable, self._enable_type)
        self._r7 = Register(32, self._clock, self._reset, self._write_data, self._data0, 0,
                      self._edge_type, self._reset_type, self._write_enable, self._enable_type)
        self._r8 = Register(32, self._clock, self._reset, self._write_data, self._data0, 0,
                      self._edge_type, self._reset_type, self._write_enable, self._enable_type)
        self._r9 = Register(32, self._clock, self._reset, self._write_data, self._data0, 0,
                      self._edge_type, self._reset_type, self._write_enable, self._enable_type)
        self._r10 = Register(32, self._clock, self._reset, self._write_data, self._data0, 0,
                      self._edge_type, self._reset_type, self._write_enable, self._enable_type)
        self._r11 = Register(32, self._clock, self._reset, self._write_data, self._data0, 0,
                      self._edge_type, self._reset_type, self._write_enable, self._enable_type)
        self._r12 = Register(32, self._clock, self._reset, self._write_data, self._data0, 0,
                      self._edge_type, self._reset_type, self._write_enable, self._enable_type)
        self._r13 = Register(32, self._clock, self._reset, self._write_data, self._data0, 0,
                      self._edge_type, self._reset_type, self._write_enable, self._enable_type)
        self._r14 = Register(32, self._clock, self._reset, self._write_data, self._data0, 0,
                      self._edge_type, self._reset_type, self._write_enable, self._enable_type)
        self._r15 = Register(32, self._clock, self._reset, self._write_data, self._data0, 0,
                      self._edge_type, self._reset_type, self._write_enable, self._enable_type)
        # register array
        self._reg = [self._r0, self._r1, self._r2, self._r3, self._r4, self._r5, self._r6, self._r7,
                     self._r8, self._r9, self._r10, self._r11, self._r12, self._r13, self._r14, self._r15]

    def inspect(self):
        # returns a dictionary message to application defining current state
        return {'type' : 'regfile', 'size' : None, 'state': None}

    def modify(self):
        raise NotImplementedError()

    def on_rising_edge(self):
        raise NotImplementedError()

    def on_falling_edge(self):
        raise NotImplementedError()

    def on_reset(self):
        raise NotImplementedError()

    def run(self,time=None):

        #NOTE: Shouldn't all registers be ran, only one of them being enabled to write?
        if self._write_enable.read() == self._enable_type:
            self._reg[self._a3.read()].run()

        self._reg[self._a1.read()].run()
        self._rd1.write(self._output[self._a1.read()].read())
        self._reg[self._a2.read()].run()
        self._rd2.write(self._output[self._a2.read()].read())
