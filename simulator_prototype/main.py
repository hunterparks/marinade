

#TODO clean up import tree
#TODO code all components for single-cycle
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
from components.arm.register_file import Register_File
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





if __name__ == "__main__":

    """
    # single cycle prototype

    #define system resources
    clk = Clock(10,0)
    rst = Reset(1)
    hooks = OrderedDict([('clk',clk),('rst',rst)])

    #define input hooks and constants
    hooks.update({'const8' : Constant(32,8)})
    hooks.update({'const4' : Constant(32,4)})
    hooks.update({'const14' : Constant(4,14)})
    hooks.update({'pmd' : LogicInput(32,0)})
    hooks.update({'pmwr' : LogicInput(1,0)})

    # define buses
    hooks.update({'pc' : Bus(32,0)})
    hooks.update({'pc8' : Bus(32,0)})
    hooks.update({'pc4' : Bus(32,0)})
    hooks.update({'instr' : Bus(32,0)})
    hooks.update({'instr_23_0' : Bus(24,0)})
    hooks.update({'instr_19_16' : Bus(4,0)})
    hooks.update({'instr_3_0' : Bus(4,0)})
    hooks.update({'instr_15_12' : Bus(4,0)})
    hooks.update({'instr_11_8' : Bus(4,0)})
    hooks.update({'instr_31_28' : Bus(4,0)})
    hooks.update({'instr_27_26' : Bus(2,0)})
    hooks.update({'instr_25_20' : Bus(6,0)})
    hooks.update({'instr_4_4' : Bus(1,0)})
    hooks.update({'imm32' : Bus(32,0)})
    hooks.update({'ra1' : Bus(4,0)})
    hooks.update({'ra2' : Bus(4,0)})
    hooks.update({'ra3' : Bus(4,0)})
    hooks.update({'rwd' : Bus(32,0)})
    hooks.update({'rd1' : Bus(32,0)})
    hooks.update({'rd2' : Bus(32,0)})
    hooks.update({'alub' : Bus(32,0)})
    hooks.update({'branch' : Bus(32,0)})
    hooks.update({'aluf' : Bus(32,0)})
    hooks.update({'aluc' : Bus(1,0)})
    hooks.update({'aluv' : Bus(1,0)})
    hooks.update({'alun' : Bus(1,0)})
    hooks.update({'aluz' : Bus(1,0)})
    hooks.update({'aluflag' : Bus(4,0)})
    hooks.update({'flag' : Bus(4,0)})
    hooks.update({'c' : Bus(1,0)})
    hooks.update({'v' : Bus(1,0)})
    hooks.update({'n' : Bus(1,0)})
    hooks.update({'z' : Bus(1,0)})
    hooks.update({'memrd' : Bus(32,0)})
    hooks.update({'wdb' : Bus(32,0)})
    hooks.update({'pcwb' : Bus(32,0)})

    #control signals
    hooks.update({'pcwr' : Bus(1,0)})
    hooks.update({'regsa' : Bus(1,0)})
    hooks.update({'regdst' : Bus(2,0)})
    hooks.update({'regwrs' : Bus(2,0)})
    hooks.update({'wdbs' : Bus(1,0)})
    hooks.update({'regwr' : Bus(1,0)})
    hooks.update({'exts' : Bus(2,0)})
    hooks.update({'alu8rcb' : Bus(1,0)})
    hooks.update({'alus' : Bus(4,0)})
    hooks.update({'aluflagwr' : Bus(1,0)})
    hooks.update({'memwr' : Bus(1,0)})
    hooks.update({'regsrc' : Bus(1,0)})
    hooks.update({'pcsrc' : Bus(2,0)})

    # generate components
    entities = OrderedDict([('clk',clk)])
    entities.update({'pc_reg' : Register(32,hooks['clk'],hooks['rst'],hooks['pcwb'],hooks['pc'],0, enable = hooks['pcwr'])})
    entities.update({'add8' : Adder(32,hooks['pc'],hooks['const8'],hooks['pc8'])})
    entities.update({'add4' : Adder(32,hooks['pc'],hooks['const4'],hooks['pc4'])})
    entities.update({'progmem' : Memory(hooks['pc'],hooks['pmd'],hooks['pmwr'],hooks['clk'],hooks['rst'],hooks['instr'])})

    entities.update({'instr_subset' : BusSubset(hooks['instr'],
                    [hooks['instr_23_0'],hooks['instr_19_16'],
                     hooks['instr_3_0'],hooks['instr_15_12'],
                     hooks['instr_11_8'],hooks['instr_31_28'],
                     hooks['instr_27_26'],hooks['instr_25_20'],
                     hooks['instr_4_4']],
                    [(0,24),(16,20),(0,4),(12,16),(8,12),(28,32),(26,28),(20,26),(4,5)])})
    entities.update({'ra1_mux' : Mux(4,[hooks['instr_3_0'],hooks['instr_19_16']],hooks['regsa'],hooks['ra1'])})
    entities.update({'ra2_mux' : Mux(4,[hooks['instr_11_8'],hooks['instr_3_0'],hooks['instr_15_12']],hooks['regdst'],hooks['ra2'])})
    entities.update({'ra3_mux' : Mux(4,[hooks['instr_19_16'],hooks['instr_15_12'],hooks['const14']],hooks['regwrs'],hooks['ra3'])})
    entities.update({'rwd_mux' : Mux(32,[hooks['wdb'],hooks['pc4']],hooks['wdbs'],hooks['rwd'])})
    entities.update({'extimm' : Extender(hooks['instr_23_0'],hooks['imm32'],hooks['exts'])})
    entities.update({'regfile' : Register_File(hooks['clk'],hooks['rst'],hooks['regwr'],hooks['rwd'],hooks['ra1'],hooks['ra2'],hooks['ra3'],hooks['rd1'],hooks['rd2'])})

    entities.update({'alu_mux' : Mux(32,[hooks['imm32'],hooks['rd2']],hooks['alu8rcb'],hooks['alub'])})
    entities.update({'add_br' : Adder(32,hooks['pc8'],hooks['imm32'],hooks['branch'])})
    entities.update({'alu' : Alu(hooks['rd1'],hooks['alub'],hooks['alus'],hooks['aluf'],hooks['aluc'],hooks['aluv'],hooks['alun'],hooks['aluz'])})
    entities.update({'aluflag_join' : BusJoin([hooks['aluc'],hooks['aluv'],hooks['alun'],hooks['aluz']],hooks['aluflag'])})
    entities.update({'aluflag_reg' : Register(4,hooks['clk'],hooks['rst'],hooks['aluflag'],hooks['flag'],enable = hooks['aluflagwr'])})
    entities.update({'flag_subset' : BusSubset(hooks['flag'],[hooks['c'],hooks['v'],hooks['n'],hooks['z']],[(0,1),(1,2),(2,3),(3,4)])})

    entities.update({'datamem' : Memory(hooks['aluf'],hooks['rd2'],hooks['memwr'],hooks['rst'],hooks['clk'],hooks['memrd'])})
    entities.update({'wdb_mux' : Mux(32,[hooks['memrd'],hooks['aluf']],hooks['regsrc'],hooks['wdb'])})
    entities.update({'pcwb_mux' : Mux(32,[hooks['branch'],hooks['pc4'],hooks['wdb']],hooks['pcsrc'],hooks['pcwb'])})

    entities.update({'controller' : ControllerSingleCycle(hooks['instr_31_28'],
                    hooks['instr_27_26'],hooks['instr_25_20'],
                    hooks['instr_15_12'],hooks['instr_4_4'],
                    hooks['c'],hooks['v'],hooks['n'],hooks['z'],
                    hooks['pcsrc'],hooks['pcwr'],hooks['regsa'],
                    hooks['regdst'],hooks['regwrs'],hooks['regwr'],
                    hooks['exts'],hooks['alu8rcb'],hooks['alus'],
                    hooks['aluflagwr'],hooks['memwr'],hooks['regsrc'],
                    hooks['wdbs'])})

    #place memory (Internal) hooks into hook list
    hooks.update({'pc_reg' : entities['pc_reg']})
    hooks.update({'progmem' : entities['progmem']})
    hooks.update({'regfile' : entities['regfile']})
    hooks.update({'aluflag_reg' : entities['aluflag_reg']})
    hooks.update({'datamem' : entities['datamem']})

    # generate simulatable architecture
    arch = Architecture(0.0001,clk,rst,hooks,entities)

    #test inspection message
    msg_inspect = {'inspect' : hooks.keys()}

    while True:
        print('----------------------------------------------------------------')
        print(arch.hook(msg_inspect))
        arch.logic_run()
        time.sleep(0.5)
    """

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
