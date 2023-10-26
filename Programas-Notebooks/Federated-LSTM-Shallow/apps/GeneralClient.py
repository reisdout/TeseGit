# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 11:06:11 2023

@author: visitante


Este arquivo define uma classe cliente, que eatá preparada para 
realizar o treinamento de uma rede neural softmax, com dados
provenientes das leituras das features (ack_ewma, send_ewma e rtt_ratio)
no momento da chegada dos ack nos clientes.
"""
import pandas as pd
from sklearn.model_selection import train_test_split
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM#, Bidirectional
#from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.metrics import confusion_matrix #,classification_report, 
#from keras.utils import np_utils
import keras.utils
import numpy as np
import matplotlib.pyplot as plt
#from sys import exit
#from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
#from sklearn.preprocessing import normalize
import seaborn as sns; sns.set()


import sys
sys.path.append('../mrsutils')

import MRSUtils as mrs 

class LoggingCallback(keras.callbacks.Callback):
    """Callback that logs message at end of epoch.
    """


    def __init__(self, parExpDir):
       
        self.exp_dir = parExpDir


    def on_epoch_end(self, epoch, logs=None):

        
        file_path = self.exp_dir+"/readme.txt"

        f = open(file_path, "a")
        msg = "{Epoch: %i} %s" % (epoch, ", ".join("%s: %f" % (k, v) for k, v in logs.items()))
        f.write(msg+"\n")
        f.close()


class Client():

    #resultadoTreinamento = np.eye(10)

    def __init__(self,parId,
                 parExperimentPath,
                 parModelpath,
                 parPrevisores_treinamento=[],
                 parPrevisores_teste=[],
                 parClasse_treinamento=[],
                 parClasse_teste=[]):
    
        
      self.id=parId
      self.experimentPath = parExperimentPath
      self.modelPath=parModelpath
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
      #self.input_shape =0;
      self.len_base_teste = 0;
      #self.centralServer.RegisterClient(self,self)
      self.previsores_treinamento=parPrevisores_treinamento
      self.previsores_teste = parPrevisores_teste 
      self.classe_treinamento = parClasse_treinamento 
      self.classe_teste = parClasse_teste
      self.history=[]

    def EvaluateServerModel(self):
      print ("Modelo do Servidor avaliado")
    
    def GetModel(self):
        
        print ("A ser implementado no Cliente Concreto")

    def LoadTrainingDataSet(self, parFromFile=False):
        
        print ("A ser implementado no Cliente Concreto")

    def RefreshModel(self, parFromTraining=False): #Constroi na primeira vez e atualiza, a partir da avaliação do servidor cetral
        print("A ser implementado no cliente concreto")

    def SetSplitedData(self, parPrevisores_treinamento,
                       parPrevisores_teste,
                       parClasse_teste,
                       parClasse_treinamento):
        self.previsores_treinamento=parPrevisores_treinamento
        self.previsores_teste = parPrevisores_teste 
        self.classe_treinamento = parClasse_treinamento 
        self.classe_teste = parClasse_teste

    def GetMapedMatrix(self):
        
        print("A ser implementado no Cliente Concreto")

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
        
        print("A ser implementado no Cliente concreto") 

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
    def GetHistory(self, parTitleValidationGraph, parTitleLossGraph,parModel):
        
        '''
        https://neptune.ai/blog/keras-loss-functions

        Binary Classification
            Binary classification loss function comes into play when solving a problem involving just two classes. For example, when predicting fraud in credit card transactions, a transaction is either fraudulent or not. 
            
            Binary Cross Entropy
            The Binary Cross entropy will calculate the cross-entropy loss between the predicted classes and the true classes. By default, the sum_over_batch_size reduction is used. This means that the loss will return the average of the per-sample losses in the batch.
            
            y_true = [[0., 1.], [0.2, 0.8],[0.3, 0.7],[0.4, 0.6]]
            y_pred = [[0.6, 0.4], [0.4, 0.6],[0.6, 0.4],[0.8, 0.2]]
            bce = tf.keras.losses.BinaryCrossentropy(reduction='sum_over_batch_size')
            bce(y_true, y_pred).numpy()
            The sum reduction means that the loss function will return the sum of the per-sample losses in the batch.
            
            bce = tf.keras.losses.BinaryCrossentropy(reduction='sum')
            bce(y_true, y_pred).numpy()
            Using the reduction as none returns the full array of the per-sample losses.
            
            bce = tf.keras.losses.BinaryCrossentropy(reduction='none')
            bce(y_true, y_pred).numpy()
            array([0.9162905 , 0.5919184 , 0.79465103, 1.0549198 ], dtype=float32)
            In binary classification, the activation function used is the sigmoid activation function. It constrains the output to a number between 0 and 1. 
        '''
        
        #print(self.history.history.keys())
        mrs.MyPrint(['Parametros de historico'], [self.history.history.keys()],parSameLine=False)
        plt.plot(self.history.history['binary_accuracy'])
        plt.plot(self.history.history['val_binary_accuracy'])
        plt.title(parTitleValidationGraph)
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.legend(['Train','Test'])
        plt.savefig(self.experimentPath+'/accuracy_'+parModel+'.png')
        plt.show()
        
        plt.plot(self.history.history['loss'])
        plt.plot(self.history.history['val_loss'])
        plt.title(parTitleLossGraph)
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.legend(['Train','Test'])
        plt.savefig(self.experimentPath+'/loss_'+parModel+'.png')
        plt.show()

    def GetPrevision(self): #evalueta indica que é uma avaliação do modelo recebido como parametro, no caso do servidor
        print("A ser implementada na classe concreta") 
       
    def SaveModel(self, parModel):
    
        classificador = self.GetModel()        
        classificador.set_weights(self.weightsClientModel)
        
        classificador_json = classificador.to_json()
        with open(self.experimentPath+"/model_"+parModel+".json",'w') as json_file:
            json_file.write(classificador_json)
        classificador.save_weights(self.experimentPath+"/model_weights_"+parModel+".h5")
        from keras2cpp import export_model
        export_model(classificador, self.experimentPath+"/example_"+parModel+".model")
        
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
    
    
    def AderenciaOutrosFluxos(self):
 
        print("A ser implementado na classe concreta")