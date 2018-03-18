"""
BusJoin component used to concatenate multiple buses into a single bus
"""

from components.abstract.entity import Entity
from components.abstract.ibus import iBusRead, iBusWrite


class BusJoin(Entity):
    """
    BusJoin concatenates the input buses into a single output bus.
    The output bus will thus have the combined bit-width of all inputs.
    Additionally, the inputs will be concatenated in increasing bit index
    order as traversed through the list.
    """

    def __init__(self, ins_b, out_b):
        "Constructor will check for valid parameters, exception thrown on invalid"

        if not isinstance(ins_b, list) or len(ins_b) <= 0:
            raise TypeError("Inputs must be a list of readables")
        elif not all(isinstance(x, iBusRead) for x in ins_b):
            raise TypeError("Inputs must be a list of readables")
        self._inputs = ins_b

        necessary_size = 0
        for x in ins_b:
            necessary_size += x.size()

        if not isinstance(out_b, iBusWrite):
            raise TypeError("Output must be writable")
        elif not out_b.size() == necessary_size:
            raise ValueError("Output must match combined input size")
        self._output = out_b

    def run(self, time=None):
        "Implements bus join behavior by concatenating inputs in increasing bit order"
        shift = 0
        val = 0
        for i in self._inputs:
            val += i.read() << shift
            shift += i.size()
        self._output.write(val)
