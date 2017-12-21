from components.abstract.combinational import Combinational
from components.abstract.ibus import iBusRead, iBusWrite

class Alu(Combinational):
    def __init__(self, a, b, alus, f, c, v, n, z):
        if a.size() != 32:
            raise ValueError("The a bus must have a size of 32-bits.")
        if b.size() != 32:
            raise ValueError('The b bus must have a size of 32-bits')
        if alus.size() != 4:
            raise ValueError('The alus bus must have a size of 4-bits')
        if f.size() != 32:
            raise ValueError('The f bus must have a size of 32-bits')
        if c.size() != 1:
            raise ValueError('The c bus must have a size of 1-bit')
        if v.size() != 1:
            raise ValueError('The v bus must have a szie of 1-bit')
        if n.size() != 1:
            raise ValueError('The n bus must have a size of 1-bit')
        if z.size() != 1:
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
        result = 0
<<<<<<< HEAD
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
        else:
            # generate 1
            self._f.write(1)
=======
        if self._alus.read() == 0: # bitwise add
            result = (self._a.read() + self._b.read()) & (2**32 - 1)
        elif self._alus.read() == 1: # bitwise subtract
            result = (self._a.read() - self._b.read()) & (2**32 - 1)
        elif self._alus.read() == 2: # bitwise and
            result = self._a.read() & self._b.read()
        elif self._alus.read() == 3: # bitwise or
            result = self._a.read() | self._b.read()
        elif self._alus.read() == 4: # bitwise xor
            result = self._a.read() ^ self._b.read()
        elif self._alus.read() == 5: # bitwise pass a
            result = self._a.read()
        elif self._alus.read() == 6: # bitwise pass b
            result = self._b.read()
        else: # generate 1
            result = 1
        self._f.write(result)

        # the following bits are used to determine when to branch
>>>>>>> 172637a9e01904bbec4048de9b474f9d22a7e9c0
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
        if operation == 'subtract' or operation == 'sub':
            if self._a.read() >> 31 != self._b.read() >> 31:
                if self._f.read() >> 31 == self._b.read() >> 31:
                    self._v.write(1)
            else:
                self._v.write(0)