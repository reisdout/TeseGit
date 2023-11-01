import sys
#from GeneralClient import Client  
from GeneralFromRouterCNN_Sigmoid_Client import ClientBufferArrivalCNN 
from GeneralTerminal import GeneralTerminal
sys.path.append('../mrsutils')
import MRSUtils as mrs
    

class TerminalCNN(GeneralTerminal):
    
    def __init__(self, 
                 parBasePath,
                 parExpDirPath,
                 parModelPath,
                 parTreino=True,
                 parLstTrainFeatures=[1,2,3]):
           
  
        super().__init__(parBasePath,parExpDirPath,parModelPath,parTreino,parLstTrainFeatures=parLstTrainFeatures)

        



    def TreinarModeloBufferArrival(self):
        
        client01 = ClientBufferArrivalCNN(0,self.basePath,self.modelPath,self.lstTermianlsPath, self.lstRouterPath,self.lstTrainFeatures,parFeaturesWindow=3)    
        client01.RefreshModel(True)
        client01.GetHistory('CNN Model Accuracy ('+self.PrepareHistoryTitle()+')', 'CNN Model Loss '+'('+self.PrepareHistoryTitle()+')',parModel="CNN")
        matrix = client01.GetMapedMatrix()
        client01.SaveModel('CNN')
        mrs.ConstructROCGraph([matrix], ["CNN"])
    
    def EvalueteModelLevarage(self):
        
        #client01 = Client(0,parExpDirPath,parBasePath)
        client01 = ClientBufferArrivalCNN(0,self.experimentPath,self.modelPath,self.lstTermianlsPath, self.lstRouterPath,parLstFeatues=self.lstTrainFeatures, parFeaturesWindow=3)
        client01.AderenciaOutrosFluxos('CNN')
