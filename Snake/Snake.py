import random
class Segment:
    """ Single snake segment """

    def __init__(self, x, y, seg_size, canvas=None, color='white'):
        self.__canvas = canvas
        self.__seg_size = seg_size
        if canvas:
            self.__instance = canvas.create_rectangle(x, y, x + seg_size, y + seg_size, fill=color)
        else:
            self.__instance = (x, y, x + seg_size, y + seg_size)

    def get_cords(self):
        return self.__canvas.coords(self.__instance) if self.__canvas else self.__instance

    def set_color(self,color):
        if self.__canvas:
            self.__canvas.itemconfig(self.__instance,fill=color)

    def draw(self, x1, y1, x2, y2, vector = None):
        if vector:
            x1 = x1 + vector[0] * self.__seg_size
            y1 = y1 + vector[1] * self.__seg_size
            x2 = x2 + vector[0] * self.__seg_size
            y2 = y2 + vector[1] * self.__seg_size

        if self.__canvas:
            self.__canvas.coords(self.__instance, x1, y1, x2, y2)
        else:
            self.__instance = (x1, y1, x2, y2)

    def delete(self):
        if self.__canvas:
            self.__canvas.delete(self.__instance)
        else:
            self.__instance = ()

    def clone(self):
        return Segment(self.get_cords()[0], self.get_cords()[1], self.__seg_size, self.__canvas)
            
class Snake:
    """ Simple Snake class """
    def __init__(self, start_cords, count_seg, seg_size, control, canvas):
        self.mapping = {"Down": (0, 1), "Right": (1, 0),
                        "Up": (0, -1), "Left": (-1, 0)}
        self.direction = "Right"
        self.vector = self.mapping["Right"]
        self.brain = control
        self.is_active = 'y'
        self.lifeTime = 0
        self.seg_size = seg_size
        self.death = ('w', 's', 'c')  # w - collisium with wall. s - collisium with snake
        self.segments = []
        # direction could be Horizontal(H) or Vertical(V)
        #self.position = random.choice(('Vertical', 'Horizontal'))
        #self.vector = self.vector = self.mapping['H_Right'] if self.position == 'Vertical' else self.mapping['V_Right']

        for i in range(count_seg):
            #if self.direction == 'Right':
            self.segments.append(Segment(start_cords[0] + seg_size * (i + 1), start_cords[1] + seg_size, seg_size, canvas))
            #else:
                #self.segments.append(Segment(start_cords[0] + seg_size, start_cords[1] + seg_size * (i + 1), seg_size, canvas))

        self.segments[-1].set_color('gray')



    def move(self, *snake_position):
        """ Moves the snake with the specified vector"""
        direction = self.brain.get_direction(*snake_position)
        # print(f'before {[x.get_cords() for x in self.segments]} pos - {self.position} dir - {direction}')
        # if self.position=='Vertical' and direction=='Left' :
        #     print('Alert');

        if (direction == 'Down' and self.direction != 'Up') or \
                (direction == 'Up' and self.direction != 'Down') or \
                (direction == 'Left' and self.direction != 'Right') or \
                (direction == 'Right' and self.direction != 'Left'):
            self.direction = direction
            self.vector = self.mapping[direction]

        for index in range(len(self.segments) - 1):
            x1, y1, x2, y2 = self.segments[index + 1].get_cords()
            self.segments[index].draw(x1, y1, x2, y2)

        x1, y1, x2, y2 = self.segments[-2].get_cords()
        self.segments[-1].draw(x1, y1, x2, y2, self.vector)
        self.lifeTime += 1

    def add_segment(self):
        """ Adds segment to the snake """
        self.segments.insert(0, self.segments[0].clone())

    def reset_snake(self, death):
        for segment in self.segments:
            segment.delete()
        self.is_active = 'n'
        self.death = death

    def get_snake_attributes(self):
        return len(self.segments), self.lifeTime, self.death
