# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 21:37:56 2023

@author: visitante

Esta classe visa validar se as previsões no python e no cpp são as mesmas


"""

import pandas as pd
from sklearn.model_selection import train_test_split
#import keras
#from keras.models import Sequential
#from keras.layers import Dense, Dropout, LSTM#, Bidirectional
#from sklearn.metrics import confusion_matrix, accuracy_score
#from sklearn.metrics import confusion_matrix #, classification_report, 
from keras.utils import np_utils
import numpy as np
#from sys import exit
#from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
#from sklearn.preprocessing import normalize
import seaborn as sns; sns.set()
import sys
sys.path.append('../mrsutils')
import MRSUtils as mrs 



class Validador():

    #resultadoTreinamento = np.eye(10)

    def __init__(self,parModelPath,parConfrontDataPath):
        
        self.modelPath = parModelPath;
        self.confrontDataPath = parConfrontDataPath;
      
        '''  
        
        
        #self.id=parId
        #elf.basePath=parBasePath
        #self.experimentPath = parExperimentPath
        #self.testPath = parTestPath
        #self.T = parPrevisionWindow
        #centralServer = Server_FederatedAMA()
        #confusionMatrizModelClient = np.full((2,2), 1)
        #confusionMatrizModelServer = np.full((2,2), 2)
        #self.currentConfusionMatriz =np.full((2,2), 0)
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
        '''


    def LoadTrainingDataSet(self, parFromFile=True): #True, pois, a princípio já vem de um experimento base
        
        base = pd.read_csv(self.basePath)
        
        base = base.drop_duplicates(subset=['ack_ewma(ms)', 'send_ewma(ms)','rtt_ratio'])
        
        
        #print (base.shape[0])
        #input("Eis a quantidade de entradas")

        base = mrs.NormalizeFeatures(base,parFromFile,self.modelPath)
        #previsores = base.iloc[:, [1,2,3,4]].values #com cwnd
        previsores = base.iloc[:, [1,2,3]].values #sem cwnd

        print(previsores[10])

        print(previsores[20])

        print(previsores[30])

        print("================SEM NORMALIZAÇÃO================================")

        

        #previsores=normalize(previsores)

        print(previsores[10])

        print(previsores[20])

        print(previsores[30])
        
        classe = base.iloc[:, 14].values
       
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
        
        #return previsores_treinamento, previsores_teste, classe_treinamento, classe_teste
        return base, classe_dummy
    


    def Confrontar(self):
 
        #previsores_treinamento, previsores_teste, classe_treinamento, classe_teste = self.LoadTrainingDataSet(parFromFile=True)
        base, classe_teste = self.LoadTrainingDataSet(parFromFile=True)
        arquivo = open(self.modelPath+"/model.json",'r')
        estrutura_classificador = arquivo.read()
        arquivo.close()
        from keras.models import model_from_json
        classificador = model_from_json(estrutura_classificador)
        classificador.load_weights(self.modelPath+"/model_weights.h5")

        classificador.compile(optimizer = 'adam', loss = 'categorical_crossentropy',
                          metrics = ['categorical_accuracy'])


        #resultado = classificador.evaluate(base, classe_teste)
        previsoes = classificador.predict(base)
        previsoes = (previsoes > 0.5)
        classe_teste2 = [np.argmax(t) for t in classe_teste]
        previsoes2 = [np.argmax(t) for t in previsoes]

        from sklearn.metrics import confusion_matrix
        matriz = confusion_matrix(previsoes2, classe_teste2)
        print(matriz)
        to_heat_map =[[matriz[0,0],matriz[0,1]],[matriz[1,0],matriz[1,1]]]
        to_heat_map = pd.DataFrame(to_heat_map, index = ["Hit","Fail"],columns = ["Fail","Hit"])
        ax = sns.heatmap(to_heat_map,annot=True, fmt="d")
        
        
def ValidarKeras2Cpp():
    
    objValidador = Validador("./","./10_0_0_2to10_1_0_2_L_Fri Sep 29 21_27_55.csv")
    objValidador.Confrontar()
