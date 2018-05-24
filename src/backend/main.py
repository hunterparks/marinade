"""
Front-end interface API.
When ran it creates a websocket server on localhost port 4242. This websocket
feeds messages to the interface. Interface API is defined as JSON.

API Documentation:

Note that timing simulation is used when in simulation view and logic simulation
used when in memory view mode. Distinction is made since step either moves a
timestep or a clockstep.

### Architecture Commands
{'assemble':{'filepath':<'file'>}} Returns {'status':{}, "errors":{}}
{'step':{'type':<'logic','edge','time'>}} Returns {'status':{}}
{'reset':{}} Returns {'status':{}}
{'load':{'filepath':<'file'>}}  Returns {'status':{}}
{'unload':{}} Returns {'status':{}}
{'program':{'filepath':<'file'>,'memory':<'hook name'>}}

### Component Commands

>>ALL
{'inspect':[<'component>']}  Returns [{'component':{<component data>}}]

>>INPUT_HOOKS (Clock, Reset, InputBus, ...)
{'generate':{'name':<'component'>,'parameters':{<component data>}}} Returns {'status':{}}

>>INTERNAL_HOOKS (Memory)
{'modify':{'name':<'component'>,'parameters':{<component data>}}} Returns {'status':{}}
{'clear':[<'components>']} Returns {'status':{}}

## More detailed component hook examples
{
    “inspect” : [ <hook names> ]
}
{
    “modify” : {
        “name” : <hook name (must be of type InternalHook)>,
        “parameters” : {
            “state” : <specific to Register not used in larger memories>
            “start” : <starting address for Memory and RegisterFile >,
            “data” : [ < contents for Memory and RegisterFile >],
        }
    }
}
{
    “generate” : {
        “name” : <hook name (must be of type InputHook)>,
        “parameters” : {
            “state” : <Input bus state as integer>
            “frequency” : <specific to Clock object>,
            “reset” : <specific to Reset object>,
        }
    }
}

"""

import json
import asyncio
import websockets
import struct
import traceback
import subprocess
from sys import platform

#from sentry.sentry import initialize_sentry

from simulator.architecture import Architecture


HOST_NAME = 'localhost'
HOST_PORT = 4242


