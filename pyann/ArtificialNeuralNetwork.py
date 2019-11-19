import numpy as nm


def sigma(x):
    return 1 / (1 + nm.exp(x))

def th(x):
    return nm.tanh(x)


def ReLU(x):
    return [a if a > 0 else 0.001 * a for a in x]
    #return (abs(x) + x) / 2


def CutOff(x, a):
    if a is not None:
        return (x - x + 1) * (x > a) if a else int(x)
    else:
        return x

ACTIVATION_FUNCTIONS = {'SIGMA': sigma, 'TH': th, 'RELU': ReLU}


class ArtificialNeuralNetwork:
    def __init__(self, ann_shape, activation_function='sigma', bias=False, hidenlayers = None):
        """ AAN - Artificial neural network """
        # [a0, a1, ..., an, an+1]
        # a0 - input size
        # a1 ... an - hidden layer size
        # an+1 - output size
        if len(ann_shape) < 3:
            raise ValueError(
                f"Neural Network should have min 3 layers - input, hidden, output. Size of the input is {len( ann_shape )}" )
        if activation_function.upper() not in ACTIVATION_FUNCTIONS.keys():
            raise ValueError( f'There is no {activation_function} in the ' \
                              f'activation function list. Available functions ' \
                              f'are {ACTIVATION_FUNCTIONS.keys()}' )
        self.__actfnc = ACTIVATION_FUNCTIONS[activation_function.upper()]
        self.__annbias = []
        self.__annshape = ann_shape
        # self.__output = nm.array([ann_shape[-1]])
        self.__hiddenlayer = []
        i = 0
        if hidenlayers:
            self.set_chromosome(hidenlayers)
        else:
            while i < len(ann_shape) - 1:
                # random matrix [-1:1)
                self.__hiddenlayer.append(2 * nm.random.random(tuple(ann_shape[i:i + 2])) - 1)
                i += 1
                if not bias and i <= len(ann_shape) - 1:
                    # zero vectors
                    self.__annbias.append(nm.zeros(tuple(ann_shape[i:i + 1]), dtype=int))
                elif i <= len(ann_shape) - 1:
                    # random biases vector [-1:1)
                    self.__annbias.append(2 * nm.random.random(tuple(ann_shape[i:i + 1])) - 1)

    def run(self, input_data, a = None):
        # results below 'a' will be setted to 0
        if len(input_data) != self.__annshape[0] and input_data:
            raise ValueError(
                f'Size of input should be {self.__annshape[0]}, you are trying to pass Len - {len(input_data)}; {input_data}' )

        result = nm.dot(input_data, self.__hiddenlayer[0])

        for i in range( len( self.__hiddenlayer ) - 1 ):
            result = self.__actfnc(nm.dot(result + self.__annbias[i], self.__hiddenlayer[i + 1]))

        return CutOff(sigma(result + self.__annbias[len(self.__annshape[1:-1])]), a).tolist()
        #return self.__actfnc(result + self.__annbiases[len(self.__annshape[1:-1])])
        # return CutOff ( self.__actfnc( result + self.__annbiases[len( self.__annshape[1:-1] )] ), a ).tolist()

    def get_chromosome(self):
        result = self.__hiddenlayer[0].ravel()
        i = 1
        while i < len( self.__hiddenlayer ):
            result = nm.concatenate( (result, self.__hiddenlayer[i].ravel()) )
            i += 1

        result = nm.concatenate((result, self.__annbias[0].ravel()))
        i = 1
        while i < len(self.__annbias):
            result = nm.concatenate((result, self.__annbias[i].ravel()))
            i += 1
        return result

    def set_chromosome(self, chromosome):
        self.__annbias.clear()
        self.__hiddenlayer.clear()
        # if self.__annshape == chromosome[0]: need to add check of compatibility of genes to ANN
        l = 0
        if type(chromosome) == list:
            ch = nm.asarray(chromosome)

        for i in range(len(self.__annshape) - 1):
            m = self.__annshape[i]
            n = self.__annshape[i + 1]
            self.__hiddenlayer.append(ch[l:l + n * m].reshape((m, n)))
            l += len(ch[l:l + n * m])
        l = 0
        i = len(self.__annshape)
        while i > 1:
            n = self.__annshape[i - 1]
            self.__annbias.insert(0, ch[-n - l:None if i == len(self.__annshape) else -l])
            l += len(ch[-n - l:None if i == len(self.__annshape) else -l])
            i -= 1
        #
        # else:
        #     raise ValueError(f'Unexpected shape - {gene[0]}. Correct shape for this ANN is {self.__annshape}')
