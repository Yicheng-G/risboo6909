""" Generated programm will be represented as tree-hierarchy of functional
    blocks. This class defines an appropriate yet structure for it and simple program evaluator.
"""

from funclib import *

import random
import time
import pickle

verbose = False 

program_stack = []

def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        if verbose:
            print '%r %2.2f sec' % \
                  (method.__name__, te-ts)
        return result

    return timed

class UnexpectedEvalError(Exception):

    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return repr(self.parameter)

class Node(object):

    def __init__(self, f, values = []):

        self.children = []
        self.setFunc(f)

        if values:
            for node in values:
                if type(node) is Node:
                    self.children.append(node)
                else:
                    # we have a leaf node
                    self.children.append(node)
        else:
            self.children = [[]] * self.func.argcnt

    def listChildren(self):
        for item in self.children:
            yield item

    def setFunc(self, f):
        self.func = f

    def getFunc(self):
        return self.func

    def rmChild(self, child):
        if type(child) is Node:
            if child in self.children:
                self.children.remove(child)
        if type(child) is int:
            if child < len(self.children):
                del self.children[child]

    def __evalNext(self, node, inp):
        res = None
        if type(node) is Node:
            res = node._eval(inp)
        else:
            if node is not None:
                res = node
            elif len(inp) > 0:
                # substitute value
                res = inp.pop(0)
        if res is None:
            if verbose:
                print 'Unexpected error!'
            raise UnexpectedEvalError()
        return res

    def _eval(self, inp):
        # evaluate if we have any children for this node
        if self.children:

            args = []

            if self.func.name == '_compare':
                # special behaviour for comparison
                if self.__evalNext(self.children[0], inp):
                    return self.__evalNext(self.children[1], inp)
                else:
                    return self.__evalNext(self.children[2], inp)

            else:

                for child in self.listChildren():
                    res = self.__evalNext(child, inp)
                    args.append(res)

            if self.func.name == '_push':
                self.__evalNext(self.children[0], inp)
                program_stack.append(*args)
                return args

            elif self.func.name == '_pop':
                if program_stack:
                    return program_stack.pop(len(program_stack) - 1)
                else:
                    return 0

                return self.func(*args)
        else:
            return None 

    def toString(self, depth = 1):
        tmp = []
        tmp.append('%s\n' % self.func.name)
        for child in self.children:
            if hasattr(child, 'toString'):
                tmp.append((' ' * depth) + '%s' % child.toString(depth + 1))
            else:   
                tmp.append((' ' * depth) + '%s\n' % child)
        return ''.join(tmp)

    def __str__(self):
        return self.toString()

def save(root, filename = "default.dat"):
    """ Serialize algorithm starting from any node """
    if verbose:
        print 'Saving to %s' % filename
    f = open(filename, 'wb')
    pickle.dump(root, f, 0)
    f.close()
    if verbose:
        print 'done!'

def load(filename = "default.dat"):
    if verbose:
        print 'Loading from %s' % filename
    f = open(filename, 'rb', 0)
    root = pickle.load(f)
    f.close()
    if verbose:
        print 'done!'
    return root 

def traverse(cur_node):
    Q = [cur_node]
    while Q:
        cur_node = Q.pop(0)
        yield(cur_node)
        if type(cur_node) is Node and cur_node.children:
            tmp = [child for child in cur_node.listChildren()]
            Q.extend(tmp)

def __prodRandomAlg(funclist, inputs, level, maxDepth):
    """ Generate random algorithm with the given depth """
    if level > maxDepth:
        if not random.randint(0, 1):
            return random.uniform(0, 1)
        inputs[0] += 1
        return []
    rndfunc = funclist[random.randint(0, len(funclist) - 1)]
    arglst = []
    for idx in xrange(rndfunc.argcnt):
        arglst.append(__prodRandomAlg(funclist, inputs, level + 1, maxDepth))
    node = Node(rndfunc, arglst)
    return node

#@timeit
def prodRandomAlg(funclist, maxDepth = 3):
    if verbose:
        print 'Generating algorithm with maxdepth = %d' % maxDepth
    random.seed()
    inputs = [0]
    res  = __prodRandomAlg(funclist, inputs, 1, maxDepth)
    if verbose:
        print 'done!'
    return res, inputs[0]

#root = Node(pop, [Node(push, [10])])
#root = Node(compare, [Node(gt, [Node(inc, [Node(ident)]), Node(inc, [Node(ident)])]), Node(add, [1, 2]), Node(sub, [1, 2])])
root, inputs = prodRandomAlg([add, sub, inc, dec, mul, div, compare, push, pop], 4)
#save(root, 'algtest')
#root  = load('pop1.dat')
print root
#print root._eval([])

