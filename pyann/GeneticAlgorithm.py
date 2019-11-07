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

    def __Bin__(self, v):
        # I assume that value will be from -1 to 1. e = 0.01
        # bin = (x - xmin)*(2^l-1)/(xmax-xmin)
        # from above x = bin * (xmax- xmin)/(2^l-1) + xmin; bin should be in dex
        # for e=0.01 l = 6
        min = -1
        max = 1
        res = ''
        for x in v:
            s = bin(int((x - min)*(2 ** 7 - 1)/(max - min))).replace('0b', '')
            for i in range(7 - len(s)):
                s = '0' + s
            res += s
        return res

    def __Dec__(self, s):
        min = -1
        max = 1
        res = []
        i = 0
        while i < len(s) - 7:
            x = min + int('0b'+s[i:i+7],2)*(max-min)/(2 ** 7 - 1)
            res.append(x)
            i += 7
        return res


    def set_population(self, population):
        self.__genes = []
        self.__stats = [x[1] for x in population]
        # added BIN code onto genes
        for p in population:
            self.__genes.append((self.__Bin__(p[0]), self.__f(p[1])))
        self.__genes.sort(key = takeSecond,reverse = True)

    def run(self):
        population = [x[0] for x in self.__genes]
        survivors = []
        deadList = []
        N = len(self.__genes)

        for i in range(int(self.__s*len(self.__genes))):
            survivors.append(population.pop(i))

        for i in range(int(self.__m*len(self.__genes))):
            deadList.append(population.pop(i))
        population.clear()
        population = deadList + survivors
        k = len(population)
        r1 = random.sample(range(len(survivors)),len(survivors))
        r2 = random.sample(range(len(survivors)),len(survivors))
        for (i, j) in ((i1, j2) for i1 in r1 for j2 in r2):
            k  += 2
            if k <= N:
                t = self.__crossover__(survivors[i], survivors[j])
                population.append(t[0])
                population.append(t[1])
            else:
                break

        r1 = random.sample(range(len(population)),int(len(population)*0.01))
        for i in r1:
            population[i] = self.__mutation__(population[i])

        return [self.__Dec__(x) for x in population]

    def __crossover__(self, gene1, gene2):
        if len(gene1) != len( gene2 ):
            raise ValueError( f'Len of the genes should be the same gene1 -  {len( gene1 )} ; gene2 - {len( gene2 )}.' )
            # half of genome will be changed
        r = random.randint(1,len(gene1)-1)
        return (gene1[:r] + gene2[r:],gene2[:r] + gene1[r:])


    def __mutation__(self, gene):
        r = random.randint(0, len(gene) - 1)
        s = '0' if gene[r] == '1' else '1'
        return s + gene[1:] if r == 0 else gene[:r - 1] + s + s[r + 1:]

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