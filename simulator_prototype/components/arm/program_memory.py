"""
ARM specific program memory module with 32-bit width.
"""

from components.core.memory import Memory, Latch_Type, Logic_States
from components.core.constant import Constant
from components.core.bus_subset import BusSubset
from components.core.bus import Bus
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

    def __init__(self, address, rst, clk, read, default_size=4096,
                 default_value=0, rst_type=Logic_States.ACTIVE_HIGH):
        """
        Buses
            address : word sized address bus to access program memory
            rst : Reset bus to clear memory
            clk : --ignored but must be valid
            read : word sized bus with addressed instruction

        Configuration
            default_size : size of program memory space in bytes
            default_value : byte value to load into unassigned memory cells
            rst_type : Activation state for reset line
        """
        # disable write behavior
        self._wd_const = Constant(32, 0)
        self._we_const = Constant(1, 0)

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
                        self._we_const, rst, clk, self._mode_const, read, default_value,
                        Latch_Type.FALLING_EDGE, rst_type, Logic_States.ACTIVE_HIGH)

    def run(self, time=None):
        """
        Update address sub-entities before calling general memory run operation
        """
        self._address_subset.run(time)
        Memory.run(self, time)

    @classmethod
    def from_dict(cls, config):
        "Implements conversion from configuration to component"
        return NotImplemented

    @classmethod
    def to_dict(cls):
        "Implements conversion from component to configuration"
        return NotImplemented
