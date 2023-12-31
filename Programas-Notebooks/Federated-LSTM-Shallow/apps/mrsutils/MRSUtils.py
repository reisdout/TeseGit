# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 11:08:28 2023

@author: visitante
"""


#from sklearn.model_selection import train_test_split
from sys import exit
import numpy as np
import pandas as pd
import seaborn as sns; sns.set()
import os
import matplotlib.pyplot as plt
import seaborn as sns
import copy


print_output = False

def MyPrint(parDescriptions,parValues,parSameLine=True):
    
    if(not print_output):
        return;
    
    for i in range (len(parDescriptions)):
        if(parSameLine):
            if(parValues[i] == ' '):
                print(parDescriptions[i])
            else:
                print(parDescriptions[i], "==>", parValues[i])
        else:
            print(parDescriptions[i],":")
            print(parValues[i])
    

def binary(num, string=True):
    bits = np.unpackbits(np.array([num]).view('u1'))
    if string:
        return np.array2string(bits, separator='')[1:-1]
    else:
        return bits

def BinarizerFloat32(parNum):
    a = np.float32(parNum)
    arrbin = binary(a,False)
    #print(arrbin)
    
    bytes = np.zeros(4)
    
    bytenum = -1;
    
    for i in range(arrbin.shape[0]):
        if(not (i % 8)):
            bytenum += 1 
        bytes[bytenum] = bytes[bytenum] + arrbin[i]*pow(2,7-(i-(8*bytenum)))
    
    return bytes



def CutBase(parNorBase, parCorte):

  if(len(parNorBase) <= parCorte):
    print("Impossivel Cortar!")
    return parNorBase;

  cuted_base = parNorBase #copy.deepcopy(parMergedBase)
  #n1 = cuteded_base[cuteded_base.Network_Situation_Router_Arrival == 1].shape[0]
  #n2 = cuteded_base[cuteded_base.Network_Situation_Router_Arrival == 2].shape[0]

  numCorte = len(cuted_base) - parCorte;
  n = 0
  fase = 0;
  i=0 #Linha a ser cortada
  more1=True
  more2=True
  print("Tamanho do Corte: ", numCorte)
  while(n < numCorte):

    if(i >= cuted_base.shape[0]):
      i=0;

    if(fase == 0 and more1):
      if(more2):
          fase = 1
      while (i < cuted_base.shape[0]):
        if(cuted_base.iloc[i]['Network_Situation_Router_Arrival'] == 1):
          cuted_base.drop(cuted_base.index[i],inplace=True)
          n = n+1
          break
        i=i+1
      if(i == cuted_base.shape[0]):
        more1=False
        
    if(n == numCorte):
        break;
    i=0
    if (fase == 1 and more2):
      if(more1):
          fase=0
      while (i < cuted_base.shape[0]):
        if(cuted_base.iloc[i]['Network_Situation_Router_Arrival'] == 2):
          cuted_base.drop(cuted_base.index[i],inplace=True)
          n = n+1
          break
        i=i+1
      if(i == cuted_base.shape[0]):
        more2=False
    #print("Corte Atual :", n)
            
   
       
  cuted_base.reset_index(drop=True,inplace=True)
  cuted_base_sampled = cuted_base.sample(frac = 1).reset_index(drop=True)
  n1 = cuted_base_sampled[cuted_base_sampled.Network_Situation_Router_Arrival == 1].shape[0]
  n2 = cuted_base_sampled[cuted_base_sampled.Network_Situation_Router_Arrival == 2].shape[0]
  print("bases cuted")
  print("Total Features: ",n1+n2)
  return cuted_base_sampled;


 


def ReadNormalizationFactors(par_model_dir):
       
       ack_ewma_normalizer=1.0
       send_ewma_normalizer=1.0
       min_rtt = 1.0 
       rtt_ratio_normalizer=1.0
       cwnd_normalizer=1.0
       
       line_ref = 0 #criado para sair dos subtratores do SubtractMin()
     
       file1 = open(par_model_dir+"/normalization_factors.txt", 'r')
       Lines = file1.readlines()
       
       ack_ewma_normalizer = float(Lines[0+line_ref].split()[len(Lines[0+line_ref].split())-1])# split retorna uma lista com as strings da linha que estão separadas por espaço
       send_ewma_normalizer = float(Lines[1+line_ref].split()[len(Lines[1+line_ref].split())-1])
       min_rtt = float(Lines[2+line_ref].split()[len(Lines[2+line_ref].split())-1])
       rtt_ratio_normalizer=float(Lines[3+line_ref].split()[len(Lines[3+line_ref].split())-1])
       cwnd_normalizer=float(Lines[4+line_ref].split()[len(Lines[4+line_ref].split())-1])
       
       return ack_ewma_normalizer, send_ewma_normalizer,min_rtt, rtt_ratio_normalizer, cwnd_normalizer


def NormalizeFeatures(data, parFromFile,par_model_dir,parMinRtt=1.0):
       
       ack_ewma_normalizer=1.0
       send_ewma_normalizer=1.0
       min_rtt=1.0
       rtt_ratio_normalizer=1.0
       cwnd_normalizer=1.0
       
       #Obtendo o RTT Ratio
    
       #data['rtt_ratio'] = data['rtt_ratio'].div(264)#264 é o rtt min do fluxo de treinamento.
        
       if(parFromFile):
          ack_ewma_normalizer, send_ewma_normalizer,min_rtt,rtt_ratio_normalizer,cwnd_normalizer = ReadNormalizationFactors(par_model_dir)
  
        
       else: 
           ack_ewma_normalizer = data['ack_ewma(ms)'].max()
           send_ewma_normalizer=data['send_ewma(ms)'].max()
           min_rtt=parMinRtt
           cwnd_normalizer=data['cwnd_(Bytes)'].max()

       data['rtt_ratio'] = data['rtt_ratio'].div(min_rtt)
       if(not (parFromFile)):
           rtt_ratio_normalizer = data['rtt_ratio'].max()
       data['ack_ewma(ms)'] = data['ack_ewma(ms)'].div(ack_ewma_normalizer)
       data['send_ewma(ms)'] = data['send_ewma(ms)'].div(send_ewma_normalizer)       
       data['rtt_ratio'] = data['rtt_ratio'].div(rtt_ratio_normalizer)
       #data['rtt_ratio'] -=1
       
       data['cwnd_(Bytes)'] = data['cwnd_(Bytes)'].div(cwnd_normalizer)
        
       if(not parFromFile):# e treinamento
           file1 = open(par_model_dir+"/normalization_factors.txt", 'w')
           file1.writelines("ack_ewma: "+str(ack_ewma_normalizer)+"\n")
           file1.writelines("send_ewma: "+str(send_ewma_normalizer)+"\n")
           file1.writelines("rtt_min: "+str(min_rtt)+"\n")
           file1.writelines("rtt_ratio: "+str(rtt_ratio_normalizer)+"\n")
           file1.writelines("cwnd_(Bytes): "+str(cwnd_normalizer)+"\n")
           file1.close()
    
       #print(ack_ewma_normalizer)
       MyPrint(['ack_ewma_normalizer'], [ack_ewma_normalizer])
       #print(send_ewma_normalizer)
       MyPrint(['send_ewma_normalizer'],[send_ewma_normalizer])
       #print(min_rtt)
       MyPrint(['min_rtt'],[min_rtt])
       #print(rtt_ratio_normalizer)  
       MyPrint(['rtt_ratio_normalizer'],[rtt_ratio_normalizer])
       #print(cwnd_normalizer) 
       MyPrint(['cwnd_normalizer'],[cwnd_normalizer])
       #print("Eis os normalizadores acima")
       MyPrint(['Eis os normalizadores acima'], [' '])
       #a=input("Eis os normalizadores acima")
       #seguir = input("Deseja Prosseguir? (N/n-->Sair)")
    
       #if(seguir == 'n' or seguir =='N'):
         #exit()


       return data


def MilimizeFeatures(data,par_exp_dir):
       
       ack_ewma_normalizer=1.0
       send_ewma_normalizer=1.0
       min_rtt=1.0
       rtt_ratio_normalizer=1.0
       cwnd_normalizer=1.0
       
       ack_ewma_normalizer = 1000
       send_ewma_normalizer=1000
       min_rtt=data['rtt_ratio'].min()
       cwnd_normalizer=1000

       data['rtt_ratio'] = data['rtt_ratio'].div(min_rtt)
       rtt_ratio_normalizer = 1
       data['ack_ewma(ms)'] = data['ack_ewma(ms)'].div(ack_ewma_normalizer)
       data['send_ewma(ms)'] = data['send_ewma(ms)'].div(send_ewma_normalizer)       
       data['rtt_ratio'] = data['rtt_ratio'].div(rtt_ratio_normalizer)
       data['cwnd_(Bytes)'] = data['cwnd_(Bytes)'].div(cwnd_normalizer)
        

       #print("Normalizado por 1000")
       #a=input("Eis os normalizadores acima")
       #seguir = input("Deseja Prosseguir? (N/n-->Sair)")
    
       #if(seguir == 'n' or seguir =='N'):
         #exit()


       return data
   

def SubtractMean(data):
    
    data_mean = data.mean(axis=0)
    

    
    data['ack_ewma(ms)'] = data['ack_ewma(ms)'] - data_mean['ack_ewma(ms)']
    data['send_ewma(ms)'] = data['send_ewma(ms)']- data_mean ['send_ewma(ms)'] 
 
    #data['rtt_ratio'] = data['rtt_ratio']-data_mean['rtt_ratio']
    #data['cwnd (Bytes)'] = data['cwnd (Bytes)']-data.mean['cwnd (Bytes)']
    return data

def SubtractMin(data, parFromFile,par_exp_dir):
    
    
    print(data['ack_ewma(ms)'].min())
    print(data['send_ewma(ms)'].min())
    input("Eis os subtratores")
    
    data['ack_ewma(ms)'] = data['ack_ewma(ms)'] - data['ack_ewma(ms)'].min()
    data['send_ewma(ms)'] = data['send_ewma(ms)']- data['send_ewma(ms)'].min()
    '''
        O -1 abaixo é devido ao fato de o RTT ratio ser dividiod pelo menor.
        se não tiver o -1, alguns vão zerar e haverá,assim, uma divisão por 
        zero na hora de se obter o RTT Ratio
    '''
    data['rtt_ratio'] = data['rtt_ratio']-(data['rtt_ratio'].min()-1)
    #data['cwnd (Bytes)'] = data['cwnd (Bytes)']-data.mean['cwnd (Bytes)']
    
    if(not parFromFile):
        file1 = open(par_exp_dir+"/normalization_factors.txt", 'w')
        file1.writelines("min_ack_ewma: "+str(data['ack_ewma(ms)'].min())+"\n")
        file1.writelines("min_send_ewma: "+str(data['send_ewma(ms)'].min())+"\n")
        file1.writelines("rtt_min: "+str(data['rtt_ratio'].min()-1)+"\n")
        file1.close()
    
    return data
 


def DeleteInconsistences(data):
        
    last_consistent = 0
    
    clean_data = data
    
    rows_to_be_dropped=[]
    
    #print(data.shape[0])
    
    for i in range(data.shape[0]):
        if((data.iloc[last_consistent]['ack_ewma(ms)'] >  data.iloc[i]['ack_ewma(ms)'] or               
            data.iloc[last_consistent]['send_ewma(ms)'] > data.iloc[i]['send_ewma(ms)'] or
            data.iloc[last_consistent]['rtt_ratio'] >     data.iloc[i]['rtt_ratio']) and
            data.iloc[last_consistent]['Last_Router_Ocupation_Router_Arrival_ewma(Packets)']< 
            data.iloc[i]['Last_Router_Ocupation_Router_Arrival_ewma(Packets)']):
            
            rows_to_be_dropped.append(i)
            
        elif((data.iloc[last_consistent]['ack_ewma(ms)'] < data.iloc[i]['ack_ewma(ms)'] or               
            data.iloc[last_consistent]['send_ewma(ms)'] <  data.iloc[i]['send_ewma(ms)'] or
            data.iloc[last_consistent]['rtt_ratio'] <      data.iloc[i]['rtt_ratio']) and
            data.iloc[last_consistent]['Last_Router_Ocupation_Router_Arrival_ewma(Packets)']> 
            data.iloc[i]['Last_Router_Ocupation_Router_Arrival_ewma(Packets)']):
                
            rows_to_be_dropped.append(i)
                
        else:
            last_consistent = i
            
    clean_data.drop(labels=rows_to_be_dropped,axis=0,inplace=True)
    print("base limpa")
    return clean_data


'''
A função abaixo, recebe duas lista de bases,
uma, uma proveniente da leitura da chegada dos ACK
no terminal e a outra na leitura quando da chegada
do pacote no roteador. Elas devem estar casadas, ou seja
cada posição i das listas deve ser referir ao mesmo terminal
da simulação. Isto também vale para a lista de mapeamento de features,
ou seja as posições correspondem as features mapeadas nas em 1 e 2, para
cada base que passou pelo merge. Em geral é sempre assim:
    
    
           Correspondente aos arquivos levandados para o terminal 0              
              |       Correspondente aos arquivos levandados para o terminal 1
              |        |       Correspondente aos arquivos levandados para o terminal 2
              |        |       |
         |---------|-------|-------|
 lista   |         |       |       |.....................................................
         |---------|-------|-------|
    
'''

def MergeAndConcatBases(parLstBaseTerninais, parLstBaseRouter):
                       
    if(len (parLstBaseRouter) != len(parLstBaseTerninais)):
        print("Listas com quantidades incompatíveis")
        exit(0)
    
    lstMergedBases=[]
    
    #lstFeaturesMapeadas1Amount=[]
    #lstFeaturesMapeadas2Amount=[]
    
    
    for i in range (len(parLstBaseRouter)):
        #print("Merge ", i)
        lstMergedBases.append(pd.merge(parLstBaseTerninais[i],parLstBaseRouter[i], on='#Ack',how='inner'))
    
    #n1=lstMergedBases[0][lstMergedBases[0].Network_Situation_Router_Arrival == 1].shape[0] #features em 1 no arquivo 1
    n1=0;
    n2=0 #seria todas as features levadas em 2 nos arquivos
    '''
    for i in range (len(lstMergedBases)):
        lstFeaturesMapeadas1Amount.append(lstMergedBases[i][lstMergedBases[i].Network_Situation_Router_Arrival == 1].shape[0])
        lstFeaturesMapeadas2Amount.append(lstMergedBases[i][lstMergedBases[i].Network_Situation_Router_Arrival == 2].shape[0])
    
   
   
    
    for i in range (1,len(lstMergedBases)):
        lstMergedBases[i].drop(lstMergedBases[i][lstMergedBases[i]['Network_Situation_Router_Arrival'] ==1].index,inplace=True)
    '''

    merged_base = pd.concat(lstMergedBases,ignore_index=True)
    #merged_base.reset_index(drop=True,inplace=True)
    min_rtt = merged_base['rtt_ratio'].min()
    
    return merged_base, min_rtt


def BalanceBase(parMergedBase):
    
    balanced_base = parMergedBase #copy.deepcopy(parMergedBase)
    n1 = balanced_base[balanced_base.Network_Situation_Router_Arrival == 1].shape[0]
    n2 = balanced_base[balanced_base.Network_Situation_Router_Arrival == 2].shape[0]
    if(not n1 or not n2):
        return balanced_base

    i = 0
    
    if(n1 > n2):
        while (n1 > n2):
            
            #print ("(",i,",",n1,",",n2,")")
            
            if(i >= balanced_base.shape[0]):
                i=0;
           
            elif(balanced_base.iloc[i]['Network_Situation_Router_Arrival'] == 1):
                balanced_base.drop(balanced_base.index[i],inplace=True)
                n1 = n1-1;
                i=i+1
            elif i < balanced_base.shape[0]-1:
                i=i+1
            else:
                i=0
                
    elif(n2 > n1):
        while (n2 > n1):
            
            #print ("(",i,",",n1,",",n2,")")
            
            if(i >= balanced_base.shape[0]):
                i=0;
           
            elif(balanced_base.iloc[i]['Network_Situation_Router_Arrival'] == 2):
                balanced_base.drop(balanced_base.index[i],inplace=True)
                n2 = n2-1;
                i=i+1
            elif i < balanced_base.shape[0]-1:
                i=i+1
            else:
                i=0
    
    
    
    #print(n1,",",n2)
    
        
    balanced_base.reset_index(drop=True,inplace=True)
    balanced_base_sampled = balanced_base.sample(frac = 1).reset_index(drop=True)
    n1 = balanced_base_sampled[balanced_base_sampled.Network_Situation_Router_Arrival == 1].shape[0]
    n2 = balanced_base_sampled[balanced_base_sampled.Network_Situation_Router_Arrival == 2].shape[0]
    print("bases merged")
    print("Total Features: ",n1+n2)
    return balanced_base_sampled;




def TileBase(data):
    
    #quantil = 0.9 degrada muito o treino, mas o desempenho da CNN consegue superar a dificuldade
    #quantil = 0.8
    #quantil = 0.7 fica show
    rttTile = data['rtt_ratio'].quantile(0.9)
    ackTile = data['ack_ewma(ms)'].quantile(0.9)
    sendTile = data['send_ewma(ms)'].quantile(0.9)
    
    '''
    dataRTT_Tile = data.drop(data[data['rtt_ratio']> rttTile].index)
    dataAckTile = data.drop(data[data['ack_ewma(ms)'] > ackTile].index)
    dataSendTile = data.drop(data[data['send_ewma(ms)'] > sendTile].index)
    dataTileConcat = pd.concat([dataRTT_Tile,dataAckTile,dataSendTile],ignore_index=True)
    dataTileConcat.drop_duplicates(subset=['ack_ewma(ms)', 'send_ewma(ms)','rtt_ratio'],keep="last",ignore_index=True,inplace=True)
    return dataTileConcat
    '''
    data.drop(data[data['rtt_ratio']> rttTile].index,inplace=True)
    data.drop(data[data['ack_ewma(ms)'] > ackTile].index,inplace=True)
    data.drop(data[data['send_ewma(ms)'] > sendTile].index,inplace=True)
    data.reset_index(drop=True,inplace=True)
    print('liquiid data: ', data.shape[0])
    return data


def RenameFile(parExpPath, parInicialCount=1):
   

    print("Renomeando...")
    files = os.listdir(parExpPath)
    
    
    router_count =parInicialCount
    terminal_count=parInicialCount
    files.sort()
    #print (files)

    for file in files:
        if 'buffer' in  file:
            #print("Renomeando ", file)
            os.rename(os.path.join(parExpPath, file), os.path.join(parExpPath,'router'+str(router_count).zfill(2)+'.csv'))
            router_count = router_count+1
            
        elif "10_" in file:
            #print("Renomeando ", file)
            os.rename(os.path.join(parExpPath, file), os.path.join(parExpPath,'terminal'+str(terminal_count).zfill(2)+'.csv'))
            terminal_count = terminal_count+1
            
        else:
            print(file, " --> nao renomeado");
        
        
def PlotROC(parData,parLabels,parTitle):

    
    df = pd.DataFrame(parData) 
    
    
    tpr = df.iloc[:,[0]].values.T
    fpr = df.iloc[:,[1]].values.T
    tpr = tpr[0]
    fpr = fpr[0]
    
    numPoints = fpr.shape[0]
    
    #descricao_experimeto = ["5","10"]
    
    descricao_experimeto = parLabels
    
    #desloc_x_text=[0,-0.0007,0,0,0]
    desloc_x_text=[0.0030,0.0010,0.0010]
    
    #desloc_y_text=[-0.1,-0.06,-0.1,-0.07,-0.1]
    
    #desloc_y_text=[-0.1,-0.06,-0.1,-0.07,-0.1]
    desloc_y_text=[-0.01,-0.1,-0.1]
    
    y_max = max(tpr)
    y_min = min(tpr)
         
    x_min = min(fpr)
    x_max = max(fpr)
 
    if(numPoints > 1):
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
    else:
        
        x_bisse = np.zeros(2)
        y_bisse = np.zeros(2)
    
        x_bisse[0] = 0.0
        y_bisse[0] = 0.0
        x_bisse[1] = 2*x_min
        y_bisse[1] = x_bisse[1]
        
        

    
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
    
    roc = sns.lineplot(df,x="FPR",y="TPR", label= 'ROC por Fluxo',color ='blue', linewidth=1.5,ax=ax).set(title=parTitle)
    sns.scatterplot(df,x="FPR",y="TPR",ax=ax,color ='blue',s=50)
    invar = sns.lineplot(x=x_bisse, y=y_bisse, sort=False, color ='red', linewidth=1.5,label="TPR=FPR",ax=ax)
    
    #Calculando as distancias do modelo sem discernimento y=x
    for i in range(numPoints):
        sns.lineplot(x=[fpr[i],fpr[i]], y=[fpr[i],tpr[i]], sort=False, color ='purple', estimator=None, linewidth=2.5,linestyle='dashed',ax=ax)
        plt.text(x = fpr[i]+desloc_x_text[i], # x-coordinate position of data label
                 y = (fpr[i]+tpr[i])/2, # y-coordinate position of data label, adjusted to be 150 below the data point
                 s="{0:.3f}".format((tpr[i]-fpr[i])),#s = str(((tpr[i]-fpr[i])/2)), # data label, formatted to ignore decimals
                 color = 'purple') # set colour of line

    #line = invar.get_lines()
    #plt.fill_between(line[0].get_xdata(), line[1].get_ydata(),line[0].get_ydata(), color='green', label="AUC",alpha=.12)
    
    
    # label points on the plot
    i=0
    for x in fpr:
     # the position of the data label relative to the data point can be adjusted by adding/subtracting a value from the x &/ y coordinates
     plt.text(x = x+desloc_x_text[i], # x-coordinate position of data label
     y = tpr[i]+desloc_y_text[i], # y-coordinate position of data label, adjusted to be 150 below the data point
     s = descricao_experimeto[i], # data label, formatted to ignore decimals
     color = 'purple') # set colour of line
     i=i+1
    
    plt.legend(loc='lower left')
    #plt.savefig('../../ROC.pdf')
    plt.show()
    
    
data = {'TPR': [1,       1           , 0.994715984147952 , 0.996268656716418 ,       1],
        'FPR': [0, 0.0106194690265487, 0.0126050420168067, 0.0108695652173913,0.00754716981132076]} 
df = pd.DataFrame(data) 


tpr = df.iloc[:,[0]].values.T
fpr = df.iloc[:,[1]].values.T

tpr = tpr[0]
fpr = fpr[0]

#PlotROC(data)




def ConstructROCGraph(parConfusionMatrizes, parPointLabels, parTitle):
    print("em construçao")
    if(len(parConfusionMatrizes) != len(parPointLabels)):
        print("Dimensoes incompativeis")
        return
    
 
    lstTPRs =  []
    lstFPRs =  []
    
    for i in range (len (parConfusionMatrizes)):
        if(not (parConfusionMatrizes[i][0][1]+parConfusionMatrizes[i][1][1])):
            print("Impossivel Construir Grafico ROC")
            return
        temp_TPR = parConfusionMatrizes[i][1][1]/(parConfusionMatrizes[i][0][1]+parConfusionMatrizes[i][1][1])
        lstTPRs.append(temp_TPR)
        if(not (parConfusionMatrizes[i][0][0]+parConfusionMatrizes[i][1][0])):
            print("Impossivel construir grafico ROC")
            return
        temp_FPR = parConfusionMatrizes[i][1][0]/(parConfusionMatrizes[i][0][0]+parConfusionMatrizes[i][1][0])
        lstFPRs.append(temp_FPR)
    
    data = {'TPR': lstTPRs,
            'FPR': lstFPRs} 

    PlotROC(data,parPointLabels,parTitle)

        
        
        
        


        
        
        