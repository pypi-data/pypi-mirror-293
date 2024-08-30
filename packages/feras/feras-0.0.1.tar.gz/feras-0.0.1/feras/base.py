import numpy as np

class Boite():

  def __init__(self):
    pass

  def forward(self, inputs):
    self.inputs = inputs
    self.output = self.operation()
    return self.output

  def backward(self, derivee_output):
    assert derivee_output.shape == self.output.shape, f"La derivee_output reçue a un shape {derivee_output.shape} et different du shape de output : {self.output.shape}"

    self.derivee_inputs = self.gradient(derivee_output)
    assert self.derivee_inputs.shape == self.inputs.shape, f"La derivee_input calculée a un shape {self.derivee_inputs.shape } et different du shape de inputs : {self.inputs.shape}"

    return self.derivee_inputs


  def operation(self):
    pass

  def gradient(self, derivee_output):
    pass
  

class BoiteParam():

  def __init__(self, param):
    self.param = param

  def forward(self, inputs):
    self.inputs = inputs
    self.output = self.operation()
    return self.output

  def backward(self, derivee_output):
    assert derivee_output.shape == self.output.shape, f"La derivee_output reçue a un shape {derivee_output.shape} et different du shape de output : {self.output}"

    self.derivee_inputs = self.gradient(derivee_output)
    assert self.derivee_inputs.shape == self.inputs.shape, f"La derivee_input calculée a un shape {self.derivee_inputs.shape } et different du shape de inputs : {self.inputs.shape}"

    self.derivee_param = self.gradient_param(derivee_output)
    assert self.derivee_param.shape == self.param.shape, f"La derivee de param a un shape {self.derivee_param.shape} et different du shape de param : {self.param.shape}"

    return self.derivee_inputs


  def operation(self):
    pass
  def gradient(self, derivee_output):
    pass


  def gradient_param(self, derivee_output):
    pass
     

class Dot(BoiteParam):

  def __init__(self, weights):
    super().__init__(weights)

  def operation(self):
    return np.dot(self.inputs, self.param)

  def gradient(self, derivee_output):
    return np.dot( derivee_output, self.param.T)

  def gradient_param(self, derivee_output):
    return np.dot(self.inputs.T, derivee_output)

  def __repr__(self):
    return "DotProduct"
  

class Add(BoiteParam):

  def __init__(self, biais):
    super().__init__(biais)

  def operation(self):
    return self.inputs + self.param

  def gradient(self, derivee_output):
    return np.ones_like(self.inputs) * derivee_output

  def gradient_param(self, derivee_output):
    r =  np.ones_like(self.param) * derivee_output
    return r.sum(axis=0).reshape(1, self.param.shape[1])

  def __repr__(self):
    return "AddBiais"
  


