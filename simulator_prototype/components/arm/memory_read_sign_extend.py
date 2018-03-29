"""
ARM Memory Read extender for use in ARMv4 after reading from memory using
byte or half word modes
"""

from components.abstract.combinational import Combinational
from components.abstract.ibus import iBusRead, iBusWrite


class MemoryReadSignExtender(Combinational):
    """
    Memory Read extender for use in ARMv4 after reading from memory using
    byte or half word modes.

    Takes an input bus of 32-bit length and outputs a 32-bit bus.
    However sign extension overwrites higher bits depending on mode selected.
    """

    def __init__(self, x, s, y):
        """
        inputs:
            x: 32-bit data read from memory
            s: Control signal to either extend or not and what size
                s(0) is enable [1] or disable [0]
                s(1) is size of incomming data [0] = byte, [1] = half-word
        outputs:
            y: resulting 32-bit data from memory with sign consideration
        """

        if not isinstance(x, iBusRead):
            raise TypeError('x bus must be readable')
        elif x.size() != 32:
            raise ValueError('x bus must be 32-bits long')
        if not isinstance(s, iBusRead):
            raise TypeError('s bus must be readable')
        elif s.size() != 2:
            raise ValueError('s bus must be 2-bits long')
        if not isinstance(y, iBusWrite):
            raise TypeError('y bus must be writable')
        elif y.size() != 32:
            raise ValueError('y bus must be 32-bits long')

        self._x = x
        self._s = s
        self._y = y

    def run(self, time=None):
        """
        s(0) = 1 then extend else pass through
        s(1) = 1 then half-word else byte
        """

        x = self._x.read()
        s = self._s.read()

        if s & 0x1 == 0:
            self._y.write(x)
        else:
            if s & 0x2 == 0x2:
                y = x & 0xFFFF
                if y & 0x8000 == 0x8000:
                    y |= (0xFFFF << 16)
                self._y.write(y)
            else:
                y = x & 0xFF
                if y & 0x80 == 0x80:
                    y |= (0xFFFFFF << 8)
                self._y.write(y)

    @classmethod
    def from_dict(cls, config):
        "Implements conversion from configuration to component"
        return NotImplemented

    @classmethod
    def to_dict(cls):
        "Implements conversion from component to configuration"
        return NotImplemented
