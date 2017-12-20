import unittest
import sys
sys.path.insert(0, '../../')
from components.arm.extender import Extender
from components.core.bus import Bus

class Extender_t(unittest.TestCase):

    def test_constructor(self):
        # initialize busses
        imm = Bus(23)
        imm32 = Bus(32)
        exts = Bus(2) 
        # test case 1
        with self.assertRaises(ValueError):
            e = Extender(imm, imm32, exts)

    def test_run(self):
        # initialize busses
        imm = Bus(24)
        imm32 = Bus(32)
        exts = Bus(2)
        # initialize extender
        e = Extender(imm, imm32, exts)
        # initialize input with value 5096
        imm.write(0b000000000001001111101000)
        # test case 2
        exts.write(0)
        e.run()
        self.assertEqual(imm32.read(), 0b11101000)
        # test case 3
        exts.write(1)
        e.run()
        self.assertEqual(imm32.read(), 0b001111101000)
        # test case 4
        exts.write(2)
        e.run()
        self.assertEqual(imm32.read(), 0b100111110100000)
        # test case 5
        imm.write(0b100000000001001111101000)
        e.run()
        self.assertEqual(imm32.read(), 0b11111110000000000100111110100000)

if __name__ == '__main__':
    unittest.main()