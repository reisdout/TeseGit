# -*- coding: utf-8 -*-

"""
Created on Mon Sep  4 15:59:52 2023

@author: visitante
"""


import pandas as pd
from sklearn.model_selection import train_test_split
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM, Bidirectional
from sklearn.metrics import confusion_matrix, accuracy_score

from sklearn.metrics import classification_report, confusion_matrix
from keras.utils import np_utils
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import normalize
import seaborn as sns; sns.set()


def ReadNormalizationFactors(par_exp_dir):
       
       ack_ewma_normalizer=1.0
       send_ewma_normalizer=1.0
       min_rtt = 1.0 
       rtt_ratio_normalizer=1.0
       cwnd_normalizer=1.0
     
       file1 = open(par_exp_dir+"/normalization_factors.txt", 'r')
       Lines = file1.readlines()
       
       ack_ewma_normalizer = float(Lines[0].split()[len(Lines[0].split())-1])# split retorna uma lista com as strings da linha que estão separadas por espaço
       send_ewma_normalizer = float(Lines[1].split()[len(Lines[1].split())-1])
       min_rtt = float(Lines[2].split()[len(Lines[2].split())-1])
       rtt_ratio_normalizer=float(Lines[3].split()[len(Lines[3].split())-1])
       cwnd_normalizer=float(Lines[4].split()[len(Lines[4].split())-1])
       
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
           cwnd_normalizer=data['cwnd (Bytes)'].max()

       data['rtt_ratio'] = data['rtt_ratio'].div(min_rtt)
       if(not (parFromFile)):
           rtt_ratio_normalizer = data['rtt_ratio'].max()
       data['ack_ewma(ms)'] = data['ack_ewma(ms)'].div(ack_ewma_normalizer)
       data['send_ewma(ms)'] = data['send_ewma(ms)'].div(send_ewma_normalizer)       
       data['rtt_ratio'] = data['rtt_ratio'].div(rtt_ratio_normalizer)
       data['cwnd (Bytes)'] = data['cwnd (Bytes)'].div(cwnd_normalizer)
        
       if(not parFromFile):
           file1 = open(par_exp_dir+"/normalization_factors.txt", 'w')
           file1.writelines("ack_ewma: "+str(ack_ewma_normalizer)+"\n")
           file1.writelines("send_ewma: "+str(send_ewma_normalizer)+"\n")
           file1.writelines("rtt_min: "+str(min_rtt)+"\n")
           file1.writelines("rtt_ratio: "+str(rtt_ratio_normalizer)+"\n")
           file1.writelines("cwnd (Bytes): "+str(cwnd_normalizer)+"\n")
           file1.close()
    
       print(ack_ewma_normalizer) 
       print(send_ewma_normalizer)
       print(min_rtt)
       print(rtt_ratio_normalizer)
       print(cwnd_normalizer) 
       print("Eis os normalizadores acima")
       #a=input("Eis os normalizadores acima")
       seguir = input("Deseja Prosseguir? (N/n-->Sair)")
    
       if(seguir == 'n' or seguir =='N'):
         exit()


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
       data['cwnd (Bytes)'] = data['cwnd (Bytes)'].div(cwnd_normalizer)
        

       print("Normalizado por 1000")
       #a=input("Eis os normalizadores acima")
       seguir = input("Deseja Prosseguir? (N/n-->Sair)")
    
       if(seguir == 'n' or seguir =='N'):
         exit()


       return data




