
from MLPTerminal import MLPTerminal

treino = True

if(treino == True):
    #Para Treinamento
    '''
    basePath = "../../Exp_0000055" #Para se montar a lista com os arquivos da base. No caso de treinameno, geralmente e a mesma do experiment path
    experimentPath = "../../Exp_0000055"  #Diretorio do experimento. Tem a conotaçao de registrar as saidas do experimento (graficos, por exemplo)
    modelPath =  "../../Exp_0000055" #De onde se deve carregar um modelo em caso de aderencia. No caso de treinamento, pode ser o experimentPath, uma vez que nao carrega modelo algum
    '''
    basePath = "../../Round_0000001/Train_Test" #Para se montar a lista com os arquivos da base. No caso de treinameno, geralmente e a mesma do experiment path
    experimentPath = "../../Round_0000001/Train_Test"  #Diretorio do experimento. Tem a conotaçao de registrar as saidas do experimento (graficos, por exemplo)
    modelPath =  "../../Round_0000001/Train_Test" #De onde se deve carregar um modelo em caso de aderencia. No caso de treinamento, pode ser o experimentPath, uma vez que nao carrega modelo algum



else:
    #Para aderencia
    
    basePath = '../../Exp_0000075_40F_Vegas' #Para se montar a lista com os arquivos da base. No caso de treinameno, geralmente e a mesma do experiment path
    experimentPath = '../../Exp_0000075_40F_Vegas'  #Diretorio do experimento. Tem a conotaçao de registrar as saidas do experimento (graficos, por exemplo)
    modelPath =  "../../Exp_0000055" #De onde se deve carregar um modelo em caso de aderencia. No caso de treinamento, pode ser o experimentPath, uma vez que nao carrega modelo algum


objTerminal = MLPTerminal(basePath, experimentPath, modelPath, parTreino=treino,parLstTrainFeatures=[1,2,3])
objTerminal.RunClient()