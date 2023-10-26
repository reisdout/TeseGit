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
#import keras
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM#, Bidirectional
#from sklearn.preprocessing import LabelEncoder
#from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from GeneralClient import Client
from GeneralClient import LoggingCallback
#from keras.utils import np_utils
#from tensorflow.keras import utils
import seaborn as sns; sns.set()


import MRSUtils as mrs


"""
Esta codificaçao representa a retomada do LSTM. A ideia
e, a partir de tres acks e suas respectivas temporizaçoes
prever o estado da rede, semelhnte ao que foi feito no artigo do
DDoS Atack.

"""

class ClientBufferArrivalLSTM(Client):

    #resultadoTreinamento = np.eye(10)

    def __init__(self,parId,parExperimentPath,parBasePath,parLstBasesTerminalsPaths, parLstBasesRoutersPaths, parFeaturesWindow):
           
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
        super().__init__(parId,parExperimentPath,parBasePath)


        
    def EvaluateServerModel(self):
      print ("Modelo do Servidor avaliado")
    
    def GetModel(self):
        
       regressor = Sequential()
       #regressor.add(LSTM(units = 100, return_sequences = True, input_shape = (self.input_shape, 4)))# 4, pois são 4 previsores
       #regressor.add(LSTM(units = 100, return_sequences = True, input_shape = (self.input_shape, 4)))# 3, retirando o valor do preenchimento do buffer.
       #regressor.add(Bidirectional(LSTM(units = 100, return_sequences = True, input_shape = (self.input_shape, 4))))
       #regressor.add(Dropout(0.3)) #zerar 30% das entradas para evitar o overfiting

       #regressor.add(LSTM(units = 100, return_sequences = True, input_shape = (self.input_shape, 4)))
       #regressor.add(LSTM(units = 20, return_sequences = True, input_shape = (self.input_shape, 4)))
       #regressor.add(LSTM(units = 10, return_sequences = True, input_shape = (self.input_shape, 4)))
       #regressor.add(LSTM(units = 6, return_sequences = True, input_shape = (self.input_shape, 4)))
       regressor.add(LSTM(units = 3, return_sequences = True, input_shape = (self.T, 3)))
       regressor.add(Dropout(0.3)) #zerar 30% das entradas para evitar o overfiting
       
       
       #regressor.add(LSTM(units = 50, return_sequences = True))
       #regressor.add(LSTM(units = 10, return_sequences = True))
       #regressor.add(LSTM(units = 6, return_sequences = True))
       regressor.add(LSTM(units = 2, return_sequences = False))
       regressor.add(Dropout(0.3))

       """
       #regressor.add(LSTM(units = 50, return_sequences = True))
       #regressor.add(LSTM(units = 10, return_sequences = True))
       #regressor.add(LSTM(units = 6, return_sequences = True))
       regressor.add(LSTM(units = self.exp_units, return_sequences = True))
       regressor.add(Dropout(0.3))

       #regressor.add(LSTM(units = 50))
       #regressor.add(LSTM(units = 10))
       #regressor.add(LSTM(units = 6))
       regressor.add(LSTM(units = self.exp_units))
       regressor.add(Dropout(0.3))
       """
       '''
       Segundo https://towardsdatascience.com/illustrated-guide-to-lstms-and-gru-s-a-step-by-step-explanation-44e9eb85bf21
       as saídas de cada unidade da LSTM e, portanto, a saída global é a dimenção do número de previsores, que, no nosso
       caso, é 4. Daí esses 4 estão sendo levados em um softmax de tres neurônios, pois há tres categorias no final"
       ''' 
       regressor.add(Dense(units = 1, activation = 'sigmoid', name="client_"+str(self.id))) #para uma previsão
       #regressor.add(Dense(units = self.n_steps_out, activation = 'sigmoid', name="client_"+str(self.id)))
       
       #regressor.compile(optimizer = 'adam', loss = 'mean_squared_error',metrics = ['mean_absolute_error'])

       return regressor



    def LoadTrainingDataSet(self, parFromFile=False):
        
        print ("Configurando dados tomados da chegada na fila e usando para LSTM....")
        
        #input()
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
     
     
        base_treinamento = base_treinamento.iloc[:, [1,2,3,13]].values
        base_teste = base_teste.iloc[:, [1,2,3,13]].values
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
            previsores.append(base_treinamento[i-self.T:i, 0:3])#o que é considerado é o limite superior do rante -1 e sem a informação do percentual de ocupação do buffer
            real_congestion_treino.append(base_treinamento[(i-1)+self.n_steps_out,3]-1)
            
            
            
        #Preparando a base de teste
        
        base_teste_len = base_teste.shape[0]
        for i in range(self.T,base_teste_len): # para as duzentas previsoes, o mesmo tramanho do Teste.csv, ou seja 290-90
          if i >= base_teste_len:
            break;
          X_teste.append(base_teste[i-self.T:i, 0:3])
          real_congestion_teste.append(base_teste[(i-1)+self.n_steps_out,3]-1)

        

        '''
          *********************************SOBRE O RESHAPE**************************************
          Veja que nesse caso não é necessário fazer o reshape, uma vez que o array previsores , já sai
          no formato [samples, timesteps, features]
          *sample: Ajanela deslizante em T vai gerar um número de inserções em previsores, correspondente ao número de samples
          *timesteps:inserções de exatamente T arrays, que nesse caso é equivalente ao timestamps, ou seja, quantas leituras no tempo estamos 
          considerando para prever. 
          *features: T arrays de n features
         
          no nosso caso:
         
          seja
         
          base_treinamento = np.array([
          [0.0618679825944638,1.48529333300134E-05,0.849658635009267,	1,	0.8],
          [0.0618642722717276,1.29963255564132E-05,0.856697088426436,0.960369635326222,0.8],
          [0.061861180336114,	1.13717804155358E-05,0.863735541843606,0.915095509799057,	0.78],
          [0.0618582945295414,9.95030786359384E-06,0.870773995260775,0.892458447035475,	0.76],
          [0.0620104177617272,8.70651048799314E-06,0.877953217746287,0.869821384271893,	0.74],
          [0.06214357712215,  7.6182100159712E-06, 0.8851324402318,0.860208385016125,	0.72],
          [0.0622600400302597	,6.66593154081194E-06	,0.892311662717312,0.847184321508311,	0.7],
          [0.0623620739055063	,5.83269009821044E-06	,0.899490885202825,	0.847184321508311,	0.68],
          [0.0624511216511761	,5.1035993896084E-06,0.906670107688337,0.847184321508311,	0.69],
          [0.062529244557678	,4.46565835855882E-06	,0.91384933017385	,0.847184321508311,	0.78],
          [0.0625974732702166,3.9074488405761E-06	,0.921028552659362	,0.847184321508311,	0.58],
          [0.0626572506920783	,3.41901106601549E-06	,0.928207775144875,0.847184321508311,	0.48],
          [0.0627096074684674	,2.99163023643782E-06	,0.935386997630387,0.847184321508311,	0.38],
          [0.0627553681155477	,2.61767645688309E-06	,0.9425662201159,0.0226370627635822,	0.18],
          [0.0627953571494827	,2.29048023874991E-06	,0.949745442601412,0.0226370627635822,	0.28],
         
         
          ])
         
         
          ou seja 15 samples, 4 features e uma a ser prevista. Vamos considerar T=3 e n_steps_out=4(n_steps_out=0 já é um a frente, ou seja tem que bater em T)  
          Daí só vai sobrar 15-(T+n_steps_out-1= 3+4-1) = 9 samples
          a saída será
         
          previsores
         1               2              3             4
        1  [[6.18679826e-02 1.48529333e-05 8.49658635e-01 1.00000000e+00]
          T [6.18642723e-02 1.29963256e-05 8.56697088e-01 9.60369635e-01]
        [6.18611803e-02 1.13717804e-05 8.63735542e-01 9.15095510e-01]] 0.7
        2  [[6.18642723e-02 1.29963256e-05 8.56697088e-01 9.60369635e-01]
          T [6.18611803e-02 1.13717804e-05 8.63735542e-01 9.15095510e-01]
        [6.18582945e-02 9.95030786e-06 8.70773995e-01 8.92458447e-01]] 0.68
        3[  [6.18611803e-02 1.13717804e-05 8.63735542e-01 9.15095510e-01]
          T [6.18582945e-02 9.95030786e-06 8.70773995e-01 8.92458447e-01]
        [6.20104178e-02 8.70651049e-06 8.77953218e-01 8.69821384e-01]] 0.69
        4[  [6.18582945e-02 9.95030786e-06 8.70773995e-01 8.92458447e-01]
          T [6.20104178e-02 8.70651049e-06 8.77953218e-01 8.69821384e-01]
        [6.21435771e-02 7.61821002e-06 8.85132440e-01 8.60208385e-01]] 0.78
        5[  [6.20104178e-02 8.70651049e-06 8.77953218e-01 8.69821384e-01]
          T [6.21435771e-02 7.61821002e-06 8.85132440e-01 8.60208385e-01]
        [6.22600400e-02 6.66593154e-06 8.92311663e-01 8.47184322e-01]] 0.58
        6[  [6.21435771e-02 7.61821002e-06 8.85132440e-01 8.60208385e-01]
          T [6.22600400e-02 6.66593154e-06 8.92311663e-01 8.47184322e-01]
        [6.23620739e-02 5.83269010e-06 8.99490885e-01 8.47184322e-01]] 0.48
        7[  [6.22600400e-02 6.66593154e-06 8.92311663e-01 8.47184322e-01]
          T [6.23620739e-02 5.83269010e-06 8.99490885e-01 8.47184322e-01]
        [6.24511217e-02 5.10359939e-06 9.06670108e-01 8.47184322e-01]] 0.38
        8[  [6.23620739e-02 5.83269010e-06 8.99490885e-01 8.47184322e-01]
          T [6.24511217e-02 5.10359939e-06 9.06670108e-01 8.47184322e-01]
        [6.25292446e-02 4.46565836e-06 9.13849330e-01 8.47184322e-01]] 0.18
        9[  [6.24511217e-02 5.10359939e-06 9.06670108e-01 8.47184322e-01]
          T [6.25292446e-02 4.46565836e-06 9.13849330e-01 8.47184322e-01]
        [6.25974733e-02 3.90744884e-06 9.21028553e-01 8.47184322e-01]] 0.28
         
          ou seja
          [samples,timestepes,features]
         
        '''
        self.previsores_treinamento,self.classe_treinamento = np.array(previsores), np.array(real_congestion_treino)
        self.previsores_teste, self.classe_teste =  np.array(X_teste), np.array(real_congestion_teste) # equivalente ao X_teste
       
        

    def RefreshModel(self, parFromTraining=False): #Constroi na primeira vez e atualiza, a partir da avaliação do servidor cetral
      #pensar melhor no critério
      
     self.LoadTrainingDataSet()
     regressor = self.GetModel();
     opt = tf.keras.optimizers.Adam(learning_rate=0.0001, weight_decay=0.00001,clipvalue = 0.5)
     regressor.compile(optimizer = opt, 
                       loss = tf.keras.losses.BinaryCrossentropy(),
                       metrics = [tf.keras.metrics.BinaryAccuracy()])
     
     #es = EarlyStopping(monitor = 'loss', min_delta = 1e-10, patience = 10, verbose = 1)
     #rlr = ReduceLROnPlateau(monitor = 'loss', factor = 0.2, patience = 5, verbose = 1)
     #mcp = ModelCheckpoint(filepath = self.exp_dir+"/pesos.h5", monitor = 'loss',  save_weights_only = True, save_freq='epoch',verbose = 1)
     #regressor.fit(previsores, real_congestion, epochs = 50, batch_size = 32, callbacks = [es, rlr, mcp])
     
     print("Treinando o modelo LSTM...")
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
        previsoes = (previsoes > 0.5)

        #classe_teste2 = [np.argmax(t) for t in self.classe_teste]
        #previsoes2 = [np.argmax(t) for t in previsoes] #para softmax
        
        ''' 
        for i in range (len(previsoes)):
            if(previsoes[i] != self.classe_teste[i]):
                print(self.previsores_teste[i])
        '''
  

        from sklearn.metrics import confusion_matrix
        matriz = confusion_matrix(self.classe_teste,previsoes)
        print(matriz)
        to_heat_map =[[matriz[0,0],matriz[0,1]],[matriz[1,0],matriz[1,1]]]
        to_heat_map = pd.DataFrame(to_heat_map, index = ["Hit","Fail"],columns = ["Fail","Hit"])
        ax = sns.heatmap(to_heat_map,annot=True, fmt="d")


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

    def GetPrevision(self): #evalueta indica que é uma avaliação do modelo recebido como parametro, no caso do servidor
      test_vectors = self.LoadTestData()
      regressor = Sequential()
      regressor.add(LSTM(units = 100, return_sequences = True, input_shape = (self.input_shape, 4)))# 4, pois são 4 previsores
      regressor.add(Dropout(0.3)) #zerar 30% das entradas para evitar o overfiting
      regressor.add(LSTM(units = 50, return_sequences = True))
      regressor.add(Dropout(0.3))
      regressor.add(LSTM(units = 50, return_sequences = True))
      regressor.add(Dropout(0.3))
      regressor.add(LSTM(units = 50))
      regressor.add(Dropout(0.3))
      regressor.add(Dense(units = 1, activation = 'sigmoid',name="client_eval_"+str(self.id)))
      regressor.compile(optimizer = 'adam', loss = 'mean_squared_error',metrics = ['mean_absolute_error'])

      regressor.set_weights(self.weightsClientModel)

      previsoes = regressor.predict(test_vectors)
      #previsoes = parNeuralModel.predict(self.test_vectors)
     
      '''
      Observe que os previsores teste tem 90 quádruplas que conduzem ao resultado
      do último estado, da quádrupla 90. Prontamente preparado para pevisões....
      '''
      #classe_teste2 = np.array([])
      #previsoes2 =  np.array([])
      classe_teste2,previsoes2 = self.GetMapedMatrix(previsoes)
      '''
      for i in range(0, len(self.base_teste)):
        if(self.real_congestion_test[i] < 0.3):
          classe_teste2 = np.append(classe_teste2,0)
        elif (self.real_congestion_test[i,0] >= 0.3 and self.real_congestion_test[i] < 0.75):
          classe_teste2= np.append(classe_teste2,1)
        else:
          classe_teste2 = np.append(classe_teste2,2)

      for i in range(0, len(previsoes)):
        if(previsoes[i] < 0.3):
          previsoes2= np.append(previsoes2,0)
        elif (previsoes[i] >= 0.3 and previsoes[i] < 0.75):
          previsoes2= np.append(previsoes2,1)
        else:
          previsoes2 = np.append(previsoes2,2)
      '''
      self.currentConfusionMatriz = confusion_matrix(classe_teste2,previsoes2)
      return self.currentConfusionMatriz # Com a configuração corrente, essa é a matriz....
        
    
    def ServerModelIsBetter(self):
        regressorServer = Sequential()
        regressorServer.add(LSTM(units = 100, return_sequences = True, input_shape = (self.input_shape, 4)))# 4, pois são 4 previsores
        regressorServer.add(Dropout(0.3)) #zerar 30% das entradas para evitar o overfiting
        regressorServer.add(LSTM(units = 50, return_sequences = True))
        regressorServer.add(Dropout(0.3))
        regressorServer.add(LSTM(units = 50, return_sequences = True))
        regressorServer.add(Dropout(0.3))
        regressorServer.add(LSTM(units = 50))
        regressorServer.add(Dropout(0.3))

        '''
        Segundo https://towardsdatascience.com/illustrated-guide-to-lstms-and-gru-s-a-step-by-step-explanation-44e9eb85bf21
        as saídas de cada unidade da LSTM e, portanto, a saída global é a dimenção do número de previsores, que, no nosso
        caso, é 4. Daí esses 4 estão sendo levados em um softmax de tres neurônios, pois há tres categorias no final"
        ''' 
        regressorServer.add(Dense(units = 1, activation = 'sigmoid',name="client_eval_"+str(self.id)))
        regressorServer.compile(optimizer = 'adam', loss = 'mean_squared_error',metrics = ['mean_absolute_error'])
        regressorServer.set_weights(self.weightsServerModel)
        return self.EvalueteServerModel(regressorServer)
    
    
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
