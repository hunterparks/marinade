"""
Multiplexer component is a standalone core component for general
architecture development.
"""

from components.abstract.ibus import iBusRead, iBusWrite
from components.abstract.combinational import Combinational
import math


class Mux(Combinational):
    """
    Mux component implements a combinational multiplexer of fixed bit width.
    Component expects an array of 2 or more input signals that match width.
    Component expects a select input control signal of size sufficent to
    select all inputs but not larger floor(log(len(inputs),2) + 1) = size

    Output follows form:
        Y = I[(S & pow(2,floor(log(len(inputs),2) + 1)))]
    """

    def __init__(self, size, inputs, select, output=None):
        "Constructor will check for valid parameters, exception thrown on invalid"

        if not isinstance(size, int) or size <= 0:
            raise TypeError('Size must be an integer greater than zero')
        self._size = size

        if not isinstance(inputs, list) or not len(inputs) > 1:
            raise TypeError('Inputs must be a list with at least two inputs')
        elif not all((isinstance(x, iBusRead) and x.size() == self._size) for x in inputs):
            raise TypeError('All inputs must be a bus with size equal to internal')
        self._inputs = inputs
        if len(inputs) < 0:
            raise ValueError('Length is less than zero')
        elif len(inputs) == 0:
            self._necessary_select_size = 0
        elif len(inputs) <= 2:
            self._necessary_select_size = len(inputs) - 1
        else:  # len > 2
            self._necessary_select_size = int(math.floor(math.log(len(inputs) - 1, 2) + 1))

        if not isinstance(select, iBusRead):
            raise TypeError('Select signal must be a bus')
        elif not select.size() == self._necessary_select_size:
            raise ValueError('Select signal does not best match input size needed {}'.format(
                self._necessary_select_size))
        self._select = select  # note going to ignore invalid cases with logic

        if not isinstance(output, iBusWrite) and not output is None:
            raise TypeError('Output must be defined as a bus or None')
        elif not output is None and not output.size() == self._size:
            raise ValueError('Output bus size must match internal')
        self._output = output

    def run(self, time=None):
        "Implements n-length mux select functionality with case ignore"

        # process select line
        s = self._select.read() & (2**self._necessary_select_size - 1)

        # select signal to pass to output
        if not self._output is None:
            if s >= len(self._inputs):
                self._output.write(0)  # selected empty entry (odd degree in)
            else:
                self._output.write(self._inputs[s].read())
