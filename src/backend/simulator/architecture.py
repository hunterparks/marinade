"""
Architecture object aggregates all simulation components into a set of of
lists as constructed. This object is to be used by the simulator to run the
processor and should be produced by the configuration parser
"""

from collections import OrderedDict, Iterable
from simulator.components.core.clock import Clock
from simulator.components.core.reset import Reset
from simulator.components.abstract.memory_block import MemoryBlock
from simulator.components.abstract.hooks import Hook, InputHook, InternalHook
from simulator.components.abstract.configuration_parser import ConfigurationParser

import simulator.package_manager as package_manager


class Architecture(ConfigurationParser):
    """
    Architecture simplifies the structure of the processor during runtime
    to an ordered list of runnable entities (including clocks) and a list
    of hooks to pass frontend messages to.
    """

    def __init__(self, time_step, clock, reset, memory, hooks, entities):
        "Constructor will check for valid parameters, exception thrown on invalid"

        # set system necessary components
        if not isinstance(clock, Clock):
            raise TypeError('Clock component is enforced as a Clock')
        elif not isinstance(reset, Reset):
            raise TypeError('Reset component is enforced as a Reset')
        elif not isinstance(memory, MemoryBlock) and memory != None:
            raise TypeError('Memory component is enfored as a MemoryBlock')

        self._main_clock = clock
        self._main_reset = reset
        self._main_memory = memory

        # set dictionary references
        if not isinstance(hooks, OrderedDict):
            raise TypeError('Hooks must be an ordered dictionary for search')
        if not isinstance(entities, OrderedDict):
            raise TypeError('Entites must be an ordered dictionary for search')

        self._hook_dict = hooks
        self._entity_dict = entities

        # set time steps
        self._logic_step = 1 / (2 * self._main_clock.frequency())

        if time_step <= 0:
            raise ValueError('Time step must be greater than zero')
        elif time_step > self._logic_step:
            raise ValueError('Time step must satisfy Nyquist criteria for main clock')

        self._time_step = time_step

    def inspect(self, message):
        "Returns object's messages from hook call"
        ret_val = {}
        if isinstance(message, Iterable) and not isinstance(message, str):
            for h in message:
                try:
                    if isinstance(self._hook_dict[h], Hook):
                        rmsg = self._hook_dict[h].inspect()
                        ret_val.update({h: rmsg})
                    else:
                        ret_val.update({h: {'error': 'hook is not of valid type'}})
                except KeyError:
                    ret_val.update({h: {'error': 'hook not in architecture'}})
        else:
            ret_val.update({'architecture-hooks-inspect': {'error': 'invalid message format'}})
        return ret_val

    def modify(self, message):
        "Returns object's messages from hook call"
        # parameter check
        if not isinstance(message, dict):
            return {'architecture-modify': {'error': 'invalid message type'}}

        ret_val = {}
        try:
            name = message['name']
        except KeyError:
            ret_val.update({'architecture-hooks-modify': {'error': 'invalid message format'}})
            return ret_val
        try:
            if isinstance(self._hook_dict[name], InternalHook):
                rmsg = self._hook_dict[name].modify(message['parameters'])
                ret_val.update({name: rmsg})
            else:
                ret_val.update({name: {'error': 'hook is not of valid type'}})
        except KeyError:
            ret_val.update({name: {'error': 'hook not in architecture'}})
        return ret_val

    def generate(self, message):
        "Returns object's messages from hook call"
        # parameter check
        if not isinstance(message, dict):
            return {'architecture-modify': {'error': 'invalid message type'}}

        ret_val = {}
        try:
            name = message['name']
        except KeyError:
            ret_val.update({'architecture-hooks-generate': {'error': 'invalid message format'}})
            return ret_val
        try:
            if isinstance(self._hook_dict[name], InputHook):
                rmsg = self._hook_dict[name].generate(message['parameters'])
                ret_val.update({name: rmsg})
            else:
                ret_val.update({name: {'error': 'hook is not of valid type'}})
        except KeyError:
            ret_val.update({name: {'error': 'hook not in architecture'}})
        return ret_val

    def clear(self, message):
        "Returns object's messages from hook call"
        ret_val = {}
        if isinstance(message, Iterable) and not isinstance(message, str):
            for h in message:
                try:
                    if isinstance(self._hook_dict[h], InternalHook):
                        rmsg = self._hook_dict[h].clear()
                        ret_val.update({h: rmsg})
                    else:
                        ret_val.update({h: {'error': 'hook is not of valid type'}})
                except KeyError:
                    ret_val.update({h: {'error': 'hook not in architecture'}})
        else:
            ret_val.update({'architecture-hooks-clear': {'error': 'invalid message format'}})
        return ret_val

    def hook(self, message):
        "Returns object's messages from hook call"
        # parameter check
        if not isinstance(message, dict):
            return {'architecture-hooks': {'error': 'invalid message type'}}

        # match to message type
        ret_val = {}
        if 'inspect' in message:
            ret_val = self.inspect(message['inspect'])
        elif 'modify' in message:
            ret_val = self.modify(message['modify'])
        elif 'generate' in message:
            ret_val = self.generate(message['generate'])
        elif 'clear' in message:
            ret_val = self.clear(message['clear'])
        else:
            ret_val.update({'architecture-hooks': {'error': 'invalid message format'}})
        return ret_val

    def time_step(self, time):
        "Computes architecture at time specified"
        for key, value in self._entity_dict.items():
            value.run(time)

    def time_run(self, time=0, steps=1):
        "Runs a timing simulation"
        t = 0
        while t < steps * self._time_step:
            self.time_step(time + t)
            t += self._time_step
        return time + t

    def edge_run(self, time=0, steps=1):
        "Run simulation to next clock edge (1/2 of logic run)"
        t = 0
        while t < steps * self._logic_step:
            self.time_step(time + t)
            t += self._logic_step
        return time + t

    def logic_run(self, time=0, steps=1):
        "Runs a logic simulation or one full clock cycle"
        t = 0
        while t < 2 * steps * self._logic_step:
            self.time_step(time + t)
            t += self._logic_step
        return time + t

    def reset(self):
        "Toggles the main reset to active state, runs a logic step"
        self._main_reset.generate({'reset': True})
        self.logic_run()
        self._main_reset.generate({'reset': False})

    def get_hooks(self):
        "Gets the list of hooks in architecture"
        return self._hook_dict

    def get_entities(self):
        "Get the list of entities in architecture"
        return self._entity_dict

    @classmethod
    def from_dict(cls, config, hooks=None):
        "Implements conversion from configuration to component"

        # TODO clean this code up

        # import packages from file
        package_manager.set_default_packages(config["packages"])

        # iterate through signals to produce hooks
        if hooks == None:
            hooks = OrderedDict()
        for signal in config["signals"]:
            if "package" in signal:
                package = signal["package"]
            else:
                package = None
            hooks.update({signal["name"]: package_manager.construct(
                signal["type"], signal, package, hooks)})

        # iterate through entities to produce entities
        entities = OrderedDict()
        for entity in config["entities"]:
            if "package" in signal:
                package = signal["package"]
            else:
                package = None

            if "signal" in entity:
                entities.update({entity["name"]: hooks[entity["signal"]]})
            else:
                entities.update({entity["name"]: package_manager.construct(
                    entity["type"], entity, package, hooks)})

        # gather system wide defintions
        system_clock = config["system_clock"]
        if system_clock != None:
            system_clock = hooks[system_clock]

        system_reset = config["system_reset"]
        if system_reset != None:
            system_reset = hooks[system_reset]

        system_memory = config["system_memory"]
        if system_memory != None:
            system_memory = hooks[system_memory]

        time_step = config["time_step"]

        return Architecture(time_step, system_clock, system_reset, system_memory,
                            hooks, entities)