class Client():

    #resultadoTreinamento = np.eye(10)

    def __init__(self,parId,parExperimentPath,parBasePath):
      self.id=parId
      self.basePath=parBasePath
      self.experimentPath = parExperimentPath
      #self.testPath = parTestPath
      #self.T = parPrevisionWindow
      #centralServer = Server_FederatedAMA()
      #confusionMatrizModelClient = np.full((2,2), 1)
      #confusionMatrizModelServer = np.full((2,2), 2)
      self.currentConfusionMatriz =np.full((2,2), 0)
      self.weightsClientModel = np.array([])
      self.weightsServerModel = []
      #self.base = pd.DataFrame()
      #self.base_treinamento =  np.array([])
      self.real_congestion_test = np.array([])
      #self.test_vectors = []
      #self.previsores = []
      #self.real_congestion = []
      #self.regressor = Sequential()
      self.input_shape =0;
      self.len_base_teste = 0;
      #self.centralServer.RegisterClient(self,self)

    def EvaluateServerModel(self):
      print ("Modelo do Servidor avaliado")
    
    def GetModel(self):
        
        classificador = Sequential()
        
        #classificador.add(Dense(units = 8, activation = 'relu', 
         #                       kernel_initializer = 'random_uniform', input_dim = 4))#Com cwnd
        
        classificador.add(Dense(units = 20, activation = 'relu', 
                                kernel_initializer = 'random_uniform', input_dim = 3))#sem cwnd
        classificador.add(Dense(units = 20, activation = 'relu', 
                                kernel_initializer = 'random_uniform'))
        classificador.add(Dense(units = 20, activation = 'relu', 
                                kernel_initializer = 'random_uniform'))
        classificador.add(Dense(units = 20, activation = 'relu', 
                                kernel_initializer = 'random_uniform'))
        classificador.add(Dense(units = 20, activation = 'relu', 
                                kernel_initializer = 'random_uniform'))
        #classificador.add(Dense(units = classe_dummy.shape[1], activation = 'softmax'))
        #classificador.add(Dense(units = 2, activation = 'softmax'))
        classificador.add(Dense(units = 1, activation = 'sigmoid'))

        #classificador.compile(optimizer = 'adam', loss = 'categorical_crossentropy',
         #                     metrics = ['categorical_accuracy']) #para softmax. lembrar de ajustar no GetMappedMatrix
        classificador.compile(optimizer = 'adam', loss = 'binary_crossentropy',
                              metrics = ['binary_accuracy']) #para sgmoid. lembrar de ajustar no GetMappedMatrix
        
        
        return classificador


    def LoadTainingDataSet(self):
        base = pd.read_csv(self.basePath)
        
        base = base.drop_duplicates(subset=['ack_ewma(ms)', 'send_ewma(ms)','rtt_ratio'])
        
        
        print (base.shape[0])
        input("Eis a quantidade de entradas")

        base = NormalizeFeatures(base,False,self.experimentPath)
        #base = MilimizeFeatures(base,self.experimentPath)

        #previsores = base.iloc[:, [1,2,3,4]].values #com cwnd
        previsores = base.iloc[:, [1,2,3]].values #sem cwnd

        print(previsores[10])

        print(previsores[20])

        print(previsores[30])

        print("================================================")

        

        previsores=normalize(previsores)

        print(previsores[10])

        print(previsores[20])

        print(previsores[30])
        
        classe = base.iloc[:, [7]].values
        classe = classe - 1#para ficar 0 e 1
 
        previsores_treinamento, previsores_teste, classe_treinamento, classe_teste = train_test_split(previsores, classe, test_size=0.20)
        
        return previsores_treinamento, previsores_teste, classe_treinamento, classe_teste
    


    def RefreshModel(self, parFromTraining=False): #Constroi na primeira vez e atualiza, a partir da avaliação do servidor cetral
      #pensar melhor no critério
                
      if(parFromTraining):#tem que construir a rede do zero e treinar os pesos
        
   
        previsores_treinamento, previsores_teste, classe_treinamento, classe_teste = self.LoadTainingDataSet()
        
        classificador = self.GetModel()

        #classificador.compile(optimizer = 'adam', loss = 'binary_crossentropy',
        #                      metrics = ['binary_accuracy'])
        print("treinando...")
        #classificador.fit(previsores_treinamento, classe_treinamento,batch_size = 512, epochs = 100,verbose=0,callbacks=[LoggingCallback(parExpDir=".")])

        classificador.fit(previsores_treinamento, classe_treinamento, batch_size = 16, epochs = 2000,
                          verbose=0)
        self.weightsClientModel = classificador.get_weights()
      else:
        if(self.ServerModelIsBetter()):
          print("Pesos atualizados de acordo com o modelo do servidor")
        else:
           print("Pesos Mantidos de acordo com o modelo do cliente")

    def GetMapedMatrix(self):
        
        previsores_treinamento, previsores_teste, classe_treinamento, classe_teste = self.LoadTainingDataSet()

        classificador = self.GetModel()
        
        classificador.set_weights(self.weightsClientModel)
        
        resultado = classificador.evaluate(previsores_teste, classe_teste)
        print(resultado)
        input("Eis os resultados")
        previsoes = classificador.predict(previsores_teste)
        print(previsoes)
        input("Eis as previsoes")
        previsoes = (previsoes > 0.5)
        arr = np.zeros((previsoes.shape[0],1))
        previsoes_col = np.append(previsoes,arr,axis=1)
        for i in range (previsoes.shape[0]):
            if(previsoes[i,0] > 0):
                previsoes_col[i,0]=0.0;
                previsoes_col[i,1]=1.0
            else:
                previsoes_col[i,0]=1.0;
                
        arr = np.zeros((classe_teste.shape[0],1))
        classe_teste_col = np.append(classe_teste,arr,axis=1)
        for i in range (classe_teste.shape[0]):
            if(classe_teste[i,0] > 0):
                classe_teste_col[i,0]=0.0;
                classe_teste_col[i,1]=1.0
            else:
                classe_teste_col[i,0]=1.0;
        
        classe_teste2 = [np.argmax(t) for t in classe_teste_col]
        #previsoes2 = [np.argmax(t) for t in previsoes] #para softmax
        previsoes2 = [np.argmax(t) for t in previsoes_col] #para sigmoid

        from sklearn.metrics import confusion_matrix
        matriz = confusion_matrix(previsoes2, classe_teste2)
        print(matriz)
        to_heat_map =[[matriz[0,0],matriz[0,1]],[matriz[1,0],matriz[1,1]]]
        to_heat_map = pd.DataFrame(to_heat_map, index = ["Hit","Fail"],columns = ["Fail","Hit"])
        ax = sns.heatmap(to_heat_map,annot=True, fmt="d")

    def EvalueteServerModel(self, parServerModel):

      test_vectors = self.LoadTestData()
      previsoes = parServerModel.predict(test_vectors)
      updated = False
      '''
      Observe que os previsores teste tem 90 quádruplas que conduzem ao resultado
      do último estado, da quádrupla 90. Prontamente preparado para pevisões....
      '''
      classe_teste2,previsoes2 = self.GetMapedMatrix(previsoes)
      matriz = confusion_matrix(classe_teste2,previsoes2)
      currentSum = 0
      newSum = 0
      if(self.currentConfusionMatriz.ndim > 1): # as vezes a rede pode errar ao ponto de dar só uma categoria, daí cai no else...
        for i in range (0, len(self.currentConfusionMatriz)):
            currentSum = currentSum + self.currentConfusionMatriz[i][i]
      else:
        currentSum = self.currentConfusionMatriz[i]
      if(matriz.ndim > 1):
        for i in range (0, len(matriz)):
          newSum = newSum + matriz[i][i]
      else:
        newSum = matriz[i]
      if(newSum > currentSum):
        self.currentConfusionMatriz = np.array(matriz)
        #self.regressor.set_weights(self.weightsServerModel)
        self.weightsClientModel.clear()
        for e in self.weightsServerModel:
          self.weightsClientModel.append(e)
        updated = True
      print ("Modelo do Servidor avaliado")
      return updated 

     


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
    def ReceiveModelFromServer(self, parCandidateMatrix):
      print("Cliente ", self.id, " Recebido Modelo do Servidor")
      self.weightsServerModel.clear()
      for e in parCandidateMatrix :
        self.weightsServerModel.append(e)
      
    def SendModelToServer(self):
      self.centralServ.ReceiveModelsFromClients(self.id)
      print("Client", self.id, "Sending Model To Server")
    '''
    def TreinarModelo(self):
      print("Cliente ", self.id, "treinando Modelo")
      time.sleep(random.randint(0,9))
      self.RefreshConfusionClientMatrix()

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
        
    def SaveModel(self):
    
        classificador = self.GetModel()        
        classificador.set_weights(self.weightsClientModel)
        
        classificador_json = classificador.to_json()
        with open(self.experimentPath+"/model.json",'w') as json_file:
            json_file.write(classificador_json)
        classificador.save_weights(self.experimentPath+"/model_weights.h5")
        from keras2cpp import export_model
        export_model(classificador, self.experimentPath+"/example.model")
        
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



def TreinarModelo(parExpDirPath, parBasePath):
    
    client01 = Client(0,parExpDirPath,parBasePath)    


    
    client01.RefreshModel(True)
    client01.GetMapedMatrix()
    

   


    #previsores_treinamento = pd.read_csv('./SQ-false-positive-filering-ML/input/x_train.csv')
    #classe_treinamento = pd.read_csv('./SQ-false-positive-filering-ML/input/y_train.csv')

    client01.SaveModel()

    '''
    classificador_json = classificador.to_json()
    with open(parExpDirPath+"/model.json",'w') as json_file:
        json_file.write(classificador_json)
    classificador.save_weights(parExpDirPath+"/model_weights.h5")
    from keras2cpp import export_model
    export_model(classificador, parExpDirPath+"/example.model")
    '''






#TreinarModelo('./Exp_0000034','./Exp_0000034/1Mono-4NewReno-noventacincocentesimos-seisdecimos-40-70-3h30min.csv')