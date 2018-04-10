from simulator.components.abstract.ibus import iBusRead, iBusWrite
from simulator.components.abstract.sequential import Sequential, Latch_Type, Logic_States


class Ifid(Sequential):
    """
    This specialized register sits between the fetch and decode stages of the
    processor
    """

    def __init__(self, pc4f, pc8f, instrf, stall, flush, clk, pc4d, pc8d, 
                 instrd, default_state=0, edge_type=Latch_Type.RISING_EDGE,
                 flush_type=Logic_States.ACTIVE_HIGH, enable=None,
                 enable_type=Logic_States.ACTIVE_HIGH):
        """
        inputs:
            pc4f: pc+4
            pc8f: pc+8
            instrf: the fetched instruction
            stall: postpones the flow of instructions if active
            flush: clears the instruction if active
            clk: clock
            enable: enables component (not typically used)
        outputs:
            pc4d: pc+4
            pc8d: pc+8
            instrd: the output instruction

        default_state: the default output
        edge_type: ifid register data latch type
        flush_type: flush signal active state
        enable_type : enable signal active state
        """

        # Inputs
        if not isinstance(pc4f, iBusRead):
            raise TypeError('The pc4f bus must be readable')
        elif pc4f.size() != 32:
            raise ValueError('The pc4f bus must have a size of 32 bits')
        if not isinstance(pc8f, iBusRead):
            raise TypeError('The pc8f bus must be readable')
        elif pc8f.size() != 32:
            raise ValueError('The pc8f bus must have a size of 32 bits')
        if not isinstance(instrf, iBusRead):
            raise TypeError('The instrf bus must be readable')
        elif instrf.size() != 32:
            raise ValueError('The instrf bus must have a size of 32 bits')
        if not isinstance(stall, iBusRead):
            raise TypeError('The stall bus must be readable')
        elif stall.size() != 1:
            raise ValueError('The stall bus must have a size of 1 bit')
        if not isinstance(flush, iBusRead):
            raise TypeError('The flush bus must be readable')
        elif flush.size() != 1:
            raise ValueError('The flush bus must have a size of 1 bit')
        if not isinstance(clk, iBusRead):
            raise TypeError('The clk bust must be readable')
        elif clk.size() != 1:
            raise ValueError('The clock bus must have a size of 1 bit')

        self._pc4f = pc4f
        self._pc8f = pc8f
        self._instrf = instrf
        self._stall = stall
        self._flush = flush
        self._clk = clk
        self._prev_clk_state = self._clk.read()

        # Outputs
        if not isinstance(pc4d, iBusWrite):
            raise TypeError('The pc4d bus must be writable')
        elif pc4d.size() != 32:
            raise ValueError('The pc4d bus must have a size of 32 bits')
        if not isinstance(pc8d, iBusWrite):
            raise TypeError('The pc8d bus must be writable')
        elif pc8d.size() != 32:
            raise TypeError('The pc8d bus must have a size of 32 bits')
        if not isinstance(instrd, iBusWrite):
            raise TypeError('The instrd bus must be writable')
        elif instrd.size() != 32:
            raise ValueError('The instrd bus must have a size of 32 bits')

        self._pc4d = pc4d
        self._pc8d = pc8d
        self._instrd = instrd

        # Attributes
        if not isinstance(default_state, int) or default_state < 0 or default_state >= 2**32:
            raise ValueError('The default state must be an integer between -1 and 4294967296')
        if not Latch_Type.valid(edge_type):
            raise ValueError('Invalid latch edge type')
        if not Logic_States.valid(flush_type):
            raise ValueError('Invalid flush state')
        if enable is not None and not isinstance(enable, iBusRead):
            raise ValueError('The enable bus must be readable')
        elif enable is not None and enable.size() != 1:
            raise ValueError('The enable bus must have a size of 1 bit')
        if not Logic_States.valid(enable_type):
            raise ValueError('Invalid enable state')

        self._default_state = default_state
        self._instrd.write(default_state)
        self._edge_type = edge_type
        self._flush_type = flush_type
        self._enable = enable
        self._enable_type = enable_type

        self._ifid = IfidState(self._pc4d, self._pc8d, self._instrd)

    def on_rising_edge(self):
        "Implements clock rising behavior: captures data if latching type matches"
        if (self._edge_type == Latch_Type.RISING_EDGE 
                or self._edge_type == Latch_Type.BOTH_EDGE):
            if ((self._flush_type == Logic_States.ACTIVE_LOW 
                    and self._flush.read() == 0)
                    or (self._flush_type == Logic_States.ACTIVE_HIGH 
                    and self._flush.read() == 1)):
                self._pc4d.write(0)
                self._pc8d.write(0)
                self._instrd.write(0)
            elif ((self._enable_type == Logic_States.ACTIVE_HIGH 
                    and self._stall.read() == 1)
                    or (self._enable_type == Logic_States.ACTIVE_LOW 
                    and self._stall.read() == 0)):
                self._pc4d.write(self._pc4d.read())
                self._pc8d.write(self._pc8d.read())
                self._instrd.write(self._instrd.read())
            else:
                self._pc4d.write(self._pc4f.read())
                self._pc8d.write(self._pc8f.read())
                self._instrd.write(self._instrf.read())

    def on_falling_edge(self):
        "Implements clock falling behavior: captures data if latching type matches"
        if (self._edge_type == Latch_Type.FALLING_EDGE 
                or self._edge_type == Latch_Type.BOTH_EDGE):
            if ((self._flush_type == Logic_States.ACTIVE_LOW 
                    and self._flush.read() == 0)
                    or (self._flush_type == Logic_States.ACTIVE_HIGH 
                    and self._flush.read() == 1)):
                self._pc4d.write(0)
                self._pc8d.write(0)
                self._instrd.write(0)
            elif ((self._enable_type == Logic_States.ACTIVE_HIGH 
                    and self._stall.read() == 1)
                    or (self._enable_type == Logic_States.ACTIVE_LOW 
                    and self._stall.read() == 0)):
                self._pc4d.write(self._pc4d.read())
                self._pc8d.write(self._pc8d.read())
                self._instrd.write(self._instrd.read())
            else:
                self._pc4d.write(self._pc4f.read())
                self._pc8d.write(self._pc8f.read())
                self._instrd.write(self._instrf.read())

    def on_reset(self):
        "Not used for this register"
        pass

    def inspect(self):
        "Returns a dictionary message to the user"
        return {'type': 'ifid register', 'state': self._ifid.get_state()}


    def modify(self, data = None):
        "Return message noting that is register cannot be modified"
        return {'error': 'ifid register cannot be modified'}


    def clear(self):
        "Return a message noting that the ifid register cannot be cleared"
        return {'error': 'ifid register cannot be cleared'}


    def run(self, time=None):
        "Timestep handler function - sequentially asserts output"

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

    @classmethod
    def from_dict(cls, config):
        "Implements conversion from configuration to component"
        return NotImplemented

    def to_dict(self):
        "Implements conversion from component to configuration"
        return NotImplemented


class IfidState():
    """
    Stores the idex registers state
    Used in the Idex class's inspect method
    Do not make new instances of this class outside of the Idex class
    """

    def __init__(self, pc4d, pc8d, instrd):
        self._pc4d = pc4d
        self._pc8d = pc8d
        self._instrd = instrd

    def get_state(self):
        return {'pc4d': self._pc4d.read(), 'pc8d': self._pc8d.read(),
                'instrd': self._instrd.read()}
