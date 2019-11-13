import Game
import pyann

SNAKE_COUNT = 2000
CUT_OFF = 0.6
WEIDTH = 800
HEIGHT = 800
SHAPE_NETURAL_NETWORK = (15, 8, 8, 4)

ACTIVATION_FUNCTION = 'Th'
NumberOfGeneration = 1609

def fitness(par):
    l = par[0]
    t = par[1]
    d = par[2]
    c = par[3]
    return 50 * l + t + par[3] * 8 - (t + 7 * par[3] if par[2] == 'w' else (t + 8 * par[3])*0.5) / (l - 2)



game1 = Game.Game(WEIDTH, HEIGHT, False)
game1.add_snakes(SNAKE_COUNT, (SHAPE_NETURAL_NETWORK, ACTIVATION_FUNCTION, True))
# game1.add_snakes(SNAKE_COUNT, 'HUMAN')
# game1.run()

learning = pyann.GeneticAlgorithm(0.1, 0.2, fitness)
f=open("stat.txt",'w+')
f.write(f'Generation    AvrFiness    AvrTime    AvrLen    BestGene')
for i in range(NumberOfGeneration):
    game1.run()
    learning.set_population(game1.get_population(),'parents')
    print(f'{i}  AvrFiness {round(sum(learning.get_fitness)/len(learning.get_fitness),2)} avrTime {round(learning.get_avr_time(),2)} avrLen {round(learning.get_avr_len(),4)}')
    generation = learning.get_childs()
    f.write(f'{i}    {sum(learning.get_fitness) / len(learning.get_fitness)}    {learning.get_avr_time()}    {learning.get_avr_len()}    {learning.best_genes()}')
    game1.clear_snakes()
    for g in generation:
        game1.add_snakes(1,(SHAPE_NETURAL_NETWORK, ACTIVATION_FUNCTION, True, g))
    game1.run(CUT_OFF)
    generation = []
    learning.set_population(game1.get_population(),"childs")
    generation = learning.get_generation(SNAKE_COUNT)
    for g in generation:
        game1.add_snakes(1,(SHAPE_NETURAL_NETWORK, ACTIVATION_FUNCTION, True, g))
