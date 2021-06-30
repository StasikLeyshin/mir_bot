command_list = []


class Command:
    def __init__(self):
        self.__keys = []
        self.topics_blocks = []
        self.topics_resolution = []
        self.description = ''
        self.condition = True
        command_list.append(self)

    @property
    def keys(self):
        return self.__keys

    @keys.setter
    def keys(self, mas):
        for k in mas:
            self.__keys.append(k.lower())

    def process(self):
        pass

    def condition(self):
        pass
