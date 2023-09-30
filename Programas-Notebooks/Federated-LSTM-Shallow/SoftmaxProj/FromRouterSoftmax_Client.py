# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 11:24:45 2023

@author: visitante

Este arquivo define uma classe cliente, que eatá preparada para 
realizar o treinamento de uma rede neural softmax, com dados
provenientes das leituras das features (ack_ewma, send_ewma e rtt_ratio)
no momento da chegada do segmento no roteador. As features são associadas às
respectivas ocupações nas filas por meio do merge no número de sequencia (seq)
Essa classe é , também, um cliente softmax, por isso deriva de Cleint
"""
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from GeneralAckSoftmax_Client import Client
from keras.utils import np_utils
import MRSUtils as mrs


class ClientBufferArrival(Client):
    
    def __init__(self,parId,parExperimentPath,parBasePath, parPacketsArrivedRoutherPath):
        
        super().__init__(parId,parExperimentPath,parBasePath)
        
        self.packetsArrivedRoutherPath = parPacketsArrivedRoutherPath
        
        
        
    def LoadTrainingDataSet(self, parFromFile=False):
        print ("Configurando dados tomados da chegada na fila....")
        
        
        
       
        
        base_ack_terminal00 = pd.read_csv(self.basePath)
        
        base_ack_terminal01 = pd.read_csv( '../Exp_0000038/terminal01.csv')
        
        base_ack_terminal02 = pd.read_csv( '../Exp_0000038/terminal02.csv')
        
        base_ack_terminal03 = pd.read_csv( '../Exp_0000038/terminal03.csv')
        
        base_packet_router00 = pd.read_csv(self.packetsArrivedRoutherPath)        
        base_packet_router01 = pd.read_csv( '../Exp_0000038/router01.csv')
        base_packet_router02 = pd.read_csv( '../Exp_0000038/router02.csv')
        base_packet_router03 = pd.read_csv( '../Exp_0000038/router03.csv')
        
        
        base_ack_terminal00.columns =  base_ack_terminal00.columns.str.replace(' ','_')
        base_ack_terminal01.columns =  base_ack_terminal01.columns.str.replace(' ','_')       
        base_ack_terminal02.columns =  base_ack_terminal02.columns.str.replace(' ','_')
        base_ack_terminal03.columns =  base_ack_terminal03.columns.str.replace(' ','_')     
        base_packet_router00.columns = base_packet_router00.columns.str.replace(' ','_')      
        base_packet_router01.columns = base_packet_router01.columns.str.replace(' ','_')
        base_packet_router02.columns = base_packet_router02.columns.str.replace(' ','_')
        base_packet_router03.columns = base_packet_router03.columns.str.replace(' ','_')
        
        
        
        base_merged = mrs.MergeAndConcatBases(base_ack_terminal00,
                                   base_ack_terminal01,
                                   base_ack_terminal02,
                                   base_ack_terminal03,
                                   base_packet_router00,
                                   base_packet_router01,
                                   base_packet_router02,
                                   base_packet_router03)
        
        
        #base = pd.merge(base_ack_terminal,base_packet_router, on='#Ack',how='inner')
        
        base_merged.drop_duplicates(subset=['ack_ewma(ms)', 'send_ewma(ms)','rtt_ratio'],keep="last",ignore_index=True)
        base_consistent = mrs.DeleteInconsistences(base_merged)
        #base = SubtractMin(base,parFromFile,self.experimentPath)
        base = mrs.NormalizeFeatures(base_consistent,parFromFile,self.experimentPath)
        previsores = base.iloc[:, [1,2,3]].values        
        classe = base.iloc[:, 13].values
        
        labelencoder = LabelEncoder()
        classe = labelencoder.fit_transform(classe)
        classe_dummy = np_utils.to_categorical(classe)
        # sem congestionamento    1 0 0
        #congestionamento medio 0 1 0
        # alto congestionamento 0 0 1

        #print (classe_dummy[363:,:])
        
        #a = input("acima, a Classe dummy. Deseja Prosseguir? ")
        #if (a == 'N' or a == 'n'):
            #exit()


        previsores_treinamento, previsores_teste, classe_treinamento, classe_teste = train_test_split(previsores, classe_dummy, test_size=0.20)
        
        return previsores_treinamento, previsores_teste, classe_treinamento, classe_teste
    
        
        
        '''
        
 
 
        


        '''
        