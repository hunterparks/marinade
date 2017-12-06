from components.abstract.hooks import InputHook

class Reset(InputHook):

    def __init__(self, name, default_state = 0):
        if not isinstance(name, str) or default_state < 0 or default_state > 1:
            raise ValueError('Initialization parameters invalid')
        self._name = name
        self._state = default_state

    def inspect(self):
        return {'name' : self._name, 'type' : 'reset', 'size' : 1, 'state' : self._state}

    def generate(self, message=None):
        self._state = (self._state + 1) % 2

    def read(self):
        return self._state
