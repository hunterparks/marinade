"""
Generic test framework class that can be extended to test various architectures
"""

import unittest
import sys
import os
sys.path.insert(0, '../../')

import json
import tablib  # external library


class TestFramework:
    """
    Generic test framework to simulate a generic architecture and generate
    the pass fail results given the appropriate template file.
    """

    def _set_architecture(self, arch_gen_fnt, arch_prog_fnt):
        """
        Supply an architecture generation function that must return
            architecture object and then hooks list
        Supply an architecture program function that takes
            architecture object and program as an array of bytes
        """
        self._arch_gen_fnt = arch_gen_fnt
        self._arch_prog_fnt = arch_prog_fnt

    def _run_simulation(self, filepath, program, cycles, inspect_msg):
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
        arch, hooks = self._arch_gen_fnt()
        self._arch_prog_fnt(arch, program)

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

        return test.csv == template.csv

    def _generic_test_procedure(self, filename, program, cycles, programname, inspetables):
        """
        General form of complete simulation test procedure.
         1) Runs simulation
         2) Stores results in a JSON file
         3) Generates an Excel file
         4) Compares against template Excel file
        """

        resultPath = os.path.dirname(os.path.realpath(__file__)) + '\\results\\'
        resultPath = resultPath + filename + '_result_' + programname
        self._run_simulation(resultPath, program, cycles, inspetables)

        # generate results in excel table for tracking
        self._process_json_to_excel(resultPath, inspetables['inspect'])

        # process results against template
        templatePath = os.path.dirname(os.path.realpath(__file__)) + '\\templates\\'
        templatePath = templatePath + filename + '_template_' + programname

        return self._compare_against_template(templatePath, resultPath)
