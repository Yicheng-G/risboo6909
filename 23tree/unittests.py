#! /usr/bin/python

# simple set of tests for 2-3 tree

from tttree import TTTree
import random, time

ITEMS = 100000
RANDMAX = 1000000


def timer(f):
    def inner(*args, **kwargs):
        start_t = time.time()
        f(*args, **kwargs)
        print 'done in %f sec' % (time.time() - start_t)
        return time.time() - start_t
    return inner

@timer
def insertTest(tree, items):
    print 'test 1 - insert %d elements...' % len(items)
    for j in items:
        tree.insertValue(j)

@timer
def consTest(tree, items): 
    print 'test 2 - checking consistency of %d elements...' % len(items)
    tree.findInorderSucc(tree.root, tree.root.min)
    maxDepth = tree.lastSearchDepth
    for j in items:
        assert(tree.contains(j))
        assert(tree.lastSearchDepth <= maxDepth)

@timer
def removeTest(tree, items):
    print 'test 3 - deleting all the elements...'
    for j in items:
        tree.removeValue(j)

ins, cons, rem  = [], [], []

for x in xrange(5):
    print 'Test N%d' % x
    tree = TTTree()
    print 'generating set...'
    items = set()
    for x in xrange(ITEMS):
        val = random.randint(0, RANDMAX)
        if val not in items: items.add(val)
    print 'done'
    ins.append(insertTest(tree, items))
    cons.append(consTest(tree, items))
    print 'shuffling...'
    items = list(items)
    random.shuffle(items)
    print 'done'
    rem.append(removeTest(tree, items))
    assert(tree.root is None)

print
print 'avg insert time %f' % (sum(ins) / len(ins))
print 'avg cons time %f' % (sum(cons) / len(cons))
print 'avg remove time %f' % (sum(rem) / len(rem))

