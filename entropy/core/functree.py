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
        self.node_id = -1

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
            raise UnexpectedEvalError('Unexpected error!')
        return res

    def _eval(self, inp = []):
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
        tmp.append('%d: %s\n' % (self.node_id, self.func.name))
        for child in self.children:
            if hasattr(child, 'toString'):
                tmp.append((' ' * depth) + '%s' % child.toString(depth + 1))
            else:   
                tmp.append((' ' * depth) + '%s\n' % child)
        return ''.join(tmp)

    def __str__(self):
        return self.toString()

class Tree(object):

    def __init__(self, root):
        self.cur_id = 0
        self.min_id, self.max_id =  999999999, -1
        self.root = root
        self.enum(set())

    def enum(self, visited):
        # assign an uniqueue ID to each node
        ids, tmp_id = set(), 0
        conflict = False

        for node in self.traverse():
            if type(node) is Node and node.node_id == -1:
                node.node_id, tmp_id = self.cur_id, self.cur_id
                self.cur_id += 1
                visited.add(node)
            elif type(node) is Node and node.node_id != -1 and node not in visited:
                if node.node_id not in ids:
                    ids.add(node.node_id)
                    if node.node_id > self.cur_id:
                        self.cur_id, tmp_id = node.node_id, self.cur_id
                    visited.add(node)
                else:
                    # conflict found, mark this node as -1 
                    node.node_id = -1
                    conflict = True

            if self.min_id > tmp_id:
                self.min_id = tmp_id
            if self.max_id < tmp_id:
                self.max_id = tmp_id

        if conflict:
            # resolve conflicts
            self.enum(visited)

    def _eval(self, inp = []):
        return self.root._eval(inp)

    def getMinMaxId(self):
        return self.min_id, self.max_id

    def getRoot(self):
        return self.root

    def save(self, filename = "default.dat"):
        """ Serialize algorithm starting from any node """
        if verbose:
            print 'Saving to %s' % filename
        f = open(filename, 'wb')
        pickle.dump(self.root, f, 0)
        f.close()
        if verbose:
            print 'done!'

    @staticmethod
    def load(filename = "default.dat"):
        if verbose:
            print 'Loading from %s' % filename
        f = open(filename, 'rb', 0)
        root = pickle.load(f)
        f.close()
        if verbose:
            print 'done!'
        self.root = root
        return self.root

    def traverse(self, cur_node = None):
        """ Non-recursive tree traversal """
        if cur_node is None:
            cur_node = self.root

        Q = [cur_node]
        while Q:
            cur_node = Q.pop(0)
            yield(cur_node)
            if type(cur_node) is Node and cur_node.children:
                tmp = [child for child in cur_node.listChildren()]
                Q.extend(tmp)

    def __str__(self):
        return str(self.root)


def __prodRandomAlgDesc(funclist, inputs, level, maxDepth):
    """ Generate random algorithm with the given depth (from TOP to BOTTOM) """

    if level > maxDepth:
        if not random.randint(0, 1):
            return random.uniform(0, 1)
        inputs[0] += 1
        return []

    rndfunc = funclist[random.randint(0, len(funclist) - 1)]
    arglst, nextNode = [], None

    for idx in xrange(rndfunc.argcnt):
        if nextNode is None:
            res = __prodRandomAlgDesc(funclist, inputs, level + 1, maxDepth)
            if type(res) is Node and res.func.name == '_demul':
                # if next node is _demul, connect all inputs of current node with that node
                nextNode = res
        else:
            res = nextNode
        arglst.append(res)

    return Node(rndfunc, arglst)

#@timeit
def prodRandomAlg(funclist, maxDepth = 3):
    if verbose:
        print 'Generating algorithm with maxdepth = %d' % maxDepth
    random.seed()
    inputs = [0]
    res  = __prodRandomAlgDesc(funclist, inputs, 1, maxDepth)
    if verbose:
        print 'done!'
    return Tree(res), inputs[0]

#root = Tree(Node(compare, [Node(gt, [Node(inc, [Node(ident)]), Node(inc, [Node(ident)])]), Node(add, [1, 2]), Node(sub, [1, 2])]))
#d = Node(demul, [2])
#root = Tree(Node(add, [d, d]))
#root, inputs = prodRandomAlg([add, sub, inc, dec, mul, div, compare, push, pop, demul], 4)
#root.save('algtest')
#root  = load('pop1.dat')
#print root
#print root.getMinMaxId()
#print root._eval([2, 1])

