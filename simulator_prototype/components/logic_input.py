from components.abstract.hooks import InputHook

class LogicInput(InputHook):

    def __init__(self, name, size, default_state = 0):
        if not isinstance(name, str) or size <= 0 or default_state < 0 or default_state > 2**size:
            raise ValueError('Initialization parameters invalid')
        self._name = name
        self._size = size
        self._state = default_state

    def inspect(self):
        return {'name' : self._name, 'type' : 'logic', 'size' : 1, 'state' : self._state}

    def generate(self, message):
        if message is not None:
            if 'state' in message:
                if isinstance(message['state'],int) and message['state'] >= 0 and message['state'] < 2**self._size:
                    self._state = message['state']
                else:
                    raise ValueError('Data in message does not match expected range')
            else:
                raise ValueError('Invalid format for message')
        else:
            raise ValueError('Expecting message to be provided')

    def read(self):
        return self._state
