import sys
#from GeneralClient import Client  
from GeneralFromRouterCNN_Sigmoid_Client import ClientBufferArrivaCNN 
from GeneralTerminal import GeneralTerminal
sys.path.append('../mrsutils')
import MRSUtils as mrs
    

class TerminalCNN(GeneralTerminal):
    
    def __init__(self, 
                 parTreino,
                 parLstTrainFeatures=[1,2,3]):
           
  
        super().__init__(parTreino,parLstTrainFeatures=parLstTrainFeatures)

        



    def TreinarModeloBufferArrival(self, parExpDirPath, parModelPath,parLstBasesTerminalsPaths, parLstBasesRoutersPaths):
        
        client01 = ClientBufferArrivaCNN(0,parExpDirPath,parModelPath,parLstBasesTerminalsPaths, parLstBasesRoutersPaths,parFeaturesWindow=3)    
        client01.RefreshModel(True)
        client01.GetHistory('CNN Model Accuracy ('+self.PrepareHistoryTitle()+')', 'CNN Model Loss '+'('+self.PrepareHistoryTitle()+')',parModel="CNN")
        matrix = client01.GetMapedMatrix()
        client01.SaveModel('CNN')
        mrs.ConstructROCGraph([matrix], ["CNN"])
    
    def EvalueteModelLevarage(parExpDirPath, parModelPath,parLstBasesTerminalsPaths, parLstBasesRoutersPaths):
        
        #client01 = Client(0,parExpDirPath,parBasePath)
        client01 = ClientBufferArrivaCNN(0,parExpDirPath,parModelPath,parLstBasesTerminalsPaths, parLstBasesRoutersPaths,parFeaturesWindow=3)
        client01.AderenciaOutrosFluxos('CNN')


objTerminal = TerminalCNN()(parTreino=True,parLstTrainFeatures=[1,3])
objTerminal.RunClient()