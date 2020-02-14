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
        while len(result) <= self.__s * self.__population_size:
            ch = r = self.__roulette_wheel_selection(2)
            kids = self.__crossover[random.randint(0,len(self.__crossover) - 1)].run(ch[0], ch[1])
            result.append(self.__mutation[i % len(self.__mutation)].run(kids[0]))
            result.append(self.__mutation[i % len(self.__mutation)].run(kids[1]))
            i += 1
        return result

    def get_population(self):
        return self.__population
