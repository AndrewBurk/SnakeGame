from tkinter import Canvas
import random
from Snake import Segment, Snake
import pyann

GameMode = ('HUMAN', 'RANDOM', 'NATURAL_NETWORK')


class Game(object):
    def __init__(self, window, width, height):
        self.__window = window
        self.__wWidth = width
        self.__wHeight = height
        self.__c = Canvas(window, width=width, height=height, bg="#003300")
        self.__seg_size = 20
        self.__c.grid()
        self.__food = []
        self.__food_lives = 200
        self.__snakes = []
        self.__gameTime = 0

        # i = self.__seg_size
        # while i < width:
        #     self.__c.create_line(i, 0, i, height, fill='white', width=1)
        #     i += self.__seg_size
        #
        # i = self.__seg_size
        # while i < height:
        #     self.__c.create_line(0, i, width, i, fill='white', width=1)
        #     i += self.__seg_size

    def __addfood__(self, n):
        posx = self.__seg_size * random.randint(1, (self.__wWidth - self.__seg_size) / self.__seg_size)
        posy = self.__seg_size * random.randint(1, (self.__wHeight - self.__seg_size) / self.__seg_size)

        self.__food.insert(0, self.__c.create_oval(posx, posy,
                                           posx + self.__seg_size, posy + self.__seg_size,
                                           fill="red"))
    def __resetfood__(self, n):
        posx = self.__seg_size * random.randint(1, (self.__wWidth - self.__seg_size) / self.__seg_size)
        posy = self.__seg_size * random.randint(1, (self.__wHeight - self.__seg_size) / self.__seg_size)
        self.__c.delete(self.__food[n])
        self.__food[n] = self.__c.create_oval(posx, posy,
                                              posx + self.__seg_size, posy + self.__seg_size,
                                              fill="red")



    def __checkCollision__(self):

        for snake in filter(lambda x: x[0].is_active == 'y', self.__snakes):
            indexS = self.__snakes.index(snake)
            # print(f'index S- {indexS}, len - {len(self.__food)}')
            food_coords = self.__c.coords(self.__food[indexS])
            head_coords = self.__c.coords(snake[0].segments[-1].instance)
            x1, y1, x2, y2 = head_coords
            # Check for collision with gamefield edges
            if x2 > self.__wWidth or x1 < 0 or y1 < 0 or y2 > self.__wHeight:
                snake[0].reset_snake(self.__c, self.__gameTime, 'w')
                self.__c.delete(self.__food[indexS])
            # Eating apples
            elif head_coords == food_coords:
                snake[0].add_segment(self.__c, self.__seg_size)
                self.__c.delete(self.__food[indexS])
                self.__resetfood__(indexS)
            # self collision
            else:
                for index in range(len(snake[0].segments) - 1):
                    if head_coords == self.__c.coords(snake[0].segments[index].instance):
                        snake[0].reset_snake(self.__c, self.__gameTime, 's')
                        self.__c.delete(self.__food[indexS])

    def clear_snakes(self):
        self.__snakes.clear()
        self.__food.clear()

    def add_snakes(self, count, control='random'):
        self.__gameTime = 0
        for i in range(count):
            posx = self.__seg_size * random.randint(1, (self.__wWidth - self.__seg_size) / self.__seg_size)
            posy = self.__seg_size * random.randint(1, (self.__wHeight - self.__seg_size) / self.__seg_size)
            snake = Snake([Segment(posx + self.__seg_size, posy + self.__seg_size, self.__seg_size, self.__c),
                           Segment(posx + self.__seg_size * 2, posy + self.__seg_size, self.__seg_size, self.__c),
                           Segment(posx + self.__seg_size * 3, posy + self.__seg_size, self.__seg_size, self.__c,
                                   "gray")])
            self.__addfood__(i)
            if control == 'RANDOM':
                self.__snakes.insert(0, [snake, 'RANDOM'])
            elif type(control) == tuple:
                self.__snakes.insert(0, [snake, pyann.ArtificialNeuralNetwork(control[0], control[1], control[2])])
            elif control == 'HUMAN':
                self.__snakes.insert(0, [snake, 'HUMAN'])
            else:
                raise ValueError(f'Unexpected arg. {control}')

    def move(self):
        # counting all snakes; Need to loop only active
        for snake in filter(lambda x: x[0].is_active == 'y', self.__snakes):
            snake[0].move(self.__seg_size, self.__c)
            snake[0].lifeTime = self.__gameTime
            if snake[0].lifeTime % self.__food_lives == 0:
                indexS = self.__snakes.index(snake)
                self.__resetfood__(indexS)

        self.__checkCollision__()
        self.__gameTime += 1

    def change_direction(self, cut_off):
        dir = ['Down', 'Up', 'Left', 'Right']
        for snake in filter(lambda x: x[0].is_active == 'y', self.__snakes):
            if snake[1] == "RANDOM":
                r = random.randint(0, 3)
                snake[0].change_direction(dir[r])
            elif snake[1] == "HUMAN":
                r = int(input())
                snake[0].change_direction(dir[r])
            else:
                d = snake[1].run(self.get_snake_position(snake), cut_off)

                if sum(d) == 1:
                    snake[0].change_direction(dir[d.index(1)])
                else:
                        indexS = self.__snakes.index(snake)
                        snake[0].reset_snake(self.__c, self.__gameTime, 's')
                        self.__c.delete(self.__food[indexS])

    def get_active_snakes_count(self):
        count = 0
        for i in range(len(self.__snakes)):
            if self.__snakes[i][0].is_active == 'y':
                count += 1
        return count

    def get_snake_position(self, snake):
        # Return vector of size 4*3=12
        #     4 - all possible directions
        #     0-3  - distance to snake itself for 4 directions
        #     4-7  - distance to the wall for 4 directions
        #     8-11 - distance to the food
        result = []
        # coords of snake head and food
        xh1, yh1, = self.__c.coords(snake[0].segments[-1].instance)[:2]
        indexS = self.__snakes.index(snake)
        xf1, yf1 = self.__c.coords(self.__food[indexS])[:2]
        up = []
        right = []
        down = []
        left = []
        for index in range(len(snake[0].segments) - 1):
            # segment coordinate
            xs1, ys1 = self.__c.coords(snake[0].segments[index].instance)[:2]
            up.append(
                (yh1 - ys1) / self.__seg_size if xs1 == xh1 and ys1 < yh1 else 0)  # direction up
            right.append((xs1 - xh1) /
                         self.__seg_size if ys1 == yh1 and xs1 > xh1 else 0)  # direction right
            down.append((ys1 - yh1) /
                        self.__seg_size if xs1 == xh1 and ys1 > yh1 else 0)  # direction down
            left.append((xh1 - xs1) /
                        self.__seg_size if ys1 == yh1 and xs1 < xh1 else 0)  # direction left

        result.append(max(up))
        result.append(max(right))
        result.append(max(down))
        result.append(max(left))

        # adding distance to the wall;
        result.append(yh1 / self.__seg_size)  # direction up
        result.append((self.__wWidth - xh1) / self.__seg_size - 1)  # direction right
        result.append((self.__wHeight - yh1) / self.__seg_size - 1)  # direction down
        result.append(xh1 / self.__seg_size)  # direction left
        # ['Down', 'Up', 'Left', 'Right']
        # distance to the food;
        result.append(
            (yh1 - yf1) / self.__seg_size if xf1 == xh1 and yf1 < yh1 else 0)  # direction up
        result.append(
            (xf1 - xh1) / self.__seg_size - 1 if yf1 == yh1 and xf1 > xh1 else 0)  # direction right
        result.append(
            (yf1 - yh1) / self.__seg_size - 1 if xf1 == xh1 and yf1 > yh1 else 0)  # direction down
        result.append(
            (xh1 - xf1) / self.__seg_size if yf1 == yh1 and xf1 < xh1 else 0)  # direction left

        # dist to wall by croos
        result.append((self.__wWidth - xh1 - self.__seg_size if xh1 + yh1 >= self.__wWidth else yh1) * 2 / self.__seg_size)  # A
        result.append((self.__wHeight - yh1 if yh1 - xh1 + self.__wWidth >= self.__wHeight else self.__wHeight - xh1) * 2 / self.__seg_size - 2)  # D
        result.append((self.__wHeight - yh1 - self.__seg_size if xh1 + yh1 >= self.__wHeight else xh1) * 2 / self.__seg_size)  # B
        result.append((yh1 if xh1 - yh1 >= 0 else xh1) * 2 / self.__seg_size)  # C

        # dist to food by cos
        result.append((xf1 - xh1)*2 / self.__seg_size if xf1 + yf1 - xh1 - yh1 == 0 and yf1 < yh1 and xf1 > xh1 else 0) #A
        result.append(
            (yf1 - yh1) * 2 / self.__seg_size if yf1 - xf1 + xh1 - yh1 == 0 and yf1 > yh1 and xf1 > xh1 else 0)  # D
        result.append(
            (yf1 - yh1) * 2 / self.__seg_size if yf1 + xf1 - xh1 - yh1 == 0 and yf1 > yh1 and xf1 < xh1 else 0)  # B
        result.append(
            (yh1 - yf1) * 2 / self.__seg_size if yf1 - xf1 + xh1 - yh1 == 0 and yf1 < yh1 and xf1 < xh1 else 0)  # c
        # for seg in snake.segments:
        #     xh1, yh1 = self.__c.coords(seg.instance)[:2]
        # print(f'({xh1 / 20},{yh1 / 20})')

        r = (((yh1 - yf1) ** 2) / (self.__seg_size * self.__seg_size) + ((xh1 - xf1) ** 2) / (
                    self.__seg_size * self.__seg_size)) ** 0.5
        result.append(r)
        result.append((xh1) / self.__seg_size)  # direction left
        result.append((yh1) / self.__seg_size)  # directi rigth
        return result

    def game_ower(self):
        game_over_text = self.__c.create_text(self.__wWidth / 2, self.__wHeight / 2, text="GAME OVER!",
                                              font='Arial 20', fill='red',
                                              state='normal')
        # self.__c.itemconfigure(game_over_text, state='normal')

    def get_population(self):
        result = []
        for s in self.__snakes:
            result.append((s[1].get_gene(), s[0].get_snake_attributes()))
        return result
