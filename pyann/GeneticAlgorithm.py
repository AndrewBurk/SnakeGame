import random
import numpy as np

def take_third(elem):
    return elem[2]


class GeneticAlgorithm:
    def __init__(self, survivors, mutation, fitness, population_size):
        if survivors < 0 or survivors > 1:
            raise ValueError( f'Unit on survivors is %. Value should be in [0,1] - {survivors} ' )
        if mutation < 0 or mutation > 1:
            raise ValueError( f"Unit on mutation is %. Value should be in [0,1] -  {mutation}" )

        self.__s = survivors
        self.__m = mutation
        self.__f = fitness
        # structure of population
        # index 0 - chromosome
        # index 1 - parameter of ch(#of foods, time of live etc
        # index 2 - fitness
        self.__population = []
        self.__population_size = population_size
        self.__selectionVector = []

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

    def __set_selection_vector__(self):
        # Am using Proportional selection to create a vector with candidates for selection
        fitness = [x[2] for x in self.__population]
        avr_fitness =  np.average(fitness)
        # std = np.std(fitness)
        # mod_fitness = [1 + (x - avr_fitness) / (2 * std) for x in fitness]
        # sum_mod_fitness = sum(mod_fitness)
        self.__selectionVector.clear()
        tmp1 = []
        for i in range(len(self.__population)):
            dm = divmod((self.__f(self.__population[i][1])/ avr_fitness), 1)
            # dm = divmod(mod_fitness[i], 1)
            tmp1.clear()
            tmp1.append(i)
            self.__selectionVector.extend(tmp1 * int(dm[0] + (1 if random.random() <= dm[1] else 0)))

    def get_len_generation(self):
        return len(self.__population)

    def get_generation(self):
        return len(self.__population)

    # New code
    def crossover_mutation(self):
        survivors = int(self.__s * self.__population_size)
        childs = []
        self.__set_selection_vector__()
        i = 0
        while i < survivors:
            r1 = random.choice(self.__selectionVector)
            r2 = random.choice(range(self.__population_size - 1))
            if r1 != r2:
                kids = self.__crossover__(self.__population[r1][0], self.__population[r2][0], 3.5)
                childs.append(kids[0])
                childs.append(kids[1])
                i += 1

        r1 = random.sample(range(len(self.__population)),int(len(self.__population)*self.__m))
        for i in r1:
            childs.append(self.__mutation__(self.__population[i][0]))

        return childs

    def update_population(self, population):
        self.__population.clear()
        for p in population:
            # (chromosome, parameters, fitness
            self.__population.append((p[0],p[1], self.__f(p[1])))
        # print(f'update {len(self.__population)}')

    def add_population(self, population):
        for p in population:
            # (chromosome, parameters, fitness
            self.__population.append((p[0],p[1],self.__f(p[1])))

    def next_population(self):
        self.__population.sort(key=take_third,reverse=True)
        return self.__population[:self.__population_size]

    # NEw^^^
    def __crossover__(self, ch1, ch2, n = None):
        #ch1 = self.__Bin__(chromosome1)
        #ch2 = self.__Bin__(chromosome2)
        #if len(ch1) != len(ch2):
        #    raise ValueError( f'Len of the chromosomes should have the same len. chromosome1 -  {len(ch1)} ; chromosome2 - {len(ch2)}.' )
        #    # half of genome will be changed
        #r = random.randint(1,len(ch1)-1)
        #return self.__Dec__(ch1[:r] + ch2[r:]), self.__Dec__(ch2[:r] + ch1[r:])
        # SBX method

        if len(ch1) != len(ch2):
            raise ValueError( f'Len of the chromosomes should have the same len. chromosome1 -  {len(ch1)} ; chromosome2 - {len(ch2)}.')
        child1 = []
        child2 = []
        for i in range(len(ch1)):
            r = random.random()
            beta = (2*r) ** (1 / (1 + n)) if r <=0.5 else (1/(2 * (1 - r))) ** (1 / (1 + n))
            child1.append(0.5 * ((1 - beta) * ch1[i] + (1 + beta) * ch2[i]))
            child2.append(0.5 * ((1 - beta) * ch2[i] + (1 + beta) * ch1[i]))
        return child1, child2

    def __mutation__(self, ch):
        g = random.randint(0, len(ch) - 1)
        #ch = self.__Bin__(ch)
        #s = '0' if ch[g] == '1' else '1'
        #return self.__Dec__(s+ ch[1:]) if g == 0 else self.__Dec__(ch[:g - 1] + s + s[g + 1:])
        ch[g] += random.gauss(0, 0.5)
        return ch


    @property
    def get_fitness(self):
        return [x[2] for x in self.__population]

    def get_best_chromosome(self):
        index = [x[2] for x in self.__population].index(max(self.get_fitness))
        return self.__population[index][0], self.__population[index][2]

    def get_avr_time(self):
        tmp = [x[1][1] for x in  self.__population]
        return sum(tmp)/len(tmp)

    def get_max_time(self):
        tmp = [x[1][1] for x in  self.__population]
        return max(tmp)

    def get_max_len(self):
        tmp = [x[1][0] for x in  self.__population]
        return (max(tmp), tmp.count(max(tmp))),(max(tmp) -1 , tmp.count(max(tmp)-1)),(max(tmp) - 2 , tmp.count(max(tmp)-2))

    def get_avr_len(self):
        tmp = [x[1][0] for x in self.__population]
        return sum(tmp)/len(tmp)