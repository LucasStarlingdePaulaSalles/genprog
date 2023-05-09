from typing import List
from genprog.modules.chromosome import *
from genprog.modules.gene import *
from genprog.modules.population import Population
from csv import reader
import time

def main():
    start_time = time.time()

    data: List[List[float]] = []

    with open('data/datasets/synth2/synth2-train.csv') as csvfile:
        spamreader = reader(csvfile)

        for row in spamreader:

            a = [float(x) for x in row]
            data.append(a)
    
    pop = Population(7,100, len(data[0])-1, 0.9, 0.05, data)

    for _ in range(100):
        pop.evolution(2)
        pop.fitness(data)
        pop.stats()
    
    print("--- %s seconds ---" % (time.time() - start_time))


    
    
if __name__ == '__main__':
    main()
    