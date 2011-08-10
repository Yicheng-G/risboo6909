class Node(object):

    def __init__(self, v = None, parent = None):
        self.__values = []
        self.__links = [None] * 4
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
            if a < self.min:    return 0
            if a > self.max:    return 1
        elif self.valcnt == 2:
            if a < self.min:    return 0
            if a > self.max:    return 2
            if self.min < a < self.max: return 1
        elif self.valcnt == 3:
            if a < self.min:    return 0
            if a > self.max:    return 3
            if self.min < a < self.med:   return 1
            if self.med < a < self.max:   return 2
        return -1

    def __rearrangeLinks(self, newVal):
        if self.valcnt != 0:
            if newVal < self.min:
                self.__links = [None] + self.__links[:3]
            elif self.valcnt == 2 and self.max > newVal > self.min:
                self.__links[3] = self.__links[2]
                self.__links[2] = self.__links[1]
                self.__links[1] = None


    # interface methods & properties

    def insertValue(self, newVal):
        if self.valcnt < 3:
            self.__rearrangeLinks(newVal)            
            self.values.append(newVal)
            self.__sort3(self.values)

    def removeValue(self, val):
        """ Remove value from the node """
        if not self.contains(val): return None
        del self.values[self.values.index(val)]

    def removeLink(self, node):
        """ Remove link from self to another node """
        for idx in xrange(self.refcnt):
            if self.links[idx] == node:
                self.links[idx] = None
                break

    def isConsistent(self):
        """ Check whether the node is consistent, this means it doesn't contain 3 items or 4 links """
        return not (self.valcnt > 2 or self.refcnt > 3)

    def getNodeItem(self, a):
        if not self.contains(a): return None
        return self.values[self.values.index(a)]       

    def isLeafNode(self):
        """ Check whether this is a leaf node or not """
        return self.refcnt == 0

    def getLinkByNo(self, n):
        """ Return node's n-th link (going from smallest to biggest) """
        return self.links[n]

    def getLinkIdx(self, destNode):
        for j in xrange(self.refcnt):
            if refs[j] == destNode: return j
        return -1

    def addLink(self, anotherNode):
        """ Add link to another node """
        if anotherNode is not None:
            idx = self.__getlink(anotherNode.min)
            if idx != -1:
                 self.links[idx] = anotherNode
        return self

    def contains(self, a):
        """ Check if node contains a given value """
        if self.valcnt == 0:  return False
        return False if (self.min > a or self.max < a) else (a in self.values)

    def chooseChild(self, a):
        """ Choose where to go according to the value a """
        idx = self.__getlink(a)
        if idx != -1: return self.links[idx]
        return None

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
    def minLink(self):
        return self.links[0]

    @property
    def valcnt(self):
        return len(self.__values)

    @property
    def refcnt(self):
        net = 0
        for idx in xrange(len(self.__links)):
            if self.__links[idx] is not None: net += 1
        return net

    @property
    def values(self):
        return self.__values

    @property
    def links(self):
        return self.__links

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, ref):
        self.__parent = ref

    # private methods

    def __sort3(self, arr):
        if len(arr) >= 2:
            if arr[0] > arr[1]: arr[0], arr[1] = arr[1], arr[0]
        if len(arr) == 3:
            if arr[1] > arr[2]: arr[1], arr[2] = arr[2], arr[1]
            if arr[0] > arr[1]: arr[0], arr[1] = arr[1], arr[0]


