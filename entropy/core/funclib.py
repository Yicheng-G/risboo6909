""" Basic functions library for functions tree """

class FunctionWrapper(object):

    def __init__(self, f):
        self.f = f
        self.argcnt = self.f.func_code.co_argcount
        self.name = self.f.__name__

    def __call__(self, *args, **kwargs):
        return self.f(*args, **kwargs)

@FunctionWrapper
def ident(a):
    # identity function
    return a

@FunctionWrapper
def inc(a):
    return a + 1

@FunctionWrapper
def dec(a):
    return a - 1

@FunctionWrapper
def add(a, b):
    return a + b

@FunctionWrapper
def sub(a, b):
    return a - b

@FunctionWrapper
def mul(a, b):
    return a * b

@FunctionWrapper
def div(a, b):
    return a / b

@FunctionWrapper
def gt(a, b):
    return a > b

@FunctionWrapper
def lt(a, b):
    return a < b

@FunctionWrapper
def compare(comparator, pos = 0, neg = 0):
    pass

