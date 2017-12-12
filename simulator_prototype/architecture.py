
class Architecture:

    def __init__(self, time_step, clock, reset, hooks, entities):

        self._main_clock = clock
        self._main_reset = reset

        self._hook_dict = hooks
        self._entity_dict = entities

        self._logic_step = 1 / (2 * self._main_clock.frequency())
        self._time_step = time_step



    def hook(self,message):
        ret_val = {}
        if 'inspect' in message:
            h_list = message['inspect']
            for h in h_list:
                ret_val.update({h : self._hook_dict[h].inspect()})
        elif 'modify' in message:
            modify = message['modify']
            name = modify['name']
            self._hook_dict[name].modify(modify['parameters'])
            ret_val.update({name : True})
        elif 'generate' in message:
            generate = message['generate']
            name = generate['name']
            self._hook_dict[name].generate(generate['parameters'])
            ret_val.update({name : True})
        else:
            raise Exception('Message contents invalid')
        return ret_val

    def time_step(self,time):
        for key, value in self._entity_dict.items():
            value.run(time)

    def time_run(self,time=0,steps=1):
        while time < steps * self._time_step:
            self.time_step(time)
            time += self._time_step
        return time

    def logic_run(self,time=0,steps=1):
        while time <  2 * steps * self._logic_step:
            self.time_step(time)
            time += self._logic_step
        return time

    def reset(self):
        self._main_reset.generate()
