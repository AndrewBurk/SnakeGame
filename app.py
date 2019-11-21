import Game
import pyann

SNAKE_COUNT = 750
CUT_OFF = 0.55
WEIDTH = 400
HEIGHT = 400
SHAPE_NETURAL_NETWORK = (28, 20, 12, 3)

ACTIVATION_FUNCTION = 'RELu'
NumberOfGeneration = 16000
# (3, 12, 'w', 12)
def fitness(par):
    l = par[0]
    t = par[1]
    d = par[2]
    c = par[3] # number of changed direction
    #return (l ** 2) * t * c - (5 * t if (d == 'w' and d != 'c') else t * 0.5)
    return 10 * l ** 6 + t - (t ** 2) / (l - 2) ** 3
    # return t + (2 ** (l-2) + 500 * (l-2) ** 2.1) - ((l-2)**1.2 * (0.25 * t) ** 1.3)

def sort(elem):
    return fitness(elem[1])

game1 = Game.Game(WEIDTH, HEIGHT, False)
game1.add_snakes(SNAKE_COUNT,(SHAPE_NETURAL_NETWORK,ACTIVATION_FUNCTION, True))
# game1.add_snakes(1,'HUMAN')
# game1.run()

generation = []
generation2 =[]
cm = []
i=0
# while len(generation) < SNAKE_COUNT:
#      game1.clear_snakes()
#      game1.add_snakes(700, (SHAPE_NETURAL_NETWORK, ACTIVATION_FUNCTION, True))
#      game1.run()
#      tmp = game1.get_population()
#
#      l = list(filter(lambda x: x[1][0] >= 3 and x[1][3] != 0, game1.get_population()))
#      if len(l) >= 1:
#         generation.extend(l)
#         i += 1
#      print(f'{len(generation)}  {i}')
#
# game1.clear_snakes()
# for g in generation[:SNAKE_COUNT]:
#      game1.add_snakes(1, (SHAPE_NETURAL_NETWORK, ACTIVATION_FUNCTION, True, g))

learning = pyann.GeneticAlgorithm(0.3, 0.04, fitness, SNAKE_COUNT)
f = open("stat.txt",'w+')
k = 0
i = 0
while i <= (NumberOfGeneration):
    game1.run(CUT_OFF)

    temp_pop = game1.get_population()

    # if k != 1:
    #     l = list(filter(lambda x: x[1][0] >= 5 and x[1][3] != 0,temp_pop))
    #     if len(l)>=1:
    #         generation2.extend(l)
    #
    # if len(generation2) >= SNAKE_COUNT and k != 1:
    #     learning.update_population(generation2)
    #     i = 0
    #     k += 1
    #     generation2 =[]
    # else:
    learning.update_population(temp_pop)

    print(f'{i} Gen{k} {len(generation2)} NumPop {learning.get_len_generation()} SumFiness {int(sum(learning.get_fitness))} avrTime {round(learning.get_avr_time(),2)} maxTime {learning.get_max_time()} avrLen {round(learning.get_avr_len(),4)} maxLen {learning.get_max_len()}')
    f.write(f'\n{i}  SumFitness {round(sum(learning.get_fitness),2)} avrTime {round(learning.get_avr_time(),2)} maxTime {learning.get_max_time()} avrLen {round(learning.get_avr_len(),4)} maxLen {learning.get_max_len()} \n {learning.get_best_chromosome()}')


    cm = learning.crossover_mutation()
    game1.clear_snakes()
    for p in cm:
        game1.add_snakes(1, (SHAPE_NETURAL_NETWORK, ACTIVATION_FUNCTION, True, p))
    game1.run(CUT_OFF)

    learning.add_population(game1.get_population())
    game1.clear_snakes()
    for p in learning.next_population():
        game1.add_snakes(1, (SHAPE_NETURAL_NETWORK, ACTIVATION_FUNCTION, True, p))
    i += 1







    # l = list(filter(lambda x: x[1][0] >= k and x[1][3] > 0,game1.get_population()))
    # if len(l)>=1:
    #     generatinon2.extend(l)
    #     gen = open(f'generationTEST.csv', 'w+')
    #     gen.write(f'{[x[1] for x in game1.get_population()]}')
    #     gen.close()
    #
    # if len(generatinon2) >= SNAKE_COUNT:
    #     learning.add_population(generatinon2)
    #     i = 0
    #     k += 1
    #     gen = open(f'generation{k}.csv', 'w+')
    #     gen.write(f'{[x[0] for x in generatinon2]} {[x[1] for x in generatinon2]}')
    #     gen.close()
    #     generatinon2 =[]
    # else:
    #     learning.add_population(game1.get_population())
    #
    # print(f'{i} Gen{k} {len(generatinon2)} NumPop {len(learning.get_generation())} SumFiness {int(sum(learning.get_fitness))} avrTime {round(learning.get_avr_time(),2)} maxTime {learning.get_max_time()} avrLen {round(learning.get_avr_len(),4)} maxLen {learning.get_max_len()}  {learning.best_chromosome()[1]}')
    # f.write(f'\n{i}  SumFiness {round(sum(learning.get_fitness),2)} avrTime {round(learning.get_avr_time(),2)} maxTime {learning.get_max_time()} avrLen {round(learning.get_avr_len(),4)} maxLen {learning.get_max_len()}    \n {learning.best_chromosome()}')
    #
    # kids = learning.get_childs()
    # # print(f'{i} NumOfKids {len(kids)}' )
    # game1.clear_snakes()
    # for g in kids:
    #     game1.add_snakes(1,(SHAPE_NETURAL_NETWORK, ACTIVATION_FUNCTION, True, g))
    # game1.run()
    #
    # generation = []
    # learning.add_population(game1.get_population())
    # game1.clear_snakes()
    #
    # generation = learning.get_generation()
    # for g in generation:
    #     game1.add_snakes(1,(SHAPE_NETURAL_NETWORK, ACTIVATION_FUNCTION, True, g))
