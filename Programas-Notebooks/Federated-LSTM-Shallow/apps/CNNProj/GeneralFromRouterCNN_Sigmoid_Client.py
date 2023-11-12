# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 11:06:11 2023

@author: visitante


Este arquivo define uma classe cliente, que eatá preparada para 
realizar o treinamento de uma rede neural softmax, com dados
provenientes das leituras das features (ack_ewma, send_ewma e rtt_ratio)
no momento da chegada dos ack nos clientes.
"""

import sys
from sys import exit
sys.path.append('../mrsutils')
sys.path.append('..')
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten,Conv2D, MaxPooling2D#, Bidirectional
from sklearn.metrics import confusion_matrix
from GeneralClient import Client
from GeneralClient import LoggingCallback
import seaborn as sns; sns.set()
from contextlib import redirect_stdout

import MRSUtils as mrs


"""
Esta codificaçao representa a retomada do LSTM. A ideia
e, a partir de tres acks e suas respectivas temporizaçoes
prever o estado da rede, semelhnte ao que foi feito no artigo do
DDoS Atack.

"""

class ClientBufferArrivalCNN(Client):

    #resultadoTreinamento = np.eye(10)

    def __init__(self,parId,parExperimentPath,parBasePath,parLstBasesTerminalsPaths, parLstBasesRoutersPaths, parClineteCNNLstFeatues=[1,2,3], parFeaturesWindow=3):
           
        #print(parLstBasesTerminalsPaths)
        #print(parLstBasesRoutersPaths)
        #input()
        if(len (parLstBasesTerminalsPaths) != len(parLstBasesRoutersPaths)):
            print("Listas com quantidades incompatíveis")
            exit(0);
        self.minRTT=1;
        self.lstBaseTerminalsPath = parLstBasesTerminalsPaths
        self.lstBaseRoutersPath = parLstBasesRoutersPaths
        self.T = parFeaturesWindow
        self.n_steps_out = 0; #e o valor do ultimo
        #self.base_treinamento =  np.array([])
        #self.base_teste =  np.array([])
        self.exp_batch_size = 64
        self.currentConfusionMatriz =np.full((2,2), 0) # Apesar de ser obtidas a partir de listas, a matriz de comfusão é numpy
        self.exp_epoch =  3000
        #self.len_base_teste = 0;
        #self.previsores_treinamento=[]
        #self.previsores_teste = [] 
        #self.classe_treinamento = [] 
        #self.classe_teste = []
        super().__init__(parId,parExperimentPath,parBasePath,parLstFeatues=parClineteCNNLstFeatues)


        
    def EvaluateServerModel(self):
      print ("Modelo do Servidor avaliado")
    
    def GetModel(self):
        
       regressor = tf.keras.Sequential()
       '''
           Este e um ponto muito importante, pois o desempenho da CNN so foi melhorado quando
           do ajuste da matriz de convoluçao para abarcar exatamente um terno de features 
           (no caso, ack_ewma, send_ewma e rtt_ratio). Por isso (1,3), no Conv2D. Diante disso, a matriz que
           passara pelo pool e de 1X3, o que motivou o pool_size=(1,2), que focara nas linhas.
       '''
       regressor.add(Conv2D(16,(1,len(self.lstFeatures)-1),input_shape=(self.T,len(self.lstFeatures),1),activation="relu"))
       regressor.add(MaxPooling2D(pool_size=(1,2),padding='same'))
       regressor.add(Flatten())       
      
       regressor.add(Dense(units = 64, activation = 'relu')) #para uma previsão
       regressor.add(Dense(units=1, activation='sigmoid'))
       #regressor.add(Dense(units = self.n_steps_out, activation = 'sigmoid', name="client_"+str(self.id)))
       
       #regressor.compile(optimizer = 'adam', loss = 'mean_squared_error',metrics = ['mean_absolute_error'])

       return regressor



    def LoadTrainingDataSet(self, parFromFile=False):
        
        print ("Configurando dados tomados da chegada na fila e usando para CNN....")
        
        lstBaseTerminals=[]
        lstBaseRouters=[]
        
        #print(self.lstBaseTerminalsPath)
        #input()
        
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
        baseNor = mrs.NormalizeFeatures(baseTile,parFromFile,self.modelPath,self.minRTT)
        
        baseNor.to_csv(self.experimentPath+'/finalbaseDebugPrevision.csv',sep=',',index=False,encoding='utf-8')
     
        #base = self.NormalizeFeatures(base,parLoadFromNotTrainedFile=False)
        base_treinamento, base_teste = self.SplitBase(baseNor)    
     
        lstFeaturestoGet = [] #Tem que abarcar as de treinamento e os respectivos valores de estado
        lstFeaturestoGet.extend(self.lstFeatures)
        lstFeaturestoGet.append(13)
     
     
        #base_treinamento = base_treinamento.iloc[:, [1,2,3,13]].values
        
        base_treinamento = base_treinamento.iloc[:, lstFeaturestoGet].values
        
        #base_teste = base_teste.iloc[:, [1,2,3,13]].values
        base_teste = base_teste.iloc[:, lstFeaturestoGet].values
        previsores=[]
        real_congestion_treino = []
        real_congestion_teste = []
        X_teste = []

        
        base_treinamento_len = base_treinamento.shape[0]
        for i in range(self.T, base_treinamento_len):
            end_ix = i+self.n_steps_out
            if end_ix > base_treinamento_len:
                break;
            #previsores.append(base_treinamento[i-self.T:i, 0:4])#o que é considerado é o limite superior do rante -1
            previsores.append(base_treinamento[i-self.T:i, 0:len(lstFeaturestoGet)-1])#o que é considerado é o limite superior do rante -1 e sem a informação do percentual de ocupação do buffer
            real_congestion_treino.append(base_treinamento[(i-1)+self.n_steps_out,len(lstFeaturestoGet)-1]-1)
            
            
            
        #Preparando a base de teste
        
        base_teste_len = base_teste.shape[0]
        for i in range(self.T,base_teste_len): # para as duzentas previsoes, o mesmo tramanho do Teste.csv, ou seja 290-90
          if i >= base_teste_len:
            break;
          X_teste.append(base_teste[i-self.T:i, 0:len(lstFeaturestoGet)-1])
          real_congestion_teste.append(base_teste[(i-1)+self.n_steps_out,len(lstFeaturestoGet)-1]-1)

        

        self.previsores_treinamento,self.classe_treinamento = np.array(previsores).reshape((len(previsores),self.T,len(self.lstFeatures),1)), np.array(real_congestion_treino)
        self.previsores_teste, self.classe_teste =  np.array(X_teste).reshape((len(X_teste),self.T,len(self.lstFeatures),1)), np.array(real_congestion_teste) # equivalente ao X_teste
       
        

    def RefreshModel(self, parFromTraining=False): #Constroi na primeira vez e atualiza, a partir da avaliação do servidor cetral
      #pensar melhor no critério
      
     self.LoadTrainingDataSet()
     regressor = self.GetModel();
     #opt = tf.keras.optimizers.legacy.Adam(learning_rate=0.0001, decay=0.00001,clipvalue = 0.5)
     opt = tf.keras.optimizers.legacy.Adam(learning_rate=0.0001)
     regressor.compile(optimizer = opt, 
                       loss = tf.keras.losses.BinaryCrossentropy(),
                       metrics = [tf.keras.metrics.BinaryAccuracy()])     #es = EarlyStopping(monitor = 'loss', min_delta = 1e-10, patience = 10, verbose = 1)
     #rlr = ReduceLROnPlateau(monitor = 'loss', factor = 0.2, patience = 5, verbose = 1)
     #mcp = ModelCheckpoint(filepath = self.exp_dir+"/pesos.h5", monitor = 'loss',  save_weights_only = True, save_freq='epoch',verbose = 1)
     #regressor.fit(previsores, real_congestion, epochs = 50, batch_size = 32, callbacks = [es, rlr, mcp])
     
     print("Treinando o modelo CNN, com {} epocas...".format(self.exp_epoch))
     self.history = regressor.fit(self.previsores_treinamento, 
                                  self.classe_treinamento, 
                                  epochs = self.exp_epoch, 
                                  batch_size = self.exp_batch_size,
                                  verbose=0,
                                  validation_split=0.2,
                                  callbacks=[LoggingCallback(parExpDir=self.experimentPath)])
     
     #self.weightsClientModel = regressor.get_weights().copy()
     self.weightsClientModel = regressor.get_weights()

    def SplitBase(self, base):
        """
            Como agora estamos nos aproximenaod do artigo do DDoS Atack, sem apelo a previsao, mas apenas a 
            detecçao, vamos dividir proporcionalmente, como no caso do modelo Sigmoid
        """
        splitPoint = (base.shape[0]*20)//100
        training_base = base.iloc[0:base.shape[0]-splitPoint,:]
        teste = base.iloc[base.shape[0]-splitPoint:base.shape[0],:]
        return training_base, teste


    def SetSplitedData(self, parPrevisores_treinamento,
                       parPrevisores_teste,
                       parClasse_teste,
                       parClasse_treinamento):
        self.previsores_treinamento=parPrevisores_treinamento
        self.previsores_teste = parPrevisores_teste 
        self.classe_treinamento = parClasse_treinamento 
        self.classe_teste = parClasse_teste

    def GetMapedMatrix(self):
        
        #previsores_treinamento, previsores_teste, classe_treinamento, classe_teste = self.LoadTrainingDataSet()

        classificador = self.GetModel()
        
        classificador.set_weights(self.weightsClientModel)
        
        #resultado = classificador.evaluate(self.previsores_teste, self.classe_teste)
        previsoes = classificador.predict(self.previsores_teste)
        
        print("SAlvando Arquivo de teste k2c...")
        for i in range (len(previsoes)):
            with open('testkeras2c.txt', 'a') as f:
                with redirect_stdout(f):
                    print(self.previsores_teste[i],self.classe_teste[i],previsoes[i])   
        
        previsoes = (previsoes > 0.5)

        #classe_teste2 = [np.argmax(t) for t in self.classe_teste]
        #previsoes2 = [np.argmax(t) for t in previsoes] #para softmax
        
        '''
        for i in range (len(previsoes)):
            if(previsoes[i] != self.classe_teste[i]):
                print(self.previsores_teste[i])
        '''
        print()
        from sklearn.metrics import confusion_matrix
        matriz = confusion_matrix(self.classe_teste,previsoes)
        print(matriz)
        to_heat_map =[[matriz[0,0],matriz[0,1]],[matriz[1,0],matriz[1,1]]]
        to_heat_map = pd.DataFrame(to_heat_map, index = ["Hit","Fail"],columns = ["Fail","Hit"])
        ax = sns.heatmap(to_heat_map,annot=True, fmt="d")
        return matriz;


    def LoadTestData(self):
      base = pd.read_csv(self.trainingPath)
      base = base.dropna()
      base_teste = pd.read_csv(self.testPath)
      base_teste = base_teste.dropna()
      self.real_congestion_test = base_teste.iloc[:, 5:6].values
      frames = [base, base_teste]
      base_completa = pd.concat(frames)
      base_completa = base_completa.drop('#Ack', axis =1)
      base_completa = base_completa.drop('cwnd (Bytes/1000)', axis =1)
      base_completa = base_completa.drop('Network Situation', axis =1)
      base_completa = base_completa.drop('AckArrival(ms)', axis =1)
      base_completa = base_completa.drop('TSInsideAck(ms)', axis =1)
      base_completa = base_completa.drop('RTTAck(ms)', axis =1)
      entradas = base_completa[len(base_completa) - len(base_teste) - self.T:].values
      #base_teste_features = base_teste.iloc[:, [1,2,3,6]].values
      print("#############len(base_teste): ",len(base_teste))
      self.len_base_teste = len(base_teste)
      X_teste = []

      for i in range(self.T, len(base_teste)+self.T): # para as duzentas previsoes, o mesmo tramanho do Teste.csv, ou seja 290-90
        X_teste.append(entradas[i-self.T:i,0:4])


      test_vectors = np.array(X_teste) # equivalente ao X_teste
      return test_vectors
    '''   
    def RefreshConfusionClientMatrix(self):
      #confrontar resultados
      self.confusionMatrizModelClient = np.full((2,2),random.randint(0,9))

    def RefreshConfusionServerMatrix(self):
      #confrontar resultados
      self.confusionMatrizModelServer = np.full((2,2),random.randint(0,9))
    '''       


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
        return matriz
            
