#! /usr/bin/python

# simple set of tests for 2-3 tree

from tttree import TTTree
import random, time

ITEMS = 1000000
RANDMAX = 100000000000
tree = TTTree(use_poll = True)

def timer(f):
    def inner(*args, **kwargs):
        start_t = time.time()
        f(*args, **kwargs)
        print 'done in %f sec' % (time.time() - start_t)
    return inner

@timer
def insertTest(items):    
    print 'test 1 - insert %d elements...' % ITEMS
    net, elements = 0, 0
    for j in xrange(ITEMS):
        val = random.randint(0, RANDMAX)
        if val not in items:
            items.add(val)
            a = time.time()
            tree.insertValue(val)
            net += (time.time() - a)
            elements += 1
    print 'tree insertion time %f, elements actually inserted %d' % (net, elements)

@timer
def consTest(items):  
    print 'test 2 - checking consistency of %d elements...' % len(items)
    for j in items:
        assert(tree.contains(j))       

@timer
def removeTest(items):
    print 'test 3 - deleting all the elements...'
    for j in items:
        tree.removeValue(j)     

items = set()
insertTest(items)
consTest(items)
removeTest(items)

