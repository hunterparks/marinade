import unittest
import sys
sys.path.insert(0, '../../')
from architecture import Architecture
from components.core.bus import Bus
from components.core.clock import Clock
from components.core.reset import Reset

class Architecture_t(unittest.TestCase):

    def test_constructor(self):
        raise NotImplementedError

    def test_hook(self):
        raise NotImplementedError

    def test_time_step(self):
        raise NotImplementedError

    def test_time_run(self):
        raise NotImplementedError

    def test_logic_step(self):
        raise NotImplementedError

    def test_logic_run(self):
        raise NotImplementedError

    def test_reset(self):
        """
        Runs a simple simulation for some time, then reset.
        Expect sequential components to change state to default.
        After time-step expect buses to be same as initial time-step
        """
        raise NotImplementedError


if __name__ == '__main__':
    unittest.main()
