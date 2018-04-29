"""
Tests Single Cycle Processor simulation against test programs. Output is
written to JSON files and Excel files.
"""

import unittest
import sys
import os
sys.path.insert(0, '../../../')

import json
import tablib

from simulator.architecture import Architecture
from simulator.tests.simulation.test_framework import TestFramework
from simulator.tests.simulation import pipeline_poc

PIPELINE_DEMO_CONFIG_FILEPATH = os.path.join(os.path.dirname(
    __file__), "../../../../config/architectures/pipeline_demo.json")


class PipelineProcessor_t(TestFramework, unittest.TestCase):
    """
    SingleCycle processor will be validated after simulation for a number of
    clock cycles. Program output will be compared against a template. Only under
    a complete match will simulation be considered valid.
    """

    msg_inspect = {
        'inspect': [
            'clk',
            'rst',
            'instrf',
            'instrd',
            'wd3',
            'pc4d',
            'braddr',
            'fe',
            'rdw',
            'fm',
            'fw',
            'rd1e',
            'fwda',
            'rd1',
            'rd2e',
            'fwdb',
            'rd2',
            'rd2m',
            'alub',
            'aluse',
            'ra1e',
            'ra2e',
            'ra3e',
            'ra3m',
            'ra3w',
            'regwrd',
            'regwre',
            'regwrm',
            'regwrw',
            'regsrcm',
            'regsrcw',
            'memwrm',
            'pcsrcd',
            'imm32e'
        ]
    }

    demo_program = [
        0xE3, 0xA0, 0xA0, 0x0A,     # mov r10, #10
        0xE3, 0xA0, 0x90, 0x09,     # mov r9, #9
        0xE3, 0xA0, 0x80, 0x08,     # mov r8, #8
        0xE3, 0xA0, 0x70, 0x07,     # mov r7, #7
        0xE3, 0xA0, 0x60, 0x06,     # mov r6, #6
        0xE3, 0xA0, 0x50, 0x05,     # mov r5, #5
        0xE3, 0xA0, 0x40, 0x04,     # mov r4, #4
        0xE3, 0xA0, 0x30, 0x03,     # mov r3, #3
        0xE3, 0xA0, 0x20, 0x02,     # mov r2, #2
        0xE3, 0xA0, 0x10, 0x01,     # mov r1, #1
        0xE3, 0xA0, 0xD0, 0x0D,     # mov r13, #13
        0xE5, 0x84, 0xD0, 0x00,     # str r13, [r4]
        0xE5, 0x94, 0xD0, 0x00,     # ldr r13, [r4]
        0xE5, 0x84, 0x60, 0x00,     # str r6, [r4]
        0xE5, 0x94, 0x50, 0x00,     # ldr r5, [r4]
        0xE3, 0xA0, 0x60, 0x06,     # mov r6, #6
        0xE2, 0x45, 0x50, 0x01,     # sub r5, r5, #1
        0xE0, 0x8A, 0xC0, 0x09,     # add r12, r10, r9
        0xE0, 0x8C, 0xC0, 0x08,     # add r12, r12, r8
        0xE0, 0x8C, 0xC0, 0x07,     # add r12, r12, r7
        0xE0, 0x8C, 0xC0, 0x06,     # add r12, r12, r6
        0xE0, 0x8C, 0xC0, 0x05,     # add r12, r12, r5
        0xE0, 0x84, 0xC0, 0x0C,     # add r12, r4, r12
        0xE0, 0x83, 0xC0, 0x0C,     # add r12, r3, r12
        0xE0, 0x82, 0xC0, 0x0C,     # add r12, r2, r12
        0xE0, 0x81, 0xC0, 0x0C,     # add r12, r1, r12
        0xE3, 0xA0, 0x00, 0x00,     # mov r0, #0
        0xE3, 0xA0, 0x10, 0x01,     # mov r1, #1
        0xE3, 0xA0, 0x20, 0x04,     # mov r2, #4
        0xE2, 0x40, 0x00, 0x20,     # sub r0, r0, #32
        0xE0, 0x0C, 0xC0, 0x00,     # and r12, r12, r0
        0xE5, 0x82, 0xC0, 0x00,     # str r12, [r2]
        0xE5, 0x92, 0x60, 0x00,     # ldr r6, [r2]
        0xE5, 0x92, 0x60, 0x00,     # ldr r6, [r2]
        0xE5, 0x92, 0x60, 0x00,     # ldr r6, [r2]
        0xE5, 0x92, 0x60, 0x00,     # ldr r6, [r2]
        0xE5, 0x92, 0x60, 0x00      # ldr r6, [r2]
    ]

    branch_hazards_program = [
        0xE3, 0xA0, 0x00, 0x0A,     # mov r0, #10       (main)
        0xEB, 0x00, 0x00, 0x09,     # bl sumn
        0xE3, 0xA0, 0xA0, 0x00,     # mov r10, #0       (if)
        0xE2, 0x4A, 0xA0, 0x20,     # sub r10, r10, #32
        0xE0, 0x00, 0xA0, 0x0A,     # and r10, r0, r10
        0xE3, 0x5A, 0x00, 0x00,     # cmp r10, #0
        0x0A, 0x00, 0x00, 0x01,     # beq done
        0xE3, 0xA0, 0xB0, 0x01,     # mov r11, #1
        0xE3, 0xA0, 0xC0, 0x04,     # mov r12, #4
        0xE5, 0x8C, 0xB0, 0x00,     # str r11, [r12]
        0xE5, 0x9C, 0x60, 0x00,     # ldr r6, [r12]     (done)
        0xEA, 0xFF, 0xFF, 0xFD,     # b done
        0xE3, 0x50, 0x00, 0x00,     # cmp r0, #0        (sumn)
        0x0A, 0x00, 0x00, 0x04,     # beq sumexit
        0xE3, 0xA0, 0x10, 0x00,     # mov r1, #0
        0xE0, 0x81, 0x10, 0x00,     # add r1, r1, r0    (loop)
        0xE2, 0x50, 0x00, 0x01,     # subs r0, r0, #1
        0x1A, 0xFF, 0xFF, 0xFC,     # bne loop
        0xE1, 0xA0, 0x00, 0x01,     # mov r0, r1
        0xE1, 0xA0, 0xF0, 0x0E      # mov pc, lr        (sumexit)
    ]

    full_program = [
        0xE3, 0xA0, 0x00, 0xFF,
        0xE3, 0xA0, 0x10, 0x01,
        0xE1, 0xA0, 0x20, 0x01,
        0xE3, 0xA0, 0x4C, 0x01,
        0xE5, 0x84, 0x01, 0x04,
        0xE0, 0x80, 0x30, 0x01,
        0xE2, 0x81, 0x40, 0x02,
        0xE0, 0x02, 0x40, 0x01,
        0xE2, 0x03, 0x4C, 0x01,
        0xE0, 0x22, 0x50, 0x03,
        0xE0, 0x22, 0x50, 0x01,
        0xE3, 0xA0, 0x4C, 0x01,
        0xE5, 0x94, 0x51, 0x04,
        0xE3, 0xA0, 0x00, 0x00,
        0xE3, 0xA0, 0x10, 0x00,
        0xE3, 0xA0, 0x20, 0x00,
        0xE3, 0xA0, 0x30, 0x00,
        0xE3, 0xA0, 0x40, 0x00,
        0xE3, 0xA0, 0x50, 0x00,
        0xEA, 0xFF, 0xFF, 0xF0,
        0xE2, 0x81, 0x10, 0x19,
        0xE2, 0x40, 0x10, 0x01,
        0xE0, 0x40, 0x20, 0x01,
        0xE3, 0x82, 0x30, 0x08,
        0xE1, 0x82, 0x40, 0x00,
        0xE3, 0xA0, 0x5C, 0x02,
        0xE5, 0x85, 0x30, 0x00,
        0xE1, 0x50, 0x00, 0x00,
        0x0A, 0xFF, 0xFF, 0xE9,
        0xE0, 0x21, 0x40, 0x02,
        0xE5, 0x95, 0x60, 0x00,
        0xEB, 0xFF, 0xFF, 0xE9,
        0xE3, 0x50, 0x00, 0x00,
        0x1A, 0xFF, 0xFF, 0xE6,
        0xE3, 0xA0, 0x10, 0x01,
        0xE3, 0xA0, 0x20, 0x00,
        0xEA, 0xFF, 0xFF, 0xE1,
        0xE3, 0xA0, 0x10, 0x00,
        0xE3, 0xA0, 0x20, 0x00,
        0xEA, 0xFF, 0xFF, 0xDE,
        0xE0, 0x81, 0x00, 0x02,
        0xE0, 0x02, 0x01, 0x90,
        0xE0, 0x23, 0x01, 0x92,
        0xE1, 0xA0, 0xF0, 0x0E
    ]

    def test_demo_program(self):
        """
        Test against a simple demo program to prove general operation
        """
        self._set_architecture(pipeline_poc.generate_pipeline_architecture,
                               pipeline_poc.program_pipeline_architecture)
        self.assertTrue(self._generic_test_procedure('pipeline_demo', self.demo_program,
                        len(self.demo_program) / 4 + 2, 'demo_prog', self.msg_inspect))

    def test_branch_hazards_program(self):
        """
        Tests against a branch hazards program to assure branch hazards work
        """
        self._set_architecture(pipeline_poc.generate_pipeline_architecture,
                               pipeline_poc.program_pipeline_architecture)
        self.assertTrue(self._generic_test_procedure('pipeline_branch_hazards',
                        self.branch_hazards_program, len(self.branch_hazards_program) / 4 + 2,
                        'hazards_prog', self.msg_inspect))

    def test_all_instruction_program(self):
        """
        Test against a program that covers all instructions to flex architecture
        simulation.
        """
        pass
        """
        self.assertTrue(self._generic_test_procedure('pipeline_full', full_program))
        """

    def test_config_file_demo(self):
        """
        Test config file form against demo program to prove general operation
        """
        def _gen():
            f = open(PIPELINE_DEMO_CONFIG_FILEPATH)
            config = json.loads(f.read())
            arch = Architecture.from_dict(config)
            hooks = arch.get_hooks()
            f.close()
            return arch, hooks

        def _prog(arch, prog):
            program_msg = {
                'modify': {
                    'name': 'progmem',
                    'parameters': {
                        'start': 0,
                        'data': prog
                    }
                }
            }
            res = arch.hook(program_msg)

        self._set_architecture(_gen, _prog)
        self.assertTrue(self._generic_test_procedure('pipeline_config_demo',
                        self.demo_program, len(self.demo_program) / 4 + 2,
                        'demo_prog', self.msg_inspect))

    def test_config_file_hardware(self):
        """
        Tests against a branch hazards program to assure branch hazards work
        """
        def _gen():
            f = open(PIPELINE_DEMO_CONFIG_FILEPATH)
            config = json.loads(f.read())
            arch = Architecture.from_dict(config)
            hooks = arch.get_hooks()
            f.close()
            return arch, hooks

        def _prog(arch, prog):
            program_msg = {
                'modify': {
                    'name': 'progmem',
                    'parameters': {
                        'start': 0,
                        'data': prog
                    }
                }
            }
            res = arch.hook(program_msg)

        self._set_architecture(_gen, _prog)
        self.assertTrue(self._generic_test_procedure('pipeline_config_branch_hazards',
                        self.branch_hazards_program, len(self.branch_hazards_program) / 4 + 2,
                        'hazards_prog', self.msg_inspect))

    def test_config_file_full(self):
        """
        Test config file form against full program to prove general operation
        """
        pass


if __name__ == '__main__':
    unittest.main()
