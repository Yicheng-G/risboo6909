""" Main engine module """

from gawrapper import GAWrapper, Population
from funclib import *

def score(alg):
    pts = 50
    try:
        for x in xrange(0, 50):
            if alg._eval([x, x]) == (x + x): pts -= 1
    except:
        pass
    return pts

engine = GAWrapper()

# first of all - create and init a new population
pop1 = Population()
pop1.setFuncList([inc, dec, add, sub, mul, ident])
pop1.setArgsReq(1)
pop1.setMaxSpecies(30)
pop1.setMaxAlgSize(3)
pop1.setReportRate(100)
pop1.setMaxGen(-1)
pop1.setScoreF(score)
pop1.setFileName('pop1.dat')

# add population to engine
engine.addPopulation(pop1)

# start evolution!
engine.startAll()