class Interface:
    """
    Interface API, responsible for mapping API calls to simulator architecture.
    """

    def __init__(self):
        """
        Constructor will default to no architecture set.
        """
        self.arch = None
        self.hooks = None
        self.time = 0

    def parse_command(self, msg):
        """
        Maps JSON command to simulator functionality.

        Param: msg is a dictionary parsed from JSON. Must be formated as
        documented.
        Returns: results from running commands passed in as dictionary
        """
        retMsg = {}

        # Architecture Commands
        if 'step' in msg:
            retMsg.update(self.step(msg['step']))
        if 'reset' in msg:
            retMsg.update(self.reset())
        if 'load' in msg:
            retMsg.update(self.load(msg['load']))
        if 'unload' in msg:
            retMsg.update(self.unload())
        if 'program' in msg:
            retMsg.update(self.program(msg['program']))
        if 'assemble' in msg:
            retMsg.update(self.assemble(msg['assemble']))

        # Component Commands
        if 'inspect' in msg:
            retMsg.update(self.handle_component_msg(msg))
        if 'generate' in msg:
            retMsg.update(self.handle_component_msg(msg))
        if 'modify' in msg:
            retMsg.update(self.handle_component_msg(msg))
        if 'clear' in msg:
            retMsg.update(self.handle_component_msg(msg))

        return retMsg

    def assemble(self, msg):
        """
        Calls either a bash script or a batch script that converts assembly
        code into machine code.
        Return: Dictionary containing results of the assembler.
        """
        try:
            f = open(msg['filepath'])
            if platform == "linux" or platform == "linux2" or platform == "darwin":
                output = subprocess.run(["./dist/backend/assembler/nix_assembler.sh", msg['filepath']], stderr=subprocess.PIPE)
                f.close()
                return {'status': True, 'errors': output.stderr.decode('utf-8')}
            elif platform == "win32":
                output = subprocess.run([r".dist\backend\assembler\windows_assembler.bat", msg['filepath']], stderr=subprocess.PIPE)
                f.close()
                return {'status': True, 'errors': output.stderr.decode('utf-8')}
        except KeyError as e:
            traceback.print_exc()
            return {'status': False, 'error': 'invalid key : {}'.format(str(e))}
        except Exception as e:
            traceback.print_exc()
            return {'status': False, 'error': 'exception : {}'.format(str(e))}


    def step(self, msg):
        """
        Steps the architecture through either a logic, edge, or time simulation.
        Param: msg constains details regarding simulation type.
        Return: dictionary containing results of simulation.
        """
        try:
            if not self.arch is None:
                if msg['type'] == 'logic':
                    self.time = self.arch.logic_run(self.time, 1)
                elif msg['type'] == 'edge':
                    self.time = self.arch.edge_run(self.time, 1)
                elif msg['type'] == 'time':
                    self.time = self.arch.time_run(self.time, 1)
                else:
                    return {'status': False, 'error': 'simulation type must be valid'}
                return {'status': True}
            else:
                return {'status': False, 'error': 'architecture needs to be loaded'}
        except KeyError:
            return {'status': False, 'error': 'step requires a type key'}

    def reset(self):
        """
        Resets the architecture back to default state. Used the configuration
        files defined reset line. Resulting behavior in architecture dependent
        on configuration file.
        Retuns status of command as dictionary.
        """
        if not self.arch is None:
            self.arch.reset()
            self.time = 0
            return {'status': True}
        else:
            return {'status': False, 'error': 'architecture needs to be loaded'}

    def load(self, msg):
        """
        Loads the an architecture from a configuration file.
        Param: msg is dictionary with a filepath specified to config file
        Return: dictionary noting resulting state of operation.
        """
        try:
            f = open(msg['filepath'])
            config = json.loads(f.read())
            self.arch = Architecture.from_dict(config)
            self.hooks = self.arch.get_hooks()
            f.close()
        except KeyError as e:
            traceback.print_exc()
            return {'status': False, 'error': 'invalid key : {}'.format(str(e))}
        except Exception as e:
            traceback.print_exc()
            return {'status': False, 'error': 'exception : {}'.format(str(e))}
        return {'status': True}

    def unload(self):
        """
        Clears the current architecture, must load a new architecture before
        further use.
        """
        if not self.arch is None:
            self.arch = None
            self.hooks = None
            self.time = 0
        return {'status': True}

    def program(self, msg):
        """
        Programs the given architecture using a targeted binary file.
        Param: msg is dictionary with a filepath to program file and the memory
               hook name to store file into.
        Returns resulting status of loading file as dictionary
        """
        if not self.arch is None:
            progpath = msg['filepath']
            binary_file = open(progpath, mode='rb')
            machine_code = binary_file.read()
            program = list(struct.unpack('B' * len(machine_code), machine_code))
            binary_file.close()
            self.arch.hook({'clear': [msg['memory']]})
            return self.arch.hook({'modify': {'name': msg['memory'], 'parameters': {'start': 0, 'data': program}}})
        else:
            return {'status': False, 'error': 'architecture needs to be loaded'}

    def handle_component_msg(self, msg):
        """
        Routes component API messages to the architecture.
        Param: msg contains the message to route toward architecture.
        Return dictionary with result status from component API call.
        """
        if not self.arch is None:
            return self.arch.hook(msg)
        else:
            return {'status': False, 'error': 'architecture needs to be loaded'}


if __name__ == "__main__":

    client = initialize_sentry()

    try:

        interface = Interface()

        async def api_call(websocket, path):
            async for message in websocket:
                try:
                    msg = json.loads(message.replace("\\", "/"))
                    retMsg = interface.parse_command(msg)
                    rxStr = json.dumps(retMsg)
                    await websocket.send(rxStr)
                except Exception:
                    await websocket.send(json.dumps({'status' : False, 'error' : 'cannot parse JSON message'}))

        asyncio.get_event_loop().run_until_complete(
            websockets.serve(api_call, HOST_NAME, HOST_PORT))
        asyncio.get_event_loop().run_forever()

    except Exception:
        client.captureException()
