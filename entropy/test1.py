""" Main engine module """

from core.gawrapper import GAWrapper, Population
from core.funclib import *

def score(alg):
    """
    pts = 100
    try:
        for x in xrange(0, 100):
            if alg.eval([x]) == ((x + 1) / 2): pts -= 1
    except:
        pass
    """
    try:
        pts = 0
        for x in xrange(0, 100):
            pts += abs(alg.eval([x]) - (x + x + x))
    except:
        pts = -1
    return pts

engine = GAWrapper()

# first of all - create and init a new population
pop1 = Population()
pop1.setFuncList([inc, dec, add, sub, mul, ident, demul])
pop1.setArgsReq(1)
pop1.setDataRange(0, 3)
pop1.setMaxSpecies(100)
pop1.setMaxAlgSize(4)
pop1.setReportRate(10)
pop1.setStopAfter(100)
#pop1.setMaxGen(3)
pop1.setMaxGen(-1)
pop1.setScoreF(score)
pop1.setFileName('pop1.dat')

# add population to engine
engine.addPopulation(pop1)

# start evolution!
engine.startAll()

