# Sparse matrix class based on 2-3 trees

from tttree import TTTree, Pair

class SparseMatrix:

    def __init__(self, dim, defaultVal = 0):
        self.dim = dim
        self.defVal = defaultVal
        self.trunk = TTTree()
        self.getidx = []
        self.maxIdx = self.__indexFunc(map(lambda x: x - 1, self.dim))

    def __indexFunc(self, idx):
        linearIdx = idx[0]
        if len(idx) > 1:
            for i in xrange(1, len(self.dim)):
                linearIdx += reduce(lambda x, y: x * y, self.dim[:i]) * idx[i]       
        # check bounds
        if 'maxIdx' in self.__dict__ and linearIdx > self.maxIdx:
            print 'Index out of bounds!'
        return linearIdx

    def __getitem__(self, idx):
        self.getidx.append(idx)
        if len(self.getidx) == len(self.dim):
            linidx = self.__indexFunc(self.getidx)
            node = self.trunk.contains(linidx)
            self.getidx = []
            if node:
                return node.getItem(linidx).val()
            return self.defVal
        return self
    
    def setitem(self, idxlst, val):
        if len(idxlst) == len(self.dim):            
            linidx = self.__indexFunc(idxlst)
            self.trunk.insertValue(Pair(linidx, val))
        return self

    def size(self):
        return self.dim
  
    def __str__(self):
        return str(self.trunk)

