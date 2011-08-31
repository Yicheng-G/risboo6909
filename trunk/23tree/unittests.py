# simple set of tests for 2-3 tree

from tttree import TTTree
import random

ITEMS = 10
RANDMAX = 100
tree = TTTree()

# test 1: random items insertion
print 'test 1 - insert %d elements...' % ITEMS
items = set()
for j in xrange(ITEMS):
    val = random.randint(0, RANDMAX) 
    items.add(val)
    tree.insertValue(val)
print 'done!'

print 'test 2 - checking consistency...'
for j in items:
    assert(tree.contains(j))       
print 'done!'

print 'test 3 - deleting all the elements...'
print items
for j in items:
    print j
    tree.removeValue(j)     
print 'done!'
