import asyncio
import websockets

import single_cycle_poc
import pipeline_poc
from architecture import Architecture

import json

# TODO need an easy way to program the architecture
#      this could be a command that specifies a file and a memory component?

print("Starting Interface")

class Interface:

    def __init__(self):
        self.arch = None
        self.hooks = None
        self.time = 0

    def step(self, msg):
        if not self.arch is None:
            if msg['type'] == 'logic':
                self.time = self.arch.logic_run(self.time,1)
            elif msg['type'] == 'edge':
                self.time = self.arch.edge_run(self.time,1)
            elif msg['type'] == 'time':
                self.time = self.arch.time_run(self.time,1)
            else:
                return {'status': False, 'error': 'simulation type must be valid'}
            print(self.time)
            return {'status': True}
        else:
            return {'status': False, 'error': 'architecture needs to be loaded'}

    def reset(self):
        if not self.arch is None:
            self.arch.reset()
            self.time = 0
            return {'status': True}
        else:
            return {'status': False, 'error': 'architecture needs to be loaded'}

    def load(self, msg):
        retVal = False
        # TODO replace this with a configuration file being loaded in the future
        if msg['filepath'] == 'single_cycle_poc.json':
            self.arch, self.hooks = single_cycle_poc.generate_single_cycle_architecture()
            return {'status': True}
        elif msg['filepath'] == 'pipeline_poc.json':
            self.arch, self.hooks = pipeline_poc.generate_pipeline_architecture()
            return {'status': True}
        else:
            return {'status': False, 'error': 'failed to load file'}

    def unload(self):
        if not self.arch is None:
            self.arch = None
            self.hooks = None
            self.time = 0
        return {'status': True}

    def program(self, msg):
        if not self.arch is None:
            progpath = msg['filepath']
            #TODO handle compilation of code
            #TODO remove test program
            program = [
                0xE3, 0xA0, 0x80, 0x0A,
                0xE2, 0x88, 0x90, 0x01,
                0xE0, 0x09, 0x09, 0x98,
                0xE3, 0xA0, 0xA0, 0x00,
                0xE2, 0x4A, 0xA0, 0x20,
                0xE0, 0x19, 0xA0, 0x0A,
                0x0A, 0x00, 0x00, 0x02,
                0xE3, 0xA0, 0xB0, 0x01,
                0xE3, 0xA0, 0xC0, 0x04,
                0xE5, 0x8C, 0xB0, 0x00,
                0xE5, 0x9C, 0x60, 0x00,
                0xEA, 0xFF, 0xFF, 0xFD
            ]
            #TODO also clear memory
            return self.arch.hook({'modify':{'name':msg['memory'],'parameters':{'start':0,'data':program}}})
        else:
            return {'status': False, 'error': 'architecture needs to be loaded'}

    def handle_component_msg(self, msg):
        if not self.arch is None:
            return self.arch.hook(msg)
        else:
            return {'status': False, 'error': 'architecture needs to be loaded'}


interface = Interface()


async def api_call(websocket, path):
    async for message in websocket:
        msg = json.loads(message)
        print(msg)
        retMsg = {}

        # Architecture Commands

        if 'step' in msg:
            retMsg.update(interface.step(msg['step']))

        if 'reset' in msg:
            retMsg.update(interface.reset())

        if 'load' in msg:
            retMsg.update(interface.load(msg['load']))

        if 'unload' in msg:
            retMsg.update(interface.unload())

        if 'program' in msg:
            retMsg.update(interface.program(msg['program']))

        # Component Commands

        if 'inspect' in msg:
            retMsg.update(interface.handle_component_msg(msg))

        if 'generate' in msg:
            retMsg.update(interface.handle_component_msg(msg))

        if 'modify' in msg:
            retMsg.update(interface.handle_component_msg(msg))

        if 'clear' in msg:
            retMsg.update(interface.handle_component_msg(msg))

        rxStr = json.dumps(retMsg)
        await websocket.send(rxStr)

asyncio.get_event_loop().run_until_complete(websockets.serve(api_call, 'localhost', 4242))
asyncio.get_event_loop().run_forever()
