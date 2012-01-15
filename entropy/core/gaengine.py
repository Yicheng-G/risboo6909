""" Simple GA engine """

import random
import copy

from funclib import *
from functree import *   

class GAInstance(object):

    MAX_INT = 99999

    def __init__(self, params):
        random.seed()
        self.params = params
        self.population = self.initRandomPop(self.params.getFuncList(), self.params.getMaxSpecies(), self.params.getMaxAlgSize())

    def initRandomPop(self, flist, maxspec, maxalg_sz):
        pop = []
        for x in xrange(maxspec):
            inst, args = prodRandomAlg(flist, 'desc', self.params.getDataRange(), random.randint(1, maxalg_sz), self.params.getArgsReq())
            pop.append([inst, args])
        return pop

    def findSubst(self, src_node, flist):
        # return the list of the functions from flist of the same arity as the given function src_f
        res = []
        for f in flist:
            if f.argcnt == src_node.func.argcnt:
                res.append(f)
        return res

    def evaluate(self):
        # get the scores for all instances and return them in array
        costs = []
        for inst in self.population:
            # compute score func
            penalty = self.params.getScoreF()(inst[0])
#            print penalty
            costs.append(penalty)

        # normalize costs
        m = min(costs)
        c = 1.0 / (max(costs) - m)
        for idx in xrange(len(costs)):
            costs[idx] = (c * (costs[idx] - m))
#        print costs
        return costs

    def roulette(self, costs):
        new_pop = []
        for idx in xrange(len(self.population)):
            rep = abs(int(costs[idx] * self.params.getMaxSpecies()))
            if rep > int(self.params.getMaxSpecies() * 0.1):
                rep = int(self.params.getMaxSpecies() * 0.1)
#            print '+', rep
            for x in xrange(rep):
                new_pop.append(self.population[idx])

        random.shuffle(new_pop)
        self.population = []

        for idx in xrange(len(new_pop)):
            self.population.append(copy.deepcopy(new_pop[idx]))

        self.population = self.population[:self.params.getMaxSpecies()]

        delta =  self.params.getMaxSpecies() - len(self.population)
#        print '*', delta
        if delta:
            tail = self.initRandomPop(self.params.getFuncList(), delta, self.params.getMaxAlgSize())
            self.population.extend(tail)

    def mutate(self):
        # do random mutations
        for item in self.population:
            if random.uniform(0, 1) <= self.params.getMutateRate():
                # take random node and replace it with another random node with the same arity
                for node in item[0].traverse():
                    if type(node) is not Node:
                        if random.uniform(0, 1) <= self.params.getMutateRate():
                            node = random.uniform(self.params.getDataRange()[0], self.params.getDataRange()[1])
                    else:
                        if random.uniform(0, 1) <= self.params.getMutateRate():
                            lst = self.findSubst(node, self.params.getFuncList())
                            new_f = random.choice(lst)
                            node.setFunc(new_f)

    def crossover(self):
        # do crossovers between entities
        if random.uniform(0, 1) <= self.params.getCrossoverRate():

            # choose random entity from current population
            if len(self.population) > 1:

                dst = src = random.choice(self.population)

                while dst == src:
                    dst = random.choice(self.population)

                # we have two unique species in src and dst to exchange 'genetic material'
                src, dst = src[0], dst[0]
                src_node, dst_node = None, None

                for node in src.traverse():
                    if random.uniform(0, 1) <= self.params.getCrossoverRate():
                        src_node = node
                        break

                for node in dst.traverse():
                    if random.uniform(0, 1) <= self.params.getCrossoverRate():
                        dst_node = node
                        break 

                if src_node and dst_node:
                    # exchange
                    src_node, dst_node = copy.deepcopy(dst_node), copy.deepcopy(src_node)
                    src.enum(set())
                    dst.enum(set())

    def getBestEntity(self, pop, costs):
        bestScore, bestItem = -GAInstance.MAX_INT, None
        for idx in xrange(len(pop)):
            item, cost = pop[idx], costs[idx]
            if cost > bestScore:
                bestItem, bestScore = item[0], cost
        return bestItem, bestScore

    def evolve(self, max_gen = 100):
        # computes evolution bounded by maximum generations number given by max_gen
        # if max_gen is -1 evolution will continue until good enough solution will be found
        best_item, best_score, gener = None, 0, 0
        costs_lst, cur_gen = [], 0
        local_best = 0
        while (cur_gen < max_gen or (max_gen == -1 and gener < self.params.getStopAfter())):
            costs = self.evaluate()
            tmp = self.getBestEntity(self.population, costs)
            """
            costs_lst.append(tmp[1])
            if len(costs_lst) == 100:
                del costs_lst[0]
            """
            if tmp[1] >= local_best:
                local_best = tmp[1]

            if tmp[1] >= best_score:
                best_score = tmp[1]
                best_item = copy.deepcopy(tmp[0])
                # exit immediately if score is 1
                if int(best_score) == 1:
                    break
                best_item.save(self.params.getFileName())
                gener = 0

            if not cur_gen % self.params.getReportRate():
                costs_lst.append(best_score)
                print 'generation N%d, best score so far is %f, local best %f' % (cur_gen, best_score, local_best)
                local_best = 0

            self.roulette(costs)
            self.mutate()
            self.crossover()
            cur_gen += 1
            gener += 1

        print best_item
        print 'score %f' % best_score
        best_item.save(self.params.getFileName())

