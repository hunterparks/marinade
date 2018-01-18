"""
ARM specific program memory module with 32-bit width.
"""

from components.core.memory import Memory, Latch_Type, Logic_States
from components.core.constant import Constant
from components.core.bus_subset import BusSubset
from components.core.bus import Bus
import math

# TODO document and write unit test


class ProgramMemory(Memory):
    """
    ARM specific program memory with 32-bit word size. This component is to be
    used for storing a program in an architecture. Note that this device does
    not allow writes from inside the architecture.

    Note to program this memory use the modify functionality.
    """

    def __init__(self, address, rst, clk, read, default_size=4096,
                 default_value=0, edge_type=Latch_Type.FALLING_EDGE,
                 rst_type=Logic_States.ACTIVE_HIGH,
                 memwr_type=Logic_States.ACTIVE_HIGH):
        """

        """
        # disable write behavior
        self._wd_const = Constant(32, 0)
        self._we_const = Constant(1, 0)

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
                        self._we_const, rst, clk, read, default_value, edge_type,
                        rst_type, memwr_type)

    def run(self, time=None):
        """
        Update address sub-entities before calling general memory run operation
        """
        self._address_subset.run(time)
        Memory.run(self, time)
