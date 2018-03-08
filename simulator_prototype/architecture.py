"""
Architecture object aggregates all simulation components into a set of of
lists as constructed. This object is to be used by the simulator to run the
processor and should be produced by the configuration parser
"""

from components.core.clock import Clock
from components.core.reset import Reset


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
        ret_val = {}
        if 'inspect' in message:
            h_list = message['inspect']
            for h in h_list:
                ret_val.update({h: self._hook_dict[h].inspect()})
        elif 'modify' in message:
            modify = message['modify']
            name = modify['name']
            self._hook_dict[name].modify(modify['parameters'])
            ret_val.update({name: True})
        elif 'generate' in message:
            generate = message['generate']
            name = generate['name']
            self._hook_dict[name].generate(generate['parameters'])
            ret_val.update({name: True})
        else:
            raise Exception('Message contents invalid')
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
