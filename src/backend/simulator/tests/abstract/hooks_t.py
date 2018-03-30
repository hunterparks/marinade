"""
Test abstract hooks: Hook, InputHook, InternalHook, OutputHook
"""

import unittest
import sys
sys.path.insert(0, '../../')
from simulator.components.abstract.hooks import Hook, InputHook, OutputHook, InternalHook


class Hook_t(unittest.TestCase):
    """
    Tests Hook interface for error on construction
    """

    def test_Hook(self):
        "Prove Constructor fails as abstract"
        with self.assertRaises(Exception):
            test = Hook()


class InputHook_t(unittest.TestCase):
    """
    Tests InputHook interface for error on construction
    """

    def test_InputHook(self):
        "Prove Constructor fails as abstract"
        with self.assertRaises(Exception):
            test = InputHook()


class OutputHook_t(unittest.TestCase):
    """
    Tests OutputHook interface for error on construction
    """

    def test_OutputHook(self):
        "Prove Constructor fails as abstract"
        with self.assertRaises(Exception):
            test = OutputHook()


class InternalHook_t(unittest.TestCase):
    """
    Tests InternalHook interface for error on construction
    """

    def test_InternalHook(self):
        "Prove Constructor fails as abstract"
        with self.assertRaises(Exception):
            test = InternalHook()


if __name__ == '__main__':
    unittest.main()
