import numpy as np
import random

def takeSecond(elem):
    return elem[1]


class GeneticAlgorithm:
    def __init__(self, mutation, survivors, fitness):
        if survivors < 0 or survivors > 1:
            raise ValueError( f'Unit on survivors is %. Value should be in [0,1] - {survivors} ' )
        if mutation < 0 or mutation > 1:
            raise ValueError( f"Unit on mutation is %. Value should be in [0,1] -  {mutation}" )

        self.__s = survivors
        self.__m = mutation
        self.__f = fitness
        self.__genes = []

    def set_population(self, population):
        self.__genes = []
        self.__stats = [x[1] for x in population]
        for p in population:
            self.__genes.append((np.array(p[0]), self.__f(p[1])))
        self.__genes.sort(key = takeSecond,reverse = True)

    def run(self):
        population = [x[0] for x in self.__genes]
        survivors = []
        deadList = []
        N = len(self.__genes)

        for i in range(int(self.__s*len(self.__genes)) + 1):
            survivors.append(population.pop(i))

        for i in range(int(self.__m*len(self.__genes)) + 1):
            deadList.append(population.pop(i))
        population.clear()
        population = deadList + survivors
        k = len(population)
        z=0
        r1 = random.sample(range(len(survivors)),len(survivors))
        r2 = random.sample(range(len(deadList)),len(deadList))
        for (i, j) in ((i1, j2) for i1 in r1 for j2 in r2):
            k  += 1
            if k <= N:
                population.append(self.__crossover__(survivors[i], deadList[j]))
                z +=1
            else:
                break
        return self.__mutation__(population)

    def __crossover__(self, gene1, gene2):
        if len(gene1) != len( gene2 ):
            raise ValueError( f'Len of the genes should be the same gene1 -  {len( gene1 )} ; gene2 - {len( gene2 )}.' )
            # half of genome will be changed
            indexes_gene1 = random.sample(range(len(gene1) - 1), int(len(gene1) / 2))
            for i in range(r):
                gene1[indexes_gene1[i]] = gene2[indexes_gene1[i]]
        return gene1


    def __mutation__(self, gene):

        r = random.randint(0, int(len(gene) / 2) - 1)
        randomIndexes = random.sample(range(int(len(gene) / 2) - 1), r)
        for i in randomIndexes:
            gene[i + int(len(gene) / 2)] += 2 * random.random() - 1
        return gene

    def best_genes(self):
        return self.__genes[0]
    @property
    def get_fitness(self):
        return [x[1] for x in self.__genes]

    def get_avr_time(self):
        tmp = [x[1] for x in self.__stats]
        return sum(tmp)/len(tmp)

    def get_avr_len(self):
        tmp = [x[0] for x in self.__stats]
        return sum(tmp)/len(tmp)

