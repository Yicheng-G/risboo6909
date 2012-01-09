""" Generated programm will be represented as tree-hierarchy of functional
    blocks. This class defines an appropriate yet structure for it and simple program evaluator.
"""

from funclib import *

import random
import time
import pickle

verbose = True

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
            if node:
                res = node
            elif len(inp) > 0:
                # substitute value
                res = inp.pop(0)
        if res is None:
            print 'Unexpected error!'
            exit(0)
        return res

    def _eval(self, inp):

        # evaluate if we have any children for this node

        if self.children:
            
            args = []

            if self.func.name == 'compare':

                # special behaviour for comparison

                if self.__evalNext(self.children[0], inp):
                    return self.__evalNext(self.children[1], inp)
                else:
                    return self.__evalNext(self.children[2], inp)
            else:
                for child in self.listChildren():
                    res = self.__evalNext(child, inp)
                    args.append(res)

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

def __prodRandomAlg(funclist, level = 1, maxDepth = 3):
    """ Generate random algorithm with the given depth """
    if level > maxDepth:
        return []
    rndfunc = funclist[random.randint(0, len(funclist) - 1)]
    arglst = []
    for idx in xrange(rndfunc.argcnt):
        arglst.append(__prodRandomAlg(funclist, level + 1, maxDepth))
    node = Node(rndfunc, arglst)
    return node

@timeit
def prodRandomAlg(funclist, maxDepth = 3):
    if verbose:
        print 'Generating algorithm with maxdepth = %d' % maxDepth
    res = __prodRandomAlg(funclist, 1, maxDepth)
    if verbose:
        print 'done!'
    return res

#root = Node(compare, [Node(gt, [Node(inc, [Node(ident)]), Node(inc, [Node(ident)])]), Node(add, [1, 2]), Node(sub, [1, 2])])
root = prodRandomAlg([add, sub, inc, dec, mul, div], 20)
