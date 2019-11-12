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
        self.__parents = []
        self.__childs = []

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


    def set_population(self, population, type):
        self.__parents = []
        self.__stats = [x[1] for x in population]
        if type not in ['parents', 'childs']:
            raise ValueError( f'Type should be parents or childs - {type} ' )

        if type == 'parents':
            self.__stats = [x[1] for x in population]
            for p in population:
                self.__parents.append((self.__Bin__(p[0]), self.__f(p[1])))
            self.__parents.sort(key=takeSecond, reverse=True)
            #Am using Proportional selection to create a vector with candidates for selection
            avrFitness = sum([x[1] for x in self.__parents]) / len(self.__parents)
            self._selectionVector = []
            for i in range(len(self.__parents)):
                dm = divmod(self.__parents[i][1] / avrFitness, 1)
                tmp = []
                tmp.append(i)
                self._selectionVector = self._selectionVector + tmp * int((dm[0] + 1 if random.random() <= dm[1] else 0))
        elif type == 'childs':
            for p in population:
                self.__childs.append((self.__Bin__(p[0]), self.__f(p[1])))
            self.__childs.sort(key=takeSecond,reverse=True)

    def get_generation(self,N):
        res = [x[0] for x in (self.__childs+self.__parents)]
        res.sort(key=takeSecond,reverse=True)
        return res[:N]

    def get_childs(self):
        survivors = int(self.__s * len(self.__parents))
        childs = []

        i = 0
        while i <= survivors:
            r1 = random.choice(self._selectionVector)
            r2 = random.choice(self._selectionVector)
            if r1 != r2:
                kids = self.__crossover__(self.__parents[r1][0], self.__parents[r2][0])
                childs.append(kids[0])
                childs.append(kids[1])
                i += 1

        r1 = random.sample(range(len(childs)),int(len(childs)*0.01))
        for i in r1:
            childs[i] = self.__mutation__(childs[i])

        return [self.__Dec__(x)  for x in childs]

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
        return self.__parents[0]
    @property
    def get_fitness(self):
        return [x[1] for x in self.__parents]

    def get_avr_time(self):
        tmp = [x[1] for x in self.__stats]
        return sum(tmp)/len(tmp)

    def get_avr_len(self):
        tmp = [x[0] for x in self.__stats]
        return sum(tmp)/len(tmp)