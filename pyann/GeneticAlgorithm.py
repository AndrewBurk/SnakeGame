import random
from pyann import GAStrategies
import bisect

class Population(list):
    def __init__(self, fitness, l:list=None):
        self.fitness = fitness
        for el in l:
            super(Population, self).append((el[0], el[1], fitness(el[1])))
        # super(Population, self).extend(l)
        # self.sort_by_fitness()
    def __eq__(self, other):
        self.clear()

    def __add__(self, other):
        return Population(self.fitness, super(Population,self).__add__(other))

    def append(self, el) -> None:
        super(Population, self).append((el[0], el[1], self.fitness(el[1])))
        # self.sort_by_fitness()

    def extend(self, iterable) -> None:
        super(Population, self).extend([(x[0], x[1], self.fitness(x[1])) for x in iterable])
        # self.sort_by_fitness()

    def sort_by_fitness(self):
        self.sort(key=(lambda x: x[2]), reverse=True)

    def get_best_chromosome(self):
        fitness = [x[2] for x in self]
        index_max_fitness = fitness.index(max(fitness))
        return self[index_max_fitness][0]

    def get_sum_fitness(self):
        return sum([x[2] for x in self])

    def get_avr_time(self):
        tmp = [x[1][1] for x in self]
        return sum(tmp)/len(tmp)

    def get_max_time(self):
        tmp = [x[1][1] for x in self]
        return max(tmp), round(self[tmp.index(max(tmp))][2])

    def get_max_len(self):
        lens = [x[1][0] for x in self]
        s = ""
        for el in sorted(list(set(lens))):
            s += f'({el},  {lens.count(el)}) '
        return s

    def get_avr_len(self):
        tmp = [x[1][0] for x in self]
        return sum(tmp)/len(tmp)

    # def get_len_generation(self):
    #     return len(self)

    def count_death(self):
        d = [x[1][2] for x in self]
        return ('w', d.count('w')), ('c', d.count('c')), ('s', d.count('s'))

class GeneticAlgorithm:
    def __init__(self, population: Population, survivors, crossover: GAStrategies, mutation: GAStrategies):
        self.__population = population
        self.__s = survivors
        self.__crossover = crossover
        self.__mutation = mutation
        self.__population_size = len(population)

    def __get_selection_vector(self):
        # Am using Proportional selection to create a vector with candidates for selection
        tmp1, selection_vector = [], []
        sum_fitness = self.__population.get_sum_fitness()
        for i in range(len(self.__population)):
            dm = divmod((self.__population.get_fitness(i) / sum_fitness) * 100, 1)
            tmp1.clear()
            tmp1.append(i)
            selection_vector.extend(tmp1 * int(dm[0] + (1 if random.random() <= dm[1] else 0)))
        random.shuffle(selection_vector)
        return selection_vector

    def __roulette_wheel_selection(self, num_individuals: int):
        selection = []
        wheel = self.__population.get_sum_fitness()
        for _ in range(num_individuals):
            pick = random.uniform(0, wheel)
            current = 0
            for (i, individual) in enumerate(self.__population):
                current += individual[2]
                if current > pick:
                    selection.append(individual[0])
                    break
        return selection

    def add_population(self, individuals):
        self.__population.extend(individuals)
        self.__population.sort_by_fitness()
        self.__population = Population(self.__population.fitness, self.__population[:self.__population_size])
        random.shuffle(self.__population)

    def get_childs(self) -> list:
        result = []
        i = 0
        r = self.__roulette_wheel_selection(500)
        while len(result) <= self.__s * self.__population_size:
            ch1 = r[random.randint(0,499)]
            ch2 = r[random.randint(0, 499)]
            kids = self.__crossover[random.randint(0,len(self.__crossover) - 1)].run(ch1, ch2)
            result.append(self.__mutation[i % len(self.__mutation)].run(kids[0]))
            result.append(self.__mutation[i % len(self.__mutation)].run(kids[1]))
            i += 1
        return result

    def get_population(self):
        return self.__population

