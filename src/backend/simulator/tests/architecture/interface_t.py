"""
Tests main backend program's API
"""

import unittest
import sys
import os

sys.path.insert(0,'../../../')
sys.path.insert(0,'../../../../')
from simulator.interface import Interface

TEST_ARCH_PATH = os.path.join(os.path.dirname(__file__),'test_architecture.json')
TEST_PROGRAM_PATH = os.path.join(os.path.dirname(__file__),'test_program.bint')
TEST_ASSEMBLE_PATH = os.path.join(os.path.dirname(__file__),'test_assemble.s')

class Interface_t(unittest.TestCase):
    """
    Test main interface API to validate correct API operation
    """

    def test_constructor(self):
        "Standard test for constructor"
        interface = Interface()

    def test_parse_command(self):
        "Test API parse"
        interface = Interface()
        retMsg = interface.parse_command({})
        self.assertEqual(retMsg,{})

        # load
        retMsg = interface.parse_command({
            'load' : {
                'filepath' : TEST_ARCH_PATH
            }
        })
        self.assertEqual(retMsg,{'status':True})

        # step
        retMsg = interface.parse_command({
            'step' : {
                'type' : 'logic'
            }
        })
        self.assertEqual(retMsg,{'status':True})

        # reset
        retMsg = interface.parse_command({'reset':{}})
        self.assertEqual(retMsg,{'status':True})

        # program
        retMsg = interface.parse_command({
            'program' : {
                'filepath':TEST_PROGRAM_PATH,'memory':'memory'
            }
        })
        self.assertTrue(retMsg['memory']['success'])

        # inspect
        retMsg = interface.parse_command({'inspect':['q']})
        self.assertIn('q',retMsg)

        # unload
        retMsg = interface.parse_command({'unload':{}})
        self.assertEqual(retMsg,{'status':True})

        # assemble
        retMsg = interface.parse_command({
            'assemble' : {
                'filepath':TEST_ASSEMBLE_PATH
            }
        })
        self.assertEqual(retMsg['errors'],'')

    def test_assemble(self):
        "Test assemble (requires GCC)"
        interface = Interface()
        retMsg = interface.assemble({'filepath':TEST_ASSEMBLE_PATH})
        self.assertEqual(retMsg['errors'],'')

    def test_step(self):
        "Test architecture clock step"
        interface = Interface()
        retMsg = interface.load({'filepath':TEST_ARCH_PATH})
        self.assertEqual(retMsg,{'status':True})

        retMsg = interface.handle_component_msg({'inspect':['q']})
        value_1 = retMsg['q']['state']

        retMsg = interface.step({'type':'logic'})
        self.assertEqual(retMsg,({'status':True}))

        retMsg = interface.handle_component_msg({'inspect':['q']})
        value_2 = retMsg['q']['state']

        self.assertNotEqual(value_1,value_2)

    def test_reset(self):
        "Test reset of architecture"
        interface = Interface()
        retMsg = interface.load({'filepath':TEST_ARCH_PATH})
        self.assertEqual(retMsg,{'status':True})

        retMsg = interface.handle_component_msg({'inspect':['q']})
        value_1 = retMsg['q']['state']

        retMsg = interface.step({'type':'logic'})
        self.assertEqual(retMsg,({'status':True}))

        retMsg = interface.handle_component_msg({'inspect':['q']})
        value_2 = retMsg['q']['state']

        self.assertNotEqual(value_1,value_2)

        retMsg = interface.reset()
        self.assertEqual(retMsg,{'status':True})

        retMsg = interface.handle_component_msg({'inspect':['q']})
        value_3 = retMsg['q']['state']

        self.assertEqual(value_1,value_3)

    def test_load(self):
        "Test load of architecture"
        interface = Interface()
        retMsg = interface.load({'filepath':TEST_ARCH_PATH})
        self.assertEqual(retMsg,{'status':True})

    def test_unload(self):
        "Test unload of architecture"
        interface = Interface()
        retMsg = interface.load({'filepath':TEST_ARCH_PATH})
        self.assertEqual(retMsg,{'status':True})
        retMsg = interface.unload()
        self.assertEqual(retMsg,{'status':True})

    def test_program(self):
        "Test program function for a valid architecture"
        interface = Interface()
        retMsg = interface.load({'filepath':TEST_ARCH_PATH})
        self.assertEqual(retMsg,{'status':True})

        retMsg = interface.handle_component_msg({'inspect':['memory']})
        self.assertEqual(len(retMsg['memory']['state']),0)

        retMsg = interface.program({'filepath':TEST_PROGRAM_PATH,'memory':'memory'})
        self.assertTrue(retMsg['memory']['success'])

        retMsg = interface.handle_component_msg({'inspect':['memory']})
        self.assertNotEqual(len(retMsg['memory']['state']),0)

    def test_handle_component_msg(self):
        "Test architecture hook API router"
        interface = Interface()
        retMsg = interface.load({'filepath':TEST_ARCH_PATH})
        self.assertEqual(retMsg,{'status':True})

        retMsg = interface.handle_component_msg({'inspect':['q']})
        self.assertIn('q',retMsg)

        retMsg = interface.handle_component_msg({
            'modify' : {
                'name' : 'memory',
                'parameters' : {
                    'start' : 0,
                    'data' : [10,20,30,40,50,60,70,80]
                }
            }
        })
        self.assertTrue(retMsg['memory']['success'])

        retMsg = interface.handle_component_msg({'inspect':['memory']})
        self.assertEqual(retMsg['memory']['state'][7],80)

        retMsg = interface.handle_component_msg({'clear' : ['memory']})
        self.assertTrue(retMsg['memory']['success'])

        retMsg = interface.handle_component_msg({'inspect':['memory']})
        self.assertEqual(len(retMsg['memory']['state']),0)

        retMsg = interface.handle_component_msg({'inspect':['const']})
        value_1 = retMsg['const']['state']

        retMsg = interface.handle_component_msg({
            'generate' : {
                'name' : 'const',
                'parameters' : {
                    'state' : value_1 + 1
                }
            }
        })
        self.assertTrue(retMsg['const']['success'])

        retMsg = interface.handle_component_msg({'inspect':['const']})
        value_2 = retMsg['const']['state']

        self.assertNotEqual(value_1,value_2)


if __name__ == "__main__":
    unittest.main()
