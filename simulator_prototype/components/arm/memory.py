from components.abstract.ibus import iBusRead, iBusWrite
from components.core.clock import Clock
from components.core.reset import Reset
from components.abstract.sequential import Sequential, Latch_Type, Logic_States
import limits

class Memory(Sequential):
    def __init__(self, a, wd, memwr, reset, clock, rd, edge_type = Latch_Type.FALLING_EDGE,
                reset_type = Logic_States.ACTIVE_LOW, memwr_type = Logic_States.ACTIVE_LOW):
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
        if not isinstance(reset, iBusRead):
            raise TypeError('The reset bus must be readable')
        elif reset.size() != 1:
            raise ValueError('The reset bus must have a size of 1 bit')
        if not isinstance(clock, iBusRead):
            raise TypeError('The clock bus must be readable')
        elif clock.size() != 1:
            raise ValueError('The clock bus must have a size of 1 bit')
        if not isinstance(rd, iBusWrite):
            raise TypeError('The rd must must be writable')
        elif rd.size() != 32:
            raise ValueError('The rd bus must have a size of 32 bits')
        if not Latch_Type.valid(edge_type):
            raise ValueError('Invalid latch edge type')
        if not Logic_States.valid(reset_type):
            raise ValueError('Invalid reset state')
        if not Logic_States.valid(memwr_type):
            raise ValueError('Invalid memwr state')
        self._a = a
        self._wd = wd
        self._memwr = memwr
        self._reset = reset
        self._clock = clock
        self._prev_clock_state = self._clock.read()
        self._rd = rd
        self._edge_type = edge_type
        self._reset_type = reset_type
        self._memwr_type = memwr_type
        self._assigned_memory = {}

    def on_rising_edge(self):
        if self._edge_type == Latch_Type.RISING_EDGE or self._edge_type == Latch_Type.BOTH_EDGE:
            self._assigned_memory[self._a.read()] = self._wd.read()

    def on_falling_edge(self):
        if self._edge_type == Latch_Type.FALLING_EDGE or self._edge_type == Latch_Type.BOTH_EDGE:
            self._assigned_memory[self._a.read()] = self._wd.read()

    def on_reset(self):
        '''
        wipes out all memory
        '''
        self._assigned_memory = {}

    def inspect(self):
        '''
        returns dictionary message to user
        '''
        return {'type': 'memory', 'size': len(self._assigned_memory)}

    def modify(self, message):
        if 'start' not in message or 'data' not in message:
            raise ValueError('The message argurment must be a dictionary that includes a "start" key and a "data" key')
        start_address = message['start']
        modified_memory = message['data']
        offset = 0
        for data in modified_memory:
            self._assigned_memory[start_address + offset] = data
            offset = offset + 32
        
    def view_memory_address(self, address):
        '''
        Used to view a 32-bit memory address.
        This method is used for testing purposes only.
        It should not be used when designing the top level architecture.
        '''
        if address not in self._assigned_memory:
            return 0x81818181
        else:
            return self._assigned_memory[address]

    def run(self, time = None):
        # write is synchronous
        if self._memwr.read() == 1:
            if self._clock.read() == 1 and self._prev_clock_state == 0:
                self.on_rising_edge()
            elif self._clock.read() == 0 and self._prev_clock_state == 1:
                self.on_falling_edge()
        self._prev_clock_state = self._clock.read()
        # read is asynchronous
        if self._a.read() not in self._assigned_memory:
            # unassinged memory is set to 0x81818181
            self._rd.write(0x81818181)
        else:
            self._rd.write(self._assigned_memory[self._a.read()])