#
#
#
# class GeneticAlgorithm:
#     def __init__(self, survivors, mutation, fitness, population_size):
#         if survivors < 0 or survivors > 1:
#             raise ValueError( f'Unit on survivors is %. Value should be in [0,1] - {survivors} ' )
#         if mutation < 0 or mutation > 1:
#             raise ValueError( f"Unit on mutation is %. Value should be in [0,1] -  {mutation}" )
#
#         self.__s = survivors
#         self.__m = mutation
#         self.__f = fitness
#         # structure of population
#         # index 0 - chromosome
#         # index 1 - parameter of ch(#of foods, time of live etc
#         # index 2 - fitness
#         self.__population = []
#         self.__population_size = population_size
#         self.__selectionVector = []
#     def __Bin__(self, v):
#         # I assume that value will be from -1 to 1. e = 0.01
#         # bin = (x - xmin)*(2^l-1)/(xmax-xmin)
#         # from above x = bin * (xmax- xmin)/(2^l-1) + xmin; bin should be in dex
#         # for e=0.01 l = 6
#         min = -1
#         max = 1
#         res = ''
#         for x in v:
#             s = bin(int((x - min)*(2 ** 7 - 1)/(max - min))).replace('0b', '')
#             for i in range(7 - len(s)):
#                 s = '0' + s
#             res += s
#         return res
#     def __Dec__(self, s):
#         min = -1
#         max = 1
#         res = []
#         i = 0
#         while i < len(s) - 7:
#             x = min + int('0b'+s[i:i+7],2)*(max-min)/(2 ** 7 - 1)
#             res.append(x)
#             i += 7
#         return res
#     def __set_selection_vector__(self):
#         # Am using Proportional selection to create a vector with candidates for selection
#         fitness = [x[2] for x in self.__population]
#         avr_fitness =  np.average(fitness)
#         # std = np.std(fitness)
#         # mod_fitness = [1 + (x - avr_fitness) / (2 * std) for x in fitness]
#         # sum_mod_fitness = sum(mod_fitness)
#         self.__selectionVector.clear()
#         tmp1 = []
#         while len(self.__selectionVector) < int(self.__s * self.__population_size):
#             for i in range(len(self.__population)):
#                 dm = divmod((self.__population[i][2]/sum(fitness)) * 100, 1)
#                 # dm = divmod(mod_fitness[i], 1)
#                 tmp1.clear()
#                 tmp1.append(i)
#                 self.__selectionVector.extend(tmp1 * int(dm[0] + (1 if random.random() <= dm[1] else 0)))
#     # New code
#     def crossover_mutation(self):
#         childs = []
#         self.__set_selection_vector__()
#         i = 0
#         for r1 in self.__selectionVector:
#             #r1 = random.choice(self.__selectionVector)
#             r2 = random.choice(range(self.__population_size))
#             if r1 != r2:
#                 if i % 2 == 0:
#                     kids = self.__crossover__(self.__population[r1][0], self.__population[r2][0], 'sbx', 50)
#                     childs.append(kids[0])
#                     childs.append(kids[1])
#                 elif i % 2 == 1:
#                     kids = self.__crossover__(self.__population[r1][0], self.__population[r2][0], 'Lbin')
#                     childs.append(kids[0])
#                     childs.append(kids[1])
#                 #else:
#                 #    kids = self.__crossover__(self.__population[r1][0], self.__population[r2][0], 'bin')
#                 #    childs.append(kids[0])
#                 #    childs.append(kids[1])
#             i += 1
#
#         r1 = random.sample(self.__population,int(self.__population_size * self.__m))
#         for p in r1:
#             childs.append(self.__mutation__(p[0]))
#
#         return childs + self.__population
#
#     def update_population(self, population):
#         self.__population.clear()
#         for p in population:
#             # (chromosome, parameters, fitness
#             self.__population.append((p[0], p[1], self.__f(p[1])))
#         # print(f'update {len(self.__population)}')
#
#     def add_population(self, population):
#         for p in population:
#             # (chromosome, parameters, fitness
#             self.__population.append((p[0], p[1], self.__f(p[1])))
#
#     def next_population(self):
#         self.__population.sort(key=take_third,reverse=True)
#         return self.__population[:self.__population_size]
#     # NEw^^^
#     def __crossover__(self, ch1, ch2, type = 'SBX', n = None):
#         if len(ch1) != len(ch2):
#             raise ValueError( f'Len of the chromosomes should have the same len. chromosome1 -  {len(ch1)} ; chromosome2 - {len(ch2)}.')
#         if type.upper() == 'BIN':
#             ch1_b = self.__Bin__(ch1)
#             ch2_b = self.__Bin__(ch2)
#             # half of genome will be changed
#             r = random.randint(1,len(ch1)-1)
#             return self.__Dec__(ch1_b[:r] + ch2_b[r:]), self.__Dec__(ch2_b[:r] + ch1_b[r:])
#         elif type.upper() == 'LBIN':
#             ch1_b = self.__Bin__(ch1)
#             ch2_b = self.__Bin__(ch2)
#             kid1, kid2 = ch1_b , ch2_b
#             for i in range(len(ch1_b) - 1):
#                 if i % 2 == 0:
#                     kid2 = kid2[:i] + ch1_b[i] + kid2[i + 1:] if i else kid2 = ch1_b[i] + kid2[i+1:]
#                 else:
#                     kid1 = kid1[:i] + ch2_b[i] + kid1[i+1:]
#             return self.__Dec__(kid1), self.__Dec__(kid2)
#         elif type.upper() == 'SBX':
#             child1 = []
#             child2 = []
#             for i in range(len(ch1)):
#                 r = random.random()
#                 beta = (2*r) ** (1 / (1 + n)) if r <= 0.5 else (1/(2 * (1 - r))) ** (1 / (1 + n))
#                 child1.append(0.5 * ((1 - beta) * ch1[i] + (1 + beta) * ch2[i]))
#                 child2.append(0.5 * ((1 - beta) * ch2[i] + (1 + beta) * ch1[i]))
#             return child1, child2
#
#     def __mutation__(self, ch):
#         g = random.randint(0, len(ch) - 1)
#         #ch = self.__Bin__(ch)
#         #s = '0' if ch[g] == '1' else '1'
#         #return self.__Dec__(s+ ch[1:]) if g == 0 else self.__Dec__(ch[:g - 1] + s + s[g + 1:])
#         ch[g] = min(ch[g] + random.gauss(0, 0.25), 1)
#         return ch
#
#     def get_len_generation(self):
#         return len(self.__population)
#
#     def get_generation(self):
#         return len(self.__population)
#
#     def get_fitness(self):
#         return [x[2] for x in self.__population]
#

