from typing import List, Dict
from genprog.modules.chromosome import *
from genprog.modules.gene import *
from genprog.modules.population import Population
from random import seed
from csv import reader
import time
import argparse as ap

def main():

    parser = ap.ArgumentParser(
                    description='Genetic programming implementation by Lucas Starling')

    parser.add_argument('filename')           
    parser.add_argument('selection')      # roulette, tournament, lexicase, random
    parser.add_argument('population')     # 50, 100, 500
    parser.add_argument('generation')     # 50, 100, 500
    parser.add_argument('cross_prob')     # 0.9, 0.6
    parser.add_argument('mutate_prob')    # 0.05, 0.3
    parser.add_argument('-e', '--elitism')
    parser.add_argument('-rs', '--random_seed')

    args = parser.parse_args()
    print(args)

    start_time = time.time()

    data: List[List[float]] = []

    with open(args.filename) as csvfile:
        spamreader = reader(csvfile)

        for row in spamreader:

            a = [float(x) for x in row]
            data.append(a)

    max_stat = {}
    mean_stat = {}
    min_stat = {}
    cross_improvec_stat = {}
    cross_worsenc_stat = {}
    unique_stat = {}

    if args.elitism == None:
        elitism = 0
    else:
        elitism = int(args.elitism)

    for i in range(int(args.generation)):
        max_stat[i+1] = []
        mean_stat[i+1] = []
        min_stat[i+1] = []
        cross_improvec_stat[i+1] = []
        cross_worsenc_stat[i+1] = []
        unique_stat[i+1] = []

    for i in range(30):
        if args.random_seed:
            seed(int(args.random_seed)+i)

        pop = Population(7, int(args.population), len(data[0])-1, float(args.cross_prob), float(args.mutate_prob), data)
        for j in range(int(args.generation)):
            pop.evolution(elitism,'tournament')
            pop.fitness(data)
            max, mean, min, cross_improvec, cross_worsenc, unique = pop.stats()
            max_stat[j+1].append(max)
            mean_stat[j+1].append(mean)
            min_stat[j+1].append(min)
            cross_improvec_stat[j+1].append(cross_improvec)
            cross_worsenc_stat[j+1].append(cross_worsenc)
            unique_stat[j+1].append(unique)

    
    print('max,mean,min,cross_improvec,cross_worsenc,unique')
    for i in range(int(args.generation)):
        gmax = sum(max_stat[i+1])/len(max_stat[i+1])
        gmean = sum(mean_stat[i+1])/len(mean_stat[i+1])
        gmin = sum(min_stat[i+1])/len(min_stat[i+1])
        gcross_improvec = sum(cross_improvec_stat[i+1])/len(cross_improvec_stat[i+1])
        gcross_worsenc = sum(cross_worsenc_stat[i+1])/len(cross_worsenc_stat[i+1])
        gunique = sum(unique_stat[i+1])/len(unique_stat[i+1])
        print(f'{i+1},{gmax:.3f},{gmean:.3f},{gmin:.3f},{gcross_improvec:.3f},{gcross_worsenc:.3f},{gunique:.3f}')


    print("--- %s seconds ---" % (time.time() - start_time))

    print(min_stat[50])


    
    
if __name__ == '__main__':
    main()
    