class TTTree(object):

    def __init__(self):
        self.root = Node()
        self.parent = None

    def __str__(self):
        """ String representation of a tree """
        pass

    def __find(self, curNode, a):
        if curNode.contains(a): return curNode
        # determine where to go further
        nextNode = curNode.chooseChild(a)
        if nextNode is None:
            return curNode
        return self.__find(nextNode, a)

    def __getLeftSibling(self, node):
        """ Returns left sibling of a node """
        if node.parent is not None:
            refidx = node.parent.getLinkIdx(node)
            if refidx != -1 and refidx != 0:
                return node.parent.links[refidx - 1]
        return None
    
    def __getRightSibling(self, node):
        """ Returns right sibling of a node """
        if node.parent is not None:
            refidx = node.parent.getLinkIdx(node)
            tmp = node.parent.links
            if refidx != -1 and refidx + 1 < len(tmp):
                return node.parent.links[refidx + 1]
        return None

    def __nextSucc(self, node):
        if not node.isLeafNode():
            return self.__nextSucc(node.minLink)
        return node

    def __findInorderSucc(self, node, a):
        if node.isLeafNode():
            return node
        new_node = node.chooseChild(a + 1)
        return self.__nextSucc(new_node)

    def __swapValues(self, node1, a1, node2, a2):
        """ Swap any two values in nodes """
        item1 = node1.getNodeItem(a1)
        item2 = node2.getNodeItem(a2)
        item1.value, item2.value = item2.value, item1.value

    def __fixNodeRemove(self, node):
        if node.valcnt == 0:
            if node is self.root:
                # remove the root, set new root pointer
                pass
            else:
                # check whether one of our siblings has two items
#                if self.__getLeftSibling(node).valcnt == 2:
                pass

    def __fixNodeInsert(self, node):
        print 'cons:', node, node.isConsistent()
        if not node.isConsistent():
            # conflict detected, try to resolve it
            if node.isLeafNode() and node is not self.root:
                
    #            print node.min, node.med, node.max
                # case for leaf node
    #            print 'parent for %s: %s %s' % (node, node.parent, node.parent.parent)
    #            print self.root.links[1]
    #            print '----'
                node.parent.insertValue(node.med)
                node.parent.removeLink(node)
                # split the node
                node.parent.addLink(Node(node.min, node.parent))
                node.parent.addLink(Node(node.max, node.parent))
                self.__fixNodeInsert(node.parent)
            else:
                # case for internal node or root node
                links = node.links
                
                if node is not self.root:
                    node.parent.insertValue(node.med)
                    node.parent.removeLink(node)
                    parent = node.parent
                else:                    
                    self.root = Node(node.med)
                    parent = self.root
                    print 'root work'

                # split the node         
                leftNode = Node(node.min, parent)
                rightNode = Node(node.max, parent)

                parent.addLink(leftNode).addLink(rightNode)
                print links[0], links[1], links[2], links[3]
                leftNode.addLink(links[0]).addLink(links[1])
                rightNode.addLink(links[2]).addLink(links[3])

                if node is not self.root:
                    self.__fixNodeInsert(parent)

        else: return

    def contains(self, a):
        """ See if we have a given value in our tree """ 
        node = self.findNode(a)
        return node if node.contains(a) else None

    def findNode(self, a):
        """ Find the node which contains the given value """
        return self.__find(self.root, a)

    def insertValue(self, a):
        """ Inserts a new value to tree and keeps it balanced """
        node = self.findNode(a)
        if node.contains(a):
            return None
        # try to insert a new value into existing node
        print 'inserting %d' % a
        node.insertValue(a)
        self.__fixNodeInsert(node)
        return self

    def removeValue(self, a):
        """ Removes a value from the tree and keeps it balanced """
        node = self.findNode(a)
        if not node.contains(a):
            return None
        succ = node
        if not node.isLeafNode():
            # swap the value we want to delete with its inorder successor (always leaf)
            succ = self.__findInorderSucc(node, a)
            self.__swapValues(node, a, succ, succ.min)
        # delete leaf node value
        succ.removeValue(a)
        # fix tree if needed
        self.__fixNodeRemove(succ)
        
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



t.insertValue(35)




t.insertValue(38)


print t.root.links[1].links[1]

t.insertValue(40)

t.insertValue(50)

# ---------------

t.removeValue(15)

print t.root.getLinksList()[2].getLinksList()[1]

