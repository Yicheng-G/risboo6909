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
        # returns linear index by the given n-d index
        linearIdx = idx[0]
        if len(idx) > 1:
            for i in xrange(1, len(self.dim)):
                linearIdx += reduce(lambda x, y: x * y, self.dim[:i]) * idx[i]       
        # check bounds
        if 'maxIdx' in self.__dict__ and linearIdx > self.maxIdx:
            print 'Index out of bounds!'
        return linearIdx

    def __invIndexFunc(self, idx):
        # returns n-d index by the given linear index
        output = [0] * len(self.dim)
        for i in xrange(len(self.dim) - 1, 0, -1):
            divisor = reduce(lambda x, y: x * y, self.dim[:i])
            result = idx / divisor
            idx -= result * divisor
            output[i] = result
        output[0] = idx
        return output

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
            res = self.trunk.insertValue(Pair(linidx, val))
            if type(res) is Pair: res.value = val
        return self

    def size(self):
        return self.dim
  
    def __str__(self):
        buf = []
        for node in self.trunk:
            for pair in node:
                if pair is not None: 
                    buf.append('%s: %s' % (self.__invIndexFunc(pair.key), pair.value))
        return ', '.join(buf)

