"""
Memwb is a barrier register for the pipeline ARM processor that seperates
the memory and write-back stages.

Configuraiton file template should follow form
{
    /* Required */

    "pc4m" : "",
    "regwrm" : "",
    "regsrcm" : "",
    "wd3sm" : "",
    "fm" : "",
    "rdm" : "",
    "ra3m" : "",
    "clk" : "",
    "pc4w" : "",
    "regwrw" : "",
    "regsrcw" : "",
    "wd3sw" : "",
    "fw" : "",
    "rdw" : "",
    "ra3w" : "",

    /* Optional */

    "append_to_signals" : true,
    "enable" : "",
    "edge_type" : "",
    "enable_type" : ""
}

append_to_signals is flag used to append an entity as hook (Used externally)
pc4m is data bus reference input
regwrm is data bus reference input
regsrcm is data bus reference input
wd3sm is data bus reference input
fm is data bus reference input
rdm is data bus reference input
ra3m is data bus reference input
clk is clock control bus reference
pc4w is data bus reference output
regwrw is data bus reference output
regsrcw is data bus reference output
wd3sw is data bus reference output
fw is data bus reference output
rdw is data bus reference output
ra3w is data bus reference output
enable is write control bus reference
edge_type is edge to clock data
enable_type is logic level to write to memory
"""

from simulator.components.abstract.ibus import iBusRead, iBusWrite
from simulator.components.abstract.sequential import Sequential, Latch_Type, Logic_States


