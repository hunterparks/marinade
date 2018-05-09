"""
ALU Flag Regsiter stores calculated results from ALU for next state controller
conditions.

Configuration file template should follow form
{
    /* Required */

    "name" : "alu_flag_register",
    "type" : "AluFlagRegister",
    "c_in" : "",
    "v_in" : "",
    "n_in" : "",
    "z_in" : "",
    "reset" : "",
    "clock" : "",
    "enable" : "",
    "c_out" : "",
    "v_out" : "",
    "n_out" : "",
    "z_out" : "",

    /* Optional */

    "package" : "arm",
    "append_to_signals" : true,
    "value" : 0,
    "edge_type" : "",
    "reset_type" : "",
    "enable_type" : ""
}

name is the entity name, used by entity map (Used externally)
type is the component class (Used externally)
package is associated package to override general (Used externally)
append_to_signals is flag used to append an entity as hook (Used externally)
c_in is data bus reference
v_in is data bus reference
n_in is data bus reference
z_in is data bus reference
clock is control bus clock line reference
reset is control bus reset line reference
enable is write control bus reference
c_out is data bus reference
v_out is data bus reference
n_out is data bus reference
z_out is data bus reference
value is default value of a byte in memory
edge_type is edge to clock data
reset_type is logic level to clear memory
enable_type is logic level to write to memory
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

    DEFAULT_STATE = 0
    DEFAULT_LATCH_TYPE = Latch_Type.RISING_EDGE
    DEFAULT_RESET_TYPE = Logic_States.ACTIVE_HIGH
    DEFAULT_ENABLE_TYPE = Logic_States.ACTIVE_HIGH

    def __init__(self, c_in, v_in, n_in, z_in, rst, clk, en, c_out, v_out, n_out,
                 z_out, default_state=DEFAULT_STATE, edge_type=DEFAULT_LATCH_TYPE,
                 reset_type=DEFAULT_RESET_TYPE, enable_type=DEFAULT_ENABLE_TYPE):
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

        if not isinstance(c_in, iBusRead) or not c_in.size() == 1:
            raise TypeError('c in must be a 1-bit readable bus')
        if not isinstance(v_in, iBusRead) or not v_in.size() == 1:
            raise TypeError('v in must be a 1-bit readable bus')
        if not isinstance(n_in, iBusRead) or not n_in.size() == 1:
            raise TypeError('n in must be a 1-bit readable bus')
        if not isinstance(z_in, iBusRead) or not z_in.size() == 1:
            raise TypeError('z in must be a 1-bit readable bus')

        if not isinstance(c_out, iBusWrite) or not c_out.size() == 1:
            raise TypeError('c out must be a 1-bit readable bus')
        if not isinstance(v_out, iBusWrite) or not v_out.size() == 1:
            raise TypeError('v out must be a 1-bit readable bus')
        if not isinstance(n_out, iBusWrite) or not n_out.size() == 1:
            raise TypeError('n out must be a 1-bit readable bus')
        if not isinstance(z_out, iBusWrite) or not z_out.size() == 1:
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

        if "value" in config:
            default_state = config["value"]
        else:
            default_state = ALUFlagRegister.DEFAULT_STATE

        if "edge_type" in config:
            edge_type = Latch_Type.fromString(config["edge_type"])
        else:
            edge_type = ALUFlagRegister.DEFAULT_LATCH_TYPE

        if "reset_type" in config:
            reset_type = Logic_States.fromString(config["reset_type"])
        else:
            reset_type = ALUFlagRegister.DEFAULT_RESET_TYPE

        if "enable_type" in config:
            enable_type = Logic_States.fromString(config["enable_type"])
        else:
            enable_type = ALUFlagRegister.DEFAULT_ENABLE_TYPE

        return ALUFlagRegister(hooks[config["c_in"]], hooks[config["v_in"]], hooks[config["n_in"]],
                               hooks[config["z_in"]], hooks[config["reset"]], hooks[config["clock"]],
                               hooks[config["enable"]], hooks[config["c_out"]], hooks[config["v_out"]],
                               hooks[config["n_out"]], hooks[config["z_out"]], default_state, edge_type,
                               reset_type, enable_type)
