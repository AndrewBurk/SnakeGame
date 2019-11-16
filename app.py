import Game
import pyann

SNAKE_COUNT = 500
CUT_OFF = 0.6
WEIDTH = 800
HEIGHT = 800
SHAPE_NETURAL_NETWORK = (15, 16, 8, 4)

ACTIVATION_FUNCTION = 'Th'
NumberOfGeneration = 1609

def fitness(par):
    l = par[0]
    t = par[1]
    d = par[2]
    c = par[3]
    return (75 * l * c + t - (t if d == 'w' else t*0.5) / (l - 2)) if d != 'c' else 75 * l + t



game1 = Game.Game(WEIDTH, HEIGHT, False)
game1.add_snakes(SNAKE_COUNT, (SHAPE_NETURAL_NETWORK, ACTIVATION_FUNCTION, True))
# game1.add_snakes(SNAKE_COUNT, 'HUMAN')
# game1.run()

learning = pyann.GeneticAlgorithm(0.2, 0.2, fitness, SNAKE_COUNT)
f = open("stat.txt",'w+')
# best_snakes = open("snake.txt",'W+')
# f.write(f'Generation    AvrFiness    AvrTime    AvrLen    BestGene')

for i in range(NumberOfGeneration):
    game1.run()
    learning.set_population(game1.get_population(),'parents')
    print(f'{i}  SumFiness {round(sum(learning.get_fitness),2)} avrTime {round(learning.get_avr_time(),2)} maxTime {learning.get_max_time()} avrLen {round(learning.get_avr_len(),4)} maxLen {learning.get_max_len()}')
    generation = learning.get_childs()
    f.write(f'\n{i}  SumFiness {round(sum(learning.get_fitness),2)} avrTime {round(learning.get_avr_time(),2)} maxTime {learning.get_max_time()} avrLen {round(learning.get_avr_len(),4)} maxLen {learning.get_max_len()}    \n {learning.best_chromosome()}')

    game1.clear_snakes()
    for g in generation:
        game1.add_snakes(1,(SHAPE_NETURAL_NETWORK, ACTIVATION_FUNCTION, True, g))
    game1.run(CUT_OFF)

    generation = []
    learning.set_population(game1.get_population(),"childs")
    generation = learning.get_generation()
    for g in generation:
        game1.add_snakes(1,(SHAPE_NETURAL_NETWORK, ACTIVATION_FUNCTION, True, g))
