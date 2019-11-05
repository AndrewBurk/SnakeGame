from tkinter import Tk
import Game
import logging
import pyann


logger = logging.getLogger("mainApp")
logger.setLevel(logging.INFO)

# create the logging file handler
fh = logging.FileHandler("mainApp.log")

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

# add handler to logger object
logger.addHandler(fh)



SNAKE_COUNT = 2000
CUT_OFF = 0.6
WEIDTH = 800
HEIGHT = 800
SHAPE_NETURAL_NETWORK = (23, 8, 4)
ACTIVATION_FUNCTION = 'Th'
NumberOfGeneration = 1600

def fitness(par):
    l = par[0]
    t = par[1]
    d = par[2]
    return 4 * l + t - (t if par[2] == 'w' else t*0.5)/l if par[2] != '' else 0


def main():
        global N
        count_active_snakes = game1.get_active_snakes_count()
        if count_active_snakes != 0 and N <= NumberOfGeneration:
            # input()
            logger.info(f'Count of active snakes - {count_active_snakes}')

            game1.move()
            game1.change_direction(CUT_OFF)

            root.after(1, main)
        else:
            # game1.game_ower()
            learning.set_population(game1.get_population())
            f.write(f'Avr finess {round(sum(learning.get_fitness)/len(learning.get_fitness),2)} avr time {round(learning.get_avr_time(),2)} avr len {round(learning.get_avr_len(),4)};best gene:{learning.best_genes()}')
            print(f'Gen - {N}Avr finess {round(sum(learning.get_fitness)/len(learning.get_fitness),2)} avr time {round(learning.get_avr_time(),2)} avr len {round(learning.get_avr_len(),4)}')
            generation = learning.run()
            game1.clear_snakes()
            for g in generation:
                game1.add_snakes(1,(SHAPE_NETURAL_NETWORK, ACTIVATION_FUNCTION, True, g))

            N = N + 1
            if N <= NumberOfGeneration:
                root.after( 1, main )
            else:
                game1.game_ower()


# Setting up window
root = Tk()
root.title("PythonicWay Snake")

game1 = Game.Game(root, WEIDTH, HEIGHT)
logger.info(f"Created game field. WEIDTH = {WEIDTH} ;HEIGHT = {HEIGHT}")

game1.add_snakes(SNAKE_COUNT, (SHAPE_NETURAL_NETWORK, ACTIVATION_FUNCTION, True))
learning = pyann.GeneticAlgorithm(0.3, 0.2, fitness)
# game1.add_snakes(SNAKE_COUNT, 'HUMAN')
logger.info(f"Created SNAKE_COUNT {SNAKE_COUNT}")

f=open("stat.txt",'w+')

N=0
main()

root.mainloop()


# n1 = pyann.ArtificialNeuralNetwork((20,10, 8,4),'SIGMA',True)
# gene1 = n1.get_gene()
# n2 = pyann.ArtificialNeuralNetwork((20,10, 8,4),'SIGMA',True)
# n2.set_gene(gene1)
#
# print( f'len gene1 - {len(gene1[1])} = {len(n2.get_gene()[1])}')
# print(sum(gene1[1]-n2.get_gene()[1]))
# gene1[1][34] = 432
# print(sum(gene1[1]-n2.get_gene()[1]))
#
# print(gene1[1])
# print(n2.get_gene()[1])

