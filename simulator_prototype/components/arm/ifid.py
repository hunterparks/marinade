from components.abstract.ibus import iBusRead, iBusWrite
from components.abstract.sequential import Sequential, Latch_Type, Logic_States

class Ifid(Sequential):
    """
        This specialized register sits between the fetch and decode stages of the processor
    """

    def __init__(self, instrf, stall, flush, clk, instrd, default_state = 0, 
                edge_type = Latch_Type.RISING_EDGE, flush_type = Logic_States.ACTIVE_HIGH,
                enable = None, enable_type = Logic_States.ACTIVE_HIGH):
        if not isinstance(instrf, iBusRead) or instrf.size() != 32:
            raise ValueError('The instrf bus must have a size of 32 bits')
        if not isinstance(stall, iBusRead) or stall.size() != 1:
            raise ValueError('The stall bus must have a size of 1 bit')
        if not isinstance(flush, iBusRead) or flush.size() != 1:
            raise ValueError('The flush bus must have a size of 1 bit')
        if not isinstance(clk, iBusRead) or clk.size() != 1:
            raise ValueError('The clock bus must have a size of 1 bit')
        if not isinstance(instrd, iBusWrite) or instrd.size() != 32:
            raise ValueError('The instrd bus must have a size of 32 bits') 
        if not isinstance(default_state, int) or default_state < 0 or default_state >= 2**32:
            raise ValueError('The default state must be an integer between -1 and 4294967296')
        if not Latch_Type.valid(edge_type):
            raise ValueError('Invalid latch edge type')
        if not Logic_States.valid(flush_type):
            raise ValueError('Invalid flush state')
        if not isinstance(enable, iBusRead) or (enable is not None and enable.size() != 1):
            raise ValueError('The enable input must have a size of 1 bit')
        if not Logic_States.valid(enable_type):
            raise ValueError('Invalid enable state')
        self._instrf = instrf
        self._stall = stall
        self._flush = flush
        self._clk = clk
        self._prev_clk_state = self._clk.read()
        self._instrd = instrd
        self._default_state = default_state
        self._instrd.write(default_state)
        self._edge_type = edge_type
        self._flush_type = flush_type
        self._enable = enable
        self._enable_type = enable_type

    def on_rising_edge(self):
        "Implements clock rising behavior: captures data if latching type matches"
        if self._edge_type == Latch_Type.RISING_EDGE or self._edge_type == Latch_Type.BOTH_EDGE:
            self._instrd.write(self._instrf.read())

    def on_falling_edge(self):
        "Implements clock falling behavior: captures data if latching type matches"
        if self._edge_type == Latch_Type.FALLING_EDGE or self._edge_type == Latch_Type.BOTH_EDGE:
            self._instrd.write(self._instrf.read())

    def on_reset(self):
        "Flushes the output to the default state defined for the register"
        self._instrd.write(self._default_state)

    def inspect(self):
        "Returns a dictionary message to the user"
        return {'type': 'ifid', 'instrf': self._instrf.read(), 'instrd': self._instrd.read()}
    
    def run(self, time = None):
        "Timestep handler function clocks data into register and asserts output"

        # process enable line
        e = True
        if self._enable is not None:
            if self._enable_type == Logic_States.ACTIVE_LOW:
                e = self._enable_type.read() == 0
            else:
                e = self._enable.read() == 1
        
        # check for clock change
        if e:
            if self._clk.read() == 1 and self._prev_clk_state == 0:
                self.on_rising_edge()
            elif self._clk.read() == 0 and self._prev_clk_state == 1:
                self.on_falling_edge()
        self._prev_clk_state = self._clk.read()

        # check for reset event
        if self._flush_type == Logic_States.ACTIVE_LOW and self._flush.read() == 0:
            self.on_reset()
        elif self._flush_type == Logic_States.ACTIVE_HIGH and self._flush.read() == 1:
            self.on_reset()