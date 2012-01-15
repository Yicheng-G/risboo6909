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

    def __evalNext(self, node, inp):
        res = None
        if type(node) is Node:
            res = self._eval(inp, node)
        else:
            if node:
                res = node[0]
            elif len(inp) > 0:
                # substitute value
                res = inp[0]
                inp = inp[1:]
                inp.append(res)

        if res is None:
            raise UnexpectedEvalError('Unexpected error!')
        return res

    def _eval(self, inp, node):
        # evaluate if we have any children for this node
        if node.children:

            args = []

            if node.func.name == '_compare':
                # special behaviour for comparison
                if self.__evalNext(node.children[0], inp):
                    return self.__evalNext(node.children[1], inp)
                else:
                    return self.__evalNext(node.children[2], inp)

            else:

                for child in node.listChildren():
                    res = self.__evalNext(child, inp)
                    args.append(res)

                if node.func.name == '_push':
                    program_stack.append(*args)
                    return args[0]         # !!

                elif node.func.name == '_pop':
                    if program_stack:
                        return program_stack.pop(len(program_stack) - 1)
                    else:
                        return 0

                elif node.func.name == '_loop':
                    
                    pass

                return node.func(*args)
        else:
            return None 


    def eval(self, inp = []):
        return self._eval(inp, self.root)

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
        return Tree(root)

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


def _prodRandomAlgDesc(funclist, inputs, level, maxDepth):
    """ Generate random algorithm with the given depth (from TOP to BOTTOM) """

    if level > maxDepth:
        if not random.randint(0, 1):
            return [random.uniform(0, 1)]
        inputs[0] += 1
        return []

    rndfunc = funclist[random.randint(0, len(funclist) - 1)]
    arglst, nextNode = [], None

    for idx in xrange(rndfunc.argcnt):
        if nextNode is None:
            res = _prodRandomAlgDesc(funclist, inputs, level + 1, maxDepth)
            if type(res) is Node and res.func.name == '_demul':
                # if next node is _demul, connect all inputs of current node with that node
                nextNode = res
            if type(res) is Node and res.func.name == '_loop':
                # loop has only label to go as its argument
                
                pass
        else:
            res = nextNode
        arglst.append(res)

    return Node(rndfunc, arglst)

"""
def _prodRandomAlgAsc(funclist, argNum, level, maxDepth, children):

    if level == 1 and argNum:
        # level = 1 is the deepest level here, so here should be input leaf nodes
        # generate argNum input nodes
        inp_list = []
        for idx in xrange(argNum):
            inp_list.append([])
        return _prodRandomAlgAsc(funclist, argNum, level + 1, maxDepth, inp_list)
    else:
        # for each child node, generate its ancestor
        num_children = len(children)
        child_idx = 0
        nodes = []

        while 1:
            # filter out function with inappropriate number of inputs
            tmp = filter(lambda f: f.func.argcnt <= (num_children - child_idx) , funclist)
            rndfunc = tmp[random.randint(0, len(tmp) - 1)]
            arglst = []

            for idx in xrange(child_idx + 1, rndfunc.func.argcnt):
                arglst.append(children[idx])
                child_idx += 1

            nodes.append(Node(rndfunc, arglst))

            if child_idx >= num_children: 
                break

        if level <= maxDepth:
            return _prodRandomAlgAsc(funclist, argNum, level, maxDepth, nodes)
        else:
            # create a root node
            return Node(
"""

#@timeit
def prodRandomAlg(funclist, method, maxDepth, argNum = -1):

    if verbose:
        print 'Generating algorithm with maxdepth = %d' % maxDepth

    inputs = [0]
    random.seed()

    if method == 'desc':
        while 1:
            inputs = [0]
            res  = _prodRandomAlgDesc(funclist, inputs, 1, maxDepth)
            if argNum == -1 or inputs[0] == argNum: 
                break
        
    elif method == 'asc':
        res  = _prodRandomAlgAsc(funclist, argNum, 1, maxDepth, [])

    if verbose:
        print 'done!'

    return Tree(res), inputs[0]


root, inputs = prodRandomAlg(funclist = [add, sub, inc, dec, mul, div, compare, push, pop, demul], method = 'desc', maxDepth = 5, argNum = 1)
#root.save('algtest')
#root  = Tree.load('../pop1.dat')
#print root
#print root.getMinMaxId()
print root.eval([2])

