import Game
import pyann

SNAKE_COUNT = 1000
CUT_OFF = 0.46
WEIDTH = 400
HEIGHT = 400
SHAPE_NETURAL_NETWORK = (24, 16, 12, 3)

ACTIVATION_FUNCTION = 'RELu'
NumberOfGeneration = 160000
# (3, 12, 'w', 12)

def fitness(par):
    l = par[0]
    t = par[1]
    d = par[2]

    c = par[3] # number of changed direction
    #return (l ** 2) * t * c - (5 * t if (d == 'w' and d != 'c') else t * 0.5)
    #return 10 * l ** 6 + t - (t ** 2) / (l - 2) ** 3
    return t + (2 ** (l-2) + 500 * (l-2) ** 2.1) - ((l-2)**1.2 * (0.25 * t) ** 1.3)

game1 = Game.Game(WEIDTH, HEIGHT, False)
#game1.add_snakes(2000,(SHAPE_NETURAL_NETWORK,ACTIVATION_FUNCTION, True))
#game1.add_snakes(1,'HUMAN')
#game1.run(CUT_OFF)

generation = []
generation2 =[]
cm = []
i=0
while len(generation) < SNAKE_COUNT:
      game1.clear_snakes()
      game1.add_snakes(1500, (SHAPE_NETURAL_NETWORK, ACTIVATION_FUNCTION, True))
      game1.run(CUT_OFF)
      tmp = game1.get_population()

      l = list(filter(lambda x: x[1][0] >= 4 and x[1][3] != 0, game1.get_population()))
      if len(l) >= 1:
         generation.extend(l)
         i += 1
      #print(f'{len(generation)}  {i}')

game1.clear_snakes()
for g in generation[:SNAKE_COUNT]:
     game1.add_snakes(1, (SHAPE_NETURAL_NETWORK, ACTIVATION_FUNCTION, True, g))

learning = pyann.GeneticAlgorithm(0.7, 0.04, fitness, SNAKE_COUNT)
f = open("stat.txt",'w+')
k = 0
i = 0
while i <= (NumberOfGeneration):
    game1.run(CUT_OFF)

    temp_pop = game1.get_population()

    learning.update_population(temp_pop)

    print(f'{i} Gen{k}({len(generation2)})  NumPop {learning.get_len_generation()} SumFiness {int(sum(learning.get_fitness))} avrTime {round(learning.get_avr_time(),2)} maxTime {learning.get_max_time()} avrLen {round(learning.get_avr_len(),3)} maxLen {learning.get_max_len()}')
    f.write(f'\n{i}  SumFitness {round(sum(learning.get_fitness),2)} avrTime {round(learning.get_avr_time(),2)} maxTime {learning.get_max_time()} avrLen {round(learning.get_avr_len(),4)} maxLen {learning.get_max_len()} \n {learning.get_best_chromosome()}')


    if len(generation2) >= 100 and k != 10:
        learning.add_population(generation2)
        i = 0
        k += 1
        generation2 =[]

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
