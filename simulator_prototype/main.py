

#TODO clean up import tree
#TODO unit testing
#TODO documentation !!!!!!

#TODO regfile should be sequential

#TODO shift register

import time

from components.core.bus import Bus
from components.core.clock import Clock
from components.core.reset import Reset
from components.core.logic_input import LogicInput
from components.abstract.sequential import Latch_Type, Logic_States

from components.core.register import Register
from components.core.adder import Adder
from components.arm.register_file_wo_pc import RegisterFile_wo_PC
from components.core.mux import Mux
from components.arm.alu import Alu
from components.core.bus_subset import BusSubset
from components.core.bus_join import BusJoin
from components.core.constant import Constant
from components.arm.memory import Memory
from components.arm.extender import Extender
from components.arm.controller_single_cycle import ControllerSingleCycle

from collections import OrderedDict
from architecture import Architecture

import asyncio
import websockets
import json


import single_cycle_poc


if __name__ == "__main__":


    # single cycle prototype
    arch, hooks = single_cycle_poc.generate_single_cycle_architecture()
    single_cycle_poc.program_single_cycle_architecture(arch)

    #test inspection message
#    msg_inspect = {'inspect' : hooks.keys()}
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

    #test file
    tf = open('single_cycle_data_output.txt', 'w')
    tf.write('{"Run":[')

    count = 0
    while count < 10:
        print('----------------------------------------------------------------')
        rstr = json.dumps(arch.hook(msg_inspect))
        print(rstr)
        if count > 0:
            tf.write(",")
        tf.write(rstr)
        arch.logic_run()
        time.sleep(0.5)
        count += 1

    tf.write(']}')
    tf.close()

    quit()














    # websocket prototype

    clk = Clock(10,0)
    rst = Reset(1)

    b0 = Bus(8,0)
    b1 = Bus(8,0)
    c1 = Constant(8,1)

    reg = Register(8,clk,rst,b0,b1)
    add = Adder(8,c1,b1,b0)

    hooks = OrderedDict([('clk',clk),('rst',rst),('b0',b0),('b1',b1),('c1',c1)])
    entities = OrderedDict([('clk',clk),('add', add),('reg', reg)])

    arch = Architecture(0.0001,clk,rst,hooks,entities)

    msg_inspect = {'inspect' : ['clk','rst','b0','b1','c1']}

    async def interface_to_frontend(websocket, path):
        async for message in websocket:
            msg = json.loads(message)

            retMsg = {}

            if 'hook' in msg:
                retMsg = arch.hook(msg['hook'])

            if 'architecture' in msg:
                if 'simulate' in msg['architecture']:
                    arch.logic_run()
                    retMsg = arch.hook(msg_inspect)

            rxStr = json.dumps(retMsg)
            await websocket.send(rxStr)

    asyncio.get_event_loop().run_until_complete(websockets.serve(interface_to_frontend, 'localhost', 4242))
    asyncio.get_event_loop().run_forever()

    # architecture prototype code

    clk = Clock(10,0)
    rst = Reset(1)

    b0 = Bus(8,0)
    b1 = Bus(8,0)
    c1 = Constant(8,1)

    reg = Register(8,clk,rst,b0,b1)
    add = Adder(8,c1,b1,b0)

    hooks = OrderedDict([('clk',clk),('rst',rst),('b0',b0),('b1',b1),('c1',c1)])
    entities = OrderedDict([('clk',clk),('add', add),('reg', reg)])

    arch = Architecture(0.0001,clk,rst,hooks,entities)

    msg_inspect = {'inspect' : ['clk','rst','b0','b1','c1']}

    while True:
        print(arch.hook(msg_inspect))
        arch.logic_run()
        time.sleep(0.01)


    # prototype code old

    clk = Clock(10,0)
    rst = Reset(1)

    c1 = LogicInput(32,1)
    c2 = LogicInput(1,1)
    address = LogicInput(4,0)

    d_bus = Bus(32,127)
    q_bus = Bus(32,0)
    m_bus = Bus(32,0)
    f_bus = Bus(32,0)
    r_bus = Bus(32,0)
    c_bus = Bus(1,0)
    v_bus = Bus(1,0)
    n_bus = Bus(1,0)
    z_bus = Bus(1,0)

    ss0_bus = Bus(8,0)
    ss1_bus = Bus(8,0)
    ss2_bus = Bus(8,0)
    ss3_bus = Bus(8,0)

    bj0 = Bus(32,0)


    reg = Register(32,clk,rst,d_bus,q_bus)
    add = Adder(32,q_bus,c1,d_bus)
    regFile = Register_File(clk,rst,c2,d_bus,address,address,address,q_bus,m_bus)
    m = Mux(32,[q_bus,m_bus],c2,f_bus)
    alu = Alu(f_bus,q_bus,Bus(1,0),r_bus,c_bus,v_bus,n_bus,z_bus)
    subset = BusSubset(q_bus,[ss0_bus,ss1_bus,ss2_bus,ss3_bus],[(0,8),(8,16),(16,24),(24,32)])
    join = BusJoin([ss3_bus,ss2_bus,ss1_bus,ss0_bus],bj0)

    add.run()
    reg.run()
    regFile.run()
    m.run()
    alu.run()
    subset.run()
    join.run()

    while True:
        print('-----------------------------------------------------------')
        print(clk.inspect())
        print(rst.inspect())
        print(d_bus.inspect())
        print(reg.inspect())
        print(q_bus.inspect())
        print(f_bus.inspect())
        print(r_bus.inspect())
        print(c_bus.inspect())
        print(v_bus.inspect())
        print(n_bus.inspect())
        print(z_bus.inspect())

        print(ss0_bus.inspect())
        print(ss1_bus.inspect())
        print(ss2_bus.inspect())
        print(ss3_bus.inspect())
        print(bj0.inspect())


        clk.generate()
        add.run()
        reg.run()
        regFile.run()
        m.run()
        alu.run()
        subset.run()
        join.run()

        time.sleep(0.01)
