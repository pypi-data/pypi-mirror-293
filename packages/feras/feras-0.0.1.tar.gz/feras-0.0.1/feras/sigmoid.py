import numpy as np
from .base import Boite

class Sigmoid(Boite):

  def __init__(self):
    super().__init__()

  def operation(self):
    return 1 / (1 + np.exp(-1 * self.inputs))

  def gradient(self, derivee_output):
    return self.output * (1 - self.output) * derivee_output

  def __repr__(self):
    return "sigmoid"