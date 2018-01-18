"""
Core memory object for generalized data memory usage.
"""

from components.abstract.ibus import iBusRead, iBusWrite
from components.abstract.memory_block import MemoryBlock, Latch_Type, Logic_States
import limits


class Memory(MemoryBlock):
    """
    Memory object provides addressable memory storage/access for an architecture.
    This is a generalized memory with constrained data size, word-size and
    default value.

    Note that this component assumes byte addressing
    """

    def __init__(self, size, bitWidth, startingAddress, address, write,
                 writeEnable, reset, clock, read, default_value=0,
                 edge_type=Latch_Type.FALLING_EDGE,
                 reset_type=Logic_States.ACTIVE_LOW,
                 writeEnable_type=Logic_States.ACTIVE_LOW):
        """
        size : Number of words in the system.
        bitWidth : Must be a multiple of a byte and greater than zero.
                    (for example placing a 1 is 8-bit word,
                    placing a 2 is 16-bit word)
        startingAddress : Must be an integer that defines first address. Last
                          address is infered from size and bitwidth

        inputs:
            address: memory address
            write: data to be written to memory
            writeEnable: control signal used to all memory to be written to
            reset: clears all assigned memory
            clock: input clock
        outputs:
            read: output of memory that was read from

        edge_type: memory data latch type
        reset_type: memory reset signal active state
        writeEnable_type : memory write enable active state
        """

        # check sizing configuration
        if not isinstance(size, int):
            raise TypeError('Size must be an integer type')
        elif size < limits.MIN_MEMORY_BLOCK or size > limits.MAX_MEMORY_BLOCK:
            raise ValueError('Size must fit within memory limits')
        if not isinstance(bitWidth, int):
            raise TypeError('Bitwidth must be an integer type')
        elif bitWidth <= 0 or bitWidth >= limits.MAX_BYTES_IN_WORD:
            raise ValueError('Bitwidth must fit within limits')
        if not isinstance(default_value, int):
            raise TypeError('Default value must be an integer')
        elif default_value < 0 or default_value > (8 * bitWidth):
            raise ValueError('Default value out of range')
        if not isinstance(startingAddress, int):
            raise TypeError('Starting address must be an integer')
        elif startingAddress < limits.MIN_ADDRESS or startingAddress > limits.MAX_ADDRESS:
            raise ValueError('Starting address must fit within limits')
        elif startingAddress + size * bitWidth > limits.MAX_ADDRESS:
            raise ValueError('Ending address must fit within limits')
        if not Latch_Type.valid(edge_type):
            raise ValueError('Invalid latch edge type')
        if not Logic_States.valid(reset_type):
            raise ValueError('Invalid reset state')
        if not Logic_States.valid(writeEnable_type):
            raise ValueError('Invalid write enable state')

        self._size = size
        self._bitWidth = bitWidth * 8
        self._default_value = default_value
        self._start_address = startingAddress
        self._end_address = startingAddress + size * bitWidth
        self._edge_type = edge_type
        self._reset_type = reset_type
        self._writeEnable_type = writeEnable_type

        # check buses
        if not isinstance(address, iBusRead):
            raise TypeError('The address bus must be readable')
        elif address.size() != self._bitWidth:
            raise ValueError('The address bus must have a size of 32 bits')
        if not isinstance(write, iBusRead):
            raise TypeError('The write bus must be readable')
        elif write.size() != self._bitWidth:
            raise ValueError('The write bus must have a size of 32 bits')
        if not isinstance(writeEnable, iBusRead):
            raise TypeError('The writeEnable bus must be readable')
        elif writeEnable.size() != 1:
            raise ValueError('The writeEnable bus must have a size of 1 bit')
        if not isinstance(reset, iBusRead):
            raise TypeError('The reset bus must be readable')
        elif reset.size() != 1:
            raise ValueError('The reset bus must have a size of 1 bit')
        if not isinstance(clock, iBusRead):
            raise TypeError('The clock bus must be readable')
        elif clock.size() != 1:
            raise ValueError('The clock bus must have a size of 1 bit')
        if not isinstance(read, iBusWrite):
            raise TypeError('The read must must be writable')
        elif read.size() != self._bitWidth:
            raise ValueError('The read bus must have a size of 32 bits')

        self._address = address
        self._write = write
        self._writeEnable = writeEnable
        self._reset = reset
        self._clock = clock
        self._prev_clock_state = self._clock.read()
        self._read = read

        # define memory space
        self._assigned_memory = {}

    def on_rising_edge(self):
        """
        implements clock rising behavior: captures data if latching type matches
        """
        address = self._address.read()
        if self._edge_type == Latch_Type.RISING_EDGE or self._edge_type == Latch_Type.BOTH_EDGE:
            if address >= self._start_address and address <= self._end_address:
                self._assigned_memory[address] = self._write.read()

    def on_falling_edge(self):
        """
        implements clock falling behavior: captures data if latching type matches
        """
        address = self._address.read()
        if self._edge_type == Latch_Type.FALLING_EDGE or self._edge_type == Latch_Type.BOTH_EDGE:
            if address >= self._start_address and address < self._end_address:
                self._assigned_memory[address] = self._write.read()

    def on_reset(self):
        """
        wipes out all memory
        """
        self._assigned_memory = {}

    def inspect(self):
        """
        returns dictionary message to user
        """
        return {'type': 'memory', 'size': self._size, 'state': self._assigned_memory}

    def modify(self, message):
        """
        allows for memory modification outside of the normal program flow
        """
        if message is None:
            return {'error': 'expecting message to be provided'}
        elif 'data' not in message or 'start' not in message:
            return {'error': 'invalid format for message'}
        start = message['start']
        data = message['data']

        if not isinstance(start, int) or start < self._start_address or start >= self._end_address:
            return {'error': 'start address must be an integer in valid range'}
        elif not isinstance(data, list):
            return {'error': 'data must be a list of integers'}
        elif (len(data) + self._start_address) > self._end_address:
            return {'error': 'address rollover not supported'}
        else:
            for i in range(0, len(data)):
                self._assigned_memory[start + (i * self._bitWidth)] = data[i]
            return {'succes': True}

    def run(self, time=None):
        """
        allows the memory to operatate during normal program execution
        """
        # write is synchronous
        if self._writeEnable.read() == 1:
            if self._clock.read() == 1 and self._prev_clock_state == 0:
                self.on_rising_edge()
            elif self._clock.read() == 0 and self._prev_clock_state == 1:
                self.on_falling_edge()
        self._prev_clock_state = self._clock.read()

        # read is asynchronous
        if self._address.read() not in self._assigned_memory:
            # unassinged memory has a default_value
            self._read.write(self._default_value)
        else:
            self._read.write(self._assigned_memory[self._address.read()])
