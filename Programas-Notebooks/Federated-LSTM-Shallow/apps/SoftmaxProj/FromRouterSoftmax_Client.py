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
from sys import exit
import sys
sys.path.append('../mrsutils')

import MRSUtils as mrs



class ClientBufferArrival(Client):
    
    def __init__(self,parId,parExperimentPath,parBasePath,parLstBasesTerminalsPaths, parLstBasesRoutersPaths):
           
        print(parLstBasesTerminalsPaths)
        print(parLstBasesRoutersPaths)
        input()
        if(len (parLstBasesTerminalsPaths) != len(parLstBasesRoutersPaths)):
            print("Listas com quantidades incompatíveis")
            exit(0);
        self.minRTT=1;
        self.lstBaseTerminalsPath = parLstBasesTerminalsPaths
        self.lstBaseRoutersPath = parLstBasesRoutersPaths
        #self.previsores_treinamento=[]
        #self.previsores_teste = [] 
        #self.classe_treinamento = [] 
        #self.classe_teste = []
        super().__init__(parId,parExperimentPath,parBasePath)


        
        
        
    def LoadTrainingDataSet(self, parFromFile=False):
        print ("Configurando dados tomados da chegada na fila....")
        
        
        lstBaseTerminals=[]
        lstBaseRouters=[]
        
        print(self.lstBaseTerminalsPath)
        
        #df = pd.read_csv(self.lstBaseTerminalsPath[0])
        '''
        mrs
        '''
        for i in range(len(self.lstBaseRoutersPath)):        
            lstBaseTerminals.append(pd.read_csv(self.lstBaseTerminalsPath[i],dtype={
                '#Ack': 'int',
                'ack_ewma(ms)': 'float',
                'send_ewma(ms)': 'float',
                'rtt_ratio': 'float',
                'cwnd (Bytes)':'int',
                'Last Router Ocupation Ack Arriaval(Packets)':'float',
                'Last Router Ocupation Packet Sent(Packets)':'float',
                'Network Situation':'int',
                'AckArrival(ms)':'int',
                'TSInsideAck(ms)':'int',
                'RTTAck(ms)':'int'}))         
                
            lstBaseRouters.append(pd.read_csv(self.lstBaseRoutersPath[i],dtype={
                '#Ack': 'int',
                'Last Router Ocupation Router Arrival(Packets)': 'float',
                'Last Router Ocupation Router Arrival_ewma(Packets)': 'float',
                'Network Situation Router Arrival': 'int',
                'Measure Time':'int'}))
        
        for i in range(len(self.lstBaseTerminalsPath)):
            
            lstBaseTerminals[i].columns = lstBaseTerminals[i].columns.str.replace(' ','_')
            lstBaseRouters[i].columns = lstBaseRouters[i].columns.str.replace(' ','_')
         
        
        
        base_merged, self.minRTT = mrs.MergeAndConcatBases(lstBaseTerminals,lstBaseRouters)
        '''
        mrs
        '''
        
                
        base_merged.drop_duplicates(subset=['ack_ewma(ms)', 'send_ewma(ms)','rtt_ratio'],keep="last",ignore_index=True)
        #base_consistent = mrs.DeleteInconsistences(base_merged)
        #base = mrs.SubtractMin(base_consistent,parFromFile,self.experimentPath)
        #baseTile = mrs.TileBase(base_consistent)
        baseTile = mrs.TileBase(base_merged)
        baseNor = mrs.NormalizeFeatures(baseTile,parFromFile,self.experimentPath,self.minRTT)
        baseNor.to_csv(self.experimentPath+'/finalbaseDebugPrevision.csv',sep=',',index=False,encoding='utf-8')
        ####baseNor = pd.read_csv(self.experimentPath+'/finalbaseDebugPrevision.csv')
       
        previsores = baseNor.iloc[:, [1,2,3]].values        
        classe = baseNor.iloc[:, 13].values
        
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


        self.previsores_treinamento, self.previsores_teste,self.classe_treinamento,self.classe_teste = train_test_split(previsores, classe_dummy, test_size=0.20)
        
        print("Dados preparados")
        #return previsores_treinamento, previsores_teste, classe_treinamento, classe_teste
    
        
        
        '''
        
 
 
        


        '''
        