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

class Register_File(Combinational):

    def __init__(self, name, clock, reset, write_enable, write_data, a1, a2, a3, rd1, rd2,
                 edge_type = Latch_Type.FALLING_EDGE, reset_type = Logic_States.ACTIVE_LOW,
                 enable_type = Logic_States.ACTIVE_HIGH):
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
        self._edge_type = edge_type
        self._reset_type = reset_type
        self._enable_type = enable_type
        # output busses from internal registers
        self._data0 = Bus('data0', 32)
        self._data1 = Bus('data1', 32)
        self._data2 = Bus('data2', 32)
        self._data3 = Bus('data3', 32)
        self._data4 = Bus('data4', 32)
        self._data5 = Bus('data5', 32)
        self._data6 = Bus('data6', 32)
        self._data7 = Bus('data7', 32)
        self._data8 = Bus('data8', 32)
        self._data9 = Bus('data9', 32)
        self._data10 = Bus('data10', 32)
        self._data11 = Bus('data11', 32)
        self._data12 = Bus('data12', 32)
        self._data13 = Bus('data13', 32)
        self._data14 = Bus('data14', 32)
        self._data15 = Bus('data15', 32)
         # output bus array
        self._output = [self._data0, self._data1, self._data2, self._data3, self._data4, self._data5,
                        self._data6, self._data7, self._data8, self._data9, self._data10, self._data11,
                        self._data12, self._data13, self._data14, self._data15]
        # initialize registers
        self._r0 = Register('r0', 32, self._clock, self._reset, self._write_data, self._data0, 0,
                      self._edge_type, self._reset_type, self._write_enable, self._enable_type)
        self._r1 = Register('r1', 32, self._clock, self._reset, self._write_data, self._data0, 0,
                      self._edge_type, self._reset_type, self._write_enable, self._enable_type)
        self._r2 = Register('r2', 32, self._clock, self._reset, self._write_data, self._data0, 0,
                      self._edge_type, self._reset_type, self._write_enable, self._enable_type)
        self._r3 = Register('r3', 32, self._clock, self._reset, self._write_data, self._data0, 0,
                      self._edge_type, self._reset_type, self._write_enable, self._enable_type)
        self._r4 = Register('r4', 32, self._clock, self._reset, self._write_data, self._data0, 0,
                      self._edge_type, self._reset_type, self._write_enable, self._enable_type)
        self._r5 = Register('r5', 32, self._clock, self._reset, self._write_data, self._data0, 0,
                      self._edge_type, self._reset_type, self._write_enable, self._enable_type)
        self._r6 = Register('r6', 32, self._clock, self._reset, self._write_data, self._data0, 0,
                      self._edge_type, self._reset_type, self._write_enable, self._enable_type)
        self._r7 = Register('r7', 32, self._clock, self._reset, self._write_data, self._data0, 0,
                      self._edge_type, self._reset_type, self._write_enable, self._enable_type)
        self._r8 = Register('r8', 32, self._clock, self._reset, self._write_data, self._data0, 0,
                      self._edge_type, self._reset_type, self._write_enable, self._enable_type)
        self._r9 = Register('r9', 32, self._clock, self._reset, self._write_data, self._data0, 0,
                      self._edge_type, self._reset_type, self._write_enable, self._enable_type)
        self._r10 = Register('r10', 32, self._clock, self._reset, self._write_data, self._data0, 0,
                      self._edge_type, self._reset_type, self._write_enable, self._enable_type)
        self._r11 = Register('r11', 32, self._clock, self._reset, self._write_data, self._data0, 0,
                      self._edge_type, self._reset_type, self._write_enable, self._enable_type)
        self._r12 = Register('r12', 32, self._clock, self._reset, self._write_data, self._data0, 0,
                      self._edge_type, self._reset_type, self._write_enable, self._enable_type)
        self._r13 = Register('r13', 32, self._clock, self._reset, self._write_data, self._data0, 0,
                      self._edge_type, self._reset_type, self._write_enable, self._enable_type)
        self._r14 = Register('r14', 32, self._clock, self._reset, self._write_data, self._data0, 0,
                      self._edge_type, self._reset_type, self._write_enable, self._enable_type)
        self._r15 = Register('r15', 32, self._clock, self._reset, self._write_data, self._data0, 0,
                      self._edge_type, self._reset_type, self._write_enable, self._enable_type)
        # register array
        self._reg = [self._r0, self._r1, self._r2, self._r3, self._r4, self._r5, self._r6, self._r7,
                     self._r8, self._r9, self._r10, self._r11, self._r12, self._r13, self._r14, self._r15]

    def inspect(self):
        # returns a dictionary message to application defining current state
        return {'name' : self._name, 'type' : 'regfile', 'size' : None, 'state': None}

    def run(self,time=None):
        if self._write_enable.read() == self._enable_type:
            self._reg[self._a3.read()].run()

        self._reg[self._a1.read()].run()
        self._rd1.write(self._output[self._a1.read()].read())
        self._reg[self._a2.read()].run()
        self._rd2.write(self._output[self._a2.read()].read())
