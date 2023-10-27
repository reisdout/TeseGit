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
import sys
from sys import exit
sys.path.append('../mrsutils')
sys.path.append('..')
import numpy as np
import pandas as pd
import tensorflow as tf
#from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from GeneralClient import Client
import keras
from keras.layers import Dense


#from keras.utils import np_utils
#import keras.utils.to_categorical
#from tensorflow.keras import utils
from keras.models import Sequential
import seaborn as sns; sns.set()


import MRSUtils as mrs



class ClientBufferArrivalSigmoid(Client):
    
    def __init__(self,parId,parExperimentPath,parBasePath,parLstBasesTerminalsPaths, parLstBasesRoutersPaths):
           
        #print(parLstBasesTerminalsPaths)
        #print(parLstBasesRoutersPaths)
        #input()
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


    def GetModel(self):
        
        classificador = Sequential()
        
        #classificador.add(Dense(units = 8, activation = 'relu', 
         #                       kernel_initializer = 'random_uniform', input_dim = 4))#Com cwnd
        
        classificador.add(Dense(units = 20, activation = 'relu', 
                                kernel_initializer = 'random_uniform', input_dim = 3))#sem cwnd
        
        classificador.add(Dense(units = 20, activation = 'relu', 
                                kernel_initializer = 'random_uniform'))
        #classificador.add(Dense(units = classe_dummy.shape[1], activation = 'softmax'))
        classificador.add(Dense(units = 1, activation = 'sigmoid'))
        
        
        

        
        return classificador

        
    def LoadTrainingDataSet(self, parFromFile=False):
        print ("Configurando dados tomados da chegada na fila....")
        
        
        lstBaseTerminals=[]
        lstBaseRouters=[]
        
        #print(self.lstBaseTerminalsPath)
        
        #df = pd.read_csv(self.lstBaseTerminalsPath[0])
        '''
        mrs
        '''
        for i in range(len(self.lstBaseRoutersPath)):        
            lstBaseTerminals.append(pd.read_csv(self.lstBaseTerminalsPath[i],dtype={
                '#Ack': 'int',
                'ack_ewma(ms)': 'float32',
                'send_ewma(ms)': 'float32',
                'rtt_ratio': 'float32',
                'cwnd (Bytes)':'int',
                'Last Router Ocupation Ack Arriaval(Packets)':'float32',
                'Last Router Ocupation Packet Sent(Packets)':'float32',
                'Network Situation':'int',
                'AckArrival(ms)':'int',
                'TSInsideAck(ms)':'int',
                'RTTAck(ms)':'int'}))         
                
            lstBaseRouters.append(pd.read_csv(self.lstBaseRoutersPath[i],dtype={
                '#Ack': 'int',
                'Last Router Ocupation Router Arrival(Packets)': 'float32',
                'Last Router Ocupation Router Arrival_ewma(Packets)': 'float32',
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
        baseNor = mrs.NormalizeFeatures(baseTile,parFromFile,self.modelPath,self.minRTT)
        baseNor.to_csv(self.experimentPath+'/finalbaseDebugPrevision.csv',sep=',',index=False,encoding='utf-8')
        ####baseNor = pd.read_csv(self.experimentPath+'/finalbaseDebugPrevision.csv')
       
        previsores = baseNor.iloc[:, [1,2,3]].values        
        classe = baseNor.iloc[:, 13].values
        classe -=1        
        self.previsores_treinamento, self.previsores_teste,self.classe_treinamento,self.classe_teste = train_test_split(previsores, classe, test_size=0.20)
        
        print("Dados preparados")
        #return previsores_treinamento, previsores_teste, classe_treinamento, classe_teste
    
        
    def GetMapedMatrix(self):
        
        #previsores_treinamento, previsores_teste, classe_treinamento, classe_teste = self.LoadTrainingDataSet()

        classificador = self.GetModel()
        
        classificador.set_weights(self.weightsClientModel)
        
        #resultado = classificador.evaluate(self.previsores_teste, self.classe_teste)
        previsoes = classificador.predict(self.previsores_teste)
        previsoes = (previsoes > 0.5)

                
        '''
        for i in range (len(previsoes2)):
            if(previsoes2[i] != classe_teste2[i]):
                print(self.previsores_teste[i])
        '''

        from sklearn.metrics import confusion_matrix
        matriz = confusion_matrix(self.classe_teste,previsoes)
        print(matriz)
        to_heat_map =[[matriz[0,0],matriz[0,1]],[matriz[1,0],matriz[1,1]]]
        to_heat_map = pd.DataFrame(to_heat_map, index = ["Hit","Fail"],columns = ["Fail","Hit"])
        sns.heatmap(to_heat_map,annot=True, fmt="d")
        return matriz;
        
        
    def AderenciaOutrosFluxos(self,parModel):
 
        #previsores_treinamento, previsores_teste, classe_treinamento, classe_teste = self.LoadTrainingDataSet(parFromFile=True)
        self.LoadTrainingDataSet(parFromFile=True)
        arquivo = open(self.modelPath+"/model_"+parModel+".json",'r')
        estrutura_classificador = arquivo.read()
        arquivo.close()
        from keras.models import model_from_json
        classificador = model_from_json(estrutura_classificador)
        classificador.load_weights(self.modelPath+"/model_weights_"+parModel+".h5") 
        #resultado = classificador.evaluate(self.previsores_teste, self.classe_teste)
        previsoes = classificador.predict(self.previsores_teste)
        previsoes = (previsoes > 0.5)

        from sklearn.metrics import confusion_matrix
        matriz = confusion_matrix(previsoes, self.classe_teste)
        print(matriz)
        to_heat_map =[[matriz[0,0],matriz[0,1]],[matriz[1,0],matriz[1,1]]]
        to_heat_map = pd.DataFrame(to_heat_map, index = ["Hit","Fail"],columns = ["Fail","Hit"])
        sns.heatmap(to_heat_map,annot=True, fmt="d")



    def RefreshModel(self, parFromTraining=False): #Constroi na primeira vez e atualiza, a partir da avaliação do servidor cetral
      #pensar melhor no critério
      
        #A filosofia, aqui, e sempre treinar do zero! 
        
        self.LoadTrainingDataSet()
        classificador = self.GetModel()
    
        #classificador.compile(optimizer = 'adam', loss = 'binary_crossentropy',
        #                      metrics = ['binary_accuracy'])
        
        #classificador.fit(previsores_treinamento, classe_treinamento,batch_size = 512, epochs = 100,verbose=0,callbacks=[LoggingCallback(parExpDir=".")])
        
        opt = keras.optimizers.Adam(learning_rate=0.0001)
        
       
        
        classificador.compile(optimizer = opt, 
                              loss = tf.keras.losses.BinaryCrossentropy(),
                              metrics = [tf.keras.metrics.BinaryAccuracy()]) 
        
        print("treinando...com 64 de bach-size e 3000 épocas, utilizabdo Sigmoid")
        print("Taxa de Aprendizado 0.0001")
        self.history = classificador.fit(self.previsores_treinamento, 
                          self.classe_treinamento, 
                          batch_size = 64, 
                          epochs = 3000,
                          validation_split=0.2,
                          verbose=0)
        self.weightsClientModel = classificador.get_weights()
     