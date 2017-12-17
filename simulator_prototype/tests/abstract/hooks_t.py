import unittest
import sys
sys.path.insert(0,'../../')
from components.abstract.hooks import Hook, InputHook, OutputHook, InternalHook

class Hook_t(unittest.TestCase):

    def test_Hook(self):
        "Prove Constructor fails as abstract"
        with self.assertRaises(Exception):
            test = Hook()

class InputHook_t(unittest.TestCase):

    def test_InputHook(self):
        "Prove Constructor fails as abstract"
        with self.assertRaises(Exception):
            test = InputHook()

class OutputHook_t(unittest.TestCase):

    def test_OutputHook(self):
        "Prove Constructor fails as abstract"
        with self.assertRaises(Exception):
            test = OutputHook()

class InternalHook_t(unittest.TestCase):

    def test_InternalHook(self):
        "Prove Constructor fails as abstract"
        with self.assertRaises(Exception):
            test = InternalHook()

if __name__ == '__main__':
    unittest.main()
