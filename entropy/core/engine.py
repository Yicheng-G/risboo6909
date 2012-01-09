""" Main engine module """

from gawrapper import GAWrapper, Population
from funclib import *

def test(chromosome):
    return sum(chromosome)

engine = GAWrapper()

# first of all - create and init a new population
pop1 = Population()
pop1.setFuncList([inc, dec])
pop1.setMaxSpecies(20)
pop1.setScoreF(test)

# add population to engine
engine.addPopulation(pop1)

# start evolution!
engine.startAll()

