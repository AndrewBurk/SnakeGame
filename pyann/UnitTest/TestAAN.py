import unittest
import pyann.ArtificialNeuralNetwork as ann

class TestANN(unittest.TestCase):
    def test_init_ANN(self):
        hidden_layers = [1.0] * 21 + [2] * 30
        nn_bias = ann((4,5,3,2),'th',False,hidden_layers)
        self.assertEqual(hidden_layers, list(nn_bias.get_chromosome()))

    def test_setCH_ANN(self):
        hidden_layers = [1.0] * 21 + [2] * 30
        nn_bias = ann((4,5,3,2),'th',False)
        nn_bias.set_chromosome(hidden_layers)
        self.assertEqual(hidden_layers, list(nn_bias.get_chromosome()))

    def test_run_ANN(self):
        hidden_layers = [1.0] * 41 + [2.0]*10
        input = []
        input.append(1)
        input.append(1)
        input.append(1)
        input.append(1)
        nn_bias = ann((4,5,3,2),'th',True, hidden_layers)
        # sigma(th(3*(th(1+2"bais")+2"bais))+2"bais") = 0.04743
        self.assertEqual((0.04743, 0.04743), (round(nn_bias.run(input)[0], 5), round(nn_bias.run(input)[1], 5)))

if __name__ == '__main__':
    unittest.main()
