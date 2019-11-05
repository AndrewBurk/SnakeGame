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
        result = []
        survivors = int(self.__s*len(self.__genes)) + 1
        randomIndexes = random.sample(range(len(self.__genes)), survivors)
        for i in range(survivors):
            result.append(self.__crossover__(self.__genes[i][0], self.__genes[randomIndexes[i]][0]))


        r = int(self.__m*len(self.__genes)) + 1
        randomIndexes = random.sample(range(len(self.__genes)-survivors), r)
        for i in randomIndexes:
            result.append(self.__mutation__(self.__genes[i+survivors][0]))

        r = len(self.__genes) - int(self.__m*len(self.__genes))  - int(self.__s*len(self.__genes)) - 2


        for i in range(r):
            result.append(self.__genes[i][0])
        # print(f'len of res - {len(result)}')

        return result

    def __crossover__(self, gene1, gene2):
        if len(gene1) != len( gene2 ):
            raise ValueError( f'Len of the genes should be the same gene1 -  {len( gene1 )} ; gene2 - {len( gene2 )}.' )
            r = random.randint(0,len(gene1))
            indexes_gene1 = random.sample(range(len(gene1)), r)

            for i in range(r):
                gene1[indexes_gene1[i]] = gene2[indexes_gene1[i]]
        return gene1


    def __mutation__(self, gene):

        r = random.randint(0, len(gene))
        randomIndexes = random.sample(range(len(gene)), r)
        for i in randomIndexes:
            gene[i] += 2 * random.random() - 1


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

