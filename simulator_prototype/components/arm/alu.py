"""
ARM ALU object for use in ARMv4 architecture
"""

from components.abstract.combinational import Combinational
from components.abstract.ibus import iBusRead, iBusWrite



class Alu(Combinational):
    """
    ALU object operates on a and b word sized inputs. Operations are selected
    through the ALUS control signal. Selectable operations are
        * add
        * subtract
        * and
        * or
        * xor
        * pass a
        * pass b
        * multiplication
        * generate 1
    The functional result (word size) along with various condition flags are
    outputed. An external register is necessary to maintain state of condition
    signals.
    """

    ALUS_ADD_CMD = 0    # F = A + B
    ALUS_SUB_CMD = 1    # F = A - B
    ALUS_AND_CMD = 2    # F = A & B
    ALUS_OR_CMD  = 3    # F = A | B
    ALUS_XOR_CMD = 4    # F = A ^ B
    ALUS_A_CMD   = 5    # F = A
    ALUS_B_CMD   = 6    # F = B
    ALUS_MUL_CMD = 7    # F = A * B


    def __init__(self, a, b, alus, f, c, v, n, z):
        """
        inputs:
            a: 32-bit input to the alu
            b: 32-bit input to the alu
            alus: 4-bit control signal for the alu
        outputs:
            f: 32-bit output to the alu
            c: carry bit
            v: signed overflow bit
            n: negative bit
            z: zero bit
        """

        if not isinstance(a, iBusRead):
            raise TypeError('The a bus must be readable')
        elif a.size() != 32:
            raise ValueError('The a bus must have a size of 32-bits.')
        if not isinstance(b, iBusRead):
            raise TypeError('The b bus must be readable')
        elif b.size() != 32:
            raise ValueError('The b bus must have a size of 32-bits')
        if not isinstance(alus, iBusRead):
            raise TypeError('The alus bus must be readable')
        elif alus.size() != 4:
            raise ValueError('The alus bus must have a size of 4-bits')
        if not isinstance(f, iBusWrite):
            raise TypeError('The f bus must be writeable')
        elif f.size() != 32:
            raise ValueError('The f bus must have a size of 32-bits')
        if not isinstance(c, iBusWrite):
            raise TypeError('The c bus must be writable')
        elif c.size() != 1:
            raise ValueError('The c bus must have a size of 1-bit')
        if not isinstance(v, iBusWrite):
            raise TypeError('The v bus must be writeable')
        elif v.size() != 1:
            raise ValueError('The v bus must have a szie of 1-bit')
        if not isinstance(n, iBusWrite):
            raise TypeError('The n bus must be writeable')
        elif n.size() != 1:
            raise ValueError('The n bus must have a size of 1-bit')
        if not isinstance(z, iBusWrite):
            raise TypeError('The z bus must be writeable')
        elif z.size() != 1:
            raise ValueError('The z bus must have a size of 1-bit')

        self._a = a
        self._b = b
        self._alus = alus
        self._f = f
        self._c = c
        self._v = v
        self._n = n
        self._z = z


    @staticmethod
    def _generate_f(alus,a,b):
        """
        ALU result computed as indicated for the enumerated control signal.
        Note most significant bit triggers a write 1 regardless of lower bits.
        """
        if alus == Alu.ALUS_ADD_CMD:
            return (a + b) & (2**32 - 1)
        elif alus == Alu.ALUS_SUB_CMD:
            return (a - b) & (2**32 - 1)
        elif alus == Alu.ALUS_AND_CMD:
            return a & b
        elif alus == Alu.ALUS_OR_CMD:
            return a | b
        elif alus == Alu.ALUS_XOR_CMD:
            return a ^ b
        elif alus == Alu.ALUS_A_CMD:
            return a
        elif alus == Alu.ALUS_B_CMD:
            return b
        elif alus == Alu.ALUS_MUL_CMD:
            return (a * b) & (2**32 - 1)
        else: # generate 1
            return 1


    @staticmethod
    def _generate_c(alus,a,b):
        """
        Carry result is 1 if overflow occurred during operation (add, sub)
        else 0.
        """
        operation = (alus == Alu.ALUS_ADD_CMD or alus == Alu.ALUS_SUB_CMD)
        a_msb = ((a & 0x80000000) >> 31)
        b_msb = ((b & 0x80000000) >> 31)
        return 1 if operation and a_msb == 1 and b_msb  == 1 else 0


    @staticmethod
    def _generate_v(alus,a,b,f):
        """
        Signed overflow returns 1 if during operation a sign change occurs
        else 0.
        """
        retval = 0
        a_msb = (a & 0x80000000) >> 31
        b_msb = (b & 0x80000000) >> 31
        f_msb = (f & 0x80000000) >> 31

        if alus == Alu.ALUS_ADD_CMD and a_msb == b_msb and f_msb != a_msb:
            retval = 1
        elif alus == Alu.ALUS_SUB_CMD and a_msb != b_msb and f_msb == b_msb:
            retval = 1
        elif alus == Alu.ALUS_MUL_CMD and a_msb == b_msb:
            if f_msb != a_msb and a_msb == 0:
                retval = 1
            elif f_msb == a_msb and a_msb == 1:
                retval = 1
        else:
            retval = 0

        return retval


    @staticmethod
    def _generate_n(f):
        """
        Result is negative if two's compliment of f msb is 1 else 0
        """
        return (f & 0x80000000) >> 31


    @staticmethod
    def _generate_z(f):
        """
        Result is zero if f is zero
        """
        return 1 if f == 0 else 0


    def run(self, time = None):
        "implements run functionality for the alu"

        #sample input signals
        a = self._a.read()
        b = self._b.read()
        alus = self._alus.read()

        #output computed output signals
        f = self._generate_f(alus,a,b)
        self._f.write(f)
        self._c.write(self._generate_c(alus,a,b))
        self._v.write(self._generate_v(alus,a,b,f))
        self._n.write(self._generate_n(f))
        self._z.write(self._generate_z(f))
