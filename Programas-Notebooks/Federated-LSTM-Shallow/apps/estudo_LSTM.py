#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 15:17:55 2023

@author: ns
"""

import numpy as np
import pandas as pd
#import keras
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM#, Bidirectional
#from sklearn.preprocessing import LabelEncoder
#from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from GeneralClient import Client
from GeneralClient import LoggingCallback
#from keras.utils import np_utils
#from tensorflow.keras import utils


model = Sequential()

model.add(LSTM(3, input_shape=(2,3),  return_sequences=True))
model.add(LSTM(1,return_sequences=True))
#model.add(Dense(units = 1, activation = 'sigmoid'))#para uma previsão
model.summary()
