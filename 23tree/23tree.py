class Node(object):

    def __init__(self, v = None, parent = None):
        self.__values = []
        self.__links = []
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
        # rearrange links when adding a new node
        if self.valcnt != 0:            
            if newVal < self.min:
                # shift all the links to the right when adding new min element
                self.__links = [None] + self.links[:self.refcnt]
            elif self.valcnt == 2 and self.refcnt == 3 and self.max > newVal > self.min:
                # rearrange middle links when adding med element
                self.links[3] = self.links[2]
                self.links[2] = self.links[1]
                self.links[1] = None

    def __sort3(self, arr):
        if len(arr) >= 2:
            if arr[0] > arr[1]: arr[0], arr[1] = arr[1], arr[0]
        if len(arr) == 3:
            if arr[1] > arr[2]: arr[1], arr[2] = arr[2], arr[1]
            if arr[0] > arr[1]: arr[0], arr[1] = arr[1], arr[0]


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
        self.links.remove(node)

    def isConsistent(self):
        """ Check whether the node is consistent, this means it doesn't contain 3 items or 4 links """
        return not (self.valcnt > 2 or self.refcnt > 3)

    def isLeafNode(self):
        """ Check whether this is a leaf node or not """
        return self.refcnt == 0

    def isEmptyNode(self):
        """ Returns true if node doesn't containt any  value """
        return self.valcnt == 0

    def getLink(self, linkIdx):
        if linkIdx >= self.refcnt or linkIdx < 0: return None
        return self.links[linkIdx]

    def getLinkIdx(self, destNode):
        """ Get index of the link which points to the given node """
        try:
            return self.links.index(destNode)
        except ValueError:
            return -1

    def addLink(self, anotherNode):
        """ Add link to another node """
        if anotherNode is not None:
            idx = self.__getlink(anotherNode.min)
            if idx != -1:
                if idx < self.refcnt:
                    self.links[idx] = anotherNode
                else:
                    self.links.append(anotherNode)                
                anotherNode.parent = self
        return self

    def contains(self, a):
        """ Check if node contains a given value """
        if self.valcnt == 0:  return False
        return False if (self.min > a or self.max < a) else (a in self.values)

    def chooseChild(self, a):
        """ Choose where to go according to the value a """
        idx = self.__getlink(a)
        if idx != -1 and idx < self.refcnt: 
            return self.links[idx]
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
        return len(self.values)

    @property
    def refcnt(self):
        return len(self.links)

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



