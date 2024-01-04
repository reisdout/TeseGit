#O nome e terminal, pois partir dele sao acionados os clientes

import os
import sys
sys.path.append('../mrsutils')
import MRSUtils as mrs

class Terminal():

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
      self.InicializarArquivoMatrizesConfusao()
    
    
    def InicializarArquivoMatrizesConfusao(self):
        if(os.path.isfile(self.modelPath+"/traincfs.csv")):
            return;
        with open(self.modelPath+"/traincfs.csv", "a") as f:
            f.write("Modelo, ")
            f.write("Fase, ")
            f.write("Fluxos, ")
            f.write("a00, ")
            f.write("a01, ")
            f.write("a10, ")
            f.write("a11\n")

 
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
                
    
    def GetNumFlows(self):
        
        if(not os.path.isfile(self.basePath+"/numFlows.txt")):
            print("Impossivel determinar numero de fluxos")
            return -1;
        
        #Esssa funçao vai depender do 
        
        if(not self.lstRouterPath or not self.lstTermianlsPath):
            return 0;
        
        file1 = open(self.basePath+"/numFlows.txt", "r")
        a = file1.readline()
        print (a)
        return int(a.strip())
        
     
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
            self.EvalueteModelLevarage()
    
    def SalvarMatrizesDeConfusao(self,parModelo, parFase, parFluxos, parMatrix):
        
        with open(self.modelPath+"/traincfs.csv", "a") as f:
            f.write(parModelo+", ")
            f.write(parFase+", ")
            f.write(parFluxos+", ")
            f.write(str(parMatrix[0,0])+", ")
            f.write(str(parMatrix[0,1])+", ")
            f.write(str(parMatrix[1,0])+", ")
            f.write(str(parMatrix[1,1])+"\n")

        
        