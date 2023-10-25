import sys
from GeneralClient import Client  
from GeneralFromRouterCNN_Sigmoid_Client import ClientBufferArrivaCNN
import os
import os
sys.path.append('../mrsutils')
import MRSUtils as mrs

basePath = "../../Exp_0000055" #Para se montar a lista com os arquivos da base. No caso de treinameno, geralmente e a mesma do experiment path

experimentPath = "../../Exp_0000055"  #Diretorio do experimento. Tem a conotaçao de registrar as saidas do experimento (graficos, por exemplo)

#experimentPath = Exp_0000056_AderenciaMLP_05_Fluxos

modelPath =  "../../Exp_0000055" #De onde se deve carregar um modelo em caso de aderencia. No caso de treinamento, pode ser o experimentPath, uma vez que nao carrega modelo algum



def TreinarModeloBufferArrival(parExpDirPath, parModelPath,parLstBasesTerminalsPaths, parLstBasesRoutersPaths):
    
    client01 = ClientBufferArrivaCNN(0,parExpDirPath,parModelPath,parLstBasesTerminalsPaths, parLstBasesRoutersPaths,parFeaturesWindow=3)    
    client01.RefreshModel(True)
    client01.GetHistory(parTitleValidationGraph='CNN Model Accuracy', parTitleLossGraph='CNN Model Loss',parModel="CNN")
    client01.GetMapedMatrix()
    client01.SaveModel('CNN')

def EvalueteModelLevarage(parExpDirPath, parModelPath,parLstBasesTerminalsPaths, parLstBasesRoutersPaths):
    
    #client01 = Client(0,parExpDirPath,parBasePath)
    client01 = ClientBufferArrivaCNN(0,parExpDirPath,parModelPath,parLstBasesTerminalsPaths, parLstBasesRoutersPaths)
    client01.AderenciaOutrosFluxos()





files = os.listdir(basePath)

lstTermianlsPath=[]
lstRouterPath=[]
    
    
files.sort()
#print (files)
#input()

for file in files:
    
    if 'terminal' in  file:
        #print("Adicionando aos Terminais", file)
        lstTermianlsPath.append(os.path.join(basePath, file))

        
    elif "router" in file:
        #print("Adicionando aos roteadores", file)
        lstRouterPath.append(os.path.join(basePath, file))
 
        
    else:
        mrs.MyPrint([file], ['Nao adicionado'])
    

TreinarModeloBufferArrival(experimentPath,experimentPath, lstTermianlsPath,lstRouterPath)

#EvalueteModelLevarage(experimentPath,modelPath, lstTermianlsPath,lstRouterPath)
