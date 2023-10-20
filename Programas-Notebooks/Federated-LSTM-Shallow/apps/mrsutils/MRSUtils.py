# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 11:08:28 2023

@author: visitante
"""


#from sklearn.model_selection import train_test_split
from sys import exit
import pandas as pd
import seaborn as sns; sns.set()
import os

def ReadNormalizationFactors(par_exp_dir):
       
       ack_ewma_normalizer=1.0
       send_ewma_normalizer=1.0
       min_rtt = 1.0 
       rtt_ratio_normalizer=1.0
       cwnd_normalizer=1.0
       
       line_ref = 0 #criado para sair dos subtratores do SubtractMin()
     
       file1 = open(par_exp_dir+"/normalization_factors.txt", 'r')
       Lines = file1.readlines()
       
       ack_ewma_normalizer = float(Lines[0+line_ref].split()[len(Lines[0+line_ref].split())-1])# split retorna uma lista com as strings da linha que estão separadas por espaço
       send_ewma_normalizer = float(Lines[1+line_ref].split()[len(Lines[1+line_ref].split())-1])
       min_rtt = float(Lines[2+line_ref].split()[len(Lines[2+line_ref].split())-1])
       rtt_ratio_normalizer=float(Lines[3+line_ref].split()[len(Lines[3+line_ref].split())-1])
       cwnd_normalizer=float(Lines[4+line_ref].split()[len(Lines[4+line_ref].split())-1])
       
       return ack_ewma_normalizer, send_ewma_normalizer,min_rtt, rtt_ratio_normalizer, cwnd_normalizer


def NormalizeFeatures(data, parFromFile,par_exp_dir,parMinRtt=1.0):
       
       ack_ewma_normalizer=1.0
       send_ewma_normalizer=1.0
       min_rtt=1.0
       rtt_ratio_normalizer=1.0
       cwnd_normalizer=1.0
       
       #Obtendo o RTT Ratio
    
       #data['rtt_ratio'] = data['rtt_ratio'].div(264)#264 é o rtt min do fluxo de treinamento.
        
       if(parFromFile):
          ack_ewma_normalizer, send_ewma_normalizer,min_rtt,rtt_ratio_normalizer,cwnd_normalizer = ReadNormalizationFactors(par_exp_dir)
  
        
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
        
       if(not parFromFile):
           file1 = open(par_exp_dir+"/normalization_factors.txt", 'w')
           file1.writelines("ack_ewma: "+str(ack_ewma_normalizer)+"\n")
           file1.writelines("send_ewma: "+str(send_ewma_normalizer)+"\n")
           file1.writelines("rtt_min: "+str(min_rtt)+"\n")
           file1.writelines("rtt_ratio: "+str(rtt_ratio_normalizer)+"\n")
           file1.writelines("cwnd_(Bytes): "+str(cwnd_normalizer)+"\n")
           file1.close()
    
       print(ack_ewma_normalizer) 
       print(send_ewma_normalizer)
       print(min_rtt)
       print(rtt_ratio_normalizer)
       print(cwnd_normalizer) 
       print("Eis os normalizadores acima")
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

    balanced_base = pd.concat(lstMergedBases,ignore_index=True)
    min_rtt = balanced_base['rtt_ratio'].min()
    
    n1 = balanced_base[balanced_base.Network_Situation_Router_Arrival == 1].shape[0]
    n2 = balanced_base[balanced_base.Network_Situation_Router_Arrival == 2].shape[0]

    i = 0
    
    if(n1 > n2):
        while (n1 > n2):
            
            print ("(",i,",",n1,",",n2,")")
            
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
            
            print ("(",i,",",n1,",",n2,")")
            
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
    
    
    
    print(n1,",",n2)
        
    balanced_base.reset_index(drop=True,inplace=True)
    balanced_base_sampled = balanced_base.sample(frac = 1).reset_index(drop=True)
    n1 = balanced_base[balanced_base.Network_Situation_Router_Arrival == 1].shape[0]
    n2 = balanced_base[balanced_base.Network_Situation_Router_Arrival == 2].shape[0]
    print("bases merged")
    return balanced_base_sampled, min_rtt


def TileBase(data):
    
    rttTile = data['rtt_ratio'].quantile(0.9)
    ackTile = data['ack_ewma(ms)'].quantile(0.7)
    sendTile = data['send_ewma(ms)'].quantile(0.7)
    
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
    return data


def RenameFile(parExpPath, parInicialCount=1):
   

   
    files = os.listdir(parExpPath)
    
    
    router_count =parInicialCount
    terminal_count=parInicialCount
    files.sort()
    print (files)

    for file in files:
        if 'buffer' in  file:
            print("Renomeando ", file)
            os.rename(os.path.join(parExpPath, file), os.path.join(parExpPath,'router'+str(router_count).zfill(2)+'.csv'))
            router_count = router_count+1
            
        elif "10_" in file:
            print("Renomeando ", file)
            os.rename(os.path.join(parExpPath, file), os.path.join(parExpPath,'terminal'+str(terminal_count).zfill(2)+'.csv'))
            terminal_count = terminal_count+1
            
        else:
            print(file, " --> nao renomeado");
        
        
        
        
        
        
        


        
        
        