#omgamganapathayenamaha
#omgamganapathayenamaha
#omgamganapathayenamaha
#omgamganapathayenamaha
#omgamganapathayenamaha
import tensorflow as tf
class omgamganapathayenamaha:
  def __init__(self, num_classes=10, input_shape=(784,), input_dtype=tf.float64, output_activation="softmax"):
    inputs = tf.keras.layers.Input(shape=input_shape, dtype=input_dtype)
    x = tf.keras.layers.Dense(units=128, activation="relu")(inputs)
    x = tf.keras.layers.Dropout(0.2)(x)
    x = tf.keras.layers.Dense(units=128, activation="relu")(x)
    x = tf.keras.layers.Dropout(0.2)(x)
    x = tf.keras.layers.Dense(units=128, activation="relu")(x)
    x = tf.keras.layers.Dropout(0.2)(x)
    outputs = tf.keras.layers.Dense(units=num_classes, activation=output_activation)(x)
    model = tf.keras.Model(inputs,outputs)
    model.compile(optimizer='adam', loss=tf.keras.losses.SparseCategoricalCrossentropy(), metrics=tf.keras.metrics.SparseCategoricalAccuracy())
    self.__model__ = model

  def __getattr__(self, name):
    def method(*args, **kargs):
      try:
        class_method = getattr(self.__model__, name)
        self.result = class_method(*args, **kargs)
        return self.result
      except Exception as e:
        print(e)
    return method
