"""
Tests Single Cycle Processor simulation against test programs. Output is
written to JSON files and Excel files.
"""

import unittest
import sys
import os
sys.path.insert(0, '../../')

import json
import tablib
import pipeline_poc


class PipelineProcessor_t(unittest.TestCase):
    """
    SingleCycle processor will be validated after simulation for a number of
    clock cycles. Program output will be compared against a template. Only under
    a complete match will simulation be considered valid.
    """

    @staticmethod
    def _run_simulation(filepath, program, cycles, inspect_msg):
        """
        Iterate through a logical simulation of processor for defined cycles.
        On each iteration capture using the defined message, save results to
        a json file specified in filepath.

        Note that an architecture program is just a list of machine-code
        """

        # open json file
        tf = open(filepath + '.json', 'w')
        tf.write('{"Run":[')

        # generate architecture / program
        arch, hooks = pipeline_poc.generate_pipeline_architecture()
        pipeline_poc.program_pipeline_architecture(arch, program)

        # run simulation
        count = 0
        while count < cycles:
            rstr = json.dumps(arch.hook(inspect_msg))
            if count > 0:
                tf.write(",")
            tf.write(rstr)
            arch.logic_run()
            count += 1

        tf.write(']}')
        tf.close()

    @staticmethod
    def _process_json_to_excel(filepath, headers):
        """
        Parse JSON file into excel table for comparison and visualization
        """
        data = tablib.Dataset()
        data.headers = headers

        # parse input file
        with open(filepath + '.json', mode='r') as input_json_file:
            input_dict = json.loads(input_json_file.read())

            for step in input_dict["Run"]:
                data.append(['0x{:X}'.format(step[x]["state"]) for x in data.headers])

        data = data.transpose()

        with open(filepath + '.xls', 'wb') as f:
            f.write(data.xls)

    @staticmethod
    def _compare_against_template(templatePath, testPath):
        """
        Compares two excel tables for same contents. Returns true if passes
        else false.
        """
        testf = open(testPath + '.xls', 'rb')
        templatef = open(templatePath + '.xls', 'rb')
        test = tablib.Dataset().load(testf.read())
        template = tablib.Dataset().load(templatef.read())
        testf.close()
        templatef.close()
        return template.dict == test.dict

    def _generic_test_procedure(self, filename, program):
        """
        General form of complete simulation test procedure.
         1) Runs simulation
         2) Stores results in a JSON file
         3) Generates an Excel file
         4) Compares against template Excel file
        """
        msg_inspect = {
            'inspect': [
                'clk',
                'rst',
                'instrf',
                'instrd',
                'wd3',
                'pc4',
                'ra1e',
                'ra2e',
                'ra3e',
                'ra3m',
                'ra3w',
                'fe',
                'fm',
                'fw',
                'fwda',
                'fwdb',
                'rd1d',
                'rd1',
                'rd2d',
                'rd2e',
                'rd2',
                'rd2m',
                'imm32d',
                'imm32e',
                'alub',
                'aluse',
                'regwrw',
                'regsrcw'
            ]
        }

        # generate JSON through simulation
        resultPath = os.path.dirname(os.path.realpath(__file__)) + '\\results\\'
        resultPath = resultPath + filename + '_result'
        self._run_simulation(resultPath, program, 31, msg_inspect)

        # generate results in excel table for tracking
        self._process_json_to_excel(resultPath, msg_inspect['inspect'])

        # process results against template
        templatePath = os.path.dirname(os.path.realpath(__file__)) + '\\templates\\'
        templatePath = templatePath + filename + '_template'

        return self._compare_against_template(templatePath, resultPath)

    def test_demo_program(self):
        """
        Test against a simple demo program to prove general operation
        """
        demo_program = [
            0xE3, 0xA0, 0xA0, 0x0A,
            0xE3, 0xA0, 0x90, 0x09,
            0xE3, 0xA0, 0x80, 0x08,
            0xE3, 0xA0, 0x70, 0x07,
            0xE3, 0xA0, 0x60, 0x06,
            0xE3, 0xA0, 0x50, 0x05,
            0xE3, 0xA0, 0x40, 0x04,
            0xE3, 0xA0, 0x30, 0x03,
            0xE3, 0xA0, 0x20, 0x02,
            0xE3, 0xA0, 0x10, 0x01,
            0xE0, 0x8A, 0xC0, 0x09,
            0xE0, 0x8C, 0xC0, 0x08,
            0xE0, 0x8C, 0xC0, 0x07,
            0xE0, 0x8C, 0xC0, 0x06,
            0xE0, 0x8C, 0xC0, 0x05,
            0xE0, 0x84, 0xC0, 0x0C,
            0xE0, 0x83, 0xC0, 0x0C,
            0xE0, 0x82, 0xC0, 0x0C,
            0xE0, 0x81, 0xC0, 0x0C,
            0xE3, 0xA0, 0x00, 0x00,
            0xE3, 0xA0, 0x10, 0x01,
            0xE3, 0xA0, 0x20, 0x04,
            0xE2, 0x40, 0x00, 0x20,
            0xE0, 0x0C, 0xC0, 0x00,
            0xE5, 0x82, 0xC0, 0x00,
            0xE5, 0x92, 0x60, 0x00,
            0xE5, 0x92, 0x60, 0x00,
            0xE5, 0x92, 0x60, 0x00,
            0xE5, 0x92, 0x60, 0x00,
            0xE5, 0x92, 0x60, 0x00
        ]
        self.assertTrue(self._generic_test_procedure('pipeline_demo', demo_program))

    def test_all_instruction_program(self):
        """
        Test against a program that covers all instructions to flex architecture
        simulation.
        """
        pass
        """
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

        self.assertTrue(self._generic_test_procedure('pipeline_full', full_program))
        """


if __name__ == '__main__':
    unittest.main()
