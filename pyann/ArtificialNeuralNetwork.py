import numpy as np

def sigma(x):
    return 1 / (1 + np.exp(x))

def th(x):
    return np.tanh(x)

def softmax(x):
    return np.exp(x) / np.sum(np.exp(x))

ReLU = lambda x: (abs(x) + x) / 2
    #lambda x: np.maximum(0, x)
    #return (abs(x) + x) / 2

def CutOff(x, a):
    if a:
        return (x - x + 1) * (x > a) if a else int(x)
    else:
        return x

ACTIVATION_FUNCTIONS = {'SIGMA': sigma, 'TH': th, 'RELU': ReLU}


class ArtificialNeuralNetwork:
    def __init__(self, ann_shape, activation_function = 'sigma', bias = False, hidden_layers = None):
        """ AAN - Artificial neural network """
        # [a0, a1, ..., an, an+1]
        # a0 - input size
        # a1 ... an - hidden layer size
        # an+1 - output size
        if len(ann_shape) < 3:
            raise ValueError(
                f"Neural Network should have min 3 layers - input, hidden, output. Size of the input is {len(ann_shape)}" )
        if activation_function.upper() not in ACTIVATION_FUNCTIONS.keys():
            raise ValueError( f'There is no {activation_function} in the ' \
                              f'activation function list. Available functions ' \
                              f'are {ACTIVATION_FUNCTIONS.keys()}' )
        self.__act_fnc = ACTIVATION_FUNCTIONS[activation_function.upper()]
        self.__ann_bias = []
        self.__ann_shape = ann_shape
        # self.__output = nm.array([ann_shape[-1]])
        self.__hidden_layer = []
        i = 0

        if hidden_layers is not None:
            self.set_chromosome(hidden_layers)
        else:
            while i < len(ann_shape) - 1:
                # random matrix [-1:1)
                self.__hidden_layer.append(2 * np.random.random(tuple(ann_shape[i:i + 2])) - 1)
                i += 1
                if not bias and i <= len(ann_shape) - 1:
                    # zero vectors
                    self.__ann_bias.append(np.zeros(tuple(ann_shape[i:i + 1]), dtype=int))
                elif i <= len(ann_shape) - 1:
                    # random biases vector [-1:1)
                    self.__ann_bias.append(2 * np.random.random(tuple(ann_shape[i:i + 1])) - 1)

    def run(self, input_data):
        # results below 'a' will be set to 0
        if len(input_data) != self.__ann_shape[0] and input_data:
            raise ValueError(
                f'Size of input should be {self.__ann_shape[0]}, you are trying to pass Len - {len(input_data)}; {input_data}' )
        result = input_data
        for i in range(len(self.__hidden_layer) - 1):
            result = self.__act_fnc(np.dot(result, self.__hidden_layer[i]) + self.__ann_bias[i])
        return sigma(np.dot(result, self.__hidden_layer[-1])).tolist()
        #return self.__actfnc(result + self.__annbiases[len(self.__annshape[1:-1])])
        # return CutOff ( self.__actfnc( result + self.__annbiases[len( self.__annshape[1:-1] )] ), a ).tolist()

    def get_chromosome(self):
        result = self.__hidden_layer[0].ravel()
        i = 1
        while i < len(self.__hidden_layer):
            result = np.concatenate((result, self.__hidden_layer[i].ravel()))
            i += 1

        result = np.concatenate((result, self.__ann_bias[0].ravel()))
        i = 1
        while i < len(self.__ann_bias):
            result = np.concatenate((result, self.__ann_bias[i].ravel()))
            i += 1
        return result

    def set_chromosome(self, chromosome):
        self.__ann_bias.clear()
        self.__hidden_layer.clear()
        # if self.__annshape == chromosome[0]: need to add check of compatibility of genes to ANN
        l = 0
        # if type(chromosome) == list:
        ch = np.asarray(chromosome)

        for i in range(len(self.__ann_shape) - 1):
            m = self.__ann_shape[i]
            n = self.__ann_shape[i + 1]
            self.__hidden_layer.append(ch[l:l + n * m].reshape((m, n)))
            l += len(ch[l:l + n * m])
        l = 0
        i = len(self.__ann_shape)
        while i > 1:
            n = self.__ann_shape[i - 1]
            self.__ann_bias.insert(0, ch[-n - l:None if i == len(self.__ann_shape) else -l])
            l += len(ch[-n - l:None if i == len(self.__ann_shape) else -l])
            i -= 1
        #
        # else:
        #     raise ValueError(f'Unexpected shape - {gene[0]}. Correct shape for this ANN is {self.__annshape}')
