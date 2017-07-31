###########################################################
# Interpreter Memory System
###########################################################

class MemorySpace:
    def __init__(self, name):
        self.name = name   # mainly for debugging purposes
        self.symval = {}   # (symbol, value) pairs

    def __str__(self):
        return ('Memory Space of \'{name}\':\n    {symval}'.format(
            name = self.name,
            symval = self.symval))

    def enter(self, id, value):
        self.symval[id] = value

    def update(self, id, value):
        self.symval[id] = value

    def retrieve(self, id):
        return self.symval.get(id, None)

###########################################################
# Top-level script tests
###########################################################
if __name__ == '__main__':
    space = MemorySpace('main')
    space.enter('a', 3)
    space.enter('b', 4)
    print(space)
    print(space.retrieve('b'))
    print(space.retrieve('c'))
