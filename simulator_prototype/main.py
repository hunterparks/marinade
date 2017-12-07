
#TODO git ignore .pyc

import time

from components.bus import Bus
from components.clock import Clock
from components.reset import Reset
from components.logic_input import LogicInput
from components.abstract.sequential import Latch_Type, Logic_States

from components.register import Register
from components.adder import Adder

if __name__ == "__main__":

    clk = Clock('clk',0)
    rst = Reset('rst',0)

    constant = LogicInput('constant-1',8,1)
    enable = LogicInput('enable',1,1)
    carry = Bus('carry',1,0)
    d_bus = Bus('d_bus',8,127)
    q_bus = Bus('q_bus',8,0)

    reg = Register('reg',8,clk,rst,d_bus,q_bus,0,Latch_Type.RISING_EDGE,Logic_States.ACTIVE_HIGH,enable,Logic_States.ACTIVE_HIGH)
    add = Adder('adder',8,q_bus,constant,d_bus,carry)
    add.run()
    reg.run()

    while True:
        print('-----------------------------------------------------------')
        print(clk.inspect())
        print(rst.inspect())
        print(d_bus.inspect())
        print(reg.inspect())
        print(q_bus.inspect())

        clk.generate()
        add.run()
        reg.run()

        time.sleep(0.01)
