"""
Test arm component ControllerSingleCycle
"""

import unittest
import sys
sys.path.insert(0, '../../')
from simulator.components.arm.controller_single_cycle_full import ControllerSingleCycle
from simulator.components.core.bus import Bus


class ControllerSingleCycle_t(unittest.TestCase):
    """
    Test ControllerSingleCycle's constructor, run and hook functionality

    Note: Run tested through simulation
    """

    def test_constructor(self):
        "tests 4 bad constructors - not all possible constructors tested"
        instruction = Bus(32)
        c = Bus(1)
        v = Bus(1)
        n = Bus(1)
        z = Bus(1)
        pcwr = Bus(1, 0)
        regsa = Bus(1, 0)
        regsb = Bus(1, 0)
        regdst = Bus(2, 0)
        regwrs = Bus(2, 0)
        wdbs = Bus(1, 0)
        regwr = Bus(1, 0)
        exts = Bus(2, 0)
        alusrcb = Bus(1, 0)
        alus = Bus(4, 0)
        aluflagwr = Bus(1, 0)
        shop = Bus(2, 0)
        shctrl = Bus(2, 0)
        accen = Bus(1, 0)
        memwr = Bus(1, 0)
        memty = Bus(2, 0)
        regsrc = Bus(1, 0)
        pcsrc = Bus(2, 0)

        scc = ControllerSingleCycle(instruction,c,v,n,z,pcsrc,pcwr,regsa,
                                    regdst,regsb,regwrs,regwr,exts,alusrcb,
                                    alus,shop,shctrl,accen,aluflagwr,memty,
                                    memwr,regsrc,wdbs)

    def test_inspect(self):
        "tests the single cycle processors inspect method"
        instruction = Bus(32)
        c = Bus(1)
        v = Bus(1)
        n = Bus(1)
        z = Bus(1)
        pcwr = Bus(1, 0)
        regsa = Bus(1, 0)
        regsb = Bus(1, 0)
        regdst = Bus(2, 0)
        regwrs = Bus(2, 0)
        wdbs = Bus(1, 0)
        regwr = Bus(1, 0)
        exts = Bus(2, 0)
        alusrcb = Bus(1, 0)
        alus = Bus(4, 0)
        aluflagwr = Bus(1, 0)
        shop = Bus(2, 0)
        shctrl = Bus(2, 0)
        accen = Bus(1, 0)
        memwr = Bus(1, 0)
        memty = Bus(2, 0)
        regsrc = Bus(1, 0)
        pcsrc = Bus(2, 0)

        scc = ControllerSingleCycle(instruction,c,v,n,z,pcsrc,pcwr,regsa,
                                    regdst,regsb,regwrs,regwr,exts,alusrcb,
                                    alus,shop,shctrl,accen,aluflagwr,memty,
                                    memwr,regsrc,wdbs)

        ins = scc.inspect()
        self.assertTrue(ins['type'] == 'sc-controller')
        self.assertTrue(ins['state'] is None)

    def test_modify(self):
        "tests the single cycle processor modify method"
        instruction = Bus(32)
        c = Bus(1)
        v = Bus(1)
        n = Bus(1)
        z = Bus(1)
        pcwr = Bus(1, 0)
        regsa = Bus(1, 0)
        regsb = Bus(1, 0)
        regdst = Bus(2, 0)
        regwrs = Bus(2, 0)
        wdbs = Bus(1, 0)
        regwr = Bus(1, 0)
        exts = Bus(2, 0)
        alusrcb = Bus(1, 0)
        alus = Bus(4, 0)
        aluflagwr = Bus(1, 0)
        shop = Bus(2, 0)
        shctrl = Bus(2, 0)
        accen = Bus(1, 0)
        memwr = Bus(1, 0)
        memty = Bus(2, 0)
        regsrc = Bus(1, 0)
        pcsrc = Bus(2, 0)

        scc = ControllerSingleCycle(instruction,c,v,n,z,pcsrc,pcwr,regsa,
                                    regdst,regsb,regwrs,regwr,exts,alusrcb,
                                    alus,shop,shctrl,accen,aluflagwr,memty,
                                    memwr,regsrc,wdbs)

        mod = scc.modify(None)
        self.assertTrue('error' in mod)  # modify is not implemented for controller

        mod = scc.modify({'state': 0})
        self.assertTrue('error' in mod)  # modify is not implemented for controller

    def test_clear(self):
        "tests the single cycle processor clear method"
        instruction = Bus(32)
        c = Bus(1)
        v = Bus(1)
        n = Bus(1)
        z = Bus(1)
        pcwr = Bus(1, 0)
        regsa = Bus(1, 0)
        regsb = Bus(1, 0)
        regdst = Bus(2, 0)
        regwrs = Bus(2, 0)
        wdbs = Bus(1, 0)
        regwr = Bus(1, 0)
        exts = Bus(2, 0)
        alusrcb = Bus(1, 0)
        alus = Bus(4, 0)
        aluflagwr = Bus(1, 0)
        shop = Bus(2, 0)
        shctrl = Bus(2, 0)
        accen = Bus(1, 0)
        memwr = Bus(1, 0)
        memty = Bus(2, 0)
        regsrc = Bus(1, 0)
        pcsrc = Bus(2, 0)

        scc = ControllerSingleCycle(instruction,c,v,n,z,pcsrc,pcwr,regsa,
                                    regdst,regsb,regwrs,regwr,exts,alusrcb,
                                    alus,shop,shctrl,accen,aluflagwr,memty,
                                    memwr,regsrc,wdbs)

        mod = scc.clear()
        self.assertTrue('error' in mod)  # modify is not implemented for controller


if __name__ == '__main__':
    unittest.main()
