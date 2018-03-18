"""
ARM ALU object for use in ARMv4 architecture
"""

from components.abstract.combinational import Combinational
from components.abstract.ibus import iBusRead, iBusWrite


class Alu(Combinational):
    """
    ALU object operates on a and b word sized inputs. Operations are selected
    through the ALUS control signal. Selectable operations are
        0 add
        1 subtract
        2 and
        3 or
        4 xor
        5 pass a
        6 pass b
        7 multiplication
        8 add with carry
        9 subtract with carry
        10 reverse subtract
        11 reverse subtract with carry
        12 and not
        13 generate 0 (for future)
        14 generate 0
        15 generate 1
    The functional result (word size) along with various condition flags are
    outputed. An external register is necessary to maintain state of condition
    signals.
    """

    SHIFTOP_LL = 0          # B << SH
    SHIFTOP_LR = 1          # B >> SH
    SHIFTOP_AR = 2          # (+-) B >> SH
    SHIFTOP_RR = 3          # B[32 to SH] >> SH | B[SH to 0] << (32 - SH)

    ALUS_ADD_CMD = 0        # F = A + B
    ALUS_SUB_CMD = 1        # F = A - B
    ALUS_AND_CMD = 2        # F = A & B
    ALUS_OR_CMD = 3         # F = A | B
    ALUS_XOR_CMD = 4        # F = A ^ B
    ALUS_A_CMD = 5          # F = A
    ALUS_B_CMD = 6          # F = B
    ALUS_MUL_CMD = 7        # F = A * B
    ALUS_ADD_W_C_CMD = 8    # F = A + B + Cin
    ALUS_SUB_W_C_CMD = 9    # F = A - B - Cin
    ALUS_RSB_CMD = 10       # F = B - A
    ALUS_RSB_W_C_CMD = 11   # F = B - A - Cin
    ALUS_AND_NOT_CMD = 12   # F = A & ~B
    ALUS_NOT_B_CMD = 13     # F = ~B
    ALUS_GEN_0_CMD = 14     # F = 0
    ALUS_GEN_1_CMD = 15     # F = 1

    def __init__(self, a, b, ar, alus, shift, cin, shiftOp, shiftCtrl, accEn, f, cout, v, n, z):
        """
        inputs:
            a: 32-bit input to the alu
            b: 32-bit input to the alu
            ar: 32-bit input to alu either for barrel shifting or as accumulate
            alus: 4-bit control signal for the alu
            shift: 5-bit barrel shift value
            cin: carry bit
            shiftOp: commands the barrel shifter on b to perform operation
            shiftCtrl: control signal to either perform shift or not
                        B(0) is enable bit, shift on [1] disable on [0]
                        B(1) is select either register [1] or constant shift [0]
            accEn: accumulate enable add ar to alu result before f if [1]
        outputs:
            f: 32-bit output to the alu
            cout: carry bit
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
        if not isinstance(ar, iBusRead):
            raise TypeError('The ar bus must be readable')
        elif ar.size() != 32:
            raise ValueError('The ar bus must have a size of 32-bits')
        if not isinstance(alus, iBusRead):
            raise TypeError('The alus bus must be readable')
        elif alus.size() != 4:
            raise ValueError('The alus bus must have a size of 4-bits')
        if not isinstance(shift, iBusRead):
            raise TypeError('The shift bus must be readable')
        elif shift.size() != 5:
            raise ValueError('The shift bus must have a size of 5-bits')
        if not isinstance(cin, iBusRead):
            raise TypeError('The cin bus must be readable')
        elif cin.size() != 1:
            raise ValueError('The cin bus must have a size of 1-bit')
        if not isinstance(shiftOp, iBusRead):
            raise TypeError('The shiftOp bus must be readable')
        elif shiftOp.size() != 2:
            raise ValueError('The shiftOp bus must have a size of 2-bits')
        if not isinstance(shiftCtrl, iBusRead):
            raise TypeError('The shiftCtrl bus must be readable')
        elif shiftCtrl.size() != 2:
            raise ValueError('The shiftCtrl bus must have a size of 2-bit')
        if not isinstance(accEn, iBusRead):
            raise TypeError('The accEn bus must be readable')
        elif accEn.size() != 1:
            raise ValueError('The accEn bus must have a size of 1-bit')
        if not isinstance(f, iBusWrite):
            raise TypeError('The f bus must be writeable')
        elif f.size() != 32:
            raise ValueError('The f bus must have a size of 32-bits')
        if not isinstance(cout, iBusWrite):
            raise TypeError('The cout bus must be writable')
        elif cout.size() != 1:
            raise ValueError('The cout bus must have a size of 1-bit')
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
        self._ar = ar
        self._alus = alus
        self._sh = shift
        self._shop = shiftOp
        self._shcr = shiftCtrl
        self._cin = cin
        self._accEn = accEn
        self._f = f
        self._cout = cout
        self._v = v
        self._n = n
        self._z = z

    @staticmethod
    def _generate_f(alus, a, b, cin):
        """
        ALU result computed as indicated for the enumerated control signal.
        Note most significant bit triggers a write 1 regardless of lower bits.

        Returns 33-bit number (MSB is carry)
        """
        if alus == Alu.ALUS_ADD_CMD:
            return (a + b) & (2**33 - 1)
        elif alus == Alu.ALUS_SUB_CMD:
            return (a - b) & (2**33 - 1)
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
            return (a * b) & (2**33 - 1)
        elif alus == Alu.ALUS_ADD_W_C_CMD:
            return (a + b + cin) & (2**33 - 1)
        elif alus == Alu.ALUS_SUB_W_C_CMD:
            return (a - b - (~cin)%2) & (2**33 - 1)
        elif alus == Alu.ALUS_RSB_CMD:
            return (b - a) & (2**33 - 1)
        elif alus == Alu.ALUS_RSB_W_C_CMD:
            return (b - a - (~cin)%2) & (2**33 - 1)
        elif alus == Alu.ALUS_AND_NOT_CMD:
            return a & (~b)
        elif alus == Alu.ALUS_NOT_B_CMD:
            return (~b) & (2**33 - 1)
        elif alus == Alu.ALUS_GEN_0_CMD:
            return 0
        elif alus == Alu.ALUS_GEN_1_CMD:
            return 1
        else:  # error case
            return 0

    @staticmethod
    def _generate_c(alus, f):
        """
        Carry result is 1 if overflow occurred during operation (add, sub)
        else 0.
        """
        operation = (alus == Alu.ALUS_ADD_CMD or alus == Alu.ALUS_SUB_CMD
                     or alus == Alu.ALUS_ADD_W_C_CMD or alus == Alu.ALUS_SUB_W_C_CMD
                     or alus == Alu.ALUS_RSB_CMD or alus == Alu.ALUS_RSB_W_C_CMD)
        return 1 if operation and (f & (2**33-1)) >> 32 else 0

    @staticmethod
    def _generate_v(alus, a, b, f):
        """
        Signed overflow returns 1 if during operation a sign change occurs
        else 0.
        """
        retval = 0
        a_msb = (a & 0x80000000) >> 31
        b_msb = (b & 0x80000000) >> 31
        f_msb = (f & 0x80000000) >> 31

        add_operation = (alus == Alu.ALUS_ADD_CMD or alus == Alu.ALUS_ADD_W_C_CMD)
        sub_operation = (alus == Alu.ALUS_SUB_CMD or alus == Alu.ALUS_SUB_W_C_CMD
                         or alus == Alu.ALUS_RSB_CMD or alus == Alu.ALUS_RSB_W_C_CMD)

        if add_operation and a_msb == b_msb and f_msb != a_msb:
            retval = 1
        elif sub_operation and a_msb != b_msb and f_msb == b_msb:
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

    def _barrel_shift(self, b, shift, shop):
        """
        Barrel shifter follows enumarated shift commands to follow extension
        and fill requirements.
        Result is 32-bit value
        """
        if shop == self.SHIFTOP_LL:
            retval = b << shift
        elif shop == self.SHIFTOP_LR:
            retval = b >> shift
        elif shop == self.SHIFTOP_AR:
            if b < (1 << 31):
                retval = b >> shift
            else:
                retval = (-1 * (((~b) & (2**32 - 1)) + 1)) >> shift
        elif shop == self.SHIFTOP_RR:
            retval = b
            for i in range(0, shift):
                temp = retval & 1
                retval = (retval >> 1) | (temp << 31)
        else:
            retval = b
        return (retval) & (2**32 - 1)

    def run(self, time=None):
        "implements run functionality for the alu"

        # sample input signals
        a = self._a.read()
        b = self._b.read()
        alus = self._alus.read()
        shift = self._sh.read()
        cin = self._cin.read()

        # barrel shift on b either register or immediate
        if (self._shcr.read() & 0x1) == 1:
            if (self._shcr.read() & 0x2) == 0x2:
                sh = self._ar.read() & 0xFF
            else:
                sh = self._sh.read()
            b = self._barrel_shift(b, sh, self._shop.read())

        # calculate ALU result
        f = self._generate_f(alus, a, b, cin)

        # accumulate
        if self._accEn.read():
            f += self._ar.read()

        # output computed output signals
        self._f.write(f & (2**32 - 1))
        self._cout.write(self._generate_c(alus, f))
        self._v.write(self._generate_v(alus, a, b, self._f.read()))
        self._n.write(self._generate_n(self._f.read()))
        self._z.write(self._generate_z(self._f.read()))
