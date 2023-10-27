import sys
#from GeneralClient import Client  
from GeneralFromRouterLSTM_Sigmoid_Client import ClientBufferArrivalLSTM
import os
sys.path.append('../mrsutils')
import MRSUtils as mrs
    
treino = True


if(treino == True):
    #Para Treinamento
    
    basePath = "../../Exp_0000055" #Para se montar a lista com os arquivos da base. No caso de treinameno, geralmente e a mesma do experiment path
    experimentPath = "../../Exp_0000055"  #Diretorio do experimento. Tem a conotaçao de registrar as saidas do experimento (graficos, por exemplo)
    modelPath =  "../../Exp_0000055" #De onde se deve carregar um modelo em caso de aderencia. No caso de treinamento, pode ser o experimentPath, uma vez que nao carrega modelo algum



else:
    #Para aderencia
    
    basePath = '../../Exp_0000056_Aderencia_05_Fluxos' #Para se montar a lista com os arquivos da base. No caso de treinameno, geralmente e a mesma do experiment path
    experimentPath = '../../Exp_0000056_Aderencia_05_Fluxos'  #Diretorio do experimento. Tem a conotaçao de registrar as saidas do experimento (graficos, por exemplo)
    modelPath =  "../../Exp_0000055" #De onde se deve carregar um modelo em caso de aderencia. No caso de treinamento, pode ser o experimentPath, uma vez que nao carrega modelo algum



def TreinarModeloBufferArrival(parExpDirPath, parModelPath,parLstBasesTerminalsPaths, parLstBasesRoutersPaths):
    
    client01 = ClientBufferArrivalLSTM(0,parExpDirPath,parModelPath,parLstBasesTerminalsPaths, parLstBasesRoutersPaths,parFeaturesWindow=3)    
    client01.RefreshModel(True)
    client01.GetHistory('LSTM Model Accuracy', 'LSTM Model Loss','LSTM')
    matrix = client01.GetMapedMatrix()
    client01.SaveModel("LSTM")
    mrs.ConstructROCGraph([matrix], ["LSTM"])


def EvalueteModelLevarage(parExpDirPath, parBasePath,parLstBasesTerminalsPaths, parLstBasesRoutersPaths):
    
    #client01 = Client(0,parExpDirPath,parBasePath)
    client01 = ClientBufferArrivalLSTM(0,parExpDirPath,parBasePath,parLstBasesTerminalsPaths, parLstBasesRoutersPaths,parFeaturesWindow=3)
    client01.AderenciaOutrosFluxos('LSTM')



files = os.listdir(basePath)

lstTermianlsPath=[]
lstRouterPath=[]
    
    
files.sort()
#print (files)
#input()

for file in files:
    
    if 'terminal' in  file:
        mrs.MyPrint(["Adicionando aos Terminais"], [' '])
        lstTermianlsPath.append(os.path.join(basePath, file))

        
    elif "router" in file:
        mrs.MyPrint(["Adicionando aos roteadores"], [' '])
        lstRouterPath.append(os.path.join(basePath, file))

        
    else:
        mrs.MyPrint([file], ['Nao adicionado'])
        
        
    
#no "TreinarModeloBufferArrival", o modelPath e onde se salva o modelo, que no caso do treinamento e o mesmo do experimentPath
if(treino):
    TreinarModeloBufferArrival(experimentPath,experimentPath, lstTermianlsPath,lstRouterPath)


#no "EvalueteModelLevarage", o modelPath e de onde se carrega o modelo cuja aderencia deve ser avaliada.
else:
    EvalueteModelLevarage(basePath,modelPath, lstTermianlsPath,lstRouterPath)
