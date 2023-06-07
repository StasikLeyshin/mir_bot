
from functools import wraps

command_list = []
command_bs_dictionary = {}


class Command:
    def __init__(self, __keys=None, topics_blocks=None, topics_resolution=None, description='', name='', condition=True,
                 fully=False, mandatory=False, score=0):
        if topics_resolution is None:
            topics_resolution = []
        if topics_blocks is None:
            topics_blocks = []
        if __keys is None:
            __keys = []
        self.__keys = __keys
        self.topics_blocks = topics_blocks
        self.topics_resolution = topics_resolution
        self.description = description
        self.name = name
        self.condition = condition
        self.fully = fully
        self.mandatory = mandatory
        self.score = score
        self.regular = False
        self.loyal = False
        command_list.append(self)

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # print(f'Спим {self._delay} сек.')
            # sleep(self._delay)
            val = func(*args, **kwargs)
            return val

        return wrapper

    @property
    def keys(self):
        return self.__keys

    @keys.setter
    def keys(self, mas):
        for k in mas:
            self.__keys.append(k.lower())

    def process(self):
        pass

    def set_dictionary(self, name):
        self.name = name
        command_bs_dictionary[name] = [self]

    def condition(self):
        pass
