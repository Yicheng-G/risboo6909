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
        self.__lt = ref

    @property
    def greaterThan(self):
        return self.__gt

    @greaterThan.setter
    def greaterThan(self, ref):
        self.__gt = ref


class Node(object):

    def __init__(self):
        self.__values = []
        self.__parent = None

    def __str__(self):
        out = ''
        for v in self.values:
            out += (str(v) + ' ')
        return out

    # interface methods & properties

    def insertValue(self, val):
        if self.valcnt < 3:
            self.__values.append(Value(val))
            self.__sort3(self.__values)

    def addLink(self, ref):
        # see where to insert this link
        
        pass 

    def setParent(self, obj):
        self.__parent = obj

    def contains(self, a):
        """ Check if node contains a given value """   
        return False if (self.min > a or self.max < a) else (a in self.values)

    def chooseChild(self, a):
        """ Choose where to go according to the value a """
        if self.valcnt == 2:
            if a < self.min:    return self.min.lessThan
            if a > self.max:    return self.max.greaterThan
            if a > self.min and a < self.max: return self.min.greaterThan
        elif self.valcnt == 3:
            pass

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
    def values(self):
        return self.__values

    @property
    def parent(self):
        return self.__parent

    # private methods

    def __sort3(self, arr):
        if len(arr) >= 2:
            if arr[0].value > arr[1].value: arr[0].value, arr[1].value = arr[1].value, arr[0].value
        if len(arr) == 3:
            if arr[1].value > arr[2].value: arr[1].value, arr[2].value = arr[2].value, arr[1].value
            if arr[0].value > arr[1].value: arr[0].value, arr[1].value = arr[1].value, arr[0].value


class TTTree(object):

    def __init__(self):
        self.__root = Node()        

    def __find(self, curnode, a):
        if curnode.contains(a): return curnode
        # determine where to go further
         

    def contains(self, a):
        """ See if we have a given value in our tree """ 
        return self.__find(self.__root, a)

    def findNode(self, a):
        """ Find the node which contains the given value """
        pass

    def insertValue(self, a):
        """ Inserts a new value to tree and resolves conflicts if needed """
        
        pass

n = Node()
n.insertValue(10)
n.insertValue(5)
n.insertValue(20)

print n.med


#t = TTTree()
#t.addValue(12)

