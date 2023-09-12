# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 16:00:02 2023

@author: visitante
"""

from keras.models import Model
from keras.layers import Input
from keras.models import Sequential
from keras.layers import LSTM,Dense
from numpy import array
import keras
k_init = keras.initializers.Constant(value=0.1)
b_init = keras.initializers.Constant(value=0)
r_init = keras.initializers.Constant(value=0.1)
# LSTM units
units = 1
regressor = Sequential()
# define model
inputs1 = Input(shape=(3, 2))
#lstm1 = LSTM(units, return_sequences=True, kernel_initializer=k_init, bias_initializer=b_init, recurrent_initializer=r_init)(inputs1)
regressor.add(LSTM(units = units, return_sequences = True, input_shape = (3,2)))
regressor.add(Dense(units = 5, activation = 'sigmoid'))



#model = Model(inputs=inputs1, outputs=lstm1)
#regressor.add(lstm1)
# define input data
data = array([0.1, 0.2, 0.3, 0.1, 0.2, 0.3]).reshape((1,3,2))
# make and show prediction
output = regressor.predict(data)
print(output, output.shape)