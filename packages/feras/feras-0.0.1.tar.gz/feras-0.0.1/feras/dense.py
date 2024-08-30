from .base import Boite, BoiteParam, Dot, Add
import numpy as np

class Dense():

  def __init__(self, neurons, activation=None):
    self.neurons = neurons
    self.activation = activation
    self.params = []
    self.suite = []
    self.initialisation = True


  def build(self, inputs):
    # weights initialization
    np.random.seed(42)

    self.weights = np.random.randn(inputs.shape[1], self.neurons)
    self.biais = np.random.randn(1, self.neurons)

    self.params.append(self.weights)
    self.params.append(self.biais)

    # construction de la suite d'opération
    self.suite = [Dot(weights=self.params[0]), Add(biais=self.params[1])]
    if self.activation:
      self.suite.append(self.activation)



  def forward(self, inputs):
    if self.initialisation:
      self.build(inputs)
      self.initialisation = False

    for boite in self.suite:
      inputs = boite.forward(inputs)

    self.output = inputs

    return self.output


  def backward(self, derivee_output):
    assert derivee_output.shape == self.output.shape

    for boite in reversed(self.suite):
      derivee_output = boite.backward(derivee_output)

    derivee_inputs = derivee_output

    self.get_layer_gradients()

    return derivee_inputs
  

  def get_layer_gradients(self):

    self.derivee_params = []

    for boite in self.suite:
      if issubclass(boite.__class__, BoiteParam):
        self.derivee_params.append(boite.derivee_param)



  def __repr__(self):
    r = f"DenseLayer(neurons={self.neurons})"
    if self.activation:
      r += " avec Sigmoid"

    return r