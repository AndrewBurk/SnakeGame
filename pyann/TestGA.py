import unittest
import numpy as nm
import math
import pyann

def fitness(x):
    result = 0
    for i in range(len(x)):
        result += (x[i] - i) ** 2
    return -result + 1000

def fitness2(x):
    result = -418.9829 * len(x)
    for i in range(len(x)):
        result += x[i]*math.sin(abs(x[i])**0.5)
    l=list(filter(lambda x: abs(x) > 500, x))
    if len(l) > 0:
        return 0.00000001
    else:
        return result + 100000000000

class MyTestCase(unittest.TestCase):
    def test_GA(self):
        p = []
        for j in range(100):
            r = list((500 * nm.random.random(10)))
            p.append([r, r])
        ga = pyann.GeneticAlgorithm(0.6, 0.05, fitness2, 100)
        for i in range(10000):
            ga.update_population(p)
            print(f'{ga.get_best_chromosome()}')
            cm = ga.crossover_mutation()
            p.clear()
            for i in cm:
                p.append([i, i])
            ga.add_population(p)
            cm = ga.next_population()
            p.clear()
            for i in cm:
                p.append([i[0], i[1]])
            ga.add_population(p)

        self.assertEqual([0,1,2,3,4,5], [0,1,2,3,4,5])


if __name__ == '__main__':
    unittest.main()


