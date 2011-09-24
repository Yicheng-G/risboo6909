# Dijkstra path search based on sparse matrix data structure
# to avoid surplus memory usage in many cases

from smatrix import SparseMatrix
import heapq

INF = 2 ** 31

def getNeighbours(M, pointIdx):
    tmp = []    
    for i in xrange(M.size()[1]):
        if M[pointIdx][i] != -1 and i != pointIdx:
            heapq.heappush(tmp, (M[pointIdx][i], i))
    return tmp

def recursiveStep(cur_node, lst, visited, M):
    minNode, minWeight, cur_weight = None, 0, M[cur_node][cur_node] 
    while lst:
        item = heapq.heappop(lst)
        weight, node = item
        if node in visited:
            continue
        if not minNode: 
            minNode = node
        if M[node][node] > cur_weight + weight:
            M.setitem([node, node], cur_weight + weight)
    if minNode:
        visited.append(minNode)
        recursiveStep(minNode, getNeighbours(M, minNode), visited, M)

def dijkstraAlgorithm(M, startPoint):
    # make all the nodes weights equal to infinity first
    cols, rows = M.size()[0], M.size()[1]
    if len(M.size()) != 2 or cols != rows:
        print 'Error: wrong matrix size'
        return
    # fill diagonal with INFs (initial distances)
    for i in xrange(rows):
        M.setitem([i, i], INF)
    M.setitem([startPoint, startPoint], 0)
    # from - is a column of a matrix, to - is a row of a matrix
    recursiveStep(startPoint, getNeighbours(M, startPoint), [startPoint], M)

"""
# test case
M = SparseMatrix(dim = [6, 6], defaultVal = -1)

# graph has been taken from ru.wikipedia.org
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
M.setitem([4, 3], 6)
M.setitem([3, 4], 6)

dijkstraAlgorithm(M, 0)

print M
"""

