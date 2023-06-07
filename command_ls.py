
command_ls_list = []
command_ls_dictionary = {}


class Command:


    def __init__(self):

        self.__keys = []
        self.topics_blocks = []
        self.topics_resolution = []
        self.description = ''
        self.name = ''
        self.condition = True
        self.fully = False
        self.loyal = False
        self.mandatory = False
        self.regular = False
        command_ls_list.append(self)

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
        command_ls_dictionary[name] = [self]

    def condition(self):
        pass
