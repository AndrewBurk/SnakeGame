import random


class Segment(object):
    """ Single snake segment """

    def __init__(self, x, y, seg_size, canvas, color='white'):
        self.instance = canvas.create_rectangle(x, y,
                                                x + seg_size, y + seg_size,
                                                fill=color)


class Snake(object):
    """ Simple Snake class """

    def __init__(self, segments):
        self.segments = segments
        # possible moves
        self.mapping = {"Down": (0, 1), "Right": (1, 0),
                        "Up": (0, -1), "Left": (-1, 0)}
        # initial movement direction
        self.direction = "Right"
        self.vector = self.mapping["Right"]
        self.is_active = 'y'
        self.lifeTime = 0
        self.__death = ('w', 's') # w - collisiom with wall. s - collisium with snake

    def move(self, seg_size, canvas):
        """ Moves the snake with the specified vector"""
        for index in range(len(self.segments) - 1):
            segment = self.segments[index].instance
            x1, y1, x2, y2 = canvas.coords(self.segments[index + 1].instance)
            canvas.coords(segment, x1, y1, x2, y2)

        x1, y1, x2, y2 = canvas.coords(self.segments[-2].instance)
        canvas.coords(self.segments[-1].instance,
                      x1 + self.vector[0] * seg_size, y1 + self.vector[1] * seg_size,
                      x2 + self.vector[0] * seg_size, y2 + self.vector[1] * seg_size)

    def add_segment(self, canvas, seg_size):
        """ Adds segment to the snake """
        last_seg = canvas.coords(self.segments[0].instance)
        x = last_seg[2] - seg_size
        y = last_seg[3] - seg_size
        self.segments.insert(0, Segment(x, y, seg_size, canvas))
        # if len(self.segments) > 3:
        #     print(len(self.segments))

    def change_direction(self, direction):
        """ Changes direction of snake """
        # if event.keysym in self.mapping:
        #     self.vector = self.mapping[event.keysym]
        # dir = ['Down', 'Up', 'Left', 'Right']
        # r = random.randint(0, 3)
        if (direction == 'Down' and self.direction != 'Up') or \
                (direction == 'Up' and self.direction != 'Down') or \
                (direction == 'Left' and self.direction != 'Right') or \
                (direction == 'Right' and self.direction != 'Left'):
            self.direction = direction
            self.vector = self.mapping[direction]

    def reset_snake(self, canvas, life_time, death):
        for segment in self.segments:
            canvas.delete(segment.instance)
        self.is_active = 'n'
        self.lifeTime = life_time
        self.__death = death

    def get_snake_attributes(self):
        return len(self.segments), self.lifeTime, self.__death




