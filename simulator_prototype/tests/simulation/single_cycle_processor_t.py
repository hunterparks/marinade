"""
Tests Single Cycle Processor simulation against test programs. Output is
written to JSON files and Excel files.
"""

import unittest
import sys
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
    def _run_simulation(filepath,program,cycles,inspect_msg):
        """
        Iterate through a logical simulation of processor for defined cycles.
        On each iteration capture using the defined message, save results to
        a json file specified in filepath.

        Note that an architecture program is just a list of machine-code
        """

        #open json file
        tf = open(filepath + '.json', 'w')
        tf.write('{"Run":[')

        # generate architecture / program
        arch, hooks = single_cycle_poc.generate_single_cycle_architecture()
        single_cycle_poc.program_single_cycle_architecture(arch,program)

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
    def _process_json_to_excel(filepath,headers):
        """
        Parse JSON file into excel table for comparison and visualization
        """
        data = tablib.Dataset()
        data.headers = headers

        #parse input file
        with open(filepath + '.json', mode='r') as input_json_file:
            input_dict = json.loads(input_json_file.read())

            for step in input_dict["Run"]:
                data.append(['0x{:X}'.format(step[x]["state"]) for x in data.headers])

        data = data.transpose()

        with open(filepath + '.xls', 'wb') as f:
            f.write(data.xls)


    @staticmethod
    def _compare_against_template(templatePath,testPath):
        """
        Compares two excel tables for same contents. Returns true if passes
        else false.
        """
        test = tablib.Dataset().load(open(testPath + '.xls', 'rb').read())
        template = tablib.Dataset().load(open(templatePath + '.xls', 'rb').read())
        return template.dict == test.dict


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

        msg_inspect = {
            'inspect' : [
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
        if __name__ == '__main__':
            resultPath = 'results\\'
        else:
            resultPath = 'simulation\\results\\'
        resultPath = resultPath + 'single_cycle_demo_result'
        self._run_simulation(resultPath,demo_program,15,msg_inspect)

        #generate results in excel table for tracking
        self._process_json_to_excel(resultPath,msg_inspect['inspect'])

        #process results against template
        if __name__ == '__main__':
            templatePath = 'results\\'
        else:
            templatePath = 'simulation\\templates\\'
        templatePath = templatePath + 'single_cycle_demo_template'
        self.assertTrue(self._compare_against_template(templatePath,resultPath))


    def test_all_instruction_program(self):
        """
        Test against a program that covers all instructions to flex architecture
        simulation.
        """
        raise NotImplementedError


if __name__ == '__main__':
    unittest.main()
