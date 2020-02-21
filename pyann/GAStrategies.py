from abc import ABC, abstractmethod
import random
import numpy as np
def clip(x,a,b):
    if x < a:
        return a
    elif x > b:
        return b
    else:
        return x

class CrossoverMutation(ABC):
    def __init__(self):
        self.__min = -1
        self.__max = 1
        self.__e = 25

    def __Bin__(self, v):
        # I assume that value will be from -1 to 1. e = 0.01
        # bin = (x - xmin)*(2^l-1)/(xmax-xmin)
        # from above x = bin * (xmax- xmin)/(2^l-1) + xmin; bin should be in dex
        # for e=0.01 l = 6
        res = ''
        for x in v:
            s = bin(int((x - self.__min)*(2 ** self.__e - 1)/(self.__max - self.__min))).replace('0b', '')
            for i in range(self.__e - len(s)):
                s = '0' + s
            res += s
        return res

    def __Dec__(self, s):
        res = []
        i = 0
        while i <= len(s) - self.__e:
            x = self.__min + int('0b' + s[i: i + self.__e], 2)*(self.__max - self.__min)/(2 ** self.__e - 1)
            res.append(x)
            i += self.__e
        return res

    @abstractmethod
    def run(self, ch1, ch2):
        pass

class GaussianMutation(CrossoverMutation):
    def __init__(self, prop_gen_mutation=0.05, prop_mutation_occurs=1, mu=0, sigma=0.45):
        self.__mu = mu
        self.__sigma = sigma
        self.__prop_gen_mutation = prop_gen_mutation
        self.__prop_mutation_occurs = prop_mutation_occurs

    def run(self, ch1, ch2 = None):
        if random.random() < self.__prop_mutation_occurs:
            for i in range(len(ch1)):
                if random.random() < self.__prop_gen_mutation:
                    ch1[i] = clip((ch1[i] + random.gauss(self.__mu, self.__sigma) * 0.2), -1., 1.)
        return ch1

class BinaryMutation(CrossoverMutation):
    def __init__(self, prop_gen_mutation=0.05, prop_mutation_occurs=1):
        self.__prop_gen_mutation = prop_gen_mutation
        self.__prop_mutation_occurs = prop_mutation_occurs
        super().__init__()

    def run(self, ch1, ch2 = None):
        if random.random() < self.__prop_mutation_occurs:
            ch1_b = self.__Bin__(ch1)
            for i in range(len(ch1_b)):
                if random.random() < self.__prop_gen_mutation:
                    s = '0' if ch1_b[i] == '1' else '1'
                    ch1_b = ch1_b[:i] + s + ch1_b[i+1:]
            return self.__Dec__(ch1_b)
        else:
            return ch1


class SBX(CrossoverMutation):
    """simulated binary crossover"""
    def __init__(self, eta=100):
        self.__eta = eta

    def run(self, ch1: np.ndarray, ch2: np.ndarray):
        if len(ch1) != len(ch2):
            raise ValueError(f'Len of chromosomes should have the same len. chromosome1 -  {len(ch1)} ; chromosome2 - {len(ch2)}.')

        if max(ch1) > 1 or min(ch1) < -1 or max(ch2) > 1 or min(ch2) < -1:
            raise ValueError(f'Blya!!')

        r = np.random.random(ch1.shape)
        beta = np.empty(ch1.shape)
        beta[r <= 0.5] = (2 * r[r <= 0.5]) ** (1 / (1 + self.__eta))
        beta[r > 0.5]  = (1 / (2 * (1 - r[r > 0.5]))) ** (1 / (1 + self.__eta))
        child1 = 0.5 * ((1 - beta) * ch1 + (1 + beta) * ch2)
        child2 = 0.5 * ((1 - beta) * ch2 + (1 + beta) * ch1)

        return np.clip(child1, -1., 1.), np.clip(child2, -1., 1.)

class MPBX(CrossoverMutation):
    """multi point binary crossover"""
    def __init__(self):
        super().__init__()

    def run(self, ch1, ch2):
        ch1_b = self.__Bin__(ch1)
        ch2_b = self.__Bin__(ch2)
        child1, child2 = ch1_b, ch2_b
        for i in range(len(ch1_b) - 1):
            if i % 2 == 0:
                child2 = child2[:i] + ch1_b[i] + child2[i + 1:] if i else ch1_b[i] + child2[i + 1:]
            else:
                child1 = child1[:i] + ch2_b[i] + child1[i + 1:]
        return self.__Dec__(child1), self.__Dec__(child2)

class SPBX_BIN(CrossoverMutation):
    """single point binary crossover"""
    def __init__(self):
        super().__init__()

    def run(self, ch1, ch2):
        ch1_b = self.__Bin__(ch1)
        ch2_b = self.__Bin__(ch2)
        # half of genome will be changed
        r = random.randint(1,len(ch1)-1)
        return self.__Dec__(ch1_b[:r] + ch2_b[r:]), self.__Dec__(ch2_b[:r] + ch1_b[r:])

class SPBX(CrossoverMutation):
    def run(self, ch1, ch2):
        r = random.randint(1,len(ch1)-1)
        return np.concatenate((ch1[:r],ch2[r:])), np.concatenate((ch2[:r], ch1[r:]))

