from components.abstract.controller import Controller
from components.abstract.controller import iBusRead, iBusWrite

class ControllerSingleCycle(Controller):

    def __init__(self, cond, op, funct, rd, bit4, c, v, n, z, pcsrc, pcwr, regsa,
                regdst, regwrs, regwr, exts, alusrcb, alus, aluflagwr, memwr, regsrc, wd3s):
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
        self._wd3s = wd3s

    def run(self, time):
        # pcsrc
        if self._op.read() == 0b10 and (self._cond.read() == 0b110 or self._cond.read() == 0b0000 or self._cond.read() == 0b0001):
            self._pcsrc.write(0b00)
        elif self._op.read() == 0b00 and self._rd == 0b1111:
            self._pcsrc.write(0b10)
        else:
            self._pcsrc.write(0b01)
        # pcwr - Always a 1 for the single cycle processor
        self._pcwr.write(0b1)
        #regsa
        if self._op.read() == 0b00 and self._bit4.read() == 0b1 and (self._funct.read() == 0b000000 or self._funct.read() == 0b000001):
            self._regsa.write(0b0)
        else:
            self._regsa.write(0b1)
        #regdst
        if self._op.read() == 0b01 and self._funct.read() == 0b011000:
            self._regdst.write(0b10)
        elif self._op.read() == 0b00 and self._bit4.read() == 0b1 and (self._funct.read() == 0b000000 or self._funct.read() == 0b000001):
            self._regdst.write(0b00)
        else:
            self._regdst.write(0b01)
        # regwrs
        if self._op.read() == 0b10 and ((self._funct.read() >> 4) == 0b01 or (self._funct.read() >> 4) == 0b11):
            self._regwrs.write(0b10)
        elif self._op.read() == 0b00 and self._bit4.read() == 0b1 and (self._funct.read() == 0b000000 or self._funct.read() == 0b000001):
            self._regwrs.write(0b00)
        else:
            self._regwrs.write(0b01)
        # regwr
        if self._op.read() == 0b00 and (self._funct.read() == 0b010101 or self._funct.read() == 0b110101):
            self._regwr.write(0b0)
        elif self._op.read() == 0b01 and self._funct.read() == 0b011000:
            self._regwr.write(0b0)
        elif self._op.read() == 0b10 and ((self._funct.read() >> 4) == 0b01 or (self._funct.read() >> 4) == 0b11):
            self._regwr.write(0b0)
        else:
            self._regwr.write(0b1)
        # exts
        if self._op.read() == 0b10:
            self._exts.write(0b10)
        elif self._op.read() == 0b01 and (self._funct.read() == 0b011000 or self._funct.read() == 0b011001):
            self._exts.write(0b01)
        else:
            self._exts.write(0b00)
        # alusrcb
        if self._op.read() == 0b00:
            if (self._funct.read() == 0b000000 or self._funct.read() == 0b000010 or
                    self._funct.read() == 0b000100 or self._funct.read() == 0b000110 or
                    self._funct.read() == 0b001000 or self._funct.read() == 0b001010 or
                    self._funct.read() == 0b001110 or self._funct.read() == 0b010001 or
                    self._funct.read() == 0b010011 or self._funct.read() == 0b010101 or
                    self._funct.read() == 0b010111 or self._funct.read() == 0b011000 or
                    self._funct.read() == 0b011000 or self._funct.read() == 0b011010 or
                    self._funct.read() == 0b011100 or self._funct.read() == 0b011110 or
                    self._funct.read() == 0b000001 or self._funct.read() == 0b000011 or
                    self._funct.read() == 0b000101 or self._funct.read() == 0b000111 or
                    self._funct.read() == 0b001001 or self._funct.read() == 0b001011 or
                    self._funct.read() == 0b011011 or self._funct.read() == 0b011101 or
                    self._funct.read() == 0b011111):
                self._alusrcb.write(0b1)
            elif self._bit4.read() == 0b1 and (self._funct.read() == 0b000000 or self._funct.read() == 0b000001):
                self._alusrcb.write(0b1)
            else:
                self._alusrcb.write(0b0)
        # alus
        if (self._op.read() == 0b00 and (self._funct.read() == 0b001000 or
                self._funct.read() == 0b101000 or self._funct.read() == 0b001001 or
                self._funct.read() == 0b101001)):
            self._alus.write(0b0000)
        elif (self._op.read() == 0b10 and (self._funct.read() == 0b011000 or
                self._funct.read() == 0b011001)):
            self._alus.write(0b0000)
        elif (self._op.read() == 0b00 and (self._funct.read() == 0b000100 or
                self._funct.read() == 0b100100 or self._funct.read() == 0b010101 or
                self._funct.read() == 0b110101 or self._funct.read() == 0b000101 or
                self._funct.read() == 0b100101)):
            self._alus.write(0b0001)
        elif (self._op.read() == 0b00 and (self._funct.read() == 0b000000 or
                self._funct.read() == 0b100000 or self._funct.read() == 0b100001 or
                self._funct.read() == 0b100001)):
            self._alus.write(0b0010)
        elif (self._op.read() == 0b00 and (self._funct.read() == 0b011000 or
                self._funct.read() == 0b111000 or self._funct.read() == 0b011001 or
                self._funct.read() == 0b111001)):
            self._alus.write(0b0011)
        elif (self._op.read() == 0b00 and (self._funct.read() == 0b000010 or
                self._funct.read() == 0b100010 or self._funct.read() == 0b000011 or
                self._funct.read() == 0b100011)):
            self._alus.write(0b0100)
        elif (self._op.read() == 0b00 and (self._funct.read() == 0b011010 or
                self._funct.read() == 0b111010 or self._funct.read() == 0b011011 or
                self._funct.read() == 0b111011)):
            self._alus.write(0b0110)
        elif (self._op.read() == 0b00 and self._bit4.read() == 0b1 and (self._funct.read() == 0b000000 or
                self._funct.read() == 0b000001)):
            self._alus.write(0b0111)
        else:
            self._alus.write(0b1111)
        # aluflagwr
        if self._op.read() == 0b00:
            if (self._funct.read() == 0b010101 or self._funct.read() == 0b110101 or
                    self._funct.read() == 0b010101 or self._funct.read() == 0b110101 or
                    self._funct.read() == 0b000001 or self._funct.read() == 0b100001 or
                    self._funct.read() == 0b000011 or self._funct.read() == 0b100011 or
                    self._funct.read() == 0b000101 or self._funct.read() == 0b100101 or
                    self._funct.read() == 0b000111 or self._funct.read() == 0b100111 or
                    self._funct.read() == 0b001001 or self._funct.read() == 0b101001 or
                    self._funct.read() == 0b001011 or self._funct.read() == 0b101011 or
                    self._funct.read() == 0b001111 or self._funct.read() == 0b101111 or
                    self._funct.read() == 0b010001 or self._funct.read() == 0b110001 or
                    self._funct.read() == 0b010011 or self._funct.read() == 0b110011 or
                    self._funct.read() == 0b010111 or self._funct.read() == 0b110111 or
                    self._funct.read() == 0b011001 or self._funct.read() == 0b111001 or
                    self._funct.read() == 0b011011 or self._funct.read() == 0b111011 or
                    self._funct.read() == 0b011101 or self._funct.read() == 0b111101 or
                    self._funct.read() == 0b011111 or self._funct.read() == 0b111111 or
                    (self._funct.read() == 0b000001 and self._bit4.read() == 0b1)):
                self._aluflagwr.write(0b1)
            else:
                self._aluflagwr.write(0b0)
        # memwr
        if self._op.read() == 0b01 and self._funct.read() == 0b011000:
            self._memwr.write(0b1)
        else:
            self._memwr.write(0b0)
        #regsrc
        if self._op.read() == 0b10 and self._funct.read() == 0b011001:
            self._regsrc.write(0b0)
        else:
            self._regsrc.write(0b1)
        #wd3s
        if self._op.read() == 0b10 and ((self._funct.read() >> 4) == 0b01 or (self._funct.read() >> 4) == 0b11):
            self._wd3s.write(1)
        else:
            self._wd3s.write(0)


    def inspect(self):
        return {'type': 'sc-controller', 'cond': self._cond.read(), 'op': self._op.read(), 
                'funct': self._funct.read(), 'rd': self._rd.read(), 'bit4': self._bit4.read(), 
                'c': self._c.read(), 'v': self._v.read(), 'n': self._n.read(), 'z': self._z.read(),
                'pcsrc': self._pcsrc.read(), 'pcwr': self._pcwr.read(), 'regsa': self._regsa.read(),
                'regdst': self._regdst.read(), 'regwrs': self._regwrs.read(),
                'regwr': self._regwr.read(), 'exts': self._exts.read(), 
                'alusrcb': self._alusrcb.read(), 'alus': self._alus.read(), 
                'aluflagwr': self._aluflagwr.read(), 'memwr': self._memwr.read(), 
                'regsrc': self._regsrc.read(), 'wd3s': self._wd3s.read()}

    def modify(self, data=None):
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
