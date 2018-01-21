"""
Architecture object aggregates all simulation components into a set of of
lists as constructed. This object is to be used by the simulator to run the
processor and should be produced by the configuration parser
"""

# TODO break hook apart into seperate functions

from collections import OrderedDict, Iterable

from components.core.clock import Clock
from components.core.reset import Reset

from components.abstract.hooks import Hook, InputHook, InternalHook


class Architecture:
    """
    Architecture simplifies the structure of the processor during runtime
    to an ordered list of runnable entities (including clocks) and a list
    of hooks to pass frontend messages to.
    """

    def __init__(self, time_step, clock, reset, hooks, entities):
        "Constructor will check for valid parameters, exception thrown on invalid"

        # set system necessary components
        if not isinstance(clock, Clock):
            raise TypeError('Clock component is enforced as a clock')
        elif not isinstance(reset, Reset):
            raise TypeError('Reset component is enforced as a reset')

        self._main_clock = clock
        self._main_reset = reset

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

    def hook(self, message):
        "Returns objects messages from hook call"
        # parameter check
        if not isinstance(message, dict):
            return {'architecture-hooks': {'error': 'invalid message type'}}

        # match to message type
        ret_val = {}
        if 'inspect' in message:
            h_list = message['inspect']
            if isinstance(h_list, Iterable) and not isinstance(h_list, str):
                for h in h_list:
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

        elif 'modify' in message:
            modify = message['modify']
            try:
                name = modify['name']
            except KeyError:
                ret_val.update({'architecture-hooks-modify': {'error': 'invalid message format'}})
                return ret_val
            try:
                if isinstance(self._hook_dict[name], InternalHook):
                    rmsg = self._hook_dict[name].modify(modify['parameters'])
                    ret_val.update({name: rmsg})
                else:
                    ret_val.update({name: {'error': 'hook is not of valid type'}})
            except KeyError:
                ret_val.update({name: {'error': 'hook not in architecture'}})

        elif 'generate' in message:
            generate = message['generate']
            try:
                name = generate['name']
            except KeyError:
                ret_val.update({'architecture-hooks-generate': {'error': 'invalid message format'}})
                return ret_val
            try:
                if isinstance(self._hook_dict[name], InputHook):
                    rmsg = self._hook_dict[name].generate(generate['parameters'])
                    ret_val.update({name: rmsg})
                else:
                    ret_val.update({name: {'error': 'hook is not of valid type'}})
            except KeyError:
                ret_val.update({name: {'error': 'hook not in architecture'}})

        else:
            ret_val.update({'architecture-hooks': {'error': 'invalid message format'}})
        return ret_val

    def time_step(self, time):
        "Computes architecture at time specified"
        for key, value in self._entity_dict.items():
            value.run(time)

    def time_run(self, time=0, steps=1):
        "Runs a timing simulation"
        t = time
        while t < (steps * self._time_step + time):
            self.time_step(t)
            t += self._time_step
        return t

    def logic_run(self, time=0, steps=1):
        "Runs a logic simulation or one full clock cycle"
        t = time
        while t < (2 * steps * self._logic_step + time):
            self.time_step(t)
            t += self._logic_step
        return t

    def reset(self):
        "Toggles the main reset to active state, runs a logic step"
        self._main_reset.generate({'reset': True})
        self.logic_run()
        self._main_reset.generate({'reset': False})
