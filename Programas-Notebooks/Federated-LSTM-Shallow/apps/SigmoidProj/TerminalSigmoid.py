import sys
sys.path.append('..')
#from GeneralClient import Client  
from FromRouterSigmoid_Client import ClientBufferArrivalSigmoid
from GeneralTerminal import GeneralTerminal




class TerminalSigmoid(GeneralTerminal):
    
    def __init__(self, 
                 parTreino,
                 parLstTrainFeatures = [1,2,3]):
           
  
        super().__init__(parTreino,parLstTrainFeatures=parLstTrainFeatures)


    
    
    
    def TreinarModeloBufferArrival(self,parExperimentPath, parModelPath,parLstBasesTerminalsPaths, parLstBasesRoutersPaths):
        
        
        
       
        
        client01 = ClientBufferArrivalSigmoid(0,parExperimentPath,parModelPath,parLstBasesTerminalsPaths, parLstBasesRoutersPaths,self.lstTrainFeatures)    
        client01.RefreshModel(True)
        client01.GetHistory('MLP Model Accuracy ('+self.PrepareHistoryTitle()+')','MLP Model Loss '+'('+self.PrepareHistoryTitle()+')','MLP')
        client01.GetMapedMatrix()
        client01.SaveModel("MLP")
    
        '''
        classificador_json = classificador.to_json()
        with open(parExpDirPath+"/model.json",'w') as json_file:
            json_file.write(classificador_json)
        classificador.save_weights(parExpDirPath+"/model_weights.h5")
        from keras2cpp import export_model
        export_model(classificador, parExpDirPath+"/example.model")
        
        '''
    
    def EvalueteModelLevarage(parBasePath, parModelPath,parLstBasesTerminalsPaths, parLstBasesRoutersPaths):
        
        #client01 = Client(0,parExpDirPath,parBasePath)
        client01 = ClientBufferArrivalSigmoid(0,parBasePath,parModelPath,parLstBasesTerminalsPaths, parLstBasesRoutersPaths)
        client01.AderenciaOutrosFluxos("MLP")
        
        
