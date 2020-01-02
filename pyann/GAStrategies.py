from abc import ABC, abstractmethod
import random

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

    def __Bin__(self, v):
        # I assume that value will be from -1 to 1. e = 0.01
        # bin = (x - xmin)*(2^l-1)/(xmax-xmin)
        # from above x = bin * (xmax- xmin)/(2^l-1) + xmin; bin should be in dex
        # for e=0.01 l = 6
        res = ''
        for x in v:
            s = bin(int((x - self.__min)*(2 ** 7 - 1)/(self.__max - self.__min))).replace('0b', '')
            for i in range(7 - len(s)):
                s = '0' + s
            res += s
        return res

    def __Dec__(self, s):
        res = []
        i = 0
        while i < len(s) - 7:
            x = self.__min + int('0b' + s[i: i + 7], 2)*(self.__max - self.__min)/(2 ** 7 - 1)
            res.append(x)
            i += 7
        return res

    @abstractmethod
    def run(self, ch1, ch2):
        pass

class GaussianMutation(CrossoverMutation):
    def __init__(self,mu = 0, sigma = 0.45):
        self.__mu = mu
        self.__sigma = sigma

    def run(self, ch1, ch2 = None):
        i = random.randint(0, len(ch1) - 1)
        ch1[i] = clip(ch1[i] + random.gauss(self.__mu, self.__sigma), -1., 1.)
        return ch1

class BinaryMutation(CrossoverMutation):
    def run(self, ch1, ch2 = None):
        ch1_b = self.__Bin__(ch1)
        i = random.randint(0, len(ch1_b) - 1)
        s = '0' if ch1_b[i] == '1' else '1'
        return self.__Dec__(s + ch1_b[1:]) if i == 0 else self.__Dec__(ch1_b[:i - 1] + s + ch1_b[i:])


class SBX(CrossoverMutation):
    """simulated binary crossover"""
    def __init__(self, n = 100):
        self.__n = n
    def run(self, ch1, ch2, **param):
        if len(ch1) != len(ch2):
            raise ValueError(f'Len of chromosomes should have the same len. chromosome1 -  {len(ch1)} ; chromosome2 - {len(ch2)}.')
        child1 = []
        child2 = []

        if max(ch1) > 1 or min(ch1) < -1 or max(ch2) > 1 or min(ch2) < -1 :
            raise ValueError(f'Blya!!')

        for i in range(len(ch1)):
            r = random.random()
            beta = (2 * r) ** (1 / (1 + self.__n)) if r <= 0.5 else (1 / (2 * (1 - r))) ** (1 / (1 + self.__n))
            child1.append(clip(0.5 * ((1 - beta) * ch1[i] + (1 + beta) * ch2[i]), -1., 1.))
            child2.append(clip(0.5 * ((1 - beta) * ch2[i] + (1 + beta) * ch1[i]), -1., 1.))
        return child1, child2

class LBIN(CrossoverMutation):
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

class SPBX(CrossoverMutation):
    """single point binary crossover"""
    def run(self, ch1, ch2):
            ch1_b = self.__Bin__(ch1)
            ch2_b = self.__Bin__(ch2)
            # half of genome will be changed
            r = random.randint(1,len(ch1)-1)
            return self.__Dec__(ch1_b[:r] + ch2_b[r:]), self.__Dec__(ch2_b[:r] + ch1_b[r:])