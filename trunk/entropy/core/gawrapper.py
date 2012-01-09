""" Wrapper for pyevolove library to support multiprocessing
    and more convenient usage.
"""

import pyevolve
import copy_reg
import types
import time

from multiprocessing import Pool
from pyevolve import G1DList
from pyevolve import GSimpleGA
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

    def setFuncList(self, funclist):
        self.funclist = funclist
        self.funccnt = len(self.funclist)

    def getFuncCnt(self):
        return self.funccnt

    def setMaxSpecies(self, n):
        self.maxSpecies = n

    def getMaxSpecies(self):
        return self.maxSpecies

    def setScoreF(self, f):
        self.score_func = f

    def setFitness(self):
        pass

    def start(self):
        genome = G1DList.G1DList(self.getMaxSpecies())
        genome.setParams(rangemin = 0, rangemax = self.getFuncCnt() - 1)
        genome.evaluator.set(self.score_func)
        ga = GSimpleGA.GSimpleGA(genome, interactiveMode = False)
        ga.evolve(freq_stats = 10)

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

