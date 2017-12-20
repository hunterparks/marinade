"""

"""

from components.core.clock import Clock
from components.core.reset import Reset
from components.core.bus import Bus
from components.core.logic_input import LogicInput
from components.abstract.sequential import Sequential, Latch_Type, Logic_States
from components.core.register import Register
from enum import Enum
from components.abstract.combinational import Combinational

class RegisterFile(Sequential):
    """

    """

    def __init__(self, num_reg, reg_size, clock, reset, write_addr, write_data, read_addrs, read_datas, enable=None,
            default_state = 0,edge_type = Latch_Type.FALLING_EDGE, reset_type = Logic_States.ACTIVE_LOW,enable_type = Logic_States.ACTIVE_HIGH):
        """
            Constructor will check for valid parameters, exception thrown on invalid

            Parameters:
                num_reg : number of registers in register file
                reg_size : bit size of registers in register file
                clock : clock bus of size 1 for register file
                reset : reset bus of size 1 for register file
                write_addr : write address of iBusRead size appropriate for num_reg
                write_data : write address of iBusRead size appropriate for reg_size
                read_addr : read address array of iBusRead with no more than num_reg
                            each bus must be of size appropriate for reg selection
                read_data : read data array of iBusWrite with no more than num_reg
                            each bus must have size equal to reg_size
                enable : bit enabling write behavior for specified registers
                         (Optional) if not specified then assumed active
                default_state : initial and reset state that registers take on
                edge_type : Latching type for registers (all must be same)
                reset_type : logic state to cause reset event
                enable_type : logic state to allow write behavior
        """

        #TODO error checking

        #external connections
        self._reset = reset
        self._enable = enable
        self._waddr = write_addr
        self._wdata = write_data
        self._raddrs = read_addrs
        self._rdatas = read_datas

        #configuration
        self._edge_type = edge_type
        self._reset_type = reset_type
        self._enable_type = enable_type
        self._reg_size = reg_size
        self._num_reg = num_reg

        #internal structure
        self._regs = []
        self._ens = []
        self._datas = []

        for i in range(num_reg):
            en = Bus(1,0)
            da = Bus(reg_size,0)
            self._ens.append(en)
            self._datas.append(da)
            self._regs.append(Register(reg_size,clock,reset,write_data,da,
                              default_state,edge_type,reset_type,en,Logic_States.ACTIVE_HIGH))


    def inspect(self):
        "Returns dictionary message to user"
        states = []
        for d in self._datas:
            states.append(d.read())

        return {
                    'type' : 'register',
                    'length' : self._num_reg, # number of elements
                    'size' : self._reg_size, # bit size of register
                    'state': states # array of all register output values
               }


    def modify(self):
        "Handles message from user to modify memory contents"
        raise NotImplementedError()


    def on_rising_edge(self):
        "Not useful since enable bit is inactive but triggers rising edge on all"
        for r in self._regs:
            r.on_rising_edge()


    def on_falling_edge(self):
        "Not useful since enable bit is inactive but triggers falling edge on all"
        for r in self._regs:
            r.on_falling_edge()


    def on_reset(self):
        "Triggers reset on all"
        for r in self._regs:
            r.on_reset()


    def run(self,time=None):
        "Timestep handler function routes write and read data from registers"
        #process enable line
        e = True
        if not self._enable is None:
            if self._enable_type == Logic_States.ACTIVE_LOW:
                e = self._enable.read() == 0
            else:
                e = self._enable.read() == 1

        #write data to register
        if e:
            self._ens[self._waddr.read()].write(1)

        #check for reset event
        if self._reset_type == Logic_States.ACTIVE_LOW and self._reset.read() == 0:
            self.on_reset()
        elif self._reset_type == Logic_States.ACTIVE_HIGH and self._reset.read() == 1:
            self.on_reset()

        #run registers
        for r in self._regs:
            r.run(time)

        #read from registers and assert output
        for i in range(len(self._raddrs)):
            self._rdatas[i].write(self._datas[self._raddrs[i].read()].read())

        #clear enable flags for register selected
        if e:
            self._ens[self._waddr.read()].write(0)
