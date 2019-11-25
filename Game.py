import tkinter as tk
import random
from Snake import Segment, Snake
import pyann
import time

GameMode = ('HUMAN', 'RANDOM', 'NATURAL_NETWORK')


class Game():
    def __init__(self, width, height, display=True):

        if display:
            self.__root = tk.Tk()
            self.__root.title("PythonicWay Snake")
            self.__c = tk.Canvas(width=width, height=height, bg="#003300")
            self.__c.grid()
        else:
            self.__c = None
        self.__display = display
        self.__wWidth = width
        # self.f=open('cut_off.csv','w+')
        self.__wHeight = height
        self.__seg_size = 20
        self.__listfoods = []
        self.__food_lives = 50
        self.__snakes = []
        self.__gameTime = 1

        # i = self.__seg_size
        # while i < width:
        #    self.__c.create_line(i, 0, i, height, fill='white', width=1)
        #    i += self.__seg_size
        #
        # i = self.__seg_size
        # while i < height:
        #    self.__c.create_line(0, i, width, i, fill='white', width=1)
        #    i += self.__seg_size

    def __addfood__(self):
        posx = self.__seg_size * random.randint(0, (self.__wWidth - self.__seg_size) / self.__seg_size)
        posy = self.__seg_size * random.randint(0, (self.__wHeight - self.__seg_size) / self.__seg_size)
        food = Segment(posx, posy, self.__seg_size, self.__c, "red")
        # list of foods has time of food living(seconf par) and food
        self.__listfoods.insert(0,[food, 0])

    def __resetfood__(self, n):
        posx = self.__seg_size * random.randint(0, (self.__wWidth - self.__seg_size) / self.__seg_size)
        posy = self.__seg_size * random.randint(0, (self.__wHeight - self.__seg_size) / self.__seg_size)
        self.__listfoods[n][1] = 0
        self.__listfoods[n][0].draw(posx, posy,
                                 posx + self.__seg_size, posy + self.__seg_size,
                                 self.__c)

    def __checkCollision__(self):

        for snake in filter(lambda x: x[0].is_active == 'y', self.__snakes):
            indexS = self.__snakes.index(snake)
            food_coords = self.__listfoods[indexS][0].get_coords(self.__c)
            head_coords = snake[0].segments[-1].get_coords(self.__c)
            x1, y1, x2, y2 = head_coords
            # Check for collision with gamefield edges
            if x2 > self.__wWidth or x1 < 0 or y1 < 0 or y2 > self.__wHeight:
                snake[0].reset_snake(self.__c, self.__gameTime, 'w')
                self.__listfoods[indexS][0].delete(self.__c)
            # Eating apples
            elif head_coords == food_coords:
                snake[0].add_segment(self.__c, self.__seg_size)
                # self.__listfoods[indexS].delete(self.__c)
                self.__resetfood__(indexS)
            # self collision
            else:
                for index in range(len(snake[0].segments) - 1):
                    if head_coords == snake[0].segments[index].get_coords(self.__c):
                        snake[0].reset_snake(self.__c, self.__gameTime, 's')
                        self.__listfoods[indexS][0].delete(self.__c)

    def clear_snakes(self):
        self.__snakes.clear()
        self.__listfoods.clear()

    def add_snakes(self, count, control='random'):
        self.__gameTime = 1
        for i in range(count):
            posx, posy = 44444, 44444
            while posx + 4 * self.__seg_size >= self.__wWidth or posy + 4 * self.__seg_size >= self.__wHeight:
                posx = self.__seg_size * random.randint(1, (self.__wWidth - self.__seg_size) / self.__seg_size)
                posy = self.__seg_size * random.randint(1, (self.__wHeight - self.__seg_size) / self.__seg_size)
            d = random.choice(['Vertical'])
            if d == 'Horizontal':
                snake = Snake([Segment(posx + self.__seg_size, posy + self.__seg_size, self.__seg_size, self.__c),
                               Segment(posx + self.__seg_size * 2, posy + self.__seg_size, self.__seg_size, self.__c),
                               Segment(posx + self.__seg_size * 3, posy + self.__seg_size, self.__seg_size, self.__c, "gray")], d)
            else:
                snake = Snake([Segment(posx + self.__seg_size, posy + self.__seg_size, self.__seg_size, self.__c),
                        Segment(posx + self.__seg_size, posy + self.__seg_size * 2, self.__seg_size, self.__c),
                        Segment(posx + self.__seg_size, posy + self.__seg_size * 3, self.__seg_size, self.__c, "gray")], d)

            if control == 'RANDOM':
                self.__snakes.insert(0, [snake, 'RANDOM'])
            elif type(control) == tuple:
                self.__snakes.insert(0, [snake, pyann.ArtificialNeuralNetwork(control[0], control[1], control[2])])
            elif control == 'HUMAN':
                self.__snakes.insert(0, [snake, 'HUMAN'])
            else:
                raise ValueError(f'Unexpected arg. {control}')
            self.__addfood__()
    def move(self):
        # counting all snakes; Need to loop only active
        for snake in list(filter(lambda x: x[0].is_active == 'y', self.__snakes)):
            indexS = self.__snakes.index(snake)
            snake[0].move(self.__seg_size, self.__c)
            snake[0].lifeTime = self.__gameTime
            self.__listfoods[indexS][1] += 1
            if self.__listfoods[indexS][1] % self.__food_lives == 0:
                snake[0].reset_snake(self.__c, self.__gameTime, 'c')
                self.__listfoods[indexS][0].delete(self.__c)
        self.__checkCollision__()
        self.__gameTime += 1

    def change_direction(self, cut_off):
        dir = ['Continue', 'Left', 'Right']
        for snake in list(filter(lambda x: x[0].is_active == 'y', self.__snakes)):
            if snake[1] == "RANDOM":
                r = random.randint(0, 3)
                snake[0].change_direction(dir[r])
            elif snake[1] == "HUMAN":
                r = int(input())
                snake[0].change_direction(dir[r])
            else:
                # tmp = snake[1].run(self.get_snake_position(snake))
                d = snake[1].run(self.get_snake_position(snake), cut_off)
                # self.f.write(f'{cut_off} {tmp[0]} {tmp[1]} {tmp[2]} {d[0]} {d[1]} {d[2]} {sum(d)}\n')
                #index = max(enumerate(d), key=lambda x: x[1])[0]
                #snake[0].change_direction(dir[index])
                if sum(d) == 1:
                     snake[0].change_direction(dir[d.index(1)])

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
        xh1, yh1, = snake[0].segments[-1].get_coords(self.__c)[:2]
        indexS = self.__snakes.index(snake)
        xf1, yf1 = self.__listfoods[indexS][0].get_coords(self.__c)[:2]
        up, up_c, right, right_c, down, down_c, left, left_c = [], [], [], [], [], [], [], []

        for index in range(len(snake[0].segments) - 1):
            # segment coordinate
            xs1, ys1 = snake[0].segments[index].get_coords(self.__c)[:2]
            if xs1 == xh1 and ys1 < yh1: up.append(yh1 - ys1)  # direction up
            if ys1 == yh1 and xs1 > xh1: right.append(xs1 - xh1)  # direction right
            if xs1 == xh1 and ys1 > yh1: down.append(ys1 - yh1)  # direction down
            if ys1 == yh1 and xs1 < xh1: left.append(xh1 - xs1)  # direction left
            # dis by cos to self
            if xs1 - ys1 + yh1 - xh1 == 0 and ys1 < yh1 and xs1 < xh1: up_c.append((xh1 - xs1) / self.__wHeight)  # A
            if -ys1 - xs1 + yh1 + xh1 == 0 and yh1 >= ys1 and xs1 >= xh1: right_c.append((yh1 - ys1) / self.__wWidth)  # B
            if xs1 - ys1 + yh1 - xh1 == 0 and ys1 >= yh1 and xs1 >= xh1: down_c.append((xs1 - xh1) / self.__wHeight)  # C
            if -ys1 - xs1 + yh1 + xh1 == 0 and yh1 < ys1 and xs1 < xh1: left_c.append((ys1 - yh1) / self.__wWidth)  # D

        result.append(0 if len(up) == 0 else min(up) / self.__wHeight)
        result.append(0 if len(right) == 0 else min(right) / self.__wWidth)
        result.append(0 if len(down) == 0 else min(down) / self.__wHeight)
        result.append(0 if len(left) == 0 else min(left) / self.__wWidth)

        result.append(0 if len(up_c) == 0 else min(up_c))
        result.append(0 if len(right_c) == 0 else min(right_c))
        result.append(0 if len(down_c) == 0 else min(down_c))
        result.append(0 if len(left_c) == 0 else min(left_c))

        # adding distance to the wall;
        result.append(yh1 / self.__wHeight )  # direction up
        result.append((self.__wWidth - xh1 - self.__seg_size ) / self.__wWidth)  # direction right
        result.append((self.__wHeight - yh1 - self.__seg_size) /self.__wHeight)  # direction down
        result.append(xh1 / self.__wWidth )  # direction left
        # ['Down', 'Up', 'Left', 'Right']
        # distance to the food;
        result.append(1 + 0*(yh1 - yf1) / self.__wHeight if xf1 == xh1 and yf1 < yh1 else 0)  # direction up
        result.append(1 + 0*(xf1 - xh1) / self.__wWidth if yf1 == yh1 and xf1 > xh1 else 0)  # direction right
        result.append(1 + 0*(yf1 - yh1) / self.__wHeight if xf1 == xh1 and yf1 > yh1 else 0)  # direction down
        result.append(1 + 0*(xh1 - xf1) / self.__wWidth if yf1 == yh1 and xf1 < xh1 else 0)  # direction left

         # dist to wall by croos
        result.append(yh1 / self.__wWidth if yh1 <= xh1 else xh1 / self.__wHeight) #A
        result.append(yh1 / self.__wWidth if yh1 <= -xh1 + self.__wHeight else (self.__wHeight - xh1 - self.__seg_size) / self.__wHeight) #B
        result.append((self.__wHeight - xh1 - self.__seg_size) / self.__wHeight if yh1 <= xh1 else (self.__wHeight - yh1 - self.__seg_size) /self.__wHeight) #C
        result.append( xh1 /self.__wHeight if yh1 <= -xh1 + self.__wHeight else (self.__wWidth - yh1 - self.__seg_size) /self.__wWidth) #D

        # # dist to food by cos
        result.append(1 + 0*(xh1 - xf1) /self.__wHeight if xf1 - yf1 + yh1 - xh1 == 0 and yf1 < yh1 and xf1 < xh1 else 0) #A
        result.append(1 + 0*(yh1 - yf1) /self.__wWidth if -yf1 - xf1 + yh1 + xh1 == 0 and yh1 >= yf1 and xf1 >= xh1 else 0)  # B
        result.append(1 + 0*(xf1 - xh1) /self.__wHeight if xf1 - yf1 + yh1 - xh1 == 0 and yf1 >= yh1 and xf1 >= xh1 else 0)  # C
        result.append(1 + 0*(yf1 - yh1) /self.__wWidth if -yf1 - xf1 + yh1 + xh1 == 0 and yh1 < yf1 and xf1 < xh1 else 0)  # D


        #result.append(1 if snake[0].direction == 'Up' else 0)
        #result.append(1 if snake[0].direction == 'Right' else 0)
        #result.append(1 if snake[0].direction == 'Left' else 0)
        #result.append(1 if snake[0].direction == 'Down' else 0)
        # print(f'self up {result[0]} \n'
        #       f'self rigth {result[1]} \n'
        #       f'self down {result[2]} \n'
        #       f'self left {result[3]} \n'
        #       f'cros self A {result[4]} \n'
        #       f'cros self B {result[5]} \n'
        #       f'cros self C {result[6]} \n'
        #       f'cros self D {result[7]} \n'
        #       f'wall up {result[8]} \n'
        #       f'wall rigth {result[9]} \n'
        #       f'wall down {result[10]} \n'
        #       f'wall left {result[11]} \n'
        #       f'food up {result[12]} \n'
        #       f'food rigth {result[13]} \n'
        #       f'food down {result[14]} \n'
        #       f'food left {result[15]} \n'
        #       f'cros A {result[16]} \n'
        #       f'cros B {result[17]} \n'
        #       f'cros C {result[18]} \n'
        #       f'cros D {result[19]} \n'
        #       f'cros food A {result[20]} \n'
        #       f'cros food B {result[21]} \n'
        #       f'cros food C {result[22]} \n'
        #       f'cros food D {result[23]} \n'
        #       f'head up {result[24]} \n'
        #       f'head right {result[25]} \n'
        #       f'head left {result[26]} \n'
        #       f'head down {result[27]} \n'
        #       f'xh {xh1/self.__wWidth} \n'
        #       f'yh {yh1/self.__wWidth} \n'
        #       f'xf {xf1/self.__wWidth} \n'
        #       f'yf {yf1 / self.__wWidth} \n')
        return result

    def game_ower(self):
        game_over_text = self.__c.create_text(self.__wWidth / 2, self.__wHeight / 2, text="GAME OVER!",
                                              font='Arial 20', fill='red',
                                              state='normal')
        # self.__c.itemconfigure(game_over_text, state='normal')

    def get_population(self):
        result = []
        for s in self.__snakes:
            result.append((s[1].get_chromosome(), s[0].get_snake_attributes()))
        return result

    def run(self, cut_off = 0.6, speed = 0.1):
        count_active_snakes = self.get_active_snakes_count()
        while count_active_snakes != 0:
            # self.get_snake_position(self.__snakes[0])
            self.move()
            self.change_direction(cut_off)
            if self.__display:
                time.sleep(speed)
                self.__root.update()
            count_active_snakes = self.get_active_snakes_count()
