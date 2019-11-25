
import random

class Segment(object):
    """ Single snake segment """

    def __init__(self, x, y, seg_size, canvas=None, color='white'):
        if canvas != None:
            self.__instance = canvas.create_rectangle(x, y, x + seg_size, y + seg_size, fill=color)
        else:
            self.__instance = (x, y, x + seg_size, y + seg_size)

    def get_coords(self, canvas=None):
        return canvas.coords(self.__instance) if canvas != None else self.__instance
      
    def draw(self, x1, y1, x2, y2, canvas=None):
        if canvas != None:
            canvas.coords(self.__instance, x1, y1, x2, y2)
        else:
            self.__instance = (x1, y1, x2, y2)

    def delete(self,canvas=None):
        if canvas != None:
            canvas.delete(self.__instance)
        else:
            self.__instance = ()
            
class Snake:
    """ Simple Snake class """

    def __init__(self, segments, dir):
        self.segments = segments
        # possible moves
        # self.mapping = {"Down": (0, 1), "Right": (1, 0),
        #                 "Up": (0, -1), "Left": (-1, 0)}

        self.mapping = {'H_Right': (0, 1), 'V_Right': (1, 0),
                        'H_Left': (0, -1), 'V_Left': (-1, 0)}
        # direction could be Horizontal(H) or Vertical(V)
        # initial movement direction
        # d = random.choice(['Horizontal', 'Vertical'])
        self.direction = dir
        self.vector = self.mapping[dir[0].upper() + '_Right']
        self.is_active = 'y'
        self.lifeTime = 0
        self.countOfChangeDirection = 0
        self.__death = ('w', 's', 'c')  # w - collisium with wall. s - collisium with snake


    def move(self, seg_size, canvas):
        """ Moves the snake with the specified vector"""
        for index in range(len(self.segments) - 1):
            x1, y1, x2, y2 = self.segments[index + 1].get_coords(canvas)
            self.segments[index].draw(x1, y1, x2, y2, canvas)

        x1, y1, x2, y2 = self.segments[-2].get_coords(canvas)
        self.segments[-1].draw(
                x1 + self.vector[0] * seg_size, y1 + self.vector[1] * seg_size,
                x2 + self.vector[0] * seg_size, y2 + self.vector[1] * seg_size, canvas)

    def add_segment(self, canvas, seg_size):
        """ Adds segment to the snake """
        last_seg = self.segments[0].get_coords(canvas)
        x = last_seg[2] - seg_size
        y = last_seg[3] - seg_size
        self.segments.insert(0, Segment(x, y, seg_size, canvas))

    def change_direction(self, direction):
        """ Changes direction of snake """
        # if event.keysym in self.mapping:
        #     self.vector = self.mapping[event.keysym]
        # dir = ['Down', 'Up', 'Left', 'Right']
        # r = random.randint(0, 3)
        if self.direction == 'Vertical' and direction != 'Continue':
            self.vector = self.mapping['H_' + direction]
            self.direction = 'Horizontal'
            self.countOfChangeDirection += 1
        elif self.direction == 'Horizontal' and direction != 'Continue':
            self.vector = self.mapping['V_' + direction]
            self.direction = 'Vertical'
            self.countOfChangeDirection += 1

    def reset_snake(self, canvas, life_time, death):
        for segment in self.segments:
            segment.delete(canvas)
        self.is_active = 'n'
        self.lifeTime = life_time
        self.__death = death

    def get_snake_attributes(self):
        return len(self.segments), self.lifeTime, self.__death, self.countOfChangeDirection
