
from components.bus import Bus
from components.clock import Clock
from components.reset import Reset
from components.logic_input import LogicInput

from components.register import Register, Register_Edge_Type, Register_Reset_Type
from components.adder import Adder

if __name__ == "__main__":

    clk = Clock('clk',0)
    rst = Reset('rst',0)

    constant = LogicInput('constant-1',8,1)
    carry = Bus('carry',1,0)
    d_bus = Bus('d_bus',8,127)
    q_bus = Bus('q_bus',8,0)

    reg = Register('reg',clk,rst,d_bus,q_bus,8,0,Register_Edge_Type.LATCH_RISING_EDGE,Register_Reset_Type.RESET_ACTIVE_HIGH)
    add = Adder('adder',8,q_bus,constant,d_bus,carry)
    #TODO make this a loop at some point to really prove out the idea

    print('-----------------------------------------------------------')
    print(clk.inspect())
    print(rst.inspect())
    print(d_bus.inspect())
    print(reg.inspect())
    print(q_bus.inspect())

    add.run()
    reg.run()

    print('-----------------------------------------------------------')
    print(clk.inspect())
    print(rst.inspect())
    print(d_bus.inspect())
    print(reg.inspect())
    print(q_bus.inspect())

    clk.generate()
    add.run()
    reg.run()

    print('-----------------------------------------------------------')
    print(clk.inspect())
    print(rst.inspect())
    print(d_bus.inspect())
    print(reg.inspect())
    print(q_bus.inspect())

    clk.generate()
    #rst.generate()
    add.run()
    reg.run()

    print('-----------------------------------------------------------')
    print(clk.inspect())
    print(rst.inspect())
    print(d_bus.inspect())
    print(reg.inspect())
    print(q_bus.inspect())

    clk.generate()
    #rst.generate()
    add.run()
    reg.run()

    print('-----------------------------------------------------------')
    print(clk.inspect())
    print(rst.inspect())
    print(d_bus.inspect())
    print(reg.inspect())
    print(q_bus.inspect())
