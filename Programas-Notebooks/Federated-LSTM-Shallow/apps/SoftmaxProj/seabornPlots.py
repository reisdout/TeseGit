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


def PlotROC(parData,parLabels):

    
    df = pd.DataFrame(parData) 
    
    
    tpr = df.iloc[:,[0]].values.T
    fpr = df.iloc[:,[1]].values.T
    tpr = tpr[0]
    fpr = fpr[0]
    
    numPoints = fpr.shape[0]
    
    #descricao_experimeto = ["5","10"]
    
    descricao_experimeto = parLabels
    
    #desloc_x_text=[0,-0.0007,0,0,0]
    desloc_x_text=[0,0]
    
    #desloc_y_text=[-0.1,-0.06,-0.1,-0.07,-0.1]
    
    #desloc_y_text=[-0.1,-0.06,-0.1,-0.07,-0.1]
    desloc_y_text=[-0.1,-0.1]
    
    y_max = max(tpr)
    y_min = min(tpr)
         
    x_min = min(fpr)
    x_max = max(fpr)
 
    
    pass_bisse = (x_max-x_min)/(numPoints-1)  
    #x_bisse = np.array([0,0.003,0.006,0.010,0.0126050420168067])
    #y_bisse = np.array([0,0.003,0.006,0.010,0.0126050420168067])
    x_bisse = np.zeros(numPoints)
    y_bisse = np.zeros(numPoints)

    x_bisse[0] = x_min
    y_bisse[0] = x_min
    
    

    for i in range(1,numPoints):
        x_bisse[i] = x_bisse[0]+i*pass_bisse
        y_bisse[i] = x_bisse[i]
    
    # Create the pandas DataFrame 
    
    fig = plt.figure(figsize=(20,20))
    # print dataframe. 
    fig, ax = plt.subplots()
    #ax.set_xlim(left=-0.0015, right=0.015)
    #ax.set_xlim(left=x_min-0.0015, right=x_max+0.015)
    #ax.set_ylim(bottom=-0.020, top=1.05)
    #ax.set_ylim(bottom=y_min-0.020, top=y_max+1.05)
    
    custom_params = {"axes.spines.right": False, "axes.spines.top": False}
    sns.set_theme(style="ticks", rc=custom_params)
    sns.set_theme(style="whitegrid", palette="pastel")
    
    
    
    sns.axes_style("ticks")
    
    roc = sns.lineplot(df,x="FPR",y="TPR", label= 'ROC por Fluxo',color ='blue', linewidth=1.5,ax=ax).set(title="ROC - Modelo 20 Fluxos")
    sns.scatterplot(df,x="FPR",y="TPR",ax=ax,color ='blue',s=50)
    invar = sns.lineplot(x=x_bisse, y=y_bisse, sort=False, color ='red', linewidth=1.5,label="TPR=FPR",ax=ax)
    
    line = invar.get_lines()
    plt.fill_between(line[0].get_xdata(), line[1].get_ydata(),line[0].get_ydata(), color='green', label="AUC",alpha=.12)
    
    
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
    
    
data = {'TPR': [1,       1           , 0.994715984147952 , 0.996268656716418 ,       1],
        'FPR': [0, 0.0106194690265487, 0.0126050420168067, 0.0108695652173913,0.00754716981132076]} 
df = pd.DataFrame(data) 


tpr = df.iloc[:,[0]].values.T
fpr = df.iloc[:,[1]].values.T

tpr = tpr[0]
fpr = fpr[0]

#PlotROC(data)




def ConstructROCGraph(parConfusionMatrizes, parPointLabels):
    print("em construçao")
    if(len(parConfusionMatrizes) != len(parPointLabels)):
        print("Dimensoes incompativeis")
        return
    
 
    lstTPRs =  []
    lstFPRs =  []
    
    for i in range (len (parConfusionMatrizes)):
        temp_TPR = parConfusionMatrizes[i][1][1]/(parConfusionMatrizes[i][0][1]+parConfusionMatrizes[i][1][1])
        lstTPRs.append(temp_TPR)
        temp_FPR = parConfusionMatrizes[i][1][0]/(parConfusionMatrizes[i][0][0]+parConfusionMatrizes[i][1][0])
        lstFPRs.append(temp_FPR)
    
    data = {'TPR': lstTPRs,
            'FPR': lstFPRs} 

    PlotROC(data,parPointLabels)
cf1 = np.array([[854,0],[34,781]])
cf2 = np.array([[554,4],[36,787]])
lstCFs = [cf1,cf2]
lstLabels = ["40 MLP","10 CNN"]

ConstructROCGraph(lstCFs, lstLabels)




    
    
    
    