class TTTree(object):

    def __init__(self):
        self.__root = Node()

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
        if node is not None and node.parent is not None:
            refidx = node.parent.getLinkIdx(node)
            return node.parent.getLink(refidx - 1)
        return None
    
    def __getRightSibling(self, node):
        """ Returns right sibling of a node """
        if node is not None and node.parent is not None:
            refidx = node.parent.getLinkIdx(node)
            return node.parent.getLink(refidx + 1)
        return None

    def __getSiblings(self, node):
        """ Returns node's siblings """
        # check whether one of our siblings has two items
        lS, rS = None, None
        lCnt, rCnt = 0, 0       
        if self.__getRightSibling(node) is not None:
            rS = self.__getRightSibling(node)
            rCnt = rS.valcnt
        if self.__getLeftSibling(node) is not None:
            lS = self.__getLeftSibling(node)
            lCnt = lS.valcnt
        return lS, lCnt, rS, rCnt

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
        idx1, idx2 = node1.values.index(a1), node2.values.index(a2)
        node1.values[idx1], node2.values[idx2] = node2.values[idx2], node1.values[idx1]

    def __fixNodeRemove(self, node, parent = -1):
        
        """ Fix deletion """
      
        if node.isEmptyNode():

            if node is not self.root:

                if parent == -1:
                    parent = node.parent
     
                if node.isEmptyNode() or not node.isConsistent():

                    lS, lCnt, rS, rCnt = self.__getSiblings(node)
                    rSS, lSS = self.__getRightSibling(rS), self.__getLeftSibling(lS)

                    redistribute = True
                    
                    if rS != None or lS != None:

                        if   rCnt == 2 or (rCnt == 1 and rSS != None and rSS.valcnt == 2):
                            sib = rS
                        elif lCnt == 2 or (lCnt == 1 and lSS != None and lSS.valcnt == 2):
                            sib = lS
                        elif lCnt == 1:
                            sib, redistribute = lS, False
                        elif rCnt == 1:
                            sib, redistribute = rS, False

                    if redistribute:
                        # case 1: sibling leaf exists and contains 2 items => redistribute

                        # left and right case
                        if parent.valcnt == 1:
                            if node == parent.getLink(0):
                                parent_val, sib_val = parent.min, sib.min
                                child = sib.chooseChild(sib_val - 1)
                            elif node == parent.getLink(1):
                                parent_val, sib_val = parent.max, sib.max
                                child = sib.chooseChild(sib_val + 1)  
                        else:
                            if sib == parent.getLink(1):
                                # left
                                if node == parent.getLink(0):
                                    parent_val, sib_val = parent.min, sib.min
                                    child = sib.chooseChild(sib_val - 1)
                                # right
                                elif node == parent.getLink(2):
                                    parent_val, sib_val = parent.max, sib.max
                                    child = sib.chooseChild(sib_val + 1)
                            # middle
                            elif sib == parent.getLink(2):
                                parent_val, sib_val = parent.max, sib.min
                                child = sib.chooseChild(sib_val - 1)
                            elif sib == parent.getLink(0):
                                parent_val, sib_val = parent.min, sib.max
                                child = sib.chooseChild(sib_val + 1)

                        if not node.isLeafNode():
                            # if this is not a leaf node, redistribute the links also
                            node.addLink(child)
                            sib.removeLink(child)

                        node.insertValue(parent_val)
                        parent.removeValue(parent_val)
                        parent.insertValue(sib_val)
                        sib.removeValue(sib_val)                

                        next_node = sib

                    else:
                        # case 2: sibling leaf exists and contains only 1 item => merge
                        if parent.valcnt == 1:
                            parent_val = parent.values[0]
                        else:                            
                            if sib == parent.getLink(0):
                                parent_val = parent.min
                            elif sib == parent.getLink(1):
                                if sib == rS:
                                    parent_val = parent.min
                                elif sib == lS:
                                    parent_val = parent.max

                        child = node.getLink(0)

                        assert(node.refcnt == 1)

                        if not node.isLeafNode():
                            sib.addLink(child)

                        sib.insertValue(parent_val)
                        parent.removeValue(parent_val)
                        parent.removeLink(node)

                        next_node = sib
                    
                self.__fixNodeRemove(next_node, parent) 
            
            else:
                # root node
                self.root = self.getLink(0)
                        


    def __fixNodeInsert(self, node):
        if not node.isConsistent():
            # conflict detected, try to resolve it
            if node.isLeafNode() and node is not self.root:               
                # case for leaf node
                node.parent.insertValue(node.med)
                node.parent.removeLink(node)
                # split the node
                node.parent.addLink(Node(node.min, node.parent))
                node.parent.addLink(Node(node.max, node.parent))
                self.__fixNodeInsert(node.parent)
            else:
                # case for internal node or root node 
                if node is not self.root:
                    node.parent.insertValue(node.med)
                    node.parent.removeLink(node)
                    parent = node.parent
                else:                    
                    self.root = Node(node.med)
                    parent = self.root
                # split the node
                leftNode = Node(node.min, parent)
                rightNode = Node(node.max, parent)

                parent.addLink(leftNode).addLink(rightNode)
                leftNode.addLink(node.getLink(0)).addLink(node.getLink(1))
                rightNode.addLink(node.getLink(2)).addLink(node.getLink(3))

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
        node.insertValue(a)
        self.__fixNodeInsert(node)
        return self

    def removeValue(self, a):
        """ Removes a value from the tree and keeps it balanced """
        node = self.findNode(a)
        if not node.contains(a):
            return None
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
#t.insertValue(40)
#t.insertValue(50)

#t.insertValue(39)

# ---------------

t.removeValue(26)

print t.root.links[1].links[1]


