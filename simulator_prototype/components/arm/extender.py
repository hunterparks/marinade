"""

"""

from components.abstract.combinational import Combinational
from components.abstract.ibus import iBusRead, iBusWrite

class Extender(Combinational):
    """

    """

    def __init__(self, imm, exts, imm32):
        """
        inputs:
            imm: 24-bit immediate
            exts: extender control signal
        output:
            imm32: resulting 32-bit immediate
        """

        if not isinstance(imm, iBusRead):
            raise TypeError('The imm bus must be readable')
        elif imm.size() != 24:
            raise ValueError('The imm bus must have a size of 24-bits')
        if not isinstance(exts, iBusRead):
            raise TypeError('The exts bus must be readable')
        elif exts.size() != 2:
            raise ValueError('The exts bus must have a size of 2-bits')
        if not isinstance(imm32, iBusWrite):
            raise TypeError('The imm32 bus must be writable')
        elif imm32.size() != 32:
            raise ValueError('The imm32 bus must have a size of 32-bits')
        self._imm = imm
        self._exts = exts
        self._imm32 = imm32

    def run(self, time = None):
        """
        exts = 0 for data processing instructions
        exts = 1 for load and store instructions
        exts = 2 or 3 for branch instructions
        """

        # keep only the 8 most least significant bits
        if self._exts.read() == 0:
            self._imm32.write(self._imm.read() & 0x000000FF)
        # keep only the 12 most least significant bits
        elif self._exts.read() == 1:
            self._imm32.write(self._imm.read() & 0x00000FFF)
        else:
            # sign extend the immediate and add put 0's in the 2 least significant bits
            new_imm = self._imm.read()
            signed_bit = (0x800000 & new_imm) >> 23
            if signed_bit == 1:
                new_imm = 0x3F000000 | new_imm
            self._imm32.write(new_imm << 2)
