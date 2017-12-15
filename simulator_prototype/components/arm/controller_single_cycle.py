from components.abstract.controller import Controller
from components.abstract.controller import iBusRead, iBusWrite

class ControllerSingleCycle(Controller):

    def __init__(self, cond, op, funct, rd, bit4, c, v, n, z, pcsrc, pcwr, regsa,
                regdst, regwrs, regwr, exts, alusrcb, alus, aluflagwr, memwr, regsrc, wdbs):
        self._cond = cond
        self._op = op
        self._funct = funct
        self._rd = rd
        self._bit4 = bit4
        self._c = c
        self._v = v
        self._n = n
        self._z = z
        self._pcsrc = pcsrc
        self._pcwr = pcwr
        self._regsa = regsa
        self._regdst = regdst
        self._regwrs = regwrs
        self._regwr = regwr
        self._exts = exts
        self._alusrcb = alusrcb
        self._alus = alus
        self._aluflagwr = aluflagwr
        self._memwr = memwr
        self._regsrc = regsrc
        self._wdbs = wdbs

    def run(self,time):
        # pcsrc signal
        if self._op.read() == 0b10 and (self._cond.read() == 0b110 or self._cond.read() == 0b0000 or self._cond.read() = 0b0001):
            self._pcsrc.write(0b00)
        elif self._op.read() == 0b00 and self._rd = 0b1111:
            self._pcsrc.write(0b10)
        else:
            self._pcsrc.write(0b01)

    def inspect(self):
        "Not implemented for single cycle"
        pass

    def modify(self,data=None):
        "Not implemented for single cycle"
        pass

    def on_rising_edge(self):
        "Not implemented for single cycle"
        pass

    def on_falling_edge(self):
        "Not implemented for single cycle"
        pass

    def on_reset(self):
        "Not implemented for single cycle"
        pass
