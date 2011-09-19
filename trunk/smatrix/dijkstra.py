# Dijkstra path search based on sparse matrix data structure
# to avoid surplus memory usage in many cases

from smatrix import SparseMatrix

INF = 10^5

def dijkstraRoutine(M):
    # make all the nodes weights equal to infinity first
    
    pass


# test case
M = SparseMatrix(dim = [6, 6])

# grpah has been taken from ru.wikipedia.org
M.setitem([0, 5], 14)
M.setitem([5, 0], 14)
M.setitem([0, 2], 9)
M.setitem([2, 0], 9)
M.setitem([0, 1], 7)
M.setitem([1, 0], 7)
M.setitem([5, 4], 9)
M.setitem([4, 5], 9)
M.setitem([5, 2], 2)
M.setitem([2, 5], 2)
M.setitem([2, 1], 10)
M.setitem([1, 2], 10)
M.setitem([2, 3], 11)
M.setitem([3, 2], 11)
M.setitem([1, 3], 15)
M.setitem([3, 1], 15)
M.setitem([4, 2], 6)
M.setitem([2, 4], 6)

print M

dijkstraRoutine(M)

