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
import single_cycle_poc


class SingleCycleProcessor_t(unittest.TestCase):
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
        arch, hooks = single_cycle_poc.generate_single_cycle_architecture()
        single_cycle_poc.program_single_cycle_architecture(arch, program)

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
                'rd2',
            ]
        }

        # generate JSON through simulation
        resultPath = os.path.dirname(os.path.realpath(__file__)) + '\\results\\'
        resultPath = resultPath + filename + '_result'
        self._run_simulation(resultPath, program, 15, msg_inspect)

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
            0xE3A0800A,
            0xE2889001,
            0xE0090998,
            0xE3A0A000,
            0xE24AA020,
            0xE019A00A,
            0x0A000002,
            0xE3A0B001,
            0xE3A0C004,
            0xE58CB000,
            0xE59C6000,
            0xEAFFFFFD
        ]
        self.assertTrue(self._generic_test_procedure('single_cycle_demo', demo_program))

    def test_all_instruction_program(self):
        """
        Test against a program that covers all instructions to flex architecture
        simulation.
        """
        full_program = [
            0xE3A000FF,
            0xE3A01001,
            0xE1A02001,
            0xE3A04C01,
            0xE5840104,
            0xE0803001,
            0xE2814002,
            0xE0024001,
            0xE2034C01,
            0xE0225003,
            0xE0225001,
            0xE3A04C01,
            0xE5945104,
            0xE3A00000,
            0xE3A01000,
            0xE3A02000,
            0xE3A03000,
            0xE3A04000,
            0xE3A05000,
            0xEAFFFFF0,
            0xE2811019,
            0xE2401001,
            0xE0402001,
            0xE3823008,
            0xE1824000,
            0xE3A05C02,
            0xE5853000,
            0xE1500000,
            0x0AFFFFE9,
            0xE0214002,
            0xE5956000,
            0xEBFFFFE9,
            0xE3500000,
            0x1AFFFFE6,
            0xE3A01001,
            0xE3A02000,
            0xEAFFFFE1,
            0xE3A01000,
            0xE3A02000,
            0xEAFFFFDE,
            0xE0810002,
            0xE0020190,
            0xE0230192,
            0xE1A0F00E
        ]

        self.assertTrue(self._generic_test_procedure('single_cycle_full', full_program))


if __name__ == '__main__':
    unittest.main()
