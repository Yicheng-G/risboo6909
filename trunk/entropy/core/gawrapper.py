""" Wrapper for pyevolove library to support multiprocessing
    and more convenient usage.
"""

import copy_reg
import types
import time

from multiprocessing import Pool
from gaengine import GAInstance
from funclib import *

def _pickle_method(method):
    func_name = method.im_func.__name__
    obj = method.im_self
    cls = method.im_class
    return _unpickle_method, (func_name, obj, cls)

def _unpickle_method(func_name, obj, cls):
    for cls in cls.mro():
        try:
            func = cls.__dict__[func_name]
        except KeyError:
            pass
        else:
            break
    return func.__get__(obj, cls)

copy_reg.pickle(types.MethodType, _pickle_method, _unpickle_method)


class Population(object):

    def __init__(self):
        self.funclist = []
        self.funccnt = 0
        self.score_func = None
        self.maxGen = -1
        self.mutateRate = 0.3
        self.stopAfterGen = 10000
        self.filename = 'default.dat'

    def setStopAfter(self, n):
        self.stopAfterGen = n

    def getStopAfter(self):
        return self.stopAfterGen

    def setFileName(self, filename):
        self.filename = filename

    def getFileName(self):
        return self.filename 

    def setFuncList(self, funclist):
        self.funclist = funclist
        self.funccnt = len(self.funclist)

    def getFuncList(self):
        return self.funclist

    def getFuncCnt(self):
        return self.funccnt

    def setMutateRate(self, n):
        self.mutateRate = n

    def getMutateRate(self):
        return self.mutateRate

    def setReportRate(self, n):
        self.reportRate = n 

    def getReportRate(self):
        return self.reportRate

    def setMaxAlgSize(self, n):
        self.maxAlgSize = n

    def getMaxAlgSize(self):
        return self.maxAlgSize

    def setMaxSpecies(self, n):
        self.maxSpecies = n

    def getMaxSpecies(self):
        return self.maxSpecies

    def setArgsReq(self, n):
        self.argsReq = n

    def getArgsReq(self):
        return self.argsReq

    def setMaxGen(self, n):
        self.maxGen = n

    def getMaxGen(self):
        return self.maxGen

    def setScoreF(self, f):
        self.score_func = f

    def getScoreF(self):
        return self.score_func

    def start(self):
        ga = GAInstance(self)
        ga.evolve(self.getMaxGen())

class GAWrapper(object):

    def __init__(self, max_proc = 2):
        self.populations = []
        self.maxProc = max_proc
        self.pool = Pool(processes = self.maxProc, maxtasksperchild = 1)

    def addPopulation(self, pop):
        self.populations.append(pop) 

    def startAll(self):
        results = []
        for pop in self.populations: 
            results.append(self.pool.apply_async(pop.start))
        for res in results:
            res.wait()

