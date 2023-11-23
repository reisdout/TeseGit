from TerminalCNN import TerminalCNN



treino = False

if(treino == True):
    #Para Treinamento
    
    basePath = "../../Exp_0000055" #Para se montar a lista com os arquivos da base. No caso de treinameno, geralmente e a mesma do experiment path
    experimentPath = "../../Exp_0000055"  #Diretorio do experimento. Tem a conotaçao de registrar as saidas do experimento (graficos, por exemplo)
    modelPath =  "../../Exp_0000055" #De onde se deve carregar um modelo em caso de aderencia. No caso de treinamento, pode ser o experimentPath, uma vez que nao carrega modelo algum



else:
    #Para aderencia
    
    #basePath = '../../Exp_0000056_Aderencia_05_Fluxos' #Para se montar a lista com os arquivos da base. No caso de treinameno, geralmente e a mesma do experiment path
    #experimentPath = '../../Exp_0000056_Aderencia_05_Fluxos'  #Diretorio do experimento. Tem a conotaçao de registrar as saidas do experimento (graficos, por exemplo)
    #modelPath =  "../../Exp_0000055" #De onde se deve carregar um modelo em caso de aderencia. No caso de treinamento, pode ser o experimentPath, uma vez que nao carrega modelo algum

    basePath = '../../Exp_0000063_05F_BBR' #Para se montar a lista com os arquivos da base. No caso de treinameno, geralmente e a mesma do experiment path
    experimentPath = '../../Exp_0000063_05F_BBR'  #Diretorio do experimento. Tem a conotaçao de registrar as saidas do experimento (graficos, por exemplo)
    modelPath =  "../../Exp_0000055" #De onde se deve carregar um modelo em caso de aderencia. No caso de treinamento, pode ser o experimentPath, uma vez que nao carrega modelo algum



objTerminal = TerminalCNN(basePath, experimentPath, modelPath, parTreino=treino,parLstTrainFeatures=[1,2,3])
objTerminal.RunClient()