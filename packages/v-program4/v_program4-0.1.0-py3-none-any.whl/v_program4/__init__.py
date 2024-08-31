
# v_program4/__init__.py

import random
from math import exp
from random import seed

def initialize_network(n_inputs, n_hidden, n_outputs):
    network = list()
    hidden_layer = [{'weights': [random.uniform(-0.5, 0.5) for _ in range(n_inputs + 1)]} for _ in range(n_hidden)]
    network.append(hidden_layer)
    output_layer = [{'weights': [random.uniform(-0.5, 0.5) for _ in range(n_hidden + 1)]} for _ in range(n_outputs)]
    network.append(output_layer)
    
    print("\nThe initialized Neural Network:\n")
    for i, layer in enumerate(network, start=1):
        for j, neuron in enumerate(layer, start=1):
            print(f"\nLayer[{i}] Node[{j}]:\n", neuron)
    
    return network

def activate(weights, inputs):
    activation = weights[-1]
    for i in range(len(weights) - 1):
        activation += weights[i] * inputs[i]
    return activation

def transfer(activation):
    return 1.0 / (1.0 + exp(-activation))

def forward_propagate(network, row):
    inputs = row
    for layer in network:
        new_inputs = []
        for neuron in layer:
            activation = activate(neuron['weights'], inputs)
            neuron['output'] = transfer(activation)
            new_inputs.append(neuron['output'])
        inputs = new_inputs
    return inputs

def transfer_derivative(output):
    return output * (1.0 - output)

def backward_propagate_error(network, expected):
    for i in reversed(range(len(network))):
        layer = network[i]
        errors = list()
        if i != len(network) - 1:
            for j in range(len(layer)):
                error = sum(neuron['weights'][j] * neuron['delta'] for neuron in network[i + 1])
                errors.append(error)
        else:
            for j in range(len(layer)):
                neuron = layer[j]
                errors.append(expected[j] - neuron['output'])
        
        for j in range(len(layer)):
            neuron = layer[j]
            neuron['delta'] = errors[j] * transfer_derivative(neuron['output'])

def update_weights(network, row, l_rate):
    for i in range(len(network)):
        inputs = row[:-1]
        if i != 0:
            inputs = [neuron['output'] for neuron in network[i - 1]]
        for neuron in network[i]:
            for j in range(len(inputs)):
                neuron['weights'][j] += l_rate * neuron['delta'] * inputs[j]
            neuron['weights'][-1] += l_rate * neuron['delta']

def train_network(network, train, l_rate, n_epoch, n_outputs):
    print("\nNetwork Training Begins:\n")
    for epoch in range(n_epoch):
        sum_error = 0
        for row in train:
            outputs = forward_propagate(network, row)
            expected = [0 for _ in range(n_outputs)]
            expected[row[-1]] = 1
            sum_error += sum([(expected[i] - outputs[i])**2 for i in range(len(expected))])
            backward_propagate_error(network, expected)
            update_weights(network, row, l_rate)
        print(f'>epoch={epoch}, lrate={l_rate:.3f}, error={sum_error:.3f}')
    print("\nNetwork Training Ends:\n")

def predict(network, row):
    outputs = forward_propagate(network, row)
    return outputs.index(max(outputs))
