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
        title = "ROC CNN Treino - Dados {} Fluxos\n".format(len(self.lstTermianlsPath))+'({})'.format(self.PrepareHistoryTitle())
        mrs.ConstructROCGraph([matrix], ["CNN"],title)
        client01.SaveModel("CNN_"+self.PrepareHistoryTitle().replace(", ","_"))
        
    
    def EvalueteModelLevarage(self):
        
        #client01 = Client(0,parExpDirPath,parBasePath)
        client01 = ClientBufferArrivalCNN(0,self.experimentPath,self.modelPath,self.lstTermianlsPath, self.lstRouterPath, parClineteCNNLstFeatues=self.lstTrainFeatures, parFeaturesWindow=3)
        matrix =client01.AderenciaOutrosFluxos('CNN_'+self.PrepareHistoryTitle().replace(", ","_"))
        title = "ROC CNN Generalizaçao - Dados {:.0f} Fluxos\n".format(len(self.lstTermianlsPath))+'({})'.format(self.PrepareHistoryTitle())
        mrs.ConstructROCGraph([matrix], ["CNN"],title)
