import tensorflow as tf
from tensorflow import keras

import numpy as np
import matplotlib as plt


model = tf.keras.models.Sequential([
  tf.keras.layers.Dense(18, input_shape=('none')),
  tf.keras.layers.Dense(20),
  tf.keras.layers.Dense(20),
  tf.keras.layers.Dense(2)
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.BinaryCrossentropy(),
              metrics='accuracy')

