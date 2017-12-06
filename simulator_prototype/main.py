
from components.bus import Bus
from components.clock import Clock
from components.reset import Reset
from components.logic_input import LogicInput

from components.register import Register, Register_Edge_Type, Register_Reset_Type

if __name__ == "__main__":

    clk = Clock('clk',0)
    rst = Reset('rst',0)

    d_bus = LogicInput('d_bus',8,127)
    q_bus = Bus('q_bus',8,0)

    reg = Register('reg',clk,rst,d_bus,q_bus,8,0,Register_Edge_Type.LATCH_RISING_EDGE,Register_Reset_Type.RESET_ACTIVE_HIGH)

    #TODO make this a loop at some point to really prove out the idea

    # this is a comments

    print('-----------------------------------------------------------')
    print(clk.inspect())
    print(rst.inspect())
    print(d_bus.inspect())
    print(reg.inspect())
    print(q_bus.inspect())

    reg.run()

    print('-----------------------------------------------------------')
    print(clk.inspect())
    print(rst.inspect())
    print(d_bus.inspect())
    print(reg.inspect())
    print(q_bus.inspect())

    clk.generate()
    reg.run()

    print('-----------------------------------------------------------')
    print(clk.inspect())
    print(rst.inspect())
    print(d_bus.inspect())
    print(reg.inspect())
    print(q_bus.inspect())

    clk.generate()
    rst.generate()
    reg.run()

    print('-----------------------------------------------------------')
    print(clk.inspect())
    print(rst.inspect())
    print(d_bus.inspect())
    print(reg.inspect())
    print(q_bus.inspect())

    clk.generate()
    rst.generate()
    reg.run()

    print('-----------------------------------------------------------')
    print(clk.inspect())
    print(rst.inspect())
    print(d_bus.inspect())
    print(reg.inspect())
    print(q_bus.inspect())
