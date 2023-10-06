
from GeneralAckSoftmax_Client import Client  
from FromRouterSoftmax_Client import ClientBufferArrival





       
    



def TreinarModelo(parExpDirPath, parBasePath):
    
    client01 = Client(0,parExpDirPath,parBasePath)    


    
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

#TreinarModelo('./Exp_0000034','./Exp_0000034/1Mono-4NewReno-noventacincocentesimos-seisdecimos-40-70-3h30min.csv')

#TreinarModelo('./Exp_0000037','./Exp_0000037/05fl-10h-95_60-compatibilizado.csv')




def TreinarModeloBufferArrival(parExpDirPath, parBasePath,parLstBasesTerminalsPaths, parLstBasesRoutersPaths):
    
    client01 = ClientBufferArrival(0,parExpDirPath,parBasePath,parLstBasesTerminalsPaths, parLstBasesRoutersPaths)    
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

def EvalueteModelLevarage(parExpDirPath,
                          parBasePath):
    
    client01 = Client(0,parExpDirPath,parBasePath)
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


lstTermianlsPath=['../../Exp_0000040/terminal01.csv',
                  '../../Exp_0000040/terminal02.csv',
                  '../../Exp_0000040/terminal03.csv',
                  '../../Exp_0000040/terminal04.csv',
                  '../../Exp_0000040/terminal05.csv',
                  '../../Exp_0000040/terminal06.csv',
                  '../../Exp_0000040/terminal07.csv',
                  '../../Exp_0000040/terminal08.csv']
'''
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


'''

lstRouterPath=['../../Exp_0000040/router01.csv',
               '../../Exp_0000040/router02.csv' ,
               '../../Exp_0000040/router03.csv',
               '../../Exp_0000040/router04.csv',
               '../../Exp_0000040/router05.csv',
               '../../Exp_0000040/router06.csv',
               '../../Exp_0000040/router07.csv',
               '../../Exp_0000040/router08.csv']
'''               
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

TreinarModeloBufferArrival('../../Exp_0000038','../../Exp_0000038/terminal00.csv', lstTermianlsPath,lstRouterPath)



