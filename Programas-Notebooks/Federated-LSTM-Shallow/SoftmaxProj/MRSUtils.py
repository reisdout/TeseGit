# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 11:08:28 2023

@author: visitante
"""


#from sklearn.model_selection import train_test_split
import pandas as pd
import seaborn as sns; sns.set()

def ReadNormalizationFactors(par_exp_dir):
       
       ack_ewma_normalizer=1.0
       send_ewma_normalizer=1.0
       min_rtt = 1.0 
       rtt_ratio_normalizer=1.0
       cwnd_normalizer=1.0
       
       line_ref = 3 #criado para sair dos subtratores do SubtractMin()
     
       file1 = open(par_exp_dir+"/normalization_factors.txt", 'r')
       Lines = file1.readlines()
       
       ack_ewma_normalizer = float(Lines[0+line_ref].split()[len(Lines[0+line_ref].split())-1])# split retorna uma lista com as strings da linha que estão separadas por espaço
       send_ewma_normalizer = float(Lines[1+line_ref].split()[len(Lines[1+line_ref].split())-1])
       min_rtt = float(Lines[2+line_ref].split()[len(Lines[2+line_ref].split())-1])
       rtt_ratio_normalizer=float(Lines[3+line_ref].split()[len(Lines[3+line_ref].split())-1])
       cwnd_normalizer=float(Lines[4+line_ref].split()[len(Lines[4+line_ref].split())-1])
       
       return ack_ewma_normalizer, send_ewma_normalizer,min_rtt, rtt_ratio_normalizer, cwnd_normalizer


def NormalizeFeatures(data, parFromFile,par_exp_dir):
       
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
           min_rtt=data['rtt_ratio'].min()
           cwnd_normalizer=data['cwnd_(Bytes)'].max()

       data['rtt_ratio'] = data['rtt_ratio'].div(min_rtt)
       if(not (parFromFile)):
           rtt_ratio_normalizer = data['rtt_ratio'].max()
       data['ack_ewma(ms)'] = data['ack_ewma(ms)'].div(ack_ewma_normalizer)
       data['send_ewma(ms)'] = data['send_ewma(ms)'].div(send_ewma_normalizer)       
       data['rtt_ratio'] = data['rtt_ratio'].div(rtt_ratio_normalizer)
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


def MergeAndConcatBases(bt00,
                        bt01,
                        bt02,
                        bt03,
                        br00,
                        br01,
                        br02,
                        br03):

    
    base00 = pd.merge(bt00,br00, on='#Ack',how='inner')
    base01 = pd.merge(bt01,br01, on='#Ack',how='inner')
    base02 = pd.merge(bt02,br02, on='#Ack',how='inner')
    base03 = pd.merge(bt03,br03, on='#Ack',how='inner')
    
    #base01 = base01.drop(base01[base01['Network_Situation_Router_Arrival'] ==1].index).reset_index() #reset_index para colocar os índices na sequencia
    #base02 = base02.drop(base02[base02['Network_Situation_Router_Arrival'] ==1].index).reset_index() #reset_index para colocar os índices na sequencia
    base03_droped = base03.drop(base03[base03['Network_Situation_Router_Arrival'] ==1].index).reset_index() #reset_index para colocar os índices na sequencia


    
    n1 = base02[base02.Network_Situation_Router_Arrival == 1].shape[0]
    n2 = base02[base02.Network_Situation_Router_Arrival == 2].shape[0]
    
    #while (n2 < n1)
    #balanced_df = pd.concat([base02,base00]).reset_index()
    
    #balanced_list = [base02,base00]
    
   # balanced_df = pd.concat(balanced_list)
    balanced_df= pd.concat([base02,base03_droped],ignore_index=True)
    balanced_df=balanced_df.drop('index', axis =1) # devido ao fato de a concatenação estar duplicando o index
    
    
    n1 = balanced_df[balanced_df.Network_Situation_Router_Arrival == 1].shape[0]
    n2 = balanced_df[balanced_df.Network_Situation_Router_Arrival == 2].shape[0]
    
    i = 0
    while (n1 > n2):
        
        print ("(",i,",",n1,",",n2,")")
       
        if(balanced_df.iloc[i]['Network_Situation_Router_Arrival'] == 1):
            balanced_df.drop(balanced_df.index[i],inplace=True)
            n1 = n1-1;
            i=i+1
        elif i < balanced_df.shape[0]-1:
            i=i+1
        else:
            i=0
    balanced_df.reset_index()
    balanced_df_sampled = balanced_df.sample(frac = 1).reset_index(drop=True)
    n1 = balanced_df[balanced_df.Network_Situation_Router_Arrival == 1].shape[0]
    n2 = balanced_df[balanced_df.Network_Situation_Router_Arrival == 2].shape[0]
    print("bases merged")
    return balanced_df_sampled
    
    



