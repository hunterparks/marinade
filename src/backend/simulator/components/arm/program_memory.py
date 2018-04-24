"""
ARM specific program memory module with 32-bit width.
"""

from simulator.components.core.memory import Memory, Latch_Type, Logic_States
from simulator.components.core.constant import Constant
from simulator.components.core.bus_subset import BusSubset
from simulator.components.core.bus import Bus
import math


class ProgramMemory(Memory):
    """
    ARM specific program memory with 32-bit word size. This component is to be
    used for storing a program in an architecture. Note that this device does
    not allow writes from inside the architecture.

    Note to program this memory use the modify functionality.

    Note that address space is ghosted if the address bus is greater than the
    size defined for the module.
    """

    DEFAULT_SIZE = 4096
    DEFAULT_STATE = 0
    DEFAULT_RESET_TYPE = Logic_States.ACTIVE_HIGH

    def __init__(self, address, rst, read, default_size=DEFAULT_SIZE,
                 default_value=DEFAULT_STATE, rst_type=DEFAULT_RESET_TYPE):
        """
        Buses
            address : word sized address bus to access program memory
            rst : Reset bus to clear memory
            read : word sized bus with addressed instruction

        Configuration
            default_size : size of program memory space in bytes
            default_value : byte value to load into unassigned memory cells
            rst_type : Activation state for reset line
        """
        # disable write behavior
        self._wd_const = Constant(32, 0)
        self._we_const = Constant(1, 0)
        self._clk_const = Constant(1,0)

        # default mode to word access
        self._mode_const = Constant(2, 3)

        # ghost memory on bus to lower needed bits
        if default_size == 0:
            size = 0
        elif default_size < 2:
            size = 1
        else:  # len > 2
            size = int(math.floor(math.log(default_size - 1, 2) + 1))

        self._address_general = Bus(size)
        self._address_subset = BusSubset(address, [self._address_general], [(0, size)])

        # Construct generalized memory passing parameters
        Memory.__init__(self, default_size, 4, 0, self._address_general, self._wd_const,
                        self._we_const, rst, self._clk_const, self._mode_const, read, default_value,
                        Latch_Type.FALLING_EDGE, rst_type, Logic_States.ACTIVE_HIGH)

    def run(self, time=None):
        """
        Update address sub-entities before calling general memory run operation
        """
        self._address_subset.run(time)
        Memory.run(self, time)

    @classmethod
    def from_dict(cls, config, hooks):
        "Implements conversion from configuration to component"

        if "size" in config:
            size = config["size"]
        else:
            size = ProgramMemory.DEFAULT_SIZE

        if "value" in config:
            value = config["value"]
        else:
            value = ProgramMemory.DEFAULT_STATE

        if "reset_type" in config:
            reset_type = Logic_States.fromString(config["reset_type"])
        else:
            reset_type = ProgramMemory.DEFAULT_RESET_TYPE

        return ProgramMemory(hooks[config["address"]],hooks[config["reset"]],
                             hooks[config["read"]],size,value,reset_type)
