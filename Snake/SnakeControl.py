from abc import ABC, abstractmethod
import random
import numpy as np
from pyann import ArtificialNeuralNetwork
direction = ('Down', 'Right', 'Up','Left')

class  Direction(ABC):
    """To do"""
    @abstractmethod
    def get_direction(self, *args):
        pass

class RandomMove(Direction):
    def get_direction(self, *args):
        return direction[random.randint(0, 2)]

class HumanMove(Direction):
    def get_direction(self, *args):
        # if event.keysym in self.mapping:
        #     self.vector = self.mapping[event.keysym]
        dir = {"w":2, "s":0, "d":1, "a":3}
        try:
            a = (input("Enter direction: "))
            if a not in ('w', 's', 'a', 'd'):
                raise ValueError("Value should be in [0;3].")
            print(dir[a])
            return direction[dir[a]]
        except ValueError:
            print("Please enter number.")

class ANNMove(Direction):
    def __init__(self, cut_off, *ann_setup):
        self.brain = ArtificialNeuralNetwork(*ann_setup)
        self.__cut_off = cut_off

    def get_direction(self, *args):
        #d = [0 if x < self.__cut_off else 1 for x in self.brain.run(*args)]
        #if sum(d) == 1:
        return direction[np.argmax(self.brain.run(*args))]
        #else:
        #    return 'Continue'

    # TODO move it into snake class
    def get_chromosome(self):
        return self.brain.get_chromosome()

    def set_chromosome(self, ch):
        return self.brain.set_chromosome(ch)
