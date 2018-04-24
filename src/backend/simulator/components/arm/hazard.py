"""
Hazard controller for ARM v4 Pipeline Processor
"""

from simulator.components.abstract.ibus import iBusRead, iBusWrite


class HazardController():
    """
    Hazard Controller - Handles hazards that occur in the top level
    pipeline architecture
    """

    def __init__(self, ra1e, ra2e, ra3e, ra3m, ra3w, regwrm,
                 regwrw, regsrcm, regsrcw, memwrm, pcsrcd, fwda, fwdb,
                 fwds, stallf, flushf, flushd):
        """
        inputs:
            ra1e: register number
            ra2e: register number
            ra3e: register number
            ra3m: register number
            ra3w: register number
            regwrm: selects whether to write back to the regfile
            regwrw: selects whether to write back to the regfile
            regsrcm: selects whether the alu output or data memory is feedback
            regsrcw: selects whether the alu output or data memory is feedback
            memwrm: selects whether to write to memory
            pcsrcd: selects the instruction given to the fetch stage
        outputs:
            fwda: fowarding for the a input of the alu
            fwdb: fowarding for the b input of the alu
            fwds: fowarding for data memory
            stallf: stalls the pipeline
            flushf: clears the pipeline
            flushd: NOT USED
        """
        # Inputs
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
        if not isinstance(regsrcm, iBusRead):
            raise TypeError('The regsrcm bus must be readable')
        elif regsrcm.size() != 1:
            raise ValueError('The regsrcm bus must have a size of 1 bit')
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

        self._ra1e = ra1e
        self._ra2e = ra2e
        self._ra3e = ra3e
        self._ra3m = ra3m
        self._ra3w = ra3w
        self._regwrm = regwrm
        self._regwrw = regwrw
        self._regsrcm = regsrcm
        self._regsrcw = regsrcw
        self._memwrm = memwrm
        self._pcsrcd = pcsrcd

        # Outputs
        if not isinstance(fwda, iBusWrite):
            raise TypeError('The fwda bus must be writable')
        elif fwda.size() != 3:
            raise ValueError('The fwda bus must have a size of 3 bits')
        if not isinstance(fwdb, iBusWrite):
            raise TypeError('The fwdb bus must be writable')
        elif fwdb.size() != 3:
            raise ValueError('The fwdb bus must have a size of 3 bits')
        if not isinstance(fwds, iBusWrite):
            raise TypeError('The fwds bus must be writable')
        elif fwds.size() != 1:
            raise ValueError('The fwds bus must have a size of 1 bit')
        if not isinstance(stallf, iBusWrite):
            raise TypeError('The stalld bus must be writable')
        elif stallf.size() != 1:
            raise ValueError('The stalld bus must have a size of 1 bit')
        if not isinstance(flushf, iBusWrite):
            raise TypeError('The flushd bus must be writable')
        elif flushf.size() != 1:
            raise ValueError('The flushd bus must have a size of 1 bit')
        if not isinstance(flushd, iBusWrite):
            raise TypeError('The flushe bus must be writable')
        elif flushd.size() != 1:
            raise ValueError('The flushe bus must have a size of 1 bit')

        self._fwda = fwda
        self._fwdb = fwdb
        self._fwds = fwds
        self._stallf = stallf
        self._flushf = flushf
        self._flushd = flushd

    @staticmethod
    def _generate_fwda(ra1e, ra3m, ra3w, regwrm, regwrw, regsrcm, regsrcw):
        """
        Forward hazard control for the a input of the alu in the case of a
        register-use hazard
        """
        if (ra1e.read() == ra3m.read() and regwrm.read() == 1
                and regsrcm.read() != 0):
            return 0b010    # Register-use hazard occured
        elif (ra1e.read() == ra3w.read() and regwrw.read() == 1
                and regsrcw.read() != 0):
            return 0b001    # Register-use hazard occured
        elif ra1e.read() == ra3m.read() and regsrcm.read() == 0:
            return 0b011    # Load-use hazard occured (in mem)
        elif ra1e.read() == ra3w.read() and regsrcw.read() == 0:
            return 0b100    # Load-use hazard occured (in wb)
        else:
            return 0b000    # No hazard occured

    @staticmethod
    def _generate_fwdb(ra2e, ra3m, ra3w, regwrm, regwrw, regsrcm, regsrcw):
        """
        Forward hazard control for the b input of the alu in the case of a
        register-use hazard
        """
        if (ra2e.read() == ra3m.read() and regwrm.read() == 1
                and regsrcm.read() != 0):
            return 0b010    # Register-use hazard occured
        elif (ra2e.read() == ra3w.read() and regwrw.read() == 1
                and regsrcw.read() != 0):
            return 0b001    # Register-use hazard occured
        elif ra2e.read() == ra3m.read() and regsrcm.read() == 0:
            return 0b011    # Load-use hazard occured (in mem)
        elif ra2e.read() == ra3w.read() and regsrcw.read() == 0:
            return 0b100    # Load-use hazard occured (in wb)
        else:
            return 0b000    # No hazard occured

    @staticmethod
    def _generate_fwds(ra3m, ra3w, memwrm):
        "Forward hazard control in the case of a use-store hazard"
        if ra3m.read() == ra3w.read() and memwrm.read() == 1:
            return 1        # Use-store hazard
        else:
            return 0        # No use-store hazard

    @staticmethod
    def _generate_stallf(pcsrcd):
        "Prevents the outputs of the ifid register from changing value"
        if pcsrcd.read() == 2:
            return 1
        else:
            return 0

    @staticmethod
    def _generate_flushf(pcsrcd, ra3e):
        "Sets the outputs of the ifid register to 0"
        if pcsrcd.read() == 0 or (pcsrcd.read() == 2 and ra3e.read() == 0xF):
            return 1        # Branch hazard occured
        else:
            return 0        # No branch hazard occured

    @staticmethod
    def _generate_flushd():
        """
        Method returns 0 because branch hazards are being detected in
        the decode stage
        """
        return 0

    def run(self, time=None):
        "Timestep handler function computes control output given instruction"

        # Read inputs
        ra1e = self._ra1e
        ra2e = self._ra2e
        ra3e = self._ra3e
        ra3m = self._ra3m
        ra3w = self._ra3w
        regwrm = self._regwrm
        regwrw = self._regwrw
        regsrcm = self._regsrcm
        regsrcw = self._regsrcw
        memwrm = self._memwrm
        pcsrcd = self._pcsrcd

        # Generate control outputs
        self._fwda.write(self._generate_fwda(ra1e, ra3m, ra3w, regwrm, regwrw,
                                             regsrcm, regsrcw))
        self._fwdb.write(self._generate_fwdb(ra2e, ra3m, ra3w, regwrm, regwrw,
                                             regsrcm, regsrcw))
        self._fwds.write(self._generate_fwds(ra3m, ra3w, memwrm))
        self._stallf.write(self._generate_stallf(pcsrcd))
        self._flushf.write(self._generate_flushf(pcsrcd, ra3e))
        self._flushd.write(self._generate_flushd())

    def inspect(self):
        "Return message noting that this controller does not not contain state"
        return {'type': 'hazard-controller', 'state': None}

    def modify(self, data=None):
        "Return message noting that this controller does not contain state"
        return {'error': 'hazard controller cannot be modified'}

    @classmethod
    def from_dict(cls, config, hooks):
        "Implements conversion from configuration to component"
        return HazardController(hooks[config["ra1e"]],hooks[config["ra2e"]],
                                hooks[config["ra3e"]],hooks[config["ra3w"]],
                                hooks[config["regwrm"]],hooks[config["regwrw"]],
                                hooks[config["regsrcm"]],hooks[config["regsrcw"]],
                                hooks[config["memwrm"]],hooks[config["pcsrcd"]],
                                hooks[config["fwda"]],hooks[config["fwdb"]],
                                hooks[config["fwds"]],hooks[config["stallf"]],
                                hooks[config["flushf"]],hooks[config["flushd"]])