class Memwb(Sequential):
    "This specialized register sits between the memory and write back stages"

    DEFAULT_LATCH_TYPE = Latch_Type.RISING_EDGE
    DEFAULT_ENABLE_TYPE = Logic_States.ACTIVE_HIGH
    DEFAULT_ENABLE_BUS = None

    def __init__(self, pc4m, regwrm, regsrcm, wd3sm, fm, rdm, ra3m, clk, pc4w,
                 regwrw, regsrcw, wd3sw, fw, rdw, ra3w,
                 edge_type=DEFAULT_LATCH_TYPE, enable=DEFAULT_ENABLE_BUS,
                 enable_type=DEFAULT_ENABLE_TYPE):
        """
        inputs:
            pc4m: pc+4
            regwrm: selects whether to write back to the regfile
            regsrcm: selects whether the alu output or memory is feedback
            wd3sm: selects what data to write to the regfile
            fm: output of execute stage
            rdm: output of data memory
            ra3m: register number
            clk: clock
            enable: enables component (not typically used)
        outputs:
            pc4w: pc+4
            regwrw: selects whether to write back to the regfile
            regsrcw: selects whether the alu output or memory is feedback
            wd3sw: selects what data to write to the regfile
            fw: output of the execute stage
            rdw: output of data memory
            ra3w: register number

        edge_type: memwb register data latch type
        enable_type: enable signal active state
        """

        # Inputs
        if not isinstance(pc4m, iBusRead):
            raise TypeError('The pc4m bus must be readable')
        elif pc4m.size() != 32:
            raise ValueError('The pc4m bus must have a size of 32 bits')
        if not isinstance(regwrm, iBusRead):
            raise TypeError('The regwrm bus must be readable')
        elif regwrm.size() != 1:
            raise ValueError('The regwrm bus must have a size of 1 bit')
        if not isinstance(regsrcm, iBusRead):
            raise TypeError('The regsrcm bus must be readable')
        elif regsrcm.size() != 1:
            raise ValueError('The regsrm bus must have a size of 1 bit')
        if not isinstance(wd3sm, iBusRead):
            raise TypeError('The wd3sm bus must be readable')
        elif wd3sm.size() != 1:
            raise ValueError('The wd3sm bus must have a size of 1 bit')
        if not isinstance(fm, iBusRead):
            raise TypeError('The fm bus must be readable')
        elif fm.size() != 32:
            raise ValueError('The fm bus must have a size of 32 bits')
        if not isinstance(rdm, iBusRead):
            raise TypeError('The rdm bus must be readable')
        elif rdm.size() != 32:
            raise ValueError('The rdm bus must have a size of 32 bits')
        if not isinstance(ra3m, iBusRead):
            raise TypeError('The ra3m bus must be readable')
        elif ra3m.size() != 4:
            raise ValueError('The ra3m bus must have a size of 4 bits')
        if not isinstance(clk, iBusRead):
            raise TypeError('The clk bus must be readable')
        elif clk.size() != 1:
            raise ValueError('The clk bus must have a size of 1 bit')

        self._pc4m = pc4m
        self._regwrm = regwrm
        self._regsrcm = regsrcm
        self._wd3sm = wd3sm
        self._fm = fm
        self._rdm = rdm
        self._ra3m = ra3m
        self._clk = clk
        self._prev_clk_state = self._clk.read()

        # Outputs
        if not isinstance(pc4w, iBusWrite):
            raise TypeError('The pc4w bus must be writable')
        elif pc4w.size() != 32:
            raise ValueError('The pc4w bus must have a size of 32 bits')
        if not isinstance(regwrw, iBusWrite):
            raise TypeError('The regwrw bus must be writable')
        elif regwrw.size() != 1:
            raise ValueError('The regwrw bus must have a size of 1 bit')
        if not isinstance(regsrcw, iBusWrite):
            raise TypeError('The regsrcw bus must be writable')
        elif regsrcw.size() != 1:
            raise ValueError('The regsrcw bus must have a size of 1 bit')
        if not isinstance(wd3sw, iBusWrite):
            raise TypeError('The wd3sw bus must be writable')
        elif wd3sw.size() != 1:
            raise ValueError('The wd3sw bus must have a size of 1 bit')
        if not isinstance(fw, iBusWrite):
            raise TypeError('The fw bus must be writable')
        elif fw.size() != 32:
            raise ValueError('The fw bus must have a size of 32 bits')
        if not isinstance(rdw, iBusWrite):
            raise TypeError('The rdw bus must be writable')
        elif rdw.size() != 32:
            raise ValueError('The rdw bus must have a size of 32 bits')
        if not isinstance(ra3w, iBusWrite):
            raise TypeError('The ra3w bus must be writable')
        elif ra3w.size() != 4:
            raise ValueError('The ra3w bus must have a size of 4 bits')

        self._pc4w = pc4w
        self._regwrw = regwrw
        self._regsrcw = regsrcw
        self._wd3sw = wd3sw
        self._fw = fw
        self._rdw = rdw
        self._ra3w = ra3w

        # Attributes
        if not Latch_Type.valid(edge_type):
            raise ValueError('Invalid latch edge type')
        if enable is not None and not isinstance(enable, iBusRead):
            raise ValueError('The enable bus must be readable')
        elif enable is not None and enable.size() != 1:
            raise ValueError('The enable bus must have a size of 1 bit')
        if not Logic_States.valid(enable_type):
            raise ValueError('Invalid enable state')

        self._edge_type = edge_type
        self._enable = enable
        self._enable_type = enable_type

    def on_rising_edge(self):
        "Implements clock rising behavior: captures data if latch type matches"
        if (self._edge_type == Latch_Type.RISING_EDGE
                or self._edge_type == Latch_Type.BOTH_EDGE):
            self._pc4w.write(self._pc4m.read())
            self._regwrw.write(self._regwrm.read())
            self._regsrcw.write(self._regsrcm.read())
            self._wd3sw.write(self._wd3sm.read())
            self._fw.write(self._fm.read())
            self._rdw.write(self._rdm.read())
            self._ra3w.write(self._ra3m.read())

    def on_falling_edge(self):
        "Implements clock rising behavior: captures data if latch type matches"
        if (self._edge_type == Latch_Type.FALLING_EDGE
                or self._edge_type == Latch_Type.BOTH_EDGE):
            self._pc4w.write(self._pc4m.read())
            self._regwrw.write(self._regwrm.read())
            self._regsrcw.write(self._regsrcm.read())
            self._wd3sw.write(self._wd3sm.read())
            self._fw.write(self._fm.read())
            self._rdw.write(self._rdm.read())
            self._ra3w.write(self._ra3m.read())

    def on_reset(self):
        "Not used for this register"
        pass

    def inspect(self):
        "Returns a dictionary message to the user"
        return {'type': 'memwb register', 'state': self._get_state()}

    def modify(self, data=None):
        "Return a message noting that is register cannot be modified"
        return {'error': 'memwb register cannot be modified'}

    def clear(self):
        "Return a message noting that the memwb register cannot be cleared"
        return {'error': 'memwb register cannot be cleared'}

    def run(self, time=None):
        "Timestep handler function - seqeuntially asserts output"

        # process enable line
        e = True
        if self._enable is not None:
            if self._enable_type == Logic_States.ACTIVE_LOW:
                e = self._enable_type.read() == 0
            else:
                e = self._enable.read() == 1

        # check for clock change
        if e:
            if self._clk.read() == 1 and self._prev_clk_state == 0:
                self.on_rising_edge()
            elif self._clk.read() == 0 and self._prev_clk_state == 1:
                self.on_falling_edge()
        self._prev_clk_state = self._clk.read()

    @classmethod
    def from_dict(cls, config, hooks):
        "Implements conversion from configuration to component"

        if "edge_type" in config:
            edge_type = Latch_Type.fromString(config["edge_type"])
        else:
            edge_type = Memwb.DEFAULT_LATCH_TYPE

        if "enable" in config:
            enable = hooks[config["enable"]]
        else:
            enable = Memwb.DEFAULT_ENABLE_BUS

        if "enable_type" in config:
            enable_type = Logic_States.fromString(config["enable_type"])
        else:
            enable_type = Memwb.DEFAULT_ENABLE_TYPE

        return Memwb(hooks[config["pc4m"]],hooks[config["regwrm"]],hooks[config["regsrcm"]],
                     hooks[config["wd3sm"]],hooks[config["fm"]],hooks[config["rdm"]],
                     hooks[config["ra3m"]],hooks[config["clk"]],hooks[config["pc4w"]],
                     hooks[config["regwrw"]],hooks[config["regsrcw"]],hooks[config["wd3sw"]],
                     hooks[config["fw"]],hooks[config["rdw"]],hooks[config["ra3w"]],
                     edge_type,enable,enable_type)

    def _get_state(self):
        """Create map between name and data of register state"""
        return {'pcsrcw': self._pc4w.read(),
                'regwrew': self._regwrw.read(), 'regsrcw': self._regsrcw.read(),
                'wd3sw': self._wd3sw.read(), 'fw': self._fw.read(),
                'rdw': self._rdw.read(), 'ra3w': self._ra3w.read()}
