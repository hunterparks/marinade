"""
ARM specific data memory module with 32-bit width.
"""

from simulator.components.core.memory import Memory, Latch_Type, Logic_States
from simulator.components.core.bus_subset import BusSubset
from simulator.components.core.bus import Bus
from simulator.components.core.constant import Constant
import math


class DataMemory(Memory):
    """
    ARM specific data memory with 32-bit word size. Thsi component is to be used
    to store data during execution of architecture.

    Note to change state during operation, use modify functionality.

    Note that address space is ghosted if the address bus is greater than the
    size defined for the module.
    """

    def __init__(self, address, write, writeEnable, reset, clock, read,
                 mode=None, default_size=4096, default_value=0x81,
                 edge_type=Latch_Type.FALLING_EDGE,
                 rst_type=Logic_States.ACTIVE_HIGH,
                 memwr_type=Logic_States.ACTIVE_HIGH):
        """
        Buses
            address : bus of size at least as large as size to map to cells
            write : word sized bus (32-bit) to write to addressed cell
            writeEnable : enable line to save write data to memory on clock edge
            reset : System reset line to clear memory
            clock: System clock line to store memory
            read : word sized bus (32-bit) to read from addressed cell
            mode : 2-bit bus signaling read type of memory
                        0 = memory off (return 0) (no write)
                        1 = byte access (read/write ignores upper bits)
                        2 = half-word access (read/write ignores upper bits)
                        3 = word access (default)

        Configuration
            default_size : size of program memory space in bytes
            default_value : byte value to load into unassigned memory cells
            edge_type : Store data on this clock edge
            rst_type : Activation state for reset line
            memwr_type : Activation state for storing on write clock edge
        """
        #handle optional accessMode bus
        if mode is None:
            mode = Constant(2, 3)

        # ghost memory on bus to lower needed bits
        if default_size < 0:
            raise ValueError('Size must be within valid range')
        elif default_size == 0:
            size = 0
        elif default_size < 2:
            size = 1
        else:  # len > 2
            size = int(math.floor(math.log(default_size - 1, 2) + 1))

        self._address_general = Bus(size)
        self._address_subset = BusSubset(address, [self._address_general], [(0, size)])

        # Construct generalized memory passing parameters
        Memory.__init__(self, default_size, 4, 0, self._address_general, write,
                        writeEnable, reset, clock, mode, read,
                        default_value, edge_type, rst_type, memwr_type)

    def run(self, time=None):
        """
        Update address sub-entities before calling general memory run operation
        """
        self._address_subset.run(time)
        Memory.run(self, time)

    @classmethod
    def from_dict(cls, config, hooks):
        "Implements conversion from configuration to component"
        return NotImplemented
