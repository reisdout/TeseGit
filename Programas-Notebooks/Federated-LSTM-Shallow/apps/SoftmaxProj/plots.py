#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 21:24:11 2023

@author: ns
"""

import matplotlib.pyplot as plt
import numpy as np


time = np.array([0,0.001,0.003,0.006,0.0126])
fpr = np.array([ 0, 0.0106194690265487, 0.0126050420168067, 0.0108695652173913,0.00754716981132076])
tpr = np.array([1, 1, 0.994715984147952, 0.996268656716418,1])

# Initialize figure and axis
fig, ax = plt.subplots(figsize=(5, 5))

ax.set_xlim(left=0, right=0.013)
ax.set_ylim(bottom=-0.020, top=1.01)

# Plot lines
ax.plot(np.array([0,0.0126]), np.array([0,0.0126]), color="green",linewidth=3)
ax.plot(fpr, tpr, color="red",linewidth=3)
ax.set_facecolor('white')

for axis in ['top', 'bottom', 'left', 'right']:
  ax.spines[axis].set_color('black')

# Fill area when income > expenses with green
ax.fill_between(
    time, tpr, fpr, where=(tpr > fpr), 
    interpolate=True, color="blue", alpha=0.15, 
    label="AUC"
)

"""
# Fill area when income <= expenses with red
ax.fill_between(
    time, income, expenses, where=(income <= expenses), 
    interpolate=True, color="red", alpha=0.25,
    label="Negative"
)
"""

ax.legend();



