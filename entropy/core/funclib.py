""" Basic functions library for functions tree """

class FunctionWrapper(object):

    def __init__(self, f):
        self.f = f
        self.argcnt = self.f.func_code.co_argcount
        self.name = self.f.__name__

    def __call__(self, *args, **kwargs):
        return self.f(*args, **kwargs)

def _ident(a):
    # identity function
    return a
ident = FunctionWrapper(_ident)

def _inc(a):
    return a + 1
inc = FunctionWrapper(_inc)

def _dec(a):
    return a - 1
dec = FunctionWrapper(_dec)

def _add(a, b):
    return a + b
add = FunctionWrapper(_add)

def _sub(a, b):
    return a - b
sub = FunctionWrapper(_sub)

def _mul(a, b):
    return a * b
mul = FunctionWrapper(_mul)

def _div(a, b):
    return a / b
div = FunctionWrapper(_div)

def _gt(a, b):
    return a > b
gt = FunctionWrapper(_gt)

def _lt(a, b):
    return a < b
lt = FunctionWrapper(_lt)

def _compare(comparator, pos = 0, neg = 0):
    # this is just a dummy function for comparison, parameters pos and neg are not to pass any value, instead
    # they only needed for _compare to have two possible branches to continue execution whether the result of comparison
    # is positive or negative
    pass
compare = FunctionWrapper(_compare)

def _demul(a):
    # demultiplexing of a value
    return a
demul = FunctionWrapper(_demul)

def _goto(label):
    pass

def _loop(loop_to):
    # label is index of node to loop
    pass
loop = FunctionWrapper(_loop)

def _push(a):
    # push value into stack
    pass
push = FunctionWrapper(_push)

def _pop(popval = 0):
    # pop value from stack (LIFO order) 
    pass
pop = FunctionWrapper(_pop)

