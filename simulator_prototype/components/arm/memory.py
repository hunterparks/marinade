"""
ARM memory object for use in ARMv4 architecture
"""

# TODO maybe we should generalize this class (-> Core) and then produce datamem and progmem components (-> arm)

from components.abstract.ibus import iBusRead, iBusWrite
from components.abstract.memory_block import MemoryBlock, Latch_Type, Logic_States
import limits


class Memory(MemoryBlock):
    """
    Memory object provides addressable memory storage/access for an architecture.
    This memory assumes full range of address space (2^32). Additionally, this
    module has a word size of 32 bits and data is written in words (not bytes).
    Finally, the default state is not zero, rather it takes on a value of
    0x81818181.
    """

    def __init__(self, a, wd, memwr, rst, clk, rd, edge_type=Latch_Type.FALLING_EDGE,
                 rst_type=Logic_States.ACTIVE_LOW, memwr_type=Logic_States.ACTIVE_LOW):
        """
        inputs:
            a: memory address
            wd: data to be written to memory
            memwr: control signal used to all memory to be written to
            rst: clears all assigned memory
            clk: input clock
        outputs:
            rd: output of memory that was read from

        edge_type: memory data latch type
        rst_type: memory reset signal active state
        memwr_type : memory write enable active state
        """

        if not isinstance(a, iBusRead):
            raise TypeError('The a bus must be readable')
        elif a.size() != 32:
            raise ValueError('The a bus must have a size of 32 bits')
        if not isinstance(wd, iBusRead):
            raise TypeError('The wd bus must be readable')
        elif wd.size() != 32:
            raise ValueError('The wd bus must have a size of 32 bits')
        if not isinstance(memwr, iBusRead):
            raise TypeError('The memwr bus must be readable')
        elif memwr.size() != 1:
            raise ValueError('The memwr bus must have a size of 1 bit')
        if not isinstance(rst, iBusRead):
            raise TypeError('The rst bus must be readable')
        elif rst.size() != 1:
            raise ValueError('The rst bus must have a size of 1 bit')
        if not isinstance(clk, iBusRead):
            raise TypeError('The clk bus must be readable')
        elif clk.size() != 1:
            raise ValueError('The clk bus must have a size of 1 bit')
        if not isinstance(rd, iBusWrite):
            raise TypeError('The rd must must be writable')
        elif rd.size() != 32:
            raise ValueError('The rd bus must have a size of 32 bits')
        if not Latch_Type.valid(edge_type):
            raise ValueError('Invalid latch edge type')
        if not Logic_States.valid(rst_type):
            raise ValueError('Invalid rst state')
        if not Logic_States.valid(memwr_type):
            raise ValueError('Invalid memwr state')

        self._a = a
        self._wd = wd
        self._memwr = memwr
        self._rst = rst
        self._clk = clk
        self._prev_clk_state = self._clk.read()
        self._rd = rd
        self._edge_type = edge_type
        self._rst_type = rst_type
        self._memwr_type = memwr_type
        self._assigned_memory = {}

    def on_rising_edge(self):
        """
        implements clock rising behavior: captures data if latching type matches
        """
        if self._edge_type == Latch_Type.RISING_EDGE or self._edge_type == Latch_Type.BOTH_EDGE:
            self._assigned_memory[self._a.read()] = self._wd.read()

    def on_falling_edge(self):
        """
        implements clock falling behavior: captures data if latching type matches
        """
        if self._edge_type == Latch_Type.FALLING_EDGE or self._edge_type == Latch_Type.BOTH_EDGE:
            self._assigned_memory[self._a.read()] = self._wd.read()

    def on_reset(self):
        """
        wipes out all memory
        """
        self._assigned_memory = {}

    def inspect(self):
        """
        returns dictionary message to user
        """
        # TODO printout memory when inspected
        return {'type': 'memory', 'size': len(self._assigned_memory)}

    def modify(self, message):
        """
        allows for memory modification outside of the normal program flow
        """
        # TODO this needs to return a JSON not an error

        if 'start' not in message or 'data' not in message:
            raise ValueError(
                'The message argurment must be a dictionary that includes a "start" key and a "data" key')
        start_address = message['start']
        modified_memory = message['data']
        offset = 0
        for data in modified_memory:
            self._assigned_memory[start_address + offset] = data
            # TODO this needs to account for rollover for fixed size memory
            offset = offset + 4

    def view_memory_address(self, address):
        """
        used to view a 32-bit memory address (used for testing purposes only)
        """
        if address not in self._assigned_memory:
            return 0x81818181
        else:
            return self._assigned_memory[address]

    def run(self, time=None):
        """
        allows the memory to operatate during normal program execution
        """
        # write is synchronous
        if self._memwr.read() == 1:
            if self._clk.read() == 1 and self._prev_clk_state == 0:
                self.on_rising_edge()
            elif self._clk.read() == 0 and self._prev_clk_state == 1:
                self.on_falling_edge()
        self._prev_clk_state = self._clk.read()

        # read is asynchronous
        if self._a.read() not in self._assigned_memory:
            # unassinged memory is set to 0x81818181
            self._rd.write(0x81818181)
        else:
            self._rd.write(self._assigned_memory[self._a.read()])
