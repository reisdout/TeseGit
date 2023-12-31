#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 09:45:00 2023

@author: ns
"""

import sys
#from GeneralClient import Client  
from LSTMModule import LSTMModule
from Terminal import Terminal
sys.path.append('../mrsutils')
import MRSUtils as mrs
    

class LSTMTerminal(Terminal):
    
    def __init__(self,
                 parBasePath,
                 parExpDirPath,
                 parModelPath,
                 parTreino=True,
                 parLstTrainFeatures=[1,2,3]):
           
  
        super().__init__(parBasePath,parExpDirPath,parModelPath,parTreino,parLstTrainFeatures=parLstTrainFeatures)

        
        
        
    def TreinarModeloBufferArrival(self):
        
        client01 = LSTMModule(0,self.basePath,self.modelPath,self.lstTermianlsPath, self.lstRouterPath,self.lstTrainFeatures,parFeaturesWindow=3)    
        client01.RefreshModel(True)
        client01.GetHistory('LSTM Model Accuracy ('+self.PrepareHistoryTitle()+')', 'LSTM Model Loss '+'('+self.PrepareHistoryTitle()+')','LSTM')
        matrix = client01.GetMapedMatrix()        
        title = "ROC LSTM Treino - Dados {} Fluxos\n".format(len(self.lstTermianlsPath))+'({})'.format(self.PrepareHistoryTitle())
        
        mrs.ConstructROCGraph([matrix], ["LSTM"],title)
        client01.SaveModel("LSTM_"+self.PrepareHistoryTitle().replace(", ","_"))
        self.SalvarMatrizesDeConfusao("LSTM_"+self.PrepareHistoryTitle().replace(", ","_"),"Treino", "20",matrix)
    
    def EvalueteModelLevarage(self):
        
        #client01 = Client(0,parExpDirPath,parBasePath)
        client01 = LSTMModule(0,self.experimentPath,self.modelPath,self.lstTermianlsPath, self.lstRouterPath,parClienteLSTMLstFeatues=self.lstTrainFeatures, parFeaturesWindow=3)
        matrix = client01.AderenciaOutrosFluxos('LSTM_'+self.PrepareHistoryTitle().replace(", ","_"))
        title = "ROC LSTM Generalizaçao - Dados {:.0f} Fluxos\n".format(len(self.lstTermianlsPath))+'({})'.format(self.PrepareHistoryTitle())
        mrs.ConstructROCGraph([matrix], ["LSTM"],title)
        self.SalvarMatrizesDeConfusao("LSTM_"+self.PrepareHistoryTitle().replace(", ","_"),"Aderencia", str(len(self.lstTermianlsPath)),matrix)
