#O nome e terminal, pois partir dele sao acionados os clientes

import os
import sys
sys.path.append('../mrsutils')
import MRSUtils as mrs

class GeneralTerminal():

    #resultadoTreinamento = np.eye(10)

    def __init__(self,
                 parBasePath,
                 parExperimentPath,
                 parModelPath,
                 parTreino = True,
                 parLstTrainFeatures=[1,2,3]):
    
        
      self.lstFeatures_Names = ['#', "ACK_ewma", "Send_ewma","RTT_ratio"]#Replica o cabeçlho do csv
      self.treino = parTreino
      self.lstTermianlsPath=[]
      self.lstRouterPath=[]      
      '''
      Observe que os terminais tem os tres caminhos, pois precisam sempre do base_path para carregar o caminho dos arquivos.
      Os clientes ja nao precisam receber o base_path, pois ja recebem o caminho da base de trinamento dos terminais, por isso
      na instanciçao dos clientes, pasasa-se o experiment_path e nao base_path.
      Lembrando que po model_path so faz real sentido quando da avaliaçao do treinamento, quando deve ser necessariamente diferente de 
      experimentPath.
      '''
      self.basePath = parBasePath
      self.experimentPath = parExperimentPath
      self.modelPath = parModelPath
      self.lstTrainFeatures = parLstTrainFeatures
      
 
    def GetCvsPathFiles(self):   
    
        files = os.listdir(self.basePath)            
        files.sort()
        #print (files)
        #input()
        
        for file in files:
            
            if 'terminal' in  file:
                mrs.MyPrint(["Adicionando aos Terminais"], [' '])
                self.lstTermianlsPath.append(os.path.join(self.basePath, file))
        
                
            elif "router" in file:
                mrs.MyPrint(["Adicionando aos roteadores"], [' '])
                self.lstRouterPath.append(os.path.join(self.basePath, file))
        
                
            else:
                mrs.MyPrint([file], ['Nao adicionado'])
                
                
    def PrepareHistoryTitle(self):
        
        title = ''
        
        for t in range (len(self.lstTrainFeatures)):
            title = title +self.lstFeatures_Names[self.lstTrainFeatures[t]] 
            if(t < len(self.lstTrainFeatures) -1):
                title = title+', '
        return title
        


    def RunClient(self):
        
        self.GetCvsPathFiles()
        #no "TreinarModeloBufferArrival", o modelPath e onde se salva o modelo, que no caso do treinamento e o mesmo do experimentPath
        if(self.treino):
            self.TreinarModeloBufferArrival()
        
        
        #no "EvalueteModelLevarage", o modelPath e de onde se carrega o modelo cuja aderencia deve ser avaliada.
        else:
            self.EvalueteModelLevarage(self.basePath, self.modelPath, self.lstTermianlsPath,self.lstRouterPath)
