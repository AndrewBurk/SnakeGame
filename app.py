import Game
import pyann

SNAKE_COUNT = 2000
SNAKE_COUNT = 10
CUT_OFF = 0.6
WEIDTH = 800
HEIGHT = 800
SHAPE_NETURAL_NETWORK = (23, 8, 4)
ACTIVATION_FUNCTION = 'Th'
NumberOfGeneration = 16

def fitness(par):
    l = par[0]
    t = par[1]
    d = par[2]
    return 4 * l + t - (t if par[2] == 'w' else t*0.5)/l



game1 = Game.Game(WEIDTH, HEIGHT)
game1.add_snakes(SNAKE_COUNT, (SHAPE_NETURAL_NETWORK, ACTIVATION_FUNCTION, True))


learning = pyann.GeneticAlgorithm(0.3, 0.2, fitness)

for i in range(NumberOfGeneration):
    game1.run()
    learning.set_population(game1.get_population())
    print(f'Gen - {i}Avr finess {round(sum(learning.get_fitness)/len(learning.get_fitness),2)} avr time {round(learning.get_avr_time(),2)} avr len {round(learning.get_avr_len(),4)}')
    generation = learning.run()
    game1.clear_snakes()
    for g in generation:
        game1.add_snakes(1,(SHAPE_NETURAL_NETWORK, ACTIVATION_FUNCTION, True, g))
