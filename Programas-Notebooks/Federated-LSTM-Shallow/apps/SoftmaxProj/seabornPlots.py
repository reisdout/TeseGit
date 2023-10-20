#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 09:32:03 2023

@author: ns
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd 
import numpy as np

  
# initialize list of lists 


data = {'FPR': [0, 0.0106194690265487, 0.0126050420168067, 0.0108695652173913,0.00754716981132076], 
        'TPR': [1,       1           , 0.994715984147952 , 0.996268656716418 ,       1]} 
  

fpr = np.array([ 0, 0.0106194690265487, 0.0126050420168067, 0.0108695652173913,0.00754716981132076])
tpr = np.array([ 1,        1          , 0.994715984147952 , 0.996268656716418 ,1])

descricao_experimeto = ["5","10","20","30","40"]
desloc_x_text=[0,-0.0007,0,0,0]
desloc_y_text=[-0.1,-0.06,-0.1,-0.07,-0.1]

x_bisse = np.array([0,0.003,0.006,0.010,0.013])
y_bisse = np.array([0,0.003,0.006,0.010,0.013])
# Create the pandas DataFrame 
df = pd.DataFrame(data) 
fig = plt.figure(figsize=(20,20))
# print dataframe. 
fig, ax = plt.subplots()
ax.set_xlim(left=-0.002, right=0.015)
ax.set_ylim(bottom=-0.020, top=1.05)

custom_params = {"axes.spines.right": False, "axes.spines.top": False}
sns.set_theme(style="ticks", rc=custom_params)
sns.set_theme(style="whitegrid", palette="pastel")



sns.axes_style("ticks")

roc = sns.lineplot(df,x="FPR",y="TPR", label= 'ROCXFluxos',color ='blue', linewidth=1.5,ax=ax).set(title="ROC - Modelo 20 Fluxos")
sns.scatterplot(df,x="FPR",y="TPR",ax=ax,color ='blue',s=50)
invar = sns.lineplot(x=x_bisse, y=y_bisse, sort=False, color ='red', linewidth=1.5,label="No Sense",ax=ax)

line = invar.get_lines()
plt.fill_between(line[1].get_xdata(), line[1].get_ydata(),line[0].get_ydata(), color='green', label="AUC",alpha=.12)

# label points on the plot
i=0
for x in fpr:
 # the position of the data label relative to the data point can be adjusted by adding/subtracting a value from the x &/ y coordinates
 plt.text(x = x+desloc_x_text[i], # x-coordinate position of data label
 y = tpr[i]+desloc_y_text[i], # y-coordinate position of data label, adjusted to be 150 below the data point
 s = descricao_experimeto[i], # data label, formatted to ignore decimals
 color = 'purple') # set colour of line
 i=i+1

plt.legend(loc='center right')
plt.savefig('../../ROC.pdf')
plt.show()