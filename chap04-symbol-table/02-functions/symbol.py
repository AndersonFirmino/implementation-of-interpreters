###########################################################
# Symbol Table and Symbol Scope Implementation
###########################################################

###########################################################
# Scope
###########################################################
class Scope:
    def __init__(self, parentScope = None):
        self.parentScope = parentScope # None if global (outermost) scope
        self.symbols = {}              # symbols of this scope

    def resolve(self, name):
        '''
        Find a symbol in the current scope or its upstream scopes.
        '''
        sym = self.symbols.get(name)
        if sym is None and self.parentScope is not None:
            return self.parentScope.resolve(name)
        return sym

    def define(self, name):
        '''
        Define a symbol in the current scope.
        '''
        self.symbols[name] = Symbol(name, self)

###########################################################
# Symbol
###########################################################
class Symbol:
    def __init__(self, name, scope):
        self.name = name
        self.scope = scope  # the scope that contains it

###########################################################
# FunctionScope -- Contains an ordered dictionary of parameters
###########################################################
from collections import OrderedDict
class FunctionScope(Scope):
    def __init__(self, name, parentScope):
        self.name = name
        self.parentScope = parentScope
        self.symbols = OrderedDict()     # parameters

###########################################################
# Top-level script tests
###########################################################
if __name__ == '__main__':
    '''
    Building scope tree for lua code:
    length = 4
    width = 5

    function area(width, length)
        return width * length
    end
    s = area(width, length)
    '''

    globals = Scope()
    globals.define('width')
    globals.define('length')
    globals.define('area')

    funcscope = FunctionScope('area', globals)
    funcscope.define('width')
    funcscope.define('length')

    globals.define('s')

    print(globals.symbols.keys())
    print(funcscope.symbols.keys())
