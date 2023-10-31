#O nome e terminal, pois partir dele sao acionados os clientes

import os
import sys
sys.path.append('../mrsutils')
import MRSUtils as mrs

class GeneralTerminal():

    #resultadoTreinamento = np.eye(10)

    def __init__(self,
                 parTreino = True,
                 parLstTrainFeatures=[1,2,3]):
    
        
      self.lstFeatures_Names = ['#', "ACK_ewma", "Send_ewma","RTT_ratio"]#Replica o cabeçlho do csv
      self.treino = parTreino
      self.lstTermianlsPath=[]
      self.lstRouterPath=[]            
      self.basePath = []
      self.experimentPath =[]
      self.modelPath = []
      self.lstTrainFeatures = parLstTrainFeatures
      if(self.treino == True):
          #Para Treinamento
          
          self.basePath = "../../Exp_0000055" #Para se montar a lista com os arquivos da base. No caso de treinameno, geralmente e a mesma do experiment path
          self.experimentPath = "../../Exp_0000055"  #Diretorio do experimento. Tem a conotaçao de registrar as saidas do experimento (graficos, por exemplo)
          self.modelPath =  "../../Exp_0000055" #De onde se deve carregar um modelo em caso de aderencia. No caso de treinamento, pode ser o experimentPath, uma vez que nao carrega modelo algum



      else:
          #Para aderencia
          
          self.basePath = '../../Exp_0000056_Aderencia_05_Fluxos' #Para se montar a lista com os arquivos da base. No caso de treinameno, geralmente e a mesma do experiment path
          self.experimentPath = '../../Exp_0000056_Aderencia_05_Fluxos'  #Diretorio do experimento. Tem a conotaçao de registrar as saidas do experimento (graficos, por exemplo)
          self.modelPath =  "../../Exp_0000055" #De onde se deve carregar um modelo em caso de aderencia. No caso de treinamento, pode ser o experimentPath, uma vez que nao carrega modelo algum

    def GetCvsFiles(self):   
    
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
        
        self.GetCvsFiles()
        #no "TreinarModeloBufferArrival", o modelPath e onde se salva o modelo, que no caso do treinamento e o mesmo do experimentPath
        if(self.treino):
            self.TreinarModeloBufferArrival(self.experimentPath,self.experimentPath, self.lstTermianlsPath,self.lstRouterPath)
        
        
        #no "EvalueteModelLevarage", o modelPath e de onde se carrega o modelo cuja aderencia deve ser avaliada.
        else:
            self.EvalueteModelLevarage(self.basePath, self.modelPath, self.lstTermianlsPath,self.lstRouterPath)
