"""
BusSubset component used to break apart a single bus into composite signals

Configuration file template should follow form
{
    /* Required */

    "name" : "bus_subset",
    "type" : "BusSubset",
    "input" : "",
    "outputs" : [],
    "bounds" : [],

    /* Optional */

    "package" : ""core
}

name is the entity name, used by entity map (Used externally)
type is the component class (Used externally)
package is associated package to override general (Used externally)
input is the bus reference to split
outputs is an array of string bus references to break input into
bounds is an array of two element arrays defining start and end of an output
    for should follow [min,max+1]
"""

from simulator.components.abstract.entity import Entity
from simulator.components.abstract.ibus import iBusRead, iBusWrite


class BusSubset(Entity):
    """
    BusSubset pull multiple output buses together from a common source.
    The subsets must be atleast one element and no more than the size of the
    bus. Additionally, the range of bits pulled from the bus must be
    sequential.
    """

    def __init__(self, in_b, outs_b, outs_range):
        "Constructor will check for valid parameters, exception thrown on invalid"

        if not isinstance(in_b, iBusRead):
            raise TypeError('Input bus must be readable')
        self._input = in_b

        if not isinstance(outs_b, list) or len(outs_b) <= 0:
            raise TypeError('Outputs must be a list with at least one element')
        elif not all(isinstance(x, iBusWrite) and x.size() <= in_b.size() for x in outs_b):
            raise ValueError('Output buses must be writable')
        self._outputs = outs_b

        if not isinstance(outs_range, list) or not len(outs_b) == len(outs_range):
            raise TypeError('Output ranges must be a list corresponding to outputs')
        for i in range(0, len(outs_range)):
            if not isinstance(outs_range[i], (tuple,list)) or not len(outs_range[i]) == 2:
                raise TypeError('Range must be a tuple or list with two elements')
            elif not outs_range[i][0] < outs_range[i][1]:
                raise ValueError('Range must start position first')
            elif not outs_range[i][1] <= in_b.size():
                raise ValueError('Range specified must not be greater than size')
            elif not (outs_range[i][1] - outs_range[i][0]) == outs_b[i].size():
                raise ValueError('Range specified must match corresponding bus size')
        self._range = outs_range

    def run(self, time=None):
        "Implements bus subset behavior by storing a masked shifted input to each"
        for x in range(0, len(self._outputs)):
            mask = 2**self._range[x][1] - 2**self._range[x][0]
            val = (self._input.read() & mask) >> self._range[x][0]
            self._outputs[x].write(val)

    @classmethod
    def from_dict(cls, config, hooks):
        "Implements conversion from configuration to component"
        outputs = [hooks[o] for o in config["outputs"]]
        output_range = [r for r in config["bounds"]]

        return BusSubset(hooks[config["input"]],outputs,output_range)
