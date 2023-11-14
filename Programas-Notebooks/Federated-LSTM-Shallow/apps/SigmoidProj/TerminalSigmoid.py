import sys
sys.path.append('..')
#from GeneralClient import Client  
from FromRouterSigmoid_Client import ClientBufferArrivalSigmoid
from GeneralTerminal import GeneralTerminal
import MRSUtils as mrs




class TerminalSigmoid(GeneralTerminal):
    
    def __init__(self,                  
                 parBasePath,
                 parExperimentPath,
                 parModelPath,
                 parTreino=True,
                 parLstTrainFeatures = [1,2,3]):
           
  
        super().__init__(parBasePath,
                         parExperimentPath,
                         parModelPath,
                         parTreino,
                         parLstTrainFeatures)


    
    
    
    def TreinarModeloBufferArrival(self):
        
        client01 = ClientBufferArrivalSigmoid(0,self.basePath,self.modelPath,self.lstTermianlsPath, self.lstRouterPath,self.lstTrainFeatures)    
        client01.RefreshModel(True)
        client01.GetHistory('MLP Model Accuracy ('+self.PrepareHistoryTitle()+')','MLP Model Loss '+'('+self.PrepareHistoryTitle()+')','MLP')
        matrix = client01.GetMapedMatrix()
        title = "ROC MLP Treino - Dados {} Fluxos\n".format(len(self.lstTermianlsPath))+'({})'.format(self.PrepareHistoryTitle())
        mrs.ConstructROCGraph([matrix], ["MLP"],title)
        client01.SaveModel("MLP_"+self.PrepareHistoryTitle())
    
        '''
        classificador_json = classificador.to_json()
        with open(parExpDirPath+"/model.json",'w') as json_file:
            json_file.write(classificador_json)
        classificador.save_weights(parExpDirPath+"/model_weights.h5")
        from keras2cpp import export_model
        export_model(classificador, parExpDirPath+"/example.model")
        
        '''
    
    def EvalueteModelLevarage(self):
        
        #client01 = Client(0,parExpDirPath,parBasePath)
        client01 = ClientBufferArrivalSigmoid(0,self.experimentPath,self.modelPath,self.lstTermianlsPath, self.lstRouterPath,parClienteMLPLstFeatues=self.lstTrainFeatures)
        matrix=client01.AderenciaOutrosFluxos("MLP_"+self.PrepareHistoryTitle())
        title = "ROC MLP Generalizaçao - Dados {:.0f} Fluxos\n".format(len(self.lstTermianlsPath)/2)+'({})'.format(self.PrepareHistoryTitle())
        mrs.ConstructROCGraph([matrix], ["MLP"],title)
        
        
