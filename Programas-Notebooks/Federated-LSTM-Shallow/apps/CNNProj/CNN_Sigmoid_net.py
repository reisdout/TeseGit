
from GeneralClient import Client  
from GeneralFromRouterCNN_Sigmoid_Client import ClientBufferArrivaCNN
import os





       
    



def TreinarModelo(parExpDirPath, parBasePath):
    
    client01 = Client(0,parExpDirPath,parBasePath)    


    
    client01.RefreshModel(True)
    client01.GetMapedMatrix()    
    client01.SaveModel()

    '''
    classificador_json = classificador.to_json()
    with open(parExpDirPath+"/model.json",'w') as json_file:
        json_file.write(classificador_json)
    classificador.save_weights(parExpDirPath+"/model_weights.h5")
    from keras2cpp import export_model
    export_model(classificador, parExpDirPath+"/example.model")
    '''

#TreinarModelo('./Exp_0000034','./Exp_0000034/1Mono-4NewReno-noventacincocentesimos-seisdecimos-40-70-3h30min.csv')

#TreinarModelo('./Exp_0000037','./Exp_0000037/05fl-10h-95_60-compatibilizado.csv')


'''
 parExpDirPath -> Onde se salva o modelo, no caso de treinamento, ou de onde 
 se carega os pesos no sado de aderencia
'''

def TreinarModeloBufferArrival(parExpDirPath, parBasePath,parLstBasesTerminalsPaths, parLstBasesRoutersPaths):
    
    client01 = ClientBufferArrivaCNN(0,parExpDirPath,parBasePath,parLstBasesTerminalsPaths, parLstBasesRoutersPaths,parFeaturesWindow=3)    
    client01.RefreshModel(True)
    client01.GetMapedMatrix()
    

   


    #previsores_treinamento = pd.read_csv('./SQ-false-positive-filering-ML/input/x_train.csv')
    #classe_treinamento = pd.read_csv('./SQ-false-positive-filering-ML/input/y_train.csv')

    client01.SaveModel()

    '''
    classificador_json = classificador.to_json()
    with open(parExpDirPath+"/model.json",'w') as json_file:
        json_file.write(classificador_json)
    classificador.save_weights(parExpDirPath+"/model_weights.h5")
    from keras2cpp import export_model
    export_model(classificador, parExpDirPath+"/example.model")
    
    '''

def EvalueteModelLevarage(parExpDirPath, parBasePath,parLstBasesTerminalsPaths, parLstBasesRoutersPaths):
    
    #client01 = Client(0,parExpDirPath,parBasePath)
    client01 = ClientBufferArrivaCNN(0,parExpDirPath,parBasePath,parLstBasesTerminalsPaths, parLstBasesRoutersPaths)
    client01.AderenciaOutrosFluxos()


#TreinarModelo('./Exp_0000034','./Exp_0000034/1Mono-4NewReno-noventacincocentesimos-seisdecimos-40-70-3h30min.csv')

#TreinarModelo('./Exp_0000037','./Exp_0000037/05fl-10h-95_60-compatibilizado.csv')


"""
As listas abaixo devem estar "casadas, ou seja,
a posição i das listas deve ter, respectivamente,
 as leituras da chegada dos ack nos terminais
e a da chegada do segmento no roteador, a fim de
se fazer o mege posterior.


"""

experimentDataPath = '../../Exp_0000055'

files = os.listdir(experimentDataPath)

lstTermianlsPath=[]
lstRouterPath=[]
    
    
#files.sort()
#print (files)
input()

for file in files:
    
    if 'terminal' in  file:
        #print("Adicionando aos Terminais", file)
        lstTermianlsPath.append(os.path.join(experimentDataPath, file))

        
    elif "router" in file:
        #print("Adicionando aos roteadores", file)
        lstRouterPath.append(os.path.join(experimentDataPath, file))
 
        
    else:
        print(file, " --> nao Adicionado");
    
    
