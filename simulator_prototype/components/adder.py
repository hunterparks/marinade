from components.abstract.ibus import iBusRead, iBusWrite
from components.bus import Bus
from components.logic_input import LogicInput
from components.abstract.combinational import Combinational

class Adder(Combinational):

    #TODO enforce bus size rules
    def __init__(self, name, size, a_bus, b_bus, y_bus=None, carry=None):
        if not isinstance(name,str) or size <= 0 :
            raise ValueError('Initialization parameters invalid')
        self._name = name
        self._size = size

        if not isinstance(a_bus,iBusRead) or not isinstance(b_bus,iBusRead):
            raise ValueError('Input buses must be readable')
        self._a = a_bus
        self._b = b_bus

        if not isinstance(y_bus,iBusWrite) and not y_bus is None:
            raise ValueError('If output bus defined then must be writable')
        self._y = y_bus

        if not isinstance(carry,iBusWrite) and not carry is None:
            raise ValueError('If carry bus defined then must be writable')
        self._carry = carry

    #TODO do check on size to prevent a larger than allowed values
    def run(self):
        y = (self._a.read() + self._b.read())
        c = 1 if y / (2**self._size) else 0

        if not self._y is None:
            self._y.write(y % 2**self._size)
        if not self._carry is None:
            self._carry.write(c)
