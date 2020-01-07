import tkinter as tk
import random
from Snake import Segment, Snake
import time
from abc import ABC, abstractmethod

class TrainingEnv(ABC):
    @abstractmethod
    def run(self, **param):
        pass

    @abstractmethod
    def get_chromosomes(self):
        pass


class Field(TrainingEnv):
    def __init__(self, width, height, seg_size, display=True):
        if display:
            self.__root = tk.Tk()
            self.__root.title("Pythonic Way Snake")
            self.__canvas = tk.Canvas(width=width, height=height, bg="#003300")
            self.__canvas.grid()
        else:
            self.__canvas = None
        self.__display = display
        self.__wWidth = width
        self.__wHeight = height
        self.__seg_size = seg_size
        self.__foods = []
        self.__food_lives = 75
        self.__snakes = []
        self.__gameTime = 1

    def __add_food(self):
        posx = self.__seg_size * random.randint(0, (self.__wWidth - self.__seg_size) / self.__seg_size)
        posy = self.__seg_size * random.randint(0, (self.__wHeight - self.__seg_size) / self.__seg_size)
        food = Segment(posx, posy, self.__seg_size, self.__canvas, "red")
        # list of foods has time of food living(second parameter) and food itself
        self.__foods.append([food, 0])

    def __reset_food(self, n, reset_time = True):
        posx = self.__seg_size * random.randint(0, (self.__wWidth - self.__seg_size) / self.__seg_size)
        posy = self.__seg_size * random.randint(0, (self.__wHeight - self.__seg_size) / self.__seg_size)
        self.__foods[n][1] = 0 if reset_time else self.__foods[n][1]
        self.__foods[n][0].draw(posx, posy,
                                posx + self.__seg_size, posy + self.__seg_size)

    def __check_collision(self):
        for snake in filter(lambda x: x.is_active == 'y', self.__snakes):
            indexS = self.__snakes.index(snake)
            food_coords = self.__foods[indexS][0].get_cords()
            head_coords = snake.segments[-1].get_cords()
            x1, y1, x2, y2 = head_coords
            # Check for collision with gamefield edges
            if x2 > self.__wWidth or x1 < 0 or y1 < 0 or y2 > self.__wHeight:
                snake.reset_snake('w')
                self.__foods[indexS][0].delete()
            # Eating apples
            elif head_coords == food_coords:
                snake.add_segment()
                self.__reset_food(indexS)
            # self collision
            else:
                for index in range(len(snake.segments) - 1):
                    if head_coords == snake.segments[index].get_cords():
                        snake.reset_snake('s')
                        self.__foods[indexS][0].delete()

    def __get_snake_position(self, snake):
        # Return vector of size 4*3=12
        #     4 - all possible directions
        #     0-3  - distance to snake itself for 4 directions
        #     4-7  - distance to the wall for 4 directions
        #     8-11 - distance to the food
        result = []
        # coords of snake head and food
        xh1, yh1 = snake.segments[-1].get_cords()[:2]
        indexS = self.__snakes.index(snake)
        xf1, yf1 = self.__foods[indexS][0].get_cords()[:2]
        up, up_c, right, right_c, down, down_c, left, left_c = [], [], [], [], [], [], [], []

        for index in range(len(snake.segments) - 1):
            # segment coordinate
            xs1, ys1 = snake.segments[index].get_cords()[:2]
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
        result.append(1 + 0 * (yh1 - yf1) / self.__wHeight if xf1 == xh1 and yf1 < yh1 else 0)  # direction up
        result.append(1 + 0 * (xf1 - xh1) / self.__wWidth if yf1 == yh1 and xf1 > xh1 else 0)  # direction right
        result.append(1 + 0 * (yf1 - yh1) / self.__wHeight if xf1 == xh1 and yf1 > yh1 else 0)  # direction down
        result.append(1 + 0 * (xh1 - xf1) / self.__wWidth if yf1 == yh1 and xf1 < xh1 else 0)  # direction left

         # dist to wall by croos
        result.append(yh1 / self.__wWidth if yh1 <= xh1 else xh1 / self.__wHeight) #A
        result.append(yh1 / self.__wWidth if yh1 <= -xh1 + self.__wHeight else (self.__wHeight - xh1 - self.__seg_size) / self.__wHeight) #B
        result.append((self.__wHeight - xh1 - self.__seg_size) / self.__wHeight if yh1 <= xh1 else (self.__wHeight - yh1 - self.__seg_size) /self.__wHeight) #C
        result.append( xh1 /self.__wHeight if yh1 <= -xh1 + self.__wHeight else (self.__wWidth - yh1 - self.__seg_size) /self.__wWidth) #D

        # # dist to food by cos
        result.append(1 + 0 * (xh1 - xf1) /self.__wHeight if xf1 - yf1 + yh1 - xh1 == 0 and yf1 < yh1 and xf1 < xh1 else 0) #A
        result.append(1 + 0 * (yh1 - yf1) /self.__wWidth if -yf1 - xf1 + yh1 + xh1 == 0 and yh1 >= yf1 and xf1 >= xh1 else 0)  # B
        result.append(1 + 0 * (xf1 - xh1) /self.__wHeight if xf1 - yf1 + yh1 - xh1 == 0 and yf1 >= yh1 and xf1 >= xh1 else 0)  # C
        result.append(1 + 0 * (yf1 - yh1) /self.__wWidth if -yf1 - xf1 + yh1 + xh1 == 0 and yh1 < yf1 and xf1 < xh1 else 0)  # D

        result.append(1 if snake.direction == 'Down' else 0)
        result.append(1 if snake.direction == 'Right' else 0)
        result.append(1 if snake.direction == 'Up' else 0)
        result.append(1 if snake.direction == 'Left' else 0)

        xt, yt = snake.segments[0].get_cords()[:2]
        xnt, ynt = snake.segments[1].get_cords()[:2]
        result.append(1 if (yt - ynt) > 0 and (xnt - xt == 0) else 0)
        result.append(1 if (yt - ynt) == 0 and (xnt - xt > 0) else 0)
        result.append(1 if (yt - ynt) < 0 and (xnt - xt == 0) else 0)
        result.append(1 if (yt - ynt) == 0 and (xnt - xt < 0) else 0)
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

    def add_elements(self, control, count=1):
        self.__gameTime = 1
        for i in range(count):
            posx, posy = 44444, 44444
            while posx + 4 * self.__seg_size >= self.__wWidth or posy + 4 * self.__seg_size >= self.__wHeight:
                posx = self.__seg_size * random.randint(1, (self.__wWidth - self.__seg_size) / self.__seg_size)
                posy = self.__seg_size * random.randint(1, (self.__wHeight - self.__seg_size) / self.__seg_size)
            snake = Snake((posx, posy), 3, self.__seg_size, control, self.__canvas)

            self.__snakes.append(snake)
            self.__add_food()

    def move(self):
        # counting all snakes; Need to loop only active
        for snake in list(filter(lambda x: x.is_active == 'y', self.__snakes)):
            indexS = self.__snakes.index(snake)
            snake.move(self.__get_snake_position(snake))
            self.__foods[indexS][1] += 1
            #if self.__foods[indexS][1] % self.__food_lives == 0:
            #    self.__reset_food(indexS, False)
            if self.__foods[indexS][1] == self.__food_lives:
                snake.reset_snake('c')
                self.__foods[indexS][0].delete()
        self.__check_collision()
        self.__gameTime += 1

    def run(self, **param):
        if not('speed' in param.keys()):
            param['speed'] = 0.00001
        count_active_snakes = len(list(filter(lambda x: x.is_active == 'y', self.__snakes)))
        while count_active_snakes != 0:
            self.move()
            if self.__display:
                time.sleep(param['speed'])
                self.__root.update()
            count_active_snakes = len(list(filter(lambda x: x.is_active == 'y', self.__snakes)))

    def clear(self):
        self.__snakes.clear()
        self.__foods.clear()
        self.__gameTime = 1

    def get_chromosomes(self):
        return [(x.brain.get_chromosome(),x.get_snake_attributes()) for x in self.__snakes]
