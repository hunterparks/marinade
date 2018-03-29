"""
Tests Single Cycle Processor simulation against test programs. Output is
written to JSON files and Excel files.
"""

import unittest
import sys
sys.path.insert(0, '../../')

import single_cycle_poc
from tests.simulation.test_framework import TestFramework


class SingleCycleProcessor_t(TestFramework, unittest.TestCase):
    """
    SingleCycle processor will be validated after simulation for a number of
    clock cycles. Program output will be compared against a template. Only under
    a complete match will simulation be considered valid.
    """

    demo_program = [
        0xE3, 0xA0, 0x80, 0x0A,
        0xE2, 0x88, 0x90, 0x01,
        0xE0, 0x09, 0x09, 0x98,
        0xE3, 0xA0, 0xA0, 0x00,
        0xE2, 0x4A, 0xA0, 0x20,
        0xE0, 0x19, 0xA0, 0x0A,
        0x0A, 0x00, 0x00, 0x02,
        0xE3, 0xA0, 0xB0, 0x01,
        0xE3, 0xA0, 0xC0, 0x04,
        0xE5, 0x8C, 0xB0, 0x00,
        0xE5, 0x9C, 0x60, 0x00,
        0xEA, 0xFF, 0xFF, 0xFD
    ]

    demo_inspect = {
        'inspect': [
            'clk',
            'rst',
            'wdb',
            'pc4',
            'branch',
            'instr',
            'pcsrc',
            'pcwr',
            'regsa',
            'regdst',
            'regwrs',
            'regwr',
            'exts',
            'alus',
            'aluflagwr',
            'memwr',
            'regsrc',
            'wdbs',
            'imm32',
            'rd1',
            'rd2'
        ]
    }

    required_program = [
        0xe3, 0xa0, 0x20, 0x0a,
        0xe1, 0xa0, 0x30, 0x02,
        0xe1, 0xa0, 0x40, 0x03,
        0xe0, 0x82, 0x10, 0x03,
        0xe2, 0x82, 0x10, 0x01,
        0xe0, 0x02, 0x10, 0x03,
        0xe2, 0x02, 0x10, 0x01,
        0xe1, 0x51, 0x00, 0x01,
        0xe3, 0x51, 0x00, 0x01,
        0xe0, 0x22, 0x10, 0x03,
        0xe2, 0x22, 0x10, 0x01,
        0xe0, 0x01, 0x03, 0x92,
        0xe0, 0x21, 0x43, 0x92,
        0xe1, 0x82, 0x10, 0x03,
        0xe3, 0x82, 0x10, 0x01,
        0xe0, 0x42, 0x10, 0x03,
        0xe2, 0x42, 0x10, 0x01,
        0xe5, 0x82, 0x10, 0x00,
        0xe5, 0x83, 0x20, 0x04,
        0xe5, 0x92, 0x50, 0x00,
        0xe5, 0x93, 0x50, 0x04,
        0xea, 0x00, 0x00, 0x00,
        0xe2, 0x80, 0x00, 0x00,
        0xeb, 0x00, 0x00, 0x02,
        0xe2, 0x80, 0x00, 0x00,
        0xe2, 0x80, 0x00, 0x00,
        0xe2, 0x80, 0x00, 0x00,
        0xe3, 0xa0, 0x10, 0x01,
        0xe3, 0xa0, 0x00, 0x00,
        0xe0, 0x80, 0x21, 0x01,
        0xe0, 0x80, 0x31, 0xe2,
        0x0a, 0x00, 0x00, 0x02,
        0xe2, 0x80, 0x00, 0x00,
        0x1a, 0x00, 0x00, 0x00,
        0xe2, 0x80, 0x00, 0x00,
        0xea, 0xff, 0xff, 0xdb
    ]

    required_inspect = {
        'inspect': [
            'clk',
            'rst',
            'instr',
            'pc4',
            'wdb',
            'z'
        ]
    }

    def test_demo_program(self):
        """
        Test against a simple demo program to prove general operation
        """

        self._set_architecture(single_cycle_poc.generate_single_cycle_architecture,
                               single_cycle_poc.program_single_cycle_architecture)
        self.assertTrue(self._generic_test_procedure(
            'single_cycle_demo', self.demo_program, len(self.demo_program) / 4 + 2, 'demo_prog', self.demo_inspect))

    def test_all_instruction_program(self):
        """
        Test against a program that covers all instructions to flex architecture
        simulation.
        """

        self._set_architecture(single_cycle_poc.generate_single_cycle_architecture,
                               single_cycle_poc.program_single_cycle_architecture)
        self.assertTrue(self._generic_test_procedure(
            'single_cycle_demo', self.required_program, len(self.required_program) / 4 + 2, 'full_prog', self.required_inspect))


if __name__ == '__main__':
    unittest.main()
