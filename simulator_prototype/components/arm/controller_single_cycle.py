
from components.abstract.controller import Controller

class ControllerSingleCycle(Controller):

    def __init__(self, cond, op, funct, rd, bit4, c, v, n, z, pcsrc, pcwr, regsa,
                regdst, regwrs, regwr, exts, alusrcb, alus, aluflagwr, memwr, regsrc, wdbs):
        pass

    def run(self,time):
        pass

    def inspect(self):
        "Not implemented for single cycle"
        pass

    def modify(self,data=None):
        "Not implemented for single cycle"
        pass

    def on_rising_edge(self):
        "Not implemented for single cycle"
        pass

    def on_falling_edge(self):
        "Not implemented for single cycle"
        pass

    def on_reset(self):
        "Not implemented for single cycle"
        pass
