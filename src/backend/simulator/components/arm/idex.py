from simulator.components.abstract.ibus import iBusRead, iBusWrite
from simulator.components.abstract.sequential import Sequential, Latch_Type, Logic_States


class Idex(Sequential):
    """
    This specialized register sits between the decode and execute stages of the processor
    """

    def __init__(self, pc4d, regwrd, alusrcbd, alusd, aluflagwrd,
                 memwrd, regsrcd, wd3sd, rd1d, rd2d, imm32d, ra1d, ra2d, ra3d,
                 flush, clk, pc4e, regwre, alusrcbe, aluse, aluflagwre,
                 memwre, regsrce, wd3se, rd1e, rd2e, imm32e, ra1e, ra2e, ra3e,
                 edge_type=Latch_Type.RISING_EDGE, flush_type=Logic_States.ACTIVE_HIGH,
                 enable=None, enable_type=Logic_States.ACTIVE_HIGH):
        """
        inputs:
            pc4d: pc+4
            regwrd: selects whether to write back to the regfile
            alusrcbd: selects what value input B of the alu recieves
            alusd: selects the operation of the alu
            aluflagwrd: selects whether to update the C, V, N, and Z flags
            memwrd: selects whether to write to memory
            regsrcd: selects whether the alu output or memory is feedback
            wd3sd: selects what data to write to the regfile
            rd1d: register value
            rd2d: register value
            imm32d: 32-bit immediate value
            ra1d: register number
            ra2d: register number
            ra3d: register number
            flush: clears the instruction if active
            clk: clock
            enable: enables component (not typically used)
        outputs:
            pc4e: pc+4
            regwre: selects whether to write back to the regfile
            alusrcbe: selects what value input B of the alu recieves
            aluse: selects the operation of the alu
            aluflagwre: selects whether to update the C, V, N, and Z flags
            memwre: selects whether or not to write to memory
            regsrce: selects whether the alu output or memory is feedback
            wd3se: selects what data to write to the regfile
            rd1e: register value
            rd2e: register value
            imm32e: 32-bit immediate value
            ra1e: register number
            ra2e: register number
            ra3e: register number

        edge_type: idex register data latch type
        flush_type: flush signal active state
        enable_type: enable signal active state
        """

        if not isinstance(pc4d, iBusRead):
            raise TypeError('The pc4d bus must be readable')
        elif pc4d.size() != 32:
            raise ValueError('The pc4d bus must have a size of 32 bits')
        if not isinstance(regwrd, iBusRead):
            raise TypeError('The regwrd bus must be readable')
        elif regwrd.size() != 1:
            raise ValueError('The regwrd bus must have a size of 1 bit')
        if not isinstance(alusrcbd, iBusRead):
            raise TypeError('The alusrcbd bus must be readable')
        elif alusrcbd.size() != 1:
            raise ValueError('The alusd must have a size of 4 bits')
        if not isinstance(alusd, iBusRead):
            raise TypeError('The alusd bus must be readable')
        elif alusd.size() != 4:
            raise ValueError('The alusd bus must have a size of 4 bits')
        if not isinstance(aluflagwrd, iBusRead):
            raise TypeError('The aluflagwr bus must be readable')
        elif aluflagwrd.size() != 1:
            raise ValueError('The aluflagwr bus must have a size of 1 bit')
        if not isinstance(memwrd, iBusRead):
            raise TypeError('The memwrd bus must be readable')
        elif memwrd.size() != 1:
            raise ValueError('The memwrd bus must have a size of 1 bit')
        if not isinstance(regsrcd, iBusRead):
            raise TypeError('The regsrcd bus must be readable')
        elif regsrcd.size() != 1:
            raise ValueError('The regsrcd bus must have a size of 1 bit')
        if not isinstance(wd3sd, iBusRead):
            raise TypeError('The wd3sd bust must be readable')
        elif wd3sd.size() != 1:
            raise ValueError('The wd3sd bus must have a size of 1 bit')
        if not isinstance(rd1d, iBusRead):
            raise TypeError('The rd1d bus must be readable')
        elif rd1d.size() != 32:
            raise ValueError('The rd1d bus must have a size of 32 bits')
        if not isinstance(rd2d, iBusRead):
            raise TypeError('The rd2d bus must be readable')
        elif rd2d.size() != 32:
            raise ValueError('The rd2d bus must have a size of 32 bits')
        if not isinstance(imm32d, iBusRead):
            raise TypeError('The imm32d bus must be readable')
        elif imm32d.size() != 32:
            raise ValueError('The imm32d bus must have a size of 32 bits')
        if not isinstance(ra1d, iBusRead):
            raise TypeError('The ra1d bus must be readable')
        elif ra1d.size() != 4:
            raise ValueError('The ra1d bus must have a size of 4 bits')
        if not isinstance(ra2d, iBusRead):
            raise TypeError('The ra2d bus must be readable')
        elif ra2d.size() != 4:
            raise ValueError('The ra2d bus must have a size of 4 bits')
        if not isinstance(ra3d, iBusRead):
            raise TypeError('The ra3d bus must be readable')
        elif ra3d.size() != 4:
            raise ValueError('The ra3d bus must have a size of 4 bits')
        if not isinstance(flush, iBusRead):
            raise TypeError('The flush bus must be readable')
        elif flush.size() != 1:
            raise ValueError('The flush bus size must have a size of 1')
        if not isinstance(clk, iBusRead):
            raise TypeError('The clk bus must be readable')
        elif clk.size() != 1:
            raise ValueError('The clk must have a size of 1 bit')
        if not isinstance(pc4e, iBusRead):
            raise TypeError('The pc4e bus must be readable')
        elif pc4e.size() != 32:
            raise ValueError('The pc4e bus must have a size of 32 bits')
        if not isinstance(regwre, iBusWrite):
            raise TypeError('The regwre bus must be writable')
        elif regwre.size() != 1:
            raise ValueError('The regwre bust must have a size of 1 bit')
        if not isinstance(alusrcbe, iBusWrite):
            raise TypeError('The alusrcbe bus must be writable')
        elif alusrcbe.size() != 1:
            raise ValueError('The alusrcbe bus must have a size of 1 bit')
        if not isinstance(aluse, iBusWrite):
            raise TypeError('The aluse bus must be writable')
        elif aluse.size() != 4:
            raise ValueError('The aluse bus must have a size of 4 bits')
        if not isinstance(aluflagwre, iBusWrite):
            raise TypeError('The alufalgwre bus must be writable')
        elif aluflagwre.size() != 1:
            raise ValueError('The alusflagwre bus must have a size of 1 bit')
        if not isinstance(memwre, iBusWrite):
            raise TypeError('The memwre bus must be writable')
        elif memwre.size() != 1:
            raise ValueError('The memwre bus must have a size of 1 bit')
        if not isinstance(regsrce, iBusWrite):
            raise TypeError('The regsrce bus must be writable')
        elif regsrce.size() != 1:
            raise ValueError('The regsrce bus must have a size of 1 bit')
        if not isinstance(wd3se, iBusWrite):
            raise TypeError('The wd3se bus must be writable')
        elif wd3se.size() != 1:
            raise ValueError('The wd3se bust must have a size of 1 bit')
        if not isinstance(rd1e, iBusWrite):
            raise TypeError('The rd1e bus must be writable')
        elif rd1e.size() != 32:
            raise ValueError('The rd1e bus must have a size of 32 bits')
        if not isinstance(rd2e, iBusWrite):
            raise TypeError('The rd2e bus must be writable')
        elif rd2e.size() != 32:
            raise ValueError('The rd2e bus must have a size of 32 bits')
        if not isinstance(imm32e, iBusWrite):
            raise TypeError('The imm32e bus must be writable')
        elif imm32e.size() != 32:
            raise ValueError('The imm32e bus must have a size of 32 bits')
        if not isinstance(ra1e, iBusWrite):
            raise TypeError('The ra1e bus must be writable')
        elif ra1e.size() != 4:
            raise ValueError('The ra1e bus must have a size of 4 bits')
        if not isinstance(ra2e, iBusWrite):
            raise TypeError('The ra2e bus must be writable')
        elif ra2e.size() != 4:
            raise ValueError('The ra2e bus must have a size of 4 bits')
        if not isinstance(ra3e, iBusWrite):
            raise TypeError('The ra3e bus must be writable')
        elif ra3e.size() != 4:
            raise TypeError('The ra3e bus must have a size of 4 bits')
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

        self._pc4d = pc4d
        self._regwrd = regwrd
        self._alusrcbd = alusrcbd
        self._alusd = alusd
        self._aluflagwrd = aluflagwrd
        self._memwrd = memwrd
        self._regsrcd = regsrcd
        self._wd3sd = wd3sd
        self._rd1d = rd1d
        self._rd2d = rd2d
        self._imm32d = imm32d
        self._ra1d = ra1d
        self._ra2d = ra2d
        self._ra3d = ra3d
        self._flush = flush
        self._clk = clk
        self._prev_clk_state = self._clk.read()
        self._pc4e = pc4e
        self._regwre = regwre
        self._alusrcbe = alusrcbe
        self._aluse = aluse
        self._aluflagwre = aluflagwre
        self._memwre = memwre
        self._regsrce = regsrce
        self._wd3se = wd3se
        self._rd1e = rd1e
        self._rd2e = rd2e
        self._imm32e = imm32e
        self._ra1e = ra1e
        self._ra2e = ra2e
        self._ra3e = ra3e
        self._edge_type = edge_type
        self._flush_type = flush_type
        self._enable = enable
        self._enable_type = enable_type

        self._state = IdexState(self._pc4e, self._regwre, self._alusrcbe,
                                self._aluse, self._aluflagwre, self._memwre, self._regsrce,
                                self._wd3se, self._rd1e, self._rd2e, self._imm32e, self._ra1e,
                                self._ra2e, self._ra3e)


    def on_rising_edge(self):
        """
        Implements clock rising behavior: captures data if latch type matches
        """
        if self._edge_type == Latch_Type.RISING_EDGE or self._edge_type == Latch_Type.BOTH_EDGE:
            if ((self._flush_type == Logic_States.ACTIVE_LOW and self._flush.read() == 0)
                    or (self._flush_type == Logic_States.ACTIVE_HIGH and self._flush.read() == 1)):
                self._pc4e.write(0)
                self._regwre.write(0)
                self._alusrcbe.write(0)
                self._aluse.write(0)
                self._aluflagwre.write(0)
                self._memwre.write(0)
                self._regsrce.write(0)
                self._wd3se.write(0)
                self._rd1e.write(0)
                self._rd2e.write(0)
                self._imm32e.write(0)
                self._ra1e.write(0)
                self._ra2e.write(0)
                self._ra3e.write(0)
            else:
                self._pc4e.write(self._pc4d.read())
                self._regwre.write(self._regwrd.read())
                self._alusrcbe.write(self._alusrcbd.read())
                self._aluse.write(self._alusd.read())
                self._aluflagwre.write(self._aluflagwrd.read())
                self._memwre.write(self._memwrd.read())
                self._regsrce.write(self._regsrcd.read())
                self._wd3se.write(self._wd3sd.read())
                self._rd1e.write(self._rd1d.read())
                self._rd2e.write(self._rd2d.read())
                self._imm32e.write(self._imm32d.read())
                self._ra1e.write(self._ra1d.read())
                self._ra2e.write(self._ra2d.read())
                self._ra3e.write(self._ra3d.read())

    def on_falling_edge(self):
        """
        Implements clock falling behavior: captures data if latch type matches
        """
        if self._edge_type == Latch_Type.FALLING_EDGE or self._edge_type == Latch_Type.BOTH_EDGE:
            if ((self._flush_type == Logic_States.ACTIVE_LOW and self._flush.read() == 0)
                    or (self._flush_type == Logic_States.ACTIVE_HIGH and self._flush.read() == 1)):
                self._pc4e.write(0)
                self._regwre.write(0)
                self._alusrcbe.write(0)
                self._aluse.write(0)
                self._aluflagwre.write(0)
                self._memwre.write(0)
                self._regsrce.write(0)
                self._wd3se.write(0)
                self._rd1e.write(0)
                self._rd2e.write(0)
                self._imm32e.write(0)
                self._ra1e.write(0)
                self._ra2e.write(0)
                self._ra3e.write(0)
            else:
                self._pc4e.write(self._pc4d.read())
                self._regwre.write(self._regwrd.read())
                self._alusrcbe.write(self._alusrcbd.read())
                self._aluse.write(self._alusd.read())
                self._aluflagwre.write(self._aluflagwrd.read())
                self._memwre.write(self._memwrd.read())
                self._regsrce.write(self._regsrcd.read())
                self._wd3se.write(self._wd3sd.read())
                self._rd1e.write(self._rd1d.read())
                self._rd2e.write(self._rd2d.read())
                self._imm32e.write(self._imm32d.read())
                self._ra1e.write(self._ra1d.read())
                self._ra2e.write(self._ra2d.read())
                self._ra3e.write(self._ra3d.read())

    def on_reset(self):
        """
        Not used for this register
        """
        pass


    def inspect(self):
        """
        Returns a dictionary message to the user
        """
        return {'type': 'idex register', 'state': self._state}


    def modify(self, data = None):
        """
        Return message noting that is register cannot be modified
        """
        return {'error' : 'idex register cannot be modified'}


    def clear(self):
        "Return a message noting that the idex register cannot be cleared"
        return {'error': 'idex register cannot be cleared'}


    def run(self, time=None):
        """
        Timestep handler function - sequentially asserts output
        """
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


