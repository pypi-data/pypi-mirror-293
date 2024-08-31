import numpy as np

class NeuralNetwork:
    def __init__(self, number_of_layers, layer_sizes, learning_rate=0.1):
        # Initialize network parameters
        self.learning_rate = learning_rate
        
        # Weights and biases initialization
        self.weightsMatrix = []
        self.biasesMatrix = []
        self.numLayers = number_of_layers
        self.layerSizes = layer_sizes
        for layer in range(number_of_layers - 1):
            weights = np.random.randn(layer_sizes[layer], layer_sizes[layer + 1])
            biases = np.random.randn(1, layer_sizes[layer + 1])
            self.weightsMatrix.append(weights)
            self.biasesMatrix.append(biases)

    # Activation function: Sigmoid and its derivative
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, x):
        return x * (1 - x)

    # Forward pass
    def forward(self, X):
        self.layer_input = []
        self.layer_output = [X]  # Start with input layer output

        for layer in range(self.numLayers - 1):
            layer_input = np.dot(self.layer_output[-1], self.weightsMatrix[layer]) + self.biasesMatrix[layer]
            self.layer_input.append(layer_input)
            self.layer_output.append(self.sigmoid(layer_input))

        self.final_output = self.layer_output[-1]
        return self.final_output

    # Backward pass (backpropagation)
    def backward(self, X, y):
        error = y - self.final_output
        d_output = error * self.sigmoid_derivative(self.final_output)
        deltas = [d_output]

        # Calculate deltas for all layers
        for layer in range(self.numLayers - 2, 0, -1):
            error_hidden_layer = deltas[-1].dot(self.weightsMatrix[layer].T)
            d_hidden_layer = error_hidden_layer * self.sigmoid_derivative(self.layer_output[layer])
            deltas.append(d_hidden_layer)

        deltas.reverse()

        # Update weights and biases
        for layer in range(self.numLayers - 1):
            self.weightsMatrix[layer] += self.layer_output[layer].T.dot(deltas[layer]) * self.learning_rate
            self.biasesMatrix[layer] += np.sum(deltas[layer], axis=0, keepdims=True) * self.learning_rate

    # Training the network
    loss_progress = []
    
    def train(self, X, y, epochs=10000):
        for epoch in range(epochs):
            self.forward(X)
            self.backward(X, y)
            
            if epoch % (epochs // 10) == 0:
                loss = np.mean(np.abs(y - self.final_output))
                self.loss_progress.append(loss)

    # Predicting using the trained network
    def predict(self, X):
        return self.forward(X)
        
    # Retrieving loss progress
    def getLoss(self):
        return self.loss_progress