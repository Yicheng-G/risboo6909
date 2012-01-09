""" Generated programm will be represented as tree-hierarchy of functional
    blocks. This class defines an appropriate yet structure for it and simple program evaluator.
"""

from funclib import *


class Node(object):

    def __init__(self, f, values = []):
        self.children = []
        self.func = f

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


def prodRandomAlg():

    pass

#root = Node(mul, [Node(inc, [Node(ident)]), Node(inc, [Node(ident)])])
root = Node(compare, [Node(gt, [Node(inc, [Node(ident)]), Node(inc, [Node(ident)])]), Node(add, [1, 2]), Node(sub, [1, 2])])
print root

print root._eval([20, 1])
