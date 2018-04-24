"""
Architecture object aggregates all simulation components into a set of of
lists as constructed. This object is to be used by the simulator to run the
processor and should be produced by the configuration parser

Configuration file should follow form

{
    "packages" : [],
    "system_clock" : null,
    "system_reset" : null,
    "system_memory" : null,
    "time_step" : 1,

    "signals" : [],
    "entities" : []
}

packages is the list of default packages to search in for a given component type
    additionally, each component can specify a package key that allows for
    redirection to desired component

system_clock is a reference to the main clock of the architecture
    the frequency of this clock is used to determine the edge and logic step
    size. Also used to verify that the time_step value is valid

system_reset is a reference to the main reset for the architecture
    this signal is enforced by special handlers to quickly clear the architecture

system_memory is a reference to the memory component that is to be programmed
    this signal may be null

time_step is the timing simulation step size, must meet Nyquist criteria for
    the system_clock

signals is a list of bus components
    the component is constructed accoriding to the definition in the package
    manager

entities is a list of runable components
    if a component has key signal then it is interpretted as a signal that needs
        to be appended to the entity list
    if a component has key symbolic then it is interpretted as being a
        non-runnable container with a set of sub entities
    else a component is regarded as concrete and is constructed according to
        the definition in the package manager
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
        """
        Implements conversion from configuration to component

        config is dictionary following architecture standard template
        hooks is optional list of signal objects to start architecture

        Returns an architecture object with components
        """

        # import packages from file
        package_manager.set_default_packages(config["packages"])

        # iterate through signals to produce hooks
        hooks = cls._parse_signals(config, hooks)

        # iterate through entities to produce entities
        entities = cls._parse_entities(config, hooks)

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

    @classmethod
    def _parse_signals(cls, config, hooks):
        """
        Parse a list of components (signals) from configuration object.

        Configuration signals must be a list of signals where each one follows
        the configuration template for the given type

        config is reference to dictionary with entities for configuration
        hooks is dictionary containing signals to link components (or None)

        returns a an ordered dictionary of updated hooks
        """
        if hooks == None:
            hooks = OrderedDict()
        for signal in config["signals"]:
            if "package" in signal:
                package = signal["package"]
            else:
                package = None

            hooks.update({signal["name"]: package_manager.construct(
                signal["type"], signal, package, hooks)})
        return hooks

    @classmethod
    def _parse_entities(cls, config, hooks):
        """
        Parse a list of components (entities) from configuration object.

        Configuration entities may take several forms

            if the entity is a signal then an insert of hook is made into
                entities list
            else if the entity is a symbolic then the component is treated as a
                container for another list of entities
            else the entity is concrete and is constructed after searching the
                package tree

        Additional options

            if package is supplied then the component will be searched only in
                that list (of strings)
            if append_to_signals is supplied then component is also added as a
                hook

        config is reference to dictionary with entities for configuration
        hooks is dictionary containing signals to link components

        returns a an ordered dictionary of entities
        """
        entities = OrderedDict()
        for entity in config["entities"]:
            if "package" in entity:
                package = entity["package"]
            else:
                package = None

            if "signal" in entity:
                entities.update({entity["name"]: hooks[entity["signal"]]})
            elif "symbolic" in entity and entity["symbolic"]:
                if "entities" in entity:
                    entities.update(cls._parse_entities(entity, hooks))
            else:
                entities.update({entity["name"]: package_manager.construct(
                    entity["type"], entity, package, hooks)})
                if "append_to_signals" in entity and entity["append_to_signals"]:
                    hooks.update({entity["name"]: entities[entity["name"]]})
        return entities
