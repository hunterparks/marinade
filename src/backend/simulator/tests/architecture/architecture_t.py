"""
Tests Architecture object which defines a collection of entities and hooks
"""

import unittest
import sys
sys.path.insert(0, '../../')

from collections import OrderedDict

from simulator.architecture import Architecture
from simulator.components.core.bus import Bus
from simulator.components.core.clock import Clock
from simulator.components.core.reset import Reset
from simulator.components.core.constant import Constant

from simulator.components.core.adder import Adder
from simulator.components.core.register import Register


class Architecture_t(unittest.TestCase):
    """
    Tests Architecture's constructor, hook interface, time and logic simulation
    """

    @staticmethod
    def _generate_architecture():
        "Generates a valid simple architecture for test"
        hooks = OrderedDict([('clk', Clock(1)), ('rst', Reset(0))])
        hooks.update({'d_bus': Bus(8, 0)})
        hooks.update({'q_bus': Bus(8, 0)})
        hooks.update({'const_1': Constant(8, 1)})

        entities = OrderedDict([('clk', hooks['clk'])])
        entities.update(
            {'reg': Register(8, hooks['clk'], hooks['rst'], hooks['d_bus'], hooks['q_bus'], default_state=255)})
        hooks.update({'reg': entities['reg']})
        entities.update({'adder': Adder(8, hooks['q_bus'], hooks['const_1'], hooks['d_bus'])})

        arch = Architecture(0.25, hooks['clk'], hooks['rst'], None, hooks, entities)
        return arch, hooks, entities

    def test_constructor(self):
        """
        Test constructor with a simple architecture along with invalid cases.
        """
        hooks = OrderedDict([('clk', Clock(1)), ('rst', Reset(0))])
        hooks.update({'d_bus': Bus(8, 0)})
        hooks.update({'q_bus': Bus(8, 0)})
        hooks.update({'const_1': Constant(8, 1)})

        entities = OrderedDict([('clk', hooks['clk'])])
        entities.update(
            {'reg': Register(8, hooks['clk'], hooks['rst'], hooks['d_bus'], hooks['q_bus'], default_state=255)})
        hooks.update({'reg': entities['reg']})
        entities.update({'adder': Adder(8, hooks['q_bus'], hooks['const_1'], hooks['d_bus'])})

        # time step must be positive
        with self.assertRaises(ValueError):
            arch = Architecture(0, hooks['clk'], hooks['rst'],  None, hooks, entities)

        # time step must not be greater than logic step
        with self.assertRaises(ValueError):
            arch = Architecture(0.6, hooks['clk'], hooks['rst'],  None, hooks, entities)

        # provide a not Clock type clock
        with self.assertRaises(TypeError):
            arch = Architecture(0.25, Bus(1), hooks['rst'],  None, hooks, entities)

        # provide a not Reset type reset
        with self.assertRaises(TypeError):
            arch = Architecture(0.25, hooks['clk'], Bus(1),  None, hooks, entities)

        # provide wrong data structure for hooks
        with self.assertRaises(TypeError):
            arch = Architecture(0.25, Clock(1), Reset(),  None, [], OrderedDict())

        # provide wrong data structure for entities
        with self.assertRaises(TypeError):
            arch = Architecture(0.25, Clock(1), Reset(),  None, OrderedDict(), {})

        # provide wrong data structure for entities
        with self.assertRaises(TypeError):
            arch = Architecture(0.25, Clock(1), Reset(),  None, OrderedDict(), [])

        # construct valid empty architecture
        arch = Architecture(0.25, Clock(1), Reset(),  None, OrderedDict(), OrderedDict())

        # construct valid architecture with contents
        arch = Architecture(0.25, hooks['clk'], hooks['rst'],  None, hooks, entities)

    def test_inspect(self):
        """
        Test inspect interface for valid object inspection
        """
        arch, hooks, entities = self._generate_architecture()

        # valid case
        rmsg = arch.inspect(hooks)
        self.assertEqual(rmsg['reg']['state'], 255)
        self.assertEqual(rmsg['clk']['state'], 0)
        self.assertEqual(rmsg['rst']['state'], 0)
        self.assertEqual(rmsg['d_bus']['state'], 0)
        self.assertEqual(rmsg['q_bus']['state'], 0)
        self.assertEqual(rmsg['const_1']['state'], 1)

        # invalid missing hook in architecture
        rmsg = arch.inspect(['test'])
        self.assertTrue('error' in rmsg['test'])

        # invalid not an iterable type
        rmsg = arch.inspect(7)
        self.assertTrue('error' in rmsg['architecture-hooks-inspect'])

        # invalid not an iterable type
        rmsg = arch.inspect(None)
        self.assertTrue('error' in rmsg['architecture-hooks-inspect'])

        # invalid hook type does not support inspect
        hooks.update({'test': Adder(8, hooks['d_bus'], hooks['q_bus'], Bus(8))})
        rmsg = arch.inspect(['test'])
        self.assertTrue('error' in rmsg['test'])

        # invalid string is not used as an iterable
        hooks.update({'test': Adder(8, hooks['d_bus'], hooks['q_bus'], Bus(8))})
        rmsg = arch.inspect('test')
        self.assertTrue('error' in rmsg['architecture-hooks-inspect'])

        # test with empty
        arch = Architecture(0.25, Clock(1), Reset(), None, OrderedDict(), OrderedDict())
        arch.inspect([])

    def test_modify(self):
        """
        Test modify interface for valid object modify
        """
        arch, hooks, entities = self._generate_architecture()

        # valid operation
        rmsg = arch.hook({'inspect': ['reg']})
        self.assertEqual(rmsg['reg']['state'], 255)
        rmsg = arch.modify({'name': 'reg', 'parameters': {'state': 15}})
        self.assertTrue('reg' in rmsg)
        self.assertTrue(rmsg['reg']['success'])
        rmsg = arch.hook({'inspect': ['reg']})
        self.assertEqual(rmsg['reg']['state'], 15)

        # invalid (lack of entity name)
        rmsg = arch.modify({'came': 'reg', 'parameters': {'state': 25}})
        self.assertTrue('error' in rmsg['architecture-hooks-modify'])
        rmsg = arch.hook({'inspect': ['reg']})
        self.assertEqual(rmsg['reg']['state'], 15)

        # invalid hook is not in architecture
        rmsg = arch.modify({'name': 'test', 'parameters': {'state': 35}})
        self.assertTrue('error' in rmsg['test'])

        # invalid, hook does not support modify
        rmsg = arch.modify({'name': 'rst', 'parameters': {'state': 45}})
        self.assertTrue('error' in rmsg['rst'])
        rmsg = arch.hook({'inspect': ['rst']})
        self.assertEqual(rmsg['rst']['state'], 0)

        # test with empty
        arch = Architecture(0.25, Clock(1), Reset(), None, OrderedDict(), OrderedDict())
        rmsg = arch.modify({'name': 'test', 'parameters': {'state': 99}})
        self.assertTrue('error' in rmsg['test'])

    def test_generate(self):
        """
        Test generate interface for valid object generate
        """
        arch, hooks, entities = self._generate_architecture()

        # valid operation
        rmsg = arch.hook({'inspect': ['clk']})
        self.assertEqual(rmsg['clk']['state'], 0)
        rmsg = arch.generate({'name': 'clk', 'parameters': {'state': 1}})
        self.assertTrue('clk' in rmsg)
        self.assertTrue(rmsg['clk']['success'])
        rmsg = arch.hook({'inspect': ['clk']})
        self.assertEqual(rmsg['clk']['state'], 1)

        # invalid (lack of entity name)
        rmsg = arch.generate({'came': 'clk', 'parameters': {'state': 0}})
        self.assertTrue('error' in rmsg['architecture-hooks-generate'])
        rmsg = arch.hook({'inspect': ['clk']})
        self.assertEqual(rmsg['clk']['state'], 1)

        # invalid hook is not in architecture
        rmsg = arch.generate({'name': 'test', 'parameters': {'state': 0}})
        self.assertTrue('error' in rmsg['test'])

        # invalid, hook does not support generate
        rmsg = arch.generate({'name': 'reg', 'parameters': {'state': 0}})
        self.assertTrue('error' in rmsg['reg'])
        rmsg = arch.hook({'inspect': ['reg']})
        self.assertEqual(rmsg['reg']['state'], 255)

        # test with empty
        arch = Architecture(0.25, Clock(1), Reset(), None, OrderedDict(), OrderedDict())
        rmsg = arch.generate({'name': 'test', 'parameters': {'state': 99}})
        self.assertTrue('error' in rmsg['test'])

    def test_hook(self):
        """
        Test hook interface for general behavior
        """
        arch, hooks, entities = self._generate_architecture()

        # invalid command in message
        rmsg = arch.hook({'test': []})
        self.assertTrue('error' in rmsg['architecture-hooks'])

        # invalid message type
        rmsg = arch.hook(None)
        self.assertTrue('error' in rmsg['architecture-hooks'])

    def test_hook_inspect(self):
        """
        Test hook interface for valid inspect behavior
        """
        arch, hooks, entities = self._generate_architecture()

        # valid case
        rmsg = arch.hook({'inspect': hooks})
        self.assertEqual(rmsg['reg']['state'], 255)
        self.assertEqual(rmsg['clk']['state'], 0)
        self.assertEqual(rmsg['rst']['state'], 0)
        self.assertEqual(rmsg['d_bus']['state'], 0)
        self.assertEqual(rmsg['q_bus']['state'], 0)
        self.assertEqual(rmsg['const_1']['state'], 1)

        # invalid missing hook in architecture
        rmsg = arch.hook({'inspect': ['test']})
        self.assertTrue('error' in rmsg['test'])

        # invalid not an iterable type
        rmsg = arch.hook({'inspect': 7})
        self.assertTrue('error' in rmsg['architecture-hooks-inspect'])

        # invalid not an iterable type
        rmsg = arch.hook({'inspect': None})
        self.assertTrue('error' in rmsg['architecture-hooks-inspect'])

        # invalid hook type does not support inspect
        hooks.update({'test': Adder(8, hooks['d_bus'], hooks['q_bus'], Bus(8))})
        rmsg = arch.hook({'inspect': ['test']})
        self.assertTrue('error' in rmsg['test'])

        # invalid string is not used as an iterable
        hooks.update({'test': Adder(8, hooks['d_bus'], hooks['q_bus'], Bus(8))})
        rmsg = arch.hook({'inspect': 'test'})
        self.assertTrue('error' in rmsg['architecture-hooks-inspect'])

        # test with empty
        arch = Architecture(0.25, Clock(1), Reset(), None, OrderedDict(), OrderedDict())
        arch.hook({'inspect': []})

    def test_hook_modify(self):
        """
        Test hook interface for valid modify behavior
        """
        arch, hooks, entities = self._generate_architecture()

        # valid operation
        rmsg = arch.hook({'inspect': ['reg']})
        self.assertEqual(rmsg['reg']['state'], 255)
        rmsg = arch.hook({'modify': {'name': 'reg', 'parameters': {'state': 15}}})
        self.assertTrue('reg' in rmsg)
        self.assertTrue(rmsg['reg']['success'])
        rmsg = arch.hook({'inspect': ['reg']})
        self.assertEqual(rmsg['reg']['state'], 15)

        # invalid (lack of entity name)
        rmsg = arch.hook({'modify': {'came': 'reg', 'parameters': {'state': 25}}})
        self.assertTrue('error' in rmsg['architecture-hooks-modify'])
        rmsg = arch.hook({'inspect': ['reg']})
        self.assertEqual(rmsg['reg']['state'], 15)

        # invalid hook is not in architecture
        rmsg = arch.hook({'modify': {'name': 'test', 'parameters': {'state': 35}}})
        self.assertTrue('error' in rmsg['test'])

        # invalid, hook does not support modify
        rmsg = arch.hook({'modify': {'name': 'rst', 'parameters': {'state': 45}}})
        self.assertTrue('error' in rmsg['rst'])
        rmsg = arch.hook({'inspect': ['rst']})
        self.assertEqual(rmsg['rst']['state'], 0)

        # test with empty
        arch = Architecture(0.25, Clock(1), Reset(), None, OrderedDict(), OrderedDict())
        rmsg = arch.hook({'modify': {'name': 'test', 'parameters': {'state': 99}}})
        self.assertTrue('error' in rmsg['test'])

    def test_hook_generate(self):
        """
        Test hook interface for valid generate behavior
        """
        arch, hooks, entities = self._generate_architecture()

        # valid operation
        rmsg = arch.hook({'inspect': ['clk']})
        self.assertEqual(rmsg['clk']['state'], 0)
        rmsg = arch.hook({'generate': {'name': 'clk', 'parameters': {'state': 1}}})
        self.assertTrue('clk' in rmsg)
        self.assertTrue(rmsg['clk']['success'])
        rmsg = arch.hook({'inspect': ['clk']})
        self.assertEqual(rmsg['clk']['state'], 1)

        # invalid (lack of entity name)
        rmsg = arch.hook({'generate': {'came': 'clk', 'parameters': {'state': 0}}})
        self.assertTrue('error' in rmsg['architecture-hooks-generate'])
        rmsg = arch.hook({'inspect': ['clk']})
        self.assertEqual(rmsg['clk']['state'], 1)

        # invalid hook is not in architecture
        rmsg = arch.hook({'generate': {'name': 'test', 'parameters': {'state': 0}}})
        self.assertTrue('error' in rmsg['test'])

        # invalid, hook does not support generate
        rmsg = arch.hook({'generate': {'name': 'reg', 'parameters': {'state': 0}}})
        self.assertTrue('error' in rmsg['reg'])
        rmsg = arch.hook({'inspect': ['reg']})
        self.assertEqual(rmsg['reg']['state'], 255)

        # test with empty
        arch = Architecture(0.25, Clock(1), Reset(), None, OrderedDict(), OrderedDict())
        rmsg = arch.hook({'generate': {'name': 'test', 'parameters': {'state': 99}}})
        self.assertTrue('error' in rmsg['test'])

    def test_time_step(self):
        """
        Runs a time simulation step to verify correct end result behavior of
        simple simulation.
        """
        arch, hooks, entities = self._generate_architecture()

        arch.time_step(0)
        rmsg = arch.hook({'inspect': hooks})
        self.assertEqual(rmsg['reg']['state'], 255)
        self.assertEqual(rmsg['clk']['state'], 0)
        self.assertEqual(rmsg['rst']['state'], 0)
        self.assertEqual(rmsg['d_bus']['state'], 0)
        self.assertEqual(rmsg['q_bus']['state'], 255)
        self.assertEqual(rmsg['const_1']['state'], 1)

        arch.time_step(0.5)
        rmsg = arch.hook({'inspect': hooks})
        self.assertEqual(rmsg['reg']['state'], 0)
        self.assertEqual(rmsg['clk']['state'], 1)
        self.assertEqual(rmsg['rst']['state'], 0)
        self.assertEqual(rmsg['d_bus']['state'], 1)
        self.assertEqual(rmsg['q_bus']['state'], 0)
        self.assertEqual(rmsg['const_1']['state'], 1)

        # test with empty
        arch = Architecture(0.25, Clock(1), Reset(), None, OrderedDict(), OrderedDict())
        arch.time_step(0.5)

    def test_time_run(self):
        """
        Runs a time simulation to verify correct end result behavior of simple
        simulation.
        """
        arch, hooks, entities = self._generate_architecture()

        t = arch.time_run(0, 1)
        self.assertEqual(t, 0.25)
        rmsg = arch.hook({'inspect': hooks})
        self.assertEqual(rmsg['reg']['state'], 255)
        self.assertEqual(rmsg['clk']['state'], 0)
        self.assertEqual(rmsg['rst']['state'], 0)
        self.assertEqual(rmsg['d_bus']['state'], 0)
        self.assertEqual(rmsg['q_bus']['state'], 255)
        self.assertEqual(rmsg['const_1']['state'], 1)

        t = arch.time_run(t, 2)
        self.assertEqual(t, 0.75)
        rmsg = arch.hook({'inspect': hooks})
        self.assertEqual(rmsg['reg']['state'], 0)
        self.assertEqual(rmsg['clk']['state'], 1)
        self.assertEqual(rmsg['rst']['state'], 0)
        self.assertEqual(rmsg['d_bus']['state'], 1)
        self.assertEqual(rmsg['q_bus']['state'], 0)
        self.assertEqual(rmsg['const_1']['state'], 1)

        # test with empty
        arch = Architecture(0.25, Clock(1), Reset(), None, OrderedDict(), OrderedDict())
        t = arch.time_run(0, 2)
        t = arch.time_run(t, 3)

    def test_logic_run(self):
        """
        Runs a logic simulation to verify correct end result behavior of simple
        simulation.
        """
        arch, hooks, entities = self._generate_architecture()

        arch.logic_run()
        arch.logic_run()
        arch.logic_run()
        rmsg = arch.hook({'inspect': hooks})

        self.assertEqual(rmsg['reg']['state'], 2)
        self.assertEqual(rmsg['clk']['state'], 1)
        self.assertEqual(rmsg['rst']['state'], 0)
        self.assertEqual(rmsg['d_bus']['state'], 3)
        self.assertEqual(rmsg['q_bus']['state'], 2)
        self.assertEqual(rmsg['const_1']['state'], 1)

        arch, hooks, entities = self._generate_architecture()

        t = arch.logic_run()
        t = arch.logic_run(t)
        t = arch.logic_run(t, 3)
        rmsg = arch.hook({'inspect': hooks})

        self.assertEqual(rmsg['reg']['state'], 4)
        self.assertEqual(rmsg['clk']['state'], 1)
        self.assertEqual(rmsg['rst']['state'], 0)
        self.assertEqual(rmsg['d_bus']['state'], 5)
        self.assertEqual(rmsg['q_bus']['state'], 4)
        self.assertEqual(rmsg['const_1']['state'], 1)

        # test with empty
        arch = Architecture(0.25, Clock(1), Reset(), None, OrderedDict(), OrderedDict())
        t = arch.logic_run(0, 2)
        t = arch.logic_run(t, 3)

    def test_reset(self):
        """
        Runs a simple simulation for some time, then reset.
        Expect sequential components to change state to default.
        After time-step expect buses to be same as initial time-step
        """
        arch, hooks, entities = self._generate_architecture()

        arch.logic_run()
        rmsg = arch.hook({'inspect': ['reg']})
        self.assertTrue('reg' in rmsg)
        self.assertEqual(rmsg['reg']['state'], 0)

        arch.reset()
        rmsg = arch.hook({'inspect': ['reg']})
        self.assertTrue('reg' in rmsg)
        self.assertEqual(rmsg['reg']['state'], 255)

        arch.logic_run()
        rmsg = arch.hook({'inspect': ['reg']})
        self.assertTrue('reg' in rmsg)
        self.assertEqual(rmsg['reg']['state'], 0)

        # test with empty
        arch = Architecture(0.25, Clock(1), Reset(), None, OrderedDict(), OrderedDict())
        arch.reset()

    def test_clear(self):
        """
        Test clear hook behavior
        """
        arch, hooks, entities = self._generate_architecture()

        #write data
        msg = arch.modify({'name':'reg','parameters':{'state':25}})
        msg = arch.inspect(['reg'])
        self.assertEqual(msg['reg']['state'],25)

        # clear memory
        msg = arch.clear(['reg'])
        self.assertTrue('success' in msg['reg'])

        # validate clear
        msg = arch.inspect(['reg'])
        self.assertEqual(msg['reg']['state'],0xFF)

    def test_hook_clear(self):
        """
        Test hook clear behavior
        """
        arch, hooks, entities = self._generate_architecture()

        #write data
        msg = arch.hook({'modify':{'name':'reg','parameters':{'state':25}}})
        msg = arch.hook({'inspect':['reg']})
        self.assertEqual(msg['reg']['state'],25)

        # clear memory
        msg = arch.hook({'clear':['reg']})
        self.assertTrue('success' in msg['reg'])

        # validate clear
        msg = arch.hook({'inspect':['reg']})
        self.assertEqual(msg['reg']['state'],0xFF)

    def test_from_dict(self):
        "Validates dictionary constructor"

        config = {
            "packages" : ["user"],
            "system_clock" : "clk",
            "system_reset" : "rst",
            "system_memory" : None,
            "time_step" : 0.001,

            "signals" : [
                {
                    "name" : "container",
                    "symbolic" : True,
                    "view" : {},
                    "signals" : [
                        {
                            "name" : "clk",
                            "package" : "core",
                            "simulation" : {
                                "model" : "Clock",
                                "frequency" : 1,
                                "append_to_entities" : True,
                                "width" : 1
                            },
                            "view" : {}
                        },
                        {
                            "name" : "rst",
                            "package" : "core",
                            "simulation" : {
                                "model" : "Reset",
                                "width" : 1
                            },
                            "view" : {}
                        },
                        {
                            "name" : "d",
                            "package" : "core",
                            "simulation" : {
                                "model" : "Bus",
                                "width" : 4
                            },
                            "view" : {}
                        },
                        {
                            "name" : "q",
                            "package" : "core",
                            "simulation" : {
                                "model" : "Bus",
                                "width" : 4
                            },
                            "view" : {}
                        },
                        {
                            "name" : "const",
                            "package" : "core",
                            "simulation" : {
                                "model" : "Constant",
                                "width" : 4,
                                "value" : 3
                            },
                            "view" : {}
                        }
                    ]
                }
            ],

            "entities" : [
                {
                    "name" : "container",
                    "symbolic" : True,
                    "view" : {},
                    "entities" : [
                        {
                            "name" : "adder",
                            "package" : "core",
                            "simulation" : {
                                "model" : "Adder",
                                "width" : 4,
                                "input_1" : "const",
                                "input_2" : "q",
                                "output" : "d"
                            },
                            "view" : {}
                        },
                        {
                            "name" : "register",
                            "package" : "core",
                            "simulation" : {
                                "model" : "Register",
                                "append_to_signals" : True,
                                "width" : 4,
                                "clock" : "clk",
                                "reset" : "rst",
                                "input" : "d",
                                "output" : "q",
                                "edge_type" : "both_edge"
                            },
                            "view" : {}
                        }
                    ]
                }
            ]
        }

        arch = Architecture.from_dict(config)

        self.assertEqual(arch.inspect(["q"])["q"]["state"],0)

        arch.logic_run()
        arch.logic_run()
        arch.logic_run()

        self.assertEqual(arch.inspect(["q"])["q"]["state"],15)


if __name__ == '__main__':
    unittest.main()
