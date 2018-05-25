"""
Core memory object for generalized data memory usage.

Configuration file template should follow form
{
    /* Required */

    "size" : 64,
    "bytes_per_word" : 4,
    "start_address" : 0,
    "address" : "",
    "write" : "",
    "enable" : "",
    "reset" : "",
    "clock" : "",
    "access_mode" : "",
    "read" : "",

    /* Optional */

    "append_to_signals" : true,
    "value" : 0,
    "edge_type" : "",
    "reset_type" : "",
    "enable_type" : ""
}

append_to_signals is flag used to append an entity as hook (Used externally)
size is number of bytes in memory
bytes_per_word is number of bytes considered as one word for word access mode
start_address is the first address that has a byte associated with it
address is bus reference to memory element to read / write
write is the data bus reference to store into memory
enable is write control bus reference
reset is control bus reset line reference
clock is control bus clock line reference
access_mode is control bus selecting memory access type
read is data bus reference to read from memory
value is default value of a byte in memory
edge_type is edge to clock data
reset_type is logic level to clear memory
enable_type is logic level to write to memory
"""

import math

import simulator.limits as limits

from simulator.components.abstract.ibus import iBusRead, iBusWrite
from simulator.components.abstract.memory_block import MemoryBlock, Latch_Type, Logic_States


