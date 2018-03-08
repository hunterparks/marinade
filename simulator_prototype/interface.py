import asyncio
import websockets

import single_cycle_poc
from architecture import Architecture

import json

# TODO need an easy way to program the architecture
#      this could be a command that specifies a file and a memory component?


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
            program = []
            #TODO handle compilation of code
            return arch.hook({'modify':{'name':msg['memory'],'parameters':{'start':0,'data':program}}})
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
