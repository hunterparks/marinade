import unittest
import sys
sys.path.insert(0, '../../')
from components.arm.memory import Memory, Latch_Type, Logic_States
from components.core.bus import Bus

class Memory_t(unittest.TestCase):

    def test_constructor(self):
        '''
        tests 2 bad constructors - not all possible bad constructors tested
        '''
        a = Bus(32)
        wd = Bus(32)
        memwr = Bus(1)
        reset = Bus(1)
        clock = Bus(1)
        rd = Bus(32)
        # test case 1
        with self.assertRaises(TypeError):
            mem = Memory(32, wd, memwr, reset, clock, rd)
        # test case 2
        with self.assertRaises(ValueError):
            mem = Memory(a, memwr, wd, reset, clock, rd)

    def test_on_rising_edge(self):
        '''
        tests the memory's on_rising_edge function
        '''
        a = Bus(32)
        wd = Bus(32)
        memwr = Bus(1)
        reset = Bus(1)
        clock = Bus(1)
        rd = Bus(32)
        # test case 3
        a.write(0x1000)
        wd.write(4)
        mem = Memory(a, wd, memwr, reset, clock, rd)
        mem.on_rising_edge()
        self.assertEqual(mem.view_memory_address(a.read()), 0x81818181)
        # test case 4
        mem = Memory(a, wd, memwr, reset, clock, rd, Latch_Type.RISING_EDGE)
        mem.on_rising_edge()
        self.assertEqual(mem.view_memory_address(a.read()), 4)

    def test_on_falling_edge(self):
        '''
        tests the memory's on_falling_edge function
        '''
        a = Bus(32)
        wd = Bus(32)
        memwr = Bus(1)
        reset = Bus(1)
        clock = Bus(1)
        rd = Bus(32)
        # test case 5
        a.write(0x1000)
        wd.write(5)
        mem = Memory(a, wd, memwr, reset, clock, rd)
        mem.on_falling_edge()
        self.assertEqual(mem.view_memory_address(a.read()), 5)
        # test case 6
        a.write(0x1100)
        wd.write(8)
        mem = Memory(a, wd, memwr, reset, clock, rd, Latch_Type.RISING_EDGE)
        mem.on_falling_edge()
        self.assertEqual(mem.view_memory_address(a.read()), 0x81818181)

    def test_on_reset(self):
        a = Bus(32)
        wd = Bus(32)
        memwr = Bus(1)
        reset = Bus(1)
        clock = Bus(1)
        rd = Bus(32)
        # test case 7
        a.write(0x1000)
        wd.write(1)
        mem = Memory(a, wd, memwr, reset, clock, rd)
        mem.on_falling_edge()
        a.write(0x1100)
        wd.write(1)
        mem.on_falling_edge()
        msg = mem.inspect()
        self.assertEqual(msg['size'], 2)
        mem.on_reset()
        msg = mem.inspect()
        self.assertEqual(msg['size'], 0)

    def test_modify(self):
        a = Bus(32)
        wd = Bus(32)
        memwr = Bus(1)
        reset = Bus(1)
        clock = Bus(1)
        rd = Bus(32)
        mem = Memory(a, wd, memwr, reset, clock, rd)
        # test case 8
        mem.modify({'start': 0x1000, 'data': [10, 2]})
        self.assertEqual(mem.view_memory_address(0x1000), 10)
        self.assertEqual(mem.view_memory_address(0x1020), 2)
        # test case 9
        with self.assertRaises(ValueError):
            mem.modify({'star': 0x20, 'data': [5]})

    def test_run(self):
        a = Bus(32)
        wd = Bus(32)
        memwr = Bus(1)
        reset = Bus(1)
        clock = Bus(1)
        rd = Bus(32)
        mem = Memory(a, wd, memwr, reset, clock, rd)
        # test case 10
        a.write(0x1000)
        wd.write(1)
        clock.write(1)
        mem.run()
        self.assertEqual(rd.read(), 0x81818181)
        #test case 11
        clock.write(0)
        memwr.write(1)
        mem.run()
        self.assertEqual(rd.read(), 1)

if __name__ == '__main__':
    unittest.main()
