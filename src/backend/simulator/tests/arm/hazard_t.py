"""
Tests the hazard controller
"""

import unittest
import sys
sys.path.insert(0, '../../')
from components.arm.hazard import HazardController
from components.core.bus import Bus

class HazardController_t(unittest.TestCase):
    "Unit tests for hazard controller"

    def test_contructor(self):
        "Tests constructor with valid and invalid configuration"
        ra1d = Bus(4)
        ra2d = Bus(4)
        ra1e = Bus(4)
        ra2e = Bus(4)
        ra3e = Bus(4)
        ra3m = Bus(4)
        ra3w = Bus(4)
        regwrm = Bus(1)
        regwrw = Bus(1)
        regsrce = Bus(1)
        regsrcw = Bus(1)
        memwrm = Bus(1)
        pcsrcd = Bus(2)
        fwda = Bus(2)
        fwdb = Bus(2)
        fwds = Bus(1)
        stalld = Bus(1)
        flushd = Bus(1)
        flushe = Bus(1)

        invalidBusSize = Bus(7)
        invalidBusType = 'w'

        with self.assertRaises(ValueError):
            hazard_controller = HazardController(ra1d, ra2d, ra1e, ra2e, ra3e, ra3m,
                                                ra3w, regwrm, regwrw, regsrce,
                                                regsrcw, invalidBusSize, pcsrcd, fwda,
                                                fwdb, fwds, stalld, flushd, flushe)

        with self.assertRaises(TypeError):
            hazard_controller = HazardController(ra1d, ra2d, ra1e, ra2e, ra3e, ra3m,
                                                ra3w, invalidBusType, regwrw, regsrce,
                                                regsrcw, memwrm, pcsrcd, fwda,
                                                fwdb, fwds, stalld, flushd, flushe)

        hazard_controller = HazardController(ra1d, ra2d, ra1e, ra2e, ra3e, ra3m,
                                            ra3w, regwrm, regwrw, regsrce,
                                            regsrcw, memwrm, pcsrcd, fwda,
                                            fwdb, fwds, stalld, flushd, flushe)


    def test_generate_fwda(self):
        "Tests the _generate_fwda method"
        ra1e = Bus(4)
        ra3m = Bus(4)
        ra3w = Bus(4)
        regwrm = Bus(1)
        regwrw = Bus(1)
        regsrcw = Bus(1)

        self.assertEqual(HazardController._generate_fwda(ra1e, ra3m, ra3w, regwrm, regwrw, regsrcw), 0)
        ra1e.write(4)
        ra3w.write(4)
        regsrcw.write(1)
        self.assertEqual(HazardController._generate_fwda(ra1e, ra3m, ra3w, regwrm, regwrw, regsrcw), 3)
        ra1e.write(5)
        ra3m.write(5)
        regwrm.write(1)
        self.assertEqual(HazardController._generate_fwda(ra1e, ra3m, ra3w, regwrm, regwrw, regsrcw), 2)
        ra1e.write(4)
        regsrcw.write(0)
        regwrw.write(1)
        self.assertEqual(HazardController._generate_fwda(ra1e, ra3m, ra3w, regwrm, regwrw, regsrcw), 1)

    
    def test_generate_fwdb(self):
        "Tests _generate_fwdb method"
        ra2e = Bus(4)
        ra3m = Bus(4)
        ra3w = Bus(4)
        regwrm = Bus(1)
        regwrw = Bus(1)
        regsrcw = Bus(1)

        self.assertEqual(HazardController._generate_fwdb(ra2e, ra3m, ra3w, regwrm, regwrw, regsrcw), 0)
        ra2e.write(4)
        ra3w.write(4)
        regsrcw.write(1)
        self.assertEqual(HazardController._generate_fwdb(ra2e, ra3m, ra3w, regwrm, regwrw, regsrcw), 3)
        ra2e.write(5)
        ra3m.write(5)
        regwrm.write(1)
        self.assertEqual(HazardController._generate_fwdb(ra2e, ra3m, ra3w, regwrm, regwrw, regsrcw), 2)
        ra2e.write(4)
        regsrcw.write(0)
        regwrw.write(1)
        self.assertEqual(HazardController._generate_fwdb(ra2e, ra3m, ra3w, regwrm, regwrw, regsrcw), 1)


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


    def test_generate_stalld(self):
        "Tests the _generate_stalld method"
        ra1d = Bus(4)
        ra2d = Bus(4)
        ra3e = Bus(4)
        regsrce = Bus(1)

        self.assertEqual(HazardController._generate_stalld(ra1d, ra2d, ra3e, regsrce), 0)
        ra1d.write(3)
        ra3e.write(3)
        regsrce.write(1)
        self.assertEqual(HazardController._generate_stalld(ra1d, ra2d, ra3e, regsrce), 1)


    def test_generate_flushd(self):
        "Tests the _generate_flushd method"
        pcsrcd = Bus(2)

        self.assertEqual(HazardController._generate_flushd(pcsrcd), 1)
        pcsrcd.write(2)
        self.assertEqual(HazardController._generate_flushd(pcsrcd), 0)

    
    def test_run(self):
        "Tests the run method"
        ra1d = Bus(4)
        ra2d = Bus(4)
        ra1e = Bus(4)
        ra2e = Bus(4)
        ra3e = Bus(4)
        ra3m = Bus(4)
        ra3w = Bus(4)
        regwrm = Bus(1)
        regwrw = Bus(1)
        regsrce = Bus(1)
        regsrcw = Bus(1)
        memwrm = Bus(1)
        pcsrcd = Bus(2)
        fwda = Bus(2)
        fwdb = Bus(2)
        fwds = Bus(1)
        stalld = Bus(1)
        flushd = Bus(1)
        flushe = Bus(1)

        hazard_controller = HazardController(ra1d, ra2d, ra1e, ra2e, ra3e, ra3m,
                                            ra3w, regwrm, regwrw, regsrce,
                                            regsrcw, memwrm, pcsrcd, fwda,
                                            fwdb, fwds, stalld, flushd, flushe)
        # fwda output expected to be 3
        ra1e.write(4)
        ra3w.write(4)
        regsrcw.write(1)
        # fwdb output expected to be 0
        # fwds output expected to be 1
        ra3m.write(4)
        memwrm.write(1)
        # stalld output expected to be 1
        ra1d.write(3)
        ra3e.write(3)
        regsrce.write(1)
        # flushd output expected to be 0
        pcsrcd.write(1)

        hazard_controller.run()
        self.assertEqual(fwda.read(), 3)
        self.assertEqual(fwdb.read(), 0)
        self.assertEqual(fwds.read(), 1)
        self.assertEqual(stalld.read(), 1)
        self.assertEqual(flushd.read(), 0)


    def test_inspect(self):
        "Tests the inspect method"
        ra1d = Bus(4)
        ra2d = Bus(4)
        ra1e = Bus(4)
        ra2e = Bus(4)
        ra3e = Bus(4)
        ra3m = Bus(4)
        ra3w = Bus(4)
        regwrm = Bus(1)
        regwrw = Bus(1)
        regsrce = Bus(1)
        regsrcw = Bus(1)
        memwrm = Bus(1)
        pcsrcd = Bus(2)
        fwda = Bus(2)
        fwdb = Bus(2)
        fwds = Bus(1)
        stalld = Bus(1)
        flushd = Bus(1)
        flushe = Bus(1)

        hazard_controller = HazardController(ra1d, ra2d, ra1e, ra2e, ra3e, ra3m,
                                            ra3w, regwrm, regwrw, regsrce,
                                            regsrcw, memwrm, pcsrcd, fwda,
                                            fwdb, fwds, stalld, flushd, flushe)
        
        self.assertEqual(hazard_controller.inspect()['type'], 'hazard-controller')
        self.assertEqual(hazard_controller.inspect()['state'], None)


    def test_modify(self):
        "Tests the modify method"
        ra1d = Bus(4)
        ra2d = Bus(4)
        ra1e = Bus(4)
        ra2e = Bus(4)
        ra3e = Bus(4)
        ra3m = Bus(4)
        ra3w = Bus(4)
        regwrm = Bus(1)
        regwrw = Bus(1)
        regsrce = Bus(1)
        regsrcw = Bus(1)
        memwrm = Bus(1)
        pcsrcd = Bus(2)
        fwda = Bus(2)
        fwdb = Bus(2)
        fwds = Bus(1)
        stalld = Bus(1)
        flushd = Bus(1)
        flushe = Bus(1)

        hazard_controller = HazardController(ra1d, ra2d, ra1e, ra2e, ra3e, ra3m,
                                            ra3w, regwrm, regwrw, regsrce,
                                            regsrcw, memwrm, pcsrcd, fwda,
                                            fwdb, fwds, stalld, flushd, flushe)
        
        self.assertEqual(hazard_controller.modify()['error'], 'hazard controller cannot be modified')



if __name__ == '__main__':
    unittest.main()