from components.abstract.sequential import Sequential, Latch_Type, Logic_States
from components.core.bus import iBusRead, iBusWrite


class Exmem(Sequential):
    """
    This specialized register sits between the decode and execute stages of the
    processor
    """
    def __init__(self, pcsrce, regwrse, regwre, memwre, regsrce, wd3se, rd2e, fe, ra3e, clk,
                 pcsrcm, regwrsm, regwrm, memwrm, regsrcm, wd3sm, fm, rd2m, ra3m,
                 edge_type=Latch_Type.RISING_EDGE, enable=None,
                 enable_type=Logic_States.ACTIVE_HIGH):
        """
        inputs:
            pcsrce: selects the instruction given to the fetch stage
            regwrse: selects which register is passed into input a2 of the regfile
            regwre: selects whether to write back to the refile
            memwre: selects whether to write to memory
            regsrce: selects whether a alu output or memory is feedback
            wd3se: selects what data to write to the regfile
            rd2e: register value
            fe: output of execute stage
            ra3e: register number
            clk: clock
            enable: enables component (not typically used)
        outputs:
            pcsrce: selects the instruction given to the fetch stage
            regwrse: selects which register is passed into input a2 of the regfile
            regwre: selects whether to write back to the refile
            memwre: selects whether to write to memory
            regsrce: selects whether a alu output or memory is feedback
            wd3se: selects what data to write to the regfile
            rd2e: register value
            fe: output of execute stage
            ra3e: register number

        enable_type: exmem register data latch type
        enable_type: enable signal active state
        """

        if not isinstance(pcsrce, iBusRead):
            raise TypeError('The pcsrce bus must be readable')
        elif pcsrce.size() != 2:
            raise ValueError('The pcsrce bus must have a size of 2 bits')
        if not isinstance(regwrse, iBusRead):
            raise TypeError('The regwrse bus must be readable')
        elif regwrse.size() != 2:
            raise ValueError('The regwrs bus must have a size of 2 bits')
        if not isinstance(regwre, iBusRead):
            raise TypeError('The regwre bus must be readable')
        elif regwre.size() != 1:
            raise ValueError('The regwre bus must have a size of 1 bit')
        if not isinstance(memwre, iBusRead):
            raise TypeError('The memwre bus must be readable')
        elif memwre.size() != 1:
            raise ValueError('The memwre bus must have a size of 1 bit')
        if not isinstance(regsrce, iBusRead):
            raise TypeError('The regsrce bus must be readable')
        elif regsrce.size() != 1:
            raise ValueError('The regsrce bus must have a size of 1 bit')
        if not isinstance(wd3se, iBusRead):
            raise TypeError('The wd3se bus must be readable')
        elif wd3se.size() != 1:
            raise ValueError('The wd3se bus must have a size of 1 bit')
        if not isinstance(rd2e, iBusRead):
            raise TypeError('The rd2e bus must be readable')
        elif rd2e.size() != 32:
            raise ValueError('The rd2e bus must have a size of 32 bits')
        if not isinstance(fe, iBusRead):
            raise TypeError('The fe bus must be readable')
        elif fe.size() != 32:
            raise ValueError('The fe bus must have a size of 323 bits')
        if not isinstance(ra3e, iBusRead):
            raise TypeError('The ra3e but must be readable')
        elif ra3e.size() != 4:
            raise ValueError('The ra3e bus must have a size of 4 bits')
        if not isinstance(clk, iBusRead):
            raise TypeError('The clk bus must be readable')
        elif clk.size() != 1:
            raise ValueError('The clk bus must have a size of 1 bit')
        if not isinstance(pcsrcm, iBusWrite):
            raise TypeError('The pcsrcm bus must be writable')
        elif pcsrcm.size() != 2:
            raise ValueError('The pcsrcm bus must have a size of 2 bits')
        if not isinstance(regwrsm, iBusWrite):
            raise TypeError('The regwrsm bus must be readable')
        elif regwrsm.size() != 2:
            raise ValueError('The regwrsm bus must have a size of 2 bits')
        if not isinstance(regwrm, iBusWrite):
            raise TypeError('The regwrm bus must be writable')
        elif regwrm.size() != 1:
            raise ValueError('The regwrm bus must have a size of 1 bit')
        if not isinstance(memwrm, iBusWrite):
            raise TypeError('The memwrm bus must be writable')
        elif memwrm.size() != 1:
            raise ValueError('The memwrm bus must have a size of 1 bit')
        if not isinstance(regsrcm, iBusWrite):
            raise TypeError('The regsrcm bus must be writable')
        elif regsrcm.size() != 1:
            raise ValueError('The regsrcm bus must have a size of 1 bit')
        if not isinstance(wd3sm, iBusWrite):
            raise TypeError('The wd3sm bus must be writable')
        elif wd3sm.size() != 1:
            raise ValueError('The wd3sm bus must have a size of 1 bit')
        if not isinstance(fm, iBusWrite):
            raise TypeError('The fm bus must be writable')
        elif fm.size() != 32:
            raise ValueError('The fm bus must have a size of 32 bits')
        if not isinstance(rd2m, iBusWrite):
            raise TypeError('The rd2m bus must be writable')
        elif rd2m.size() != 32:
            raise ValueError('The rd2m bus must have a size of 32 bits')
        if not isinstance(ra3m, iBusWrite):
            raise TypeError('The ra3m bus must be writable')
        elif ra3m.size() != 4:
            raise ValueError('The ra3m bus must have a size of 4 bits')
        if not Latch_Type.valid(edge_type):
            raise ValueError('Invalid latch edge type')
        if enable is not None and not isinstance(enable, iBusRead):
            raise ValueError('The enable bus must be readable')
        elif enable is not None and enable.size() != 1:
            raise ValueError('The enable bus must have a size of 1 bit')
        if not Logic_States.valid(enable_type):
            raise ValueError('Invalid enable state')

        self._pcsrce = pcsrce
        self._regwrse = regwrse
        self._regwre = regwre
        self._memwre = memwre
        self._regsrce = regsrce
        self._wd3se = wd3se
        self._rd2e = rd2e
        self._fe = fe
        self._ra3e = ra3e
        self._clk = clk
        self._prev_clk_state = self._clk.read()
        self._pcsrcm = pcsrcm
        self._regwrsm = regwrsm
        self._regwrm = regwrm
        self._memwrm = memwrm
        self._regsrcm = regsrcm
        self._wd3sm = wd3sm
        self._fm = fm
        self._rd2m = rd2m
        self._ra3m = ra3m
        self._edge_type = edge_type
        self._enable = enable
        self._enable_type = enable_type

        self._state = ExmemState(self._pcsrcm, self._regwrsm, self._regwrm, self._memwrm, 
                                self._regsrcm, self._wd3sm, self._fm, self._rd2m, self._ra3m)


    def on_rising_edge(self):
        """
        Implements clock rising behavior: captures data if latch type matches
        """
        if self._edge_type == Latch_Type.RISING_EDGE or self._edge_type == Latch_Type.BOTH_EDGE:
            self._pcsrcm.write(self._pcsrce.read())
            self._regwrsm.write(self._regwrse.read())
            self._regwrm.write(self._regwre.read())
            self._memwrm.write(self._memwre.read())
            self._regsrcm.write(self._regsrce.read())
            self._wd3sm.write(self._wd3se.read())
            self._fm.write(self._fe.read())
            self._rd2m.write(self._rd2e.read())
            self._ra3m.write(self._ra3e.read())

    def on_falling_edge(self):
        """
        Implements clock falling behavior: captures data if latch type matches
        """

        if self._edge_type == Latch_Type.FALLING_EDGE or self._edge_type == Latch_Type.BOTH_EDGE:
            self._pcsrcm.write(self._pcsrce.read())
            self._regwrsm.write(self._regwrse.read())
            self._regwrm.write(self._regwre.read())
            self._memwrm.write(self._memwre.read())
            self._regsrcm.write(self._regsrce.read())
            self._wd3sm.write(self._wd3se.read())
            self._fm.write(self._fe.read())
            self._rd2m.write(self._rd2e.read())
            self._ra3m.write(self._ra3e.read())

    def on_reset(self):
        "Not used for this register"
        pass

    def inspect(self):
        "Returns a dictionary message to the user"
        return {'type': 'exmem register', 'state': self._state}


    def modify(self, data = None):
        """
        Return message noting that is register cannot be modified
        """
        return {'error' : 'exmem register cannot be modified'}


    def run(self, time = None):
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


class ExmemState():
    """
    Stores the exmem registers state
    Used in the Exmem class's inspect method
    Note: Do not make new instances of this class outside of the Exmem class
    """

    def __init__(self, pcsrcm, regwrsm, regwrm, memwrm, regsrcm, wd3sm, fm, rd2m, ra3m):
        self._pcsrcm = pcsrcm
        self._regwrsm = regwrsm
        self._regwrm = regwrm
        self._memwrm = memwrm
        self._regsrcm = regsrcm
        self._wd3sm = wd3sm
        self._fm = fm
        self._rd2m = rd2m
        self._ra3m = ra3m


    def get_state(self):
        return {'pcsrcm': self._pcsrcm.read(), 'regwrsm': self._regwrsm.read(),
                'regwrem': self._regwrm.read(), 'memwrm': self._memwrm.read(),
                'regsrcm': self._regsrcm.read(), 'wd3sm': self._wd3sm.read(),
                'fm': self._fm.read(), 'rd2m': self._rd2m.read(),
                'ra3m': self._ra3m.read()}
