#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 17:37:06 2023

@author: ns
"""






import numpy as np

def binary(num, string=True):
    bits = np.unpackbits(np.array([num]).view('u1'))
    if string:
        return np.array2string(bits, separator='')[1:-1]
    else:
        return bits

#a = np.float32(3.4)
a = np.float32(0.0620017)
arrbin = binary(a,False)
print(arrbin)

bytes = np.zeros(4)

bytenum = -1;

for i in range(arrbin.shape[0]):
    if(not (i % 8)):
        bytenum += 1 
    bytes[bytenum] = bytes[bytenum] + arrbin[i]*pow(2,7-(i-(8*bytenum)))
    
    
print(bytes)