class IdexState():
    """
    Stores the idex registers state
    Used in the Idex class's inspect method
    Note: Do not make new instances of this class outside of the Idex class
    """

    def __init__(self, pc4e, regwre, alusrcbe, aluse, aluflagwre, memwre, regsrce,
                wd3se, rd1e, rd2e, imm32e, ra1e, ra2e, ra3e):
        self._pc4e = pc4e
        self._regwre = regwre
        self._alusrcbe = alusrcbe
        self._aluse = aluse
        self._aluflagwre = aluflagwre
        self._memwre = memwre
        self._regsrce = regsrce
        self._wd3se = wd3se
        self._rd1e = rd1e
        self._rd2e = rd2e
        self._imm32e = imm32e
        self._ra1e = ra1e
        self._ra2e = ra2e
        self._ra3e = ra3e

    def get_state(self):
        return {'pcsrce': self._pc4e.read(),
                'regwre': self._regwre.read(), 'alusrcbe': self._alusrcbe.read(),
                'aluse': self._aluse.read(), 'aluflagwre': self._aluflagwre.read(),
                'memwre': self._memwre.read(), 'regsrce': self._regsrce.read(),
                'wd3se': self._wd3se.read(), 'rd1e': self._rd1e.read(),
                'rd2e': self._rd2e.read(), 'imm32e': self._imm32e.read(),
                'ra1e': self._ra1e.read(), 'ra2e': self._ra2e.read(),
                'ra3e': self._ra3e.read()}
