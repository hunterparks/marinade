from components.abstract.combinational import Combinational
from components.abstract.ibus import iBusRead, iBusWrite

class Alu(Combinational):
    def __init__(self, a, b, alus, f, c, v, n, z):
        if not isinstance(a, iBusRead) or a.size() != 32:
            raise ValueError("The a bus must have a size of 32-bits.")
        if not isinstance(b, iBusRead) or b.size() != 32:
            raise ValueError('The b bus must have a size of 32-bits')
        if not isinstance(alus, iBusRead) or alus.size() != 4:
            raise ValueError('The alus bus must have a size of 4-bits')
        if not isinstance(f, iBusWrite) or f.size() != 32:
            raise ValueError('The f bus must have a size of 32-bits')
        if not isinstance(c, iBusWrite) or c.size() != 1:
            raise ValueError('The c bus must have a size of 1-bit')
        if not isinstance(v, iBusWrite) or v.size() != 1:
            raise ValueError('The v bus must have a szie of 1-bit')
        if not isinstance(n, iBusWrite) or n.size() != 1:
            raise ValueError('The n bus must have a size of 1-bit')
        if not isinstance(z, iBusWrite) or z.size() != 1:
            raise ValueError('The z bus must have a size of 1-bit')
        self._a = a
        self._b = b
        self._alus = alus
        self._f = f
        self._c = c
        self._v = v
        self._n = n
        self._z = z

    def run(self, time = None):
        if self._alus.read() == 0:
            # bitwise add
            self._f.write((self._a.read() + self._b.read()) & (2**32 - 1))
            self.carry()
            self.signed_overflow('add')
        elif self._alus.read() == 1:
            # bitwise subtract
            self._f.write((self._a.read() - self._b.read()) & (2**32 - 1))
            self.carry()
            self.signed_overflow('sub')
        elif self._alus.read() == 2:
            # bitwise and
            self._f.write(self._a.read() & self._b.read())
        elif self._alus.read() == 3:
            # bitwise or
            self._f.write(self._a.read() | self._b.read())
        elif self._alus.read() == 4:
            # bitwise xor
            self._f.write(self._a.read() ^ self._b.read())
        elif self._alus.read() == 5:
            # bitwise pass a
            self._f.write(self._a.read())
        elif self._alus.read() == 6:
            # bitwise pass b
            self._f.write(self._b.read())
        elif self._alus.read() == 7:
            # bitwise multiplication
            self._f.write(self._a.read() * self._b.read())
            self.signed_overflow('mul')
        else:
            # generate 1
            self._f.write(1)
        # negative
        self._n.write(self._f.read() >> 31)
        # zero
        if self._f.read() == 0:
            self._z.write(1)
        else:
            self._z.write(0)
            
    def carry(self):
        if self._a.read() >> 31 and self._b.read() >> 31:
            self._c.write(1)
        else:
            self._c.write(0)

    def signed_overflow(self, operation):
        if operation == 'add':
            if self._a.read() >> 31 == self._b.read() >> 31:
                if self._f.read() >> 31 != self._a.read() >> 31:
                    self._v.write(1)
            else:
                self._v.write(0)
        elif operation == 'subtract' or operation == 'sub':
            if self._a.read() >> 31 != self._b.read() >> 31:
                if self._f.read() >> 31 == self._b.read() >> 31:
                    self._v.write(1)
            else:
                self._v.write(0)
        elif operation == 'multiply' or operation == 'mul':
            if self._a.read() >> 31 == self._b.read() >> 31 and self._a.read() >> 31 == 0:
                if self._f.read() >> 31 != self._a.read() >> 31:
                    self._v.write(1)
            elif self._a.read() >> 31 == self._b.read() >> 31 and self._a.read() >> 31 == 1:
                if self._f.read() >> 31 == self._a.read() >> 31:
                    self._v.write(1)
            else:
                self._v.write(0)