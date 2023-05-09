from copy import deepcopy
from typing import List
from math import sqrt
from random import choices, random
from genprog.modules.gene import available_non_terminals, available_terminals, calc_max_depth
from genprog.modules.chromosome import Chromosome, grow, full

class Population:
    def __init__(self, max_depth: int, indc: int, varc: int, pcross: float, pmutate: float, data: List[List[float]], constants: List[int] = []) -> None:
        self.max_depth = max_depth
        self.indc = indc
        self.pcross = pcross
        self.pmutate = pmutate
        self.varc = varc
        self.pop_fitness: List[float] = []
        self.gen = 0
        self.data = data

        terminals = available_terminals(varc, constants)
        non_terminals = available_non_terminals()
        # temporary 
        self.population = [Chromosome(self.max_depth, [grow,full], terminals, non_terminals) for _ in range(self.indc)]
        self.fitness(data)

    def evolution(self):
        target: Chromosome = self.population[0]
        sencond_parent = False

        new_pop: List[Chromosome] = []
        for _ in range(self.indc):

            ind = self.roulette()

            do_cross = random() <= self.pcross

            if do_cross:
                if not sencond_parent:
                    target = ind
                    sencond_parent = True

                else:
                    ind1 = deepcopy(target)
                    ind2 = deepcopy(ind)

                    gene1, idx1 = ind1.crossover_choice()
                    gene2, idx2 = ind2.crossover_choice()

                    aux = gene1.children[idx1]

                    gene1.children[idx1] = gene2.children[idx2]
                    gene2.children[idx2] = aux

                    new_md1 = calc_max_depth(gene1)
                    if  new_md1 > self.max_depth:
                        new_pop.append(target)
                    else:
                        ind1.depth = new_md1
                        new_pop.append(ind1)
                    
                    new_md2 = calc_max_depth(gene2)
                    if new_md2 > self.max_depth:
                        new_pop.append(ind)
                    else:
                        ind2.depth = new_md2
                        new_pop.append(ind2)
                    
                    sencond_parent = False

            else:
                new_pop.append(deepcopy(ind))

        if sencond_parent:
            new_pop.append(deepcopy(target))
            sencond_parent = False

        for nind in new_pop:
            do_mutate = random() <= self.pmutate
            if do_mutate:
                nind.mutate()

        self.population.clear()
        self.population = new_pop
        self.gen += 1

    
    def fitness(self, data: List[List[float]]):

        if len(data[0]) != self.varc + 1:
            raise Exception('Wrong Data Type')
        
        self.pop_fitness.clear()
        for ind in self.population:
            sum_squared_err = 0
            for vars in data:
                err = ind.root.eval(vars[:-1]) - vars[-1]
                squared_err = err**2
                sum_squared_err += squared_err
            
            mean_squared_err = sum_squared_err / self.indc

            self.pop_fitness.append(sqrt(mean_squared_err))
    
    def roulette(self) -> Chromosome:
        weights = [1 - (i/sum(self.pop_fitness)) for i in self.pop_fitness]
        return choices(self.population, weights=weights, k=1)[0]

    def stats(self):
        print(f'{self.gen},{max(self.pop_fitness):.3f},{sum(self.pop_fitness)/self.indc:.3f},{min(self.pop_fitness):.3f}')