class Value(object):

    def __init__(self, value, lt = None, gt = None):
        self.__value = value
        self.__gt = lt
        self.__lt = gt

    def __str__(self):
        return '%s' % self.value

    def __eq__(self, other):
        return self.value == other.value if isinstance(other, Value) else other == self.value

    def __gt__(self, other):
        return self.value > other.value if isinstance(other, Value) else self.value > other

    def __lt__(self, other):
        return self.value < other.value if isinstance(other, Value) else self.value < other

    # interface methods & properties

    def resetLinks(self):
        self.__lt = self.__gt = None

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, a):
        self.__value = a

    @property
    def lessThan(self):
        return self.__lt

    @lessThan.setter
    def lessThan(self, ref):
        """ Link to the element less than self """
        self.__lt = ref

    @property
    def greaterThan(self):
        """ Link to the element greater than self """
        return self.__gt

    @greaterThan.setter
    def greaterThan(self, ref):
        self.__gt = ref


class Node(object):

    LEFT = 0
    RIGHT = 1

    def __init__(self, v = None, parent = None):
        self.__values = []
        self.__parent = parent
        if v != None:
            if type(v) is list:
                for item in v:
                    self.insertValue(item)
            else:
                self.insertValue(v)

    def __str__(self):
        out = ''
        for v in self.values:
            out += (str(v) + ' ')
        return out

    def __getlink(self, a):
        if self.valcnt == 1:
            if a < self.min:    return self.values[0], self.LEFT
            if a > self.max:    return self.values[0], self.RIGHT
        elif self.valcnt == 2:
            if a < self.min:    return self.values[0], self.LEFT
            if a > self.max:    return self.values[1], self.RIGHT
            if a > self.min and a < self.max: return self.values[0], self.RIGHT
        elif self.valcnt == 3:
            if a < self.min:    return self.values[0], self.LEFT
            if a > self.max:    return self.values[2], self.RIGHT
            if a > self.min and a < self.med:   return self.values[1], self.LEFT
            if a > self.med and a < self.max:   return self.values[1], self.RIGHT
        return None, None

    # interface methods & properties

    def insertValue(self, val):
        if self.valcnt < 3:
            if type(val) is not Value:
                self.__values.append(Value(val))
            else:
                self.__values.append(val)
            self.__sort3(self.__values)

    def removeValue(self, val):
        """ Remove value from the node """
        if not self.contains(val): return None
        del self.__values[self.values.index(val)]

    def removeLink(self, node):
        """ Remove link from self to node """
        for ref in self.values:
            if ref.lessThan == node: 
                ref.lessThan = None
            if ref.greaterThan == node:
                ref.greaterThan = None

    def isConsistent(self):
        """ Check whether the node is consistent, this means it doesn't contain 3 items or 4 links """
        return not (self.valcnt > 2 or self.refcnt > 3)

    def isLeafNode(self):
        """ Check whether this is a leaf node or not """
        return self.refcnt == 0

    def addLink(self, nodeRef):
        """ Add link to another node """
        if nodeRef is None: return
        ref, side = self.__getlink(nodeRef.min)
        if ref != None:
            if side == self.LEFT: ref.lessThan = nodeRef
            else: ref.greaterThan = nodeRef
            nodeRef.parent = self

    def contains(self, a):
        """ Check if node contains a given value """
        if self.valcnt == 0:  return False
        return False if (self.min > a or self.max < a) else (a in self.values)

    def chooseChild(self, a):
        """ Choose where to go according to the value a """
        ref, side = self.__getlink(a)
        if ref != None:
            if side == self.LEFT: return ref.lessThan
            else: return ref.greaterThan

    @property
    def min(self):
        return self.values[0]

    @property
    def med(self):
        if self.valcnt == 3:
            return self.values[1]
        else: return None

    @property
    def max(self):
        return self.values[self.valcnt - 1]

    @property
    def valcnt(self):
        return len(self.__values)

    @property
    def refcnt(self):
        tmp = set()
        for val in self.values:
            if val.lessThan != None:
                tmp.add(val.lessThan)
            if val.greaterThan != None:
                tmp.add(val.greaterThan)
        return len(tmp)

    @property
    def values(self):
        return self.__values

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, ref):
        self.__parent = ref

    # private methods

    def __sort3(self, arr):
        if len(arr) >= 2:
            if arr[0].value > arr[1].value: arr[0].value, arr[1].value = arr[1].value, arr[0].value
        if len(arr) == 3:
            if arr[1].value > arr[2].value: arr[1].value, arr[2].value = arr[2].value, arr[1].value
            if arr[0].value > arr[1].value: arr[0].value, arr[1].value = arr[1].value, arr[0].value


class TTTree(object):

    def __init__(self):
        self.root = Node()
        self.parent = None

    def __str__(self):
        """ String representation of a tree, this operation mb cpu consuming """
        pass

    def __find(self, curNode, a):
        if curNode.contains(a): return curNode
        # determine where to go further
        nextNode = curNode.chooseChild(a)
        if nextNode is None:
            return curNode
        return self.__find(nextNode, a)

    def __fixNode(self, node):
        if not node.isConsistent():
            # conflict detected, try to resolve it
            if node is self.root:
                # take the middle element of a root node and treat it as a new root node
                self.root = Node(node.med.value)
                leftNode = Node(node.min.value, self.root)
                rightNode = Node(node.max.value, self.root)
                self.root.addLink(leftNode)
                self.root.addLink(rightNode)

                leftNode.addLink(node.med.lessThan)
                rightNode.addLink(node.med.greaterThan)
            elif node.isLeafNode():
                # case for leaf node
                print node.min.value, node.med.value, node.max.value
                print node.parent
                node.parent.insertValue(node.med.value)
                leftNode = Node(node.min.value, node.parent)
                rightNode = Node(node.max.value, node.parent)
                node.parent.removeLink(node)
                node.parent.addLink(leftNode)
                node.parent.addLink(rightNode)
                self.__fixNode(node.parent)
            else:
                # case for internal node (the hardest one)
                mid = node.med

                leftNode = Node(node.min.value, node.parent)
                rightNode = Node(node.max.value, node.parent)

                node.parent.removeLink(node)
                
                leftNode.addLink(mid.lessThan)
                rightNode.addLink(mid.greaterThan)

                node.parent.addLink(leftNode)
                node.parent.addLink(rightNode)

                self.__fixNode(node.parent)
 

        else: return

    def contains(self, a):
        """ See if we have a given value in our tree """ 
        node = self.findNode(a)
        return node if node.contains(a) else None

    def findNode(self, a):
        """ Find the node which contains the given value """
        return self.__find(self.root, a)

    def insertValue(self, a):
        """ Inserts a new value to tree and resolves conflicts if needed """
        node = self.findNode(a)
        if node.contains(a): 
            return None
        # try to insert a new value into existing node
        node.insertValue(a)
        self.__fixNode(node)
        return node
        
    @property
    def root(self):
        return self.__root

    @root.setter
    def root(self, ref):
        self.__root = ref


t = TTTree()
t.insertValue(12)
t.insertValue(20)
t.insertValue(15)

t.insertValue(25)
t.insertValue(27)
t.insertValue(30)

t.insertValue(26)

print t.root.max.greaterThan.min.greaterThan


