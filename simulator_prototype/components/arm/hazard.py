from components.abstract.ibus import iBusRead, iBusWrite

class hazardController():

    def __init__(self, ra1d, ra2d, ra1e, ra2e, ra3e, ra3m, ra3w, regwrm,
                regwrw, regsrce, regsrcw, memwrm, pcsrcd, fwda, fwdb, fwds,
                stalld, flushd, flushe):
        if not isinstance(ra1d, iBusRead):
            raise TypeError('The ra1d bus must be readable')
        elif ra1d.size() != 4:
            raise ValueError('The ra1d bus must have a size of 4 bits')
        if not isinstance(ra2d, iBusRead):
            raise TypeError('The ra2d bus must be readable')
        elif ra2d.size() != 4:
            raise ValueError('The ra2d bus must have a size of 4 bits')
        if not isinstance(ra1e, iBusRead):
            raise TypeError('The ra1e bus must be readable')
        elif ra1e.size() != 4:
            raise ValueError('The ra1e bus must have a size of 4 bits')
        if not isinstance(ra2e, iBusRead):
            raise TypeError('The ra2e bus must be readable')
        elif ra2e.size() != 4:
            raise ValueError('The ra2e bus must have a size of 4 bits')
        if not isinstance(ra3e, iBusRead):
            raise TypeError('The ra3e bus must be readable')
        elif ra3e.size() != 4:
            raise ValueError('The ra3e bus must have a size of 4 bits')
        if not isinstance(ra3m, iBusRead):
            raise TypeError('The ra3m bus must be readable')
        elif ra3m.size() != 4:
            raise ValueError('The ra3m bus must have a size of 4 bits')
        if not isinstance(ra3w, iBusRead):
            raise TypeError('The ra3w bus must be readable')
        elif ra3w.size() != 4:
            raise ValueError('The ra3w bus must have a size of 4 bits')
        if not isinstance(regwrm, iBusRead):
            raise TypeError('The regwrm bus must be readable')
        elif regwrm.size() != 1:
            raise ValueError('The regwrm bus must have a size of 1 bit')
        if not isinstance(regwrw, iBusRead):
            raise TypeError('The regwrw bus must be readable')
        elif regwrw.size() != 1:
            raise ValueError('The regwrw bus must have a size of 1 bit')
        if not isinstance(regsrce, iBusRead):
            raise TypeError('The regsrce bus must be readable')
        elif regsrce.size() != 1:
            raise ValueError('The regsrce bus must have a size of 1 bit')
        if not isinstance(regsrcw, iBusRead):
            raise TypeError('The regsrcw bus must be readable')
        elif regsrcw.size() != 1:
            raise ValueError('The regsrcw bus must have a size of 1 bit')
        if not isinstance(memwrm, iBusRead):
            raise TypeError('The memwrm bus must be readable')
        elif memwrm.size() != 1:
            raise ValueError('The memwrm bus must have a size of 1 bit')
        if not isinstance(pcsrcd, iBusRead):
            raise TypeError('The pcsrcd bus must be readable')
        elif pcsrcd.size() != 2:
            raise ValueError('The pcsrcd bus must have a size of 2 bits')
        
        self._ra1d = ra1d
        self._ra2d = ra2d
        self._ra1e = ra1e
        self._ra2e = ra2e
        self._ra3e = ra3e
        self._ra3m = ra3m
        self._ra3w = ra3w
        self._regwrm = regwrm
        self._regwrw = regwrw
        self._regsrce = regsrce
        self._regsrcw = regsrcw
        self._memwrm = memwrm
        self._pcsrcd = pcsrcd

        if not isinstance(fwda, iBusWrite):
            raise TypeError('The fwda bus must be writable')
        elif fwda.size() != 2:
            raise ValueError('The fwda bus must have a size of 2 bits')
        if not isinstance(fwdb, iBusWrite):
            raise TypeError('The fwdb bus must be writable')
        elif fwdb.size() != 2:
            raise ValueError('The fwdb bus must have a size of 2 bits')
        if not isinstance(fwds, iBusWrite):
            raise TypeError('The fwds bus must be writable')
        elif fwds.size() != 1:
            raise ValueError('The fwds bus must have a size of 1 bit')
        if not isinstance(stalld, iBusWrite):
            raise TypeError('The stalld bus must be writable')
        elif stalld.size() != 1:
            raise ValueError('The stalld bus must have a size of 1 bit')
        if not isinstance(flushd, iBusWrite):
            raise TypeError('The flushd bus must be writable')
        elif flushd.size() != 1:
            raise ValueError('The flushd bus must have a size of 1 bit')
        if not isinstance(flushe, iBusWrite):
            raise TypeError('The flushe bus must be writable')
        elif flushe.size() != 1:
            raise ValueError('The flushe bus must have a size of 1 bit')

        self._fwda = fwda
        self._fwdb = fwdb
        self._fwds = fwds
        self._stalld = stalld
        self._flushd = flushd
        self._flushe = flushe

    
    @staticmethod
    def _generate_fwda(ra1e, ra3m, ra3w, regwrm, regwrw, regsrcw):
        # If pipeline processor does not work - check the if statement below
        if ra1e.read() == ra3w.read() and regsrcw.read() == 1:
            return 0b11     # Load-use hazard occured
        elif ra1e.read() == ra3m.read() and regwrm.read() == 1:
            return 0b10     # Register-use hazard occured
        elif ra1e.read() == ra3w.read() and regwrw.read() == 1:
            return 0b01     # Register-use hazard occured
        else:
            return 0b00     # No hazard occured


    @staticmethod
    def _generate_fwdb(ra2e, ra3m, ra3w, regwrm, regwrw, regsrcw):
        # If pipeline processor does not work - check the if statement below
        if ra2e.read() == ra3w.read() and regsrcw.read() == 1:
            return 0b11     # Load-use hazard occured
        elif ra2e.read() == ra3m.read() and regwrm.read() == 1:
            return 0b10     # Register-use hazard occured
        elif ra2e.read() == ra3w.read() and regwrw.read() == 1:
            return 0b01     # Register-use hazard occured
        else:
            return 0b00     # No hazard occured


    @staticmethod
    def _generate_fwds(ra3m, ra3w, memwrm):
        # If pipeline processor does not work - check the code below
        if ra3m.read() == ra3w.read() and memwrm == 1:
            return 1        # Use-store hazard
        else:
            return 0        # No use-store hazard


    @staticmethod
    def _generate_stalld(ra1d, ra2d, ra3e, regsrce):
        # If pipeline processor does not work - check the code below
        if ((ra1d.read() == ra3e.read() or ra2d.read() == ra3e.read()) 
                and regsrce.read() == 1):
            return 1        # Load-use hazard occured
        else:
            return 0        # No load-use hazard detected


    @staticmethod
    def _generate_flushd(pcsrcd):
        # If pipeline processor does not work - check the code below
        if pcsrcd.read() == 0:
            return 1        # Branch hazard occured
        else:
            return 0        # No branch hazard occured


    @staticmethod
    def _generate_flushe():
        '''
        Method is not implemented because branch hazards are being detected in
        the decode stage
        '''
        pass


    def run(self, time = None):
        "Timestep handler function computes control output given instruction"

        # Read inputs
        ra1d = self._ra1d
        ra2d = self._ra2d
        ra1e = self._ra1e
        ra2e = self._ra2e
        ra3e = self._ra3e
        ra3m = self._ra3m
        ra3w = self._ra3w
        regwrm = self._regwrm
        regwrw = self._regwrw
        regsrce = self._regsrce
        regsrcw = self._regsrcw
        memwrm = self._memwrm
        pcsrcd = self._pcsrcd

        # Generate control outputs
        self._fwda.write(self._generate_fwda(ra1e, ra3m, ra3w, regwrm, regwrw, regsrcw))
        self._fwdb.write(self._generate_fwdb(ra2e, ra3m, ra3w, regwrm, regwrw, regsrcw))
        self._fwds.write(self._generate_fwds(ra3m, ra3w, memwrm))
        self._stalld.write(self._generate_stalld(ra1d, ra2d, ra3e, regsrce))
        self._flushd.write(self._generate_flushd(pcsrcd))
        self._flushe.write(self._generate_flushe())


    def inspect(self):
        "Return message noting that this controller does not not contain state"
        return {'type': 'hazard-controller', 'state': None}


    def modify(self, data = None):
        "Return message noting that this controller does not contain state"
        return {'error': 'hazard controller cannot be modified'}