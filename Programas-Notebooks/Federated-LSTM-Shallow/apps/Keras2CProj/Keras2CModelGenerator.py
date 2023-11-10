#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 11:20:27 2023

@author: ns
"""

from keras2c import k2c

modelPath = '/home/ns/TeseGit/Programas-Notebooks/Federated-LSTM-Shallow/apps/SigmoidProj/keras2c_model'

k2c(modelPath, 'keras2c_model', malloc=False, num_tests=10, verbose=True)