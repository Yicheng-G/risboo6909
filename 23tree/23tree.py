class Node:

    def getOrdered(self):
        if len(self.__values) != 0:
            a = max(self.__values)
            c = min(self.__values)
            return a, c
        return None

    def addVal(self, val):
        if len(self.__values) < 3:
            self.__values.add(val)
 
    def __init__(self):
        self.__values = set()


n = Node()
n.addVal(10)
n.addVal(5)
n.addVal(20)
print n.getOrdered()

