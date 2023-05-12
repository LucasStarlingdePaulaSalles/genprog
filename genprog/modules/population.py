from copy import deepcopy
from typing import List
from random import choices, random, sample
from genprog.modules.gene import available_non_terminals, available_terminals, calc_max_depth
from genprog.modules.chromosome import Chromosome, grow, full
from math import inf 


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
        self.crossc = 0
        self.cross_improvc = 0
        self.unique: set[str] = set()

        terminals = available_terminals(varc, constants)
        non_terminals = available_non_terminals()
        
        self.population = [Chromosome(self.max_depth, [grow,full], terminals, non_terminals) for _ in range(self.indc)]
        self.fitness(data)
        self.mean_fitness = sum(self.pop_fitness)/len(self.pop_fitness)

    def evolution(self, elite: int = 0, selection: str = 'roulette'):
        target: Chromosome = self.population[0]
        sencond_parent = False
        self.crossc = 0
        self.cross_improvc = 0
        self.unique = set()
        new_pop: List[Chromosome] = []

        def fit_sort(ind: Chromosome):
            return ind.fit_val

        for ind in sorted(self.population, key=fit_sort)[:elite]:
            new_pop.append(deepcopy(ind))

        for _ in range(self.indc-elite):

            if selection == 'roulette':
                ind = self.roulette()
            elif selection == 'tournament':
                ind = self.tournament()
            elif selection == 'lexicase':
                ind = self.lexicase()
            elif selection == 'random':
                ind = self.random()
            else:
                raise Exception('Invalid selector')

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

                    ind1.update_fenotype()
                    ind1.fitness(self.data)
                    ind2.update_fenotype()
                    ind2.fitness(self.data)

                    mean_p_fit = (target.fit_val + ind.fit_val)/2

                    new_md1 = calc_max_depth(gene1)
                    if  new_md1 > self.max_depth:
                        new_pop.append(deepcopy(target))
                        self.unique.add(target.fenotype)
                    else:
                        if new_md1 > ind1.depth: ind1.depth = new_md1
                        self.crossc += 1
                        if ind1.fit_val < mean_p_fit:
                            self.cross_improvc += 1
                        
                        new_pop.append(ind1)
                        self.unique.add(ind1.fenotype)

                    
                    new_md2 = calc_max_depth(gene2)
                    if new_md2 > self.max_depth:
                        new_pop.append(deepcopy(ind))
                        self.unique.add(ind.fenotype)
                    else:
                        if new_md2 > ind2.depth: ind2.depth = new_md2
                        self.crossc += 1
                        if  ind2.fit_val < mean_p_fit:
                            self.cross_improvc += 1
                        
                        new_pop.append(ind2)
                        self.unique.add(ind2.fenotype)
                    
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
                new_md = calc_max_depth(nind.root)
                if new_md > nind.depth: nind.depth = new_md

        self.population.clear()
        self.population = new_pop
        self.indc = len(new_pop)
        self.gen += 1

    
    def fitness(self, data: List[List[float]]):

        if len(data[0]) != self.varc + 1:
            raise Exception('Wrong Data Type')
        
        self.pop_fitness.clear()
        for ind in self.population:
            rmse = ind.fitness(data)
            self.pop_fitness.append(rmse)
        
        self.mean_fitness = sum(self.pop_fitness)/len(self.pop_fitness)
    
    def random(self) -> Chromosome:
        return choices(self.population, k=1)[0]

    def roulette(self) -> Chromosome:
        weights = [1 - (i/sum(self.pop_fitness)) for i in self.pop_fitness]
        return choices(self.population, weights=weights, k=1)[0]

    def tournament(self) -> Chromosome:
        tournament = sample(range(self.indc), k=2)
        idx = tournament[0]
        if self.pop_fitness[tournament[1]] < self.pop_fitness[idx]:
            idx = tournament[1]

        return self.population[idx]

    def lexicase(self) -> Chromosome:
        cases =  sample(range(len(self.data)), len(self.data))
        candidates = [x for x  in range(len(self.population))]

        while len(cases) > 0 and len(candidates) > 1:
            case_idx = cases.pop()
            
            best_fit = inf
            case_candidates = []
        
            for candidate_idx in candidates:
                fit = self.population[candidate_idx].fitness([self.data[case_idx]], False)

                if fit < best_fit:
                    best_fit = fit
                    case_candidates = [candidate_idx]

                elif fit == best_fit:
                    case_candidates.append(candidate_idx)
            

            candidates = case_candidates
        
        if len(candidates) > 1:
            return self.population[choices(candidates,k=1)[0]]
        
        return self.population[candidates[0]]

    def stats(self):
        return max(self.pop_fitness), self.mean_fitness, min(self.pop_fitness), self.cross_improvc, self.crossc-self.cross_improvc, self.indc-len(self.unique)
    
    def print_stats(self):
        print(f'{self.gen},{max(self.pop_fitness):.3f},{self.mean_fitness:.3f},{min(self.pop_fitness):.3f},{self.indc-len(self.unique)}')