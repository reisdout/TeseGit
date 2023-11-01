#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 09:45:00 2023

@author: ns
"""

import sys
#from GeneralClient import Client  
from GeneralFromRouterLSTM_Sigmoid_Client import ClientBufferArrivalLSTM
from GeneralTerminal import GeneralTerminal
sys.path.append('../mrsutils')
import MRSUtils as mrs
    

class TerminalLSTM(GeneralTerminal):
    
    def __init__(self, 
                 parTreino,
                 parLstTrainFeatures=[1,2,3]):
           
  
        super().__init__(parTreino,parLstTrainFeatures=parLstTrainFeatures)

        
        
        
    def TreinarModeloBufferArrival(self, parExpDirPath, parModelPath,parLstBasesTerminalsPaths, parLstBasesRoutersPaths):
        
        client01 = ClientBufferArrivalLSTM(0,parExpDirPath,parModelPath,parLstBasesTerminalsPaths, parLstBasesRoutersPaths,parFeaturesWindow=3,parLstFeatues=[1,2,3])    
        client01.RefreshModel(True)
        client01.GetHistory('LSTM Model Accuracy ('+self.PrepareHistoryTitle()+')', 'LSTM Model Loss '+'('+self.PrepareHistoryTitle()+')','LSTM')
        matrix = client01.GetMapedMatrix()
        client01.SaveModel("LSTM")
        mrs.ConstructROCGraph([matrix], ["LSTM"])
    
    
    def EvalueteModelLevarage(self, parExpDirPath, parBasePath,parLstBasesTerminalsPaths, parLstBasesRoutersPaths):
        
        #client01 = Client(0,parExpDirPath,parBasePath)
        client01 = ClientBufferArrivalLSTM(0,parExpDirPath,parBasePath,parLstBasesTerminalsPaths, parLstBasesRoutersPaths,parFeaturesWindow=3)
        client01.AderenciaOutrosFluxos('LSTM')
        