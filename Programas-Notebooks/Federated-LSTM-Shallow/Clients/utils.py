# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 11:08:28 2023

@author: visitante
"""


from sklearn.model_selection import train_test_split
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
