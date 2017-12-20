from components.abstract.combinational import Combinational
from components.abstract.ibus import iBusRead, iBusWrite

class Alu(Combinational):
    def __init__(self, a, b, alus, f, c, v, n, z):
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
        if self._alus.read() == 0:
            # bitwise add
            result = (self._a.read() + self._b.read()) & (2**32 - 1)
        elif self._alus.read() == 1:
            # bitwise subtract
            result = (self._a.read() - self._b.read()) & (2**32 - 1)
        elif self._alus.read() == 2:
            # bitwise and
            result = self._a.read() & self._b.read()
        elif self._alus.read() == 3:
            # bitwise or
            result = self._a.read() | self._b.read()
        elif self._alus.read() == 4:
            # bitwise xor
            result = self._a.read() ^ self._b.read()
        elif self._alus.read() == 5:
            # bitwise pass a
            result = self._a.read()
        elif self._alus.read() == 6:
            # bitwise pass b
            result = self._b.read()
        else:
            # generate 1
            result = 1
        self._f.write(result)

        # the following bits are used to determine when to branch
        # negative
        self._n.write(self._f.read() >> 31)

        # zero
        if self._f.read() == 0:
            self._z.write(1)
        else:
            self._z.write(0)

        # carry (always 0 for now)
        self._c.write(0)

        # signed overflow (always 0 for now)
        self._v.write(0)