class Memory(MemoryBlock):
    """
    Memory object provides addressable memory storage/access for an architecture.
    This is a generalized memory with constrained data size, word-size and
    default value.

    Note that this component assumes byte addressing,
    Note that this component assumes big-endian word storage
    """

    MEM_MODE_OFF = 0
    MEM_MODE_BYTE = 1
    MEM_MODE_HALF = 2
    MEM_MODE_WORD = 3

    DEFAULT_STATE = 0
    DEFAULT_LATCH_TYPE = Latch_Type.RISING_EDGE
    DEFAULT_RESET_TYPE = Logic_States.ACTIVE_HIGH
    DEFAULT_ENABLE_TYPE = Logic_States.ACTIVE_HIGH

    def __init__(self, size, bytesPerWord, startingAddress, address, write,
                 writeEnable, reset, clock, accessMode, read, default_value=0,
                 edge_type=Latch_Type.FALLING_EDGE,
                 reset_type=Logic_States.ACTIVE_HIGH,
                 writeEnable_type=Logic_States.ACTIVE_HIGH):
        """
        size : Number of bytes in the memory block.
        bytesPerWord : Must be a multiple of a byte and greater than zero.
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
            accessMode : type of read, write as
                    0b00 : "off"
                    0b01 : "byte"
                    0b10 : "half-word"
                    0b11 : "word"
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
        if not isinstance(bytesPerWord, int):
            raise TypeError('bytesPerWord must be an integer type')
        elif bytesPerWord <= 0 or bytesPerWord > limits.MAX_BYTES_IN_WORD:
            raise ValueError('bytesPerWord must fit within limits')
        if not isinstance(default_value, int):
            raise TypeError('Default value must be an integer')
        elif default_value < 0 or default_value >= 256:
            raise ValueError('Default value out of range')
        if not isinstance(startingAddress, int):
            raise TypeError('Starting address must be an integer')
        elif startingAddress < limits.MIN_ADDRESS or startingAddress > limits.MAX_ADDRESS:
            raise ValueError('Starting address must fit within limits')
        elif startingAddress + size > limits.MAX_ADDRESS:
            raise ValueError('Ending address must fit within limits')
        if not Latch_Type.valid(edge_type):
            raise ValueError('Invalid latch edge type')
        if not Logic_States.valid(reset_type):
            raise ValueError('Invalid reset state')
        if not Logic_States.valid(writeEnable_type):
            raise ValueError('Invalid write enable state')

        self._size = size
        self._bitWidth = bytesPerWord * 8
        self._default_value = default_value
        self._start_address = startingAddress
        self._end_address = startingAddress + size
        self._edge_type = edge_type
        self._reset_type = reset_type
        self._writeEnable_type = writeEnable_type

        # generate necessary parameters that buses must fit
        if size == 0:
            self._necessary_length = 0
        elif size < 2:
            self._necessary_length = 1
        else:  # len > 2
            self._necessary_length = int(math.floor(math.log(size - 1, 2) + 1))

        # check buses
        if not isinstance(address, iBusRead):
            raise TypeError('The address bus must be readable')
        elif address.size() != self._necessary_length:
            raise ValueError('The address bus must have valid range {}'.format(
                self._necessary_length))
        if not isinstance(write, iBusRead):
            raise TypeError('The write bus must be readable')
        elif write.size() != self._bitWidth:
            raise ValueError('The write bus must have matching word size')
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
        if not isinstance(accessMode, iBusRead):
            raise TypeError('The accessMode bus must be readable')
        elif accessMode.size() != 2:
            raise ValueError('The accessMode bus must have a size of 2 bit')
        if not isinstance(read, iBusWrite):
            raise TypeError('The read must must be writable')
        elif read.size() != self._bitWidth:
            raise ValueError('The read bus must have matching word size')

        self._address = address
        self._write = write
        self._writeEnable = writeEnable
        self._reset = reset
        self._clock = clock
        self._prev_clock_state = self._clock.read()
        self._read = read
        self._mode = accessMode

        # define memory space as bytes
        self._assigned_memory = {}

    def _write_word_to_memory(self, address, word):
        """
        Splits a word intp bytes and stored them into memory. Note that this
        device does support address rollover on edge case, however memory limits
        will be enforced.
        """
        for i in range(0, self._bitWidth // 8):
            b_index = (address - self._start_address + i) % (2**self._necessary_length)
            if b_index + self._start_address < self._end_address:  # address is valid
                byte = (word >> (self._bitWidth - 8 * (i + 1))) & 0xFF
                self._assigned_memory[b_index + self._start_address] = byte

    def _read_word_from_memory(self, address):
        """
        Generate word from bytes stored in memory starting at address.
        Note that this device does support rollover of address space for edge
        case.

        Returns an integer of memory unit defined word size
        """
        word = 0
        for i in range(0, self._bitWidth // 8):
            b_index = (address - self._start_address + i) % (2**self._necessary_length)
            if b_index in self._assigned_memory:
                b_index += self._start_address
                word |= self._assigned_memory[b_index] << (self._bitWidth - 8 * (i + 1))
            else:
                word |= self._default_value << (self._bitWidth - 8 * (i + 1))
        return word

    def _write_half_to_memory(self, address, word):
        """
        Splits a half-word intp bytes and stored them into memory. Note that this
        device does support address rollover on edge case, however memory limits
        will be enforced.
        """
        for i in range(0, (self._bitWidth // 2) // 8):
            b_index = (address - self._start_address + i) % (2**self._necessary_length)
            if b_index + self._start_address < self._end_address:  # address is valid
                byte = (word >> ((self._bitWidth // 2) - 8 * (i + 1))) & 0xFF
                self._assigned_memory[b_index + self._start_address] = byte

    def _read_half_from_memory(self, address):
        """
        Read a half-word from bute addressable memory.
        Note that this device does support rollover of address space for edge
        case.

        Returns an integer of memory unit defined word size
        """
        word = 0
        for i in range(0, (self._bitWidth // 2) // 8):
            b_index = (address - self._start_address + i) % (2**self._necessary_length)
            if b_index in self._assigned_memory:
                b_index += self._start_address
                word |= self._assigned_memory[b_index] << ((self._bitWidth // 2) - 8 * (i + 1))
            else:
                word |= self._default_value << ((self._bitWidth // 2) - 8 * (i + 1))
        return word

    def _write_byte_to_memory(self, address, word):
        """
        Write a byte from byte addressable memory.Note that this device does
        support address rollover on edge case, however memory limits will be
        enforced.
        """
        b_index = (address - self._start_address) % (2**self._necessary_length)
        if b_index + self._start_address < self._end_address:  # address is valid
            byte = word & 0xFF
            self._assigned_memory[b_index + self._start_address] = byte

    def _read_byte_from_memory(self, address):
        """
        Read a byte from byte addressable memory
        Note that this device does support rollover of address space for edge
        case.

        Returns an integer of memory unit defined word size
        """
        word = 0
        b_index = (address - self._start_address + i) % (2**self._necessary_length)
        if b_index in self._assigned_memory:
            b_index += self._start_address
            word = self._assigned_memory[b_index]
        else:
            word = self._default_value
        return word

    def on_rising_edge(self):
        """
        implements clock rising behavior: captures data if latching type matches
        """
        address = self._address.read()
        if self._edge_type == Latch_Type.RISING_EDGE or self._edge_type == Latch_Type.BOTH_EDGE:
            if self._mode.read() == Memory.MEM_MODE_WORD:
                self._write_word_to_memory(address, self._write.read())
            elif self._mode.read() == Memory.MEM_MODE_HALF:
                self._write_half_to_memory(address, self._write.read())
            elif self._mode.read() == Memory.MEM_MODE_BYTE:
                self._write_byte_to_memory(address, self._write.read())

    def on_falling_edge(self):
        """
        implements clock falling behavior: captures data if latching type matches
        """
        address = self._address.read()
        if self._edge_type == Latch_Type.FALLING_EDGE or self._edge_type == Latch_Type.BOTH_EDGE:
            if self._mode.read() == Memory.MEM_MODE_WORD:
                self._write_word_to_memory(address, self._write.read())
            elif self._mode.read() == Memory.MEM_MODE_HALF:
                self._write_half_to_memory(address, self._write.read())
            elif self._mode.read() == Memory.MEM_MODE_BYTE:
                self._write_byte_to_memory(address, self._write.read())

    def on_reset(self):
        """
        wipes out all memory
        """
        self._assigned_memory = {}

    def inspect(self):
        """
        returns dictionary message to user
        """
        return {
            'type': 'Memory',
            'size': self._size,
            'state': self._assigned_memory,
            'default_state' : self._default_value
        }

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
        elif (len(data) + start + self._start_address) > self._end_address:
            return {'error': 'address rollover not supported for modify'}
        elif len(data) <= 0:
            return {'error': 'data must have contents to store'}
        else:
            # validate all memory before store
            if not all((isinstance(x, int) and x >= 0 and x < 256) for x in data):
                return {'error': 'data must be represented as unsigned bytes'}

            # store data
            for i in range(0, len(data)):
                b_index = (start - self._start_address + i) % (2**self._necessary_length)
                if b_index + self._start_address < self._end_address:  # address is valid
                    self._assigned_memory[b_index + self._start_address] = data[i]

            return {'success': True}

    def clear(self):
        "Hook method to clear memory, thereby returning it to default value"
        self.on_reset()
        return {'success': True}

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

        # check for reset event
        if self._reset_type == Logic_States.ACTIVE_LOW and self._reset.read() == 0:
            self.on_reset()
        elif self._reset_type == Logic_States.ACTIVE_HIGH and self._reset.read() == 1:
            self.on_reset()

        # read is asynchronous
        read = 0
        if self._mode.read() == Memory.MEM_MODE_WORD:
            read = self._read_word_from_memory(self._address.read())
        elif self._mode.read() == Memory.MEM_MODE_HALF:
            read = self._read_half_from_memory(self._address.read())
        elif self._mode.read() == Memory.MEM_MODE_BYTE:
            read = self._read_byte_from_memory(self._address.read())
        self._read.write(read)

    @classmethod
    def from_dict(cls, config, hooks):
        "Implements conversion from configuration to component"

        if "value" in config:
            default_state = config["value"]
        else:
            default_state = Memory.DEFAULT_STATE

        if "edge_type" in config:
            edge_type = Latch_Type.fromString(config["edge_type"])
        else:
            edge_type = Memory.DEFAULT_LATCH_TYPE

        if "reset_type" in config:
            reset_type = Logic_States.fromString(config["reset_type"])
        else:
            reset_type = Memory.DEFAULT_RESET_TYPE

        if "enable_type" in config:
            enable_type = Logic_States.fromString(config["enable_type"])
        else:
            enable_type = Memory.DEFAULT_ENABLE_TYPE

        return Memory(config["size"], config["bytes_per_word"],
                      config["start_address"], hooks[config["address"]],
                      hooks[config["write"]], hooks[config["enable"]],
                      hooks[config["reset"]], hooks[config["clock"]],
                      hooks[config["access_mode"]], hooks[config["read"]],
                      default_state, edge_type, reset_type, enable_type)
