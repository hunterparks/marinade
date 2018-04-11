"""
Tests the hazard.py module
Must be run in the marinade/src/backend/simulator/tests/arm
"""

import unittest
import sys
sys.path.insert(0, '../../../')
from simulator.components.arm.hazard import HazardController
from simulator.components.core.bus import Bus

class HazardController_t(unittest.TestCase):
    "Unit tests for hazard.py module"

    def test_contructor(self):
        "Tests constructor with valid and invalid configuration"
        ra1e = Bus(4)
        ra2e = Bus(4)
        ra3e = Bus(4)
        ra3m = Bus(4)
        ra3w = Bus(4)
        regwrm = Bus(1)
        regwrw = Bus(1)
        regsrcm = Bus(1)
        regsrcw = Bus(1)
        memwrm = Bus(1)
        pcsrcd = Bus(2)
        fwda = Bus(3)
        fwdb = Bus(3)
        fwds = Bus(1)
        stallf = Bus(1)
        flushf = Bus(1)
        flushd = Bus(1)

        invalidBusSize = Bus(7)
        invalidBusType = 'w'

        with self.assertRaises(ValueError):
            HazardController(ra1e, ra2e, ra3e, ra3m, ra3w, regwrm, regwrw, 
                             regsrcm, regsrcw, invalidBusSize, pcsrcd, fwda, 
                             fwdb, fwds, stallf, flushf, flushd)

        with self.assertRaises(TypeError):
            HazardController(ra1e, ra2e, ra3e, ra3m, ra3w, invalidBusType, 
                             regwrw, regsrcm, regsrcw, memwrm, pcsrcd, fwda, 
                             fwdb, fwds, stallf, flushf, flushd)

        HazardController(ra1e, ra2e, ra3e, ra3m, ra3w, regwrm, regwrw, regsrcm, 
                         regsrcw, memwrm, pcsrcd, fwda, fwdb, fwds, stallf, 
                         flushf, flushd)


    def test_generate_fwda(self):
        "Tests the _generate_fwda method"
        ra1e = Bus(4)
        ra3m = Bus(4)
        ra3w = Bus(4)
        regwrm = Bus(1)
        regwrw = Bus(1)
        regsrcm = Bus(1)
        regsrcw = Bus(1)

        ra1e.write(4)
        self.assertEqual(HazardController._generate_fwda(ra1e, ra3m, ra3w, regwrm, regwrw, regsrcm, regsrcw), 0)
        ra3w.write(4)
        self.assertEqual(HazardController._generate_fwda(ra1e, ra3m, ra3w, regwrm, regwrw, regsrcm, regsrcw), 4)
        ra3m.write(4)
        self.assertEqual(HazardController._generate_fwda(ra1e, ra3m, ra3w, regwrm, regwrw, regsrcm, regsrcw), 3)
        ra1e.write(5)
        ra3m.write(5)
        regwrm.write(1)
        regsrcm.write(1)
        self.assertEqual(HazardController._generate_fwda(ra1e, ra3m, ra3w, regwrm, regwrw, regsrcm, regsrcw), 2)
        ra1e.write(8)
        ra3w.write(8)
        regwrw.write(1)
        regsrcw.write(1)
        self.assertEqual(HazardController._generate_fwda(ra1e, ra3m, ra3w, regwrm, regwrw, regsrcm, regsrcw), 1)


    def test_generate_fwdb(self):
        "Tests _generate_fwdb method"
        ra2e = Bus(4)
        ra3m = Bus(4)
        ra3w = Bus(4)
        regwrm = Bus(1)
        regwrw = Bus(1)
        regsrcm = Bus(1)
        regsrcw = Bus(1)

        ra2e.write(4)
        self.assertEqual(HazardController._generate_fwdb(ra2e, ra3m, ra3w, regwrm, regwrw, regsrcm, regsrcw), 0)
        ra3w.write(4)
        self.assertEqual(HazardController._generate_fwdb(ra2e, ra3m, ra3w, regwrm, regwrw, regsrcm, regsrcw), 4)
        ra3m.write(4)
        self.assertEqual(HazardController._generate_fwdb(ra2e, ra3m, ra3w, regwrm, regwrw, regsrcm, regsrcw), 3)
        ra2e.write(5)
        ra3m.write(5)
        regwrm.write(1)
        regsrcm.write(1)
        self.assertEqual(HazardController._generate_fwdb(ra2e, ra3m, ra3w, regwrm, regwrw, regsrcm, regsrcw), 2)
        ra2e.write(8)
        ra3w.write(8)
        regwrw.write(1)
        regsrcw.write(1)
        self.assertEqual(HazardController._generate_fwdb(ra2e, ra3m, ra3w, regwrm, regwrw, regsrcm, regsrcw), 1)


    def test_generate_fwds(self):
        "Tests the _generate_fwds method"
        ra3m = Bus(4)
        ra3w = Bus(4)
        memwrm = Bus(1)

        self.assertEqual(HazardController._generate_fwds(ra3m, ra3w, memwrm), 0)
        ra3m.write(8)
        ra3w.write(8)
        memwrm.write(1)
        self.assertEqual(HazardController._generate_fwds(ra3m, ra3w, memwrm), 1)


    def test_generate_stallf(self):
        "Tests the _generate_stallf method"
        pcsrcd = Bus(2)

        pcsrcd.write(1)
        self.assertEqual(HazardController._generate_stallf(pcsrcd), 0)
        pcsrcd.write(2)
        self.assertEqual(HazardController._generate_stallf(pcsrcd), 1)
        pcsrcd.write(0)
        self.assertEqual(HazardController._generate_stallf(pcsrcd), 0)


    def test_generate_flushf(self):
        "Tests the _generate_flushf method"
        pcsrcd = Bus(2)
        ra3e = Bus(4)

        self.assertEqual(HazardController._generate_flushf(pcsrcd, ra3e), 1)
        pcsrcd.write(1)
        self.assertEqual(HazardController._generate_flushf(pcsrcd, ra3e), 0)
        pcsrcd.write(2)
        ra3e.write(0xF)
        self.assertEqual(HazardController._generate_flushf(pcsrcd, ra3e), 1)


    def test_run(self):
        "Tests the run method"
        ra1e = Bus(4)
        ra2e = Bus(4)
        ra3e = Bus(4)
        ra3m = Bus(4)
        ra3w = Bus(4)
        regwrm = Bus(1)
        regwrw = Bus(1)
        regsrcm = Bus(1)
        regsrcw = Bus(1)
        memwrm = Bus(1)
        pcsrcd = Bus(2)
        fwda = Bus(3)
        fwdb = Bus(3)
        fwds = Bus(1)
        stallf = Bus(1)
        flushf = Bus(1)
        flushd = Bus(1)

        hazard_controller = HazardController(ra1e, ra2e, ra3e, ra3m, ra3w, 
                                             regwrm, regwrw, regsrcm, regsrcw, 
                                             memwrm, pcsrcd, fwda, fwdb, fwds, 
                                             stallf, flushf, flushd)
        # fwda output expected to be 3
        ra1e.write(4)
        ra3w.write(4)
        regsrcw.write(1)
        # fwdb output expected to be 0
        # fwds output expected to be 1
        ra3m.write(4)
        memwrm.write(1)
        # stallf output expected to be 1
        pcsrcd.write(2)
        # flushf output expected to be 0
        # flushd output expected to be 0

        hazard_controller.run()
        self.assertEqual(fwda.read(), 3)
        self.assertEqual(fwdb.read(), 0)
        self.assertEqual(fwds.read(), 1)
        self.assertEqual(stallf.read(), 1)
        self.assertEqual(flushf.read(), 0)
        self.assertEqual(flushd.read(), 0)


    def test_inspect(self):
        "Tests the inspect method"
        ra1e = Bus(4)
        ra2e = Bus(4)
        ra3e = Bus(4)
        ra3m = Bus(4)
        ra3w = Bus(4)
        regwrm = Bus(1)
        regwrw = Bus(1)
        regsrcm = Bus(1)
        regsrcw = Bus(1)
        memwrm = Bus(1)
        pcsrcd = Bus(2)
        fwda = Bus(3)
        fwdb = Bus(3)
        fwds = Bus(1)
        stallf = Bus(1)
        flushf = Bus(1)
        flushd = Bus(1)

        hazard_controller = HazardController(ra1e, ra2e, ra3e, ra3m, ra3w, 
                                             regwrm, regwrw, regsrcm, regsrcw, 
                                             memwrm, pcsrcd, fwda, fwdb, fwds, 
                                             stallf, flushf, flushd)

        self.assertEqual(hazard_controller.inspect()['type'], 'hazard-controller')
        self.assertEqual(hazard_controller.inspect()['state'], None)


    def test_modify(self):
        "Tests the modify method"
        ra1e = Bus(4)
        ra2e = Bus(4)
        ra3e = Bus(4)
        ra3m = Bus(4)
        ra3w = Bus(4)
        regwrm = Bus(1)
        regwrw = Bus(1)
        regsrcm = Bus(1)
        regsrcw = Bus(1)
        memwrm = Bus(1)
        pcsrcd = Bus(2)
        fwda = Bus(3)
        fwdb = Bus(3)
        fwds = Bus(1)
        stallf = Bus(1)
        flushf = Bus(1)
        flushd = Bus(1)

        hazard_controller = HazardController(ra1e, ra2e, ra3e, ra3m, ra3w, 
                                             regwrm, regwrw, regsrcm, regsrcw, 
                                             memwrm, pcsrcd, fwda, fwdb, fwds, 
                                             stallf, flushf, flushd)

        self.assertEqual(hazard_controller.modify()['error'], 'hazard controller cannot be modified')



if __name__ == '__main__':
    unittest.main()
