#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 11:20:27 2023

@author: ns
"""

from keras2c import k2c

modelPath = './Selected_Models/CNN_ACK_RTT/keras2c_model_CNN_ACK_ewma_RTT_ratio'



k2c(modelPath, 'keras2c_model', malloc=False, num_tests=10, verbose=True)