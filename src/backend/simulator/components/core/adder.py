"""
Adder component is a standalone core component for general architecture
development.

Configuration file template should follow form
{
    /* Required */

    "name" : "adder",
    "type" : "Adder",

    "size" : 1,
    "input_1" : "",
    "input_2" : "",

    /* Optional */
    "package" : ""core,
    "output" : "",
    "carry_in" : "",
    "carry_out" : ""
}

name is the entity name, used by entity map (Used externally)
type is the component class (Used externally)
package is associated package to override general (Used externally)
size is the bit-width for this component
input_1 is string reference for input bus of bit-width
input_2 is string reference for input bus of bit-width
output is an optional string reference for output bus of bit-width
carry_in is an optional string reference for input bus of 1 bit
carry_out is an optional string reference for output bus of 1 bit
"""

from simulator.components.abstract.ibus import iBusRead, iBusWrite
from simulator.components.abstract.combinational import Combinational


class Adder(Combinational):
    """
    Adder component implements a combinational adder of fixed bit width.
    Component expects two input signals to be of same size as internal.

    Output follows form:
        Y = A + B + CIN
        COUT = (A + B + CIN) >= (2 ^ BIT_WIDTH)
    """

    def __init__(self, size, a_bus, b_bus, y_bus=None, carry_in=None, carry_out=None):
        "Constructor will check for valid parameters, exception thrown on invalid"

        if not isinstance(size, int) or size <= 0:
            raise TypeError('Size must be integer greater than zero')
        self._size = size

        if not isinstance(a_bus, iBusRead) or not isinstance(b_bus, iBusRead):
            raise TypeError('Input buses must be readable')
        elif not a_bus.size() == size or not b_bus.size() == size:
            raise ValueError('Input buses size must match internal size {}'.format(size))
        self._a = a_bus
        self._b = b_bus

        if not isinstance(y_bus, iBusWrite) and not y_bus is None:
            raise TypeError('If output bus defined then must be writable')
        elif not y_bus is None and not y_bus.size() == size:
            raise ValueError('Output bus size must match internal size {}'.format(size))
        self._y = y_bus

        if not isinstance(carry_in, iBusRead) and not carry_in is None:
            raise TypeError('If carry bus defined them must be readable')
        elif not carry_in is None and not carry_in.size() == 1:
            raise ValueError('Carry bus must be size {}'.format(1))
        self._carry_in = carry_in

        if not isinstance(carry_out, iBusWrite) and not carry_out is None:
            raise TypeError('If carry bus defined then must be writable')
        elif not carry_out is None and not carry_out.size() == 1:
            raise ValueError('Carry bus must be size {}'.format(1))
        self._carry_out = carry_out

    def run(self, time=None):
        "Implements add functionality with rollover and carry bit"

        # process input carry bit
        cin = 0
        if not self._carry_in is None:
            cin = self._carry_in.read()

        # run combinational function
        y = (self._a.read() + self._b.read() + cin)
        cout = 1 if y / (2**self._size) else 0
        if not isinstance(y, int) or not isinstance(cout, int):
            raise TypeError('Produced non-integer result')

        #assert outputs
        if not self._y is None:
            self._y.write(y % 2**self._size)
        if not self._carry_out is None:
            self._carry_out.write(cout)

    @classmethod
    def from_dict(cls, config, hooks):
        "Implements conversion from configuration to component"
        if "output" in config:
            output = hooks[config["output"]]
        else:
            output = None

        if "carry_in" in config:
            carry_in = hooks[config["carry_in"]]
        else:
            carry_in = None

        if "carry_out" in config:
            carry_out = hooks[config["carry_out"]]
        else:
            carry_out = None

        return Adder(config["size"], hooks[config["input_1"]],
                     hooks[config["input_2"]], output, carry_in, carry_out)
