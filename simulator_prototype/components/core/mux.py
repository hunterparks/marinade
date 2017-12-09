"""

"""

from components.abstract.ibus import iBusRead, iBusWrite
from components.abstract.combinational import Combinational
import math


class Mux(Combinational):
    """

    """

    def __init__(self, name, size, inputs, select, output=None):
        "Constructor will check for valid parameters, exception thrown on invalid"

        if not isinstance(name,str):
            raise ValueError('Name must be a string')
        elif not isinstance(size,int) or size <= 0:
            raise ValueError('Size must be an integer greater than zero')
        self._name = name
        self._size = size

        print(len(inputs))
        if not isinstance(inputs,list) or not len(inputs) > 1:
            raise ValueError('Inputs must be a list with at least two inputs')
        elif not all((isinstance(x,iBusRead) and x.size() == self._size) for x in inputs):
            raise ValueError('All inputs must be a bus with size equal to internal')
        self._inputs = inputs
        self._necessary_select_size = int(math.ceil(len(inputs) / 2))

        if not isinstance(select,iBusRead):
            raise ValueError('Select signal must be a bus')
        elif not select.size() == self._necessary_select_size:
            raise ValueError('Select signal does not best match input size needed {}'.format(self._necessary_select_size))
        self._select = select #note going to ignore invalid cases with logic

        if not isinstance(output,iBusWrite) and not output is None:
            raise ValueError('Output must be defined as a bus or None')
        elif not output.size() == self._size:
            raise ValueError('Output bus size must match internal')
        self._output = output

    def run(self,time=None):
        "Implements n-length mux select functionality with case ignore"

        #process select line
        s = self._select.read() & (2**self._necessary_select_size - 1)

        #select signal to pass to output
        if not self._output is None:
            self._output.write(self._inputs[s].read())