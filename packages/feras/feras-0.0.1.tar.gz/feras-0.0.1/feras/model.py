from copy import deepcopy
import pickle

class Model():

  def __init__(self, layers):
    self.layers = layers
    self.compiled = False


  def forward(self, inputs):


    for layer in self.layers:

      inputs = layer.forward(inputs)
    self.output = inputs
    return self.output


  def backward(self, loss_derivee):

    assert loss_derivee.shape == self.output.shape

    for layer in reversed(self.layers):
      loss_derivee = layer.backward(loss_derivee)

    return None
  

  def get_params(self):
    for layer in self.layers:
      yield from layer.params


  def get_derivee_params(self):
    for layer in self.layers:
      yield from layer.derivee_params


  def update(self):

    for (param, derivee_param) in zip(self.get_params(), self.get_derivee_params()):
      assert param.shape == derivee_param.shape
      param -=   self.learning_rate * derivee_param


  def compile(self, loss, learning_rate):
    self.loss = loss
    self.learning_rate = learning_rate
    self.compiled = True


  def fit(self, X, Y, epochs, validation_data=None):

    if validation_data:
      assert len(validation_data) == 2
      assert validation_data[0].shape[1] == X.shape[1]
      assert validation_data[1].shape[1] == Y.shape[1]

    self.history = {"loss":[]}
    if validation_data:
      self.history['val_loss'] = []


    if not self.compiled:
      raise NotImplementedError("Pas de loss et de learning_rate: Compilez")

    for epoch in range(epochs):
      # forward pass
      predictions = self.forward(X)
      loss = self.loss.forward(predictions, Y)
      self.history['loss'].append(loss)


      # val loss
      if validation_data:
        val_preds = self.forward(validation_data[0])
        val_loss = self.loss.forward(val_preds, validation_data[1])
        self.history['val_loss'].append(val_loss)

      log = f'Epoch {epoch+1} .............. loss : {loss}'
      if validation_data:
        log += f"  ....val_loss : {val_loss}"
      print(log)



      # backward pass
      loss_derivee = self.loss.backward()
      self.backward(loss_derivee)

      # update
      self.update()

    return self.history

  def save_model(self, file):
    model_save = deepcopy(self)

    import pickle
    with open(file, "wb") as f:
      pickle.dump(model_save, f)


  def __repr__(self):

    r = "Layers ................."
    for layer in self.layers:
      r += f" \n {str(layer)}"

    return r
  


def load_model(file):
  with open(file, 'rb') as f:
    model_load = pickle.load(f)
  return model_load