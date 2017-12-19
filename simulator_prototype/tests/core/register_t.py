import unittest
import sys
sys.path.insert(0,'../../')
from components.core.register import Register
from components.core.constant import Constant
from components.core.bus import Bus
from components.core.reset import Reset
from components.core.clock import Clock

class Register_t(unittest.TestCase):

    def test_constructor(self):
        "Constructor with valid and invalid configuration"
        raise NotImplementedError("Write this test case")

    def test_rising_edge(self):
        "Verifies rising edge capture behavior"
        raise NotImplementedError("Write this test case")

    def test_falling_edge(self):
        "Verifies falling edge capture behavior"
        raise NotImplementedError("Write this test case")

    def test_reset(self):
        "Verifies reset behavior of component"
        raise NotImplementedError("Write this test case")

    def test_inspect(self):
        "Verifies hook inspect for valid return"
        raise NotImplementedError("Write this test case")

    def test_modify(self):
        "Verifies internal hook modify function"
        raise NotImplementedError("Write this test case")

    def test_run(self):
        "Verifies correct time based simulation"
        raise NotImplementedError("Write this test case")


if __name__ == '__main__':
    unittest.main()
