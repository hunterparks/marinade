from components.abstract.ibus import iBusRead, iBusWrite
from components.core.clock import Clock
from components.core.reset import Reset
from components.abstract.sequential import Sequential, Latch_Type, Logic_States
import limits

class Memory(Sequential):
    def __init__(self, a, wd, memwr, reset, clock, rd, edge_type = Latch_Type.FALLING_EDGE, 
                reset_type = Logic_States.ACTIVE_LOW, memwr_type = Logic_States.ACTIVE_LOW):
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
            self._assigned_memory[self._a.read()] == self._wd.read()
        
    def on_reset(self):
        # wipes out all memory
        self._assigned_memory = {}

    def inspect(self):
        # returns dictionary message to user
        return {'type': 'memory'}

    def modify(self, message):
        start_address = message['start']
        modified_memory = message['data']
        for data in modified_memory:
            offset = 0
            self._assigned_memory[start_address + offset] = data
            offset = offset + 32

    def run(self, time = None):
        # read is asynchronous
        if self._a.read() not in self._assigned_memory:
            # unassinged memory is set to 81818181
            self._rd.write(81818181)
        else:
            self._rd.write(self._assigned_memory[self._a.read()])
        # write is synchronous
        if self._memwr.read() == 1:
            if self._clock.read() == 1 and self._prev_clock_state == 0:
                self.on_rising_edge()
            elif self._clock.read() == 0 and self._prev_clock_state == 1:
                self.on_falling_edge()
            self._prev_clock_state = self._clock.read()