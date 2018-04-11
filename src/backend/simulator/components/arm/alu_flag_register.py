"""
ALU Flag Regsiter stores calculated results from ALU for next state controller
conditions.
"""

from simulator.components.core.bus_join import BusJoin
from simulator.components.core.bus_subset import BusSubset
from simulator.components.core.bus import Bus
from simulator.components.abstract.ibus import iBusRead, iBusWrite
from simulator.components.core.register import Register, Latch_Type, Logic_States


class ALUFlagRegister(Register):
    """
    ALU Flag Register is a specific state register for ARM architecture.
    Developed to simplifiy design by reducing need for join and subset.
    """

    def __init__(self, c_in, v_in, n_in, z_in, rst, clk, en, c_out, v_out, n_out,
                 z_out, default_state=0, edge_type=Latch_Type.RISING_EDGE,
                 reset_type=Logic_States.ACTIVE_HIGH,
                 enable_type=Logic_States.ACTIVE_HIGH):
        """
        Constructor will check for valid parameters, exception thrown on invalid

        Parameters
            c_in: 1-bit input  of 'c'
            v_in: 1-bit input of 'v'
            n_in: 1-bit input of 'n'
            z_in: 1-bit input of 'z'
            rst: Register reset
            clk: Register clock
            en: Register write enable
            c_out: 1-bit output of 'c'
            v_out: 1-bit output of 'v'
            n_out: 1-bit output of 'n'
            z_out: 1-bit output of 'z'

            default_state: Initial 4-bit state of ALU Flag
            edge_type: Clock state change to store flags
            reset_type: Asynchronous reset to default_state value
            enable_type: State to allow write to register
        """

        if not isinstance(c_in,iBusRead) or not c_in.size() == 1:
            raise TypeError('c in must be a 1-bit readable bus')
        if not isinstance(v_in,iBusRead) or not v_in.size() == 1:
            raise TypeError('v in must be a 1-bit readable bus')
        if not isinstance(n_in,iBusRead) or not n_in.size() == 1:
            raise TypeError('n in must be a 1-bit readable bus')
        if not isinstance(z_in,iBusRead) or not z_in.size() == 1:
            raise TypeError('z in must be a 1-bit readable bus')

        if not isinstance(c_out,iBusWrite) or not c_out.size() == 1:
            raise TypeError('c out must be a 1-bit readable bus')
        if not isinstance(v_out,iBusWrite) or not v_out.size() == 1:
            raise TypeError('v out must be a 1-bit readable bus')
        if not isinstance(n_out,iBusWrite) or not n_out.size() == 1:
            raise TypeError('n out must be a 1-bit readable bus')
        if not isinstance(z_out,iBusWrite) or not z_out.size() == 1:
            raise TypeError('z out must be a 1-bit readable bus')

        self._flag_in = Bus(4)
        self._join = BusJoin([c_in, v_in, n_in, z_in], self._flag_in)
        self._flag_out = Bus(4)
        self._subset = BusSubset(self._flag_out, [c_out, v_out, n_out, z_out],
                                 [(0, 1), (1, 2), (2, 3), (3, 4)])

        Register.__init__(self, 4, clk, rst, self._flag_in, self._flag_out,
                          default_state, edge_type, reset_type, en, enable_type)

    def run(self, time=None):
        "Timestep handler function clocks data into register and asserts output"

        self._join.run(time)
        Register.run(self, time)
        self._subset.run(time)

    @classmethod
    def from_dict(cls, config, hooks):
        "Implements conversion from configuration to component"
        return NotImplemented
