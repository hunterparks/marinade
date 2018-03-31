"""
Generalized register file defines addressable set of registers
"""

from simulator.components.core.bus import Bus, iBusRead, iBusWrite
from simulator.components.core.register import Sequential, Register, Latch_Type, Logic_States
import math


class RegisterFile(Sequential):
    """
    Register File component implements a set of registers with a single
    write input and a set of read outputs. All outputs and input correspond
    to an address to select which register to use.

    Component is sequential and thus requires a clock and reset to operate
    """

    def __init__(self, num_reg, reg_size, clock, reset, write_addr, write_data,
                 read_addrs, read_datas, enable=None, default_state=0,
                 edge_type=Latch_Type.RISING_EDGE,
                 reset_type=Logic_States.ACTIVE_HIGH,
                 enable_type=Logic_States.ACTIVE_HIGH):
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

        # configuration
        if not isinstance(reg_size, int) or reg_size <= 0:
            raise TypeError('Number of registers must be valid integer')
        elif not isinstance(num_reg, int) or num_reg <= 0:
            raise TypeError('Bit-width must be valid')
        elif not Latch_Type.valid(edge_type):
            raise ValueError('Invalid latch edge type')
        elif not Logic_States.valid(reset_type):
            raise ValueError('Invalid active reset type')
        elif not Logic_States.valid(enable_type):
            raise ValueError('Invalid active enable type')

        self._reg_size = reg_size
        self._num_reg = num_reg
        self._edge_type = edge_type
        self._reset_type = reset_type
        self._enable_type = enable_type

        # generate necessary parameters that buses must fit
        if num_reg == 0:
            self._necessary_length = 0
        elif num_reg < 2:
            self._necessary_length = 1
        else:  # len > 2
            self._necessary_length = int(math.floor(math.log(num_reg - 1, 2) + 1))
        self._necessary_size = self._reg_size

        # external connections
        if not isinstance(clock, iBusRead) or not clock.size() == 1:
            raise TypeError('Clock bus must be valid')
        elif not isinstance(reset, iBusRead) or not reset.size() == 1:
            raise TypeError('Reset bus must be valid')
        elif not isinstance(enable, iBusRead) or not enable.size() == 1:
            raise TypeError('Write enable bus must be readable')
        elif not isinstance(write_addr, iBusRead) or not write_addr.size() == self._necessary_length:
            raise TypeError('Write address bus must be readable')
        elif not isinstance(write_data, iBusRead) or not write_data.size() == self._necessary_size:
            raise TypeError('Write data bus must be readable')
        elif not isinstance(read_addrs, list) or not isinstance(read_datas, list):
            raise TypeError('Read buses lists must be list')
        elif not (len(read_addrs) == len(read_datas)) or len(read_addrs) <= 0 or len(read_datas) <= 0:
            raise TypeError('Read buses must having matching size greater than zero')
        elif not all((isinstance(x, iBusRead) and x.size() == self._necessary_length) for x in read_addrs):
            raise TypeError('Read address buses must be have correct size')
        elif not all((isinstance(x, iBusWrite) and x.size() == self._necessary_size) for x in read_datas):
            raise TypeError('Read data buses must be have correct size')

        self._clock = clock
        self._reset = reset
        self._enable = enable
        self._waddr = write_addr
        self._wdata = write_data
        self._raddrs = read_addrs
        self._rdatas = read_datas

        # internal structure
        self._regs = []
        self._ens = []
        self._datas = []

        for i in range(num_reg):
            en = Bus(1, 0)
            da = Bus(reg_size, 0)
            self._ens.append(en)
            self._datas.append(da)
            self._regs.append(Register(reg_size, clock, reset, write_data, da,
                                       default_state, edge_type, reset_type, en,
                                       Logic_States.ACTIVE_HIGH))

    def inspect(self):
        "Returns dictionary message to user"
        states = []
        for r in self._regs:
            states.append(r.inspect()['state'])

        return {
            'type': 'register',
            'length': self._num_reg,  # number of elements
                    'size': self._reg_size,  # bit size of register
                    'state': states  # array of all register output values
        }

    def modify(self, message):
        "Handles message from user to modify memory contents"

        if message is None:
            return {'error': 'expecting message to be provided'}
        elif 'data' not in message or 'start' not in message:
            return {'error': 'invalid format for message'}
        start = message['start']
        data = message['data']

        if not isinstance(start, int) or start < 0 or start >= self._num_reg:
            return {'error': 'start index must be an integer in valid range'}
        elif not isinstance(data, list):
            return {'error': 'data must be a list of integers'}
        elif (len(data) + start) > self._num_reg:
            return {'error': 'address rolloever not supported'}
        else:
            retval = {}
            for i in range(0, len(data)):
                tm = {'state': data[i]}
                rm = self._regs[i + start].modify(tm)
                if 'error' in rm:
                    if 'error' not in retval:
                        retval.update({'error': []})
                    retval['error'].append('r{}: {}'.format(i, rm['error']))
            if 'error' not in retval:
                retval.update({'success': True})
            return retval

    def clear(self):
        "Hook method to clear memory, thereby returning it to default value"
        self.on_reset()
        return {'success': True}

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

    def run(self, time=None):
        "Timestep handler function routes write and read data from registers"
        # process enable line
        e = True
        if not self._enable is None:
            if self._enable_type == Logic_States.ACTIVE_LOW:
                e = self._enable.read() == 0
            else:
                e = self._enable.read() == 1

        # write data to register
        if e:
            a = self._waddr.read()
            if a < self._num_reg:
                self._ens[a].write(1)

        # check for reset event
        if self._reset_type == Logic_States.ACTIVE_LOW and self._reset.read() == 0:
            self.on_reset()
        elif self._reset_type == Logic_States.ACTIVE_HIGH and self._reset.read() == 1:
            self.on_reset()

        # run registers
        for r in self._regs:
            r.run(time)

        # read from registers and assert output
        for i in range(len(self._raddrs)):
            a = self._raddrs[i].read()
            if a < self._num_reg:
                self._rdatas[i].write(self._datas[a].read())
            else:
                self._rdatas[i].write(0)

        # clear enable flags for register selected
        if e:
            a = self._waddr.read()
            if a < self._num_reg:
                self._ens[a].write(0)

    @classmethod
    def from_dict(cls, config):
        "Implements conversion from configuration to component"
        return NotImplemented

    def to_dict(self):
        "Implements conversion from component to configuration"
        return NotImplemented
