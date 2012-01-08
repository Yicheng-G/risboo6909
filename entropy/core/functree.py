""" Generated programm will be represented as tree-hierarchy of functional
    blocks. This class defines an appropriate yet simple tree structure for it.
"""

class Node(object):

    def __init__(self, maxChildren = 2):
        self.__children = []
        self.__maxChildren = maxChildren

    def listChildren(self):
        for item in self.__children:
            yield item

    def addChild(self, node):
        if len(self.__children) < self.__maxChildren:
            self.__children.append(node)


class FuncTree(object):

    def __init__(self):
        pass

   
