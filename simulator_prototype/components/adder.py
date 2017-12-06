from components.bus import Bus
from components.logic_input import LogicInput
from components.abstract.combinational import Combinational

class Adder(Combinational):

    def __init__(self, name, size, a_bus, b_bus, y_bus, carry):
        self._name = name
        self._size = size
        self._a = a_bus
        self._b = b_bus
        self._y = y_bus
        self._carry = carry

    def run(self):
        y = (self._a.read() + self._b.read())
        c = 1 if y / (2**self._size) else 0
        self._y.write(y % 2**self._size)
        self._carry.write(c)