'''
lstTermianlsPath=['../../Exp_0000050/terminal01.csv',
                  '../../Exp_0000050/terminal02.csv',
                  '../../Exp_0000050/terminal03.csv',
                  '../../Exp_0000050/terminal04.csv',
                  '../../Exp_0000050/terminal05.csv',
                  '../../Exp_0000050/terminal06.csv',
                  '../../Exp_0000050/terminal07.csv',
                  '../../Exp_0000050/terminal08.csv',
                  '../../Exp_0000050/terminal09.csv',
                  '../../Exp_0000050/terminal10.csv']


                  '../../Exp_0000050/terminal11.csv',
                  '../../Exp_0000050/terminal12.csv',
                  '../../Exp_0000050/terminal13.csv',
                  '../../Exp_0000050/terminal14.csv',
                  '../../Exp_0000050/terminal15.csv',
                  '../../Exp_0000050/terminal16.csv',
                  '../../Exp_0000050/terminal17.csv',
                  '../../Exp_0000050/terminal18.csv',
                  '../../Exp_0000050/terminal19.csv',
                  '../../Exp_0000050/terminal20.csv']

                  '../../Exp_0000039/terminal03.csv',
                  '../../Exp_0000039/terminal04.csv',
                  '../../Exp_0000039/terminal05.csv',
                  '../../Exp_0000039/terminal06.csv',
                  '../../Exp_0000039/terminal07.csv',
                  '../../Exp_0000039/terminal08.csv',
                  '../../Exp_0000039/terminal09.csv',
                  '../../Exp_0000039/terminal10.csv',
                  '../../Exp_0000039/terminal11.csv',
                  '../../Exp_0000039/terminal12.csv',
                  '../../Exp_0000039/terminal13.csv',
                  '../../Exp_0000039/terminal14.csv',
                  '../../Exp_0000039/terminal15.csv',
                  '../../Exp_0000039/terminal16.csv']




lstRouterPath=['../../Exp_0000050/router01.csv',
               '../../Exp_0000050/router02.csv' ,
               '../../Exp_0000050/router03.csv',
               '../../Exp_0000050/router04.csv',
               '../../Exp_0000050/router05.csv',
               '../../Exp_0000050/router06.csv',
               '../../Exp_0000050/router07.csv',
               '../../Exp_0000050/router08.csv',
               '../../Exp_0000050/router09.csv',
               '../../Exp_0000050/router10.csv']

             
                            
               '../../Exp_0000050/router11.csv',
               '../../Exp_0000050/router12.csv',
               '../../Exp_0000050/router13.csv',
               '../../Exp_0000050/router14.csv',
               '../../Exp_0000050/router15.csv',
               '../../Exp_0000050/router16.csv',
               '../../Exp_0000050/router17.csv',
               '../../Exp_0000050/router18.csv',
               '../../Exp_0000050/router19.csv',
               '../../Exp_0000050/router20.csv']
               ,
               '../../Exp_0000039/router03.csv',
               '../../Exp_0000039/router04.csv',
               '../../Exp_0000039/router05.csv',
               '../../Exp_0000039/router06.csv',
               '../../Exp_0000039/router07.csv',
               '../../Exp_0000039/router08.csv',
               '../../Exp_0000039/router09.csv',
               '../../Exp_0000039/router10.csv',
               '../../Exp_0000039/router11.csv',
               '../../Exp_0000039/router12.csv',
               '../../Exp_0000039/router13.csv',
               '../../Exp_0000039/router14.csv',
               '../../Exp_0000039/router15.csv',
               '../../Exp_0000039/router16.csv']

'''

TreinarModeloBufferArrival(experimentDataPath,'../../Exp_0000049/terminal00.csv', lstTermianlsPath,lstRouterPath)


#EvalueteModelLevarage('../../Exp_0000049','../../Exp_0000049/terminal00.csv', lstTermianlsPath,lstRouterPath)
